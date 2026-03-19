"""API router for authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.schemas.auth import AuthRequest, AuthResponse
from app.core.dependencies import get_db
from app.crud.schemas.user import UserInsert
from app.crud.user import create_user, get_user_by_email

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post(
    "/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED
)
def register(
    data: AuthRequest,
    db: Session = Depends(get_db),
) -> AuthResponse:
    """Register a new user with an email address."""
    existing = get_user_by_email(db, data.email)
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )
    user = create_user(db, UserInsert(email=data.email))
    return AuthResponse(id=user.id, email=user.email)


@router.post("/login", response_model=AuthResponse)
def login(
    data: AuthRequest,
    db: Session = Depends(get_db),
) -> AuthResponse:
    """Log in with an existing email address."""
    user = get_user_by_email(db, data.email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Email not registered",
        )
    return AuthResponse(id=user.id, email=user.email)
