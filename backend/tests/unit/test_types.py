"""Unit tests for enum and type definitions."""

import enum

from app.core.types import DayOfWeek, RecurrenceType, TodoStatus


class TestRecurrenceType:
    """Tests for RecurrenceType enum."""

    def test_recurrence_type_values(self):
        """RecurrenceType has the expected values."""
        assert RecurrenceType.NONE == "none"
        assert RecurrenceType.DAILY == "daily"
        assert RecurrenceType.WEEKLY == "weekly"
        assert RecurrenceType.INTERVAL == "interval"

    def test_recurrence_type_members_count(self):
        """RecurrenceType has exactly 4 members."""
        assert len(RecurrenceType) == 4


class TestDayOfWeek:
    """Tests for DayOfWeek enum."""

    def test_day_of_week_values(self):
        """DayOfWeek has correct values for all 7 days."""
        expected = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        actual = [d.value for d in DayOfWeek]
        assert actual == expected

    def test_day_of_week_members_count(self):
        """DayOfWeek has exactly 7 members."""
        assert len(DayOfWeek) == 7


class TestTodoStatus:
    """Tests for TodoStatus enum."""

    def test_todo_status_values(self):
        """TodoStatus has the expected values."""
        assert TodoStatus.COMPLETED == "completed"
        assert TodoStatus.SKIPPED == "skipped"

    def test_todo_status_members_count(self):
        """TodoStatus has exactly 2 members."""
        assert len(TodoStatus) == 2


class TestEnumsAreStrEnum:
    """Tests that all enums inherit from str."""

    def test_enums_are_str_enum(self):
        """All application enums are str enums."""
        for enum_cls in (RecurrenceType, DayOfWeek, TodoStatus):
            assert issubclass(enum_cls, str)
            assert issubclass(enum_cls, enum.Enum)
