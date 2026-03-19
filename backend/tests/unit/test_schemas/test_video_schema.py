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

VALID_YOUTUBE_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


class TestVideoInsert:
    """Tests for VideoInsert schema."""

    def test_video_insert_required_fields(self):
        """VideoInsert requires user_id, name, url."""
        uid = uuid.uuid4()
        data = VideoInsert(
            user_id=uid, name="Yoga", url=VALID_YOUTUBE_URL
        )
        assert data.user_id == uid
        assert data.comment is None

    def test_video_insert_with_comment(self):
        """VideoInsert accepts an optional comment."""
        data = VideoInsert(
            user_id=uuid.uuid4(),
            name="Yoga",
            url=VALID_YOUTUBE_URL,
            comment="Great video",
        )
        assert data.comment == "Great video"

    def test_video_insert_missing_name_raises(self):
        """VideoInsert without name raises ValidationError."""
        with pytest.raises(ValidationError):
            VideoInsert(user_id=uuid.uuid4(), url=VALID_YOUTUBE_URL)

    def test_video_insert_invalid_url_raises(self):
        """VideoInsert with non-YouTube URL raises ValidationError."""
        with pytest.raises(ValidationError, match="YouTube URL"):
            VideoInsert(
                user_id=uuid.uuid4(),
                name="Yoga",
                url="https://example.com",
            )

    def test_video_insert_random_string_url_raises(self):
        """VideoInsert with random string raises ValidationError."""
        with pytest.raises(ValidationError, match="YouTube URL"):
            VideoInsert(
                user_id=uuid.uuid4(),
                name="Yoga",
                url="not-a-url",
            )


class TestVideoInsertValidYouTubeUrls:
    """Tests that various YouTube URL formats are accepted."""

    @pytest.mark.parametrize(
        "url",
        [
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtube.com/watch?v=dQw4w9WgXcQ",
            "https://youtu.be/dQw4w9WgXcQ",
            "https://www.youtube.com/shorts/dQw4w9WgXcQ",
            "https://m.youtube.com/watch?v=dQw4w9WgXcQ",
            "http://www.youtube.com/watch?v=dQw4w9WgXcQ",
        ],
    )
    def test_valid_youtube_url_accepted(self, url):
        """Valid YouTube URLs should be accepted."""
        data = VideoInsert(
            user_id=uuid.uuid4(), name="Test", url=url
        )
        assert data.url == url


class TestVideoUpdate:
    """Tests for VideoUpdate schema."""

    def test_video_update_partial(self):
        """VideoUpdate with partial fields only includes set fields."""
        data = VideoUpdate(name="New Name")
        dumped = data.model_dump(exclude_unset=True)
        assert dumped == {"name": "New Name"}

    def test_video_update_url_none_allowed(self):
        """VideoUpdate with url=None is allowed (field not set)."""
        data = VideoUpdate()
        assert data.url is None

    def test_video_update_valid_youtube_url(self):
        """VideoUpdate with valid YouTube URL is accepted."""
        data = VideoUpdate(url=VALID_YOUTUBE_URL)
        assert data.url == VALID_YOUTUBE_URL

    def test_video_update_invalid_url_raises(self):
        """VideoUpdate with non-YouTube URL raises ValidationError."""
        with pytest.raises(ValidationError, match="YouTube URL"):
            VideoUpdate(url="https://example.com")


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
