"""CRUD operations for VideoTag model."""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.schemas.tag import TagResponse
from app.models.tag import Tag
from app.models.video_tag import VideoTag


def set_video_tags(
    db: Session, user_id: uuid.UUID, video_id: uuid.UUID,
    tag_ids: list[uuid.UUID],
) -> list[TagResponse]:
    """Replace all tags for a video with the given tag IDs.

    Uses a SAVEPOINT and row-level locking to prevent race conditions
    between the DELETE and INSERT operations.
    """
    with db.begin_nested():
        db.query(VideoTag).filter(
            VideoTag.video_id == video_id
        ).with_for_update().all()
        db.query(VideoTag).filter(VideoTag.video_id == video_id).delete()
        for tag_id in tag_ids:
            video_tag = VideoTag(
                user_id=user_id, video_id=video_id, tag_id=tag_id
            )
            db.add(video_tag)

    db.commit()
    return get_video_tags(db, video_id)


def get_video_tags(
    db: Session, video_id: uuid.UUID
) -> list[TagResponse]:
    """Get all tags for a video."""
    stmt = (
        select(Tag)
        .join(VideoTag, VideoTag.tag_id == Tag.id)
        .where(VideoTag.video_id == video_id)
    )
    tags = db.scalars(stmt).all()
    return [TagResponse.model_validate(t) for t in tags]
