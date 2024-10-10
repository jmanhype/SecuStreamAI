import pytest
from fastapi import HTTPException
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.exceptions.custom_exceptions import EventNotFoundException, InvalidEventDataException

app = FastAPI()

def test_event_not_found_exception():
    with pytest.raises(EventNotFoundException) as exc_info:
        raise EventNotFoundException(event_id=123)
    assert exc_info.value.status_code == 404
    assert "Event with id 123 not found" in str(exc_info.value.detail)

def test_invalid_event_data_exception():
    with pytest.raises(InvalidEventDataException) as exc_info:
        raise InvalidEventDataException("Invalid event type")
    assert exc_info.value.status_code == 400
    assert "Invalid event type" in str(exc_info.value.detail)

def test_http_exception_handling():
    @app.get("/test-exception")
    async def test_exception():
        raise HTTPException(status_code=418, detail="I'm a teapot")

    client = TestClient(app)
    response = client.get("/test-exception")
    assert response.status_code == 418
    assert response.json()["detail"] == "I'm a teapot"