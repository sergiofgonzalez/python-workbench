"""create user_account table.

Revision ID: 8b471e5e82ba
Revises:
Create Date: 2026-04-07 08:46:31.652919

"""

from collections.abc import Sequence

from sqlalchemy import Column, Integer, String

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8b471e5e82ba"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "user_account",
        Column("id", Integer, primary_key=True),
        Column("name", String(30), nullable=False, unique=True),
        Column("fullname", String(120), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("user_account")
