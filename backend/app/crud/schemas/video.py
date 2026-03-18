"""Pydantic schemas for Video CRUD operations."""

import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict


class VideoInsert(BaseModel):
    """Schema for creating a new video."""

    user_id: uuid.UUID
    name: str
    url: str
    comment: Optional[str] = None


class VideoUpdate(BaseModel):
    """Schema for updating a video."""

    name: Optional[str] = None
    url: Optional[str] = None
    comment: Optional[str] = None
    last_performed_date: Optional[datetime.date] = None
    next_scheduled_date: Optional[datetime.date] = None


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
    comment: Optional[str]
    last_performed_date: Optional[datetime.date]
    next_scheduled_date: Optional[datetime.date]
    created_at: datetime.datetime
    updated_at: datetime.datetime
