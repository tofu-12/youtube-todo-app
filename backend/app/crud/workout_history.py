"""CRUD operations for WorkoutHistory model."""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.schemas.workout_history import (
    WorkoutHistoryFilter,
    WorkoutHistoryInsert,
    WorkoutHistoryResponse,
)
from app.models.workout_history import WorkoutHistory


def create_workout_history(
    db: Session, data: WorkoutHistoryInsert
) -> WorkoutHistoryResponse:
    """Create a new workout history entry."""
    entry = WorkoutHistory(**data.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return WorkoutHistoryResponse.model_validate(entry)


def get_workout_histories(
    db: Session, filter_: WorkoutHistoryFilter
) -> list[WorkoutHistoryResponse]:
    """Get workout history entries with optional expiry filter."""
    stmt = select(WorkoutHistory).where(
        WorkoutHistory.user_id == filter_.user_id
    )
    if filter_.expires_after is not None:
        stmt = stmt.where(
            WorkoutHistory.expires_date >= filter_.expires_after
        )
    entries = db.scalars(stmt).all()
    return [WorkoutHistoryResponse.model_validate(e) for e in entries]


def delete_workout_history(db: Session, entry_id: uuid.UUID) -> bool:
    """Delete a workout history entry. Returns True if deleted."""
    entry = db.get(WorkoutHistory, entry_id)
    if entry is None:
        return False
    db.delete(entry)
    db.commit()
    return True
