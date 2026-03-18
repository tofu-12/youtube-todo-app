"""API schemas for today/overdue endpoints."""

import datetime
import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.api.schemas.video import TagOut


class TodayVideoOut(BaseModel):
    """Video output schema for today/overdue lists."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    url: str
    comment: Optional[str]
    next_scheduled_date: Optional[datetime.date]
    tags: list[TagOut]
