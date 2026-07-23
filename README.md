<div align="center">
  <h1>🧠 CBSE Physics Compartment Prep Dashboard</h1>
  <p><b>An AI-powered data extraction and analytics pipeline for Class 12 Physics</b></p>
  <img src="https://img.shields.io/badge/Status-Active-success.svg" alt="Status">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/AI-Mistral%20Large%20%7C%20Amazon%20Bedrock-orange.svg" alt="AI Powered">
</div>

---

## 📖 Overview

The **CBSE Physics Compartment Prep Dashboard** is a state-of-the-art study tool designed to help students maximize their preparation for the Class 12 Physics Compartment Exam in just 10 days. 

Instead of overwhelming students with entire textbooks, this pipeline **parses years of past compartment and supplementary question papers**, clusters semantic variations of questions, and uses **Generative AI** (Amazon Bedrock / Mistral Large) to validate and clean the data. The result is a highly optimized, data-backed study plan that prioritizes the most frequently repeated concepts across multiple years.

## ✨ Key Features

- **📄 Smart PDF Extraction:** Processes bilingual CBSE exam PDFs, automatically identifying and skipping alternating Hindi translation pages to prevent duplicates and OCR noise.
- **🤖 AI-Powered Validation:** Uses Amazon Bedrock LLMs to rigorously validate extracted questions, flag merged questions, fix OCR errors, and ensure zero hallucinations.
- **🧩 Semantic Clustering:** Groups rephrased versions of the exact same conceptual question using advanced text similarity matching.
- **📊 Tier-Based Priority:** 
  - 🔥 **Tier 1 (Must-Do):** Concepts that have appeared in 3 or more exam sets across multiple years.
  - ⚡ **Tier 2 (High Probability):** Concepts that have appeared in exactly 2 exam sets.
- **🎨 Data-Backed Dashboard:** Generates beautiful, printable markdown practice sheets and HTML dashboards organizing study tasks chapter-by-chapter with a strict dark-mode aesthetic.

## 📂 Project Structure

```text
├── src/
│   ├── extract_papers.py       # Core extraction engine for PDFs
│   ├── ai_verify_sheet.py      # Cleans OCR noise using Mistral Large via Bedrock
│   ├── validate_extraction.py  # Amazon Bedrock AI validation oracle
│   ├── analyze_clusters.py     # Semantic clustering logic
│   └── generate_dashboard.py   # Main analytics and tier generation
├── data/
│   ├── papers/                 # Raw PDF question papers
│   └── physics_questions_database.json # Cleaned, extracted questions
├── docs/
│   ├── multi_year_practice_sheet.md   # Raw multi-year question frequency sheet
│   ├── ai_verified_practice_sheet.md  # Final, AI-cleaned, beautiful practice sheet
│   ├── top_10_practice_sheet.md       # Top 10 most repeated questions per chapter
│   └── top_15_practice_sheet.md       # Top 15 most repeated questions per chapter
├── METHODOLOGY.md              # Detailed explanation of data pipeline
└── README.md                   # This file
```

## 🚀 Setup & Execution

### Prerequisites
- **Python 3.10+**
- **Valid AWS Credentials** with access to Amazon Bedrock (required if re-running the AI verification scripts).

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/akularya6-del/cbse-physics-prep.git
   cd cbse-physics-prep
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### 🧠 Accessing the Practice Sheets
The pipeline has already been run, and the highly optimized practice sheets are available in the `docs/` folder!
- `docs/ai_verified_practice_sheet.md`: The ultimate, AI-cleaned study sheet sorted by highest repetition.
- `docs/top_10_practice_sheet.md`: A quick-hit sheet of the top 10 questions per chapter.
- `docs/top_15_practice_sheet.md`: A slightly expanded sheet with the top 15 questions per chapter.

### 🔄 Re-running the Pipeline (Optional)
If you add new PDF papers to `data/papers/` and want to re-process everything:
1. **Extract questions:** `python3 src/extract_papers.py`
2. **Generate sheets:** Use the provided scripts to build the markdown files.
3. **Validate with AI:** `python3 src/ai_verify_sheet.py` (ensure your `AWS_BEARER_TOKEN_BEDROCK` is set in the script environment).

## 🛡️ Methodology

Our extraction explicitly targets **Compartment (`_C_`)** and **Supplementary (`-S-`)** papers. The pipeline automatically calculates "Repeater Scores" by tracking how often a specific conceptual topic appears across different years. 

By focusing on understanding over rote memorization, this plan strips away low-yield topics and focuses strictly on high-probability concepts, ensuring you spend your limited time on what truly matters.

---
<div align="center">
  <i>Built to help students conquer the Physics Compartment Exam with data, not stress.</i>
</div>
