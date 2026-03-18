"""CRUD operations for VideoRecurrence and VideoWeekday models."""

import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.schemas.recurrence import RecurrenceResponse, RecurrenceUpsert
from app.models.video_recurrence import VideoRecurrence
from app.models.video_weekday import VideoWeekday


def upsert_recurrence(
    db: Session, data: RecurrenceUpsert
) -> RecurrenceResponse:
    """Create or update a video recurrence with weekdays."""
    stmt = select(VideoRecurrence).where(
        VideoRecurrence.video_id == data.video_id
    )
    recurrence = db.scalars(stmt).first()

    if recurrence is None:
        recurrence = VideoRecurrence(
            user_id=data.user_id,
            video_id=data.video_id,
            recurrence_type=data.recurrence_type,
            interval_days=data.interval_days,
        )
        db.add(recurrence)
    else:
        recurrence.recurrence_type = data.recurrence_type
        recurrence.interval_days = data.interval_days

    db.flush()

    # Replace weekdays
    db.query(VideoWeekday).filter(
        VideoWeekday.video_recurrence_id == recurrence.id
    ).delete()

    for day in data.weekdays:
        weekday = VideoWeekday(
            user_id=data.user_id,
            video_recurrence_id=recurrence.id,
            day_of_week=day,
        )
        db.add(weekday)

    db.commit()
    db.refresh(recurrence)
    return RecurrenceResponse.model_validate(recurrence)


def get_recurrence_by_video(
    db: Session, video_id: uuid.UUID
) -> Optional[RecurrenceResponse]:
    """Get recurrence rule for a video."""
    stmt = select(VideoRecurrence).where(
        VideoRecurrence.video_id == video_id
    )
    recurrence = db.scalars(stmt).first()
    if recurrence is None:
        return None
    return RecurrenceResponse.model_validate(recurrence)


def delete_recurrence(db: Session, video_id: uuid.UUID) -> bool:
    """Delete recurrence rule for a video. Returns True if deleted."""
    stmt = select(VideoRecurrence).where(
        VideoRecurrence.video_id == video_id
    )
    recurrence = db.scalars(stmt).first()
    if recurrence is None:
        return False
    db.delete(recurrence)
    db.commit()
    return True
