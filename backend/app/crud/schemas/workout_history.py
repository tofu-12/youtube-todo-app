"""Pydantic schemas for WorkoutHistory CRUD operations."""

import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict


class WorkoutHistoryInsert(BaseModel):
    """Schema for creating a new workout history entry."""

    user_id: uuid.UUID
    video_id: uuid.UUID
    performed_date: datetime.date
    performed_at: datetime.datetime
    expires_date: datetime.date


class WorkoutHistoryFilter(BaseModel):
    """Schema for filtering workout history entries."""

    user_id: uuid.UUID
    expires_after: Optional[datetime.date] = None


class WorkoutHistoryResponse(BaseModel):
    """Schema for returning workout history data."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    video_id: uuid.UUID
    performed_date: datetime.date
    performed_at: datetime.datetime
    expires_date: datetime.date
    created_at: datetime.datetime
    updated_at: datetime.datetime
