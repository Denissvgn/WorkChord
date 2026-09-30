"""Persist delivery dependencies separately from local schedule edges."""

from alembic import op
import sqlalchemy as sa

revision = "20260930_0003"
down_revision = "20260930_0002"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("delivery_dependencies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False),
        sa.Column("prerequisite_task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="RESTRICT")),
        sa.Column("prerequisite_milestone_id", sa.Integer(), sa.ForeignKey("project_milestones.id", ondelete="RESTRICT")),
        sa.CheckConstraint("(prerequisite_task_id IS NULL) <> (prerequisite_milestone_id IS NULL)", name="ck_delivery_dependency_target"),
        sa.CheckConstraint("task_id <> prerequisite_task_id", name="ck_delivery_dependency_self"),
        sa.UniqueConstraint("task_id", "prerequisite_task_id", name="uq_delivery_task_target"),
        sa.UniqueConstraint("task_id", "prerequisite_milestone_id", name="uq_delivery_milestone_target"))
    for column in ("task_id", "prerequisite_task_id", "prerequisite_milestone_id"):
        op.create_index(f"ix_delivery_dependencies_{column}", "delivery_dependencies", [column])


def downgrade():
    raise RuntimeError("Delivery dependencies cannot be downgraded; restore a verified backup.")
