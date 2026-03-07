"""Video model definition."""

import datetime
import uuid

from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class Video(TimestampMixin, Base):
    """Video table storing YouTube video metadata and schedule info."""

    __tablename__ = "videos"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_performed_date: Mapped[datetime.date | None] = mapped_column(
        Date, nullable=True
    )
    next_scheduled_date: Mapped[datetime.date | None] = mapped_column(
        Date, nullable=True
    )

    # Relationships
    user = relationship("User", back_populates="videos")
    recurrence = relationship(
        "VideoRecurrence",
        back_populates="video",
        uselist=False,
        cascade="all, delete-orphan",
    )
    video_tags = relationship(
        "VideoTag", back_populates="video", cascade="all, delete-orphan"
    )
    todo_histories = relationship(
        "TodoHistory", back_populates="video", cascade="all, delete-orphan"
    )
    workout_histories = relationship(
        "WorkoutHistory", back_populates="video", cascade="all, delete-orphan"
    )
