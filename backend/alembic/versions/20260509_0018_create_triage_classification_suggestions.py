"""Create triage classification suggestions.

Revision ID: 20260509_0018
Revises: 20260509_0017
Create Date: 2026-05-09 00:18:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260509_0018"
down_revision: str | None = "20260509_0017"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "triage_classification_suggestions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("triage_item_id", sa.Integer(), nullable=False),
        sa.Column("suggested_type_label_slug", sa.String(length=100), nullable=True),
        sa.Column("suggested_area_label_slug", sa.String(length=100), nullable=True),
        sa.Column("suggested_priority", sa.Integer(), nullable=True),
        sa.Column(
            "suggested_label_slugs",
            sa.JSON(),
            server_default=sa.text("'[]'"),
            nullable=False,
        ),
        sa.Column(
            "unmatched_label_text",
            sa.JSON(),
            server_default=sa.text("'[]'"),
            nullable=False,
        ),
        sa.Column("suggested_assignee_id", sa.Integer(), nullable=True),
        sa.Column("suggested_assignee_hint", sa.String(length=255), nullable=True),
        sa.Column("suggested_project_id", sa.Integer(), nullable=True),
        sa.Column(
            "duplicate_candidates",
            sa.JSON(),
            server_default=sa.text("'[]'"),
            nullable=False,
        ),
        sa.Column("confidence", sa.Float(), server_default="0", nullable=False),
        sa.Column("rationale", sa.Text(), nullable=True),
        sa.Column("provider", sa.String(length=100), nullable=True),
        sa.Column("model", sa.String(length=255), nullable=True),
        sa.Column("is_fallback", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column(
            "raw_response_json",
            sa.JSON(),
            server_default=sa.text("'{}'"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint(
            "suggested_priority IS NULL OR "
            "(suggested_priority >= 1 AND suggested_priority <= 10)",
            name="ck_triage_classification_suggestions_priority_range",
        ),
        sa.CheckConstraint(
            "confidence >= 0 AND confidence <= 1",
            name="ck_triage_classification_suggestions_confidence_range",
        ),
        sa.ForeignKeyConstraint(
            ["suggested_assignee_id"],
            ["team_members.id"],
            name="fk_triage_classification_suggestions_assignee_id",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["suggested_project_id"],
            ["projects.id"],
            name="fk_triage_classification_suggestions_project_id",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["triage_item_id"],
            ["triage_items.id"],
            name="fk_triage_classification_suggestions_triage_item_id",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_triage_classification_suggestions_triage_item_id",
        "triage_classification_suggestions",
        ["triage_item_id"],
    )
    op.create_index(
        "ix_triage_classification_suggestions_suggested_assignee_id",
        "triage_classification_suggestions",
        ["suggested_assignee_id"],
    )
    op.create_index(
        "ix_triage_classification_suggestions_suggested_project_id",
        "triage_classification_suggestions",
        ["suggested_project_id"],
    )
    op.create_index(
        "ix_triage_classification_suggestions_is_fallback",
        "triage_classification_suggestions",
        ["is_fallback"],
    )
    op.create_index(
        "ix_triage_classification_suggestions_created_at",
        "triage_classification_suggestions",
        ["created_at"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_triage_classification_suggestions_created_at",
        table_name="triage_classification_suggestions",
    )
    op.drop_index(
        "ix_triage_classification_suggestions_is_fallback",
        table_name="triage_classification_suggestions",
    )
    op.drop_index(
        "ix_triage_classification_suggestions_suggested_project_id",
        table_name="triage_classification_suggestions",
    )
    op.drop_index(
        "ix_triage_classification_suggestions_suggested_assignee_id",
        table_name="triage_classification_suggestions",
    )
    op.drop_index(
        "ix_triage_classification_suggestions_triage_item_id",
        table_name="triage_classification_suggestions",
    )
    op.drop_table("triage_classification_suggestions")
