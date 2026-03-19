"""Pydantic schemas for Video CRUD operations."""

import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from app.core.validators import validate_youtube_url


class VideoInsert(BaseModel):
    """Schema for creating a new video."""

    user_id: uuid.UUID
    name: str
    url: str
    comment: Optional[str] = None
    next_scheduled_date: Optional[datetime.date] = None

    @field_validator("url")
    @classmethod
    def check_youtube_url(cls, v: str) -> str:
        """Validate that url is a YouTube URL."""
        return validate_youtube_url(v)


class VideoUpdate(BaseModel):
    """Schema for updating a video."""

    name: Optional[str] = None
    url: Optional[str] = None
    comment: Optional[str] = None
    last_performed_date: Optional[datetime.date] = None
    next_scheduled_date: Optional[datetime.date] = None

    @field_validator("url")
    @classmethod
    def check_youtube_url(cls, v: Optional[str]) -> Optional[str]:
        """Validate that url is a YouTube URL when provided."""
        if v is not None:
            return validate_youtube_url(v)
        return v


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
