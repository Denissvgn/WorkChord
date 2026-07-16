"""create project updates

Revision ID: 20260509_0010
Revises: 20260509_0009
Create Date: 2026-05-09
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260509_0010"
down_revision: Union[str, None] = "20260509_0009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "project_updates",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "project_id",
            sa.Integer(),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("health", sa.String(length=50), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("progress_text", sa.Text(), nullable=True),
        sa.Column("risks_text", sa.Text(), nullable=True),
        sa.Column("decisions_text", sa.Text(), nullable=True),
        sa.Column("next_steps_text", sa.Text(), nullable=True),
        sa.Column(
            "created_by_session_id",
            sa.Integer(),
            sa.ForeignKey("user_sessions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint(
            "health IN ('unknown', 'on_track', 'at_risk', 'off_track')",
            name="ck_project_updates_health",
        ),
    )
    op.create_index("ix_project_updates_project_id", "project_updates", ["project_id"])
    op.create_index("ix_project_updates_health", "project_updates", ["health"])
    op.create_index(
        "ix_project_updates_created_by_session_id",
        "project_updates",
        ["created_by_session_id"],
    )
    op.create_index("ix_project_updates_created_at", "project_updates", ["created_at"])
    op.create_index(
        "ix_project_updates_project_created",
        "project_updates",
        ["project_id", "created_at", "id"],
    )


def downgrade() -> None:
    op.drop_index("ix_project_updates_project_created", table_name="project_updates")
    op.drop_index("ix_project_updates_created_at", table_name="project_updates")
    op.drop_index(
        "ix_project_updates_created_by_session_id",
        table_name="project_updates",
    )
    op.drop_index("ix_project_updates_health", table_name="project_updates")
    op.drop_index("ix_project_updates_project_id", table_name="project_updates")
    op.drop_table("project_updates")
