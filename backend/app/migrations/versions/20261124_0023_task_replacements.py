"""Record audited clean-replacement dispositions between tasks."""

from alembic import op
import sqlalchemy as sa


revision = "20261124_0023"
down_revision = "20261124_0022"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "task_replacements",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False),
        sa.Column("original_task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("replacement_task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("owner_decision", sa.Text(), nullable=False),
        sa.Column("base_commit_url", sa.String(1000), nullable=False),
        sa.Column("carried_run_ids", sa.JSON(), nullable=False),
        sa.Column("moved_dependencies", sa.JSON(), nullable=False),
        sa.Column("moved_release_ids", sa.JSON(), nullable=False),
        sa.Column("original_snapshot", sa.JSON(), nullable=False),
        sa.Column("review_policy", sa.JSON(), nullable=False),
        sa.Column("decided_by_principal_id", sa.Integer(), sa.ForeignKey("principals.id", ondelete="SET NULL")),
        sa.Column("decided_by_actor_id", sa.Integer(), sa.ForeignKey("agent_actors.id", ondelete="SET NULL")),
        sa.Column("decided_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint("original_task_id <> replacement_task_id", name="ck_task_replacements_distinct"),
        sa.UniqueConstraint("original_task_id", name="uq_task_replacements_original_task_id"),
        sa.UniqueConstraint("replacement_task_id", name="uq_task_replacements_replacement_task_id"),
        sqlite_autoincrement=True,
    )
    op.create_index("ix_task_replacements_project_id", "task_replacements", ["project_id"])


def downgrade() -> None:
    # An older server would show a replaced original as plain canceled work and
    # could accept a held replacement. Keep the disposition unless none exist.
    connection = op.get_bind()
    table = sa.table("task_replacements", sa.column("id"))
    if connection.scalar(sa.select(sa.literal(1)).select_from(table).limit(1)):
        raise RuntimeError("Task replacement dispositions exist; export them before downgrading.")
    op.drop_index("ix_task_replacements_project_id", table_name="task_replacements")
    op.drop_table("task_replacements")
