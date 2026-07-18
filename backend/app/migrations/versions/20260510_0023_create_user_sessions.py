"""Create user sessions table.

Revision ID: 20260510_0023
Revises: 20260510_0022
Create Date: 2026-05-10 00:23:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260510_0023"
down_revision: str | None = "20260510_0022"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "user_sessions" not in inspector.get_table_names():
        op.create_table(
            "user_sessions",
            sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
            sa.Column("ip_address", sa.String(), nullable=False),
            sa.Column("user_agent", sa.String(), nullable=True),
            sa.Column("created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
            sa.Column("last_seen_at", sa.DateTime(), server_default=sa.func.now(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(
            "ix_user_sessions_ip_address",
            "user_sessions",
            ["ip_address"],
            unique=True,
        )

    for table_name in ("saved_views", "project_updates"):
        foreign_keys = {
            tuple(foreign_key.get("constrained_columns") or ())
            for foreign_key in sa.inspect(bind).get_foreign_keys(table_name)
        }
        if ("created_by_session_id",) not in foreign_keys:
            with op.batch_alter_table(table_name) as batch_op:
                batch_op.create_foreign_key(
                    f"fk_{table_name}_created_by_session_id_user_sessions",
                    "user_sessions",
                    ["created_by_session_id"],
                    ["id"],
                    ondelete="SET NULL",
                )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "user_sessions" not in inspector.get_table_names():
        return

    for table_name in ("saved_views", "project_updates"):
        constraint_name = (
            f"fk_{table_name}_created_by_session_id_user_sessions"
        )
        foreign_keys = {
            foreign_key.get("name"): tuple(
                foreign_key.get("constrained_columns") or ()
            )
            for foreign_key in inspector.get_foreign_keys(table_name)
        }
        if foreign_keys.get(constraint_name) == ("created_by_session_id",):
            with op.batch_alter_table(table_name) as batch_op:
                batch_op.drop_constraint(constraint_name, type_="foreignkey")

    op.drop_index("ix_user_sessions_ip_address", table_name="user_sessions")
    op.drop_table("user_sessions")
