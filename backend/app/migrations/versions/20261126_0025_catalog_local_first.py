"""Let a model catalog entry prefer a free or local model at equal adequacy."""

from alembic import op
import sqlalchemy as sa


revision = "20261126_0025"
down_revision = "20261124_0024"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "agent_model_catalog_entries",
        sa.Column("local_first", sa.Boolean(), nullable=False, server_default=sa.false()),
    )


def downgrade() -> None:
    with op.batch_alter_table("agent_model_catalog_entries") as batch:
        batch.drop_column("local_first")
