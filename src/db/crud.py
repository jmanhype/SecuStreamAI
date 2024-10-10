from sqlalchemy.orm import Session
from src.models.event import Event

def create_event(db: Session, event_data: dict):
    event = Event(**event_data)
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def get_event(db: Session, event_id: int):
    return db.query(Event).filter(Event.id == event_id).first()

def get_events(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Event).offset(skip).limit(limit).all()

def update_event(db: Session, event_id: int, event_data: dict):
    event = db.query(Event).filter(Event.id == event_id).first()
    for key, value in event_data.items():
        setattr(event, key, value)
    db.commit()
    db.refresh(event)
    return event

def delete_event(db: Session, event_id: int):
    event = db.query(Event).filter(Event.id == event_id).first()
    db.delete(event)
    db.commit()
    return event