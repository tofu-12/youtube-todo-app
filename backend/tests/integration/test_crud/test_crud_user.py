"""Integration tests for User CRUD operations."""

import datetime
import uuid

from app.crud.schemas.user import UserInsert, UserUpdate
from app.crud.user import create_user, get_user, update_user


class TestCreateUser:
    """Tests for create_user."""

    def test_create_user_defaults(self, db):
        """Creating a user with defaults yields 00:00 and Asia/Tokyo."""
        data = UserInsert(email="defaults@example.com")
        result = create_user(db, data)

        assert result.day_change_time == datetime.time(0, 0)
        assert result.timezone == "Asia/Tokyo"
        assert result.email == "defaults@example.com"
        assert result.id is not None
        assert result.created_at is not None
        assert result.updated_at is not None

    def test_create_user_custom_values(self, db):
        """Creating a user with custom values stores them correctly."""
        data = UserInsert(
            email="custom@example.com",
            day_change_time=datetime.time(5, 0),
            timezone="UTC",
        )
        result = create_user(db, data)

        assert result.day_change_time == datetime.time(5, 0)
        assert result.timezone == "UTC"


class TestGetUser:
    """Tests for get_user."""

    def test_get_user_found(self, db, sample_user):
        """Getting an existing user returns the correct data."""
        result = get_user(db, sample_user.id)

        assert result is not None
        assert result.id == sample_user.id
        assert result.timezone == sample_user.timezone

    def test_get_user_not_found(self, db):
        """Getting a nonexistent user returns None."""
        result = get_user(db, uuid.uuid4())
        assert result is None


class TestUpdateUser:
    """Tests for update_user."""

    def test_update_user_timezone(self, db, sample_user):
        """Updating timezone changes only that field."""
        data = UserUpdate(timezone="UTC")
        result = update_user(db, sample_user.id, data)

        assert result is not None
        assert result.timezone == "UTC"
        assert result.day_change_time == sample_user.day_change_time

    def test_update_user_day_change_time(self, db, sample_user):
        """Updating day_change_time changes only that field."""
        new_time = datetime.time(4, 30)
        data = UserUpdate(day_change_time=new_time)
        result = update_user(db, sample_user.id, data)

        assert result is not None
        assert result.day_change_time == new_time
        assert result.timezone == sample_user.timezone

    def test_update_user_not_found(self, db):
        """Updating a nonexistent user returns None."""
        data = UserUpdate(timezone="UTC")
        result = update_user(db, uuid.uuid4(), data)
        assert result is None

    def test_update_user_no_changes(self, db, sample_user):
        """Updating with empty data keeps existing values."""
        data = UserUpdate()
        result = update_user(db, sample_user.id, data)

        assert result is not None
        assert result.timezone == sample_user.timezone
        assert result.day_change_time == sample_user.day_change_time
