"""add check constraint and updated_at triggers

Revision ID: a1b2c3d4e5f6
Revises: 4f5595aee0e8
Create Date: 2026-03-18 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str]] = "4f5595aee0e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# All tables that have an updated_at column.
TABLES_WITH_UPDATED_AT = [
    "users",
    "videos",
    "video_recurrences",
    "video_weekdays",
    "todo_histories",
    "tags",
    "video_tags",
    "workout_histories",
]


def upgrade() -> None:
    """Add interval_days check constraint and updated_at triggers."""
    # CHECK constraint: interval_days must be >= 1 when recurrence_type is 'interval'
    op.create_check_constraint(
        "ck_interval_days_required",
        "video_recurrences",
        "(recurrence_type != 'interval') OR "
        "(interval_days IS NOT NULL AND interval_days >= 1)",
    )

    # Create trigger function for auto-updating updated_at
    op.execute(
        """
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    # Attach trigger to each table
    for table in TABLES_WITH_UPDATED_AT:
        op.execute(
            f"""
            CREATE TRIGGER tr_{table}_updated_at
                BEFORE UPDATE ON {table}
                FOR EACH ROW
                EXECUTE FUNCTION update_updated_at_column();
            """
        )


def downgrade() -> None:
    """Remove triggers, trigger function, and check constraint."""
    for table in TABLES_WITH_UPDATED_AT:
        op.execute(f"DROP TRIGGER IF EXISTS tr_{table}_updated_at ON {table};")

    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column();")

    op.drop_constraint(
        "ck_interval_days_required", "video_recurrences", type_="check"
    )
