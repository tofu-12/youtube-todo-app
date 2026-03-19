"""API router for tag endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.schemas.video import TagResponse
from app.core.dependencies import get_current_user, get_db
from app.crud.schemas.user import UserResponse
from app.crud.tag import get_tags

router = APIRouter(prefix="/api/tags", tags=["tags"])


@router.get("", response_model=list[TagResponse])
def list_tags(
    db: Session = Depends(get_db),
    user: UserResponse = Depends(get_current_user),
) -> list[TagResponse]:
    """Get all tags for the current user."""
    return get_tags(db, user.id)
