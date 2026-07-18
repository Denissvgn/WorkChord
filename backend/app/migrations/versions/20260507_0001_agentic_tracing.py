"""add agentic task source and tracing tables

Revision ID: 20260507_0001
Revises: 20260506_0000
Create Date: 2026-05-07
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260507_0001"
down_revision: Union[str, None] = "20260506_0000"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "agent_actors",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=100), nullable=False, unique=True),
        sa.Column("display_name", sa.String(length=255), nullable=False),
        sa.Column("api_key_hash", sa.String(length=128), nullable=False, unique=True),
        sa.Column("scopes", sa.Text(), nullable=False, server_default="[]"),
        # Historical compatibility repair: ``1`` is accepted by SQLite but is
        # not a valid PostgreSQL Boolean default.  Preserve the revision ID and
        # use SQLAlchemy's portable Boolean expression for both dialects.
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(), nullable=True),
    )

    with op.batch_alter_table("tasks") as batch_op:
        batch_op.add_column(sa.Column("external_key", sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column("source", sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column("source_url", sa.String(length=1000), nullable=True))
        batch_op.add_column(sa.Column("version", sa.Integer(), nullable=False, server_default="1"))
        batch_op.add_column(sa.Column("claimed_by", sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column("claim_expires_at", sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()))
        batch_op.create_foreign_key("fk_tasks_claimed_by_agent_actors", "agent_actors", ["claimed_by"], ["id"])

    op.create_index("ix_tasks_external_key", "tasks", ["external_key"])

    op.create_table(
        "task_events",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True),
        sa.Column("actor_type", sa.String(length=50), nullable=False, server_default="user"),
        sa.Column("actor_id", sa.Integer(), sa.ForeignKey("agent_actors.id"), nullable=True),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("payload", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("trace_id", sa.String(length=255), nullable=True),
        sa.Column("span_id", sa.String(length=255), nullable=True),
        sa.Column("correlation_id", sa.String(length=255), nullable=True),
        sa.Column("idempotency_key", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_task_events_task_id", "task_events", ["task_id"])
    op.create_index("ix_task_events_actor_id", "task_events", ["actor_id"])
    op.create_index("ix_task_events_event_type", "task_events", ["event_type"])
    op.create_index("ix_task_events_trace_id", "task_events", ["trace_id"])
    op.create_index("ix_task_events_correlation_id", "task_events", ["correlation_id"])
    op.create_index("ix_task_events_idempotency_key", "task_events", ["idempotency_key"])
    op.create_index("ix_task_events_created_at", "task_events", ["created_at"])

    op.create_table(
        "agent_runs",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True),
        sa.Column("actor_id", sa.Integer(), sa.ForeignKey("agent_actors.id"), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False, server_default="running"),
        sa.Column("trace_id", sa.String(length=255), nullable=True),
        sa.Column("model", sa.String(length=255), nullable=True),
        sa.Column("tool_name", sa.String(length=255), nullable=True),
        sa.Column("run_metadata", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("artifact_links", sa.Text(), nullable=False, server_default="[]"),
        sa.Column("commit_url", sa.String(length=1000), nullable=True),
        sa.Column("pr_url", sa.String(length=1000), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("idempotency_key", sa.String(length=255), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("ended_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_agent_runs_task_id", "agent_runs", ["task_id"])
    op.create_index("ix_agent_runs_actor_id", "agent_runs", ["actor_id"])
    op.create_index("ix_agent_runs_status", "agent_runs", ["status"])
    op.create_index("ix_agent_runs_trace_id", "agent_runs", ["trace_id"])
    op.create_index("ix_agent_runs_idempotency_key", "agent_runs", ["idempotency_key"])
    op.create_index("ix_agent_runs_started_at", "agent_runs", ["started_at"])

    op.create_table(
        "agent_run_events",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("run_id", sa.Integer(), sa.ForeignKey("agent_runs.id", ondelete="CASCADE"), nullable=False),
        sa.Column("event_type", sa.String(length=100), nullable=False),
        sa.Column("message", sa.Text(), nullable=True),
        sa.Column("payload", sa.Text(), nullable=False, server_default="{}"),
        sa.Column("trace_id", sa.String(length=255), nullable=True),
        sa.Column("span_id", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_agent_run_events_run_id", "agent_run_events", ["run_id"])
    op.create_index("ix_agent_run_events_event_type", "agent_run_events", ["event_type"])
    op.create_index("ix_agent_run_events_trace_id", "agent_run_events", ["trace_id"])
    op.create_index("ix_agent_run_events_created_at", "agent_run_events", ["created_at"])


def downgrade() -> None:
    op.drop_index("ix_agent_run_events_created_at", table_name="agent_run_events")
    op.drop_index("ix_agent_run_events_trace_id", table_name="agent_run_events")
    op.drop_index("ix_agent_run_events_event_type", table_name="agent_run_events")
    op.drop_index("ix_agent_run_events_run_id", table_name="agent_run_events")
    op.drop_table("agent_run_events")

    op.drop_index("ix_agent_runs_started_at", table_name="agent_runs")
    op.drop_index("ix_agent_runs_idempotency_key", table_name="agent_runs")
    op.drop_index("ix_agent_runs_trace_id", table_name="agent_runs")
    op.drop_index("ix_agent_runs_status", table_name="agent_runs")
    op.drop_index("ix_agent_runs_actor_id", table_name="agent_runs")
    op.drop_index("ix_agent_runs_task_id", table_name="agent_runs")
    op.drop_table("agent_runs")

    op.drop_index("ix_task_events_created_at", table_name="task_events")
    op.drop_index("ix_task_events_idempotency_key", table_name="task_events")
    op.drop_index("ix_task_events_correlation_id", table_name="task_events")
    op.drop_index("ix_task_events_trace_id", table_name="task_events")
    op.drop_index("ix_task_events_event_type", table_name="task_events")
    op.drop_index("ix_task_events_actor_id", table_name="task_events")
    op.drop_index("ix_task_events_task_id", table_name="task_events")
    op.drop_table("task_events")

    op.drop_index("ix_tasks_external_key", table_name="tasks")
    with op.batch_alter_table("tasks") as batch_op:
        batch_op.drop_constraint("fk_tasks_claimed_by_agent_actors", type_="foreignkey")
        batch_op.drop_column("updated_at")
        batch_op.drop_column("claim_expires_at")
        batch_op.drop_column("claimed_by")
        batch_op.drop_column("version")
        batch_op.drop_column("source_url")
        batch_op.drop_column("source")
        batch_op.drop_column("external_key")

    op.drop_table("agent_actors")
