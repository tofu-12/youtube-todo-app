"""API router for todo history endpoints."""

import datetime
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.schemas.todo_history import TodoHistoryCreateRequest, TodoHistoryOut
from app.core.dependencies import get_current_user, get_db
from app.core.types import TodoStatus
from app.crud import recurrence as crud_recurrence
from app.crud import todo_history as crud_todo_history
from app.crud import video as crud_video
from app.crud.schemas.todo_history import TodoHistoryFilter, TodoHistoryInsert
from app.crud.schemas.user import UserResponse
from app.crud.schemas.video import VideoUpdate
from app.services.recurrence_service import calculate_next_scheduled_date

router = APIRouter(prefix="/api/todo-histories", tags=["todo-histories"])


@router.get("", response_model=list[TodoHistoryOut])
def list_todo_histories(
    scheduled_date: Optional[datetime.date] = Query(default=None),
    db: Session = Depends(get_db),
    user: UserResponse = Depends(get_current_user),
) -> list[TodoHistoryOut]:
    """Get todo history entries with optional date filter."""
    filter_ = TodoHistoryFilter(
        user_id=user.id, scheduled_date=scheduled_date
    )
    return crud_todo_history.get_todo_histories(db, filter_)


@router.post(
    "", response_model=TodoHistoryOut, status_code=status.HTTP_201_CREATED
)
def create_todo_history(
    data: TodoHistoryCreateRequest,
    db: Session = Depends(get_db),
    user: UserResponse = Depends(get_current_user),
) -> TodoHistoryOut:
    """Create a todo history entry.

    When status is COMPLETED, updates last_performed_date and
    recalculates next_scheduled_date.
    """
    insert_data = TodoHistoryInsert(
        user_id=user.id,
        video_id=data.video_id,
        scheduled_date=data.scheduled_date,
        status=data.status,
    )
    entry = crud_todo_history.create_todo_history(db, insert_data)

    if data.status == TodoStatus.COMPLETED:
        crud_video.update_video(
            db,
            data.video_id,
            VideoUpdate(last_performed_date=data.scheduled_date),
            user.id,
        )
        recurrence = crud_recurrence.get_recurrence_by_video(
            db, data.video_id, user.id
        )
        if recurrence is not None:
            next_date = calculate_next_scheduled_date(
                recurrence.recurrence_type,
                data.scheduled_date,
                recurrence.interval_days,
                [w.day_of_week for w in recurrence.weekdays],
            )
            crud_video.update_video(
                db,
                data.video_id,
                VideoUpdate(next_scheduled_date=next_date),
                user.id,
            )

    return entry


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo_history(
    entry_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: UserResponse = Depends(get_current_user),
) -> None:
    """Delete a todo history entry."""
    if not crud_todo_history.delete_todo_history(db, entry_id, user.id):
        raise HTTPException(
            status_code=404, detail="Todo history entry not found"
        )
