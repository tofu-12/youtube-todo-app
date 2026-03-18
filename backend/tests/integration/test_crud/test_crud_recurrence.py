"""Integration tests for Recurrence CRUD operations."""

import uuid

from app.core.types import DayOfWeek, RecurrenceType
from app.crud.recurrence import (
    delete_recurrence,
    get_recurrence_by_video,
    upsert_recurrence,
)
from app.crud.schemas.recurrence import RecurrenceUpsert


class TestUpsertRecurrence:
    """Tests for upsert_recurrence."""

    def test_upsert_recurrence_create_daily(
        self, db, sample_user, sample_video
    ):
        """Creating a DAILY recurrence stores it correctly."""
        data = RecurrenceUpsert(
            user_id=sample_user.id,
            video_id=sample_video.id,
            recurrence_type=RecurrenceType.DAILY,
        )
        result = upsert_recurrence(db, data)

        assert result.recurrence_type == RecurrenceType.DAILY
        assert result.interval_days is None
        assert result.weekdays == []
        assert result.video_id == sample_video.id

    def test_upsert_recurrence_create_weekly_with_weekdays(
        self, db, sample_user, sample_video
    ):
        """Creating a WEEKLY recurrence with weekdays stores them."""
        data = RecurrenceUpsert(
            user_id=sample_user.id,
            video_id=sample_video.id,
            recurrence_type=RecurrenceType.WEEKLY,
            weekdays=[DayOfWeek.MON, DayOfWeek.WED, DayOfWeek.FRI],
        )
        result = upsert_recurrence(db, data)

        assert result.recurrence_type == RecurrenceType.WEEKLY
        weekday_values = {w.day_of_week for w in result.weekdays}
        assert weekday_values == {DayOfWeek.MON, DayOfWeek.WED, DayOfWeek.FRI}

    def test_upsert_recurrence_create_interval(
        self, db, sample_user, sample_video
    ):
        """Creating an INTERVAL recurrence with interval_days stores it."""
        data = RecurrenceUpsert(
            user_id=sample_user.id,
            video_id=sample_video.id,
            recurrence_type=RecurrenceType.INTERVAL,
            interval_days=3,
        )
        result = upsert_recurrence(db, data)

        assert result.recurrence_type == RecurrenceType.INTERVAL
        assert result.interval_days == 3

    def test_upsert_recurrence_update(
        self, db, sample_user, sample_video
    ):
        """Updating an existing recurrence changes its type."""
        create_data = RecurrenceUpsert(
            user_id=sample_user.id,
            video_id=sample_video.id,
            recurrence_type=RecurrenceType.DAILY,
        )
        upsert_recurrence(db, create_data)

        update_data = RecurrenceUpsert(
            user_id=sample_user.id,
            video_id=sample_video.id,
            recurrence_type=RecurrenceType.WEEKLY,
            weekdays=[DayOfWeek.SAT],
        )
        result = upsert_recurrence(db, update_data)

        assert result.recurrence_type == RecurrenceType.WEEKLY
        assert len(result.weekdays) == 1
        assert result.weekdays[0].day_of_week == DayOfWeek.SAT

    def test_upsert_recurrence_replaces_weekdays(
        self, db, sample_user, sample_video
    ):
        """Upserting replaces old weekdays with new ones entirely."""
        data1 = RecurrenceUpsert(
            user_id=sample_user.id,
            video_id=sample_video.id,
            recurrence_type=RecurrenceType.WEEKLY,
            weekdays=[DayOfWeek.MON, DayOfWeek.TUE],
        )
        upsert_recurrence(db, data1)

        data2 = RecurrenceUpsert(
            user_id=sample_user.id,
            video_id=sample_video.id,
            recurrence_type=RecurrenceType.WEEKLY,
            weekdays=[DayOfWeek.THU],
        )
        result = upsert_recurrence(db, data2)

        assert len(result.weekdays) == 1
        assert result.weekdays[0].day_of_week == DayOfWeek.THU


class TestGetRecurrenceByVideo:
    """Tests for get_recurrence_by_video."""

    def test_get_recurrence_by_video_found(
        self, db, sample_user, sample_video
    ):
        """Getting an existing recurrence returns correct data."""
        data = RecurrenceUpsert(
            user_id=sample_user.id,
            video_id=sample_video.id,
            recurrence_type=RecurrenceType.DAILY,
        )
        created = upsert_recurrence(db, data)
        result = get_recurrence_by_video(db, sample_video.id, sample_user.id)

        assert result is not None
        assert result.id == created.id
        assert result.recurrence_type == RecurrenceType.DAILY

    def test_get_recurrence_by_video_not_found(self, db, sample_user):
        """Getting a recurrence for a nonexistent video returns None."""
        result = get_recurrence_by_video(db, uuid.uuid4(), sample_user.id)
        assert result is None


class TestDeleteRecurrence:
    """Tests for delete_recurrence."""

    def test_delete_recurrence(self, db, sample_user, sample_video):
        """Deleting an existing recurrence returns True."""
        data = RecurrenceUpsert(
            user_id=sample_user.id,
            video_id=sample_video.id,
            recurrence_type=RecurrenceType.DAILY,
        )
        upsert_recurrence(db, data)

        assert delete_recurrence(db, sample_video.id, sample_user.id) is True
        assert get_recurrence_by_video(db, sample_video.id, sample_user.id) is None

    def test_delete_recurrence_not_found(self, db, sample_user):
        """Deleting a nonexistent recurrence returns False."""
        assert delete_recurrence(db, uuid.uuid4(), sample_user.id) is False
