"""
backend/tests/test_backend.py
Comprehensive automated test suite for CareerFit backend.
Covers:
1. PDF validation (empty, corrupt, valid synthetic PDF)
2. Skill extraction using regex taxonomy
3. TF-IDF Cosine Similarity bounds (0.0 to 100.0)
4. Missing skill & gap analysis
5. Invalid input edge cases
6. SQLite database persistence and deletion
"""

import os
import io
import pytest
from reportlab.pdfgen import canvas
from backend.app.services.pdf_parser import parse_pdf_resume
from backend.app.services.skill_extractor import extract_skills_from_text, categorize_skills
from backend.app.services.matcher import compute_tfidf_similarity_score, match_resume_and_job
from backend.app.services.gap_analyzer import perform_skill_gap_analysis
from backend.app.core.database import init_db, save_analysis, get_all_analyses, delete_analysis, get_dashboard_metrics

# Helper: Create synthetic in-memory PDF
def create_synthetic_pdf(text: str) -> bytes:
    buf = io.BytesIO()
    c = canvas.Canvas(buf)
    y = 750
    for line in text.split("\n"):
        c.drawString(50, y, line)
        y -= 20
    c.save()
    return buf.getvalue()

# Test 1: PDF Validation & Text Extraction
def test_pdf_valid_extraction():
    synthetic_text = "John Doe\nEmail: john@example.com\nSkills: Python, Docker, SQL, Git."
    pdf_bytes = create_synthetic_pdf(synthetic_text)
    result = parse_pdf_resume(pdf_bytes, "synthetic_resume.pdf")

    assert result["filename"] == "synthetic_resume.pdf"
    assert "Python" in result["text"]
    assert result["contact_info"]["email"] == "john@example.com"
    assert result["word_count"] > 5

def test_pdf_empty_bytes_validation():
    with pytest.raises(ValueError, match="empty"):
        parse_pdf_resume(b"", "empty.pdf")

def test_pdf_corrupt_file_validation():
    with pytest.raises(ValueError, match="Corrupt or invalid PDF format"):
        parse_pdf_resume(b"This is not a PDF header content", "corrupt.pdf")

def test_pdf_oversized_file_validation():
    # 6 MB dummy payload with max 5MB limit
    large_bytes = b"0" * (6 * 1024 * 1024)
    with pytest.raises(ValueError, match="exceeds maximum allowed limit"):
        parse_pdf_resume(large_bytes, "oversized.pdf", max_size_mb=5)

# Test 2: Skill Extraction
def test_skill_extraction_accuracy():
    text = "Developed web backends using Python, FastAPI, and PostgreSQL. Experienced with Docker and Git."
    skills = extract_skills_from_text(text)
    assert "python" in skills
    assert "fastapi" in skills
    assert "postgresql" in skills
    assert "docker" in skills
    assert "git" in skills

def test_skill_extraction_short_tokens():
    # Should detect 'c' only when it's an isolated token, not within 'cloud' or 'machine'
    text = "Proficient in C and R programming for analytics."
    skills = extract_skills_from_text(text)
    assert "c" in skills
    assert "r" in skills

    text_no_c = "Cloud architecture and cluster scaling."
    skills_no_c = extract_skills_from_text(text_no_c)
    assert "c" not in skills_no_c

# Test 3: Matching Score Bounds (0.0 to 100.0)
def test_matching_score_bounds():
    resume_text = "Experienced Python developer with Django, SQL, and Docker skills."
    job_text = "Looking for a Python software engineer with Docker, REST API, and AWS expertise."

    score = compute_tfidf_similarity_score(resume_text, job_text)
    assert 0.0 <= score <= 100.0
    assert score > 0.0  # Common terms should give non-zero similarity

def test_matching_identical_text():
    sample = "Full-stack engineer building React applications with Node.js and MongoDB."
    score = compute_tfidf_similarity_score(sample, sample)
    assert score >= 99.0  # Identical text cosine similarity is ~100%

def test_matching_empty_inputs():
    assert compute_tfidf_similarity_score("", "Job description text") == 0.0
    assert compute_tfidf_similarity_score("Resume text", "") == 0.0

# Test 4: Missing Skill & Gap Analysis
def test_skill_gap_analysis():
    resume_skills = ["python", "sql", "git"]
    job_skills = ["python", "sql", "docker", "aws"]

    match_result = match_resume_and_job(
        resume_text="Python SQL Git",
        job_text="Python SQL Docker AWS",
        pre_extracted_resume_skills=resume_skills
    )

    assert "python" in match_result["matched_skills"]
    assert "sql" in match_result["matched_skills"]
    assert "docker" in match_result["missing_skills"]
    assert "aws" in match_result["missing_skills"]

    gap_data = perform_skill_gap_analysis(
        resume_skills=resume_skills,
        job_skills=job_skills,
        matched_skills=match_result["matched_skills"],
        missing_skills=match_result["missing_skills"]
    )

    assert gap_data["summary"]["matched_count"] == 2
    assert gap_data["summary"]["missing_count"] == 2
    assert len(gap_data["actionable_suggestions"]) == 2

# Test 5: SQLite Database Persistence
def test_database_persistence():
    init_db()
    analysis_id = save_analysis(
        resume_filename="test_candidate.pdf",
        job_title="Backend Developer",
        similarity_score=68.5,
        matched_skills=["python", "sql"],
        missing_skills=["docker"],
        resume_skills=["python", "sql", "git"],
        job_skills=["python", "sql", "docker"]
    )
    assert analysis_id is not None

    all_records = get_all_analyses()
    found = [r for r in all_records if r["id"] == analysis_id]
    assert len(found) == 1
    assert found[0]["similarity_score"] == 68.5

    # Test Deletion
    deleted = delete_analysis(analysis_id)
    assert deleted is True

    # Confirm deleted
    metrics = get_dashboard_metrics()
    assert metrics is not None

# Test 6: Placement Readiness Prediction Engine (Milestone 2 - Points 4 & 10)
def test_placement_readiness_prediction():
    from backend.app.services.prediction_engine import evaluate_placement_readiness
    from backend.app.models.schemas import PlacementPredictionRequest

    # High readiness profile
    high_profile = PlacementPredictionRequest(
        name="Alex Rivera",
        branch="Computer Science and Engineering",
        cgpa=8.8,
        technical_skills=["python", "fastapi", "docker", "sql", "git", "react", "algorithms"],
        aptitude_score=85.0,
        projects_count=3,
        internships_count=1,
        communication_rating=4.5
    )
    res_high = evaluate_placement_readiness(high_profile)
    assert 0.0 <= res_high.readiness_score <= 100.0
    assert res_high.readiness_score >= 80.0
    assert res_high.readiness_band == "High Placement Readiness"
    assert len(res_high.dimensions) == 6
    assert len(res_high.strengths) > 0
    assert len(res_high.actionable_prep_strategy) > 0

    # Low readiness profile
    low_profile = PlacementPredictionRequest(
        name="Junior Student",
        branch="Civil Engineering",
        cgpa=5.8,
        technical_skills=["c"],
        aptitude_score=40.0,
        projects_count=0,
        internships_count=0,
        communication_rating=2.5
    )
    res_low = evaluate_placement_readiness(low_profile)
    assert res_low.readiness_score < 60.0
    assert res_low.readiness_band == "Foundation Building Phase"
    assert len(res_low.critical_improvements) > 0

# Test 7: Recruiter Multi-Resume Ranking Engine (Milestone 2 - Point 9)
def test_recruiter_multi_resume_ranking():
    from backend.app.services.recruiter_ranker import rank_candidates_against_jd
    from backend.app.models.schemas import RecruiterRankingRequest, CandidateInput

    req = RecruiterRankingRequest(
        job_title="Full Stack Python Engineer",
        job_description="Seeking a Full Stack Engineer with strong experience in Python, FastAPI, React, SQL, and Docker.",
        candidates=[
            CandidateInput(
                name="Candidate Strong",
                resume_text="Senior engineer skilled in Python, FastAPI, React, SQL, Docker, and Git. Built microservices."
            ),
            CandidateInput(
                name="Candidate Moderate",
                resume_text="Junior student with basic HTML, CSS, JavaScript, and introductory Python."
            ),
            CandidateInput(
                name="Candidate Weak",
                resume_text="Accountant with experience in Excel, Bookkeeping, and Financial Auditing."
            )
        ]
    )
    res = rank_candidates_against_jd(req)
    assert res.total_evaluated == 3
    assert len(res.ranked_candidates) == 3
    # Verifying descending ranking
    assert res.ranked_candidates[0].rank == 1
    assert res.ranked_candidates[0].name == "Candidate Strong"
    assert res.ranked_candidates[0].match_score > res.ranked_candidates[1].match_score
    assert res.ranked_candidates[1].match_score >= res.ranked_candidates[2].match_score
    assert res.ranked_candidates[0].match_tier in ["Strong Match", "Good Match"]

# Test 8: Opportunity Intelligence & Eligibility (Milestone 2 - Points 11-14)
def test_opportunity_intelligence():
    from backend.app.services.opportunity_service import (
        get_active_opportunities,
        generate_interview_prep_guide
    )
    from backend.app.models.schemas import OpportunityEligibilityRequest

    profile = OpportunityEligibilityRequest(
        cgpa=8.2,
        branch="Computer Science and Engineering",
        skills=["python", "java", "sql", "git"]
    )
    res = get_active_opportunities(profile)
    assert res.total_opportunities >= 4
    assert res.eligible_count > 0

    # Test Interview Prep Guide Generation
    guide = generate_interview_prep_guide("opp_01")
    assert guide.company == "Amazon"
    assert len(guide.core_technical_topics) > 0
    assert len(guide.sample_coding_questions) > 0
    assert len(guide.revision_schedule_48h) == 4

# Test 9: CareerFit AI Assistant Chatbot (Milestone 2 - Points 16 & 17)
def test_career_assistant_chatbot():
    from backend.app.services.chatbot_service import handle_chat_query
    from backend.app.models.schemas import ChatMessageRequest

    # Test opportunities query
    chat_opp = handle_chat_query(ChatMessageRequest(message="What opportunities do I have this week?"))
    assert "Amazon" in chat_opp.reply or "Microsoft" in chat_opp.reply or "deadline" in chat_opp.reply.lower()
    assert len(chat_opp.suggestions) > 0

    # Test ATS advice query
    chat_ats = handle_chat_query(ChatMessageRequest(message="How do I improve my ATS resume score?"))
    assert "XYZ" in chat_ats.reply or "heading" in chat_ats.reply.lower() or "quantify" in chat_ats.reply.lower()

# Test 10: Enriched Course & Skill Pathway Recommendations (Milestone 2 - Point 15)
def test_enriched_course_recommendations():
    from backend.app.services.gap_analyzer import generate_skill_gap_suggestions

    suggestions = generate_skill_gap_suggestions(["docker", "react", "sql"])
    assert len(suggestions) == 3
    for s in suggestions:
        assert "recommended_course" in s
        assert "estimated_effort" in s
        assert "practice_project" in s

if __name__ == "__main__":
    pytest.main(["-v", __file__])
