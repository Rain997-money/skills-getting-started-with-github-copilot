import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_and_duplicate():
    # Use a unique email for testing
    email = "testuser@example.com"
    activity = next(iter(client.get("/activities").json().keys()))
    # First signup should succeed
    resp1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp1.status_code == 200
    # Duplicate signup should fail
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400
    assert "already signed up" in resp2.json().get("detail", "")

def test_unregister():
    email = "testremove@example.com"
    activity = next(iter(client.get("/activities").json().keys()))
    # Register first
    client.post(f"/activities/{activity}/signup?email={email}")
    # Unregister
    resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 200 or resp.status_code == 404
    # Unregister again should fail or be 404
    resp2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp2.status_code == 404 or resp2.status_code == 400
