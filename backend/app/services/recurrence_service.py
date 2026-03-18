"""Business logic for video recurrence rules."""

import datetime
import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.api.schemas.recurrence import RecurrenceRequest
from app.core.types import DayOfWeek, RecurrenceType
from app.crud import recurrence as crud_recurrence
from app.crud import video as crud_video
from app.crud.schemas.recurrence import RecurrenceResponse, RecurrenceUpsert
from app.crud.schemas.video import VideoUpdate

_WEEKDAY_MAP: dict[DayOfWeek, int] = {
    DayOfWeek.MON: 0,
    DayOfWeek.TUE: 1,
    DayOfWeek.WED: 2,
    DayOfWeek.THU: 3,
    DayOfWeek.FRI: 4,
    DayOfWeek.SAT: 5,
    DayOfWeek.SUN: 6,
}


def calculate_next_scheduled_date(
    recurrence_type: RecurrenceType,
    last_performed_date: datetime.date,
    interval_days: Optional[int],
    weekdays: list[DayOfWeek],
) -> Optional[datetime.date]:
    """Calculate the next scheduled date based on recurrence rule.

    Args:
        recurrence_type: The type of recurrence.
        last_performed_date: The date the video was last performed.
        interval_days: Number of days for interval recurrence.
        weekdays: List of weekdays for weekly recurrence.

    Returns:
        The next scheduled date, or None for NONE recurrence.
    """
    if recurrence_type == RecurrenceType.NONE:
        return None

    if recurrence_type == RecurrenceType.DAILY:
        return last_performed_date + datetime.timedelta(days=1)

    if recurrence_type == RecurrenceType.INTERVAL:
        if interval_days is None:
            return None
        return last_performed_date + datetime.timedelta(days=interval_days)

    if recurrence_type == RecurrenceType.WEEKLY:
        if not weekdays:
            return None
        target_days = {_WEEKDAY_MAP[d] for d in weekdays}
        for offset in range(1, 8):
            candidate = last_performed_date + datetime.timedelta(days=offset)
            if candidate.weekday() in target_days:
                return candidate

    return None


def upsert_video_recurrence(
    db: Session,
    user_id: uuid.UUID,
    video_id: uuid.UUID,
    data: RecurrenceRequest,
) -> RecurrenceResponse:
    """Create or update a video recurrence and recalculate schedule.

    Args:
        db: Database session.
        user_id: The user ID.
        video_id: The video ID.
        data: Recurrence request data.

    Returns:
        The upserted recurrence response.
    """
    upsert_data = RecurrenceUpsert(
        user_id=user_id,
        video_id=video_id,
        recurrence_type=data.recurrence_type,
        interval_days=data.interval_days,
        weekdays=data.weekdays,
    )
    result = crud_recurrence.upsert_recurrence(db, upsert_data)

    video = crud_video.get_video(db, video_id)
    if video and video.last_performed_date is not None:
        next_date = calculate_next_scheduled_date(
            data.recurrence_type,
            video.last_performed_date,
            data.interval_days,
            data.weekdays,
        )
        crud_video.update_video(
            db, video_id, VideoUpdate(next_scheduled_date=next_date)
        )

    return result
