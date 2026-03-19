"""API router for today and overdue endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.api.schemas.today as api_today_schema
from app.core.dependencies import get_current_user, get_db
import app.crud.schemas.user as crud_user_schema
from app.services import video_service

router = APIRouter(prefix="/api", tags=["today"])


@router.get("/today", response_model=list[api_today_schema.TodayVideoResponse])
def get_today_videos(
    db: Session = Depends(get_db),
    user: crud_user_schema.UserResponse = Depends(get_current_user),
) -> list[api_today_schema.TodayVideoResponse]:
    """Get videos scheduled for today."""
    return video_service.get_today_videos(db, user)


@router.get("/overdue", response_model=list[api_today_schema.TodayVideoResponse])
def get_overdue_videos(
    db: Session = Depends(get_db),
    user: crud_user_schema.UserResponse = Depends(get_current_user),
) -> list[api_today_schema.TodayVideoResponse]:
    """Get overdue videos (scheduled before today)."""
    return video_service.get_overdue_videos(db, user)
