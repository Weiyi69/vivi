import os

os.environ.setdefault("PUBLIC_APP_URL", "http://localhost:3000")
os.environ.setdefault(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:test@127.0.0.1:5432/vivi",
)
os.environ.setdefault(
    "SESSION_SECRET",
    "test-secret-that-is-at-least-32-characters",
)

from fastapi.testclient import TestClient
from pydantic import BaseModel

from app.main import create_app

client = TestClient(create_app())


def test_liveness():
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}
    assert response.headers["X-Request-ID"]


def test_validation_error_format():
    app = create_app()

    class Payload(BaseModel):
        name: str

    @app.post("/test-validation")
    async def validate(payload: Payload):
        return payload

    validation_client = TestClient(app)
    response = validation_client.post("/test-validation", json={})
    assert response.status_code == 422
    assert response.json()["code"] == "validation_error"
