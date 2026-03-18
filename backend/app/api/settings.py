"""API router for user settings endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.schemas.settings import SettingsOut, SettingsUpdateRequest
from app.core.dependencies import get_current_user, get_db
from app.crud.schemas.user import UserResponse
from app.services import settings_service

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("", response_model=SettingsOut)
def get_settings(
    db: Session = Depends(get_db),
    user: UserResponse = Depends(get_current_user),
) -> SettingsOut:
    """Get current user settings."""
    result = settings_service.get_settings(db, user.id)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@router.put("", response_model=SettingsOut)
def update_settings(
    data: SettingsUpdateRequest,
    db: Session = Depends(get_db),
    user: UserResponse = Depends(get_current_user),
) -> SettingsOut:
    """Update user settings."""
    result = settings_service.update_settings(db, user.id, data)
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    return result
