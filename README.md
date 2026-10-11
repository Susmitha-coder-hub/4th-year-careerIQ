# CareerIQ – AI-Based Career Intelligence and Opportunity Assistant

CareerIQ is an intelligent, multi-module career and campus placement assistant engineered for students and college placement cells. It performs automated resume parsing, ATS scoring, semantic job matching, machine learning-driven placement readiness prediction, campus recruitment email intelligence, and context-grounded conversational career guidance.

---

## 🏗️ 1. System Architecture & Folder Structure

```
finalyear-project work/
│
├── app.py                         # Master Streamlit Interactive Dashboard
├── requirements.txt               # Complete Python dependencies
├── test_app.py                    # End-to-end automated verification test suite
├── README.md                      # Academic documentation & setup instructions
│
├── modules/                       # Core Intelligence Engines
│   ├── __init__.py
│   ├── resume_parser.py           # Module 1: PyMuPDF extraction, ATS scoring & suggestions
│   ├── job_matcher.py             # Module 2: Job skill extraction, TF-IDF cosine similarity & gap analysis
│   ├── placement_predictor.py     # Module 3: Scikit-learn Random Forest placement readiness classifier
│   ├── opportunity_tracker.py     # Module 4: Placement email NLP parser & iCal reminder generator
│   └── career_chatbot.py          # Module 5: Context-grounded career advisor
│
├── utils/                         # Helper Utilities & Taxonomy
│   ├── __init__.py
│   ├── skill_database.py          # Curated multi-domain skills ontology
│   ├── sample_data.py             # Pre-built benchmark resumes & job descriptions
│   └── exporter.py                # JSON & Markdown audit report generator
│
├── data/                          # Data Storage
│   ├── placement_dataset.csv      # 600-sample student placement training dataset
│   └── sample_resumes/            # Auto-generated PDF resumes for 1-click viva testing
│       ├── Alex_Rivera_SDE.pdf
│       └── Priya_Sharma_DataScience.pdf
│
└── models/                        # Serialized ML Models
    └── placement_model.pkl        # Trained Random Forest classifier & Scaler
```

---

## ⚡ 2. How to Run the Project in VS Code (Windows)

### Step 1: Open Terminal in VS Code
Open VS Code in this project folder (`c:\Users\susmi\Desktop\finalyear-project work`).  
Open the integrated terminal (`Ctrl + ~` or Terminal -> New Terminal).

### Step 2: Verify Dependencies
All dependencies are already installed in your Python 3.11 environment. If setting up on a fresh machine:
```powershell
pip install -r requirements.txt
```

### Step 3: Verify the System with Automated Tests
Run the test script to ensure all 5 modules are functional:
```powershell
python test_app.py
```
*Expected Output: `ALL MODULE TESTS PASSED PERFECTLY! SYSTEM IS 100% OPERATIONAL.`*

### Step 4: Launch the Streamlit Application
Run the Streamlit application using the Python module runner:
```powershell
python -m streamlit run app.py
```
Your default web browser will automatically open:
```
Local URL: http://localhost:8501
```

---

## 🔍 3. Core Modules & Implementation Details

| Module | Core Techniques Used | Methodology (Rule-Based vs ML) | Key Outputs |
| :--- | :--- | :--- | :--- |
| **Module 1: Resume Intelligence** | PyMuPDF, Regular Expressions, Skill Taxonomy | **Rule-based & Pattern NLP** | ATS Score (0-100), Contact extraction, Section validation, Categorized skills, Improvement suggestions |
| **Module 2: Job Intelligence** | TF-IDF Vectorization, N-Gram Cosine Similarity, Jaccard Matching | **Hybrid NLP & Statistical Cosine Sim** | Composite Match Score (%), Skill coverage (%), Matched/Missing skills, Role recommendations |
| **Module 3: Placement Intelligence** | Random Forest Classifier, Logistic Regression, StandardScaler | **Supervised Machine Learning (Scikit-Learn)** | Placement Probability (%), Readiness Tier, Confusion Matrix/F1 metrics, Upskill courses |
| **Module 4: Opportunity Intelligence** | NLP Regex Entities, iCalendar RFC 5545 | **Information Extraction & Simulation** | Extracted deadlines, Test schedules, Shortlist alerts, 1-Click .ics calendar export |
| **Module 5: Conversational AI** | Grounded Response Generator, Context Pipeline | **Context-Grounded Expert System** | Tailored ATS tips, Missing skill roadmaps, Dynamic technical interview questions |

---

## 📊 4. Experimental Evaluation & Benchmark Results

### A. Machine Learning Model Evaluation (Module 3)
Evaluated on a 20% holdout test set ($N=120$) with stratified sampling from `placement_dataset.csv`:

| Model | Test Accuracy | Precision | Recall | F1-Score | Status |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Random Forest (n=100, max_depth=6)** | **76.67%** | **78.41%** | **91.76%** | **84.57%** | Primary Production Model |
| **Logistic Regression (Baseline)** | 71.67% | 75.28% | 88.24% | 81.25% | Baseline Comparison |

**Top 3 Most Important Features (Feature Importance):**
1. **CGPA Weight:** 29.4%
2. **Aptitude Test Score:** 22.8%
3. **Coding Problems Solved:** 18.1%

---

### B. Sample Resumes Evaluation Benchmark (Modules 1 & 2)

| Test Resume | Total Skills Detected | ATS Score | Target Job Role | Composite Match | Matched Skills | Missing Skills |
| :--- | :---: | :---: | :--- | :---: | :---: | :---: |
| **Alex Rivera (SDE)** | 29 | 96 / 100 | Backend Software Engineer | 53.4% | Python, SQL, REST API, Git, Linux, Docker, etc. (16 skills) | 4 skills |
| **Priya Sharma (Data Science)** | 19 | 85 / 100 | Data Scientist / AI Engineer | 68.2% | Python, Machine Learning, Deep Learning, Pandas, etc. | 2 skills |

---

## 🎓 5. Academic Review & Viva Preparation Guide

### Key Questions the External Examiner May Ask:

**Q1: How does your ATS scoring algorithm work?**  
*Answer:* "CareerIQ computes a transparent 100-point composite score across 5 objective criteria: Contact completeness (15 pts), Standard section headings (25 pts), Skill count & domain diversity (35 pts), Action verbs & quantifiable metrics (15 pts), and Length/readability (10 pts). It avoids arbitrary grading and provides exact diagnostic pointers."

**Q2: Is your Job Matcher simply counting keywords?**  
*Answer:* "No. CareerIQ employs a dual-tier matching strategy. First, it determines exact required skill coverage using our curated taxonomy. Second, it computes semantic text alignment using TF-IDF n-gram vectorization and cosine similarity. The final Composite Score balances 60% hard skill coverage and 40% semantic text alignment."

**Q3: Where did the placement dataset come from and what are its limitations?**  
*Answer:* "For the academic prototype, a standardized dataset of 600 records was synthesized reflecting Indian engineering campus hiring cutoff trends (CGPA, aptitude tests, solved DSA problems, internships). The limitation is that it assumes a generalized placement policy; institutional deployments must be retrained on branch-specific campus placement histories."

**Q4: How does Opportunity Intelligence protect user privacy?**  
*Answer:* "The email parser only extracts content matching high-priority placement regex filters (`placements`, `campus hiring`, `assessment`, `shortlist`). It ignores personal correspondence, and in the production OAuth implementation, requests strict read-only scoped access."

---

## 🚀 6. Future Enhancements
1. Fine-tuning local LLM models (e.g. LLaMA-3 / Mistral via Ollama) for zero-shot question answering.
2. Direct integration with college ERP/Training & Placement Officer (TPO) portals.
3. Automated mock audio interview assessment using speech-to-text and sentiment analysis.
