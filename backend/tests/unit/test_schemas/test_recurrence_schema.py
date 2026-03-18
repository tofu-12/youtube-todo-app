"""Unit tests for Recurrence Pydantic schemas."""

import datetime
import uuid

import pytest
from pydantic import ValidationError

from app.core.types import DayOfWeek, RecurrenceType
from app.crud.schemas.recurrence import (
    RecurrenceResponse,
    RecurrenceUpsert,
    WeekdayResponse,
)


class TestRecurrenceUpsert:
    """Tests for RecurrenceUpsert schema."""

    def test_recurrence_upsert_daily(self):
        """DAILY recurrence with default empty weekdays."""
        data = RecurrenceUpsert(
            user_id=uuid.uuid4(),
            video_id=uuid.uuid4(),
            recurrence_type=RecurrenceType.DAILY,
        )
        assert data.recurrence_type == RecurrenceType.DAILY
        assert data.weekdays == []
        assert data.interval_days is None

    def test_recurrence_upsert_weekly_with_weekdays(self):
        """WEEKLY recurrence with weekdays list."""
        data = RecurrenceUpsert(
            user_id=uuid.uuid4(),
            video_id=uuid.uuid4(),
            recurrence_type=RecurrenceType.WEEKLY,
            weekdays=[DayOfWeek.MON, DayOfWeek.FRI],
        )
        assert len(data.weekdays) == 2

    def test_recurrence_upsert_interval_with_days(self):
        """INTERVAL recurrence with interval_days."""
        data = RecurrenceUpsert(
            user_id=uuid.uuid4(),
            video_id=uuid.uuid4(),
            recurrence_type=RecurrenceType.INTERVAL,
            interval_days=5,
        )
        assert data.interval_days == 5

    def test_recurrence_upsert_invalid_recurrence_type(self):
        """Invalid recurrence_type raises ValidationError."""
        with pytest.raises(ValidationError):
            RecurrenceUpsert(
                user_id=uuid.uuid4(),
                video_id=uuid.uuid4(),
                recurrence_type="invalid_type",
            )


class TestWeekdayResponse:
    """Tests for WeekdayResponse schema."""

    def test_weekday_response_from_attributes(self):
        """WeekdayResponse can be constructed from a dict."""
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        obj = {
            "id": uuid.uuid4(),
            "day_of_week": DayOfWeek.MON,
            "created_at": now,
            "updated_at": now,
        }
        result = WeekdayResponse.model_validate(obj)
        assert result.day_of_week == DayOfWeek.MON


class TestRecurrenceResponse:
    """Tests for RecurrenceResponse schema."""

    def test_recurrence_response_with_weekdays(self):
        """RecurrenceResponse includes nested weekdays."""
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        obj = {
            "id": uuid.uuid4(),
            "user_id": uuid.uuid4(),
            "video_id": uuid.uuid4(),
            "recurrence_type": RecurrenceType.WEEKLY,
            "interval_days": None,
            "weekdays": [
                {
                    "id": uuid.uuid4(),
                    "day_of_week": DayOfWeek.MON,
                    "created_at": now,
                    "updated_at": now,
                },
            ],
            "created_at": now,
            "updated_at": now,
        }
        result = RecurrenceResponse.model_validate(obj)
        assert len(result.weekdays) == 1
        assert result.recurrence_type == RecurrenceType.WEEKLY
