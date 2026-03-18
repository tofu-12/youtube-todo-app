"""lowercase day_of_week enum values

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-03-19 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c3d4e5f6a7b8"
down_revision: Union[str, Sequence[str]] = "b2c3d4e5f6a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_OLD_VALUES = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]
_NEW_VALUES = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


def upgrade() -> None:
    """Rename day_of_week enum labels from uppercase to lowercase."""
    for old, new in zip(_OLD_VALUES, _NEW_VALUES):
        op.execute(
            f"ALTER TYPE day_of_week RENAME VALUE '{old}' TO '{new}'"
        )


def downgrade() -> None:
    """Rename day_of_week enum labels from lowercase to uppercase."""
    for new, old in zip(_NEW_VALUES, _OLD_VALUES):
        op.execute(
            f"ALTER TYPE day_of_week RENAME VALUE '{new}' TO '{old}'"
        )
