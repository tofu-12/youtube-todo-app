"""API schemas for settings endpoints."""

import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SettingsUpdateRequest(BaseModel):
    """Request body for updating user settings."""

    day_change_time: Optional[datetime.time] = None
    timezone: Optional[str] = None


class SettingsOut(BaseModel):
    """Settings output schema for API responses."""

    model_config = ConfigDict(from_attributes=True)

    day_change_time: datetime.time
    timezone: str
