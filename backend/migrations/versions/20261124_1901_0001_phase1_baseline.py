"""Phase 1 baseline migration.

Revision ID: 0001_phase1
Revises:
Create Date: 2026-11-24
"""

from alembic import op

revision = "0001_phase1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("SELECT 1")


def downgrade() -> None:
    op.execute("SELECT 1")
