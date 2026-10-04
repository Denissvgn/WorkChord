"""Retain execution usage revisions and immutable pricing snapshots."""

from alembic import op
import sqlalchemy as sa

revision = "20261004_0007"
down_revision = "20261004_0006"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("execution_usage_records",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("run_id", sa.Integer(), sa.ForeignKey("agent_runs.id", ondelete="SET NULL")),
        sa.Column("original_run_id", sa.Integer(), nullable=False), sa.Column("run_identity", sa.String(64), nullable=False),
        sa.Column("original_task_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id", ondelete="SET NULL")),
        sa.Column("iteration_id", sa.Integer(), sa.ForeignKey("iterations.id", ondelete="SET NULL")),
        sa.Column("original_project_id", sa.Integer()), sa.Column("original_iteration_id", sa.Integer()),
        sa.Column("reporter_actor_id", sa.Integer(), sa.ForeignKey("agent_actors.id", ondelete="SET NULL")),
        sa.Column("report_id", sa.String(128), nullable=False), sa.Column("sequence", sa.Integer(), nullable=False),
        sa.Column("digest", sa.String(64), nullable=False), sa.Column("previous_digest", sa.String(64)),
        sa.Column("payload", sa.JSON(), nullable=False), sa.Column("reported_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("run_identity", "report_id", name="uq_execution_usage_report"),
        sa.UniqueConstraint("run_identity", "sequence", name="uq_execution_usage_sequence"))
    for column in ("run_id", "original_run_id", "original_task_id"):
        op.create_index(f"ix_execution_usage_records_{column}", "execution_usage_records", [column])
    op.create_index("ix_execution_usage_scope_time", "execution_usage_records", ["project_id", "iteration_id", "reported_at"])


def downgrade():
    raise RuntimeError("Usage and pricing evidence are immutable history; restore an authorized full backup for rollback")
