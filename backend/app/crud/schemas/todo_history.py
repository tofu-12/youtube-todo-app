"""Pydantic schemas for TodoHistory CRUD operations."""

import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.core.types import TodoStatus


class TodoHistoryInsert(BaseModel):
    """Schema for creating a new todo history entry."""

    user_id: uuid.UUID
    video_id: uuid.UUID
    scheduled_date: datetime.date
    status: TodoStatus


class TodoHistoryFilter(BaseModel):
    """Schema for filtering todo history entries."""

    user_id: uuid.UUID
    scheduled_date: Optional[datetime.date] = None


class TodoHistoryResponse(BaseModel):
    """Schema for returning todo history data."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    video_id: uuid.UUID
    scheduled_date: datetime.date
    status: TodoStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime


class TodoHistoryStatsFilter(BaseModel):
    """Schema for filtering todo history stats aggregation."""

    user_id: uuid.UUID
    date_from: Optional[datetime.date] = None
    tag_id: Optional[uuid.UUID] = None


class TodoHistoryStatsResponse(BaseModel):
    """Schema for returning aggregated todo history stats."""

    completed_count: int
    skipped_count: int
    total_count: int
    completion_rate: float
