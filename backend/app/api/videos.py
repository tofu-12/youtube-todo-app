"""API router for video endpoints."""

import uuid
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

import app.api.schemas.video as api_video_schema
from app.api.schemas.video import VideoCreateRequest, VideoUpdateRequest
from app.core.dependencies import get_current_user, get_db
import app.crud.schemas.user as crud_user_schema
from app.crud.schemas.video import ScheduledStatus, SortOrder, VideoSortField
from app.services import video_service

router = APIRouter(prefix="/api/videos", tags=["videos"])


@router.get("/all", response_model=list[api_video_schema.VideoResponse])
def list_all_videos(
    db: Session = Depends(get_db),
    user: crud_user_schema.UserResponse = Depends(get_current_user),
) -> list[api_video_schema.VideoResponse]:
    """Get all videos for the current user without pagination."""
    return video_service.list_all_videos(db, user.id)


@router.get("", response_model=api_video_schema.PaginatedVideoResponse)
def list_videos(
    name: Optional[str] = Query(None),
    tag_names: Optional[list[str]] = Query(None),
    scheduled_status: Optional[ScheduledStatus] = Query(None),
    sort_field: VideoSortField = Query(VideoSortField.CREATED_AT),
    sort_order: SortOrder = Query(SortOrder.DESC),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    user: crud_user_schema.UserResponse = Depends(get_current_user),
) -> api_video_schema.PaginatedVideoResponse:
    """Get videos for the current user with filtering, sorting, and pagination."""
    return video_service.list_videos(
        db,
        user,
        name=name,
        tag_names=tag_names,
        scheduled_status=scheduled_status,
        sort_field=sort_field,
        sort_order=sort_order,
        skip=skip,
        limit=limit,
    )


@router.post("", response_model=api_video_schema.VideoResponse, status_code=status.HTTP_201_CREATED)
def create_video(
    data: VideoCreateRequest,
    db: Session = Depends(get_db),
    user: crud_user_schema.UserResponse = Depends(get_current_user),
) -> api_video_schema.VideoResponse:
    """Create a new video."""
    return video_service.create_video(db, user.id, data)


@router.get("/{video_id}", response_model=api_video_schema.VideoResponse)
def get_video(
    video_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: crud_user_schema.UserResponse = Depends(get_current_user),
) -> api_video_schema.VideoResponse:
    """Get a video by ID."""
    result = video_service.get_video_detail(db, user.id, video_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return result


@router.put("/{video_id}", response_model=api_video_schema.VideoResponse)
def update_video(
    video_id: uuid.UUID,
    data: VideoUpdateRequest,
    db: Session = Depends(get_db),
    user: crud_user_schema.UserResponse = Depends(get_current_user),
) -> api_video_schema.VideoResponse:
    """Update a video."""
    result = video_service.update_video(db, user.id, video_id, data)
    if result is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return result


@router.delete("/{video_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_video(
    video_id: uuid.UUID,
    db: Session = Depends(get_db),
    user: crud_user_schema.UserResponse = Depends(get_current_user),
) -> None:
    """Delete a video."""
    if not video_service.delete_video(db, user.id, video_id):
        raise HTTPException(status_code=404, detail="Video not found")
