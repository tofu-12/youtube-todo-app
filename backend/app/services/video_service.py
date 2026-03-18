"""Business logic for video management."""

import uuid

from sqlalchemy.orm import Session

from app.api.schemas.today import TodayVideoOut
from app.api.schemas.video import TagOut, VideoCreateRequest, VideoOut, VideoUpdateRequest
from app.core.date import get_logical_today
from app.crud import tag as crud_tag
from app.crud import video as crud_video
from app.crud import video_tag as crud_video_tag
from app.crud.schemas.tag import TagInsert
from app.crud.schemas.user import UserResponse
from app.crud.schemas.video import VideoFilter, VideoInsert, VideoResponse, VideoUpdate


def _resolve_tags(
    db: Session, user_id: uuid.UUID, tag_names: list[str]
) -> list[uuid.UUID]:
    """Resolve tag names to tag IDs, creating tags as needed."""
    tag_ids = []
    for name in tag_names:
        tag = crud_tag.get_or_create_tag(db, TagInsert(user_id=user_id, name=name))
        tag_ids.append(tag.id)
    return tag_ids


def _build_video_out(
    db: Session, video_resp: "VideoResponse"
) -> VideoOut:
    """Build a VideoOut from a VideoResponse by attaching tags."""
    tags = crud_video_tag.get_video_tags(db, video_resp.id)
    return VideoOut(
        id=video_resp.id,
        name=video_resp.name,
        url=video_resp.url,
        comment=video_resp.comment,
        last_performed_date=video_resp.last_performed_date,
        next_scheduled_date=video_resp.next_scheduled_date,
        tags=[TagOut(id=t.id, name=t.name) for t in tags],
        created_at=video_resp.created_at,
        updated_at=video_resp.updated_at,
    )


def create_video(
    db: Session, user_id: uuid.UUID, data: VideoCreateRequest
) -> VideoOut:
    """Create a video with tags.

    Args:
        db: Database session.
        user_id: The user ID.
        data: Video creation request.

    Returns:
        The created video with tags.
    """
    video = crud_video.create_video(
        db,
        VideoInsert(user_id=user_id, name=data.name, url=data.url, comment=data.comment),
    )
    tag_ids = _resolve_tags(db, user_id, data.tag_names)
    if tag_ids:
        crud_video_tag.set_video_tags(db, user_id, video.id, tag_ids)
    return _build_video_out(db, video)


def get_video_detail(
    db: Session, video_id: uuid.UUID
) -> VideoOut | None:
    """Get a video with its tags.

    Args:
        db: Database session.
        video_id: The video ID.

    Returns:
        The video with tags, or None if not found.
    """
    video = crud_video.get_video(db, video_id)
    if video is None:
        return None
    return _build_video_out(db, video)


def list_videos(
    db: Session, user_id: uuid.UUID
) -> list[VideoOut]:
    """List all videos for a user with their tags.

    Args:
        db: Database session.
        user_id: The user ID.

    Returns:
        List of videos with tags.
    """
    videos = crud_video.get_videos(db, VideoFilter(user_id=user_id))
    return [_build_video_out(db, v) for v in videos]


def update_video(
    db: Session,
    user_id: uuid.UUID,
    video_id: uuid.UUID,
    data: VideoUpdateRequest,
) -> VideoOut | None:
    """Update a video and optionally its tags.

    Args:
        db: Database session.
        user_id: The user ID.
        video_id: The video ID.
        data: Video update request.

    Returns:
        The updated video with tags, or None if not found.
    """
    update_data = VideoUpdate(
        name=data.name,
        url=data.url,
        comment=data.comment,
    )
    video = crud_video.update_video(db, video_id, update_data)
    if video is None:
        return None
    if data.tag_names is not None:
        tag_ids = _resolve_tags(db, user_id, data.tag_names)
        crud_video_tag.set_video_tags(db, user_id, video_id, tag_ids)
    return _build_video_out(db, video)


def delete_video(db: Session, video_id: uuid.UUID) -> bool:
    """Delete a video.

    Args:
        db: Database session.
        video_id: The video ID.

    Returns:
        True if deleted, False if not found.
    """
    return crud_video.delete_video(db, video_id)


def get_today_videos(
    db: Session, user: UserResponse
) -> list[TodayVideoOut]:
    """Get videos scheduled for today or earlier.

    Args:
        db: Database session.
        user: The current user.

    Returns:
        List of videos due today.
    """
    today = get_logical_today(user.day_change_time, user.timezone)
    videos = crud_video.get_videos(db, VideoFilter(user_id=user.id))
    result = []
    for v in videos:
        if v.next_scheduled_date is not None and v.next_scheduled_date <= today:
            tags = crud_video_tag.get_video_tags(db, v.id)
            result.append(
                TodayVideoOut(
                    id=v.id,
                    name=v.name,
                    url=v.url,
                    comment=v.comment,
                    next_scheduled_date=v.next_scheduled_date,
                    tags=[TagOut(id=t.id, name=t.name) for t in tags],
                )
            )
    return result


def get_overdue_videos(
    db: Session, user: UserResponse
) -> list[TodayVideoOut]:
    """Get videos that are overdue (scheduled before today).

    Args:
        db: Database session.
        user: The current user.

    Returns:
        List of overdue videos.
    """
    today = get_logical_today(user.day_change_time, user.timezone)
    videos = crud_video.get_videos(db, VideoFilter(user_id=user.id))
    result = []
    for v in videos:
        if v.next_scheduled_date is not None and v.next_scheduled_date < today:
            tags = crud_video_tag.get_video_tags(db, v.id)
            result.append(
                TodayVideoOut(
                    id=v.id,
                    name=v.name,
                    url=v.url,
                    comment=v.comment,
                    next_scheduled_date=v.next_scheduled_date,
                    tags=[TagOut(id=t.id, name=t.name) for t in tags],
                )
            )
    return result
