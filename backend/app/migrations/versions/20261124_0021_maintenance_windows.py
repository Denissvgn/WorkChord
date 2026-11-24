"""Record coordinated maintenance windows and the receipts that admit them."""

from alembic import op
import sqlalchemy as sa


revision = "20261124_0021"
down_revision = "20261121_0020"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "maintenance_windows",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("state", sa.String(20), nullable=False),
        sa.Column("active_slot", sa.Integer()),
        sa.Column("release_label", sa.String(120), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("planned_start_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("planned_end_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("max_outage_seconds", sa.Integer(), nullable=False),
        sa.Column("expiry_margin_seconds", sa.Integer(), nullable=False),
        sa.Column("announced_by_principal_id", sa.Integer(), sa.ForeignKey("principals.id", ondelete="SET NULL")),
        sa.Column("announced_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True)),
        sa.Column("ended_at", sa.DateTime(timezone=True)),
        sa.Column("outcome", sa.String(20)),
        sa.Column("closing_note", sa.Text()),
        sa.Column("protected_claims", sa.JSON(none_as_null=True)),
        sa.Column("resumption", sa.JSON(none_as_null=True)),
        sa.CheckConstraint(
            "state IN ('announced', 'in_progress', 'completed', 'canceled')",
            name="ck_maintenance_windows_state",
        ),
        sa.CheckConstraint(
            "(state IN ('announced', 'in_progress') AND active_slot = 1)"
            " OR (state IN ('completed', 'canceled') AND active_slot IS NULL)",
            name="ck_maintenance_windows_active_slot",
        ),
        sa.CheckConstraint(
            "outcome IS NULL OR outcome IN ('completed', 'rolled_back', 'canceled')",
            name="ck_maintenance_windows_outcome",
        ),
        sa.CheckConstraint("planned_end_at > planned_start_at", name="ck_maintenance_windows_bounds"),
        sa.CheckConstraint(
            "max_outage_seconds >= 1 AND expiry_margin_seconds >= 60",
            name="ck_maintenance_windows_margins",
        ),
        sa.UniqueConstraint("active_slot", name="uq_maintenance_windows_active_slot"),
    )
    op.create_table(
        "maintenance_window_receipts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "window_id",
            sa.Integer(),
            sa.ForeignKey("maintenance_windows.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("kind", sa.String(30), nullable=False),
        sa.Column("receipt_key", sa.String(120), nullable=False),
        sa.Column(
            "actor_id",
            sa.Integer(),
            sa.ForeignKey("agent_actors.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("source", sa.String(20), nullable=False),
        sa.Column("task_id", sa.Integer()),
        sa.Column("run_id", sa.Integer()),
        sa.Column("assignment_id", sa.Integer()),
        sa.Column("claim_generation", sa.Integer()),
        sa.Column("claim_expires_at", sa.DateTime(timezone=True)),
        sa.Column("channel", sa.String(60)),
        sa.Column("reference", sa.String(500)),
        sa.Column("recorded_by_principal_id", sa.Integer(), sa.ForeignKey("principals.id", ondelete="SET NULL")),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "kind IN ('owner_acknowledgement', 'pm_notice')",
            name="ck_maintenance_window_receipts_kind",
        ),
        sa.CheckConstraint(
            "source IN ('agent', 'operator')",
            name="ck_maintenance_window_receipts_source",
        ),
        sa.CheckConstraint(
            "kind = 'pm_notice' OR source = 'agent'",
            name="ck_maintenance_window_receipts_owner_consent",
        ),
        sa.UniqueConstraint("window_id", "receipt_key", name="uq_maintenance_window_receipts_key"),
    )
    op.create_index(
        "ix_maintenance_window_receipts_window_id", "maintenance_window_receipts", ["window_id"]
    )
    op.create_index(
        "ix_maintenance_window_receipts_actor_id", "maintenance_window_receipts", ["actor_id"]
    )


def downgrade() -> None:
    # An older server has no admission check, so it must not inherit an open
    # window it would silently ignore.
    connection = op.get_bind()
    windows = sa.table("maintenance_windows", sa.column("state", sa.String()))
    if connection.scalar(
        sa.select(sa.literal(1)).select_from(windows)
        .where(windows.c.state.in_(("announced", "in_progress"))).limit(1)
    ):
        raise RuntimeError("Close or cancel the open maintenance window before downgrading.")
    op.drop_index("ix_maintenance_window_receipts_actor_id", table_name="maintenance_window_receipts")
    op.drop_index("ix_maintenance_window_receipts_window_id", table_name="maintenance_window_receipts")
    op.drop_table("maintenance_window_receipts")
    op.drop_table("maintenance_windows")
