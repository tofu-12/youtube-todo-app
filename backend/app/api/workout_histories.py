"""API router for workout history endpoints."""

import datetime
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import app.api.schemas.workout_history as api_workout_history_schema
from app.api.schemas.workout_history import WorkoutHistoryCreateRequest
from app.core.date import get_logical_today
from app.core.dependencies import get_current_user, get_db
from app.crud import video as crud_video
from app.crud import workout_history as crud_workout_history
import app.crud.schemas.user as crud_user_schema
import app.crud.schemas.workout_history as crud_workout_history_schema

router = APIRouter(
    prefix="/api/workout-histories", tags=["workout-histories"]
)


@router.get("", response_model=list[api_workout_history_schema.WorkoutHistoryResponse])
def list_workout_histories(
    expires_after: Optional[datetime.date] = Query(default=None),
    db: Session = Depends(get_db),
    user: crud_user_schema.UserResponse = Depends(get_current_user),
) -> list[api_workout_history_schema.WorkoutHistoryResponse]:
    """Get workout history entries with optional expiry filter.

    Defaults to filtering by logical today if no expires_after is given.
    """
    if expires_after is None:
        expires_after = get_logical_today(
            user.day_change_time, user.timezone
        )
    filter_ = crud_workout_history_schema.WorkoutHistoryFilter(
        user_id=user.id, expires_after=expires_after
    )
    entries = crud_workout_history.get_workout_histories(db, filter_)
    return [
        api_workout_history_schema.WorkoutHistoryResponse.model_validate(e)
        for e in entries
    ]


@router.post(
    "",
    response_model=api_workout_history_schema.WorkoutHistoryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_workout_history(
    data: WorkoutHistoryCreateRequest,
    db: Session = Depends(get_db),
    user: crud_user_schema.UserResponse = Depends(get_current_user),
) -> api_workout_history_schema.WorkoutHistoryResponse:
    """Create a workout history entry.

    Server calculates performed_date (logical today), performed_at (UTC now),
    and expires_date (performed_date + expires_days).
    """
    video = crud_video.get_video(db, data.video_id, user.id)
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")

    performed_date = get_logical_today(
        user.day_change_time, user.timezone
    )
    performed_at = datetime.datetime.now(datetime.timezone.utc)
    expires_date = performed_date + datetime.timedelta(days=user.workout_history_expires_days)

    insert_data = crud_workout_history_schema.WorkoutHistoryInsert(
        user_id=user.id,
        video_id=data.video_id,
        performed_date=performed_date,
        performed_at=performed_at,
        expires_date=expires_date,
    )
    entry = crud_workout_history.create_workout_history(db, insert_data)
    return api_workout_history_schema.WorkoutHistoryResponse.model_validate(entry)


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout_history(
    entry_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: crud_user_schema.UserResponse = Depends(get_current_user),
) -> None:
    """Delete a workout history entry."""
    if not crud_workout_history.delete_workout_history(db, entry_id, user.id):
        raise HTTPException(
            status_code=404, detail="Workout history entry not found"
        )
