"""CRUD operations for Video model."""

import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.schemas.video import (
    VideoFilter,
    VideoInsert,
    VideoResponse,
    VideoUpdate,
)
from app.models.video import Video


def create_video(db: Session, data: VideoInsert) -> VideoResponse:
    """Create a new video."""
    video = Video(**data.model_dump())
    db.add(video)
    db.commit()
    db.refresh(video)
    return VideoResponse.model_validate(video)


def get_video(db: Session, video_id: uuid.UUID) -> Optional[VideoResponse]:
    """Get a video by ID."""
    video = db.get(Video, video_id)
    if video is None:
        return None
    return VideoResponse.model_validate(video)


def get_videos(db: Session, filter_: VideoFilter) -> list[VideoResponse]:
    """Get all videos for a user."""
    stmt = select(Video).where(Video.user_id == filter_.user_id)
    videos = db.scalars(stmt).all()
    return [VideoResponse.model_validate(v) for v in videos]


def update_video(
    db: Session, video_id: uuid.UUID, data: VideoUpdate
) -> Optional[VideoResponse]:
    """Update a video."""
    video = db.get(Video, video_id)
    if video is None:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(video, key, value)
    db.commit()
    db.refresh(video)
    return VideoResponse.model_validate(video)


def delete_video(db: Session, video_id: uuid.UUID) -> bool:
    """Delete a video. Returns True if deleted, False if not found."""
    video = db.get(Video, video_id)
    if video is None:
        return False
    db.delete(video)
    db.commit()
    return True
