from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["air_gapped_ready"] is True


def test_routers() -> None:
    response = client.get("/routers")
    assert response.status_code == 200
    assert len(response.json()) >= 4
