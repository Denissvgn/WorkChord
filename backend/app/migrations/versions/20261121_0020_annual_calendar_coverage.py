"""Store explicitly selected annual calendars for iterations and profile owners."""

from alembic import op
import sqlalchemy as sa

revision = "20261121_0020"
down_revision = "20261121_0019"
branch_labels = None
depends_on = None


def upgrade() -> None:
    for name, owner_key, owner in (
        ("iteration_annual_calendars", "iteration_id", "iterations.id"),
        ("profile_annual_calendars", "profile_id", "profile_availability.profile_id"),
    ):
        op.create_table(
            name,
            sa.Column(owner_key, sa.Integer(), sa.ForeignKey(owner, ondelete="CASCADE"), primary_key=True),
            sa.Column(
                "calendar_id",
                sa.Integer(),
                sa.ForeignKey("calendars.id", ondelete="RESTRICT"),
                primary_key=True,
            ),
        )
        op.create_index(f"ix_{name}_calendar_id", name, ["calendar_id"])


def downgrade() -> None:
    # An older server cannot retain these explicit choices. An operator must
    # export/remove them through the owner-aware calendar command first.
    connection = op.get_bind()
    for table in ("profile_annual_calendars", "iteration_annual_calendars"):
        if connection.scalar(sa.select(sa.literal(1)).select_from(sa.table(table)).limit(1)):
            raise RuntimeError("Export and clear additional annual calendar selections before downgrading.")
    op.drop_table("profile_annual_calendars")
    op.drop_table("iteration_annual_calendars")
