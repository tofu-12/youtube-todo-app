from fastapi.testclient import TestClient

from app.main import app


class TestHealthCheck:
    def test_health_check(self):
        """GET /health returns 200 with status ok."""
        with TestClient(app) as client:
            response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}
