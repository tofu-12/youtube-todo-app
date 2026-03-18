"""Unit tests for TodoHistory Pydantic schemas."""

import datetime
import uuid

import pytest
from pydantic import ValidationError

from app.core.types import TodoStatus
from app.crud.schemas.todo_history import (
    TodoHistoryFilter,
    TodoHistoryInsert,
    TodoHistoryResponse,
)


class TestTodoHistoryInsert:
    """Tests for TodoHistoryInsert schema."""

    def test_todo_history_insert_completed(self):
        """TodoHistoryInsert with COMPLETED status."""
        data = TodoHistoryInsert(
            user_id=uuid.uuid4(),
            video_id=uuid.uuid4(),
            scheduled_date=datetime.date(2026, 3, 18),
            status=TodoStatus.COMPLETED,
        )
        assert data.status == TodoStatus.COMPLETED

    def test_todo_history_insert_skipped(self):
        """TodoHistoryInsert with SKIPPED status."""
        data = TodoHistoryInsert(
            user_id=uuid.uuid4(),
            video_id=uuid.uuid4(),
            scheduled_date=datetime.date(2026, 3, 18),
            status=TodoStatus.SKIPPED,
        )
        assert data.status == TodoStatus.SKIPPED

    def test_todo_history_insert_invalid_status(self):
        """TodoHistoryInsert with invalid status raises ValidationError."""
        with pytest.raises(ValidationError):
            TodoHistoryInsert(
                user_id=uuid.uuid4(),
                video_id=uuid.uuid4(),
                scheduled_date=datetime.date(2026, 3, 18),
                status="invalid",
            )


class TestTodoHistoryFilter:
    """Tests for TodoHistoryFilter schema."""

    def test_todo_history_filter_defaults(self):
        """TodoHistoryFilter defaults scheduled_date to None."""
        data = TodoHistoryFilter(user_id=uuid.uuid4())
        assert data.scheduled_date is None

    def test_todo_history_filter_with_date(self):
        """TodoHistoryFilter accepts a scheduled_date."""
        target = datetime.date(2026, 3, 18)
        data = TodoHistoryFilter(
            user_id=uuid.uuid4(), scheduled_date=target
        )
        assert data.scheduled_date == target


class TestTodoHistoryResponse:
    """Tests for TodoHistoryResponse schema."""

    def test_todo_history_response_from_attributes(self):
        """TodoHistoryResponse can be constructed from a dict."""
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        obj = {
            "id": uuid.uuid4(),
            "user_id": uuid.uuid4(),
            "video_id": uuid.uuid4(),
            "scheduled_date": datetime.date(2026, 3, 18),
            "status": TodoStatus.COMPLETED,
            "created_at": now,
            "updated_at": now,
        }
        result = TodoHistoryResponse.model_validate(obj)
        assert result.status == TodoStatus.COMPLETED
