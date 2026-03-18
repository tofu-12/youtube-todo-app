"""API schemas for workout history endpoints."""

import datetime
import uuid

from pydantic import BaseModel, ConfigDict


class WorkoutHistoryCreateRequest(BaseModel):
    """Request body for creating a workout history entry."""

    video_id: uuid.UUID
    expires_days: int


class WorkoutHistoryOut(BaseModel):
    """Workout history output schema for API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    video_id: uuid.UUID
    performed_date: datetime.date
    performed_at: datetime.datetime
    expires_date: datetime.date
    created_at: datetime.datetime
    updated_at: datetime.datetime
