"""Let a trusted-local session comment as the person profile it works as."""

from alembic import op
import sqlalchemy as sa


revision = "20261111_0013"
down_revision = "20261111_0012"
branch_labels = None
depends_on = None


def upgrade():
    connection = op.get_bind()
    sqlite = connection.dialect.name == "sqlite"
    if sqlite and connection.scalar(sa.text("PRAGMA foreign_keys")):
        raise RuntimeError("Comment table rebuild requires the serialized SQLite migration environment")
    for table in ("task_comments", "task_comment_revisions"):
        with op.batch_alter_table(table, recreate="always" if sqlite else "auto") as batch:
            batch.add_column(sa.Column("author_profile_id", sa.Integer(), nullable=True))
            batch.alter_column("principal_id", existing_type=sa.Integer(), nullable=True)


def downgrade():
    raise RuntimeError("Local comment authorship cannot be downgraded; restore the matching verified backup")
