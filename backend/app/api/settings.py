"""API router for user settings endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.api.schemas.settings as api_settings_schema
from app.api.schemas.settings import SettingsUpdateRequest
from app.core.dependencies import get_current_user, get_db
import app.crud.schemas.user as crud_user_schema
from app.services import settings_service

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("/timezones", response_model=list[api_settings_schema.TimezoneOption])
def get_timezones() -> list[api_settings_schema.TimezoneOption]:
    """Get available timezone options."""
    return settings_service.get_available_timezones()


@router.get("", response_model=api_settings_schema.SettingsResponse)
def get_settings(
    db: Session = Depends(get_db),
    user: crud_user_schema.UserResponse = Depends(get_current_user),
) -> api_settings_schema.SettingsResponse:
    """Get current user settings."""
    result = settings_service.get_settings(db, user.id)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.put("", response_model=api_settings_schema.SettingsResponse)
def update_settings(
    data: SettingsUpdateRequest,
    db: Session = Depends(get_db),
    user: crud_user_schema.UserResponse = Depends(get_current_user),
) -> api_settings_schema.SettingsResponse:
    """Update user settings."""
    result = settings_service.update_settings(db, user.id, data)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result
