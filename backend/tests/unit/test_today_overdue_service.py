"""Unit tests for get_today_videos and get_overdue_videos filtering logic."""

import datetime
import uuid
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from app.crud.schemas.user import UserResponse
from app.services.video_service import get_today_videos, get_overdue_videos


FIXED_TODAY = datetime.date(2026, 3, 20)
FIXED_NOW = datetime.datetime(2026, 3, 20, 12, 0, 0)


def _make_user_response():
    """Create a minimal UserResponse for testing."""
    return UserResponse(
        id=uuid.uuid4(),
        email="test@example.com",
        day_change_time=datetime.time(0, 0),
        timezone="Asia/Tokyo",
        workout_history_expires_days=90,
        created_at=FIXED_NOW,
        updated_at=FIXED_NOW,
    )


def _make_video(user_id, next_scheduled_date=None):
    """Create a mock video object that mimics an ORM Video with video_tags."""
    video = SimpleNamespace(
        id=uuid.uuid4(),
        user_id=user_id,
        name="Test Video",
        url="https://www.youtube.com/watch?v=test",
        comment=None,
        last_performed_date=None,
        next_scheduled_date=next_scheduled_date,
        video_tags=[],
        created_at=FIXED_NOW,
        updated_at=FIXED_NOW,
    )
    return video


class TestGetTodayVideos:
    """Tests for get_today_videos filtering logic."""

    @patch("app.services.video_service.get_logical_today", return_value=FIXED_TODAY)
    @patch("app.services.video_service.crud_video.get_videos_with_tags")
    def test_returns_video_scheduled_today(self, mock_get_videos, _mock_today):
        """Videos with next_scheduled_date == today should be returned."""
        user = _make_user_response()
        video = _make_video(user.id, next_scheduled_date=FIXED_TODAY)
        mock_get_videos.return_value = ([video], 1)

        result = get_today_videos(MagicMock(), user)

        assert len(result) == 1
        assert result[0].next_scheduled_date == FIXED_TODAY

    @patch("app.services.video_service.get_logical_today", return_value=FIXED_TODAY)
    @patch("app.services.video_service.crud_video.get_videos_with_tags")
    def test_excludes_past_videos(self, mock_get_videos, _mock_today):
        """Videos with next_scheduled_date < today should NOT be returned."""
        user = _make_user_response()
        yesterday = FIXED_TODAY - datetime.timedelta(days=1)
        video = _make_video(user.id, next_scheduled_date=yesterday)
        mock_get_videos.return_value = ([video], 1)

        result = get_today_videos(MagicMock(), user)

        assert len(result) == 0

    @patch("app.services.video_service.get_logical_today", return_value=FIXED_TODAY)
    @patch("app.services.video_service.crud_video.get_videos_with_tags")
    def test_excludes_future_videos(self, mock_get_videos, _mock_today):
        """Videos with next_scheduled_date > today should NOT be returned."""
        user = _make_user_response()
        tomorrow = FIXED_TODAY + datetime.timedelta(days=1)
        video = _make_video(user.id, next_scheduled_date=tomorrow)
        mock_get_videos.return_value = ([video], 1)

        result = get_today_videos(MagicMock(), user)

        assert len(result) == 0

    @patch("app.services.video_service.get_logical_today", return_value=FIXED_TODAY)
    @patch("app.services.video_service.crud_video.get_videos_with_tags")
    def test_excludes_videos_without_schedule(self, mock_get_videos, _mock_today):
        """Videos with next_scheduled_date == None should NOT be returned."""
        user = _make_user_response()
        video = _make_video(user.id, next_scheduled_date=None)
        mock_get_videos.return_value = ([video], 1)

        result = get_today_videos(MagicMock(), user)

        assert len(result) == 0


class TestGetOverdueVideos:
    """Tests for get_overdue_videos filtering logic."""

    @patch("app.services.video_service.get_logical_today", return_value=FIXED_TODAY)
    @patch("app.services.video_service.crud_video.get_videos_with_tags")
    def test_returns_past_videos(self, mock_get_videos, _mock_today):
        """Videos with next_scheduled_date < today should be returned."""
        user = _make_user_response()
        yesterday = FIXED_TODAY - datetime.timedelta(days=1)
        video = _make_video(user.id, next_scheduled_date=yesterday)
        mock_get_videos.return_value = ([video], 1)

        result = get_overdue_videos(MagicMock(), user)

        assert len(result) == 1
        assert result[0].next_scheduled_date == yesterday

    @patch("app.services.video_service.get_logical_today", return_value=FIXED_TODAY)
    @patch("app.services.video_service.crud_video.get_videos_with_tags")
    def test_excludes_today_videos(self, mock_get_videos, _mock_today):
        """Videos with next_scheduled_date == today should NOT be overdue."""
        user = _make_user_response()
        video = _make_video(user.id, next_scheduled_date=FIXED_TODAY)
        mock_get_videos.return_value = ([video], 1)

        result = get_overdue_videos(MagicMock(), user)

        assert len(result) == 0


class TestTodayOverdueNoOverlap:
    """Ensure today and overdue results do not overlap."""

    @patch("app.services.video_service.get_logical_today", return_value=FIXED_TODAY)
    @patch("app.services.video_service.crud_video.get_videos_with_tags")
    def test_no_overlap_between_today_and_overdue(self, mock_get_videos, _mock_today):
        """A video should appear in either today or overdue, never both."""
        user = _make_user_response()
        yesterday = FIXED_TODAY - datetime.timedelta(days=1)
        video_past = _make_video(user.id, next_scheduled_date=yesterday)
        video_today = _make_video(user.id, next_scheduled_date=FIXED_TODAY)
        mock_get_videos.return_value = ([video_past, video_today], 2)

        db = MagicMock()
        today_ids = {v.id for v in get_today_videos(db, user)}
        overdue_ids = {v.id for v in get_overdue_videos(db, user)}

        assert len(today_ids & overdue_ids) == 0
        assert len(today_ids) == 1
        assert len(overdue_ids) == 1
