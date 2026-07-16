"""Add actor assignments, fenced work, and durable idempotency.

Revision ID: 20260711_0028
Revises: 20260709_0027
Create Date: 2026-07-11 00:00:00.000000
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


revision: str = "20260711_0028"
down_revision: str | None = "20260709_0027"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _columns(table_name: str) -> set[str]:
    inspector = sa.inspect(op.get_bind())
    if table_name not in inspector.get_table_names():
        return set()
    return {column["name"] for column in inspector.get_columns(table_name)}


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    tables = set(inspector.get_table_names())

    actor_columns = _columns("agent_actors")
    if actor_columns:
        with op.batch_alter_table("agent_actors") as batch:
            if "role" not in actor_columns:
                batch.add_column(
                    sa.Column("role", sa.String(length=30), server_default="worker", nullable=False)
                )
            if "profile_id" not in actor_columns:
                batch.add_column(sa.Column("profile_id", sa.Integer(), nullable=True))
                batch.create_foreign_key(
                    "fk_agent_actors_profile_id",
                    "team_member_profiles",
                    ["profile_id"],
                    ["id"],
                    ondelete="SET NULL",
                )
                batch.create_index("ix_agent_actors_profile_id", ["profile_id"], unique=False)
            if "work_policy" not in actor_columns:
                batch.add_column(
                    sa.Column(
                        "work_policy",
                        sa.String(length=40),
                        server_default="assigned_only",
                        nullable=False,
                    )
                )
            if "max_parallel_work" not in actor_columns:
                batch.add_column(
                    sa.Column("max_parallel_work", sa.Integer(), server_default="1", nullable=False)
                )
            if "queue_revision" not in actor_columns:
                batch.add_column(
                    sa.Column("queue_revision", sa.Integer(), server_default="1", nullable=False)
                )
        op.execute(
            sa.text(
                "UPDATE agent_actors SET work_policy = 'assigned_only', "
                "max_parallel_work = 1"
            )
        )
        actor_checks = {
            check.get("name")
            for check in sa.inspect(bind).get_check_constraints("agent_actors")
        }
        with op.batch_alter_table("agent_actors") as batch:
            if "ck_agent_actors_supported_work_policy" not in actor_checks:
                batch.create_check_constraint(
                    "ck_agent_actors_supported_work_policy",
                    "work_policy = 'assigned_only'",
                )
            if "ck_agent_actors_supported_parallel_work" not in actor_checks:
                batch.create_check_constraint(
                    "ck_agent_actors_supported_parallel_work",
                    "max_parallel_work = 1",
                )

    profile_columns = _columns("team_member_profiles")
    if profile_columns:
        with op.batch_alter_table("team_member_profiles") as batch:
            if "seed_key" not in profile_columns:
                batch.add_column(sa.Column("seed_key", sa.String(length=120), nullable=True))
                batch.create_index(
                    "ix_team_member_profiles_seed_key", ["seed_key"], unique=True
                )
            if "profile_kind" not in profile_columns:
                batch.add_column(
                    sa.Column(
                        "profile_kind",
                        sa.String(length=30),
                        server_default="human",
                        nullable=False,
                    )
                )
            if "assignment_modes" not in profile_columns:
                batch.add_column(
                    sa.Column(
                        "assignment_modes",
                        sa.JSON(),
                        server_default=sa.text("'[]'"),
                        nullable=False,
                    )
                )

    if "team_member_profile_skills" in tables:
        profile_skill_indexes = {
            index["name"]
            for index in sa.inspect(bind).get_indexes("team_member_profile_skills")
        }
        profile_skill_constraints = {
            constraint["name"]
            for constraint in sa.inspect(bind).get_unique_constraints(
                "team_member_profile_skills"
            )
        }
        if (
            "uq_team_member_profile_skills_profile_skill_key"
            not in profile_skill_indexes | profile_skill_constraints
        ):
            duplicate = bind.execute(
                sa.text(
                    "SELECT profile_id, skill_key FROM team_member_profile_skills "
                    "GROUP BY profile_id, skill_key HAVING COUNT(*) > 1 LIMIT 1"
                )
            ).first()
            if duplicate is not None:
                raise RuntimeError(
                    "Duplicate profile skill keys must be reconciled before upgrade"
                )
            op.create_index(
                "uq_team_member_profile_skills_profile_skill_key",
                "team_member_profile_skills",
                ["profile_id", "skill_key"],
                unique=True,
            )

    task_columns = _columns("tasks")
    if task_columns:
        with op.batch_alter_table("tasks") as batch:
            if "claim_id" not in task_columns:
                batch.add_column(sa.Column("claim_id", sa.String(length=64), nullable=True))
                batch.create_index("ix_tasks_claim_id", ["claim_id"], unique=False)
            if "claim_generation" not in task_columns:
                batch.add_column(
                    sa.Column("claim_generation", sa.Integer(), server_default="0", nullable=False)
                )

    project_update_columns = _columns("project_updates")
    if project_update_columns:
        with op.batch_alter_table("project_updates") as batch:
            if "created_by_actor_id" not in project_update_columns:
                batch.add_column(sa.Column("created_by_actor_id", sa.Integer(), nullable=True))
                batch.create_foreign_key(
                    "fk_project_updates_created_by_actor_id",
                    "agent_actors",
                    ["created_by_actor_id"],
                    ["id"],
                    ondelete="SET NULL",
                )
                batch.create_index(
                    "ix_project_updates_created_by_actor_id",
                    ["created_by_actor_id"],
                    unique=False,
                )
            if "evidence_json" not in project_update_columns:
                batch.add_column(
                    sa.Column(
                        "evidence_json",
                        sa.JSON(),
                        server_default=sa.text("'{}'"),
                        nullable=False,
                    )
                )
            if "correlation_id" not in project_update_columns:
                batch.add_column(sa.Column("correlation_id", sa.String(length=255), nullable=True))
                batch.create_index(
                    "ix_project_updates_correlation_id", ["correlation_id"], unique=False
                )
            if "idempotency_key" not in project_update_columns:
                batch.add_column(sa.Column("idempotency_key", sa.String(length=255), nullable=True))
                batch.create_index(
                    "ix_project_updates_idempotency_key", ["idempotency_key"], unique=False
                )

    if "agent_task_assignments" not in tables:
        op.create_table(
            "agent_task_assignments",
            sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column("task_id", sa.Integer(), nullable=False),
            sa.Column("actor_id", sa.Integer(), nullable=False),
            sa.Column("team_member_id", sa.Integer(), nullable=True),
            sa.Column("purpose", sa.String(length=30), server_default="execution", nullable=False),
            sa.Column("queue_class", sa.String(length=30), server_default="normal", nullable=False),
            sa.Column("state", sa.String(length=30), server_default="queued", nullable=False),
            sa.Column("queue_rank", sa.Integer(), server_default="1000", nullable=False),
            sa.Column("not_before", sa.DateTime(timezone=True), nullable=True),
            sa.Column("assigned_by_actor_id", sa.Integer(), nullable=True),
            sa.Column("reviewer_profile_id", sa.Integer(), nullable=True),
            sa.Column("task_version", sa.Integer(), nullable=False),
            sa.Column("routing_snapshot", sa.Text(), server_default="{}", nullable=False),
            sa.Column("reason", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
            sa.CheckConstraint(
                "purpose IN ('execution', 'verification')",
                name="ck_agent_task_assignments_purpose",
            ),
            sa.CheckConstraint(
                "queue_class IN ('normal', 'rework', 'recovery')",
                name="ck_agent_task_assignments_queue_class",
            ),
            sa.CheckConstraint(
                "state IN ('queued', 'accepted', 'fulfilled', 'cancelled')",
                name="ck_agent_task_assignments_state",
            ),
            sa.ForeignKeyConstraint(["task_id"], ["tasks.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(["actor_id"], ["agent_actors.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(
                ["team_member_id"], ["team_members.id"], ondelete="SET NULL"
            ),
            sa.ForeignKeyConstraint(
                ["assigned_by_actor_id"], ["agent_actors.id"], ondelete="SET NULL"
            ),
            sa.ForeignKeyConstraint(
                ["reviewer_profile_id"], ["team_member_profiles.id"], ondelete="SET NULL"
            ),
        )
        op.create_index(
            "ix_agent_task_assignments_actor_queue",
            "agent_task_assignments",
            ["actor_id", "purpose", "state", "queue_rank"],
        )
        op.create_index(
            "ix_agent_task_assignments_task_state",
            "agent_task_assignments",
            ["task_id", "purpose", "state"],
        )
        op.create_index(
            "ix_agent_task_assignments_actor_id",
            "agent_task_assignments",
            ["actor_id"],
        )
        op.create_index(
            "ix_agent_task_assignments_task_id",
            "agent_task_assignments",
            ["task_id"],
        )
        op.create_index(
            "ix_agent_task_assignments_created_at",
            "agent_task_assignments",
            ["created_at"],
        )

    assignment_indexes = {
        index["name"]
        for index in sa.inspect(bind).get_indexes("agent_task_assignments")
    }
    if "uq_agent_task_assignments_live_purpose" not in assignment_indexes:
        op.create_index(
            "uq_agent_task_assignments_live_purpose",
            "agent_task_assignments",
            ["task_id", "purpose"],
            unique=True,
            sqlite_where=sa.text("state IN ('queued', 'accepted')"),
            postgresql_where=sa.text("state IN ('queued', 'accepted')"),
        )

    if "agent_idempotency_records" not in tables:
        op.create_table(
            "agent_idempotency_records",
            sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
            sa.Column("actor_id", sa.Integer(), nullable=False),
            sa.Column("operation", sa.String(length=100), nullable=False),
            sa.Column("target_type", sa.String(length=50), nullable=False),
            sa.Column("target_id", sa.Integer(), nullable=False),
            sa.Column("idempotency_key", sa.String(length=255), nullable=False),
            sa.Column("request_hash", sa.String(length=64), nullable=False),
            sa.Column("response_payload", sa.Text(), server_default="{}", nullable=False),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
            sa.ForeignKeyConstraint(["actor_id"], ["agent_actors.id"], ondelete="CASCADE"),
            sa.UniqueConstraint(
                "actor_id",
                "operation",
                "target_type",
                "target_id",
                "idempotency_key",
                name="uq_agent_idempotency_operation",
            ),
        )
        op.create_index(
            "ix_agent_idempotency_records_actor_id",
            "agent_idempotency_records",
            ["actor_id"],
        )
        op.create_index(
            "ix_agent_idempotency_records_created_at",
            "agent_idempotency_records",
            ["created_at"],
        )

    run_columns = _columns("agent_runs")
    if run_columns:
        with op.batch_alter_table("agent_runs") as batch:
            if "assignment_id" not in run_columns:
                batch.add_column(sa.Column("assignment_id", sa.Integer(), nullable=True))
                batch.create_foreign_key(
                    "fk_agent_runs_assignment_id",
                    "agent_task_assignments",
                    ["assignment_id"],
                    ["id"],
                    ondelete="SET NULL",
                )
                batch.create_index("ix_agent_runs_assignment_id", ["assignment_id"], unique=False)
            if "claim_generation" not in run_columns:
                batch.add_column(sa.Column("claim_generation", sa.Integer(), nullable=True))
            if "heartbeat_at" not in run_columns:
                batch.add_column(sa.Column("heartbeat_at", sa.DateTime(timezone=True), nullable=True))

        run_indexes = {
            index["name"] for index in sa.inspect(bind).get_indexes("agent_runs")
        }
        if "uq_agent_runs_running_assignment" not in run_indexes:
            op.create_index(
                "uq_agent_runs_running_assignment",
                "agent_runs",
                ["assignment_id"],
                unique=True,
                sqlite_where=sa.text(
                    "assignment_id IS NOT NULL AND status = 'running'"
                ),
                postgresql_where=sa.text(
                    "assignment_id IS NOT NULL AND status = 'running'"
                ),
            )

    event_columns = _columns("agent_run_events")
    if event_columns:
        with op.batch_alter_table("agent_run_events") as batch:
            if "correlation_id" not in event_columns:
                batch.add_column(sa.Column("correlation_id", sa.String(length=255), nullable=True))
                batch.create_index(
                    "ix_agent_run_events_correlation_id", ["correlation_id"], unique=False
                )
            if "idempotency_key" not in event_columns:
                batch.add_column(sa.Column("idempotency_key", sa.String(length=255), nullable=True))
        op.execute(
            sa.text(
                "UPDATE agent_run_events SET idempotency_key = NULL "
                "WHERE idempotency_key IS NOT NULL AND id NOT IN "
                "(SELECT MIN(id) FROM agent_run_events "
                "WHERE idempotency_key IS NOT NULL GROUP BY run_id, idempotency_key)"
            )
        )
        event_indexes = {
            index["name"]
            for index in sa.inspect(bind).get_indexes("agent_run_events")
        }
        if "uq_agent_run_events_run_id_idempotency_key" not in event_indexes:
            op.create_index(
                "uq_agent_run_events_run_id_idempotency_key",
                "agent_run_events",
                ["run_id", "idempotency_key"],
                unique=True,
                sqlite_where=sa.text("idempotency_key IS NOT NULL"),
                postgresql_where=sa.text("idempotency_key IS NOT NULL"),
            )

    task_event_indexes = {
        index["name"] for index in sa.inspect(bind).get_indexes("task_events")
    }
    if "uq_task_events_agent_idempotency_key" not in task_event_indexes:
        op.execute(
            sa.text(
                "UPDATE task_events SET idempotency_key = NULL "
                "WHERE idempotency_key IS NOT NULL AND actor_id IS NOT NULL "
                "AND task_id IS NOT NULL AND id NOT IN "
                "(SELECT MIN(id) FROM task_events WHERE idempotency_key IS NOT NULL "
                "AND actor_id IS NOT NULL AND task_id IS NOT NULL "
                "GROUP BY task_id, actor_id, event_type, idempotency_key)"
            )
        )
        op.create_index(
            "uq_task_events_agent_idempotency_key",
            "task_events",
            ["task_id", "actor_id", "event_type", "idempotency_key"],
            unique=True,
            sqlite_where=sa.text(
                "idempotency_key IS NOT NULL AND actor_id IS NOT NULL "
                "AND task_id IS NOT NULL"
            ),
            postgresql_where=sa.text(
                "idempotency_key IS NOT NULL AND actor_id IS NOT NULL "
                "AND task_id IS NOT NULL"
            ),
        )


def downgrade() -> None:
    bind = op.get_bind()
    tables = set(sa.inspect(bind).get_table_names())
    if "task_events" in tables:
        task_event_indexes = {
            index["name"] for index in sa.inspect(bind).get_indexes("task_events")
        }
        if "uq_task_events_agent_idempotency_key" in task_event_indexes:
            op.drop_index(
                "uq_task_events_agent_idempotency_key", table_name="task_events"
            )
    if "team_member_profile_skills" in tables:
        profile_skill_indexes = {
            index["name"]
            for index in sa.inspect(bind).get_indexes("team_member_profile_skills")
        }
        if "uq_team_member_profile_skills_profile_skill_key" in profile_skill_indexes:
            op.drop_index(
                "uq_team_member_profile_skills_profile_skill_key",
                table_name="team_member_profile_skills",
            )
    event_columns = _columns("agent_run_events")
    if event_columns:
        event_indexes = {
            index["name"]
            for index in sa.inspect(bind).get_indexes("agent_run_events")
        }
        if "uq_agent_run_events_run_id_idempotency_key" in event_indexes:
            op.drop_index(
                "uq_agent_run_events_run_id_idempotency_key",
                table_name="agent_run_events",
            )
        with op.batch_alter_table("agent_run_events") as batch:
            if "idempotency_key" in event_columns:
                batch.drop_column("idempotency_key")
            if "correlation_id" in event_columns:
                batch.drop_index("ix_agent_run_events_correlation_id")
                batch.drop_column("correlation_id")

    run_columns = _columns("agent_runs")
    if run_columns:
        run_indexes = {
            index["name"] for index in sa.inspect(bind).get_indexes("agent_runs")
        }
        if "uq_agent_runs_running_assignment" in run_indexes:
            op.drop_index(
                "uq_agent_runs_running_assignment", table_name="agent_runs"
            )
        with op.batch_alter_table("agent_runs") as batch:
            if "heartbeat_at" in run_columns:
                batch.drop_column("heartbeat_at")
            if "claim_generation" in run_columns:
                batch.drop_column("claim_generation")
            if "assignment_id" in run_columns:
                batch.drop_index("ix_agent_runs_assignment_id")
                batch.drop_constraint("fk_agent_runs_assignment_id", type_="foreignkey")
                batch.drop_column("assignment_id")

    inspector = sa.inspect(op.get_bind())
    tables = set(inspector.get_table_names())
    if "agent_idempotency_records" in tables:
        op.drop_table("agent_idempotency_records")
    if "agent_task_assignments" in tables:
        op.drop_table("agent_task_assignments")

    project_update_columns = _columns("project_updates")
    if project_update_columns:
        with op.batch_alter_table("project_updates") as batch:
            if "idempotency_key" in project_update_columns:
                batch.drop_index("ix_project_updates_idempotency_key")
                batch.drop_column("idempotency_key")
            if "correlation_id" in project_update_columns:
                batch.drop_index("ix_project_updates_correlation_id")
                batch.drop_column("correlation_id")
            if "evidence_json" in project_update_columns:
                batch.drop_column("evidence_json")
            if "created_by_actor_id" in project_update_columns:
                batch.drop_index("ix_project_updates_created_by_actor_id")
                batch.drop_constraint(
                    "fk_project_updates_created_by_actor_id", type_="foreignkey"
                )
                batch.drop_column("created_by_actor_id")

    task_columns = _columns("tasks")
    if task_columns:
        with op.batch_alter_table("tasks") as batch:
            if "claim_generation" in task_columns:
                batch.drop_column("claim_generation")
            if "claim_id" in task_columns:
                batch.drop_index("ix_tasks_claim_id")
                batch.drop_column("claim_id")

    actor_columns = _columns("agent_actors")
    if actor_columns:
        with op.batch_alter_table("agent_actors") as batch:
            actor_checks = {
                check.get("name")
                for check in sa.inspect(bind).get_check_constraints("agent_actors")
            }
            if "ck_agent_actors_supported_parallel_work" in actor_checks:
                batch.drop_constraint(
                    "ck_agent_actors_supported_parallel_work", type_="check"
                )
            if "ck_agent_actors_supported_work_policy" in actor_checks:
                batch.drop_constraint(
                    "ck_agent_actors_supported_work_policy", type_="check"
                )
            for column_name in (
                "queue_revision",
                "max_parallel_work",
                "work_policy",
            ):
                if column_name in actor_columns:
                    batch.drop_column(column_name)
            if "profile_id" in actor_columns:
                batch.drop_index("ix_agent_actors_profile_id")
                batch.drop_constraint("fk_agent_actors_profile_id", type_="foreignkey")
                batch.drop_column("profile_id")
            if "role" in actor_columns:
                batch.drop_column("role")

    profile_columns = _columns("team_member_profiles")
    if profile_columns:
        with op.batch_alter_table("team_member_profiles") as batch:
            if "assignment_modes" in profile_columns:
                batch.drop_column("assignment_modes")
            if "profile_kind" in profile_columns:
                batch.drop_column("profile_kind")
            if "seed_key" in profile_columns:
                batch.drop_index("ix_team_member_profiles_seed_key")
                batch.drop_column("seed_key")
