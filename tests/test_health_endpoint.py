from fastapi.testclient import TestClient

from app.main import app


def test_health_endpoint_returns_expected_shape():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert "status" in payload
    assert "database" in payload
    assert "scheduler_running" in payload
