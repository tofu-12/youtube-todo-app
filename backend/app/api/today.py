"""API router for today and overdue endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas.today import TodayVideoOut
from app.core.dependencies import get_current_user, get_db
from app.crud.schemas.user import UserResponse
from app.services import video_service

router = APIRouter(prefix="/api", tags=["today"])


@router.get("/today", response_model=list[TodayVideoOut])
def get_today_videos(
    db: Session = Depends(get_db),
    user: UserResponse = Depends(get_current_user),
) -> list[TodayVideoOut]:
    """Get videos scheduled for today."""
    return video_service.get_today_videos(db, user)


@router.get("/overdue", response_model=list[TodayVideoOut])
def get_overdue_videos(
    db: Session = Depends(get_db),
    user: UserResponse = Depends(get_current_user),
) -> list[TodayVideoOut]:
    """Get overdue videos (scheduled before today)."""
    return video_service.get_overdue_videos(db, user)
