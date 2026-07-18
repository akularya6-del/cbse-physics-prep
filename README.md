# CBSE Physics 10-Day Exam Prep Dashboard

An AI-powered data extraction and analytics pipeline designed to help students prepare for the CBSE Class 12 Physics Compartment Exam. By parsing years of past compartment and supplementary question papers, clustering semantic variations of questions, and validating the extraction with AI, this tool generates a highly optimized, data-backed 10-day study plan.

## 🌟 Features

- **Smart PDF Extraction:** Processes bilingual exam PDFs, automatically identifying and skipping alternating Hindi translation pages to prevent duplicates.
- **AI-Powered Validation:** Uses Amazon Bedrock LLMs (Mistral Large / Claude) to rigorously validate the extracted questions, flag merged questions, and ensure zero hallucinations or artifacts.
- **Semantic Clustering:** Groups rephrased versions of the same conceptual question using advanced text similarity matching.
- **Tier-Based Priority:** 
  - 🔴 **Tier 1 (Must-Do):** Concepts that have appeared in 3 or more exam sets.
  - 🟠 **Tier 2 (High Probability):** Concepts that have appeared in exactly 2 exam sets.
- **Data-Backed Dashboard:** Generates a beautiful, printable HTML dashboard organizing study tasks chapter-by-chapter with time estimates.

## 📂 Project Structure

```
├── src/
│   ├── extract_papers.py       # Core extraction engine for PDFs
│   ├── validate_extraction.py  # Amazon Bedrock AI validation oracle
│   ├── analyze_clusters.py     # Semantic clustering logic
│   ├── generate_dashboard.py   # Main analytics and tier generation
│   ├── patch.py                # Database patching utilities
│   └── analyze_stats.py        # Analytics on question weightage
├── data/
│   ├── papers/                 # Raw PDF question papers
│   ├── physics_questions_database.json # Cleaned, extracted questions
│   ├── question_clusters.json          # Grouped semantic clusters
│   ├── priority_dashboard.html         # Final output: The 10-Day Study Dashboard
│   └── index.html                      # Main full-syllabus analytics platform
├── docs/
│   ├── extraction_report.md
│   ├── validation_report.md
│   └── analysis_report.md
├── archive/                    # Old test scripts and utilities
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## 🚀 Setup & Execution

### Prerequisites
- Python 3.10+
- Valid AWS credentials with access to Amazon Bedrock (if re-running the AI validation)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/akularya6-del/cbse-physics-prep.git
   cd cbse-physics-prep
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Generating the Dashboard
The final dashboard has already been generated in `data/priority_dashboard.html`. To view it, start a local HTTP server:
```bash
cd data
python3 -m http.server 8000
```
Open `http://localhost:8000/priority_dashboard.html` in your browser.

### Re-running the Pipeline (Optional)
If you add new PDF papers to `data/papers/`:
1. Extract questions: `python3 src/extract_papers.py`
2. Validate with AI: `python3 src/validate_extraction.py`
3. Generate the updated dashboard (the inline python script handles this based on tier logic).

## 🛡️ Methodology
Our extraction explicitly targets Compartment (`_C_`) and Supplementary (`-S-`) papers. The pipeline automatically calculates "Repeater Scores" and builds a study plan based exclusively on concepts proven to repeat in real exams. By focusing on understanding over rote memorization, the 10-day plan strips away low-yield topics and focuses strictly on high-probability concepts.
