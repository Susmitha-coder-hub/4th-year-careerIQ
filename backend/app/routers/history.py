"""
backend/app/routers/history.py
Route handlers for SQLite analysis history and real dashboard metrics.
"""

from fastapi import APIRouter, HTTPException
from typing import List
from backend.app.models.schemas import AnalysisHistoryItem, DashboardStatsResponse
from backend.app.core.database import get_all_analyses, delete_analysis, get_dashboard_metrics

router = APIRouter(tags=["History & Metrics"])

@router.get("/history", response_model=List[AnalysisHistoryItem])
async def list_history():
    """Returns all past analysis records saved in the SQLite database."""
    return get_all_analyses()

@router.delete("/history/{analysis_id}")
async def remove_history(analysis_id: int):
    """Deletes an analysis record by ID."""
    success = delete_analysis(analysis_id)
    if not success:
        raise HTTPException(status_code=404, detail="Analysis record not found.")
    return {"status": "success", "message": f"Analysis record {analysis_id} deleted successfully."}

@router.get("/dashboard/stats", response_model=DashboardStatsResponse)
async def get_stats():
    """Calculates and returns real metrics from SQLite activity."""
    return get_dashboard_metrics()
