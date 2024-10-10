import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.auth.jwt_handler import create_access_token, decode_access_token
from src.auth.auth_bearer import JWTBearer

client = TestClient(app)

@pytest.fixture
def auth_header():
    token = create_access_token({"sub": "testuser"})
    return {"Authorization": f"Bearer {token}"}

def test_create_and_decode_access_token():
    payload = {"sub": "testuser", "role": "admin"}
    token = create_access_token(payload)
    decoded = decode_access_token(token)
    assert decoded["sub"] == "testuser"
    assert decoded["role"] == "admin"

def test_protected_route_with_valid_token(auth_header):
    response = client.get("/api/v1/protected", headers=auth_header)
    assert response.status_code == 200

def test_protected_route_without_token():
    response = client.get("/api/v1/protected")
    assert response.status_code == 403

def test_protected_route_with_invalid_token():
    response = client.get("/api/v1/protected", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 403

def test_jwt_bearer():
    bearer = JWTBearer()
    token = create_access_token({"sub": "testuser"})
    assert bearer(f"Bearer {token}") == token

def test_jwt_bearer_invalid_scheme():
    bearer = JWTBearer()
    token = create_access_token({"sub": "testuser"})
    with pytest.raises(Exception):
        bearer(f"NotBearer {token}")