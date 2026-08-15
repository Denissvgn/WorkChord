"""Add immutable, revocable plan shares.

Revision ID: 20260802_0036
Revises: 20260728_0035
Create Date: 2026-08-02 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

from app.utils.time import UTCDateTime


revision: str = "20260802_0036"
down_revision: str | None = "20260728_0035"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "plan_shares",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("public_id", sa.String(length=48), nullable=False),
        sa.Column("iteration_id", sa.Integer(), nullable=False),
        sa.Column("created_by_session_id", sa.Integer(), nullable=False),
        sa.Column("snapshot_data", sa.JSON(), nullable=False),
        sa.Column("created_at", UTCDateTime(), nullable=False),
        sa.Column("revoked_at", UTCDateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["created_by_session_id"],
            ["user_sessions.id"],
            ondelete="RESTRICT",
        ),
        sa.ForeignKeyConstraint(
            ["iteration_id"],
            ["iterations.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_plan_shares_public_id",
        "plan_shares",
        ["public_id"],
        unique=True,
    )
    op.create_index(
        "ix_plan_shares_iteration_id",
        "plan_shares",
        ["iteration_id"],
        unique=False,
    )
    op.create_index(
        "ix_plan_shares_created_by_session_id",
        "plan_shares",
        ["created_by_session_id"],
        unique=False,
    )
    op.create_index(
        "ix_plan_shares_created_at",
        "plan_shares",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        "ix_plan_shares_revoked_at",
        "plan_shares",
        ["revoked_at"],
        unique=False,
    )
    op.create_index(
        "ix_plan_shares_iteration_owner_created",
        "plan_shares",
        ["iteration_id", "created_by_session_id", "created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_plan_shares_iteration_owner_created",
        table_name="plan_shares",
    )
    op.drop_index("ix_plan_shares_revoked_at", table_name="plan_shares")
    op.drop_index("ix_plan_shares_created_at", table_name="plan_shares")
    op.drop_index(
        "ix_plan_shares_created_by_session_id",
        table_name="plan_shares",
    )
    op.drop_index("ix_plan_shares_iteration_id", table_name="plan_shares")
    op.drop_index("ix_plan_shares_public_id", table_name="plan_shares")
    op.drop_table("plan_shares")
