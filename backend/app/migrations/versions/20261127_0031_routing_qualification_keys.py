"""Keep a deployment's declared qualification keys and let catalog entries hold them."""

from alembic import op
import sqlalchemy as sa


revision = "20261127_0031"
down_revision = "20261127_0030"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "routing_qualification_keys",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("key", sa.String(120), nullable=False),
        sa.Column("label", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("state", sa.String(20), nullable=False),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("retired_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("key", name="uq_routing_qualification_keys_key"),
        sa.CheckConstraint("state IN ('active', 'retired')", name="ck_routing_qualification_keys_state"),
        sa.CheckConstraint("revision >= 1", name="ck_routing_qualification_keys_revision"),
        sa.CheckConstraint("length(trim(key)) > 0", name="ck_routing_qualification_keys_key_not_blank"),
        sa.CheckConstraint("key = lower(trim(key))", name="ck_routing_qualification_keys_key_canonical"),
        sa.CheckConstraint("length(trim(label)) > 0", name="ck_routing_qualification_keys_label_not_blank"),
        sqlite_autoincrement=True,
    )
    op.create_index("ix_routing_qualification_keys_state", "routing_qualification_keys", ["state"])
    op.create_table(
        "routing_qualification_key_revisions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "qualification_key_id",
            sa.Integer(),
            sa.ForeignKey("routing_qualification_keys.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.Column("action", sa.String(20), nullable=False),
        sa.Column("state", sa.String(20), nullable=False),
        sa.Column("label", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("actor_type", sa.String(50), nullable=False),
        sa.Column("actor_id", sa.Integer(), sa.ForeignKey("agent_actors.id"), nullable=True),
        sa.Column("correlation_id", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "qualification_key_id",
            "revision",
            name="uq_routing_qualification_key_revisions_revision",
        ),
        sa.CheckConstraint(
            "action IN ('declare', 'revise', 'retire')",
            name="ck_routing_qualification_key_revisions_action",
        ),
        sa.CheckConstraint(
            "state IN ('active', 'retired')",
            name="ck_routing_qualification_key_revisions_state",
        ),
        sa.CheckConstraint(
            "length(trim(reason)) > 0",
            name="ck_routing_qualification_key_revisions_reason_not_blank",
        ),
        sqlite_autoincrement=True,
    )
    # Existing entries hold no qualification keys; nothing is read from tool tags.
    with op.batch_alter_table("agent_model_catalog_entries") as batch:
        batch.add_column(
            sa.Column("qualification_keys", sa.JSON(), nullable=False, server_default=sa.text("'[]'"))
        )


def downgrade() -> None:
    # An older server would route without the requirement a key expresses and
    # would lose the registry's audited history, so both must be empty first.
    connection = op.get_bind()
    catalog = sa.table("agent_model_catalog_entries", sa.column("qualification_keys", sa.JSON()))
    keys = sa.table("routing_qualification_keys", sa.column("id"))
    held = any(
        value not in (None, [], "[]")
        for value in connection.execute(sa.select(catalog.c.qualification_keys)).scalars()
    )
    if held or connection.scalar(sa.select(sa.literal(1)).select_from(keys).limit(1)):
        raise RuntimeError(
            "Qualification keys are declared or held by catalog entries; clear them before downgrading."
        )
    with op.batch_alter_table("agent_model_catalog_entries") as batch:
        batch.drop_column("qualification_keys")
    op.drop_table("routing_qualification_key_revisions")
    op.drop_index("ix_routing_qualification_keys_state", table_name="routing_qualification_keys")
    op.drop_table("routing_qualification_keys")
