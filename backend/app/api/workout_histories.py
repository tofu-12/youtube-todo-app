"""API router for workout history endpoints."""

import datetime
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.schemas.workout_history import (
    WorkoutHistoryCreateRequest,
    WorkoutHistoryOut,
)
from app.core.date import get_logical_today
from app.core.dependencies import get_current_user, get_db
from app.crud import workout_history as crud_workout_history
from app.crud.schemas.user import UserResponse
from app.crud.schemas.workout_history import (
    WorkoutHistoryFilter,
    WorkoutHistoryInsert,
)

router = APIRouter(
    prefix="/api/workout-histories", tags=["workout-histories"]
)


@router.get("", response_model=list[WorkoutHistoryOut])
def list_workout_histories(
    expires_after: Optional[datetime.date] = Query(default=None),
    db: Session = Depends(get_db),
    user: UserResponse = Depends(get_current_user),
) -> list[WorkoutHistoryOut]:
    """Get workout history entries with optional expiry filter.

    Defaults to filtering by logical today if no expires_after is given.
    """
    if expires_after is None:
        expires_after = get_logical_today(
            user.day_change_time, user.timezone
        )
    filter_ = WorkoutHistoryFilter(
        user_id=user.id, expires_after=expires_after
    )
    return crud_workout_history.get_workout_histories(db, filter_)


@router.post(
    "",
    response_model=WorkoutHistoryOut,
    status_code=status.HTTP_201_CREATED,
)
def create_workout_history(
    data: WorkoutHistoryCreateRequest,
    db: Session = Depends(get_db),
    user: UserResponse = Depends(get_current_user),
) -> WorkoutHistoryOut:
    """Create a workout history entry.

    Server calculates performed_date (logical today), performed_at (UTC now),
    and expires_date (performed_date + expires_days).
    """
    performed_date = get_logical_today(
        user.day_change_time, user.timezone
    )
    performed_at = datetime.datetime.now(datetime.timezone.utc)
    expires_date = performed_date + datetime.timedelta(days=data.expires_days)

    insert_data = WorkoutHistoryInsert(
        user_id=user.id,
        video_id=data.video_id,
        performed_date=performed_date,
        performed_at=performed_at,
        expires_date=expires_date,
    )
    return crud_workout_history.create_workout_history(db, insert_data)


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_workout_history(
    entry_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: UserResponse = Depends(get_current_user),
) -> None:
    """Delete a workout history entry."""
    if not crud_workout_history.delete_workout_history(db, entry_id):
        raise HTTPException(
            status_code=404, detail="Workout history entry not found"
        )
