"""Create request sources.

Revision ID: 20260509_0017
Revises: 20260509_0016
Create Date: 2026-05-09 00:17:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260509_0017"
down_revision: str | None = "20260509_0016"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "request_sources",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("source_type", sa.String(length=50), nullable=False),
        sa.Column("source_name", sa.String(length=255), nullable=True),
        sa.Column("source_url", sa.String(length=1000), nullable=True),
        sa.Column("external_key", sa.String(length=255), nullable=True),
        sa.Column("priority_hint", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint(
            "source_type IN ('customer', 'internal', 'support', 'email', 'web', 'import')",
            name="ck_request_sources_source_type",
        ),
        sa.CheckConstraint(
            "priority_hint IS NULL OR (priority_hint >= 1 AND priority_hint <= 10)",
            name="ck_request_sources_priority_hint_range",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_request_sources_source_type", "request_sources", ["source_type"])
    op.create_index("ix_request_sources_external_key", "request_sources", ["external_key"])
    op.create_index("ix_request_sources_source_url", "request_sources", ["source_url"])
    op.create_index("ix_request_sources_created_at", "request_sources", ["created_at"])

    op.create_table(
        "request_source_links",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("request_source_id", sa.Integer(), nullable=False),
        sa.Column("triage_item_id", sa.Integer(), nullable=True),
        sa.Column("task_id", sa.Integer(), nullable=True),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint(
            "("
            "CASE WHEN triage_item_id IS NOT NULL THEN 1 ELSE 0 END + "
            "CASE WHEN task_id IS NOT NULL THEN 1 ELSE 0 END + "
            "CASE WHEN project_id IS NOT NULL THEN 1 ELSE 0 END"
            ") = 1",
            name="ck_request_source_links_exactly_one_target",
        ),
        sa.ForeignKeyConstraint(
            ["project_id"],
            ["projects.id"],
            name="fk_request_source_links_project_id",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["request_source_id"],
            ["request_sources.id"],
            name="fk_request_source_links_request_source_id",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["task_id"],
            ["tasks.id"],
            name="fk_request_source_links_task_id",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["triage_item_id"],
            ["triage_items.id"],
            name="fk_request_source_links_triage_item_id",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "request_source_id",
            "triage_item_id",
            name="uq_request_source_links_source_triage_item",
        ),
        sa.UniqueConstraint(
            "request_source_id",
            "task_id",
            name="uq_request_source_links_source_task",
        ),
        sa.UniqueConstraint(
            "request_source_id",
            "project_id",
            name="uq_request_source_links_source_project",
        ),
    )
    op.create_index(
        "ix_request_source_links_request_source_id",
        "request_source_links",
        ["request_source_id"],
    )
    op.create_index(
        "ix_request_source_links_triage_item_id",
        "request_source_links",
        ["triage_item_id"],
    )
    op.create_index("ix_request_source_links_task_id", "request_source_links", ["task_id"])
    op.create_index(
        "ix_request_source_links_project_id",
        "request_source_links",
        ["project_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_request_source_links_project_id", table_name="request_source_links")
    op.drop_index("ix_request_source_links_task_id", table_name="request_source_links")
    op.drop_index("ix_request_source_links_triage_item_id", table_name="request_source_links")
    op.drop_index(
        "ix_request_source_links_request_source_id",
        table_name="request_source_links",
    )
    op.drop_table("request_source_links")
    op.drop_index("ix_request_sources_created_at", table_name="request_sources")
    op.drop_index("ix_request_sources_source_url", table_name="request_sources")
    op.drop_index("ix_request_sources_external_key", table_name="request_sources")
    op.drop_index("ix_request_sources_source_type", table_name="request_sources")
    op.drop_table("request_sources")
