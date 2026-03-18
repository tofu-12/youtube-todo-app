"""Unit tests for SQLAlchemy model definitions."""

from app.core.database import Base
from app.models.base import TimestampMixin
from app.models.tag import Tag
from app.models.todo_history import TodoHistory
from app.models.user import User
from app.models.video import Video
from app.models.video_recurrence import VideoRecurrence
from app.models.video_tag import VideoTag
from app.models.video_weekday import VideoWeekday
from app.models.workout_history import WorkoutHistory

ALL_MODELS = [
    User,
    Video,
    Tag,
    VideoTag,
    VideoRecurrence,
    VideoWeekday,
    TodoHistory,
    WorkoutHistory,
]

EXPECTED_TABLENAMES = {
    User: "users",
    Video: "videos",
    Tag: "tags",
    VideoTag: "video_tags",
    VideoRecurrence: "video_recurrences",
    VideoWeekday: "video_weekdays",
    TodoHistory: "todo_histories",
    WorkoutHistory: "workout_histories",
}


class TestTableNames:
    """Tests for model __tablename__ attributes."""

    def test_user_tablename(self):
        assert User.__tablename__ == "users"

    def test_video_tablename(self):
        assert Video.__tablename__ == "videos"

    def test_tag_tablename(self):
        assert Tag.__tablename__ == "tags"

    def test_video_tag_tablename(self):
        assert VideoTag.__tablename__ == "video_tags"

    def test_video_recurrence_tablename(self):
        assert VideoRecurrence.__tablename__ == "video_recurrences"

    def test_video_weekday_tablename(self):
        assert VideoWeekday.__tablename__ == "video_weekdays"

    def test_todo_history_tablename(self):
        assert TodoHistory.__tablename__ == "todo_histories"

    def test_workout_history_tablename(self):
        assert WorkoutHistory.__tablename__ == "workout_histories"


class TestTimestampMixin:
    """Tests for TimestampMixin inheritance."""

    def test_user_has_timestamp_mixin(self):
        assert issubclass(User, TimestampMixin)

    def test_video_has_timestamp_mixin(self):
        assert issubclass(Video, TimestampMixin)


class TestBaseInheritance:
    """Tests for Base class inheritance."""

    def test_all_models_extend_base(self):
        """All models inherit from the SQLAlchemy Base class."""
        for model in ALL_MODELS:
            assert issubclass(model, Base), (
                f"{model.__name__} does not extend Base"
            )


class TestModelConstraints:
    """Tests for model constraint definitions."""

    def test_video_recurrence_check_constraint_defined(self):
        """VideoRecurrence has a CheckConstraint in __table_args__."""
        table_args = VideoRecurrence.__table_args__
        constraint_names = [
            c.name for c in table_args if hasattr(c, "name")
        ]
        assert "ck_interval_days_required" in constraint_names

    def test_tag_unique_constraint_defined(self):
        """Tag has a UniqueConstraint(user_id, name) in __table_args__."""
        table_args = Tag.__table_args__
        constraint_names = [
            c.name for c in table_args if hasattr(c, "name")
        ]
        assert "uq_tag_user_name" in constraint_names
