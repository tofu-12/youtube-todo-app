"""API router for video endpoints."""

import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.video import VideoCreateRequest, VideoOut, VideoUpdateRequest
from app.core.dependencies import get_current_user, get_db
from app.crud.schemas.user import UserResponse
from app.services import video_service

router = APIRouter(prefix="/api/videos", tags=["videos"])


@router.get("", response_model=list[VideoOut])
def list_videos(
    db: Session = Depends(get_db),
    user: UserResponse = Depends(get_current_user),
) -> list[VideoOut]:
    """Get all videos for the current user."""
    return video_service.list_videos(db, user.id)


@router.post("", response_model=VideoOut, status_code=status.HTTP_201_CREATED)
def create_video(
    data: VideoCreateRequest,
    db: Session = Depends(get_db),
    user: UserResponse = Depends(get_current_user),
) -> VideoOut:
    """Create a new video."""
    return video_service.create_video(db, user.id, data)


@router.get("/{video_id}", response_model=VideoOut)
def get_video(
    video_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: UserResponse = Depends(get_current_user),
) -> VideoOut:
    """Get a video by ID."""
    result = video_service.get_video_detail(db, user.id, video_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return result


@router.put("/{video_id}", response_model=VideoOut)
def update_video(
    video_id: uuid.UUID,
    data: VideoUpdateRequest,
    db: Session = Depends(get_db),
    user: UserResponse = Depends(get_current_user),
) -> VideoOut:
    """Update a video."""
    result = video_service.update_video(db, user.id, video_id, data)
    if result is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return result


@router.delete("/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_video(
    video_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: UserResponse = Depends(get_current_user),
) -> None:
    """Delete a video."""
    if not video_service.delete_video(db, user.id, video_id):
        raise HTTPException(status_code=404, detail="Video not found")
