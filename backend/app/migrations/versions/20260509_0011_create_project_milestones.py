"""create project milestones

Revision ID: 20260509_0011
Revises: 20260509_0010
Create Date: 2026-05-09
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260509_0011"
down_revision: Union[str, None] = "20260509_0010"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "project_milestones",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "project_id",
            sa.Integer(),
            sa.ForeignKey("projects.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("target_date", sa.Date(), nullable=True),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
            server_default="planned",
        ),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint(
            "status IN ('planned', 'active', 'completed', 'canceled')",
            name="ck_project_milestones_status",
        ),
    )
    op.create_index(
        "ix_project_milestones_project_id",
        "project_milestones",
        ["project_id"],
    )
    op.create_index(
        "ix_project_milestones_status",
        "project_milestones",
        ["status"],
    )
    op.create_index(
        "ix_project_milestones_target_date",
        "project_milestones",
        ["target_date"],
    )
    op.create_index(
        "ix_project_milestones_project_order",
        "project_milestones",
        ["project_id", "sort_order", "target_date", "id"],
    )


def downgrade() -> None:
    op.drop_index("ix_project_milestones_project_order", table_name="project_milestones")
    op.drop_index("ix_project_milestones_target_date", table_name="project_milestones")
    op.drop_index("ix_project_milestones_status", table_name="project_milestones")
    op.drop_index("ix_project_milestones_project_id", table_name="project_milestones")
    op.drop_table("project_milestones")
