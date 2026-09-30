"""Add retained discussion, subscriptions and the personal inbox transport."""

from alembic import op
import sqlalchemy as sa

revision = "20260930_0004"
down_revision = "20260930_0003"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("task_comments",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="SET NULL")),
        sa.Column("original_task_id", sa.Integer(), nullable=False),
        sa.Column("principal_id", sa.Integer(), sa.ForeignKey("principals.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("body", sa.Text(), nullable=False), sa.Column("mentions", sa.JSON(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False), sa.Column("deleted", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("version >= 1", name="ck_task_comment_version"))
    op.create_index("ix_task_comments_task_id", "task_comments", ["task_id"])
    op.create_table("task_comment_revisions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("comment_id", sa.Integer(), sa.ForeignKey("task_comments.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("original_task_id", sa.Integer(), nullable=False),
        sa.Column("principal_id", sa.Integer(), sa.ForeignKey("principals.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False), sa.Column("body", sa.Text(), nullable=False),
        sa.Column("mentions", sa.JSON(), nullable=False), sa.Column("deleted", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("comment_id", "version", name="uq_task_comment_revision"))
    for column in ("comment_id", "original_task_id"):
        op.create_index(f"ix_task_comment_revisions_{column}", "task_comment_revisions", [column])
    op.create_table("task_subscriptions",
        sa.Column("task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("principal_id", sa.Integer(), sa.ForeignKey("principals.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("enabled", sa.Boolean(), nullable=False), sa.Column("events", sa.JSON(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False))
    with op.batch_alter_table("outbound_webhook_deliveries") as batch:
        batch.drop_constraint("ck_outbound_webhook_deliveries_channel", type_="check")
        batch.create_check_constraint("ck_outbound_webhook_deliveries_channel", "channel IN ('webhook', 'email', 'inbox')")
    op.create_table("inbox_notifications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="SET NULL")),
        sa.Column("principal_id", sa.Integer(), sa.ForeignKey("principals.id", ondelete="CASCADE"), nullable=False),
        sa.Column("delivery_id", sa.Integer(), sa.ForeignKey("outbound_webhook_deliveries.id", ondelete="RESTRICT"), nullable=False, unique=True),
        sa.Column("event_type", sa.String(32), nullable=False), sa.Column("read", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False))
    for column in ("task_id", "principal_id"):
        op.create_index(f"ix_inbox_notifications_{column}", "inbox_notifications", [column])


def downgrade():
    raise RuntimeError("Retained discussion cannot be downgraded; restore a verified backup.")
