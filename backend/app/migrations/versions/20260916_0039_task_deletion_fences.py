"""Retain deletion versions for safe task identity restoration."""

from alembic import op
import sqlalchemy as sa

revision = "20260916_0039"
down_revision = "20260915_0038"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("task_deletion_fences",
        sa.Column("original_task_id", sa.Integer(), primary_key=True, autoincrement=False),
        sa.Column("last_version", sa.Integer(), nullable=False),
        sa.CheckConstraint("last_version >= 1", name="ck_task_deletion_fence_version"))
    # Historic snapshots record observations, not proof of the last deleted version.


def downgrade():
    raise RuntimeError("Deletion fences protect restored identities. Restore a complete backup with its matching application image.")
