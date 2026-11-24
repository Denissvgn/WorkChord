"""Retain server-proved execution equivalence across a planning reservation."""

from alembic import op
import sqlalchemy as sa

revision = "20261121_0019"
down_revision = "20261120_0018"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("tasks", sa.Column("execution_planning_window", sa.JSON(none_as_null=True), nullable=True))


def downgrade():
    # This nullable, unindexed column can be dropped natively on both
    # supported engines (SQLite 3.35 or later). Rebuilding the referenced tasks
    # table would endanger assignment and run history on SQLite. Dropping the
    # column discards every live window, so work that relied on one needs PM
    # recovery afterward.
    op.drop_column("tasks", "execution_planning_window")
