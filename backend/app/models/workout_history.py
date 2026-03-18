"""WorkoutHistory model definition."""

import datetime
import uuid

from sqlalchemy import Date, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class WorkoutHistory(TimestampMixin, Base):
    """Record of a workout session performed by the user."""

    __tablename__ = "workout_histories"
    __table_args__ = (
        UniqueConstraint(
            "video_id",
            "performed_date",
            name="uq_workout_history_video_date",
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    video_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("videos.id", ondelete="CASCADE"), nullable=False
    )
    performed_date: Mapped[datetime.date] = mapped_column(
        Date, nullable=False
    )
    performed_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    expires_date: Mapped[datetime.date] = mapped_column(
        Date, nullable=False
    )

    # Relationships
    user = relationship("User", back_populates="workout_histories")
    video = relationship("Video", back_populates="workout_histories")
