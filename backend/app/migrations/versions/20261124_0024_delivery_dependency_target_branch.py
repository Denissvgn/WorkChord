"""Let a delivery prerequisite require accepted code merged on a named branch."""

from alembic import op
import sqlalchemy as sa


revision = "20261124_0024"
down_revision = "20261124_0023"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("delivery_dependencies", sa.Column("target_branch", sa.String(255), nullable=True))


def downgrade() -> None:
    # An older server would treat an accepted but unmerged prerequisite as ready.
    connection = op.get_bind()
    table = sa.table("delivery_dependencies", sa.column("target_branch"))
    if connection.scalar(sa.select(sa.literal(1)).select_from(table).where(table.c.target_branch.is_not(None)).limit(1)):
        raise RuntimeError("Delivery prerequisites with a target branch exist; remove them before downgrading.")
    op.drop_column("delivery_dependencies", "target_branch")
