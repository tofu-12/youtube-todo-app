"""Integration tests for TodoHistory CRUD operations."""

import datetime
import uuid

from app.core.types import TodoStatus
from app.crud.schemas.todo_history import TodoHistoryFilter, TodoHistoryInsert
from app.crud.todo_history import (
    create_todo_history,
    delete_todo_history,
    get_todo_histories,
)


class TestCreateTodoHistory:
    """Tests for create_todo_history."""

    def test_create_todo_history_completed(self, db, sample_user, sample_video):
        """Creating a COMPLETED todo history entry."""
        data = TodoHistoryInsert(
            user_id=sample_user.id,
            video_id=sample_video.id,
            scheduled_date=datetime.date(2026, 3, 18),
            status=TodoStatus.COMPLETED,
        )
        result = create_todo_history(db, data)

        assert result.status == TodoStatus.COMPLETED
        assert result.scheduled_date == datetime.date(2026, 3, 18)
        assert result.user_id == sample_user.id
        assert result.video_id == sample_video.id

    def test_create_todo_history_skipped(self, db, sample_user, sample_video):
        """Creating a SKIPPED todo history entry."""
        data = TodoHistoryInsert(
            user_id=sample_user.id,
            video_id=sample_video.id,
            scheduled_date=datetime.date(2026, 3, 18),
            status=TodoStatus.SKIPPED,
        )
        result = create_todo_history(db, data)
        assert result.status == TodoStatus.SKIPPED


class TestGetTodoHistories:
    """Tests for get_todo_histories."""

    def test_get_todo_histories_all(self, db, sample_user, sample_video):
        """Getting all todo histories for a user."""
        for day_offset in range(3):
            data = TodoHistoryInsert(
                user_id=sample_user.id,
                video_id=sample_video.id,
                scheduled_date=datetime.date(2026, 3, 18)
                + datetime.timedelta(days=day_offset),
                status=TodoStatus.COMPLETED,
            )
            create_todo_history(db, data)

        result = get_todo_histories(
            db, TodoHistoryFilter(user_id=sample_user.id)
        )
        assert len(result) == 3

    def test_get_todo_histories_by_date(self, db, sample_user, sample_video):
        """Getting todo histories filtered by scheduled_date."""
        target_date = datetime.date(2026, 3, 18)
        other_date = datetime.date(2026, 3, 19)

        for d in [target_date, other_date]:
            data = TodoHistoryInsert(
                user_id=sample_user.id,
                video_id=sample_video.id,
                scheduled_date=d,
                status=TodoStatus.COMPLETED,
            )
            create_todo_history(db, data)

        result = get_todo_histories(
            db,
            TodoHistoryFilter(
                user_id=sample_user.id, scheduled_date=target_date
            ),
        )
        assert len(result) == 1
        assert result[0].scheduled_date == target_date

    def test_get_todo_histories_empty(self, db, user_factory):
        """Getting todo histories for a user with none returns empty list."""
        user = user_factory()
        result = get_todo_histories(
            db, TodoHistoryFilter(user_id=user.id)
        )
        assert result == []


class TestDeleteTodoHistory:
    """Tests for delete_todo_history."""

    def test_delete_todo_history(self, db, sample_user, sample_video):
        """Deleting an existing todo history entry returns True."""
        data = TodoHistoryInsert(
            user_id=sample_user.id,
            video_id=sample_video.id,
            scheduled_date=datetime.date(2026, 3, 18),
            status=TodoStatus.COMPLETED,
        )
        entry = create_todo_history(db, data)
        assert delete_todo_history(db, entry.id, sample_user.id) is True

    def test_delete_todo_history_not_found(self, db, sample_user):
        """Deleting a nonexistent todo history entry returns False."""
        assert delete_todo_history(db, uuid.uuid4(), sample_user.id) is False
