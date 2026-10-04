"""Retain event-time delivery observations without guessing older history."""

from alembic import op
import sqlalchemy as sa

revision = "20261004_0006"
down_revision = "20261003_0005"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("delivery_observations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("original_task_id", sa.Integer(), nullable=False),
        sa.Column("task_version", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id", ondelete="SET NULL")),
        sa.Column("iteration_id", sa.Integer(), sa.ForeignKey("iterations.id", ondelete="SET NULL")),
        sa.Column("original_project_id", sa.Integer()), sa.Column("original_iteration_id", sa.Integer()),
        sa.Column("kind", sa.String(32), nullable=False), sa.Column("source", sa.String(32), nullable=False),
        sa.Column("observed_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("original_task_id", "task_version", "kind", name="uq_delivery_observation_fact"),
        sa.CheckConstraint("task_version >= 1", name="ck_delivery_observation_version"))
    op.create_index("ix_delivery_observations_original_task_id", "delivery_observations", ["original_task_id"])
    op.create_index("ix_delivery_observations_scope_time", "delivery_observations", ["project_id", "iteration_id", "observed_at"])


def downgrade():
    raise RuntimeError("Delivery observations are immutable history; restore an authorized full backup for rollback")
