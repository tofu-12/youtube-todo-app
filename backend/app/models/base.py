"""Shared model mixins and enum definitions."""

import enum

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """Mixin that adds created_at and updated_at columns (UTC)."""

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class RecurrenceType(str, enum.Enum):
    """Recurrence rule types for video scheduling."""

    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    INTERVAL = "interval"


class DayOfWeek(str, enum.Enum):
    """Days of the week."""

    MON = "MON"
    TUE = "TUE"
    WED = "WED"
    THU = "THU"
    FRI = "FRI"
    SAT = "SAT"
    SUN = "SUN"


class TodoStatus(str, enum.Enum):
    """Status of a todo history entry."""

    COMPLETED = "completed"
    SKIPPED = "skipped"
