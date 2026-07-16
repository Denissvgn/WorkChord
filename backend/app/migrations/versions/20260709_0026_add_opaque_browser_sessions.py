"""Replace IP ownership with opaque browser-session tokens.

Revision ID: 20260709_0026
Revises: 20260516_0025
Create Date: 2026-07-09 00:26:00.000000
"""

from collections.abc import Sequence
import secrets

import sqlalchemy as sa
from alembic import op


revision: str = "20260709_0026"
down_revision: str | None = "20260516_0025"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "user_sessions" not in inspector.get_table_names():
        return

    columns = {column["name"] for column in inspector.get_columns("user_sessions")}
    with op.batch_alter_table("user_sessions") as batch:
        if "public_id" not in columns:
            batch.add_column(sa.Column("public_id", sa.String(length=24), nullable=True))
        if "session_token_hash" not in columns:
            batch.add_column(sa.Column("session_token_hash", sa.String(length=64), nullable=True))
        if "expires_at" not in columns:
            batch.add_column(sa.Column("expires_at", sa.DateTime(timezone=True), nullable=True))
        if "revoked_at" not in columns:
            batch.add_column(sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True))

    rows = bind.execute(
        sa.text("SELECT id, public_id, session_token_hash FROM user_sessions ORDER BY id")
    ).mappings().all()
    public_ids: set[str] = set()
    token_hashes: set[str] = set()
    for row in rows:
        public_id = row["public_id"]
        if not public_id or public_id in public_ids:
            public_id = secrets.token_hex(6)
            while public_id in public_ids:
                public_id = secrets.token_hex(6)
            bind.execute(
                sa.text("UPDATE user_sessions SET public_id = :public_id WHERE id = :id"),
                {"public_id": public_id, "id": row["id"]},
            )
        public_ids.add(public_id)

        token_hash = row["session_token_hash"]
        if token_hash and token_hash in token_hashes:
            # A partially applied migration must never leave one bearer token
            # resolving to multiple owners. Null hashes are intentionally
            # unclaimable and receive a new identity on the next request.
            bind.execute(
                sa.text(
                    "UPDATE user_sessions SET session_token_hash = NULL WHERE id = :id"
                ),
                {"id": row["id"]},
            )
        elif token_hash:
            token_hashes.add(token_hash)

    inspector = sa.inspect(bind)
    index_names = {index["name"] for index in inspector.get_indexes("user_sessions")}

    with op.batch_alter_table("user_sessions") as batch:
        batch.alter_column("public_id", existing_type=sa.String(length=24), nullable=False)
        if "ix_user_sessions_ip_address" in index_names:
            batch.drop_index("ix_user_sessions_ip_address")
        batch.create_index("ix_user_sessions_ip_address", ["ip_address"], unique=False)
        if "ix_user_sessions_public_id" not in index_names:
            batch.create_index("ix_user_sessions_public_id", ["public_id"], unique=True)
        if "ix_user_sessions_session_token_hash" not in index_names:
            batch.create_index(
                "ix_user_sessions_session_token_hash",
                ["session_token_hash"],
                unique=True,
            )


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "user_sessions" not in inspector.get_table_names():
        return

    index_names = {index["name"] for index in inspector.get_indexes("user_sessions")}

    # The old schema requires one row per IP. Preserve every session and its
    # ownership links while preventing a downgraded application from claiming
    # an opaque identity through historical network metadata.
    session_ids = bind.execute(sa.text("SELECT id FROM user_sessions ORDER BY id")).scalars()
    for session_id in session_ids:
        bind.execute(
            sa.text("UPDATE user_sessions SET ip_address = :ip_address WHERE id = :id"),
            {
                "ip_address": f"rollback-session-{session_id}",
                "id": session_id,
            },
        )
    with op.batch_alter_table("user_sessions") as batch:
        if "ix_user_sessions_session_token_hash" in index_names:
            batch.drop_index("ix_user_sessions_session_token_hash")
        if "ix_user_sessions_public_id" in index_names:
            batch.drop_index("ix_user_sessions_public_id")
        if "ix_user_sessions_ip_address" in index_names:
            batch.drop_index("ix_user_sessions_ip_address")
        batch.create_index("ix_user_sessions_ip_address", ["ip_address"], unique=True)
        for column_name in ("revoked_at", "expires_at", "session_token_hash", "public_id"):
            if column_name in {column["name"] for column in inspector.get_columns("user_sessions")}:
                batch.drop_column(column_name)
