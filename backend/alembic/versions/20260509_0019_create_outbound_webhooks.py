"""Create outbound webhook targets and delivery logs.

Revision ID: 20260509_0019
Revises: 20260509_0018
Create Date: 2026-05-09 00:19:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260509_0019"
down_revision: str | None = "20260509_0018"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "outbound_webhook_targets",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("url", sa.String(length=1000), nullable=False),
        sa.Column("enabled", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("subscribed_events_json", sa.JSON(), server_default=sa.text("'[]'"), nullable=False),
        sa.Column("secret", sa.String(length=500), nullable=True),
        sa.Column("headers_json", sa.JSON(), server_default=sa.text("'{}'"), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_outbound_webhook_targets_enabled",
        "outbound_webhook_targets",
        ["enabled"],
    )
    op.create_index(
        "ix_outbound_webhook_targets_created_at",
        "outbound_webhook_targets",
        ["created_at"],
    )
    op.create_index(
        "ix_outbound_webhook_targets_updated_at",
        "outbound_webhook_targets",
        ["updated_at"],
    )

    op.create_table(
        "outbound_webhook_events",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.String(length=64), nullable=False),
        sa.Column("event_type", sa.String(length=120), nullable=False),
        sa.Column("entity_type", sa.String(length=80), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=True),
        sa.Column("payload_json", sa.JSON(), server_default=sa.text("'{}'"), nullable=False),
        sa.Column("occurred_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("event_id", name="uq_outbound_webhook_events_event_id"),
    )
    op.create_index(
        "ix_outbound_webhook_events_event_id",
        "outbound_webhook_events",
        ["event_id"],
    )
    op.create_index(
        "ix_outbound_webhook_events_event_type",
        "outbound_webhook_events",
        ["event_type"],
    )
    op.create_index(
        "ix_outbound_webhook_events_entity_type",
        "outbound_webhook_events",
        ["entity_type"],
    )
    op.create_index(
        "ix_outbound_webhook_events_entity_id",
        "outbound_webhook_events",
        ["entity_id"],
    )
    op.create_index(
        "ix_outbound_webhook_events_occurred_at",
        "outbound_webhook_events",
        ["occurred_at"],
    )
    op.create_index(
        "ix_outbound_webhook_events_type_time",
        "outbound_webhook_events",
        ["event_type", "occurred_at"],
    )
    op.create_index(
        "ix_outbound_webhook_events_entity",
        "outbound_webhook_events",
        ["entity_type", "entity_id"],
    )

    op.create_table(
        "outbound_webhook_deliveries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("target_id", sa.Integer(), nullable=True),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("target_name", sa.String(length=255), nullable=False),
        sa.Column("target_url", sa.String(length=1000), nullable=False),
        sa.Column("status", sa.String(length=50), server_default="pending", nullable=False),
        sa.Column("attempt_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("last_http_status", sa.Integer(), nullable=True),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column("last_response_body", sa.Text(), nullable=True),
        sa.Column("last_attempt_at", sa.DateTime(), nullable=True),
        sa.Column("next_retry_at", sa.DateTime(), nullable=True),
        sa.Column("delivered_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint(
            "status IN ('pending', 'delivered', 'failed')",
            name="ck_outbound_webhook_deliveries_status",
        ),
        sa.ForeignKeyConstraint(
            ["event_id"],
            ["outbound_webhook_events.id"],
            name="fk_outbound_webhook_deliveries_event_id",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["target_id"],
            ["outbound_webhook_targets.id"],
            name="fk_outbound_webhook_deliveries_target_id",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_outbound_webhook_deliveries_target_id",
        "outbound_webhook_deliveries",
        ["target_id"],
    )
    op.create_index(
        "ix_outbound_webhook_deliveries_status",
        "outbound_webhook_deliveries",
        ["status"],
    )
    op.create_index(
        "ix_outbound_webhook_deliveries_event_id",
        "outbound_webhook_deliveries",
        ["event_id"],
    )
    op.create_index(
        "ix_outbound_webhook_deliveries_created_at",
        "outbound_webhook_deliveries",
        ["created_at"],
    )
    op.create_index(
        "ix_outbound_webhook_deliveries_target_status",
        "outbound_webhook_deliveries",
        ["target_id", "status"],
    )


def downgrade() -> None:
    op.drop_index("ix_outbound_webhook_deliveries_target_status", table_name="outbound_webhook_deliveries")
    op.drop_index("ix_outbound_webhook_deliveries_created_at", table_name="outbound_webhook_deliveries")
    op.drop_index("ix_outbound_webhook_deliveries_event_id", table_name="outbound_webhook_deliveries")
    op.drop_index("ix_outbound_webhook_deliveries_status", table_name="outbound_webhook_deliveries")
    op.drop_index("ix_outbound_webhook_deliveries_target_id", table_name="outbound_webhook_deliveries")
    op.drop_table("outbound_webhook_deliveries")

    op.drop_index("ix_outbound_webhook_events_entity", table_name="outbound_webhook_events")
    op.drop_index("ix_outbound_webhook_events_type_time", table_name="outbound_webhook_events")
    op.drop_index("ix_outbound_webhook_events_occurred_at", table_name="outbound_webhook_events")
    op.drop_index("ix_outbound_webhook_events_entity_id", table_name="outbound_webhook_events")
    op.drop_index("ix_outbound_webhook_events_entity_type", table_name="outbound_webhook_events")
    op.drop_index("ix_outbound_webhook_events_event_type", table_name="outbound_webhook_events")
    op.drop_index("ix_outbound_webhook_events_event_id", table_name="outbound_webhook_events")
    op.drop_table("outbound_webhook_events")

    op.drop_index("ix_outbound_webhook_targets_updated_at", table_name="outbound_webhook_targets")
    op.drop_index("ix_outbound_webhook_targets_created_at", table_name="outbound_webhook_targets")
    op.drop_index("ix_outbound_webhook_targets_enabled", table_name="outbound_webhook_targets")
    op.drop_table("outbound_webhook_targets")
