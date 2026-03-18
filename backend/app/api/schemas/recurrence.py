"""API schemas for recurrence endpoints."""

import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.core.types import DayOfWeek, RecurrenceType


class RecurrenceRequest(BaseModel):
    """Request body for creating or updating a recurrence rule."""

    recurrence_type: RecurrenceType
    interval_days: Optional[int] = None
    weekdays: list[DayOfWeek] = []


class RecurrenceOut(BaseModel):
    """Recurrence output schema for API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    recurrence_type: RecurrenceType
    interval_days: Optional[int]
    weekdays: list[DayOfWeek]
    created_at: datetime.datetime
    updated_at: datetime.datetime
