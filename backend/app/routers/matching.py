"""
backend/app/routers/matching.py
Route handlers for Resume-to-Job Matching and Skill Gap Analysis.
"""

from fastapi import APIRouter, HTTPException
from backend.app.models.schemas import MatchingRequest, MatchingResponse
from backend.app.services.matcher import match_resume_and_job
from backend.app.services.gap_analyzer import perform_skill_gap_analysis
from backend.app.core.database import save_analysis

router = APIRouter(prefix="/matching", tags=["Matching"])

@router.post("/analyze", response_model=MatchingResponse)
async def analyze_match(payload: MatchingRequest):
    """
    Computes baseline TF-IDF cosine similarity between resume and job description.
    Extracts matched, missing, and additional skills.
    Optionally persists the record to SQLite analysis history.
    """
    if len(payload.resume_text.split()) < 5:
        raise HTTPException(
            status_code=400,
            detail="Resume text is too brief to compute reliable similarity."
        )

    if len(payload.job_text.split()) < 5:
        raise HTTPException(
            status_code=400,
            detail="Job description is too brief to compute reliable similarity."
        )

    match_result = match_resume_and_job(
        resume_text=payload.resume_text,
        job_text=payload.job_text,
        pre_extracted_resume_skills=payload.resume_skills
    )

    gap_data = perform_skill_gap_analysis(
        resume_skills=match_result["resume_skills"],
        job_skills=match_result["job_skills"],
        matched_skills=match_result["matched_skills"],
        missing_skills=match_result["missing_skills"]
    )

    analysis_id = None
    if payload.save_to_history:
        analysis_id = save_analysis(
            resume_filename=payload.resume_filename or "Resume.pdf",
            job_title=payload.job_title or "Target Role",
            similarity_score=match_result["similarity_score"],
            matched_skills=match_result["matched_skills"],
            missing_skills=match_result["missing_skills"],
            resume_skills=match_result["resume_skills"],
            job_skills=match_result["job_skills"]
        )

    return {
        "analysis_id": analysis_id,
        "similarity_score": match_result["similarity_score"],
        "skill_coverage_percentage": match_result["skill_coverage_percentage"],
        "score_type": match_result["score_type"],
        "matched_skills": match_result["matched_skills"],
        "missing_skills": match_result["missing_skills"],
        "additional_skills": match_result["additional_skills"],
        "resume_skills": match_result["resume_skills"],
        "job_skills": match_result["job_skills"],
        "gap_analysis": gap_data,
        "explanation": match_result["explanation"]
    }
