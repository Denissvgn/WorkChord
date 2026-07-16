"""Add metadata JSON to triage items.

Revision ID: 20260509_0020
Revises: 20260509_0019
Create Date: 2026-05-09 00:20:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260509_0020"
down_revision: str | None = "20260509_0019"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "triage_items",
        sa.Column(
            "metadata_json",
            sa.JSON(),
            nullable=False,
            server_default=sa.text("'{}'"),
        ),
    )


def downgrade() -> None:
    op.drop_column("triage_items", "metadata_json")
