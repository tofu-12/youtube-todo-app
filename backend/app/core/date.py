"""Logical date utility for day-change-time aware date calculation."""

import datetime
from zoneinfo import ZoneInfo


def get_logical_today(
    day_change_time: datetime.time, timezone: str
) -> datetime.date:
    """Return the logical 'today' based on day-change-time and timezone.

    If the current local time is before day_change_time, the logical date
    is yesterday. Otherwise, it is today.

    Args:
        day_change_time: The time at which a new day begins for the user.
        timezone: IANA timezone string (e.g. "Asia/Tokyo").

    Returns:
        The logical date for the user.
    """
    tz = ZoneInfo(timezone)
    now_local = datetime.datetime.now(tz)
    if now_local.time() < day_change_time:
        return now_local.date() - datetime.timedelta(days=1)
    return now_local.date()
