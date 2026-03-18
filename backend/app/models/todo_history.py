"""TodoHistory model definition."""

import datetime
import uuid

from sqlalchemy import Date, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.types import TodoStatus
from app.models.base import TimestampMixin


class TodoHistory(TimestampMixin, Base):
    """Record of a todo item being completed or skipped."""

    __tablename__ = "todo_histories"
    __table_args__ = (
        UniqueConstraint(
            "video_id",
            "scheduled_date",
            name="uq_todo_history_video_date",
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
    scheduled_date: Mapped[datetime.date] = mapped_column(
        Date, nullable=False
    )
    status: Mapped[TodoStatus] = mapped_column(
        Enum(TodoStatus, name="todo_status"),
        nullable=False,
    )

    # Relationships
    user = relationship("User", back_populates="todo_histories")
    video = relationship("Video", back_populates="todo_histories")
