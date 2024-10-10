from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict
from src.services.analytics_service import get_analytics_summary, get_event_analysis

router = APIRouter()

class AnalyticsSummary(BaseModel):
    total_events: int
    high_risk_events: int
    medium_risk_events: int
    low_risk_events: int

class EventAnalysis(BaseModel):
    event_id: str
    risk_level: str
    action: str
    analysis: str

@router.get("/summary", response_model=AnalyticsSummary, summary="Get analytics summary")
async def analytics_summary():
    """
    Get a summary of analytics data.

    Returns:
        AnalyticsSummary: Summary containing total and categorized event counts.
    """
    try:
        summary = get_analytics_summary()
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/event/{event_id}", response_model=EventAnalysis, summary="Get analysis for a specific event")
async def event_analysis(event_id: str):
    """
    Get detailed analysis for a specific event.

    Args:
        event_id (str): The ID of the event.

    Returns:
        EventAnalysis: Detailed analysis of the event.
    """
    try:
        analysis = get_event_analysis(event_id)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))