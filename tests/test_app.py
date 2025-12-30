import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)

def test_signup_success():
    # Test signing up for an activity
    response = client.post("/activities/Chess Club/signup?email=test@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Signed up test@example.com for Chess Club" in data["message"]

    # Check if added
    response = client.get("/activities")
    data = response.json()
    assert "test@example.com" in data["Chess Club"]["participants"]

def test_signup_duplicate():
    # First signup
    client.post("/activities/Basketball Team/signup?email=duplicate@example.com")
    # Second should fail
    response = client.post("/activities/Basketball Team/signup?email=duplicate@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]

def test_signup_invalid_activity():
    response = client.post("/activities/Invalid Activity/signup?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]

def test_unregister_success():
    # First signup
    client.post("/activities/Tennis Club/signup?email=unregister@example.com")
    # Then unregister
    response = client.delete("/activities/Tennis Club/unregister?email=unregister@example.com")
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered unregister@example.com from Tennis Club" in data["message"]

    # Check if removed
    response = client.get("/activities")
    data = response.json()
    assert "unregister@example.com" not in data["Tennis Club"]["participants"]

def test_unregister_not_signed_up():
    response = client.delete("/activities/Art Studio/unregister?email=notsigned@example.com")
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]

def test_unregister_invalid_activity():
    response = client.delete("/activities/Invalid Activity/unregister?email=test@example.com")
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]