"""API schemas for video endpoints."""

import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from app.core.validators import validate_youtube_url


class VideoCreateRequest(BaseModel):
    """Request body for creating a video."""

    name: str
    url: str
    comment: Optional[str] = None
    tag_names: list[str] = []

    @field_validator("url")
    @classmethod
    def check_youtube_url(cls, v: str) -> str:
        """Validate that url is a YouTube URL."""
        return validate_youtube_url(v)


class VideoUpdateRequest(BaseModel):
    """Request body for updating a video."""

    name: Optional[str] = None
    url: Optional[str] = None
    comment: Optional[str] = None
    tag_names: Optional[list[str]] = None

    @field_validator("url")
    @classmethod
    def check_youtube_url(cls, v: Optional[str]) -> Optional[str]:
        """Validate that url is a YouTube URL when provided."""
        if v is not None:
            return validate_youtube_url(v)
        return v


class TagOut(BaseModel):
    """Tag output schema for API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str


class VideoOut(BaseModel):
    """Video output schema for API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    url: str
    comment: Optional[str]
    last_performed_date: Optional[datetime.date]
    next_scheduled_date: Optional[datetime.date]
    tags: list[TagOut]
    created_at: datetime.datetime
    updated_at: datetime.datetime
