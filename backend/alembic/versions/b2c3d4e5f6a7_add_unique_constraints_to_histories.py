"""add unique constraints to history tables

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-03-18 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b2c3d4e5f6a7"
down_revision: Union[str, Sequence[str]] = "a1b2c3d4e5f6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add unique constraints to todo_histories and workout_histories."""
    op.create_unique_constraint(
        "uq_todo_history_video_date",
        "todo_histories",
        ["video_id", "scheduled_date"],
    )
    op.create_unique_constraint(
        "uq_workout_history_video_date",
        "workout_histories",
        ["video_id", "performed_date"],
    )


def downgrade() -> None:
    """Remove unique constraints from todo_histories and workout_histories."""
    op.drop_constraint(
        "uq_workout_history_video_date",
        "workout_histories",
        type_="unique",
    )
    op.drop_constraint(
        "uq_todo_history_video_date",
        "todo_histories",
        type_="unique",
    )
