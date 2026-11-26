"""Record which runtime instance acknowledged each team member's handoff."""

from alembic import op
import sqlalchemy as sa


revision = "20261126_0025"
down_revision = "20261124_0024"
branch_labels = None
depends_on = None

TABLE = "agent_team_topology_members"


def upgrade() -> None:
    # Members acknowledged before this change keep every column empty: their identity reads as unknown.
    op.add_column(TABLE, sa.Column("acknowledged_runtime_instance_id", sa.String(64), nullable=True))
    op.add_column(TABLE, sa.Column("previous_runtime_instance_id", sa.String(64), nullable=True))
    op.add_column(TABLE, sa.Column("runtime_identity_changed_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column(TABLE, sa.Column("rejected_runtime_instance_id", sa.String(64), nullable=True))
    op.add_column(TABLE, sa.Column("rejected_runtime_instance_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    # An older server cannot read an acknowledgement that carries an identity, and the history would be lost.
    connection = op.get_bind()
    table = sa.table(TABLE, sa.column("acknowledged_runtime_instance_id"), sa.column("previous_runtime_instance_id"))
    if connection.scalar(
        sa.select(sa.literal(1))
        .select_from(table)
        .where(
            sa.or_(
                table.c.acknowledged_runtime_instance_id.is_not(None),
                table.c.previous_runtime_instance_id.is_not(None),
            )
        )
        .limit(1)
    ):
        raise RuntimeError("Runtime instance identities are recorded; clear them before downgrading.")
    for column in (
        "rejected_runtime_instance_at",
        "rejected_runtime_instance_id",
        "runtime_identity_changed_at",
        "previous_runtime_instance_id",
        "acknowledged_runtime_instance_id",
    ):
        op.drop_column(TABLE, column)
