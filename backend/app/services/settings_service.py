"""Business logic for user settings management."""

import uuid
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.api.schemas.settings import SettingsOut, SettingsUpdateRequest
from app.crud import user as crud_user
from app.crud.schemas.user import UserUpdate


def get_settings(db: Session, user_id: uuid.UUID) -> SettingsOut | None:
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
    return SettingsOut(
        day_change_time=user.day_change_time,
        timezone=user.timezone,
    )


def update_settings(
    db: Session, user_id: uuid.UUID, data: SettingsUpdateRequest
) -> SettingsOut | None:
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
    return SettingsOut(
        day_change_time=user.day_change_time,
        timezone=user.timezone,
    )
