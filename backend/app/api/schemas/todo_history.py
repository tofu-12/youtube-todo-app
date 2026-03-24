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

    @model_validator(mode="after")
    def validate_next_scheduled_date_required_for_skipped(self):
        """Ensure next_scheduled_date is provided when status is SKIPPED."""
        if self.status == TodoStatus.SKIPPED and self.next_scheduled_date is None:
            raise ValueError(
                "next_scheduled_date is required when status is skipped"
            )
        return self


class TodoHistoryResponse(BaseModel):
    """Todo history output schema for API responses."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    video_id: uuid.UUID
    scheduled_date: datetime.date
    status: TodoStatus
    created_at: datetime.datetime
    updated_at: datetime.datetime
