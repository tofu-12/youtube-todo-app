"""Integration tests for cascade delete behavior."""

import datetime

from sqlalchemy import select

from app.core.types import DayOfWeek, RecurrenceType, TodoStatus
from app.crud.recurrence import upsert_recurrence
from app.crud.schemas.recurrence import RecurrenceUpsert
from app.crud.schemas.todo_history import TodoHistoryInsert
from app.crud.schemas.workout_history import WorkoutHistoryInsert
from app.crud.todo_history import create_todo_history
from app.crud.video_tag import set_video_tags
from app.crud.workout_history import create_workout_history
from app.models.tag import Tag
from app.models.todo_history import TodoHistory
from app.models.user import User
from app.models.video import Video
from app.models.video_recurrence import VideoRecurrence
from app.models.video_tag import VideoTag
from app.models.video_weekday import VideoWeekday
from app.models.workout_history import WorkoutHistory


class TestUserCascadeDelete:
    """Tests for cascade delete when a User is removed."""

    def _setup_full_user(self, db, user_factory, video_factory, tag_factory):
        """Create a user with videos, tags, recurrences, and histories."""
        user = user_factory()
        video = video_factory(user.id)
        tag = tag_factory(user.id)
        set_video_tags(db, user.id, video.id, [tag.id])

        upsert_recurrence(
            db,
            RecurrenceUpsert(
                user_id=user.id,
                video_id=video.id,
                recurrence_type=RecurrenceType.WEEKLY,
                weekdays=[DayOfWeek.MON],
            ),
        )

        now = datetime.datetime.now(tz=datetime.timezone.utc)
        create_todo_history(
            db,
            TodoHistoryInsert(
                user_id=user.id,
                video_id=video.id,
                scheduled_date=datetime.date(2026, 3, 18),
                status=TodoStatus.COMPLETED,
            ),
        )
        create_workout_history(
            db,
            WorkoutHistoryInsert(
                user_id=user.id,
                video_id=video.id,
                performed_date=datetime.date(2026, 3, 18),
                performed_at=now,
                expires_date=datetime.date(2026, 3, 25),
            ),
        )
        return user

    def test_delete_user_cascades_videos(
        self, db, user_factory, video_factory, tag_factory
    ):
        """Deleting a user removes all their videos."""
        user = self._setup_full_user(
            db, user_factory, video_factory, tag_factory
        )
        user_id = user.id

        db_user = db.get(User, user_id)
        db.delete(db_user)
        db.flush()

        videos = db.scalars(
            select(Video).where(Video.user_id == user_id)
        ).all()
        assert len(videos) == 0

    def test_delete_user_cascades_tags(
        self, db, user_factory, video_factory, tag_factory
    ):
        """Deleting a user removes all their tags."""
        user = self._setup_full_user(
            db, user_factory, video_factory, tag_factory
        )
        user_id = user.id

        db_user = db.get(User, user_id)
        db.delete(db_user)
        db.flush()

        tags = db.scalars(
            select(Tag).where(Tag.user_id == user_id)
        ).all()
        assert len(tags) == 0

    def test_delete_user_cascades_todo_histories(
        self, db, user_factory, video_factory, tag_factory
    ):
        """Deleting a user removes all their todo histories."""
        user = self._setup_full_user(
            db, user_factory, video_factory, tag_factory
        )
        user_id = user.id

        db_user = db.get(User, user_id)
        db.delete(db_user)
        db.flush()

        entries = db.scalars(
            select(TodoHistory).where(TodoHistory.user_id == user_id)
        ).all()
        assert len(entries) == 0

    def test_delete_user_cascades_workout_histories(
        self, db, user_factory, video_factory, tag_factory
    ):
        """Deleting a user removes all their workout histories."""
        user = self._setup_full_user(
            db, user_factory, video_factory, tag_factory
        )
        user_id = user.id

        db_user = db.get(User, user_id)
        db.delete(db_user)
        db.flush()

        entries = db.scalars(
            select(WorkoutHistory).where(
                WorkoutHistory.user_id == user_id
            )
        ).all()
        assert len(entries) == 0

    def test_delete_user_cascades_recurrences_and_weekdays(
        self, db, user_factory, video_factory, tag_factory
    ):
        """Deleting a user removes recurrences and their weekdays."""
        user = self._setup_full_user(
            db, user_factory, video_factory, tag_factory
        )
        user_id = user.id

        db_user = db.get(User, user_id)
        db.delete(db_user)
        db.flush()

        recs = db.scalars(
            select(VideoRecurrence).where(
                VideoRecurrence.user_id == user_id
            )
        ).all()
        assert len(recs) == 0

        weekdays = db.scalars(
            select(VideoWeekday).where(
                VideoWeekday.user_id == user_id
            )
        ).all()
        assert len(weekdays) == 0


class TestVideoCascadeDelete:
    """Tests for cascade delete when a Video is removed."""

    def test_delete_video_cascades_recurrence(
        self, db, sample_user, sample_video
    ):
        """Deleting a video removes its recurrence."""
        upsert_recurrence(
            db,
            RecurrenceUpsert(
                user_id=sample_user.id,
                video_id=sample_video.id,
                recurrence_type=RecurrenceType.DAILY,
            ),
        )

        video = db.get(Video, sample_video.id)
        db.delete(video)
        db.flush()

        recs = db.scalars(
            select(VideoRecurrence).where(
                VideoRecurrence.video_id == sample_video.id
            )
        ).all()
        assert len(recs) == 0

    def test_delete_video_cascades_video_tags(
        self, db, sample_user, sample_video, tag_factory
    ):
        """Deleting a video removes its video-tag associations."""
        tag = tag_factory(sample_user.id)
        set_video_tags(db, sample_user.id, sample_video.id, [tag.id])

        video = db.get(Video, sample_video.id)
        db.delete(video)
        db.flush()

        vts = db.scalars(
            select(VideoTag).where(
                VideoTag.video_id == sample_video.id
            )
        ).all()
        assert len(vts) == 0

    def test_delete_video_cascades_todo_histories(
        self, db, sample_user, sample_video
    ):
        """Deleting a video removes its todo histories."""
        create_todo_history(
            db,
            TodoHistoryInsert(
                user_id=sample_user.id,
                video_id=sample_video.id,
                scheduled_date=datetime.date(2026, 3, 18),
                status=TodoStatus.COMPLETED,
            ),
        )

        video = db.get(Video, sample_video.id)
        db.delete(video)
        db.flush()

        entries = db.scalars(
            select(TodoHistory).where(
                TodoHistory.video_id == sample_video.id
            )
        ).all()
        assert len(entries) == 0


class TestTagCascadeDelete:
    """Tests for cascade delete when a Tag is removed."""

    def test_delete_tag_cascades_video_tags(
        self, db, sample_user, sample_video, tag_factory
    ):
        """Deleting a tag removes its video-tag associations."""
        tag = tag_factory(sample_user.id)
        set_video_tags(db, sample_user.id, sample_video.id, [tag.id])

        db_tag = db.get(Tag, tag.id)
        db.delete(db_tag)
        db.flush()

        vts = db.scalars(
            select(VideoTag).where(VideoTag.tag_id == tag.id)
        ).all()
        assert len(vts) == 0
