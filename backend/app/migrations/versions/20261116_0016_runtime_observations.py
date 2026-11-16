"""Retain advisory observations of agent runtime sessions."""

from alembic import op
import sqlalchemy as sa


revision = "20261116_0016"
down_revision = "20261116_0015"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "agent_runtime_observations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="SET NULL")),
        sa.Column("run_id", sa.Integer(), sa.ForeignKey("agent_runs.id", ondelete="SET NULL")),
        sa.Column("subject_actor_id", sa.Integer(), sa.ForeignKey("agent_actors.id", ondelete="SET NULL")),
        sa.Column("observer_session_id", sa.Integer(), sa.ForeignKey("user_sessions.id", ondelete="SET NULL")),
        sa.Column("observer_principal_id", sa.Integer(), sa.ForeignKey("principals.id", ondelete="SET NULL")),
        sa.Column("observer_label", sa.String(80)),
        sa.Column("kind", sa.String(30), nullable=False),
        sa.Column("harness_kind", sa.String(40), nullable=False),
        sa.Column("harness_session_id", sa.String(255), nullable=False),
        sa.Column("observed_model", sa.String(255)),
        sa.Column("idempotency_key", sa.String(128), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("received_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "kind IN ('session_active', 'session_idle', 'session_ended', 'model_observed')",
            name="ck_agent_runtime_observations_kind",
        ),
        sa.UniqueConstraint("observer_session_id", "idempotency_key", name="uq_agent_runtime_observation_key"),
    )
    op.create_index("ix_agent_runtime_observations_task_id", "agent_runtime_observations", ["task_id"])
    op.create_index("ix_agent_runtime_observations_run_id", "agent_runtime_observations", ["run_id"])
    op.create_index("ix_agent_runtime_observations_observer_time", "agent_runtime_observations",
                    ["observer_session_id", "received_at"])
    op.create_index("ix_agent_runtime_observations_harness", "agent_runtime_observations",
                    ["harness_kind", "harness_session_id"])


def downgrade():
    raise RuntimeError("Runtime observations cannot be downgraded; restore the matching verified backup")
