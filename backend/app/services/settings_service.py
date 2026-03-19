"""Business logic for user settings management."""

import uuid
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import HTTPException
from sqlalchemy.orm import Session

import app.api.schemas.settings as api_settings_schema
from app.api.schemas.settings import SettingsUpdateRequest
from app.core.types import Timezone
from app.crud import user as crud_user
import app.crud.schemas.user as crud_user_schema
from app.crud.schemas.user import UserUpdate


def get_available_timezones() -> list[api_settings_schema.TimezoneOption]:
    """Return a list of available timezone options.

    Returns:
        A list of TimezoneOption with value and label for each supported timezone.
    """
    return [
        api_settings_schema.TimezoneOption(value=tz.value, label=tz.value)
        for tz in Timezone
    ]


def get_settings(db: Session, user_id: uuid.UUID) -> api_settings_schema.SettingsResponse | None:
    """Get user settings.

    Args:
        db: Database session.
        user_id: The user ID.

    Returns:
        The user settings, or None if user not found.
    """
    user = crud_user.get_user(db, user_id)
    if user is None:
        return None
    return api_settings_schema.SettingsResponse(
        day_change_time=user.day_change_time,
        timezone=user.timezone,
        workout_history_expires_days=user.workout_history_expires_days,
    )


def update_settings(
    db: Session, user_id: uuid.UUID, data: SettingsUpdateRequest
) -> api_settings_schema.SettingsResponse | None:
    """Update user settings with timezone validation.

    Args:
        db: Database session.
        user_id: The user ID.
        data: Settings update request.

    Returns:
        The updated settings, or None if user not found.

    Raises:
        HTTPException: If the timezone is invalid.
    """
    if data.timezone is not None:
        try:
            ZoneInfo(data.timezone)
        except (ZoneInfoNotFoundError, KeyError):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid timezone: {data.timezone}",
            )

    update_data = UserUpdate(**data.model_dump(exclude_unset=True))
    user = crud_user.update_user(db, user_id, update_data)
    if user is None:
        return None
    return api_settings_schema.SettingsResponse(
        day_change_time=user.day_change_time,
        timezone=user.timezone,
        workout_history_expires_days=user.workout_history_expires_days,
    )
