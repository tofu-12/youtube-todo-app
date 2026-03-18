"""Integration tests for database triggers."""

import datetime

from sqlalchemy import text

from app.models.user import User
from app.models.video import Video

# A deliberately old timestamp to verify trigger resets it.
_OLD_TIMESTAMP = datetime.datetime(2000, 1, 1, tzinfo=datetime.timezone.utc)


class TestUpdatedAtTrigger:
    """Tests for the updated_at auto-update trigger.

    PostgreSQL's ``now()`` returns the transaction start time, so within
    a single transaction the trigger always produces the same timestamp.
    To test the trigger we first set ``updated_at`` to a very old value
    using a raw UPDATE that bypasses the trigger (by setting the column
    directly), then perform another UPDATE that fires the trigger, and
    verify that ``updated_at`` was overwritten with a recent timestamp.
    """

    def test_updated_at_auto_update_user(self, db, sample_user):
        """Trigger resets updated_at when a user record is modified."""
        # Set updated_at to a known old value (this UPDATE also fires
        # the trigger, but the result is now(), not '2000-01-01').
        # We therefore disable the trigger, set the old value, then
        # re-enable and do a real UPDATE.
        db.execute(text("ALTER TABLE users DISABLE TRIGGER tr_users_updated_at"))
        db.execute(
            text("UPDATE users SET updated_at = :ts WHERE id = :id"),
            {"ts": _OLD_TIMESTAMP, "id": str(sample_user.id)},
        )
        db.flush()
        db.execute(text("ALTER TABLE users ENABLE TRIGGER tr_users_updated_at"))

        user = db.get(User, sample_user.id)
        db.refresh(user)
        assert user.updated_at == _OLD_TIMESTAMP

        # Now do a real update that fires the trigger.
        db.execute(
            text("UPDATE users SET timezone = 'UTC' WHERE id = :id"),
            {"id": str(sample_user.id)},
        )
        db.flush()
        db.refresh(user)

        assert user.updated_at > _OLD_TIMESTAMP

    def test_updated_at_auto_update_video(self, db, sample_video):
        """Trigger resets updated_at when a video record is modified."""
        db.execute(text("ALTER TABLE videos DISABLE TRIGGER tr_videos_updated_at"))
        db.execute(
            text("UPDATE videos SET updated_at = :ts WHERE id = :id"),
            {"ts": _OLD_TIMESTAMP, "id": str(sample_video.id)},
        )
        db.flush()
        db.execute(text("ALTER TABLE videos ENABLE TRIGGER tr_videos_updated_at"))

        video = db.get(Video, sample_video.id)
        db.refresh(video)
        assert video.updated_at == _OLD_TIMESTAMP

        db.execute(
            text("UPDATE videos SET name = 'Updated' WHERE id = :id"),
            {"id": str(sample_video.id)},
        )
        db.flush()
        db.refresh(video)

        assert video.updated_at > _OLD_TIMESTAMP

    def test_created_at_equals_updated_at_on_create(self, db, sample_user):
        """On creation, created_at and updated_at are approximately equal."""
        user = db.get(User, sample_user.id)
        diff = abs(
            (user.updated_at - user.created_at).total_seconds()
        )
        assert diff < 2.0
