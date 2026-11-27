"""Record postponed tasks and the requirements that must hold before they resume."""

from alembic import op
import sqlalchemy as sa


revision = "20261126_0027"
down_revision = "20261126_0026"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Task status is free text, so existing rows keep their status unchanged.
    op.create_table(
        "task_postponements",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False),
        sa.Column("from_status", sa.String(16), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("postponed_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("postponed_by_principal_id", sa.Integer(), sa.ForeignKey("principals.id", ondelete="SET NULL")),
        sa.Column("postponed_by_actor_id", sa.Integer(), sa.ForeignKey("agent_actors.id", ondelete="SET NULL")),
        sa.Column("task_version", sa.Integer(), nullable=False),
        sa.Column("released", sa.JSON(), nullable=False),
        sa.Column("reactivated_at", sa.DateTime(timezone=True)),
        sa.Column("reactivated_to_status", sa.String(16)),
        sa.Column("reactivation_trigger", sa.String(32)),
        sa.Column("reactivation_reason", sa.Text()),
        sa.Column("reactivated_by_principal_id", sa.Integer(), sa.ForeignKey("principals.id", ondelete="SET NULL")),
        sa.Column("reactivated_by_actor_id", sa.Integer(), sa.ForeignKey("agent_actors.id", ondelete="SET NULL")),
        sa.CheckConstraint("from_status IN ('planned', 'active', 'resolved')", name="ck_task_postponements_from_status"),
        sa.CheckConstraint(
            "(reactivated_at IS NULL AND reactivated_to_status IS NULL AND reactivation_trigger IS NULL)"
            " OR (reactivated_at IS NOT NULL AND reactivated_to_status IN ('planned', 'resolved')"
            " AND reactivation_trigger IS NOT NULL)",
            name="ck_task_postponements_reactivation",
        ),
        sqlite_autoincrement=True,
    )
    op.create_index("ix_task_postponements_task_id", "task_postponements", ["task_id"])
    op.create_index("uq_task_postponements_open_task", "task_postponements", ["task_id"], unique=True,
                    sqlite_where=sa.text("reactivated_at IS NULL"), postgresql_where=sa.text("reactivated_at IS NULL"))
    op.create_table(
        "task_reactivation_requirements",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("postponement_id", sa.Integer(), sa.ForeignKey("task_postponements.id", ondelete="CASCADE"),
                  nullable=False),
        sa.Column("task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("kind", sa.String(32), nullable=False),
        sa.Column("target_task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="SET NULL")),
        sa.Column("target_triage_item_id", sa.Integer(), sa.ForeignKey("triage_items.id", ondelete="SET NULL")),
        sa.Column("on_date", sa.Date()),
        sa.Column("description", sa.Text()),
        sa.Column("met_at", sa.DateTime(timezone=True)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "kind IN ('predecessor_accepted', 'date', 'owner_decision', 'linked_resolved')",
            name="ck_task_reactivation_requirements_kind",
        ),
        sa.CheckConstraint(
            "(kind = 'date' AND on_date IS NOT NULL) OR (kind <> 'date' AND on_date IS NULL)",
            name="ck_task_reactivation_requirements_date",
        ),
        sa.CheckConstraint("kind <> 'owner_decision' OR description IS NOT NULL",
                           name="ck_task_reactivation_requirements_decision"),
        sa.CheckConstraint(
            "(target_task_id IS NULL OR kind IN ('predecessor_accepted', 'linked_resolved'))"
            " AND (target_triage_item_id IS NULL OR kind = 'linked_resolved')"
            " AND (target_task_id IS NULL OR target_triage_item_id IS NULL)",
            name="ck_task_reactivation_requirements_target",
        ),
        sqlite_autoincrement=True,
    )
    for column in ("postponement_id", "task_id", "target_task_id", "target_triage_item_id"):
        op.create_index(f"ix_task_reactivation_requirements_{column}", "task_reactivation_requirements", [column])


def downgrade() -> None:
    # An older server knows no postponed status: such a task would match no
    # lifecycle rule and its reactivation requirements would be lost.
    connection = op.get_bind()
    tasks = sa.table("tasks", sa.column("status"))
    postponements = sa.table("task_postponements", sa.column("id"))
    if (connection.scalar(sa.select(sa.literal(1)).select_from(tasks).where(tasks.c.status == "postponed").limit(1))
            or connection.scalar(sa.select(sa.literal(1)).select_from(postponements).limit(1))):
        raise RuntimeError("Postponed tasks or postponement history exist; reactivate and export them before downgrading.")
    for column in ("target_triage_item_id", "target_task_id", "task_id", "postponement_id"):
        op.drop_index(f"ix_task_reactivation_requirements_{column}", table_name="task_reactivation_requirements")
    op.drop_table("task_reactivation_requirements")
    op.drop_index("uq_task_postponements_open_task", table_name="task_postponements")
    op.drop_index("ix_task_postponements_task_id", table_name="task_postponements")
    op.drop_table("task_postponements")
