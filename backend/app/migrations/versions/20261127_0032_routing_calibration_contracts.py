"""Keep the deployment's calibration contracts and their append-only revisions."""

from alembic import op
import sqlalchemy as sa


revision = "20261127_0032"
down_revision = "20261127_0031"
branch_labels = None
depends_on = None

APPROVAL_CONSISTENCY = (
    "(state = 'approved' AND approved_at IS NOT NULL AND approved_by_actor_type IS NOT NULL "
    "AND approval_reason IS NOT NULL AND approved_as IS NOT NULL) OR (state = 'submitted' AND approved_at IS NULL "
    "AND approved_by_actor_type IS NULL AND approved_by_actor_id IS NULL AND approval_reason IS NULL "
    "AND approved_as IS NULL)"
)


def upgrade() -> None:
    op.create_table(
        "routing_calibration_contracts",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("key", sa.String(120), nullable=False),
        sa.Column("schema_version", sa.String(60), nullable=False),
        sa.Column("state", sa.String(20), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("terms", sa.JSON(), nullable=False),
        sa.Column("terms_digest", sa.String(64), nullable=False),
        sa.Column("submitted_by_actor_type", sa.String(50), nullable=False),
        sa.Column("submitted_by_actor_id", sa.Integer(), sa.ForeignKey("agent_actors.id"), nullable=True),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("approved_by_actor_type", sa.String(50), nullable=True),
        sa.Column("approved_by_actor_id", sa.Integer(), sa.ForeignKey("agent_actors.id"), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("approval_reason", sa.Text(), nullable=True),
        sa.Column("approved_as", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("key", name="uq_routing_calibration_contracts_key"),
        sa.CheckConstraint("state IN ('submitted', 'approved')", name="ck_routing_calibration_contracts_state"),
        sa.CheckConstraint("revision >= 1", name="ck_routing_calibration_contracts_revision"),
        sa.CheckConstraint("length(trim(key)) > 0", name="ck_routing_calibration_contracts_key_not_blank"),
        sa.CheckConstraint("key = lower(trim(key))", name="ck_routing_calibration_contracts_key_canonical"),
        sa.CheckConstraint("length(terms_digest) = 64", name="ck_routing_calibration_contracts_terms_digest"),
        sa.CheckConstraint(APPROVAL_CONSISTENCY, name="ck_routing_calibration_contracts_approval"),
        sqlite_autoincrement=True,
    )
    op.create_index("ix_routing_calibration_contracts_state", "routing_calibration_contracts", ["state"])
    op.create_table(
        "routing_calibration_contract_revisions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "contract_id",
            sa.Integer(),
            sa.ForeignKey("routing_calibration_contracts.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("action", sa.String(20), nullable=False),
        sa.Column("state", sa.String(20), nullable=False),
        sa.Column("terms", sa.JSON(), nullable=False),
        sa.Column("terms_digest", sa.String(64), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("approved_as", sa.String(255), nullable=True),
        sa.Column("actor_type", sa.String(50), nullable=False),
        sa.Column("actor_id", sa.Integer(), sa.ForeignKey("agent_actors.id"), nullable=True),
        sa.Column("correlation_id", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "contract_id",
            "revision",
            name="uq_routing_calibration_contract_revisions_revision",
        ),
        sa.CheckConstraint(
            "action IN ('submit', 'approve')",
            name="ck_routing_calibration_contract_revisions_action",
        ),
        sa.CheckConstraint(
            "state IN ('submitted', 'approved')",
            name="ck_routing_calibration_contract_revisions_state",
        ),
        sa.CheckConstraint(
            "length(trim(reason)) > 0",
            name="ck_routing_calibration_contract_revisions_reason_not_blank",
        ),
        sa.CheckConstraint(
            "(action = 'approve' AND approved_as IS NOT NULL) OR (action = 'submit' AND approved_as IS NULL)",
            name="ck_routing_calibration_contract_revisions_approved_as",
        ),
        sqlite_autoincrement=True,
    )


def downgrade() -> None:
    # Contracts and their revisions are audited history with no delete, so a
    # deployment that has submitted one cannot downgrade past this revision.
    connection = op.get_bind()
    contracts = sa.table("routing_calibration_contracts", sa.column("id"))
    if connection.scalar(sa.select(sa.literal(1)).select_from(contracts).limit(1)):
        raise RuntimeError(
            "Downgrade is unsupported once a calibration contract has been submitted: "
            "contracts keep their audited history and offer no delete."
        )
    op.drop_table("routing_calibration_contract_revisions")
    op.drop_index("ix_routing_calibration_contracts_state", table_name="routing_calibration_contracts")
    op.drop_table("routing_calibration_contracts")
