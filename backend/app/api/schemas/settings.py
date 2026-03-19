"""API schemas for settings endpoints."""

import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TimezoneOption(BaseModel):
    """A timezone option for the settings UI."""

    value: str
    label: str


class SettingsUpdateRequest(BaseModel):
    """Request body for updating user settings."""

    day_change_time: Optional[datetime.time] = None
    timezone: Optional[str] = None
    workout_history_expires_days: Optional[int] = Field(
        default=None, ge=1, le=365
    )


class SettingsResponse(BaseModel):
    """Settings output schema for API responses."""

    model_config = ConfigDict(from_attributes=True)

    day_change_time: datetime.time
    timezone: str
    workout_history_expires_days: int
