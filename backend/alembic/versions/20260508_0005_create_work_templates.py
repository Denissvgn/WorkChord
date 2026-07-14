"""create work templates table

Revision ID: 20260508_0005
Revises: 20260508_0004
Create Date: 2026-05-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260508_0005"
down_revision: Union[str, None] = "20260508_0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "work_templates",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("template_type", sa.String(length=50), nullable=False),
        sa.Column("default_title", sa.String(length=500), nullable=True),
        sa.Column("default_description", sa.Text(), nullable=True),
        sa.Column("default_priority", sa.Integer(), nullable=True),
        sa.Column("default_effort_days", sa.Float(), nullable=True),
        sa.Column("default_labels", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column("default_checklist", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column("default_payload", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint(
            "template_type IN ('task', 'project', 'triage')",
            name="ck_work_templates_template_type",
        ),
        sa.CheckConstraint(
            "default_priority IS NULL OR (default_priority >= 1 AND default_priority <= 10)",
            name="ck_work_templates_default_priority_range",
        ),
        sa.CheckConstraint(
            "default_effort_days IS NULL OR default_effort_days >= 0.1",
            name="ck_work_templates_default_effort_days_min",
        ),
    )
    op.create_index("ix_work_templates_template_type", "work_templates", ["template_type"])
    op.create_index("ix_work_templates_is_active", "work_templates", ["is_active"])
    op.create_index("ix_work_templates_sort_order", "work_templates", ["sort_order"])
    op.create_index("ix_work_templates_created_at", "work_templates", ["created_at"])
    op.create_index("ix_work_templates_updated_at", "work_templates", ["updated_at"])
    op.create_index(
        "ix_work_templates_type_active_order",
        "work_templates",
        ["template_type", "is_active", "sort_order"],
    )


def downgrade() -> None:
    op.drop_index("ix_work_templates_type_active_order", table_name="work_templates")
    op.drop_index("ix_work_templates_updated_at", table_name="work_templates")
    op.drop_index("ix_work_templates_created_at", table_name="work_templates")
    op.drop_index("ix_work_templates_sort_order", table_name="work_templates")
    op.drop_index("ix_work_templates_is_active", table_name="work_templates")
    op.drop_index("ix_work_templates_template_type", table_name="work_templates")
    op.drop_table("work_templates")
