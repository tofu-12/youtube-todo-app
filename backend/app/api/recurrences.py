"""API router for video recurrence endpoints."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import app.api.schemas.recurrence as api_recurrence_schema
from app.api.schemas.recurrence import RecurrenceRequest
from app.core.dependencies import get_current_user, get_db
from app.core.types import DayOfWeek
from app.crud import recurrence as crud_recurrence
import app.crud.schemas.user as crud_user_schema
from app.services import recurrence_service

router = APIRouter(
    prefix="/api/videos/{video_id}/recurrence", tags=["recurrences"]
)


@router.get("", response_model=api_recurrence_schema.RecurrenceResponse)
def get_recurrence(
    video_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: crud_user_schema.UserResponse = Depends(get_current_user),
) -> api_recurrence_schema.RecurrenceResponse:
    """Get recurrence rule for a video."""
    result = crud_recurrence.get_recurrence_by_video(db, video_id, user.id)
    if result is None:
        raise HTTPException(status_code=404, detail="Recurrence not found")
    return api_recurrence_schema.RecurrenceResponse(
        id=result.id,
        recurrence_type=result.recurrence_type,
        interval_days=result.interval_days,
        weekdays=[w.day_of_week for w in result.weekdays],
        created_at=result.created_at,
        updated_at=result.updated_at,
    )


@router.put("", response_model=api_recurrence_schema.RecurrenceResponse)
def upsert_recurrence(
    video_id: uuid.UUID,
    data: RecurrenceRequest,
    db: Session = Depends(get_db),
    user: crud_user_schema.UserResponse = Depends(get_current_user),
) -> api_recurrence_schema.RecurrenceResponse:
    """Create or update recurrence rule for a video."""
    result = recurrence_service.upsert_video_recurrence(
        db, user.id, video_id, data
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return api_recurrence_schema.RecurrenceResponse(
        id=result.id,
        recurrence_type=result.recurrence_type,
        interval_days=result.interval_days,
        weekdays=[w.day_of_week for w in result.weekdays],
        created_at=result.created_at,
        updated_at=result.updated_at,
    )


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
def delete_recurrence(
    video_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: crud_user_schema.UserResponse = Depends(get_current_user),
) -> None:
    """Delete recurrence rule for a video."""
    if not crud_recurrence.delete_recurrence(db, video_id, user.id):
        raise HTTPException(status_code=404, detail="Recurrence not found")
