"""Add short-lived browser-approved native connections."""

from alembic import op
import sqlalchemy as sa

revision = "20261003_0005"
down_revision = "20260930_0004"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("native_connections",
        sa.Column("request_hash", sa.String(64), primary_key=True),
        sa.Column("code_challenge", sa.String(43), nullable=False),
        sa.Column("verification_code", sa.String(9), nullable=False),
        sa.Column("request_ip_hash", sa.String(64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("approved_session_id", sa.Integer(), sa.ForeignKey("user_sessions.id", ondelete="CASCADE")),
        sa.Column("consumed_at", sa.DateTime(timezone=True)))
    for name in ("request_ip_hash", "expires_at"):
        op.create_index(f"ix_native_connections_{name}", "native_connections", [name])


def downgrade():
    op.drop_table("native_connections")
