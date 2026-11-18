"""
backend/app/routers/opportunities.py
Router for Opportunity Intelligence & Placement Reminders (Milestone 2 - Points 11-14)
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from backend.app.models.schemas import (
    OpportunityEligibilityRequest,
    OpportunityListResponse,
    InterviewPrepGuideResponse
)
from backend.app.services.opportunity_service import (
    get_active_opportunities,
    generate_interview_prep_guide
)

router = APIRouter(prefix="/opportunities", tags=["Opportunity Intelligence"])

@router.get("/", response_model=OpportunityListResponse)
def list_opportunities(
    cgpa: float = Query(7.5, ge=0.0, le=10.0),
    branch: str = Query("Computer Science and Engineering")
):
    """
    Returns active opportunities with automated eligibility & urgency computation.
    """
    try:
        profile = OpportunityEligibilityRequest(cgpa=cgpa, branch=branch, skills=[])
        return get_active_opportunities(profile)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch opportunities: {str(e)}")

@router.post("/check-eligibility", response_model=OpportunityListResponse)
def check_eligibility(profile: OpportunityEligibilityRequest):
    """
    Evaluates complete student profile (CGPA, branch, and skills) against active opportunities.
    """
    try:
        return get_active_opportunities(profile)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to evaluate eligibility: {str(e)}")

@router.get("/prep-guide/{opportunity_id}", response_model=InterviewPrepGuideResponse)
def get_prep_guide(opportunity_id: str):
    """
    Generates a 48-Hour Interview Preparation Guide for a specific placement opportunity.
    """
    try:
        return generate_interview_prep_guide(opportunity_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate prep guide: {str(e)}")
