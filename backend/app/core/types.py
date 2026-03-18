"""Enum definitions used across the application."""

import enum


class RecurrenceType(str, enum.Enum):
    """Recurrence rule types for video scheduling."""

    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    INTERVAL = "interval"


class DayOfWeek(str, enum.Enum):
    """Days of the week."""

    MON = "mon"
    TUE = "tue"
    WED = "wed"
    THU = "thu"
    FRI = "fri"
    SAT = "sat"
    SUN = "sun"


class TodoStatus(str, enum.Enum):
    """Status of a todo history entry."""

    COMPLETED = "completed"
    SKIPPED = "skipped"
