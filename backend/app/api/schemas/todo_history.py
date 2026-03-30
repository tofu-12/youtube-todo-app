"""API schemas for todo history endpoints."""

import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, model_validator

from app.core.types import TodoStatus


class TodoHistoryCreateRequest(BaseModel):
    """Request body for creating a todo history entry."""

    video_id: uuid.UUID
    scheduled_date: datetime.date
    status: TodoStatus
    next_scheduled_date: Optional[datetime.date] = None



class TodoHistoryResponse(BaseModel):
    """Todo history output schema for API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    video_id: uuid.UUID
    scheduled_date: datetime.date
    status: TodoStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime


class TodoHistoryStatsResponse(BaseModel):
    """Stats output schema for API responses."""

    completed_count: int
    skipped_count: int
    total_count: int
    completion_rate: float
