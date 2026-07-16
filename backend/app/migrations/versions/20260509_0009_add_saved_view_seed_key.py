"""add saved view seed key

Revision ID: 20260509_0009
Revises: 20260509_0008
Create Date: 2026-05-09
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260509_0009"
down_revision: Union[str, None] = "20260509_0008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "saved_views",
        sa.Column("seed_key", sa.String(length=100), nullable=True),
    )
    op.create_index(
        "ix_saved_views_seed_key",
        "saved_views",
        ["seed_key"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_saved_views_seed_key", table_name="saved_views")
    op.drop_column("saved_views", "seed_key")
