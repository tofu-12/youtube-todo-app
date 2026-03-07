"""create initial tables

Revision ID: 4f5595aee0e8
Revises:
Create Date: 2026-03-07 20:58:17.943333

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "4f5595aee0e8"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Enum types
recurrence_type_enum = postgresql.ENUM(
    "none", "daily", "weekly", "interval",
    name="recurrence_type",
    create_type=False,
)
day_of_week_enum = postgresql.ENUM(
    "MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN",
    name="day_of_week",
    create_type=False,
)
todo_status_enum = postgresql.ENUM(
    "completed", "skipped",
    name="todo_status",
    create_type=False,
)


def upgrade() -> None:
    """Create all initial tables and enum types."""
    # Create enum types
    recurrence_type_enum.create(op.get_bind(), checkfirst=True)
    day_of_week_enum.create(op.get_bind(), checkfirst=True)
    todo_status_enum.create(op.get_bind(), checkfirst=True)

    # Users
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("day_change_time", sa.Time(), nullable=False),
        sa.Column("timezone", sa.String(length=50), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Videos
    op.create_table(
        "videos",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("url", sa.String(length=500), nullable=False),
        sa.Column(
            "tags", postgresql.ARRAY(sa.String()), nullable=False
        ),
        sa.Column("comment", sa.Text(), nullable=True),
        sa.Column("last_performed_date", sa.Date(), nullable=True),
        sa.Column("next_scheduled_date", sa.Date(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Video Recurrences
    op.create_table(
        "video_recurrences",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("video_id", sa.UUID(), nullable=False),
        sa.Column("recurrence_type", recurrence_type_enum, nullable=False),
        sa.Column("interval_days", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["video_id"], ["videos.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("video_id"),
    )

    # Video Weekdays
    op.create_table(
        "video_weekdays",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("video_recurrence_id", sa.UUID(), nullable=False),
        sa.Column("day_of_week", day_of_week_enum, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["video_recurrence_id"],
            ["video_recurrences.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "video_recurrence_id",
            "day_of_week",
            name="uq_video_weekday_recurrence_day",
        ),
    )

    # Todo Histories
    op.create_table(
        "todo_histories",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("video_id", sa.UUID(), nullable=False),
        sa.Column("scheduled_date", sa.Date(), nullable=False),
        sa.Column("status", todo_status_enum, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["video_id"], ["videos.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # Workout Histories
    op.create_table(
        "workout_histories",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("video_id", sa.UUID(), nullable=False),
        sa.Column("performed_date", sa.Date(), nullable=False),
        sa.Column(
            "performed_at", sa.DateTime(timezone=True), nullable=False
        ),
        sa.Column("expires_date", sa.Date(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["video_id"], ["videos.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Drop all tables and enum types."""
    op.drop_table("workout_histories")
    op.drop_table("todo_histories")
    op.drop_table("video_weekdays")
    op.drop_table("video_recurrences")
    op.drop_table("videos")
    op.drop_table("users")

    todo_status_enum.drop(op.get_bind(), checkfirst=True)
    day_of_week_enum.drop(op.get_bind(), checkfirst=True)
    recurrence_type_enum.drop(op.get_bind(), checkfirst=True)
