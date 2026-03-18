"""Pydantic schemas for Video CRUD operations."""

import datetime
import uuid

from pydantic import BaseModel, ConfigDict


class VideoInsert(BaseModel):
    """Schema for creating a new video."""

    user_id: uuid.UUID
    name: str
    url: str
    comment: str | None = None


class VideoUpdate(BaseModel):
    """Schema for updating a video."""

    name: str | None = None
    url: str | None = None
    comment: str | None = None
    last_performed_date: datetime.date | None = None
    next_scheduled_date: datetime.date | None = None


class VideoFilter(BaseModel):
    """Schema for filtering videos."""

    user_id: uuid.UUID


class VideoResponse(BaseModel):
    """Schema for returning video data."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    url: str
    comment: str | None
    last_performed_date: datetime.date | None
    next_scheduled_date: datetime.date | None
    created_at: datetime.datetime
    updated_at: datetime.datetime
