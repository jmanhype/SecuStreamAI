import pytest
from fastapi.testclient import TestClient
from src.main import app
import time

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to SecuStreamAI"}

def test_create_event():
    event = {
        "context": "login",
        "event_description": "Failed login attempt",
        "severity": "medium",
        "source_ip": "192.168.1.100",
        "destination_ip": "10.0.0.1"
    }
    response = client.post("/api/v1/events", json=event)
    assert response.status_code == 200
    assert "event_id" in response.json()

def test_get_event():
    # First, create an event
    event = {
        "context": "network",
        "event_description": "Unusual outbound traffic",
        "severity": "high",
        "source_ip": "192.168.1.100",
        "destination_ip": "203.0.113.0"
    }
    create_response = client.post("/api/v1/events", json=event)
    event_id = create_response.json()["event_id"]

    # Now, retrieve the event
    get_response = client.get(f"/api/v1/events/{event_id}")
    assert get_response.status_code == 200
    assert get_response.json()["event_description"] == "Unusual outbound traffic"

def test_analyze_event():
    event = {
        "context": "system",
        "event_description": "Unexpected process termination",
        "severity": "high",
        "process_id": "1234"
    }
    response = client.post("/api/v1/analyze", json=event)
    assert response.status_code == 200
    assert "risk_level" in response.json()
    assert "action" in response.json()
    assert "analysis" in response.json()

def test_invalid_event_data():
    invalid_event_data = {
        "event_type": "invalid_type",
        "timestamp": "not_a_timestamp",
    }
    response = client.post("/api/v1/events/", json=invalid_event_data)
    assert response.status_code == 422  # Unprocessable Entity

def test_get_event_by_id():
    # First, create an event
    event_data = {
        "event_type": "login_attempt",
        "timestamp": 1633036800,
        "source_ip": "192.168.1.100",
        "destination_ip": "10.0.0.1",
        "severity": "low",
        "description": "Successful login",
        "user_id": "user_9012",
        "device_id": "device_345"
    }
    create_response = client.post("/api/v1/events/", json=event_data)
    event_id = create_response.json()["id"]

    # Now, get the event by ID
    response = client.get(f"/api/v1/events/{event_id}")
    assert response.status_code == 200
    assert response.json()["id"] == event_id

def test_get_nonexistent_event():
    response = client.get("/api/v1/events/99999")
    assert response.status_code == 404

def test_create_event_with_missing_fields():
    incomplete_event_data = {
        "event_type": "login_attempt",
        "timestamp": 1633036800
    }
    response = client.post("/api/v1/events/", json=incomplete_event_data)
    assert response.status_code == 422

def test_create_event_with_invalid_event_type():
    invalid_event_data = {
        "event_type": "invalid_type",
        "timestamp": 1633036800,
        "source_ip": "192.168.1.100",
        "destination_ip": "10.0.0.1",
        "severity": "medium",
        "description": "Test event",
        "user_id": "user_1234",
        "device_id": "device_567"
    }
    response = client.post("/api/v1/events/", json=invalid_event_data)
    assert response.status_code == 422

@pytest.mark.parametrize("invalid_severity", ["low", "MEDIUM", "critical"])
def test_create_event_with_invalid_severity(invalid_severity):
    event_data = {
        "event_type": "login_attempt",
        "timestamp": 1633036800,
        "source_ip": "192.168.1.100",
        "destination_ip": "10.0.0.1",
        "severity": invalid_severity,
        "description": "Test event",
        "user_id": "user_1234",
        "device_id": "device_567"
    }
    response = client.post("/api/v1/events/", json=event_data)
    assert response.status_code == 422

def test_get_events_pagination():
    # First, create multiple events
    for _ in range(15):
        client.post("/api/v1/events/", json={
            "event_type": "login_attempt",
            "timestamp": 1633036800,
            "source_ip": "192.168.1.100",
            "destination_ip": "10.0.0.1",
            "severity": "medium",
            "description": "Test event",
            "user_id": "user_1234",
            "device_id": "device_567"
        })
    
    # Test pagination
    response = client.get("/api/v1/events/?page=1&per_page=10")
    assert response.status_code == 200
    events = response.json()
    assert len(events) == 10

    response = client.get("/api/v1/events/?page=2&per_page=10")
    assert response.status_code == 200
    events = response.json()
    assert len(events) == 5

def test_analyze_event_with_invalid_data():
    invalid_event_data = {
        "event_type": "network_traffic",
        "timestamp": "invalid_timestamp",
        "severity": "ultra_high",
    }
    response = client.post("/api/v1/analyze/", json=invalid_event_data)
    assert response.status_code == 422

def test_create_event_with_invalid_data():
    invalid_event = {
        "event_type": "invalid_type",
        "timestamp": "not_a_timestamp",
        "severity": "ultra_high"
    }
    response = client.post("/api/v1/events", json=invalid_event)
    assert response.status_code == 422
    assert "detail" in response.json()

def test_analyze_nonexistent_event():
    response = client.post("/api/v1/analyze/", json={"event_id": 99999})
    assert response.status_code == 404
    assert "Event not found" in response.json()["detail"]

@pytest.mark.parametrize("invalid_id", ["abc", "-1", "0"])
def test_get_event_with_invalid_id(invalid_id):
    response = client.get(f"/api/v1/events/{invalid_id}")
    assert response.status_code == 422

def test_analyze_event_with_missing_fields():
    incomplete_event = {
        "event_type": "login_attempt"
    }
    response = client.post("/api/v1/analyze", json=incomplete_event)
    assert response.status_code == 422

def test_sql_injection_prevention():
    malicious_input = "'; DROP TABLE events; --"
    response = client.get(f"/api/v1/events/?search={malicious_input}")
    assert response.status_code != 500  # Ensure the server doesn't crash
    # Add more assertions based on your expected behavior

def test_xss_prevention():
    malicious_input = "<script>alert('XSS')</script>"
    event_data = {
        "event_type": "test",
        "description": malicious_input,
        "timestamp": int(time.time()),
        "severity": "low"
    }
    response = client.post("/api/v1/events/", json=event_data)
    assert response.status_code == 201
    event_id = response.json()["id"]
    
    # Retrieve the event and check if the script tag is escaped
    response = client.get(f"/api/v1/events/{event_id}")
    assert response.status_code == 200
    assert "<script>" not in response.text

def test_rate_limiting():
    for _ in range(100):
        response = client.get("/api/v1/events")
    assert response.status_code == 429  # Too Many Requests

def test_jwt_token_expiration():
    # Assuming you have an endpoint that requires authentication
    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImV4cCI6MTUxNjIzOTAyMn0.L8i6g3PfcHlioHCCPURC9pmXT7gdJpx3kOVdycWgx94"
    response = client.get("/api/v1/protected", headers={"Authorization": f"Bearer {expired_token}"})
    assert response.status_code == 401
    assert "Token has expired" in response.json()["detail"]

def test_csrf_protection():
    # Assuming you have CSRF protection enabled
    response = client.post("/api/v1/events/", json={}, headers={"X-CSRFToken": "invalid_token"})
    assert response.status_code == 403
    assert "CSRF" in response.json()["detail"]