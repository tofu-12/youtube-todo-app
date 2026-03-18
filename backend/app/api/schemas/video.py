"""API schemas for video endpoints."""

import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict


class VideoCreateRequest(BaseModel):
    """Request body for creating a video."""

    name: str
    url: str
    comment: Optional[str] = None
    tag_names: list[str] = []


class VideoUpdateRequest(BaseModel):
    """Request body for updating a video."""

    name: Optional[str] = None
    url: Optional[str] = None
    comment: Optional[str] = None
    tag_names: Optional[list[str]] = None


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
