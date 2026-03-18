"""VideoWeekday model definition."""

import uuid

from sqlalchemy import Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.types import DayOfWeek
from app.models.base import TimestampMixin


class VideoWeekday(TimestampMixin, Base):
    """Weekly day-of-week setting for a video recurrence."""

    __tablename__ = "video_weekdays"
    __table_args__ = (
        UniqueConstraint(
            "video_recurrence_id",
            "day_of_week",
            name="uq_video_weekday_recurrence_day",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    video_recurrence_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("video_recurrences.id", ondelete="CASCADE"),
        nullable=False,
    )
    day_of_week: Mapped[DayOfWeek] = mapped_column(
        Enum(DayOfWeek, name="day_of_week"),
        nullable=False,
    )

    # Relationships
    user = relationship("User", back_populates="video_weekdays")
    video_recurrence = relationship(
        "VideoRecurrence", back_populates="weekdays"
    )
