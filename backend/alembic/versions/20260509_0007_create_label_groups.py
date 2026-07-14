"""create label groups

Revision ID: 20260509_0007
Revises: 20260508_0006
Create Date: 2026-05-09
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260509_0007"
down_revision: Union[str, None] = "20260508_0006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "label_groups",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("key", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("color", sa.String(length=7), nullable=False, server_default="#64748b"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("seed_key", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("key", name="uq_label_groups_key"),
    )
    op.create_index("ix_label_groups_key", "label_groups", ["key"])
    op.create_index("ix_label_groups_is_active", "label_groups", ["is_active"])
    op.create_index("ix_label_groups_sort_order", "label_groups", ["sort_order"])
    op.create_index("ix_label_groups_seed_key", "label_groups", ["seed_key"], unique=True)
    op.create_index("ix_label_groups_created_at", "label_groups", ["created_at"])
    op.create_index("ix_label_groups_updated_at", "label_groups", ["updated_at"])
    op.create_index(
        "ix_label_groups_active_order",
        "label_groups",
        ["is_active", "sort_order"],
    )

    op.create_table(
        "labels",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("slug", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("group_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("color", sa.String(length=7), nullable=False, server_default="#64748b"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("seed_key", sa.String(length=100), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.ForeignKeyConstraint(["group_id"], ["label_groups.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("slug", name="uq_labels_slug"),
    )
    op.create_index("ix_labels_slug", "labels", ["slug"])
    op.create_index("ix_labels_group_id", "labels", ["group_id"])
    op.create_index("ix_labels_is_active", "labels", ["is_active"])
    op.create_index("ix_labels_sort_order", "labels", ["sort_order"])
    op.create_index("ix_labels_seed_key", "labels", ["seed_key"], unique=True)
    op.create_index("ix_labels_created_at", "labels", ["created_at"])
    op.create_index("ix_labels_updated_at", "labels", ["updated_at"])
    op.create_index("ix_labels_group_active_order", "labels", ["group_id", "is_active", "sort_order"])


def downgrade() -> None:
    op.drop_index("ix_labels_group_active_order", table_name="labels")
    op.drop_index("ix_labels_updated_at", table_name="labels")
    op.drop_index("ix_labels_created_at", table_name="labels")
    op.drop_index("ix_labels_seed_key", table_name="labels")
    op.drop_index("ix_labels_sort_order", table_name="labels")
    op.drop_index("ix_labels_is_active", table_name="labels")
    op.drop_index("ix_labels_group_id", table_name="labels")
    op.drop_index("ix_labels_slug", table_name="labels")
    op.drop_table("labels")
    op.drop_index("ix_label_groups_active_order", table_name="label_groups")
    op.drop_index("ix_label_groups_updated_at", table_name="label_groups")
    op.drop_index("ix_label_groups_created_at", table_name="label_groups")
    op.drop_index("ix_label_groups_seed_key", table_name="label_groups")
    op.drop_index("ix_label_groups_sort_order", table_name="label_groups")
    op.drop_index("ix_label_groups_is_active", table_name="label_groups")
    op.drop_index("ix_label_groups_key", table_name="label_groups")
    op.drop_table("label_groups")
