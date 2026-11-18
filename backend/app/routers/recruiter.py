"""
backend/app/routers/recruiter.py
Router for Recruiter Multi-Resume Ranking (Milestone 2 - Point 9)
"""

from fastapi import APIRouter, HTTPException
from backend.app.models.schemas import (
    RecruiterRankingRequest,
    RecruiterRankingResponse
)
from backend.app.services.recruiter_ranker import rank_candidates_against_jd

router = APIRouter(prefix="/recruiter", tags=["Recruiter Comparison"])

@router.post("/rank-resumes", response_model=RecruiterRankingResponse)
def rank_resumes(request: RecruiterRankingRequest):
    """
    Ranks multiple candidate resumes against a single Job Description.
    Returns sorted candidates with match scores, match tiers, and hiring rationale.
    """
    try:
        if not request.candidates:
            raise HTTPException(status_code=400, detail="Candidate list cannot be empty.")
        return rank_candidates_against_jd(request)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to rank candidate resumes: {str(e)}")
