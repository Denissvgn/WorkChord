"""Record the reasoning-effort setting of each model catalog entry."""

from alembic import op
import sqlalchemy as sa


revision = "20261126_0029"
down_revision = "20261126_0028"
branch_labels = None
depends_on = None

EFFORT_CHECK = "effort IN ('unknown', 'low', 'medium', 'high', 'xhigh', 'max')"


def upgrade() -> None:
    # Existing entries receive the explicit unknown value through the server
    # default; nothing is guessed from an entry's key or alias.
    with op.batch_alter_table("agent_model_catalog_entries") as batch:
        batch.add_column(
            sa.Column("effort", sa.String(20), nullable=False, server_default="unknown")
        )
        batch.create_check_constraint("ck_agent_model_catalog_effort", EFFORT_CHECK)


def downgrade() -> None:
    # An older server cannot read the setting, so dropping it would silently
    # merge entries that differ only by effort.
    connection = op.get_bind()
    table = sa.table("agent_model_catalog_entries", sa.column("effort"))
    if connection.scalar(
        sa.select(sa.literal(1)).select_from(table).where(table.c.effort != "unknown").limit(1)
    ):
        raise RuntimeError(
            "Catalog entries record an effort setting; set them to unknown before downgrading."
        )
    with op.batch_alter_table("agent_model_catalog_entries") as batch:
        batch.drop_constraint("ck_agent_model_catalog_effort", type_="check")
        batch.drop_column("effort")
