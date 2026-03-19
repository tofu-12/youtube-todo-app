"""Tests for authentication endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.core.dependencies import get_db
from app.main import app


@pytest.fixture()
def auth_client(db):
    """TestClient without user override (for auth endpoints)."""
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


class TestRegister:
    """Tests for POST /api/auth/register."""

    def test_register_success(self, auth_client):
        """New email should create a user and return 201."""
        res = auth_client.post(
            "/api/auth/register", json={"email": "new@example.com"}
        )
        assert res.status_code == 201
        body = res.json()
        assert body["email"] == "new@example.com"
        assert "id" in body

    def test_register_duplicate_email(self, auth_client):
        """Registering the same email twice should return 409."""
        auth_client.post(
            "/api/auth/register", json={"email": "dup@example.com"}
        )
        res = auth_client.post(
            "/api/auth/register", json={"email": "dup@example.com"}
        )
        assert res.status_code == 409

    def test_register_invalid_email(self, auth_client):
        """Email without @ should return 422."""
        res = auth_client.post(
            "/api/auth/register", json={"email": "invalid"}
        )
        assert res.status_code == 422


class TestLogin:
    """Tests for POST /api/auth/login."""

    def test_login_success(self, auth_client):
        """Registered email should return 200 with user data."""
        auth_client.post(
            "/api/auth/register", json={"email": "login@example.com"}
        )
        res = auth_client.post(
            "/api/auth/login", json={"email": "login@example.com"}
        )
        assert res.status_code == 200
        assert res.json()["email"] == "login@example.com"

    def test_login_not_found(self, auth_client):
        """Unregistered email should return 404."""
        res = auth_client.post(
            "/api/auth/login", json={"email": "nobody@example.com"}
        )
        assert res.status_code == 404


class TestXUserIdHeader:
    """Tests for X-User-Id header requirement on protected endpoints."""

    def test_missing_header_returns_422(self, auth_client):
        """Calling a protected endpoint without X-User-Id should return 422."""
        res = auth_client.get("/api/videos")
        assert res.status_code == 422
