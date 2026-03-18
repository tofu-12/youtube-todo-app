"""Tests for cross-user authorization bypass prevention.

Verifies that User A cannot access, modify, or delete User B's resources.
Covers issues #29, #30, and #32.
"""

import datetime

from app.core.types import RecurrenceType, TodoStatus
from app.crud import recurrence as crud_recurrence
from app.crud import todo_history as crud_todo_history
from app.crud import workout_history as crud_workout_history
from app.crud.schemas.recurrence import RecurrenceUpsert
from app.crud.schemas.todo_history import TodoHistoryInsert
from app.crud.schemas.workout_history import WorkoutHistoryInsert


class TestVideoCrossUserAccess:
    """Verify that a user cannot access another user's videos."""

    def test_list_videos_excludes_other_user(
        self, other_client, sample_video
    ):
        """GET /api/videos returns empty list for non-owner."""
        response = other_client.get("/api/videos")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_video_returns_404(self, other_client, sample_video):
        """GET /api/videos/{id} returns 404 for non-owner."""
        response = other_client.get(f"/api/videos/{sample_video.id}")
        assert response.status_code == 404

    def test_update_video_returns_404(self, other_client, sample_video):
        """PUT /api/videos/{id} returns 404 for non-owner."""
        response = other_client.put(
            f"/api/videos/{sample_video.id}",
            json={"name": "Hijacked"},
        )
        assert response.status_code == 404

    def test_delete_video_returns_404(self, other_client, sample_video):
        """DELETE /api/videos/{id} returns 404 for non-owner."""
        response = other_client.delete(f"/api/videos/{sample_video.id}")
        assert response.status_code == 404


class TestRecurrenceCrossUserAccess:
    """Verify that a user cannot access another user's recurrences."""

    def test_get_recurrence_returns_404(
        self, other_client, sample_user, sample_video, db
    ):
        """GET /api/videos/{id}/recurrence returns 404 for non-owner."""
        crud_recurrence.upsert_recurrence(
            db,
            RecurrenceUpsert(
                user_id=sample_user.id,
                video_id=sample_video.id,
                recurrence_type=RecurrenceType.DAILY,
            ),
        )
        response = other_client.get(
            f"/api/videos/{sample_video.id}/recurrence"
        )
        assert response.status_code == 404

    def test_upsert_recurrence_returns_404(
        self, other_client, sample_video
    ):
        """PUT /api/videos/{id}/recurrence returns 404 for non-owner."""
        response = other_client.put(
            f"/api/videos/{sample_video.id}/recurrence",
            json={"recurrence_type": "daily"},
        )
        assert response.status_code == 404

    def test_delete_recurrence_returns_404(
        self, other_client, sample_user, sample_video, db
    ):
        """DELETE /api/videos/{id}/recurrence returns 404 for non-owner."""
        crud_recurrence.upsert_recurrence(
            db,
            RecurrenceUpsert(
                user_id=sample_user.id,
                video_id=sample_video.id,
                recurrence_type=RecurrenceType.DAILY,
            ),
        )
        response = other_client.delete(
            f"/api/videos/{sample_video.id}/recurrence"
        )
        assert response.status_code == 404


class TestTodoHistoryCrossUserAccess:
    """Verify that a user cannot access another user's todo histories."""

    def test_list_excludes_other_user(
        self, other_client, sample_user, sample_video, db
    ):
        """GET /api/todo-histories returns empty list for non-owner."""
        crud_todo_history.create_todo_history(
            db,
            TodoHistoryInsert(
                user_id=sample_user.id,
                video_id=sample_video.id,
                scheduled_date=datetime.date(2026, 1, 1),
                status=TodoStatus.COMPLETED,
            ),
        )
        response = other_client.get("/api/todo-histories")
        assert response.status_code == 200
        assert response.json() == []

    def test_delete_returns_404(
        self, other_client, sample_user, sample_video, db
    ):
        """DELETE /api/todo-histories/{id} returns 404 for non-owner."""
        entry = crud_todo_history.create_todo_history(
            db,
            TodoHistoryInsert(
                user_id=sample_user.id,
                video_id=sample_video.id,
                scheduled_date=datetime.date(2026, 1, 2),
                status=TodoStatus.COMPLETED,
            ),
        )
        response = other_client.delete(f"/api/todo-histories/{entry.id}")
        assert response.status_code == 404


class TestWorkoutHistoryCrossUserAccess:
    """Verify that a user cannot access another user's workout histories."""

    def test_list_excludes_other_user(
        self, other_client, sample_user, sample_video, db
    ):
        """GET /api/workout-histories returns empty list for non-owner."""
        crud_workout_history.create_workout_history(
            db,
            WorkoutHistoryInsert(
                user_id=sample_user.id,
                video_id=sample_video.id,
                performed_date=datetime.date(2026, 1, 1),
                performed_at=datetime.datetime(
                    2026, 1, 1, tzinfo=datetime.timezone.utc
                ),
                expires_date=datetime.date(2026, 1, 8),
            ),
        )
        response = other_client.get("/api/workout-histories")
        assert response.status_code == 200
        assert response.json() == []

    def test_delete_returns_404(
        self, other_client, sample_user, sample_video, db
    ):
        """DELETE /api/workout-histories/{id} returns 404 for non-owner."""
        entry = crud_workout_history.create_workout_history(
            db,
            WorkoutHistoryInsert(
                user_id=sample_user.id,
                video_id=sample_video.id,
                performed_date=datetime.date(2026, 1, 2),
                performed_at=datetime.datetime(
                    2026, 1, 2, tzinfo=datetime.timezone.utc
                ),
                expires_date=datetime.date(2026, 1, 9),
            ),
        )
        response = other_client.delete(
            f"/api/workout-histories/{entry.id}"
        )
        assert response.status_code == 404
