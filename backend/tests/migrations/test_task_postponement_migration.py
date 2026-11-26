"""Task postponement migrates a populated database unchanged, and never loses postponed work on rollback."""

from datetime import date, datetime, timezone

import pytest
from alembic import command
from sqlalchemy import create_engine, event, inspect, select
from sqlalchemy.exc import IntegrityError

from app.models.agent import AgentActor, AgentRun, AgentTaskAssignment
from app.models.project import Project
from app.models.task import Task, TaskDependency
from app.models.task_postponement import TaskPostponement, TaskReactivationRequirement
from app.models.task_status_log import TaskStatusLog
from app.services.upgrade_service import alembic_config

PREVIOUS, CURRENT = "20261124_0024", "20261126_0025"
AT = datetime(2026, 11, 26, tzinfo=timezone.utc)


def _populate(db):
    """Tasks in every prior status, with dependencies, history and agent execution."""
    tasks = Task.__table__
    project = db.execute(Project.__table__.insert().values(name="Kernel")).inserted_primary_key[0]
    ids = {}
    for status in ("planned", "active", "resolved", "closed"):
        ids[status] = db.execute(tasks.insert().values(
            title=f"{status.title()} work", project_id=project, status=status, version=4, priority=3,
            progress={"criteria": [{"criterion_id": "a", "state": "completed", "evidence": "kept"}]},
            brief={"schema_version": 1, "goal": "Keep me"}, start_date=date(2026, 11, 2), end_date=date(2026, 11, 6),
        )).inserted_primary_key[0]
    db.execute(TaskDependency.__table__.insert().values(task_id=ids["planned"], depends_on_id=ids["active"]))
    db.execute(TaskStatusLog.__table__.insert().values(task_id=ids["active"], from_status="planned", to_status="active",
                                                       changed_at=AT, triggered_by="user"))
    actor = db.execute(AgentActor.__table__.insert().values(
        name="kernel-worker", display_name="Worker", role="worker", api_key_hash="0" * 64, scopes="[]",
    )).inserted_primary_key[0]
    assignment = db.execute(AgentTaskAssignment.__table__.insert().values(
        task_id=ids["active"], actor_id=actor, purpose="execution", queue_class="normal", state="accepted", task_version=4,
    )).inserted_primary_key[0]
    db.execute(AgentRun.__table__.insert().values(task_id=ids["active"], actor_id=actor, assignment_id=assignment,
                                                  status="running", started_at=AT,
                                                  execution_provenance={"source": "authenticated_work_begin"}))
    return project, ids


def _rows(db):
    return {table.name: [tuple(row) for row in db.execute(select(table).order_by(table.c.id))]
            for table in (Task.__table__, TaskDependency.__table__, TaskStatusLog.__table__,
                          AgentTaskAssignment.__table__, AgentRun.__table__)}


@pytest.mark.parametrize(
    "dialect",
    [
        pytest.param("sqlite", marks=pytest.mark.sqlite),
        pytest.param(
            "postgresql", marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network]
        ),
    ],
)
def test_postponement_migration_upgrades_populated_data_and_refuses_losing_postponed_work(
    dialect, request, tmp_path, configure_database
):
    if dialect == "postgresql":
        url = request.getfixturevalue("postgres_database").url
        configure_database(url)
    else:
        path = tmp_path / "workchord_test_task_postponement_upgrade.db"
        configure_database(f"sqlite+aiosqlite:///{path}")
        url = f"sqlite:///{path}"
    engine = create_engine(url)
    if dialect == "sqlite":
        # Enforce foreign keys as the application's own SQLite connections do.
        event.listen(engine, "connect", lambda connection, _record: connection.execute("PRAGMA foreign_keys=ON"))
    postponements, requirements, tasks = TaskPostponement.__table__, TaskReactivationRequirement.__table__, Task.__table__
    try:
        with engine.connect() as db:
            config = alembic_config(connection=db)
            command.upgrade(config, PREVIOUS)
            project, ids = _populate(db)
            db.commit()
            retained = _rows(db)
            for attempt in range(2):
                command.upgrade(config, CURRENT)
                # Every existing row, status and execution record is kept as it was.
                assert _rows(db) == retained
                assert db.execute(select(postponements)).all() == [] and db.execute(select(requirements)).all() == []
                checks = {check["name"] for check in inspect(db).get_check_constraints("task_reactivation_requirements")}
                assert {"ck_task_reactivation_requirements_kind", "ck_task_reactivation_requirements_date",
                        "ck_task_reactivation_requirements_decision", "ck_task_reactivation_requirements_target"} <= checks

                db.execute(tasks.update().where(tasks.c.id == ids["active"]).values(status="postponed"))
                target = db.execute(tasks.insert().values(title="Vendor contract", project_id=project, version=1)).inserted_primary_key[0]
                record = dict(task_id=ids["active"], from_status="active", reason="Waiting on the vendor", postponed_at=AT,
                              task_version=5, released={"run_ids": [], "assignment_ids": []})
                postponement = db.execute(postponements.insert().values(**record)).inserted_primary_key[0]
                requirement = db.execute(requirements.insert().values(
                    postponement_id=postponement, task_id=ids["active"], position=0, kind="predecessor_accepted",
                    target_task_id=target, created_at=AT)).inserted_primary_key[0]
                db.commit()
                # One open postponement per task.
                with pytest.raises(IntegrityError):
                    db.execute(postponements.insert().values(**record))
                db.rollback()
                # A requirement's shape follows its kind.
                for invalid in (dict(kind="soon"), dict(kind="date"), dict(kind="owner_decision"),
                                dict(kind="date", on_date=date(2026, 12, 1), target_task_id=ids["closed"]),
                                dict(kind="owner_decision", description="Decide", target_task_id=ids["closed"])):
                    with pytest.raises(IntegrityError):
                        db.execute(requirements.insert().values(postponement_id=postponement, task_id=ids["active"],
                                                                position=1, created_at=AT, **invalid))
                    db.rollback()
                # A deleted target leaves the requirement readable with no target.
                db.execute(tasks.delete().where(tasks.c.id == target))
                db.commit()
                assert db.execute(select(requirements.c.kind, requirements.c.target_task_id)
                                  .where(requirements.c.id == requirement)).one() == ("predecessor_accepted", None)
                with pytest.raises(RuntimeError, match="before downgrading"):
                    command.downgrade(config, PREVIOUS)
                db.rollback()
                assert len(db.execute(select(postponements)).all()) == 1
                db.execute(requirements.delete())
                db.execute(postponements.delete())
                db.commit()
                # A postponed status alone also blocks rollback.
                with pytest.raises(RuntimeError, match="before downgrading"):
                    command.downgrade(config, PREVIOUS)
                db.rollback()
                db.execute(tasks.update().where(tasks.c.id == ids["active"]).values(status="active"))
                db.commit()
                retained = _rows(db)
                if attempt == 0:
                    command.downgrade(config, PREVIOUS)
                    assert not inspect(db).has_table("task_postponements")
                    assert not inspect(db).has_table("task_reactivation_requirements")
                    assert _rows(db) == retained
                    db.commit()
    finally:
        engine.dispose()
