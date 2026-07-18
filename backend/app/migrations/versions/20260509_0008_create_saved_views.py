"""create saved views

Revision ID: 20260509_0008
Revises: 20260509_0007
Create Date: 2026-05-09
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "20260509_0008"
down_revision: Union[str, None] = "20260509_0007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "saved_views",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("view_type", sa.String(length=50), nullable=False),
        sa.Column("scope", sa.String(length=50), nullable=False),
        sa.Column("filters_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("sort_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("columns_json", sa.JSON(), nullable=False, server_default=sa.text("'{}'")),
        sa.Column("created_by_session_id", sa.Integer(), nullable=True),
        sa.Column("schema_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.CheckConstraint(
            "view_type IN ('tasks', 'projects', 'triage')",
            name="ck_saved_views_view_type",
        ),
        sa.CheckConstraint(
            "scope IN ('personal', 'shared', 'system')",
            name="ck_saved_views_scope",
        ),
        sa.CheckConstraint(
            "schema_version >= 1",
            name="ck_saved_views_schema_version_min",
        ),
        # ``user_sessions`` is introduced by revision 0023. SQLite historically
        # accepted this forward reference, while PostgreSQL rejects it. The
        # foreign key is added by 0023 after the target table exists.
    )
    op.create_index("ix_saved_views_view_type", "saved_views", ["view_type"])
    op.create_index("ix_saved_views_scope", "saved_views", ["scope"])
    op.create_index("ix_saved_views_created_by_session_id", "saved_views", ["created_by_session_id"])
    op.create_index("ix_saved_views_created_at", "saved_views", ["created_at"])
    op.create_index("ix_saved_views_updated_at", "saved_views", ["updated_at"])
    op.create_index("ix_saved_views_type_scope", "saved_views", ["view_type", "scope"])
    op.create_index(
        "ix_saved_views_type_creator",
        "saved_views",
        ["view_type", "created_by_session_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_saved_views_type_creator", table_name="saved_views")
    op.drop_index("ix_saved_views_type_scope", table_name="saved_views")
    op.drop_index("ix_saved_views_updated_at", table_name="saved_views")
    op.drop_index("ix_saved_views_created_at", table_name="saved_views")
    op.drop_index("ix_saved_views_created_by_session_id", table_name="saved_views")
    op.drop_index("ix_saved_views_scope", table_name="saved_views")
    op.drop_index("ix_saved_views_view_type", table_name="saved_views")
    op.drop_table("saved_views")
