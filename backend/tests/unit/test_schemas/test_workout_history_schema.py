"""Unit tests for WorkoutHistory Pydantic schemas."""

import datetime
import uuid

import pytest
from pydantic import ValidationError

from app.api.schemas.workout_history import WorkoutHistoryCreateRequest
from app.crud.schemas.workout_history import (
    WorkoutHistoryFilter,
    WorkoutHistoryInsert,
    WorkoutHistoryResponse,
)


class TestWorkoutHistoryInsert:
    """Tests for WorkoutHistoryInsert schema."""

    def test_workout_history_insert_valid(self):
        """WorkoutHistoryInsert with all required fields."""
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        data = WorkoutHistoryInsert(
            user_id=uuid.uuid4(),
            video_id=uuid.uuid4(),
            performed_date=datetime.date(2026, 3, 18),
            performed_at=now,
            expires_date=datetime.date(2026, 3, 25),
        )
        assert data.performed_date == datetime.date(2026, 3, 18)
        assert data.expires_date == datetime.date(2026, 3, 25)

    def test_workout_history_insert_missing_field(self):
        """WorkoutHistoryInsert without required field raises error."""
        with pytest.raises(ValidationError):
            WorkoutHistoryInsert(
                user_id=uuid.uuid4(),
                video_id=uuid.uuid4(),
                performed_date=datetime.date(2026, 3, 18),
                # missing performed_at and expires_date
            )


class TestWorkoutHistoryCreateRequest:
    """Tests for WorkoutHistoryCreateRequest API schema."""

    def test_valid_expires_days(self):
        """WorkoutHistoryCreateRequest accepts positive expires_days."""
        data = WorkoutHistoryCreateRequest(
            video_id=uuid.uuid4(),
            expires_days=1,
        )
        assert data.expires_days == 1

    def test_zero_expires_days_rejected(self):
        """WorkoutHistoryCreateRequest rejects zero expires_days."""
        with pytest.raises(ValidationError):
            WorkoutHistoryCreateRequest(
                video_id=uuid.uuid4(),
                expires_days=0,
            )

    def test_negative_expires_days_rejected(self):
        """WorkoutHistoryCreateRequest rejects negative expires_days."""
        with pytest.raises(ValidationError):
            WorkoutHistoryCreateRequest(
                video_id=uuid.uuid4(),
                expires_days=-1,
            )


class TestWorkoutHistoryFilter:
    """Tests for WorkoutHistoryFilter schema."""

    def test_workout_history_filter_defaults(self):
        """WorkoutHistoryFilter defaults expires_after to None."""
        data = WorkoutHistoryFilter(user_id=uuid.uuid4())
        assert data.expires_after is None

    def test_workout_history_filter_with_date(self):
        """WorkoutHistoryFilter accepts an expires_after date."""
        target = datetime.date(2026, 3, 22)
        data = WorkoutHistoryFilter(
            user_id=uuid.uuid4(), expires_after=target
        )
        assert data.expires_after == target


class TestWorkoutHistoryResponse:
    """Tests for WorkoutHistoryResponse schema."""

    def test_workout_history_response_from_attributes(self):
        """WorkoutHistoryResponse can be constructed from a dict."""
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        obj = {
            "id": uuid.uuid4(),
            "user_id": uuid.uuid4(),
            "video_id": uuid.uuid4(),
            "performed_date": datetime.date(2026, 3, 18),
            "performed_at": now,
            "expires_date": datetime.date(2026, 3, 25),
            "created_at": now,
            "updated_at": now,
        }
        result = WorkoutHistoryResponse.model_validate(obj)
        assert result.performed_date == datetime.date(2026, 3, 18)
