"""Integration tests for TodoHistory CRUD operations."""

import datetime
import uuid

from app.core.types import TodoStatus
from app.crud.schemas.todo_history import (
    TodoHistoryFilter,
    TodoHistoryInsert,
    TodoHistoryStatsFilter,
)
from app.crud.todo_history import (
    create_todo_history,
    delete_todo_history,
    get_todo_histories,
    get_todo_history_stats,
)
from app.crud.video_tag import set_video_tags


class TestCreateTodoHistory:
    """Tests for create_todo_history."""

    def test_create_todo_history_completed(self, db, sample_user, sample_video):
        """Creating a COMPLETED todo history entry."""
        data = TodoHistoryInsert(
            user_id=sample_user.id,
            video_id=sample_video.id,
            scheduled_date=datetime.date(2026, 3, 18),
            status=TodoStatus.COMPLETED,
        )
        result = create_todo_history(db, data)

        assert result.status == TodoStatus.COMPLETED
        assert result.scheduled_date == datetime.date(2026, 3, 18)
        assert result.user_id == sample_user.id
        assert result.video_id == sample_video.id

    def test_create_todo_history_skipped(self, db, sample_user, sample_video):
        """Creating a SKIPPED todo history entry."""
        data = TodoHistoryInsert(
            user_id=sample_user.id,
            video_id=sample_video.id,
            scheduled_date=datetime.date(2026, 3, 18),
            status=TodoStatus.SKIPPED,
        )
        result = create_todo_history(db, data)
        assert result.status == TodoStatus.SKIPPED


class TestGetTodoHistories:
    """Tests for get_todo_histories."""

    def test_get_todo_histories_all(self, db, sample_user, sample_video):
        """Getting all todo histories for a user."""
        for day_offset in range(3):
            data = TodoHistoryInsert(
                user_id=sample_user.id,
                video_id=sample_video.id,
                scheduled_date=datetime.date(2026, 3, 18)
                + datetime.timedelta(days=day_offset),
                status=TodoStatus.COMPLETED,
            )
            create_todo_history(db, data)

        result = get_todo_histories(
            db, TodoHistoryFilter(user_id=sample_user.id)
        )
        assert len(result) == 3

    def test_get_todo_histories_by_date(self, db, sample_user, sample_video):
        """Getting todo histories filtered by scheduled_date."""
        target_date = datetime.date(2026, 3, 18)
        other_date = datetime.date(2026, 3, 19)

        for d in [target_date, other_date]:
            data = TodoHistoryInsert(
                user_id=sample_user.id,
                video_id=sample_video.id,
                scheduled_date=d,
                status=TodoStatus.COMPLETED,
            )
            create_todo_history(db, data)

        result = get_todo_histories(
            db,
            TodoHistoryFilter(
                user_id=sample_user.id, scheduled_date=target_date
            ),
        )
        assert len(result) == 1
        assert result[0].scheduled_date == target_date

    def test_get_todo_histories_empty(self, db, user_factory):
        """Getting todo histories for a user with none returns empty list."""
        user = user_factory()
        result = get_todo_histories(
            db, TodoHistoryFilter(user_id=user.id)
        )
        assert result == []


class TestDeleteTodoHistory:
    """Tests for delete_todo_history."""

    def test_delete_todo_history(self, db, sample_user, sample_video):
        """Deleting an existing todo history entry returns True."""
        data = TodoHistoryInsert(
            user_id=sample_user.id,
            video_id=sample_video.id,
            scheduled_date=datetime.date(2026, 3, 18),
            status=TodoStatus.COMPLETED,
        )
        entry = create_todo_history(db, data)
        assert delete_todo_history(db, entry.id, sample_user.id) is True

    def test_delete_todo_history_not_found(self, db, sample_user):
        """Deleting a nonexistent todo history entry returns False."""
        assert delete_todo_history(db, uuid.uuid4(), sample_user.id) is False


class TestGetTodoHistoryStats:
    """Tests for get_todo_history_stats."""

    def test_stats_mixed_statuses(self, db, sample_user, sample_video):
        """Stats correctly count completed and skipped entries."""
        for i, status in enumerate(
            [TodoStatus.COMPLETED, TodoStatus.COMPLETED, TodoStatus.SKIPPED]
        ):
            create_todo_history(
                db,
                TodoHistoryInsert(
                    user_id=sample_user.id,
                    video_id=sample_video.id,
                    scheduled_date=datetime.date(2026, 3, 18)
                    + datetime.timedelta(days=i),
                    status=status,
                ),
            )

        result = get_todo_history_stats(
            db, TodoHistoryStatsFilter(user_id=sample_user.id)
        )
        assert result.completed_count == 2
        assert result.skipped_count == 1
        assert result.total_count == 3
        assert result.completion_rate == 66.7

    def test_stats_date_range(self, db, sample_user, sample_video):
        """Stats respect date_from filter."""
        for day in [10, 15, 20]:
            create_todo_history(
                db,
                TodoHistoryInsert(
                    user_id=sample_user.id,
                    video_id=sample_video.id,
                    scheduled_date=datetime.date(2026, 3, day),
                    status=TodoStatus.COMPLETED,
                ),
            )

        result = get_todo_history_stats(
            db,
            TodoHistoryStatsFilter(
                user_id=sample_user.id,
                date_from=datetime.date(2026, 3, 14),
            ),
        )
        assert result.total_count == 2

    def test_stats_with_tag_filter(
        self, db, sample_user, sample_video, video_factory, tag_factory
    ):
        """Stats respect tag_id filter."""
        tag = tag_factory(sample_user.id, name="yoga")
        set_video_tags(db, sample_user.id, sample_video.id, [tag.id])

        other_video = video_factory(sample_user.id)

        create_todo_history(
            db,
            TodoHistoryInsert(
                user_id=sample_user.id,
                video_id=sample_video.id,
                scheduled_date=datetime.date(2026, 3, 18),
                status=TodoStatus.COMPLETED,
            ),
        )
        create_todo_history(
            db,
            TodoHistoryInsert(
                user_id=sample_user.id,
                video_id=other_video.id,
                scheduled_date=datetime.date(2026, 3, 19),
                status=TodoStatus.COMPLETED,
            ),
        )

        result = get_todo_history_stats(
            db,
            TodoHistoryStatsFilter(user_id=sample_user.id, tag_id=tag.id),
        )
        assert result.total_count == 1
        assert result.completed_count == 1

    def test_stats_empty(self, db, user_factory):
        """Stats for a user with no history returns zeros."""
        user = user_factory()
        result = get_todo_history_stats(
            db, TodoHistoryStatsFilter(user_id=user.id)
        )
        assert result.completed_count == 0
        assert result.skipped_count == 0
        assert result.total_count == 0
        assert result.completion_rate == 0.0

    def test_stats_user_isolation(
        self, db, sample_user, sample_video, user_factory, video_factory
    ):
        """Stats only include entries for the specified user."""
        other_user = user_factory()
        other_video = video_factory(other_user.id)

        create_todo_history(
            db,
            TodoHistoryInsert(
                user_id=sample_user.id,
                video_id=sample_video.id,
                scheduled_date=datetime.date(2026, 3, 18),
                status=TodoStatus.COMPLETED,
            ),
        )
        create_todo_history(
            db,
            TodoHistoryInsert(
                user_id=other_user.id,
                video_id=other_video.id,
                scheduled_date=datetime.date(2026, 3, 18),
                status=TodoStatus.SKIPPED,
            ),
        )

        result = get_todo_history_stats(
            db, TodoHistoryStatsFilter(user_id=sample_user.id)
        )
        assert result.total_count == 1
        assert result.completed_count == 1
        assert result.skipped_count == 0
