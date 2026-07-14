"""Add durable multi-channel outbound delivery queue metadata.

Revision ID: 20260709_0027
Revises: 20260709_0026
Create Date: 2026-07-09 00:27:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260709_0027"
down_revision: str | None = "20260709_0026"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "outbound_webhook_deliveries" not in inspector.get_table_names():
        return

    columns = {
        column["name"]
        for column in inspector.get_columns("outbound_webhook_deliveries")
    }
    with op.batch_alter_table("outbound_webhook_deliveries") as batch:
        if "channel" not in columns:
            batch.add_column(
                sa.Column(
                    "channel",
                    sa.String(length=30),
                    server_default="webhook",
                    nullable=False,
                )
            )
        if "payload_json" not in columns:
            batch.add_column(
                sa.Column(
                    "payload_json",
                    sa.JSON(),
                    server_default=sa.text("'{}'"),
                    nullable=False,
                )
            )
        if "max_attempts" not in columns:
            batch.add_column(
                sa.Column(
                    "max_attempts",
                    sa.Integer(),
                    server_default="5",
                    nullable=False,
                )
            )
        if "lease_token" not in columns:
            batch.add_column(sa.Column("lease_token", sa.String(length=64), nullable=True))
        if "lease_expires_at" not in columns:
            batch.add_column(sa.Column("lease_expires_at", sa.DateTime(timezone=True), nullable=True))
        if "terminal_at" not in columns:
            batch.add_column(sa.Column("terminal_at", sa.DateTime(timezone=True), nullable=True))

    bind.execute(
        sa.text(
            """
            UPDATE outbound_webhook_deliveries
            SET terminal_at = COALESCE(terminal_at, updated_at)
            WHERE status = 'failed' AND next_retry_at IS NULL
            """
        )
    )

    inspector = sa.inspect(bind)
    indexes = {
        index["name"]
        for index in inspector.get_indexes("outbound_webhook_deliveries")
    }
    checks = {
        constraint["name"]
        for constraint in inspector.get_check_constraints(
            "outbound_webhook_deliveries"
        )
    }
    with op.batch_alter_table("outbound_webhook_deliveries") as batch:
        if "ck_outbound_webhook_deliveries_channel" not in checks:
            batch.create_check_constraint(
                "ck_outbound_webhook_deliveries_channel",
                "channel IN ('webhook', 'email')",
            )
        if "ix_outbound_webhook_deliveries_channel" not in indexes:
            batch.create_index(
                "ix_outbound_webhook_deliveries_channel",
                ["channel"],
                unique=False,
            )
        if "ix_outbound_webhook_deliveries_lease_token" not in indexes:
            batch.create_index(
                "ix_outbound_webhook_deliveries_lease_token",
                ["lease_token"],
                unique=False,
            )
        if "ix_outbound_webhook_deliveries_due" not in indexes:
            batch.create_index(
                "ix_outbound_webhook_deliveries_due",
                ["status", "next_retry_at", "lease_expires_at"],
                unique=False,
            )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "outbound_webhook_deliveries" not in inspector.get_table_names():
        return

    indexes = {
        index["name"]
        for index in inspector.get_indexes("outbound_webhook_deliveries")
    }
    checks = {
        constraint["name"]
        for constraint in inspector.get_check_constraints(
            "outbound_webhook_deliveries"
        )
    }
    columns = {
        column["name"]
        for column in inspector.get_columns("outbound_webhook_deliveries")
    }
    with op.batch_alter_table("outbound_webhook_deliveries") as batch:
        for index_name in (
            "ix_outbound_webhook_deliveries_due",
            "ix_outbound_webhook_deliveries_lease_token",
            "ix_outbound_webhook_deliveries_channel",
        ):
            if index_name in indexes:
                batch.drop_index(index_name)
        if "ck_outbound_webhook_deliveries_channel" in checks:
            batch.drop_constraint(
                "ck_outbound_webhook_deliveries_channel",
                type_="check",
            )
        for column_name in (
            "terminal_at",
            "lease_expires_at",
            "lease_token",
            "max_attempts",
            "payload_json",
            "channel",
        ):
            if column_name in columns:
                batch.drop_column(column_name)
