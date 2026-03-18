"""Pydantic schemas for VideoRecurrence CRUD operations."""

import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.core.types import DayOfWeek, RecurrenceType


class RecurrenceUpsert(BaseModel):
    """Schema for creating or updating a video recurrence."""

    user_id: uuid.UUID
    video_id: uuid.UUID
    recurrence_type: RecurrenceType
    interval_days: Optional[int] = None
    weekdays: list[DayOfWeek] = []


class WeekdayResponse(BaseModel):
    """Schema for returning weekday data."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    day_of_week: DayOfWeek
    created_at: datetime.datetime
    updated_at: datetime.datetime


class RecurrenceResponse(BaseModel):
    """Schema for returning recurrence data."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    video_id: uuid.UUID
    recurrence_type: RecurrenceType
    interval_days: Optional[int]
    weekdays: list[WeekdayResponse]
    created_at: datetime.datetime
    updated_at: datetime.datetime
