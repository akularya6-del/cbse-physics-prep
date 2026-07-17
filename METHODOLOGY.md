# Methodology

## Overview
This document outlines the methodology used to extract, classify, cluster, and statistically validate CBSE Class 12 Physics Compartment Exam questions (2022-2096). The pipeline guarantees that all intelligence insights are derived purely from the dataset itself, rather than external assumptions.

## Phase 1: Data Extraction & Topic Classification
1. **Source Material**: PDF files of question papers from `./papers/`.
2. **Metadata Extraction**: Regular expressions parse filename conventions to identify the year, paper type (Main vs. Compartment), and Set Number.
3. **Question Parsing**: Each paper's text is parsed sequentially to isolate discrete questions, assigning Section (A-E) and default mark weightages where explicit marks are missing.
4. **Topic Classification**: A dictionary of 15 core CBSE topics and their exhaustive keywords (30+ per topic) is used. A string-matching algorithm scores each question against the topic dictionary. Questions explicitly requesting derivations (e.g., "derive", "show that") amplify the matched topic's score by 1.5x.

## Phase 2: Semantic Clustering
1. **Embedding**: `SentenceTransformers` (`all-MiniLM-L6-v2`) vectorizes the raw text of each question.
2. **Agglomerative Clustering**: Questions are clustered using Agglomerative Clustering with a `cosine` affinity metric and `average` linkage.
3. **Thresholding**: A strict distance threshold of 0.25 guarantees that questions grouped into the same cluster exhibit extremely high semantic similarity (>0.75 cosine similarity).
4. **Boundary Rules**: Clustering is strictly performed *within* topic boundaries. Cross-topic clustering is disabled to prevent conceptually disparate questions from merging.
5. **Centroid Identification**: The cluster's `conceptLabel` is dynamically defined by identifying the member question that holds the highest average cosine similarity to all other members in that cluster.

## Cross-Set Deduplication Rule
**Rule:** Same-year different-set questions are treated as **independent occurrences**.

**Justification:** Extensive analysis of CBSE set variations shows that the board typically shuffles question order or makes minor numerical modifications to core concepts rather than replacing concepts entirely. A repeated concept across multiple sets in the same year signifies higher examiner priority for that concept. Deduplication would artificially penalize the importance of universally tested concepts. By treating them independently, the statistical tests (like Frequency and Compartment Bias) accurately reflect the concept's true prevalence in the testing pool.

## Phase 3: Statistical Validation
To elevate insights beyond simple counting, rigorous statistical tests measure the relevance and trends of each topic:
- **Chi-Square Test**: Measures Compartment Bias (whether a topic appears disproportionately often in Compartment exams vs. Main exams).
- **Mann-Whitney U Test**: Measures Marks Weightage differences.
- **Z-Test**: Evaluates the propensity for Derivation-heavy questions.
- **Mann-Kendall Trend Test**: Detects monotonic trends over time (increasing or decreasing prevalence).

Each metric is Min-Max normalized (0-100), and a Composite Priority Score is generated to drive the final Intelligence Dashboard recommendations.
