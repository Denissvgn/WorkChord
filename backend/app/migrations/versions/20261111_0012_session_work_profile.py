"""Let a trusted-local browser session choose the person profile it works as."""

from alembic import op
import sqlalchemy as sa


revision = "20261111_0012"
down_revision = "20261009_0011"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("user_sessions", sa.Column("local_profile_id", sa.Integer(), nullable=True))


def downgrade():
    with op.batch_alter_table("user_sessions") as batch:
        batch.drop_column("local_profile_id")
