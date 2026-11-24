"""Record dated availability adjustments on iteration capacity rows."""

from alembic import op
import sqlalchemy as sa

revision = "20261124_0022"
down_revision = "20261124_0021"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "team_member_capacity_adjustments",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "team_member_id",
            sa.Integer(),
            sa.ForeignKey("team_members.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("availability_percent", sa.Float(), nullable=False),
        sa.Column("base_availability_percent", sa.Float(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("group_token", sa.String(36), nullable=False),
        sa.Column(
            "created_by_principal_id",
            sa.Integer(),
            sa.ForeignKey("principals.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("withdrawn_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "withdrawn_by_principal_id",
            sa.Integer(),
            sa.ForeignKey("principals.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("withdrawal_reason", sa.Text(), nullable=True),
        sa.Column("withdrawn_group_token", sa.String(36), nullable=True),
        sa.CheckConstraint("end_date >= start_date", name="ck_team_member_capacity_adjustments_dates"),
        sa.CheckConstraint(
            "availability_percent >= 0 AND availability_percent <= 100",
            name="ck_team_member_capacity_adjustments_percent",
        ),
        sqlite_autoincrement=True,
    )
    op.create_index(
        "ix_team_member_capacity_adjustments_member_dates",
        "team_member_capacity_adjustments",
        ["team_member_id", "start_date", "end_date"],
    )
    op.create_index(
        "ix_team_member_capacity_adjustments_group_token",
        "team_member_capacity_adjustments",
        ["group_token"],
    )


def downgrade() -> None:
    # An older server would silently count the row's whole-iteration percentage
    # on adjusted dates. Withdraw and export the adjustments first.
    connection = op.get_bind()
    table = sa.table("team_member_capacity_adjustments", sa.column("withdrawn_at"))
    active = connection.scalar(
        sa.select(sa.literal(1)).select_from(table).where(table.c.withdrawn_at.is_(None)).limit(1)
    )
    if active:
        raise RuntimeError("Withdraw active capacity adjustments before downgrading.")
    op.drop_index("ix_team_member_capacity_adjustments_group_token", table_name="team_member_capacity_adjustments")
    op.drop_index("ix_team_member_capacity_adjustments_member_dates", table_name="team_member_capacity_adjustments")
    op.drop_table("team_member_capacity_adjustments")
