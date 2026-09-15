"""Expand task ownership, backlog, effort and canonical brief history.

SQLite rebuilds with foreign keys disabled inside an explicit transaction, then
checks every foreign key before committing. Re-entry after schema application is
safe; each backfilled row carries its own completion marker.
"""

import json

from alembic import op
import sqlalchemy as sa

from app.utils.time import UTCDateTime

revision = "20260915_0038"
down_revision = "20260915_0037"
branch_labels = None
depends_on = None


def backfill_tasks(connection, *, after_id=0, limit=500, apply=True):
    """Return bounded diagnostics; apply each legacy row at most once."""
    metadata = sa.MetaData()
    tasks = sa.Table("tasks", metadata, autoload_with=connection)
    members = sa.Table("team_members", metadata, autoload_with=connection)
    profiles = sa.Table("team_member_profiles", metadata, autoload_with=connection)
    rows = connection.execute(sa.select(tasks).where(tasks.c.id > after_id, tasks.c.domain_backfill_version == 0).order_by(tasks.c.id).limit(limit)).mappings().all()
    results = []
    for task in rows:
        issues = []
        values = {"domain_backfill_version": 1, "legacy_estimate": {"effort_days": task["effort_days"], "effort_hours": task["effort_hours"]}}
        owner = connection.execute(sa.select(profiles.c.id, profiles.c.profile_kind).join(members, members.c.profile_id == profiles.c.id).where(members.c.id == task["assignee_id"])).first() if task["assignee_id"] else None
        if owner and owner.profile_kind == "human":
            values.update(owner_profile_id=owner.id, ownership_provenance="legacy_capacity_link")
        elif task["assignee_id"]:
            issues.append("capacity_has_no_unambiguous_human_profile")
            values["ownership_provenance"] = "legacy_unlinked"
        if task["effort_days"] == 1 and task["effort_hours"] == 8:
            values.update(effort_days=None, effort_hours=None, estimate_provenance="unknown")
            issues.append("legacy_default_estimate_preserved_as_unknown")
        elif task["effort_hours"] is not None:
            hours = task["effort_hours"]
            if hours < 0:
                values.update(effort_days=None, effort_hours=None, estimate_provenance="unknown")
                issues.append("invalid_legacy_estimate_preserved")
            else:
                values.update(effort_days=hours / 8, estimate_provenance="assumed")
                if task["effort_days"] is not None and abs(task["effort_days"] * 8 - hours) > 0.000001:
                    issues.append("legacy_units_disagreed_hours_retained")
        elif task["effort_days"] is not None and task["effort_days"] >= 0:
            values.update(effort_hours=task["effort_days"] * 8, estimate_provenance="assumed")
        else:
            values.update(effort_days=None, effort_hours=None, estimate_provenance="unknown")
        if task["is_summary"]:
            values.update(effort_days=0, effort_hours=0, estimate_provenance="assumed")
        values["domain_migration_notes"] = issues
        if apply:
            connection.execute(tasks.update().where(tasks.c.id == task["id"], tasks.c.domain_backfill_version == 0).values(**values))
        results.append({"task_id": task["id"], "issues": issues})
    return results


def _expand():
    connection = op.get_bind()
    existing = {item["name"] for item in sa.inspect(connection).get_columns("tasks")}
    columns = [
        sa.Column("owner_profile_id", sa.Integer(), nullable=True),
        sa.Column("ownership_provenance", sa.String(32), nullable=False, server_default="unassigned"),
        sa.Column("nominal_day_hours", sa.Float(), nullable=False, server_default="8"),
        sa.Column("estimate_provenance", sa.String(32), nullable=False, server_default="unknown"),
        sa.Column("legacy_estimate", sa.JSON(), nullable=True),
        sa.Column("blocked_reason", sa.Text(), nullable=True),
        sa.Column("canceled_at", UTCDateTime(), nullable=True),
        sa.Column("canceled_reason", sa.Text(), nullable=True),
        sa.Column("canceled_by_principal_id", sa.Integer(), nullable=True),
        sa.Column("execution_mode", sa.String(16), nullable=False, server_default="scheduled"),
        sa.Column("brief", sa.JSON(), nullable=True),
        sa.Column("brief_revision", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("brief_provenance", sa.String(32), nullable=False, server_default="legacy_text"),
        sa.Column("legacy_description", sa.Text(), nullable=True),
        sa.Column("brief_migration_notes", sa.JSON(), nullable=True),
        sa.Column("artifact_revision", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("progress", sa.JSON(), nullable=True),
        sa.Column("domain_backfill_version", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("domain_migration_notes", sa.JSON(), nullable=True),
    ]
    for column in columns:
        if column.name not in existing:
            op.add_column("tasks", column)
    if "nominal_day_hours" not in {item["name"] for item in sa.inspect(connection).get_columns("calendars")}:
        op.add_column("calendars", sa.Column("nominal_day_hours", sa.Float(), nullable=False, server_default="8"))

    reflected = sa.Table("tasks", sa.MetaData(), autoload_with=connection)
    if connection.dialect.name == "sqlite":
        actions = {row[3]: row[6] for row in connection.exec_driver_sql("PRAGMA foreign_key_list(tasks)")}
        for constraint in reflected.foreign_key_constraints:
            if len(constraint.columns) == 1:
                action = actions.get(next(iter(constraint.columns)).name)
                if action and action != "NO ACTION":
                    constraint.ondelete = action
    checks = {item["name"] for item in sa.inspect(connection).get_check_constraints("tasks")}
    fks = {tuple(item["constrained_columns"]) for item in sa.inspect(connection).get_foreign_keys("tasks")}
    nullable = {item["name"]: item["nullable"] for item in sa.inspect(connection).get_columns("tasks")}
    needs_rebuild = not all(nullable[name] for name in ("iteration_id", "effort_days", "effort_hours")) or ("owner_profile_id",) not in fks
    if needs_rebuild:
        with op.batch_alter_table("tasks", copy_from=reflected, table_kwargs={"sqlite_autoincrement": True}, naming_convention={"fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s"}) as batch:
            for name in ("iteration_id", "effort_days", "effort_hours"):
                batch.alter_column(name, existing_type=sa.Integer() if name == "iteration_id" else sa.Float(), nullable=True)
            for name, target in (("owner_profile_id", "team_member_profiles"), ("canceled_by_principal_id", "principals")):
                if (name,) not in fks:
                    batch.create_foreign_key(f"fk_tasks_{name}_{target}", target, [name], ["id"], ondelete="RESTRICT")
            for name, sql in (("ck_tasks_work_scope", "iteration_id IS NOT NULL OR project_id IS NOT NULL"),
                              ("ck_tasks_nominal_day_hours", "nominal_day_hours > 0 AND nominal_day_hours <= 24")):
                if name not in checks:
                    batch.create_check_constraint(name, sql)
    indexes = {item["name"] for item in sa.inspect(connection).get_indexes("tasks")}
    if "ix_tasks_owner_profile_id" not in indexes:
        op.create_index("ix_tasks_owner_profile_id", "tasks", ["owner_profile_id"])
    table_names = set(sa.inspect(connection).get_table_names())
    for name, fields, unique in (
        ("task_brief_revisions", [sa.Column("revision", sa.Integer(), nullable=False), sa.Column("payload", sa.JSON(), nullable=False), sa.Column("provenance", sa.String(32), nullable=False)], ("revision", "uq_task_brief_revision")),
        ("task_progress_records", [sa.Column("brief_revision", sa.Integer(), nullable=False), sa.Column("artifact_revision", sa.Integer(), nullable=False), sa.Column("payload", sa.JSON(), nullable=False)], ("artifact_revision", "uq_task_progress_revision")),
        ("task_review_records", [sa.Column("brief_revision", sa.Integer(), nullable=False), sa.Column("artifact_revision", sa.Integer(), nullable=False), sa.Column("verdict", sa.String(16), nullable=False), sa.Column("reason", sa.Text(), nullable=False), sa.Column("evidence", sa.Text(), nullable=False)], None),
    ):
        if name in table_names:
            continue
        op.create_table(name, sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("task_id", sa.Integer(), sa.ForeignKey("tasks.id", ondelete="SET NULL"), nullable=True),
            sa.Column("original_task_id", sa.Integer(), nullable=False),
            sa.Column("task_version", sa.Integer(), nullable=False),
            sa.Column("principal_id", sa.Integer(), sa.ForeignKey("principals.id", ondelete="RESTRICT"), nullable=True),
            sa.Column("created_at", UTCDateTime(), nullable=False), *fields,
            *([sa.UniqueConstraint("original_task_id", unique[0], name=unique[1])] if unique else []))
        op.create_index(f"ix_{name}_task_id", name, ["task_id"])
        op.create_index(f"ix_{name}_original_task_id", name, ["original_task_id"])
    package_columns = {column["name"] for column in sa.inspect(connection).get_columns("agent_work_packages")}
    for name in ("task_context_version", "task_brief_revision", "task_artifact_revision", "task_brief_digest"):
        if name not in package_columns:
            op.add_column("agent_work_packages", sa.Column(name, sa.String(64) if name.endswith("digest") else sa.Integer(), nullable=True))
    snapshot_columns = {column["name"] for column in sa.inspect(connection).get_columns("application_snapshots")}
    if "project_id" not in snapshot_columns:
        with op.batch_alter_table("application_snapshots") as batch:
            batch.add_column(sa.Column("project_id", sa.Integer(), nullable=True))
            batch.alter_column("iteration_id", existing_type=sa.Integer(), nullable=True)
            batch.create_foreign_key("fk_application_snapshots_project_id_projects", "projects", ["project_id"], ["id"], ondelete="CASCADE")
            batch.create_unique_constraint("uq_application_snapshot_project_filename", ["project_id", "filename"])
            batch.create_check_constraint("ck_application_snapshot_scope", "iteration_id IS NOT NULL OR project_id IS NOT NULL")
            batch.create_index("ix_application_snapshots_project_id", ["project_id"])
    after = 0
    while rows := backfill_tasks(connection, after_id=after):
        after = rows[-1]["task_id"]
    checks = {item["name"] for item in sa.inspect(connection).get_check_constraints("tasks")}
    if "ck_tasks_effort_hours" not in checks:
        # Legacy invalid values are quarantined before installing the constraint.
        reflected = sa.Table("tasks", sa.MetaData(), autoload_with=connection)
        if connection.dialect.name == "sqlite":
            actions = {row[3]: row[6] for row in connection.exec_driver_sql("PRAGMA foreign_key_list(tasks)")}
            for constraint in reflected.foreign_key_constraints:
                action = actions.get(next(iter(constraint.columns)).name)
                if action and action != "NO ACTION":
                    constraint.ondelete = action
        with op.batch_alter_table("tasks", copy_from=reflected, table_kwargs={"sqlite_autoincrement": True}) as batch:
            batch.create_check_constraint("ck_tasks_effort_hours", "effort_hours IS NULL OR effort_hours >= 0")


def upgrade():
    connection = op.get_bind()
    if connection.dialect.name != "sqlite":
        _expand()
        return
    with op.get_context().autocommit_block():
        connection.exec_driver_sql("PRAGMA foreign_keys=OFF")
        connection.exec_driver_sql("BEGIN IMMEDIATE")
        try:
            _expand()
            if connection.exec_driver_sql("PRAGMA foreign_key_check").first() is not None:
                raise RuntimeError("Foreign key validation failed; task migration rolled back")
            connection.exec_driver_sql("COMMIT")
        except BaseException:
            connection.exec_driver_sql("ROLLBACK")
            raise
        finally:
            connection.exec_driver_sql("PRAGMA foreign_keys=ON")


def downgrade():
    raise RuntimeError("Canonical work history cannot be downcast safely. Restore a complete backup with the matching application image.")
