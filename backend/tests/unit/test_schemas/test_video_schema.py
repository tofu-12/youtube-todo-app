"""Unit tests for Video Pydantic schemas."""

import datetime
import uuid

import pytest
from pydantic import ValidationError

from app.crud.schemas.video import (
    VideoFilter,
    VideoInsert,
    VideoResponse,
    VideoUpdate,
)


class TestVideoInsert:
    """Tests for VideoInsert schema."""

    def test_video_insert_required_fields(self):
        """VideoInsert requires user_id, name, url."""
        uid = uuid.uuid4()
        data = VideoInsert(
            user_id=uid, name="Yoga", url="https://example.com"
        )
        assert data.user_id == uid
        assert data.comment is None

    def test_video_insert_with_comment(self):
        """VideoInsert accepts an optional comment."""
        data = VideoInsert(
            user_id=uuid.uuid4(),
            name="Yoga",
            url="https://example.com",
            comment="Great video",
        )
        assert data.comment == "Great video"

    def test_video_insert_missing_name_raises(self):
        """VideoInsert without name raises ValidationError."""
        with pytest.raises(ValidationError):
            VideoInsert(user_id=uuid.uuid4(), url="https://example.com")


class TestVideoUpdate:
    """Tests for VideoUpdate schema."""

    def test_video_update_partial(self):
        """VideoUpdate with partial fields only includes set fields."""
        data = VideoUpdate(name="New Name")
        dumped = data.model_dump(exclude_unset=True)
        assert dumped == {"name": "New Name"}


class TestVideoFilter:
    """Tests for VideoFilter schema."""

    def test_video_filter_requires_user_id(self):
        """VideoFilter requires user_id."""
        uid = uuid.uuid4()
        data = VideoFilter(user_id=uid)
        assert data.user_id == uid


class TestVideoResponse:
    """Tests for VideoResponse schema."""

    def test_video_response_from_attributes(self):
        """VideoResponse can be constructed from a dict-like object."""
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        uid = uuid.uuid4()
        obj = {
            "id": uuid.uuid4(),
            "user_id": uid,
            "name": "Test",
            "url": "https://example.com",
            "comment": None,
            "last_performed_date": None,
            "next_scheduled_date": None,
            "created_at": now,
            "updated_at": now,
        }
        result = VideoResponse.model_validate(obj)
        assert result.name == "Test"
        assert result.user_id == uid
