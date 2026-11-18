# CareerFit: AI-Based Career Intelligence & Job Matching System
**Final-Year CSE Project — Implementation Milestone 2 (~50-60% Planned Scope Completed)**

CareerFit is an AI-driven career intelligence platform that enables students and job seekers to understand their skills, improve their resumes, evaluate placement readiness, compare resumes against recruiter job specifications, discover proactive opportunity alerts, and prepare for interviews through an integrated AI assistant.

---

## 🏗️ 1. Architecture & Technology Stack

- **Frontend**: React (Vite) + Tailwind CSS + Lucide Icons
- **Backend API**: Python 3.11 + FastAPI + Uvicorn
- **PDF Extraction**: `pypdf` (selectable text streams, validation for size, encryption, empty, and image-only scans)
- **Text Processing & ML**: Scikit-Learn (`TfidfVectorizer`, Cosine Similarity) + Rule-Based Skill Ontology + Multi-factor Evaluation Models
- **Data Storage**: SQLite (`careerfit.db` for persisted analysis records and metrics)
- **Testing & Docs**: Pytest (16 automated test cases, 100% passing) + Swagger UI (`/docs`)

```
finalyear-project work/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI Application Entry, CORS & Router Mounts
│   │   ├── core/
│   │   │   ├── config.py            # Environment Configuration
│   │   │   └── database.py          # SQLite Connection & CRUD Operations
│   │   ├── services/
│   │   │   ├── pdf_parser.py        # Module 1: pypdf Extraction & Validation
│   │   │   ├── skill_extractor.py   # Module 2: Configurable Skill Dictionary & Regex
│   │   │   ├── matcher.py           # Module 3: TF-IDF Cosine Similarity Engine
│   │   │   ├── gap_analyzer.py      # Module 4: Skill Gap & Course Recommendations
│   │   │   ├── prediction_engine.py # Module 6: Placement Readiness Prediction Engine
│   │   │   ├── recruiter_ranker.py  # Module 7: Multi-Resume Comparison & Recruiter Ranking
│   │   │   ├── opportunity_service.py # Module 8: Opportunity Intelligence & Prep Guide
│   │   │   └── chatbot_service.py   # Module 9: Universal AI Career Assistant Engine
│   │   ├── routers/
│   │   │   ├── resumes.py           # POST /api/resumes/parse
│   │   │   ├── jobs.py              # POST /api/jobs/analyze
│   │   │   ├── matching.py          # POST /api/matching/analyze
│   │   │   ├── history.py           # GET /api/history, DELETE /api/history/{id}
│   │   │   ├── prediction.py        # POST /api/prediction/placement-readiness
│   │   │   ├── recruiter.py         # POST /api/recruiter/rank-resumes
│   │   │   ├── opportunities.py     # GET /api/opportunities/, POST /check-eligibility
│   │   │   └── chat.py              # POST /api/chat/message
│   │   └── models/
│   │       └── schemas.py           # Pydantic Schemas
│   └── tests/
│       └── test_backend.py          # 16 Automated Pytest Unit Tests
│
├── frontend/
│   ├── src/
│   │   ├── api/client.js            # Centralized Fetch API Client
│   │   ├── components/
│   │   │   ├── Sidebar.jsx          # Grouped Navigation (Student / Recruiter / System)
│   │   │   └── Header.jsx           # Status Indicators & Demo Mode Badge
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx        # Real SQLite Metrics & Activity
│   │   │   ├── ResumeAnalyzer.jsx   # Module 1: PDF Upload & Text Preview
│   │   │   ├── JobMatching.jsx      # Module 2: TF-IDF Similarity & Overlaps
│   │   │   ├── SkillGapAnalysis.jsx # Module 3: Domain Gaps & Course Recommendations
│   │   │   ├── PlacementPrediction.jsx # Module 6: Placement Readiness & Dimension Ratings
│   │   │   ├── RecruiterComparison.jsx # Module 7: Multi-Resume Ranking & Rationale
│   │   │   ├── OpportunityIntelligence.jsx # Module 8: Placement Drives & 48h Prep Pack
│   │   │   ├── CareerChatbot.jsx    # Module 9: Universal AI Career Assistant Chatbot
│   │   │   ├── AnalysisHistory.jsx  # Module 5: SQLite History & Record Deletion
│   │   │   └── AboutCareerFit.jsx   # Milestone Scope & Academic Specification
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

## 🧪 3. Automated Test Results (16/16 Passed)

Run the backend test suite:
```powershell
python -m pytest backend/tests/test_backend.py -v
```

### Verified Test Summary:
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
| `test_placement_readiness_prediction` | Module 6 | 6-dimension weighted readiness evaluation (Points 4 & 10) | **PASSED** |
| `test_recruiter_multi_resume_ranking` | Module 7 | Multi-resume comparison & leaderboard ranking (Point 9) | **PASSED** |
| `test_opportunity_intelligence` | Module 8 | Campus drive eligibility, reminders & 48h prep guide (Points 11–14) | **PASSED** |
| `test_career_assistant_chatbot` | Module 9 | Universal chat query handling & dynamic suggestions (Points 16 & 17) | **PASSED** |
| `test_enriched_course_recommendations` | Module 4 | Course recommendations with effort & project roadmaps (Point 15) | **PASSED** |

---

## 📊 4. Scope Mapping for Academic Review

| Milestone 1 & 2 Implemented Features (~50-60% Scope) | Remaining Future Scope (Milestone 3 / Final Viva) |
| :--- | :--- |
| ✅ PDF Upload & Text Parsing via `pypdf` | ⏳ Automated Live Gmail OAuth2 daemon inbox polling |
| ✅ Configurable technical skills taxonomy & regex parsing | ⏳ Live job board web scrapers (LinkedIn, Naukri) |
| ✅ TF-IDF Cosine Similarity Baseline (0–100 score) | ⏳ Fine-tuned BERT dual-encoder model checkpoint |
| ✅ Overlapping vs Missing Skill Gap Analysis | ⏳ Enterprise Role-Based Access Control (RBAC) |
| ✅ Course & Learning Pathway Recommendations (Point 15) | ⏳ Live WhatsApp / Discord webhook deployment |
| ✅ SQLite History Archive & Record Deletion | |
| ✅ Placement Readiness Prediction Engine (Points 4 & 10) | |
| ✅ Recruiter Multi-Resume Ranking & Leaderboard (Point 9) | |
| ✅ Opportunity Intelligence, Urgency Alerts & 48h Prep (Points 11–14) | |
| ✅ Universal AI Career Assistant Chatbot (Points 16 & 17) | |
| ✅ Complete React + Tailwind SaaS UI (All Modules Integrated) | |

---

## 🔒 5. Privacy & Ethical Disclosure
- **No Raw Text Storage:** CareerFit never saves raw candidate resume text in SQLite. Only computed metadata, detected skill tags, and similarity scores are archived.
- **No Hallucinated Qualifications:** The system never recommends fabricating credentials or stuffing keywords into resumes.
- **Academic Estimation:** Placement readiness scoring is explicitly presented as an educational diagnostic estimate, not a guaranteed corporate placement offer.
