"""Keep the reviewed task revision alongside the revision produced by the verdict."""

from alembic import op
import sqlalchemy as sa


revision = "20261128_0034"
down_revision = "20261127_0033"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("task_review_records", sa.Column("reviewed_task_version", sa.Integer(), nullable=True))


def downgrade() -> None:
    table = sa.table("task_review_records", sa.column("reviewed_task_version"))
    retained = sa.select(table.c.reviewed_task_version).where(table.c.reviewed_task_version.is_not(None)).limit(1)
    if op.get_bind().scalar(retained) is not None:
        raise RuntimeError("Downgrading would discard recorded review revisions.")
    op.drop_column("task_review_records", "reviewed_task_version")
