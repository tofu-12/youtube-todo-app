"""Pydantic schemas for User CRUD operations."""

import datetime
import uuid

from pydantic import BaseModel, ConfigDict


class UserInsert(BaseModel):
    """Schema for creating a new user."""

    day_change_time: datetime.time = datetime.time(0, 0)
    timezone: str = "Asia/Tokyo"


class UserUpdate(BaseModel):
    """Schema for updating user settings."""

    day_change_time: datetime.time | None = None
    timezone: str | None = None


class UserResponse(BaseModel):
    """Schema for returning user data."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    day_change_time: datetime.time
    timezone: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
