"""VideoRecurrence model definition."""

import uuid

from sqlalchemy import Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.types import RecurrenceType
from app.models.base import TimestampMixin


class VideoRecurrence(TimestampMixin, Base):
    """Recurrence rule for a video (1:1 with Video)."""

    __tablename__ = "video_recurrences"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    video_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("videos.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )
    recurrence_type: Mapped[RecurrenceType] = mapped_column(
        Enum(RecurrenceType, name="recurrence_type"),
        nullable=False,
    )
    interval_days: Mapped[int | None] = mapped_column(
        Integer, nullable=True
    )

    # Relationships
    user = relationship("User", back_populates="video_recurrences")
    video = relationship("Video", back_populates="recurrence")
    weekdays = relationship(
        "VideoWeekday",
        back_populates="video_recurrence",
        cascade="all, delete-orphan",
    )
