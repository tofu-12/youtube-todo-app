"""FastAPI dependency injection providers."""

from collections.abc import Generator

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.crud.schemas.user import UserInsert, UserResponse
from app.crud.user import create_user
from app.models.user import User


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and ensure it is closed after use."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
) -> UserResponse:
    """Return the single MVP user, creating one if none exists."""
    stmt = select(User).limit(1)
    user = db.scalars(stmt).first()
    if user is not None:
        return UserResponse.model_validate(user)
    return create_user(db, UserInsert())
