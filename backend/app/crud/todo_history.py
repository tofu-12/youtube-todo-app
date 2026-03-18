"""CRUD operations for TodoHistory model."""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.schemas.todo_history import (
    TodoHistoryFilter,
    TodoHistoryInsert,
    TodoHistoryResponse,
)
from app.models.todo_history import TodoHistory


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


def delete_todo_history(db: Session, entry_id: uuid.UUID) -> bool:
    """Delete a todo history entry. Returns True if deleted."""
    entry = db.get(TodoHistory, entry_id)
    if entry is None:
        return False
    db.delete(entry)
    db.commit()
    return True
