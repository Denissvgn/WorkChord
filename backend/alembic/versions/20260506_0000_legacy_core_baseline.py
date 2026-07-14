"""Baseline for pre-backlog core planning schema.

Revision ID: 20260506_0000
Revises: None
Create Date: 2026-05-06
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260506_0000"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "calendars",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("holidays", sa.JSON(), nullable=True),
        sa.Column("weekend_days", sa.JSON(), nullable=True),
        sa.Column("short_days", sa.JSON(), nullable=True),
    )

    op.create_table(
        "iterations",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("manager_email", sa.String(length=255), nullable=True),
        sa.Column("calendar_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["calendar_id"], ["calendars.id"]),
    )

    op.create_table(
        "team_members",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("position", sa.String(length=255), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("availability_percent", sa.Float(), nullable=True),
        sa.Column("professionalism_coefficient", sa.Float(), nullable=True),
        sa.Column("operational_utilization", sa.Float(), nullable=True),
        sa.Column("iteration_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["iteration_id"],
            ["iterations.id"],
            ondelete="SET NULL",
        ),
    )

    op.create_table(
        "vacations",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("team_member_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["team_member_id"], ["team_members.id"]),
    )

    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("priority", sa.Integer(), nullable=True),
        sa.Column("effort_days", sa.Float(), nullable=True),
        sa.Column("effort_hours", sa.Float(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("actual_start_date", sa.Date(), nullable=True),
        sa.Column("actual_end_date", sa.Date(), nullable=True),
        sa.Column("calculated_effort_days", sa.Float(), nullable=True),
        sa.Column("min_start_date", sa.Date(), nullable=True),
        sa.Column("max_end_date", sa.Date(), nullable=True),
        sa.Column("is_optional", sa.Boolean(), nullable=True),
        sa.Column("is_deferred", sa.Boolean(), nullable=True),
        sa.Column("tags", sa.String(length=1000), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=True),
        sa.Column("iteration_id", sa.Integer(), nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("assignee_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["iteration_id"], ["iterations.id"]),
        sa.ForeignKeyConstraint(["parent_id"], ["tasks.id"]),
        sa.ForeignKeyConstraint(["assignee_id"], ["team_members.id"]),
    )
    op.create_index("ix_tasks_iteration_id", "tasks", ["iteration_id"])
    op.create_index("ix_tasks_parent_id", "tasks", ["parent_id"])
    op.create_index("ix_tasks_assignee_id", "tasks", ["assignee_id"])

    op.create_table(
        "task_dependencies",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("depends_on_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["task_id"], ["tasks.id"]),
        sa.ForeignKeyConstraint(["depends_on_id"], ["tasks.id"]),
    )
    op.create_index("ix_task_dependencies_task_id", "task_dependencies", ["task_id"])
    op.create_index(
        "ix_task_dependencies_depends_on_id",
        "task_dependencies",
        ["depends_on_id"],
    )

    op.create_table(
        "task_status_logs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("from_status", sa.String(length=50), nullable=False),
        sa.Column("to_status", sa.String(length=50), nullable=False),
        sa.Column("changed_at", sa.DateTime(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("triggered_by", sa.String(length=50), nullable=False),
        sa.Column("affected_task_ids", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["task_id"], ["tasks.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_task_status_logs_task_id", "task_status_logs", ["task_id"])
    op.create_index("ix_task_status_logs_changed_at", "task_status_logs", ["changed_at"])


def downgrade() -> None:
    op.drop_index("ix_task_status_logs_changed_at", table_name="task_status_logs")
    op.drop_index("ix_task_status_logs_task_id", table_name="task_status_logs")
    op.drop_table("task_status_logs")
    op.drop_index("ix_task_dependencies_depends_on_id", table_name="task_dependencies")
    op.drop_index("ix_task_dependencies_task_id", table_name="task_dependencies")
    op.drop_table("task_dependencies")
    op.drop_index("ix_tasks_assignee_id", table_name="tasks")
    op.drop_index("ix_tasks_parent_id", table_name="tasks")
    op.drop_index("ix_tasks_iteration_id", table_name="tasks")
    op.drop_table("tasks")
    op.drop_table("vacations")
    op.drop_table("team_members")
    op.drop_table("iterations")
    op.drop_table("calendars")
