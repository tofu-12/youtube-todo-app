"""CRUD operations for TodoHistory model."""

import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.types import TodoStatus
from app.crud.schemas.todo_history import (
    TodoHistoryFilter,
    TodoHistoryInsert,
    TodoHistoryResponse,
    TodoHistoryStatsFilter,
    TodoHistoryStatsResponse,
)
from app.models.todo_history import TodoHistory
from app.models.video_tag import VideoTag


def create_todo_history(
    db: Session, data: TodoHistoryInsert
) -> TodoHistoryResponse:
    """Create a new todo history entry."""
    entry = TodoHistory(**data.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return TodoHistoryResponse.model_validate(entry)


def get_todo_histories(
    db: Session, filter_: TodoHistoryFilter
) -> list[TodoHistoryResponse]:
    """Get todo history entries with optional date filter."""
    stmt = select(TodoHistory).where(
        TodoHistory.user_id == filter_.user_id
    )
    if filter_.scheduled_date is not None:
        stmt = stmt.where(
            TodoHistory.scheduled_date == filter_.scheduled_date
        )
    entries = db.scalars(stmt).all()
    return [TodoHistoryResponse.model_validate(e) for e in entries]


def delete_todo_history(
    db: Session, entry_id: uuid.UUID, user_id: uuid.UUID
) -> bool:
    """Delete a todo history entry, scoped to the given user."""
    stmt = select(TodoHistory).where(
        TodoHistory.id == entry_id, TodoHistory.user_id == user_id
    )
    entry = db.scalars(stmt).first()
    if entry is None:
        return False
    db.delete(entry)
    db.commit()
    return True


def get_todo_history_stats(
    db: Session, filter_: TodoHistoryStatsFilter
) -> TodoHistoryStatsResponse:
    """Aggregate todo history counts by status with optional filters."""
    stmt = (
        select(TodoHistory.status, func.count().label("cnt"))
        .where(TodoHistory.user_id == filter_.user_id)
    )
    if filter_.date_from is not None:
        stmt = stmt.where(TodoHistory.scheduled_date >= filter_.date_from)
    if filter_.tag_id is not None:
        stmt = stmt.join(
            VideoTag, TodoHistory.video_id == VideoTag.video_id
        ).where(VideoTag.tag_id == filter_.tag_id)
    stmt = stmt.group_by(TodoHistory.status)

    rows = db.execute(stmt).all()
    counts = {row.status: row.cnt for row in rows}
    completed = counts.get(TodoStatus.COMPLETED, 0)
    skipped = counts.get(TodoStatus.SKIPPED, 0)
    total = completed + skipped
    rate = round(completed / total * 100, 1) if total > 0 else 0.0

    return TodoHistoryStatsResponse(
        completed_count=completed,
        skipped_count=skipped,
        total_count=total,
        completion_rate=rate,
    )
