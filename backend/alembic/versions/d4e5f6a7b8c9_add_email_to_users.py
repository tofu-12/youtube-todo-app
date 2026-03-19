"""Add email column to users table.

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-03-19

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d4e5f6a7b8c9"
down_revision = "c3d4e5f6a7b8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add email column to users table."""
    # Add column as nullable first to handle existing rows.
    op.add_column("users", sa.Column("email", sa.String(255), nullable=True))

    # Set a placeholder email for any existing rows.
    op.execute(
        "UPDATE users SET email = 'user_' || id::text || '@example.com' "
        "WHERE email IS NULL"
    )

    # Make the column non-nullable.
    op.alter_column("users", "email", nullable=False)

    # Add unique constraint.
    op.create_unique_constraint("uq_users_email", "users", ["email"])


def downgrade() -> None:
    """Remove email column from users table."""
    op.drop_constraint("uq_users_email", "users", type_="unique")
    op.drop_column("users", "email")
