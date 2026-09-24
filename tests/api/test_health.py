from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_api_is_running():
    response = client.get("/docs")

    assert response.status_code == 200