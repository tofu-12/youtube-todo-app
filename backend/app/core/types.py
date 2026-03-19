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


class Timezone(str, enum.Enum):
    """Supported IANA timezone identifiers."""

    UTC = "UTC"
    ASIA_TOKYO = "Asia/Tokyo"
    ASIA_SEOUL = "Asia/Seoul"
    ASIA_SHANGHAI = "Asia/Shanghai"
    ASIA_SINGAPORE = "Asia/Singapore"
    ASIA_KOLKATA = "Asia/Kolkata"
    EUROPE_LONDON = "Europe/London"
    EUROPE_PARIS = "Europe/Paris"
    AMERICA_NEW_YORK = "America/New_York"
    AMERICA_CHICAGO = "America/Chicago"
    AMERICA_LOS_ANGELES = "America/Los_Angeles"
    AMERICA_SAO_PAULO = "America/Sao_Paulo"
    PACIFIC_HONOLULU = "Pacific/Honolulu"
    PACIFIC_AUCKLAND = "Pacific/Auckland"
    AUSTRALIA_SYDNEY = "Australia/Sydney"
