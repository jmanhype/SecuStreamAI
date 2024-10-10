from fastapi import APIRouter, HTTPException
from typing import List
from pydantic import BaseModel
import json
import logging
from api import dependencies
from services.kafka_client import produce_event
from pipeline.event_pipeline import process_event
from services.redis_client import redis_client  # New import
from config import settings  # Add this import
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.models.db_models import Event as DBEvent

router = APIRouter()
logger = logging.getLogger(__name__)

class Event(BaseModel):
    event_type: str
    timestamp: int
    source_ip: str
    destination_ip: str
    severity: str
    description: str
    user_id: str
    device_id: str

@router.post("/", status_code=201, summary="Create a new security event")
async def create_event(event: Event, db: Session = dependencies(get_db)):
    """
    Create a new security event by producing it to Kafka, processing it, and storing in the database.

    Args:
        event (Event): The security event data.
        db (Session): Database session.

    Returns:
        dict: Confirmation message with the processing result.
    """
    try:
        # Produce event to Kafka
        await produce_event(settings.KAFKA_TOPIC, event.dict())
        
        # Process the event
        result = await process_event(event.dict())
        
        # Store event in the database
        db_event = DBEvent(**event.dict(), **result)
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        
        return {"message": "Event created and processed successfully", "result": result}
    except Exception as e:
        logger.error(f"Failed to create and process event: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[Event], summary="Retrieve all security events")
async def get_events():
    """
    Retrieve all security events.

    Returns:
        List[Event]: A list of all security events.
    """
    try:
        # Fetch events from Redis cache
        events = []
        keys = redis_client.redis.scan_iter("event:*")
        for key in keys:
            event_data = redis_client.get(key)
            if event_data:
                events.append(Event(**event_data))
        return events
    except Exception as e:
        logger.error(f"Error fetching events: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve events")