import json
import sys
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity
import traceback

def main():
    try:
        with open('physics_questions_database.json', 'r') as f:
            db = json.load(f)
    except Exception as e:
        print(f"Error loading database: {e}")
        sys.exit(1)

    questions = db.get("questions", [])
    
    # Filter out unclassified
    valid_qs = [q for q in questions if q.get("topicCode") != "00"]
    
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer('all-MiniLM-L6-v2')
    except Exception as e:
        print(f"Error loading sentence-transformers model: {e}")
        traceback.print_exc()
        sys.exit(1)

    # Group by topic
    topics = {}
    for q in valid_qs:
        topic = q['topicCode']
        if topic not in topics:
            topics[topic] = []
        topics[topic].append(q)
        
    clusters_output = []
    cluster_counter = 1

    for topic_code, topic_qs in topics.items():
        topic_name = topic_qs[0]['topicName']
        
        if len(topic_qs) < 2:
            # Skip clustering, singleton
            for q in topic_qs:
                cid = f"CL-{topic_code}-{cluster_counter:03d}"
                cluster_counter += 1
                clusters_output.append({
                    "clusterId": cid,
                    "topicCode": topic_code,
                    "topicName": topic_name,
                    "conceptLabel": q['questionText'],
                    "canonicalQuestion": q['questionText'],
                    "variantCount": 1,
                    "variants": [{
                        "questionId": q['id'],
                        "year": q['year'],
                        "paperType": q['paperType'],
                        "setNumber": q['setNumber'],
                        "marks": q['marks'],
                        "questionText": q['questionText']
                    }],
                    "yearSpread": {
                        "totalYearsAppeared": 1,
                        "yearsList": [q['year']],
                        "compartmentYears": [q['year']] if q['paperType'] == 'Compartment' else [],
                        "mainYears": [q['year']] if q['paperType'] == 'Main' else []
                    },
                    "marksRange": {
                        "min": q['marks'] if q['marks'] is not None else 0,
                        "max": q['marks'] if q['marks'] is not None else 0,
                        "average": q['marks'] if q['marks'] is not None else 0
                    }
                })
            continue

        # More than 2 questions, perform clustering
        texts = [q['questionText'] for q in topic_qs]
        try:
            embeddings = model.encode(texts)
        except Exception as e:
            print(f"Error encoding texts for topic {topic_code}: {e}")
            continue

        # Agglomerative clustering with cosine affinity
        # Distance threshold 0.25 (which maps to >0.75 cosine similarity for grouping)
        # Note: scikit-learn AgglomerativeClustering with distance_threshold requires n_clusters=None
        clustering = AgglomerativeClustering(
            n_clusters=None,
            metric='cosine',
            linkage='average',
            distance_threshold=0.25
        )
        
        try:
            labels = clustering.fit_predict(embeddings)
        except Exception as e:
            print(f"Clustering error on topic {topic_code}: {e}")
            # fallback to singletons
            labels = range(len(topic_qs))
            
        # Group by label
        clustered_groups = {}
        for idx, label in enumerate(labels):
            if label not in clustered_groups:
                clustered_groups[label] = []
            clustered_groups[label].append(idx)
            
        for label, indices in clustered_groups.items():
            cid = f"CL-{topic_code}-{cluster_counter:03d}"
            cluster_counter += 1
            
            group_qs = [topic_qs[i] for i in indices]
            
            # Find centroid (conceptLabel / canonicalQuestion)
            if len(indices) == 1:
                centroid_q = group_qs[0]
            else:
                group_embeddings = embeddings[indices]
                sim_matrix = cosine_similarity(group_embeddings)
                avg_sims = sim_matrix.mean(axis=1)
                centroid_idx_local = np.argmax(avg_sims)
                centroid_q = group_qs[centroid_idx_local]
                
            variants = []
            years = set()
            comp_years = set()
            main_years = set()
            marks = []
            
            for q in group_qs:
                variants.append({
                    "questionId": q['id'],
                    "year": q['year'],
                    "paperType": q['paperType'],
                    "setNumber": q['setNumber'],
                    "marks": q['marks'],
                    "questionText": q['questionText']
                })
                years.add(q['year'])
                if q['paperType'] == 'Compartment':
                    comp_years.add(q['year'])
                else:
                    main_years.add(q['year'])
                if q['marks'] is not None:
                    marks.append(q['marks'])
                    
            clusters_output.append({
                "clusterId": cid,
                "topicCode": topic_code,
                "topicName": topic_name,
                "conceptLabel": centroid_q['questionText'],
                "canonicalQuestion": centroid_q['questionText'],
                "variantCount": len(variants),
                "variants": variants,
                "yearSpread": {
                    "totalYearsAppeared": len(years),
                    "yearsList": sorted(list(years)),
                    "compartmentYears": sorted(list(comp_years)),
                    "mainYears": sorted(list(main_years))
                },
                "marksRange": {
                    "min": min(marks) if marks else 0,
                    "max": max(marks) if marks else 0,
                    "average": round(sum(marks)/len(marks), 1) if marks else 0
                }
            })

    with open("question_clusters.json", "w") as f:
        json.dump(clusters_output, f, indent=2)
        
    print(f"Generated {len(clusters_output)} clusters.")

if __name__ == "__main__":
    main()
