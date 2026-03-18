"""Integration tests for database constraints."""

import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from app.core.types import DayOfWeek, RecurrenceType, TodoStatus
from app.models.tag import Tag
from app.models.todo_history import TodoHistory
from app.models.video import Video
from app.models.video_recurrence import VideoRecurrence
from app.models.video_tag import VideoTag
from app.models.video_weekday import VideoWeekday


class TestTagUniqueConstraint:
    """Tests for the (user_id, name) unique constraint on tags."""

    def test_tag_unique_user_name(self, db, sample_user):
        """Same user cannot have two tags with the same name."""
        tag1 = Tag(user_id=sample_user.id, name="yoga")
        db.add(tag1)
        db.flush()

        tag2 = Tag(user_id=sample_user.id, name="yoga")
        db.add(tag2)
        with pytest.raises(IntegrityError):
            db.flush()
        db.rollback()

    def test_tag_unique_different_users_same_name(
        self, db, user_factory
    ):
        """Different users can have tags with the same name."""
        user1 = user_factory()
        user2 = user_factory()

        tag1 = Tag(user_id=user1.id, name="yoga")
        tag2 = Tag(user_id=user2.id, name="yoga")
        db.add_all([tag1, tag2])
        db.flush()  # Should not raise


class TestVideoTagUniqueConstraint:
    """Tests for the (video_id, tag_id) unique constraint on video_tags."""

    def test_video_tag_unique(self, db, sample_user, sample_video, tag_factory):
        """Same video-tag pair cannot be duplicated."""
        tag = tag_factory(sample_user.id)

        vt1 = VideoTag(
            user_id=sample_user.id,
            video_id=sample_video.id,
            tag_id=tag.id,
        )
        db.add(vt1)
        db.flush()

        vt2 = VideoTag(
            user_id=sample_user.id,
            video_id=sample_video.id,
            tag_id=tag.id,
        )
        db.add(vt2)
        with pytest.raises(IntegrityError):
            db.flush()
        db.rollback()


class TestVideoRecurrenceUniqueConstraint:
    """Tests for the unique video_id constraint on video_recurrences."""

    def test_video_recurrence_unique_video_id(
        self, db, sample_user, sample_video
    ):
        """A video cannot have two recurrence records."""
        rec1 = VideoRecurrence(
            user_id=sample_user.id,
            video_id=sample_video.id,
            recurrence_type=RecurrenceType.DAILY,
        )
        db.add(rec1)
        db.flush()

        rec2 = VideoRecurrence(
            user_id=sample_user.id,
            video_id=sample_video.id,
            recurrence_type=RecurrenceType.WEEKLY,
        )
        db.add(rec2)
        with pytest.raises(IntegrityError):
            db.flush()
        db.rollback()


class TestVideoWeekdayUniqueConstraint:
    """Tests for the unique constraint on video_weekdays."""

    def test_video_weekday_unique_recurrence_day(
        self, db, sample_user, sample_video
    ):
        """Same recurrence cannot have two entries for the same day."""
        rec = VideoRecurrence(
            user_id=sample_user.id,
            video_id=sample_video.id,
            recurrence_type=RecurrenceType.WEEKLY,
        )
        db.add(rec)
        db.flush()

        wd1 = VideoWeekday(
            user_id=sample_user.id,
            video_recurrence_id=rec.id,
            day_of_week=DayOfWeek.MON,
        )
        db.add(wd1)
        db.flush()

        wd2 = VideoWeekday(
            user_id=sample_user.id,
            video_recurrence_id=rec.id,
            day_of_week=DayOfWeek.MON,
        )
        db.add(wd2)
        with pytest.raises(IntegrityError):
            db.flush()
        db.rollback()


class TestIntervalDaysCheckConstraint:
    """Tests for the ck_interval_days_required check constraint."""

    def test_interval_days_check_constraint_null(
        self, db, sample_user, sample_video
    ):
        """INTERVAL type with interval_days=None raises IntegrityError."""
        rec = VideoRecurrence(
            user_id=sample_user.id,
            video_id=sample_video.id,
            recurrence_type=RecurrenceType.INTERVAL,
            interval_days=None,
        )
        db.add(rec)
        with pytest.raises(IntegrityError):
            db.flush()
        db.rollback()

    def test_interval_days_check_constraint_zero(
        self, db, sample_user, video_factory
    ):
        """INTERVAL type with interval_days=0 raises IntegrityError."""
        video = video_factory(sample_user.id)
        rec = VideoRecurrence(
            user_id=sample_user.id,
            video_id=video.id,
            recurrence_type=RecurrenceType.INTERVAL,
            interval_days=0,
        )
        db.add(rec)
        with pytest.raises(IntegrityError):
            db.flush()
        db.rollback()

    def test_interval_days_non_interval_type_null_ok(
        self, db, sample_user, sample_video
    ):
        """DAILY type with interval_days=None is allowed."""
        rec = VideoRecurrence(
            user_id=sample_user.id,
            video_id=sample_video.id,
            recurrence_type=RecurrenceType.DAILY,
            interval_days=None,
        )
        db.add(rec)
        db.flush()  # Should not raise


class TestForeignKeyConstraints:
    """Tests for foreign key constraints."""

    def test_video_fk_invalid_user(self, db):
        """Creating a video with a nonexistent user_id raises error."""
        video = Video(
            user_id=uuid.uuid4(),
            name="Test",
            url="https://example.com",
        )
        db.add(video)
        with pytest.raises(IntegrityError):
            db.flush()
        db.rollback()

    def test_tag_fk_invalid_user(self, db):
        """Creating a tag with a nonexistent user_id raises error."""
        tag = Tag(user_id=uuid.uuid4(), name="test")
        db.add(tag)
        with pytest.raises(IntegrityError):
            db.flush()
        db.rollback()
