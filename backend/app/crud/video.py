"""CRUD operations for Video model."""

import uuid
from typing import Optional

from sqlalchemy import asc, desc, distinct, func, select
from sqlalchemy.orm import Session, selectinload

from app.crud.schemas.video import (
    ScheduledStatus,
    SortOrder,
    VideoFilter,
    VideoInsert,
    VideoResponse,
    VideoUpdate,
)
from app.models.tag import Tag
from app.models.video import Video
from app.models.video_tag import VideoTag


def create_video(db: Session, data: VideoInsert) -> VideoResponse:
    """Create a new video."""
    video = Video(**data.model_dump())
    db.add(video)
    db.commit()
    db.refresh(video)
    return VideoResponse.model_validate(video)


def get_video(
    db: Session, video_id: uuid.UUID, user_id: uuid.UUID
) -> Optional[VideoResponse]:
    """Get a video by ID, scoped to the given user."""
    stmt = select(Video).where(Video.id == video_id, Video.user_id == user_id)
    video = db.scalars(stmt).first()
    if video is None:
        return None
    return VideoResponse.model_validate(video)


def get_videos(db: Session, filter_: VideoFilter) -> list[VideoResponse]:
    """Get all videos for a user."""
    stmt = select(Video).where(Video.user_id == filter_.user_id)
    videos = db.scalars(stmt).all()
    return [VideoResponse.model_validate(v) for v in videos]


def get_videos_with_tags(
    db: Session, filter_: VideoFilter
) -> tuple[list[Video], int]:
    """Get videos for a user with tags eagerly loaded, filtered and paginated."""
    stmt = select(Video).where(Video.user_id == filter_.user_id)

    # Name partial match filter
    if filter_.name:
        stmt = stmt.where(Video.name.ilike(f"%{filter_.name}%"))

    # Tag names AND filter
    if filter_.tag_names:
        stmt = (
            stmt.join(Video.video_tags)
            .join(VideoTag.tag)
            .where(Tag.name.in_(filter_.tag_names))
            .group_by(Video.id)
            .having(
                func.count(distinct(Tag.id)) == len(filter_.tag_names)
            )
        )

    # Scheduled status filter
    if filter_.scheduled_status and filter_.today is not None:
        if filter_.scheduled_status == ScheduledStatus.OVERDUE:
            stmt = stmt.where(
                Video.next_scheduled_date.isnot(None),
                Video.next_scheduled_date < filter_.today,
            )
        elif filter_.scheduled_status == ScheduledStatus.TODAY:
            stmt = stmt.where(Video.next_scheduled_date == filter_.today)
        elif filter_.scheduled_status == ScheduledStatus.UPCOMING:
            stmt = stmt.where(Video.next_scheduled_date > filter_.today)
        elif filter_.scheduled_status == ScheduledStatus.UNSCHEDULED:
            stmt = stmt.where(Video.next_scheduled_date.is_(None))

    # Total count before pagination
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = db.scalar(count_stmt) or 0

    # Sort
    sort_col = getattr(Video, filter_.sort_field.value)
    order_fn = asc if filter_.sort_order == SortOrder.ASC else desc
    stmt = stmt.order_by(order_fn(sort_col).nulls_last())

    # Pagination and eager loading
    stmt = (
        stmt.offset(filter_.skip)
        .limit(filter_.limit)
        .options(selectinload(Video.video_tags).selectinload(VideoTag.tag))
    )

    return list(db.scalars(stmt).unique().all()), total


def update_video(
    db: Session, video_id: uuid.UUID, data: VideoUpdate, user_id: uuid.UUID
) -> Optional[VideoResponse]:
    """Update a video, scoped to the given user."""
    stmt = select(Video).where(Video.id == video_id, Video.user_id == user_id)
    video = db.scalars(stmt).first()
    if video is None:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(video, key, value)
    db.commit()
    db.refresh(video)
    return VideoResponse.model_validate(video)


def delete_video(
    db: Session, video_id: uuid.UUID, user_id: uuid.UUID
) -> bool:
    """Delete a video, scoped to the given user."""
    stmt = select(Video).where(Video.id == video_id, Video.user_id == user_id)
    video = db.scalars(stmt).first()
    if video is None:
        return False
    db.delete(video)
    db.commit()
    return True
