from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to CivicRoute AI"


def test_health():
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_report():
    report = {
        "category": "pothole",
        "description": (
            "A large pothole near the bus stop is causing "
            "motorcycles to swerve."
        ),
        "location_zone": "Ward-12",
        "latitude": 21.1458,
        "longitude": 79.0882,
    }

    response = client.post("/api/v1/reports", json=report)

    assert response.status_code == 201
    assert response.json()["message"] == "Report submitted successfully"
    assert response.json()["status"] == "SUBMITTED"
    assert "id" in response.json()


def test_invalid_category():
    report = {
        "category": "unknown_problem",
        "description": "A damaged road near the market.",
        "location_zone": "Ward-12",
    }

    response = client.post("/api/v1/reports", json=report)

    assert response.status_code == 422


def test_invalid_latitude():
    report = {
        "category": "pothole",
        "description": "A large pothole near the market.",
        "location_zone": "Ward-12",
        "latitude": 95,
        "longitude": 79.0882,
    }

    response = client.post("/api/v1/reports", json=report)

    assert response.status_code == 422

