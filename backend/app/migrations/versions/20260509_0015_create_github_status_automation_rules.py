"""create github status automation rules

Revision ID: 20260509_0015
Revises: 20260509_0014
Create Date: 2026-05-09
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260509_0015"
down_revision: Union[str, None] = "20260509_0014"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "github_status_automation_rules",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("github_event_type", sa.String(length=100), nullable=False),
        sa.Column("from_status", sa.String(length=50), nullable=True),
        sa.Column("target_status", sa.String(length=50), nullable=False),
        sa.Column("reason_template", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default=sa.text("0")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint(
            "github_event_type IN ("
            "'github_pr_opened', 'github_pr_reopened', 'github_pr_ready_for_review', "
            "'github_pr_synchronize', 'github_pr_closed', 'github_pr_merged'"
            ")",
            name="ck_github_status_rules_event_type",
        ),
        sa.CheckConstraint(
            "from_status IS NULL OR from_status IN ('planned', 'active', 'resolved', 'closed')",
            name="ck_github_status_rules_from_status",
        ),
        sa.CheckConstraint(
            "target_status IN ('active', 'resolved', 'closed')",
            name="ck_github_status_rules_target_status",
        ),
    )
    op.create_index(
        "ix_github_status_rules_event_enabled",
        "github_status_automation_rules",
        ["github_event_type", "enabled"],
    )
    op.create_index(
        "ix_github_status_rules_sort",
        "github_status_automation_rules",
        ["sort_order", "id"],
    )


def downgrade() -> None:
    op.drop_index("ix_github_status_rules_sort", table_name="github_status_automation_rules")
    op.drop_index("ix_github_status_rules_event_enabled", table_name="github_status_automation_rules")
    op.drop_table("github_status_automation_rules")
