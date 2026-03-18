"""Tests to verify unique constraints on history models."""

from sqlalchemy import UniqueConstraint

from app.models.todo_history import TodoHistory
from app.models.workout_history import WorkoutHistory


class TestTodoHistoryConstraints:
    """Verify TodoHistory model has the expected unique constraint."""

    def test_has_table_args(self) -> None:
        """TodoHistory must define __table_args__."""
        assert hasattr(TodoHistory, "__table_args__")

    def test_unique_constraint_exists(self) -> None:
        """TodoHistory must have a unique constraint on (video_id, scheduled_date)."""
        constraints = [
            c
            for c in TodoHistory.__table__.constraints
            if isinstance(c, UniqueConstraint)
        ]
        matching = [
            c
            for c in constraints
            if c.name == "uq_todo_history_video_date"
        ]
        assert len(matching) == 1
        column_names = {col.name for col in matching[0].columns}
        assert column_names == {"video_id", "scheduled_date"}


class TestWorkoutHistoryConstraints:
    """Verify WorkoutHistory model has the expected unique constraint."""

    def test_has_table_args(self) -> None:
        """WorkoutHistory must define __table_args__."""
        assert hasattr(WorkoutHistory, "__table_args__")

    def test_unique_constraint_exists(self) -> None:
        """WorkoutHistory must have a unique constraint on (video_id, performed_date)."""
        constraints = [
            c
            for c in WorkoutHistory.__table__.constraints
            if isinstance(c, UniqueConstraint)
        ]
        matching = [
            c
            for c in constraints
            if c.name == "uq_workout_history_video_date"
        ]
        assert len(matching) == 1
        column_names = {col.name for col in matching[0].columns}
        assert column_names == {"video_id", "performed_date"}
