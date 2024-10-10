import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.db.database import get_db
from src.models.event import Event
from sqlalchemy.orm import Session
from src.message_brokers.kafka_producer import produce_event
from src.services.redis_client import RedisClient
from src.pipeline.model_inference import perform_inference

client = TestClient(app)

@pytest.fixture(scope="module")
def db():
    db = next(get_db())
    yield db
    db.close()

@pytest.fixture
def redis_client():
    return RedisClient()

def test_end_to_end_event_flow_with_kafka_and_cache(db: Session, redis_client, mocker):
    # Mock Kafka producer
    mock_produce = mocker.patch('src.message_brokers.kafka_producer.produce_event')
    
    # Create an event
    event_data = {
        "event_type": "login_attempt",
        "timestamp": 1633036800,
        "source_ip": "192.168.1.100",
        "destination_ip": "10.0.0.1",
        "severity": "medium",
        "description": "Failed login attempt from unusual location",
        "user_id": "user_1234",
        "device_id": "device_567"
    }
    response = client.post("/api/v1/events/", json=event_data)
    assert response.status_code == 201
    event_id = response.json()["id"]

    # Verify event is produced to Kafka
    mock_produce.assert_called_once()

    # Retrieve the event
    response = client.get(f"/api/v1/events/{event_id}")
    assert response.status_code == 200
    assert response.json()["event_type"] == "login_attempt"

    # Verify event is cached
    cached_event = redis_client.get(f"event:{event_id}")
    assert cached_event is not None

    # Analyze the event
    response = client.post("/api/v1/analyze/", json=event_data)
    assert response.status_code == 200
    analysis = response.json()
    assert "risk_level" in analysis
    assert "action" in analysis
    assert "analysis" in analysis

    # Verify event is stored in the database
    db_event = db.query(Event).filter(Event.id == event_id).first()
    assert db_event is not None
    assert db_event.event_type == "login_attempt"

def test_component_interaction(mocker):
    mock_kafka = mocker.patch('src.message_brokers.kafka_producer.produce_event')
    mock_redis = mocker.patch('src.cache.redis_client.RedisClient.set')
    mock_db = mocker.patch('src.db.crud.create_event')
    mock_analyze = mocker.patch('src.pipeline.model_inference.perform_inference')

    event_data = {
        "event_type": "network_traffic",
        "timestamp": 1633036800,
        "source_ip": "192.168.1.100",
        "destination_ip": "10.0.0.1",
        "severity": "high",
        "description": "Unusual outbound traffic",
    }

    response = client.post("/api/v1/events/", json=event_data)
    assert response.status_code == 201

    mock_kafka.assert_called_once()
    mock_redis.assert_called_once()
    mock_db.assert_called_once()
    mock_analyze.assert_called_once()

def test_high_load_scenario():
    events = [
        {
            "event_type": "network_traffic",
            "timestamp": 1633036800 + i,
            "source_ip": f"192.168.1.{i % 255}",
            "destination_ip": f"10.0.0.{i % 255}",
            "severity": "low",
            "description": f"Test event {i}",
            "user_id": f"user_{i}",
            "device_id": f"device_{i}"
        }
        for i in range(100)
    ]

    for event in events:
        response = client.post("/api/v1/events/", json=event)
        assert response.status_code == 201

    response = client.get("/api/v1/events/?page=1&per_page=50")
    assert response.status_code == 200
    assert len(response.json()) == 50

@pytest.mark.asyncio
async def test_adaptive_hybrid_approach(db: Session, redis_client, mocker):
    mock_kafka = mocker.patch('src.message_brokers.kafka_producer.produce_event')
    mock_rule_based = mocker.patch('src.pipeline.model_inference.rule_based_inference')
    mock_pytorch = mocker.patch('src.pipeline.model_inference.pytorch_inference')
    mock_dspy = mocker.patch('src.pipeline.model_inference.dspy_inference')

    events = [
        {"context": "login", "event_description": "Successful login", "severity": "low"},
        {"context": "network", "event_description": "Unusual traffic pattern", "severity": "high"},
        {"context": "system", "event_description": "New process created", "severity": "medium"}
    ]

    for event in events:
        response = client.post("/api/v1/events/", json=event)
        assert response.status_code == 201
        event_id = response.json()["id"]

        analysis_response = client.post("/api/v1/analyze/", json={"event_id": event_id})
        assert analysis_response.status_code == 200
        analysis = analysis_response.json()

        assert "risk_level" in analysis
        assert "action" in analysis
        assert "analysis" in analysis

    mock_kafka.assert_called()
    mock_rule_based.assert_called()
    mock_pytorch.assert_called()
    mock_dspy.assert_called()

    # Verify adaptive behavior
    event_counts = await perform_inference({"get_event_counts": True})
    assert "rule_based" in event_counts
    assert "pytorch" in event_counts
    assert "dspy" in event_counts