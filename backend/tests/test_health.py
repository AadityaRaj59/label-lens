from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_api_metadata() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["name"] == "LabelLens API"
    assert response.json()["docs"] == "/docs"


def test_health_endpoint() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "labellens-api"}
