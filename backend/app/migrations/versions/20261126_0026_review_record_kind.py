"""Tell an owner's override acceptance apart from an ordinary review in review history."""

from alembic import op
import sqlalchemy as sa


revision = "20261126_0026"
down_revision = "20261126_0025"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("task_review_records",
                  sa.Column("kind", sa.String(32), nullable=False, server_default="review"))


def downgrade() -> None:
    # An older server would present an owner override as an ordinary review.
    connection = op.get_bind()
    table = sa.table("task_review_records", sa.column("kind"))
    if connection.scalar(sa.select(sa.literal(1)).select_from(table).where(table.c.kind != "review").limit(1)):
        raise RuntimeError("Owner override acceptances exist in review history; they cannot be downgraded without losing their kind.")
    op.drop_column("task_review_records", "kind")
