"""CRUD operations for User model."""

import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.crud.schemas.user import UserInsert, UserResponse, UserUpdate
from app.models.user import User


def create_user(db: Session, data: UserInsert) -> UserResponse:
    """Create a new user."""
    user = User(**data.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)


def get_user(db: Session, user_id: uuid.UUID) -> UserResponse | None:
    """Get a user by ID."""
    user = db.get(User, user_id)
    if user is None:
        return None
    return UserResponse.model_validate(user)


def update_user(
    db: Session, user_id: uuid.UUID, data: UserUpdate
) -> UserResponse | None:
    """Update user settings."""
    user = db.get(User, user_id)
    if user is None:
        return None
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return UserResponse.model_validate(user)
