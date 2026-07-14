"""create triage items table

Revision ID: 20260508_0004
Revises: 20260507_0003
Create Date: 2026-05-08
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260508_0004"
down_revision: Union[str, None] = "20260507_0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "triage_items",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("source", sa.String(length=100), nullable=True),
        sa.Column("source_url", sa.String(length=1000), nullable=True),
        sa.Column("external_key", sa.String(length=255), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="new"),
        sa.Column("priority_hint", sa.Integer(), nullable=True),
        sa.Column("assignee_hint", sa.String(length=255), nullable=True),
        sa.Column("labels", sa.JSON(), nullable=False, server_default=sa.text("'[]'")),
        sa.Column("snoozed_until", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column(
            "project_hint_id",
            sa.Integer(),
            sa.ForeignKey("projects.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "iteration_hint_id",
            sa.Integer(),
            sa.ForeignKey("iterations.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "duplicate_of_id",
            sa.Integer(),
            sa.ForeignKey("triage_items.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "duplicate_task_id",
            sa.Integer(),
            sa.ForeignKey("tasks.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column(
            "converted_task_id",
            sa.Integer(),
            sa.ForeignKey("tasks.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.CheckConstraint(
            "duplicate_of_id IS NULL OR duplicate_task_id IS NULL",
            name="ck_triage_items_one_duplicate_target",
        ),
        sa.CheckConstraint(
            "priority_hint IS NULL OR (priority_hint >= 1 AND priority_hint <= 10)",
            name="ck_triage_items_priority_hint_range",
        ),
    )
    op.create_index("ix_triage_items_status", "triage_items", ["status"])
    op.create_index("ix_triage_items_external_key", "triage_items", ["external_key"])
    op.create_index("ix_triage_items_project_hint_id", "triage_items", ["project_hint_id"])
    op.create_index("ix_triage_items_iteration_hint_id", "triage_items", ["iteration_hint_id"])
    op.create_index("ix_triage_items_snoozed_until", "triage_items", ["snoozed_until"])
    op.create_index("ix_triage_items_duplicate_of_id", "triage_items", ["duplicate_of_id"])
    op.create_index("ix_triage_items_duplicate_task_id", "triage_items", ["duplicate_task_id"])
    op.create_index("ix_triage_items_converted_task_id", "triage_items", ["converted_task_id"])
    op.create_index("ix_triage_items_created_at", "triage_items", ["created_at"])
    op.create_index("ix_triage_items_updated_at", "triage_items", ["updated_at"])


def downgrade() -> None:
    op.drop_index("ix_triage_items_updated_at", table_name="triage_items")
    op.drop_index("ix_triage_items_created_at", table_name="triage_items")
    op.drop_index("ix_triage_items_converted_task_id", table_name="triage_items")
    op.drop_index("ix_triage_items_duplicate_task_id", table_name="triage_items")
    op.drop_index("ix_triage_items_duplicate_of_id", table_name="triage_items")
    op.drop_index("ix_triage_items_snoozed_until", table_name="triage_items")
    op.drop_index("ix_triage_items_iteration_hint_id", table_name="triage_items")
    op.drop_index("ix_triage_items_project_hint_id", table_name="triage_items")
    op.drop_index("ix_triage_items_external_key", table_name="triage_items")
    op.drop_index("ix_triage_items_status", table_name="triage_items")
    op.drop_table("triage_items")
