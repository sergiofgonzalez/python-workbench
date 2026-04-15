"""add created_at col in user_account table.

Revision ID: 965aa2324ea1
Revises: 8b471e5e82ba
Create Date: 2026-04-07 09:16:53.131319

"""

from collections.abc import Sequence

from sqlalchemy import Column, DateTime

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "965aa2324ea1"
down_revision: str | Sequence[str] | None = "8b471e5e82ba"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "user_account",
        Column("created_at", DateTime(), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("user_account", "created_at")
