import json
from typing import Dict
from api import dependencies
from core.config import settings
from services.redis_client import redis_client
import logging
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.models.db_models import Event as DBEvent
from sqlalchemy import func
from fastapi import Depends

logger = logging.getLogger(__name__)

def get_analytics_summary(db: Session = Depends(get_db)) -> Dict:
    """
    Retrieve a summary of analytics data from the database.

    Args:
        db (Session): Database session.

    Returns:
        Dict: Summary containing total and categorized event counts.
    """
    try:
        total_events = db.query(func.count(DBEvent.id)).scalar()
        high_risk_events = db.query(func.count(DBEvent.id)).filter(DBEvent.risk_level == "high").scalar()
        medium_risk_events = db.query(func.count(DBEvent.id)).filter(DBEvent.risk_level == "medium").scalar()
        low_risk_events = db.query(func.count(DBEvent.id)).filter(DBEvent.risk_level == "low").scalar()

        return {
            "total_events": total_events,
            "high_risk_events": high_risk_events,
            "medium_risk_events": medium_risk_events,
            "low_risk_events": low_risk_events
        }
    except Exception as e:
        logger.error(f"Error retrieving analytics summary: {e}")
        return {
            "total_events": 0,
            "high_risk_events": 0,
            "medium_risk_events": 0,
            "low_risk_events": 0
        }

def get_event_analysis(event_id: str, db: Session = dependencies(get_db)) -> Dict:
    """
    Retrieve detailed analysis for a specific event from the database.

    Args:
        event_id (str): The ID of the event.
        db (Session): Database session.

    Returns:
        Dict: Detailed analysis of the event.
    """
    try:
        event = db.query(DBEvent).filter(DBEvent.id == event_id).first()
        if event:
            return {
                "event_id": event.id,
                "risk_level": event.risk_level,
                "action": event.action,
                "analysis": event.analysis
            }
        else:
            return {
                "event_id": event_id,
                "analysis": "No analysis found for this event."
            }
    except Exception as e:
        logger.error(f"Error retrieving analysis for event {event_id}: {e}")
        return {
            "event_id": event_id,
            "analysis": "Error retrieving analysis."
        }

def update_risk_counters(risk_level: str):
    """
    Update the counters for different risk levels.

    Args:
        risk_level (str): The risk level of the event.
    """
    try:
        # Increment total events
        new_total = redis_client.increment("total_events") or 0

        # Define mapping for risk levels
        key_map = {
            "high": "high_risk_events",
            "medium": "medium_risk_events",
            "low": "low_risk_events"
        }

        key = key_map.get(risk_level.lower())
        if key:
            new_count = redis_client.increment(key) or 0
            logger.info(f"Updated '{key}' counter to {new_count}.")
        else:
            logger.warning(f"Unknown risk level: {risk_level}")
    except Exception as e:
        logger.error(f"Error updating risk counters: {e}")