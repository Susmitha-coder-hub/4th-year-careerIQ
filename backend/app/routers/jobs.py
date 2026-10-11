"""
backend/app/routers/jobs.py
Route handlers for Job Description analysis and skill extraction.
"""

from fastapi import APIRouter, HTTPException
from backend.app.models.schemas import JobAnalysisRequest, JobAnalysisResponse
from backend.app.services.skill_extractor import extract_skills_from_text, categorize_skills

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/analyze", response_model=JobAnalysisResponse)
async def analyze_job_description(payload: JobAnalysisRequest):
    """
    Validates job description text, extracts recognized technical skills,
    and returns a structured domain breakdown.
    """
    raw_text = payload.job_description.strip()
    if len(raw_text.split()) < 5:
        raise HTTPException(
            status_code=400,
            detail="Job description is too brief. Please enter at least 1-2 descriptive paragraphs with role requirements."
        )

    skills = extract_skills_from_text(raw_text)
    categorized = categorize_skills(skills)

    return {
        "job_title": payload.job_title or "Target Role",
        "word_count": len(raw_text.split()),
        "detected_skills": skills,
        "categorized_skills": categorized
    }
