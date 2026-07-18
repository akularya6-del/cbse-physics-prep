import json
import sys
import numpy as np
import pandas as pd
from scipy.stats import chisquare, mannwhitneyu
from statsmodels.stats.weightstats import ztest
import pymannkendall as mk

def normalize(value, min_val, max_val):
    if max_val == min_val:
        return 50.0
    return ((value - min_val) / (max_val - min_val)) * 100.0

def calculate_statistical_metrics(topic_qs, all_qs):
    # Prepare data for testing
    # For a topic:
    # qs per year
    
    comp_qs = [q for q in topic_qs if q['paperType'] == 'Compartment']
    main_qs = [q for q in topic_qs if q['paperType'] == 'Main']
    
    # 1. Chi-Square (Compartment Bias)
    comp_count = len(comp_qs)
    main_count = len(main_qs)
    
    all_comp = len([q for q in all_qs if q['paperType'] == 'Compartment'])
    all_main = len([q for q in all_qs if q['paperType'] == 'Main'])
    
    chi_sq_result = "INSUFFICIENT_DATA"
    if comp_count + main_count > 1 and all_comp > 0 and all_main > 0:
        expected_comp = (comp_count + main_count) * (all_comp / (all_comp + all_main))
        expected_main = (comp_count + main_count) * (all_main / (all_comp + all_main))
        if expected_comp > 0 and expected_main > 0:
            try:
                stat, p = chisquare([comp_count, main_count], f_exp=[expected_comp, expected_main])
                chi_sq_result = {"statistic": float(stat), "p_value": float(p), "significant": bool(p < 0.05)}
            except:
                pass

    # 2. Mann-Whitney U (Marks Weightage)
    comp_marks = [q['marks'] for q in comp_qs if q['marks'] is not None]
    main_marks = [q['marks'] for q in main_qs if q['marks'] is not None]
    
    mwu_result = "INSUFFICIENT_DATA"
    if len(comp_marks) > 0 and len(main_marks) > 0:
        if len(set(comp_marks)) == 1 and len(set(main_marks)) == 1 and comp_marks[0] == main_marks[0]:
            pass # zero variance
        else:
            try:
                stat, p = mannwhitneyu(comp_marks, main_marks, alternative='two-sided')
                mwu_result = {"statistic": float(stat), "p_value": float(p), "significant": bool(p < 0.05)}
            except:
                pass
                
    # 3. Z-Test (Derivation Heavy)
    topic_deriv = [1 if q['hasDerivation'] else 0 for q in topic_qs]
    all_deriv = [1 if q['hasDerivation'] else 0 for q in all_qs]
    
    ztest_result = "INSUFFICIENT_DATA"
    if len(topic_deriv) > 1 and len(all_deriv) > 1:
        if len(set(topic_deriv)) <= 1 and len(set(all_deriv)) <= 1 and list(set(topic_deriv)) == list(set(all_deriv)):
            pass # zero variance
        else:
            try:
                stat, p = ztest(topic_deriv, all_deriv)
                ztest_result = {"statistic": float(stat), "p_value": float(p), "significant": bool(p < 0.05)}
            except:
                pass
                
    # 4. Mann-Kendall (Trend Analysis)
    years = sorted(list(set(q['year'] for q in all_qs)))
    if len(years) > 1:
        trend_data = []
        for y in years:
            y_qs = [q for q in topic_qs if q['year'] == y]
            trend_data.append(len(y_qs))
            
        mk_result = "INSUFFICIENT_DATA"
        try:
            res = mk.original_test(trend_data)
            mk_result = {
                "trend": res.trend,
                "p_value": float(res.p),
                "z_score": float(res.z),
                "significant": bool(res.p < 0.05)
            }
        except:
            pass
    else:
        mk_result = "INSUFFICIENT_DATA"
            
    return {
        "chiSquare": chi_sq_result,
        "mannWhitneyU": mwu_result,
        "zTest": ztest_result,
        "mannKendall": mk_result
    }

def main():
    try:
        with open('physics_questions_database.json', 'r') as f:
            db = json.load(f)
    except Exception as e:
        print(f"Error loading DB: {e}")
        sys.exit(1)
        
    try:
        with open('question_clusters.json', 'r') as f:
            clusters = json.load(f)
    except Exception as e:
        print(f"Error loading clusters: {e}")
        sys.exit(1)
        
    questions = [q for q in db.get("questions", []) if q.get("topicCode") != "00"]
    
    topics = {}
    for q in questions:
        code = q['topicCode']
        if code not in topics:
            topics[code] = []
        topics[code].append(q)
        
    raw_metrics = {}
    stat_results = {}
    
    # Calculate raw metrics and stats per topic
    for topic_code, topic_qs in topics.items():
        comp_qs = [q for q in topic_qs if q['paperType'] == 'Compartment']
        
        freq = len(topic_qs)
        comp_bias = len(comp_qs) / len(topic_qs) if len(topic_qs) > 0 else 0
        marks_arr = [q['marks'] for q in topic_qs if q['marks']]
        avg_marks = np.mean(marks_arr) if marks_arr else 0
        
        # Recency score
        current_year = max([q['year'] for q in questions]) if questions else 2024
        recency_weight = sum([1.0 / (current_year - q['year'] + 1) for q in topic_qs])
        
        deriv_ratio = sum([1 for q in topic_qs if q['hasDerivation']]) / len(topic_qs) if topic_qs else 0
        
        # Cluster density (avg cluster size)
        topic_clusters = [c for c in clusters if c['topicCode'] == topic_code]
        cluster_density = np.mean([c['variantCount'] for c in topic_clusters]) if topic_clusters else 1
        
        raw_metrics[topic_code] = {
            "frequency": freq,
            "compartmentBias": comp_bias,
            "averageMarks": avg_marks,
            "recencyWeight": recency_weight,
            "derivationRatio": deriv_ratio,
            "clusterDensity": cluster_density
        }
        
        stat_results[topic_code] = calculate_statistical_metrics(topic_qs, questions)
        
    # Find min/max for normalization
    normalized_metrics = {}
    priority_scores = {}
    
    for metric in ["frequency", "compartmentBias", "averageMarks", "recencyWeight", "derivationRatio", "clusterDensity"]:
        vals = [raw_metrics[tc][metric] for tc in raw_metrics]
        min_val = min(vals) if vals else 0
        max_val = max(vals) if vals else 0
        
        for tc in raw_metrics:
            if tc not in normalized_metrics:
                normalized_metrics[tc] = {}
            normalized_metrics[tc][metric] = normalize(raw_metrics[tc][metric], min_val, max_val)
            
    for tc in raw_metrics:
        # Composite score
        nm = normalized_metrics[tc]
        score = (nm['frequency'] * 0.25 +
                 nm['compartmentBias'] * 0.20 +
                 nm['averageMarks'] * 0.15 +
                 nm['recencyWeight'] * 0.15 +
                 nm['derivationRatio'] * 0.10 +
                 nm['clusterDensity'] * 0.15)
        priority_scores[tc] = round(score, 2)
        
    intelligence_db = {
        "topics": {}
    }
    
    for tc in raw_metrics:
        intelligence_db["topics"][tc] = {
            "topicName": topics[tc][0]['topicName'],
            "priorityScore": priority_scores[tc],
            "rawMetrics": raw_metrics[tc],
            "normalizedMetrics": normalized_metrics[tc],
            "statisticalTests": stat_results[tc]
        }
        
    with open("question_intelligence.json", "w") as f:
        json.dump(intelligence_db, f, indent=2)
        
    # Generate analysis_report.md
    report = ["# Statistical Analysis Report", ""]
    
    # Topic Rankings
    sorted_topics = sorted(priority_scores.items(), key=lambda x: x[1], reverse=True)
    report.append("## Topic Priority Rankings")
    report.append("| Rank | Topic | Composite Score |")
    report.append("|---|---|---|")
    for idx, (tc, score) in enumerate(sorted_topics):
        tname = topics[tc][0]['topicName']
        report.append(f"| {idx+1} | {tname} (Code: {tc}) | {score:.2f} |")
        
    report.append("")
    report.append("## Key Statistical Findings")
    # Identify significant things
    for tc, _ in sorted_topics:
        stats = stat_results[tc]
        tname = topics[tc][0]['topicName']
        findings = []
        if stats['chiSquare'] != "INSUFFICIENT_DATA" and stats['chiSquare'].get('significant'):
            findings.append("Significant Compartment Bias (Chi-Square p<0.05)")
        if stats['mannWhitneyU'] != "INSUFFICIENT_DATA" and stats['mannWhitneyU'].get('significant'):
            findings.append("Significant Marks Weightage Difference (Mann-Whitney U p<0.05)")
        if stats['zTest'] != "INSUFFICIENT_DATA" and stats['zTest'].get('significant'):
            findings.append("Significant Derivation Heavy (Z-Test p<0.05)")
        if stats['mannKendall'] != "INSUFFICIENT_DATA" and stats['mannKendall'].get('significant'):
            findings.append(f"Significant Trend: {stats['mannKendall']['trend']} (Mann-Kendall p<0.05)")
            
        if findings:
            report.append(f"**{tname}**: {', '.join(findings)}")
            
    report.append("")
    report.append("## Top Repeating Clusters")
    sorted_clusters = sorted(clusters, key=lambda x: x['variantCount'], reverse=True)
    for c in sorted_clusters[:10]:
        report.append(f"- **{c['variantCount']} variants**: {c['conceptLabel']} (Topic {c['topicCode']})")
        
    with open("analysis_report.md", "w") as f:
        f.write("\n".join(report))
        
    print("Statistical analysis complete.")

if __name__ == "__main__":
    main()
