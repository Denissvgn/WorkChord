"""Add provider-neutral model catalog and actor bindings.

Revision ID: 20260718_0029
Revises: 20260711_0028
Create Date: 2026-07-18 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260718_0029"
down_revision: str | None = "20260711_0028"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "agent_model_catalog_entries",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("key", sa.String(length=120), nullable=False),
        sa.Column("provider", sa.String(length=120), nullable=False),
        sa.Column("configured_model_alias", sa.String(length=255), nullable=False),
        sa.Column("reasoning_tier", sa.Integer(), nullable=False),
        sa.Column("context_tier", sa.String(length=20), nullable=False),
        sa.Column(
            "modality_tags",
            sa.JSON(),
            server_default=sa.text("'[\"text\"]'"),
            nullable=False,
        ),
        sa.Column("cost_tier", sa.String(length=20), nullable=False),
        sa.Column("latency_tier", sa.String(length=20), nullable=False),
        sa.Column("enabled", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("revision", sa.Integer(), server_default="1", nullable=False),
        sa.Column("last_verified_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "reasoning_tier >= 1 AND reasoning_tier <= 3",
            name="ck_agent_model_catalog_reasoning_tier",
        ),
        sa.CheckConstraint(
            "context_tier IN ('small', 'medium', 'large')",
            name="ck_agent_model_catalog_context_tier",
        ),
        sa.CheckConstraint(
            "cost_tier IN ('low', 'medium', 'high')",
            name="ck_agent_model_catalog_cost_tier",
        ),
        sa.CheckConstraint(
            "latency_tier IN ('fast', 'balanced', 'slow')",
            name="ck_agent_model_catalog_latency_tier",
        ),
        sa.CheckConstraint(
            "revision >= 1",
            name="ck_agent_model_catalog_revision",
        ),
        sa.CheckConstraint(
            "length(trim(key)) > 0",
            name="ck_agent_model_catalog_key_not_blank",
        ),
        sa.CheckConstraint(
            "key = lower(trim(key))",
            name="ck_agent_model_catalog_key_canonical",
        ),
        sa.CheckConstraint(
            "length(trim(provider)) > 0",
            name="ck_agent_model_catalog_provider_not_blank",
        ),
        sa.CheckConstraint(
            "length(trim(configured_model_alias)) > 0",
            name="ck_agent_model_catalog_alias_not_blank",
        ),
        sa.UniqueConstraint("key", name="uq_agent_model_catalog_key"),
    )
    op.create_index(
        "ix_agent_model_catalog_enabled",
        "agent_model_catalog_entries",
        ["enabled"],
    )

    op.create_table(
        "agent_model_bindings",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("actor_id", sa.Integer(), nullable=False),
        sa.Column("model_catalog_id", sa.Integer(), nullable=False),
        sa.Column("is_default", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("enabled", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column(
            "tool_tags",
            sa.JSON(),
            server_default=sa.text("'[]'"),
            nullable=False,
        ),
        sa.Column(
            "data_policy_tags",
            sa.JSON(),
            server_default=sa.text("'[]'"),
            nullable=False,
        ),
        sa.Column("revision", sa.Integer(), server_default="1", nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            "revision >= 1",
            name="ck_agent_model_bindings_revision",
        ),
        sa.CheckConstraint(
            "(NOT is_default) OR enabled",
            name="ck_agent_model_bindings_default_enabled",
        ),
        sa.ForeignKeyConstraint(
            ["actor_id"],
            ["agent_actors.id"],
            ondelete="CASCADE",
            name="fk_agent_model_bindings_actor_id",
        ),
        sa.ForeignKeyConstraint(
            ["model_catalog_id"],
            ["agent_model_catalog_entries.id"],
            ondelete="RESTRICT",
            name="fk_agent_model_bindings_model_catalog_id",
        ),
        sa.UniqueConstraint(
            "actor_id",
            "model_catalog_id",
            name="uq_agent_model_bindings_actor_catalog",
        ),
    )
    op.create_index(
        "ix_agent_model_bindings_actor_enabled",
        "agent_model_bindings",
        ["actor_id", "enabled"],
    )
    op.create_index(
        "ix_agent_model_bindings_catalog_enabled",
        "agent_model_bindings",
        ["model_catalog_id", "enabled"],
    )
    op.create_index(
        "uq_agent_model_bindings_default_enabled",
        "agent_model_bindings",
        ["actor_id"],
        unique=True,
        sqlite_where=sa.text("is_default AND enabled"),
        postgresql_where=sa.text("is_default AND enabled"),
    )


def downgrade() -> None:
    op.drop_index(
        "uq_agent_model_bindings_default_enabled",
        table_name="agent_model_bindings",
    )
    op.drop_index(
        "ix_agent_model_bindings_catalog_enabled",
        table_name="agent_model_bindings",
    )
    op.drop_index(
        "ix_agent_model_bindings_actor_enabled",
        table_name="agent_model_bindings",
    )
    op.drop_table("agent_model_bindings")
    op.drop_index(
        "ix_agent_model_catalog_enabled",
        table_name="agent_model_catalog_entries",
    )
    op.drop_table("agent_model_catalog_entries")
