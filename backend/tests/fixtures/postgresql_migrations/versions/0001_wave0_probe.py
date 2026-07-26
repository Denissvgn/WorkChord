"""Create the Wave 0 PostgreSQL lifecycle probe.

Revision ID: 0001_wave0_probe
Revises: None
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "0001_wave0_probe"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "wave0_database_probe",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("value", sa.String(length=100), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("wave0_database_probe")

