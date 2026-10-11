# CareerFit: AI-Based Career Intelligence & Job Matching System
**Final-Year CSE Project — Implementation Milestone 1 (~30% Planned Scope)**

CareerFit is an AI-driven career intelligence platform that enables students and job seekers to analyze PDF resumes, match them against job description requirements using TF-IDF cosine similarity baselines, and receive structured, ethical skill gap analyses.

---

## 🏗️ 1. Architecture & Technology Stack

- **Frontend**: React (Vite) + Tailwind CSS + Lucide Icons
- **Backend API**: Python 3.11 + FastAPI + Uvicorn
- **PDF Extraction**: `pypdf` (selectable text streams, validation for size, encryption, empty and image-only scans)
- **Text Processing & ML**: Scikit-Learn (`TfidfVectorizer`, Cosine Similarity) + Rule-Based Skill Ontology
- **Data Storage**: SQLite (`careerfit.db` for persisted analysis records and metrics)
- **Testing & Docs**: Pytest (11 automated test cases) + Swagger UI (`/docs`)

```
finalyear-project work/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI Application Entry & CORS
│   │   ├── core/
│   │   │   ├── config.py            # Environment Configuration
│   │   │   └── database.py          # SQLite Connection & CRUD Operations
│   │   ├── services/
│   │   │   ├── pdf_parser.py        # Module 1: pypdf Extraction & Validation
│   │   │   ├── skill_extractor.py   # Module 2: Configurable Skill Dictionary & Regex
│   │   │   ├── matcher.py           # Module 3: TF-IDF Cosine Similarity Engine
│   │   │   └── gap_analyzer.py      # Module 4: Skill Gap & Ethical Advice Service
│   │   ├── routers/
│   │   │   ├── resumes.py           # POST /api/resumes/parse
│   │   │   ├── jobs.py              # POST /api/jobs/analyze
│   │   │   ├── matching.py          # POST /api/matching/analyze
│   │   │   └── history.py           # GET /api/history, DELETE /api/history/{id}
│   │   └── models/
│   │       └── schemas.py           # Pydantic Schemas
│   └── tests/
│       └── test_backend.py          # 11 Automated Pytest Unit Tests
│
├── frontend/
│   ├── src/
│   │   ├── api/client.js            # Centralized Fetch API Client
│   │   ├── components/
│   │   │   ├── Sidebar.jsx          # Responsive Navigation
│   │   │   └── Header.jsx           # Status Indicators & Demo Mode Badge
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx        # Real SQLite Metrics & Activity
│   │   │   ├── ResumeAnalyzer.jsx   # Module 1: PDF Upload & Text Preview
│   │   │   ├── JobMatching.jsx      # Module 2: TF-IDF Similarity & Overlaps
│   │   │   ├── SkillGapAnalysis.jsx # Module 3: Domain Gaps & Practical Advice
│   │   │   ├── AnalysisHistory.jsx  # Module 5: SQLite History & Record Deletion
│   │   │   └── AboutCareerFit.jsx   # Milestone Scope, Methodology & Limitations
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
│
└── careerfit.db                     # Local SQLite Database
```

---

## ⚡ 2. How to Run Locally in VS Code (Windows)

Both services can be launched directly in VS Code terminal:

### A. Start the FastAPI Backend
Open a terminal in the project root:
```powershell
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
- API Base: `http://127.0.0.1:8000`
- Interactive Swagger UI: `http://127.0.0.1:8000/docs`

### B. Start the React Frontend
Open a second terminal window:
```powershell
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```
- Frontend UI: `http://127.0.0.1:5173/`

---

## 🧪 3. Automated Test Results (Module 6)

Run the backend test suite:
```powershell
python -m pytest backend/tests/test_backend.py -v
```

### Verified Test Summary (11/11 Passed):
| Test Case | Module | Description | Result |
| :--- | :--- | :--- | :---: |
| `test_pdf_valid_extraction` | Module 1 | Valid synthetic PDF text and contact parsing | **PASSED** |
| `test_pdf_empty_bytes_validation` | Module 1 | 0-byte file rejection | **PASSED** |
| `test_pdf_corrupt_file_validation` | Module 1 | Corrupted PDF header rejection | **PASSED** |
| `test_pdf_oversized_file_validation` | Module 1 | Enforces 5 MB file size limit | **PASSED** |
| `test_skill_extraction_accuracy` | Module 2 | Detects exact skills (python, docker, sql, git) | **PASSED** |
| `test_skill_extraction_short_tokens` | Module 2 | Distinguishes isolated "C" and "R" from words | **PASSED** |
| `test_matching_score_bounds` | Module 3 | Bounded TF-IDF cosine score (0.0 to 100.0) | **PASSED** |
| `test_matching_identical_text` | Module 3 | Identical texts yield ~100% similarity | **PASSED** |
| `test_matching_empty_inputs` | Module 3 | Handles empty inputs gracefully (returns 0.0) | **PASSED** |
| `test_skill_gap_analysis` | Module 4 | Categorizes missing skills & outputs guidance | **PASSED** |
| `test_database_persistence` | Module 5 | SQLite save, fetch, and delete round-trip | **PASSED** |

---

## 📊 4. Scope Mapping for Academic Review (12 October 2026)

| Milestone 1 Implemented Features (~30%) | Out of Scope for Milestone 1 (Planned Future Work) |
| :--- | :--- |
| ✅ PDF Upload & Text Parsing via `pypdf` | ⏳ Automated Gmail / placement inbox monitoring |
| ✅ Configurable technical skills taxonomy | ⏳ Placement readiness prediction ML model |
| ✅ TF-IDF Cosine Similarity Baseline (0–100) | ⏳ Generative LLM resume re-writing |
| ✅ Overlapping vs Missing Skill Gap Analysis | ⏳ Live job board web scrapers |
| ✅ SQLite History Archive & Record Deletion | ⏳ Multi-resume recruiter ranking algorithms |
| ✅ Clean SaaS Dashboard (React + Tailwind CSS) | ⏳ External chatbot integrations (WhatsApp/Discord) |

---

## 🔒 5. Privacy & Ethical Disclosure
- **No Raw Text Storage:** CareerFit never saves raw candidate resume text in SQLite. Only computed metadata, detected skill tags, and similarity scores are archived.
- **No Hallucinated Qualifications:** The system never recommends fabricating credentials or stuffing keywords into resumes.
