"""
backend/app/routers/prediction.py
Router for Placement Readiness Prediction (Milestone 2 - Points 4 & 10)
"""

from fastapi import APIRouter, HTTPException
from backend.app.models.schemas import (
    PlacementPredictionRequest,
    PlacementPredictionResponse
)
from backend.app.services.prediction_engine import evaluate_placement_readiness

router = APIRouter(prefix="/prediction", tags=["Placement Prediction"])

@router.post("/placement-readiness", response_model=PlacementPredictionResponse)
def predict_placement_readiness(profile: PlacementPredictionRequest):
    """
    Evaluates multi-factor profile readiness for campus placements.
    Returns composite score (0-100), dimensional breakdown, strengths, and prep plan.
    """
    try:
        return evaluate_placement_readiness(profile)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to evaluate placement readiness: {str(e)}")
