"""create external links

Revision ID: 20260509_0014
Revises: 20260509_0013
Create Date: 2026-05-09
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260509_0014"
down_revision: Union[str, None] = "20260509_0013"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "external_links",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("entity_type", sa.String(length=50), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column("external_key", sa.String(length=255), nullable=True),
        sa.Column("url", sa.String(length=1000), nullable=True),
        sa.Column("title", sa.String(length=500), nullable=True),
        sa.Column("status", sa.String(length=100), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint(
            "entity_type IN ('task', 'project', 'release')",
            name="ck_external_links_entity_type",
        ),
        sa.CheckConstraint(
            "provider IN ('github', 'gitlab', 'figma', 'sentry', 'custom')",
            name="ck_external_links_provider",
        ),
    )
    op.create_index(
        "ix_external_links_entity",
        "external_links",
        ["entity_type", "entity_id"],
    )
    op.create_index(
        "ix_external_links_provider_key",
        "external_links",
        ["provider", "external_key"],
    )
    op.create_index("ix_external_links_url", "external_links", ["url"])
    op.create_index("ix_external_links_updated_at", "external_links", ["updated_at"])


def downgrade() -> None:
    op.drop_index("ix_external_links_updated_at", table_name="external_links")
    op.drop_index("ix_external_links_url", table_name="external_links")
    op.drop_index("ix_external_links_provider_key", table_name="external_links")
    op.drop_index("ix_external_links_entity", table_name="external_links")
    op.drop_table("external_links")
