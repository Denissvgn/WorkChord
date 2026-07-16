"""add work template seed key

Revision ID: 20260508_0006
Revises: 20260508_0005
Create Date: 2026-05-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260508_0006"
down_revision: Union[str, None] = "20260508_0005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "work_templates",
        sa.Column("seed_key", sa.String(length=100), nullable=True),
    )
    op.create_index(
        "ix_work_templates_seed_key",
        "work_templates",
        ["seed_key"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_work_templates_seed_key", table_name="work_templates")
    op.drop_column("work_templates", "seed_key")
