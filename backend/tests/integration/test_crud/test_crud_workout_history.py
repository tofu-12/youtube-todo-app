"""Integration tests for WorkoutHistory CRUD operations."""

import datetime
import uuid

from app.crud.schemas.workout_history import (
    WorkoutHistoryFilter,
    WorkoutHistoryInsert,
)
from app.crud.workout_history import (
    create_workout_history,
    delete_workout_history,
    get_workout_histories,
)


class TestCreateWorkoutHistory:
    """Tests for create_workout_history."""

    def test_create_workout_history(self, db, sample_user, sample_video):
        """Creating a workout history entry stores all fields."""
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        data = WorkoutHistoryInsert(
            user_id=sample_user.id,
            video_id=sample_video.id,
            performed_date=datetime.date(2026, 3, 18),
            performed_at=now,
            expires_date=datetime.date(2026, 3, 25),
        )
        result = create_workout_history(db, data)

        assert result.performed_date == datetime.date(2026, 3, 18)
        assert result.expires_date == datetime.date(2026, 3, 25)
        assert result.user_id == sample_user.id
        assert result.video_id == sample_video.id


class TestGetWorkoutHistories:
    """Tests for get_workout_histories."""

    def test_get_workout_histories_all(self, db, sample_user, sample_video):
        """Getting all workout histories for a user."""
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        for day_offset in range(3):
            data = WorkoutHistoryInsert(
                user_id=sample_user.id,
                video_id=sample_video.id,
                performed_date=datetime.date(2026, 3, 18)
                + datetime.timedelta(days=day_offset),
                performed_at=now,
                expires_date=datetime.date(2026, 3, 25)
                + datetime.timedelta(days=day_offset),
            )
            create_workout_history(db, data)

        result = get_workout_histories(
            db, WorkoutHistoryFilter(user_id=sample_user.id)
        )
        assert len(result) == 3

    def test_get_workout_histories_with_expires_after(
        self, db, sample_user, sample_video
    ):
        """Getting workout histories filtered by expires_after."""
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        # Entry expiring on Mar 20 (should be excluded when filter >= Mar 22)
        create_workout_history(
            db,
            WorkoutHistoryInsert(
                user_id=sample_user.id,
                video_id=sample_video.id,
                performed_date=datetime.date(2026, 3, 18),
                performed_at=now,
                expires_date=datetime.date(2026, 3, 20),
            ),
        )
        # Entry expiring on Mar 25 (should be included when filter >= Mar 22)
        create_workout_history(
            db,
            WorkoutHistoryInsert(
                user_id=sample_user.id,
                video_id=sample_video.id,
                performed_date=datetime.date(2026, 3, 19),
                performed_at=now,
                expires_date=datetime.date(2026, 3, 25),
            ),
        )

        result = get_workout_histories(
            db,
            WorkoutHistoryFilter(
                user_id=sample_user.id,
                expires_after=datetime.date(2026, 3, 22),
            ),
        )
        assert len(result) == 1
        assert result[0].expires_date == datetime.date(2026, 3, 25)

    def test_get_workout_histories_empty(self, db, user_factory):
        """Getting workout histories for a user with none returns empty."""
        user = user_factory()
        result = get_workout_histories(
            db, WorkoutHistoryFilter(user_id=user.id)
        )
        assert result == []


class TestDeleteWorkoutHistory:
    """Tests for delete_workout_history."""

    def test_delete_workout_history(self, db, sample_user, sample_video):
        """Deleting an existing workout history entry returns True."""
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        data = WorkoutHistoryInsert(
            user_id=sample_user.id,
            video_id=sample_video.id,
            performed_date=datetime.date(2026, 3, 18),
            performed_at=now,
            expires_date=datetime.date(2026, 3, 25),
        )
        entry = create_workout_history(db, data)
        assert delete_workout_history(db, entry.id) is True

    def test_delete_workout_history_not_found(self, db):
        """Deleting a nonexistent workout history entry returns False."""
        assert delete_workout_history(db, uuid.uuid4()) is False
