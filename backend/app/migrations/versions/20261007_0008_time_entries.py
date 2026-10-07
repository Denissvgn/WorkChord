"""Retain private minute records and append-only correction history."""

from alembic import op
import sqlalchemy as sa

revision = "20261007_0008"
down_revision = "20261004_0007"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("time_entries",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("task_id", sa.Integer()), sa.Column("principal_id", sa.Integer(), nullable=False),
        sa.Column("task_title", sa.String(500)), sa.Column("request_id", sa.String(36), nullable=False),
        sa.Column("creation_digest", sa.String(64), nullable=False),
        sa.Column("work_date", sa.Date(), nullable=False), sa.Column("timezone", sa.String(64), nullable=False),
        sa.Column("minutes", sa.Integer(), nullable=False), sa.Column("note", sa.Text(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False), sa.Column("voided", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("minutes >= 1 AND minutes <= 1440", name="ck_time_entry_minutes"),
        sa.CheckConstraint("version >= 1", name="ck_time_entry_version"),
        sa.UniqueConstraint("principal_id", "request_id", name="uq_time_entry_request"),
        sqlite_autoincrement=True)
    op.create_index("ix_time_entry_author_date", "time_entries", ["principal_id", "work_date"])
    op.create_index("ix_time_entry_project_date", "time_entries", ["project_id", "work_date"])
    op.create_table("time_entry_revisions",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("entry_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False), sa.Column("principal_id", sa.Integer(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False), sa.Column("work_date", sa.Date(), nullable=False),
        sa.Column("timezone", sa.String(64), nullable=False), sa.Column("minutes", sa.Integer(), nullable=False),
        sa.Column("note", sa.Text(), nullable=False), sa.Column("voided", sa.Boolean(), nullable=False),
        sa.Column("reason", sa.String(1000), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("minutes >= 1 AND minutes <= 1440", name="ck_time_revision_minutes"),
        sa.CheckConstraint("version >= 1", name="ck_time_revision_version"),
        sa.UniqueConstraint("entry_id", "version", name="uq_time_entry_revision"))
    op.create_index("ix_time_revision_entry", "time_entry_revisions", ["entry_id", "version"])


def downgrade():
    raise RuntimeError("Time-entry corrections are immutable history; restore an authorized full backup for rollback")
