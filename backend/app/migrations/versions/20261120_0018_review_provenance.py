"""Preserve execution provenance and project review selection."""

from alembic import op
import sqlalchemy as sa

revision = "20261120_0018"
down_revision = "20261116_0017"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("projects", sa.Column("require_different_review_publisher", sa.Boolean(), nullable=False, server_default=sa.false()))
    op.add_column("agent_model_catalog_entries", sa.Column("publisher_key", sa.String(120)))
    op.add_column("agent_task_assignments", sa.Column("review_selection", sa.JSON(none_as_null=True)))
    op.add_column("agent_runs", sa.Column("execution_provenance", sa.JSON(none_as_null=True)))


def downgrade():
    for table, column in (
        ("agent_runs", "execution_provenance"),
        ("agent_task_assignments", "review_selection"),
        ("agent_model_catalog_entries", "publisher_key"),
        ("projects", "require_different_review_publisher"),
    ):
        with op.batch_alter_table(table) as batch:
            batch.drop_column(column)
