"""Add workout_history_expires_days to users.

Revision ID: e5f6a7b8c9d0
Revises: d4e5f6a7b8c9
Create Date: 2026-03-19

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "e5f6a7b8c9d0"
down_revision: Union[str, None] = "d4e5f6a7b8c9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add workout_history_expires_days column with CHECK constraint."""
    op.add_column(
        "users",
        sa.Column(
            "workout_history_expires_days",
            sa.Integer(),
            nullable=False,
            server_default="90",
        ),
    )
    op.create_check_constraint(
        "ck_users_workout_history_expires_days",
        "users",
        "workout_history_expires_days >= 1 AND workout_history_expires_days <= 365",
    )


def downgrade() -> None:
    """Remove workout_history_expires_days column and constraint."""
    op.drop_constraint(
        "ck_users_workout_history_expires_days", "users", type_="check"
    )
    op.drop_column("users", "workout_history_expires_days")
