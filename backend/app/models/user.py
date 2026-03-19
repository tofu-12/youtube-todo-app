"""User model definition."""

import datetime
import uuid

from sqlalchemy import String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class User(TimestampMixin, Base):
    """User table storing per-user settings."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False
    )
    day_change_time: Mapped[datetime.time] = mapped_column(
        Time, default=datetime.time(0, 0), nullable=False
    )
    timezone: Mapped[str] = mapped_column(
        String(50), default="Asia/Tokyo", nullable=False
    )

    # Relationships (cascade delete all child records)
    videos = relationship(
        "Video", back_populates="user", cascade="all, delete-orphan"
    )
    video_recurrences = relationship(
        "VideoRecurrence", back_populates="user", cascade="all, delete-orphan"
    )
    video_weekdays = relationship(
        "VideoWeekday", back_populates="user", cascade="all, delete-orphan"
    )
    tags = relationship(
        "Tag", back_populates="user", cascade="all, delete-orphan"
    )
    video_tags = relationship(
        "VideoTag", back_populates="user", cascade="all, delete-orphan"
    )
    todo_histories = relationship(
        "TodoHistory", back_populates="user", cascade="all, delete-orphan"
    )
    workout_histories = relationship(
        "WorkoutHistory", back_populates="user", cascade="all, delete-orphan"
    )
