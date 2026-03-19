"""Integration tests for Video CRUD operations."""

import datetime
import uuid

from app.crud.schemas.video import VideoFilter, VideoInsert, VideoUpdate
from app.crud.video import (
    create_video,
    delete_video,
    get_video,
    get_videos,
    update_video,
)


class TestCreateVideo:
    """Tests for create_video."""

    def test_create_video_minimal(self, db, sample_user):
        """Creating a video with required fields only."""
        data = VideoInsert(
            user_id=sample_user.id,
            name="Morning Yoga",
            url="https://www.youtube.com/watch?v=abc",
        )
        result = create_video(db, data)

        assert result.name == "Morning Yoga"
        assert result.url == "https://www.youtube.com/watch?v=abc"
        assert result.comment is None
        assert result.last_performed_date is None
        assert result.next_scheduled_date is None
        assert result.user_id == sample_user.id

    def test_create_video_with_next_scheduled_date(self, db, sample_user):
        """Creating a video with next_scheduled_date stores it."""
        data = VideoInsert(
            user_id=sample_user.id,
            name="Scheduled Workout",
            url="https://www.youtube.com/watch?v=sched",
            next_scheduled_date=datetime.date(2026, 4, 1),
        )
        result = create_video(db, data)
        assert result.next_scheduled_date == datetime.date(2026, 4, 1)

    def test_create_video_with_comment(self, db, sample_user):
        """Creating a video with a comment stores it."""
        data = VideoInsert(
            user_id=sample_user.id,
            name="HIIT",
            url="https://www.youtube.com/watch?v=xyz",
            comment="30 min session",
        )
        result = create_video(db, data)
        assert result.comment == "30 min session"


class TestGetVideo:
    """Tests for get_video."""

    def test_get_video_found(self, db, sample_user, sample_video):
        """Getting an existing video returns correct data."""
        result = get_video(db, sample_video.id, sample_user.id)

        assert result is not None
        assert result.id == sample_video.id
        assert result.name == sample_video.name

    def test_get_video_not_found(self, db, sample_user):
        """Getting a nonexistent video returns None."""
        result = get_video(db, uuid.uuid4(), sample_user.id)
        assert result is None


class TestGetVideos:
    """Tests for get_videos."""

    def test_get_videos_by_user(self, db, sample_user, video_factory):
        """Getting videos for a user returns all their videos."""
        video_factory(sample_user.id)
        video_factory(sample_user.id)

        result = get_videos(db, VideoFilter(user_id=sample_user.id))
        assert len(result) == 2

    def test_get_videos_empty(self, db, user_factory):
        """Getting videos for a user with none returns empty list."""
        user = user_factory()
        result = get_videos(db, VideoFilter(user_id=user.id))
        assert result == []

    def test_get_videos_user_isolation(
        self, db, sample_user, video_factory, user_factory
    ):
        """Videos from other users are not included."""
        video_factory(sample_user.id)
        other_user = user_factory()
        video_factory(other_user.id)

        result = get_videos(db, VideoFilter(user_id=sample_user.id))
        assert len(result) == 1
        assert result[0].user_id == sample_user.id


class TestUpdateVideo:
    """Tests for update_video."""

    def test_update_video_name(self, db, sample_user, sample_video):
        """Updating a video name changes only that field."""
        data = VideoUpdate(name="New Name")
        result = update_video(db, sample_video.id, data, sample_user.id)

        assert result is not None
        assert result.name == "New Name"
        assert result.url == sample_video.url

    def test_update_video_schedule_dates(self, db, sample_user, sample_video):
        """Updating schedule dates stores them correctly."""
        today = datetime.date.today()
        data = VideoUpdate(
            last_performed_date=today,
            next_scheduled_date=today + datetime.timedelta(days=3),
        )
        result = update_video(db, sample_video.id, data, sample_user.id)

        assert result is not None
        assert result.last_performed_date == today
        assert result.next_scheduled_date == today + datetime.timedelta(days=3)

    def test_update_video_not_found(self, db, sample_user):
        """Updating a nonexistent video returns None."""
        data = VideoUpdate(name="X")
        result = update_video(db, uuid.uuid4(), data, sample_user.id)
        assert result is None


class TestDeleteVideo:
    """Tests for delete_video."""

    def test_delete_video(self, db, sample_user, sample_video):
        """Deleting an existing video returns True and removes it."""
        assert delete_video(db, sample_video.id, sample_user.id) is True
        assert get_video(db, sample_video.id, sample_user.id) is None

    def test_delete_video_not_found(self, db, sample_user):
        """Deleting a nonexistent video returns False."""
        assert delete_video(db, uuid.uuid4(), sample_user.id) is False
