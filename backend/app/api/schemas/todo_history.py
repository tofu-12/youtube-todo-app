"""API schemas for todo history endpoints."""

import datetime
import uuid

from pydantic import BaseModel, ConfigDict

from app.core.types import TodoStatus


class TodoHistoryCreateRequest(BaseModel):
    """Request body for creating a todo history entry."""

    video_id: uuid.UUID
    scheduled_date: datetime.date
    status: TodoStatus


class TodoHistoryOut(BaseModel):
    """Todo history output schema for API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    video_id: uuid.UUID
    scheduled_date: datetime.date
    status: TodoStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
