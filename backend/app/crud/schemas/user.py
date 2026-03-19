"""Pydantic schemas for User CRUD operations."""

import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserInsert(BaseModel):
    """Schema for creating a new user."""

    email: str
    day_change_time: datetime.time = datetime.time(0, 0)
    timezone: str = "Asia/Tokyo"
    workout_history_expires_days: int = 90


class UserUpdate(BaseModel):
    """Schema for updating user settings."""

    day_change_time: Optional[datetime.time] = None
    timezone: Optional[str] = None
    workout_history_expires_days: Optional[int] = None


class UserResponse(BaseModel):
    """Schema for returning user data."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    day_change_time: datetime.time
    timezone: str
    workout_history_expires_days: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
