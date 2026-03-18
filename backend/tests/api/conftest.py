import pytest
from fastapi.testclient import TestClient

from app.core.dependencies import get_current_user, get_db
from app.main import app


@pytest.fixture()
def client(db, sample_user):
    """Create a TestClient with dependency overrides for db and current user."""
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[get_current_user] = lambda: sample_user
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
