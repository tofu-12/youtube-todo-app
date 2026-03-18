"""Unit tests for User Pydantic schemas."""

import datetime
import uuid

from app.crud.schemas.user import UserInsert, UserResponse, UserUpdate


class TestUserInsert:
    """Tests for UserInsert schema."""

    def test_user_insert_defaults(self):
        """UserInsert provides sensible defaults."""
        data = UserInsert()
        assert data.day_change_time == datetime.time(0, 0)
        assert data.timezone == "Asia/Tokyo"

    def test_user_insert_custom(self):
        """UserInsert accepts custom values."""
        data = UserInsert(
            day_change_time=datetime.time(5, 0), timezone="UTC"
        )
        assert data.day_change_time == datetime.time(5, 0)
        assert data.timezone == "UTC"


class TestUserUpdate:
    """Tests for UserUpdate schema."""

    def test_user_update_all_none(self):
        """UserUpdate defaults all fields to None."""
        data = UserUpdate()
        assert data.day_change_time is None
        assert data.timezone is None

    def test_user_update_partial(self):
        """UserUpdate with partial fields only includes set fields."""
        data = UserUpdate(timezone="UTC")
        dumped = data.model_dump(exclude_unset=True)
        assert "timezone" in dumped
        assert "day_change_time" not in dumped


class TestUserResponse:
    """Tests for UserResponse schema."""

    def test_user_response_from_attributes(self):
        """UserResponse can be constructed from a dict-like object."""
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        obj = {
            "id": uuid.uuid4(),
            "day_change_time": datetime.time(0, 0),
            "timezone": "Asia/Tokyo",
            "created_at": now,
            "updated_at": now,
        }
        result = UserResponse.model_validate(obj)
        assert result.timezone == "Asia/Tokyo"
        assert result.id == obj["id"]
