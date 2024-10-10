import pytest
from sqlalchemy.orm import Session
from src.db.database import get_db
from src.db.models import Event
from src.db.crud import create_event, get_event, get_events, update_event, delete_event

@pytest.fixture(scope="module")
def db():
    db = next(get_db())
    yield db
    db.close()

def test_create_event(db: Session):
    event_data = {
        "event_type": "test_event",
        "timestamp": 1633036800,
        "source_ip": "192.168.1.100",
        "destination_ip": "10.0.0.1",
        "severity": "medium",
        "description": "Test event",
    }
    event = create_event(db, event_data)
    assert event.id is not None
    assert event.event_type == "test_event"

def test_get_event(db: Session):
    event_data = {
        "event_type": "get_test",
        "timestamp": 1633036800,
        "source_ip": "192.168.1.101",
        "destination_ip": "10.0.0.2",
        "severity": "low",
        "description": "Get test event",
    }
    created_event = create_event(db, event_data)
    retrieved_event = get_event(db, created_event.id)
    assert retrieved_event is not None
    assert retrieved_event.event_type == "get_test"

def test_get_events(db: Session):
    events = get_events(db)
    assert isinstance(events, list)
    assert all(isinstance(event, Event) for event in events)

def test_update_event(db: Session):
    event_data = {
        "event_type": "update_test",
        "timestamp": 1633036800,
        "source_ip": "192.168.1.102",
        "destination_ip": "10.0.0.3",
        "severity": "high",
        "description": "Update test event",
    }
    event = create_event(db, event_data)
    updated_data = {"severity": "critical"}
    updated_event = update_event(db, event.id, updated_data)
    assert updated_event.severity == "critical"

def test_delete_event(db: Session):
    event_data = {
        "event_type": "delete_test",
        "timestamp": 1633036800,
        "source_ip": "192.168.1.103",
        "destination_ip": "10.0.0.4",
        "severity": "medium",
        "description": "Delete test event",
    }
    event = create_event(db, event_data)
    delete_event(db, event.id)
    assert get_event(db, event.id) is None