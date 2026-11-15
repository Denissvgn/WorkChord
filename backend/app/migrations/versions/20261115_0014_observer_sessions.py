"""Record a session's access level, and what a pairing request asks for."""

from alembic import op
import sqlalchemy as sa


revision = "20261115_0014"
down_revision = "20261111_0013"
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    sqlite = connection.dialect.name == "sqlite"
    if sqlite and connection.scalar(sa.text("PRAGMA foreign_keys")):
        raise RuntimeError("Session table rebuild requires the serialized SQLite migration environment")
    with op.batch_alter_table("user_sessions", recreate="always" if sqlite else "auto") as batch:
        batch.add_column(sa.Column("access", sa.String(length=16), nullable=False, server_default="full"))
        batch.add_column(sa.Column("client_label", sa.String(length=80), nullable=True))
        batch.create_check_constraint("ck_user_sessions_access", "access IN ('full', 'observe')")
    with op.batch_alter_table("native_connections", recreate="always" if sqlite else "auto") as batch:
        batch.add_column(sa.Column("requested_access", sa.String(length=16), nullable=False, server_default="full"))
        batch.add_column(sa.Column("client_label", sa.String(length=80), nullable=True))
        batch.create_check_constraint("ck_native_connections_requested_access", "requested_access IN ('full', 'observe')")


def downgrade():
    raise RuntimeError("Observer sessions cannot be downgraded; restore the matching verified backup")
