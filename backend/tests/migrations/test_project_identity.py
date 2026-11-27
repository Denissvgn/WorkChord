"""Project allocation floors, dependent preservation and transactional rebuilds."""

from datetime import UTC, datetime
import sqlite3
from uuid import uuid4

from alembic import command
import pytest
from sqlalchemy import MetaData, Table, create_engine, event, text
from sqlalchemy.engine import Engine

from app.models.calendar import Calendar
from app.models.identity import CommandAudit, Principal, ProjectMembership
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.task import Task
from app.models.time_entry import TimeEntry, TimeEntryRevision
from app.services.upgrade_service import alembic_config, run_alembic_upgrade
from tests.support import schema_snapshot


def legacy_store(tmp_path, configure_database):
    path = tmp_path / "project-identity.db"
    configure_database(f"sqlite+aiosqlite:///{path}")
    engine = create_engine(f"sqlite:///{path}")
    with engine.connect() as db:
        command.upgrade(alembic_config(connection=db), "20261007_0008")
    return path, engine


def insert_legacy_project(db, **values):
    """Insert through the reflected legacy table so newer ORM columns stay out."""
    legacy = Table("projects", MetaData(), autoload_with=db)
    row = {}
    for column in Project.__table__.columns:
        if column.name not in legacy.c or column.default is None:
            continue
        default = column.default
        row[column.name] = default.arg(None) if default.is_callable else default.arg
    row.update(values)
    return db.execute(legacy.insert().values(**row))


def retained_entry(db, project_id):
    values = dict(project_id=project_id, task_id=None, principal_id=1, work_date=datetime(2026, 1, 1).date(),
        timezone="UTC", minutes=90, note="Retained private evidence", version=1, voided=False)
    result = db.execute(TimeEntry.__table__.insert().values(**values, request_id=str(uuid4()), creation_digest="a" * 64))
    db.execute(TimeEntryRevision.__table__.insert().values(**{key: value for key, value in values.items() if key != "task_id"},
        entry_id=result.inserted_primary_key[0], reason="Recorded"))


def seed_dependents(db):
    db.execute(Principal.__table__.insert().values(id=1, kind="human", display_name="Owner"))
    insert_legacy_project(db, id=5, name="Current project")
    db.execute(Calendar.__table__.insert().values(id=1, name="Calendar", year=2026))
    db.execute(Iteration.__table__.insert().values(id=1, name="Iteration", calendar_id=1, project_id=5,
        start_date=datetime(2026, 1, 1).date(), end_date=datetime(2026, 1, 31).date()))
    db.execute(Task.__table__.insert().values(id=1, title="Deliverable", project_id=5, iteration_id=1))
    db.execute(ProjectMembership.__table__.insert().values(principal_id=1, project_id=5, role="manager"))
    db.execute(CommandAudit.__table__.insert().values(principal_id=1, project_id=5, action="projects:edit",
        source="rest", correlation_id="creation", details={"entity_id": 5}))
    retained_entry(db, 90)


def database_rows(engine):
    catalog = schema_snapshot(engine)
    with engine.connect() as db:
        return {name: [dict(row._mapping) for row in db.execute(text(f'SELECT * FROM "{name}"'))]
                for name in sorted(catalog) if name != "alembic_version"}


# Columns later revisions add, with the value every retained row receives.
LATER_COLUMNS = {
    "projects": {"require_different_review_publisher": 0, "routing_conflict_mode": "refuse"},
    "agent_model_catalog_entries": {"local_first": 0, "effort": "unknown", "qualification_keys": "[]"},
    "tasks": {"execution_planning_window": None},
    "task_review_records": {"kind": "review"},
}


@pytest.mark.sqlite
@pytest.mark.parametrize("empty_projects", [False, True])
def test_upgrade_preserves_dependents_and_retained_allocation_floor(tmp_path, configure_database, empty_projects):
    path, engine = legacy_store(tmp_path, configure_database)
    try:
        with engine.begin() as db:
            if empty_projects:
                retained_entry(db, 90)
            else:
                seed_dependents(db)
        before_rows, before_catalog = database_rows(engine), schema_snapshot(engine)
        run_alembic_upgrade(backup=False, run_repairs=False)
        after_rows = database_rows(engine)
        assert after_rows.pop("agent_runtime_observations") == []
        for table in ("iteration_annual_calendars", "profile_annual_calendars",
                      "maintenance_windows", "maintenance_window_receipts"):
            assert after_rows.pop(table) == []
        assert after_rows.pop("team_member_capacity_adjustments") == []
        assert after_rows.pop("task_replacements") == []
        for table in ("task_postponements", "task_reactivation_requirements"):
            assert after_rows.pop(table) == []
        for table in ("routing_qualification_keys", "routing_qualification_key_revisions",
                      "routing_calibration_contracts", "routing_calibration_contract_revisions"):
            assert after_rows.pop(table) == []
        for table, columns in LATER_COLUMNS.items():
            for row in after_rows[table]:
                for column, value in columns.items():
                    assert row.pop(column) == value
        assert after_rows == before_rows
        after_catalog = schema_snapshot(engine)
        allocation = after_catalog["team_members"]
        assert allocation["columns"].pop("allocation_token") == {"type": {"family": "text"}, "nullable": False}
        allocation["unique_constraints"].remove(("allocation_token",))
        profiles = after_catalog["team_member_profiles"]
        assert profiles["columns"].pop("profile_token") == {"type": {"family": "text"}, "nullable": False}
        profiles["unique_constraints"].remove(("profile_token",))
        # Later revisions: the profile a trusted-local session works as, and comments it writes.
        assert after_catalog["user_sessions"]["columns"].pop("local_profile_id") == {"type": {"family": "integer"}, "nullable": True}
        for table in ("task_comments", "task_comment_revisions"):
            comments = after_catalog[table]["columns"]
            assert comments.pop("author_profile_id") == {"type": {"family": "integer"}, "nullable": True}
            assert comments["principal_id"]["nullable"] is True
            comments["principal_id"]["nullable"] = False
        # The access level and label of a session, and of the pairing request that issued it.
        for table, column in (("user_sessions", "access"), ("native_connections", "requested_access")):
            rebuilt = after_catalog[table]
            assert rebuilt["columns"].pop(column) == {"type": {"family": "text"}, "nullable": False}
            assert rebuilt["columns"].pop("client_label") == {"type": {"family": "text"}, "nullable": True}
            rebuilt["checks"].remove(f"ck_{table}_{column}")
        # A later revision keeps a run's declared harness session in searchable columns.
        runs = after_catalog["agent_runs"]
        for column in ("harness_kind", "harness_session_id"):
            assert runs["columns"].pop(column) == {"type": {"family": "text"}, "nullable": True}
        runs["indexes"].remove(("ix_agent_runs_harness_session_id", ("harness_session_id",), False))
        # Later revisions record review provenance and the execution planning window.
        assert runs["columns"].pop("execution_provenance") == {"type": {"family": "json"}, "nullable": True}
        assert after_catalog["agent_task_assignments"]["columns"].pop("review_selection") == {"type": {"family": "json"}, "nullable": True}
        assert after_catalog["agent_model_catalog_entries"]["columns"].pop("publisher_key") == {"type": {"family": "text"}, "nullable": True}
        assert after_catalog["agent_model_catalog_entries"]["columns"].pop("local_first") == {"type": {"family": "boolean"}, "nullable": False}
        assert after_catalog["agent_model_catalog_entries"]["columns"].pop("effort") == {"type": {"family": "text"}, "nullable": False}
        after_catalog["agent_model_catalog_entries"]["checks"].remove("ck_agent_model_catalog_effort")
        assert after_catalog["agent_model_catalog_entries"]["columns"].pop("qualification_keys") == {"type": {"family": "json"}, "nullable": False}
        # A later revision keeps the deployment's declared qualification keys.
        assert "ck_routing_qualification_keys_state" in after_catalog.pop("routing_qualification_keys")["checks"]
        assert "ck_routing_qualification_key_revisions_action" in after_catalog.pop(
            "routing_qualification_key_revisions")["checks"]
        # A later revision keeps the deployment's calibration contracts.
        assert "ck_routing_calibration_contracts_approval" in after_catalog.pop("routing_calibration_contracts")["checks"]
        assert "ck_routing_calibration_contract_revisions_action" in after_catalog.pop(
            "routing_calibration_contract_revisions")["checks"]
        assert after_catalog["projects"]["columns"].pop("require_different_review_publisher") == {"type": {"family": "boolean"}, "nullable": False}
        # A later revision lets a project refuse or only warn about inconsistent task routing.
        assert after_catalog["projects"]["columns"].pop("routing_conflict_mode") == {"type": {"family": "text"}, "nullable": False}
        after_catalog["projects"]["checks"].remove("ck_projects_routing_conflict_mode")
        assert after_catalog["tasks"]["columns"].pop("execution_planning_window") == {"type": {"family": "json"}, "nullable": True}
        # A later revision records which annual calendars an iteration or profile spans.
        for table in ("iteration_annual_calendars", "profile_annual_calendars"):
            assert after_catalog.pop(table)["columns"]["calendar_id"]["nullable"] is False
        # A later revision records coordinated maintenance windows and their receipts.
        assert "ck_maintenance_windows_state" in after_catalog.pop("maintenance_windows")["checks"]
        assert "ck_maintenance_window_receipts_kind" in after_catalog.pop("maintenance_window_receipts")["checks"]
        # A later revision adds the advisory runtime observation table.
        assert after_catalog.pop("agent_runtime_observations")["checks"] == ["ck_agent_runtime_observations_kind"]
        # A later revision records dated adjustments on capacity rows.
        assert after_catalog.pop("team_member_capacity_adjustments")["checks"] == [
            "ck_team_member_capacity_adjustments_dates", "ck_team_member_capacity_adjustments_percent"]
        # A later revision records audited clean-replacement dispositions, and a later one supersessions.
        assert after_catalog.pop("task_replacements")["checks"] == [
            "ck_task_replacements_disposition", "ck_task_replacements_distinct", "ck_task_replacements_replacement_basis"]
        # A later revision lets a delivery prerequisite name the branch its code must merge on.
        assert after_catalog["delivery_dependencies"]["columns"].pop("target_branch") == {"type": {"family": "text"}, "nullable": True}
        # A later revision tells an owner's override acceptance apart from an ordinary review.
        assert after_catalog["task_review_records"]["columns"].pop("kind") == {"type": {"family": "text"}, "nullable": False}
        # A later revision records postponed tasks and their reactivation requirements.
        assert after_catalog.pop("task_postponements")["checks"] == [
            "ck_task_postponements_from_status", "ck_task_postponements_reactivation"]
        assert after_catalog.pop("task_reactivation_requirements")["checks"] == [
            "ck_task_reactivation_requirements_date", "ck_task_reactivation_requirements_decision",
            "ck_task_reactivation_requirements_kind", "ck_task_reactivation_requirements_target"]
        # A later revision records which runtime instance acknowledged each team member's handoff.
        members = after_catalog["agent_team_topology_members"]["columns"]
        for column in (
            "issued_runtime_instance_id",
            "acknowledged_runtime_instance_id",
            "previous_runtime_instance_id",
            "rejected_runtime_instance_id",
        ):
            assert members.pop(column) == {"type": {"family": "text"}, "nullable": True}
        for column in ("runtime_identity_changed_at", "rejected_runtime_instance_at"):
            assert members.pop(column)["nullable"] is True
        assert after_catalog == before_catalog
        with engine.begin() as db:
            assert "AUTOINCREMENT" in db.scalar(text("SELECT sql FROM sqlite_master WHERE name='projects'"))
            inserted = db.execute(Project.__table__.insert().values(name="Unrelated new scope"))
            assert inserted.inserted_primary_key[0] == 91
            db.execute(Project.__table__.delete().where(Project.id == 91))
            inserted = db.execute(Project.__table__.insert().values(name="Next scope"))
            assert inserted.inserted_primary_key[0] == 92
            assert db.exec_driver_sql("PRAGMA foreign_key_check").fetchall() == []
        run_alembic_upgrade(backup=False, run_repairs=False)
        assert path.exists()
    finally:
        engine.dispose()


@pytest.mark.sqlite
@pytest.mark.parametrize("failure_point", ["drop table projects", "create index ix_projects_status"])
def test_failed_rebuild_rolls_back_schema_and_all_dependent_rows(tmp_path, configure_database, failure_point):
    path, engine = legacy_store(tmp_path, configure_database)
    with engine.begin() as db:
        seed_dependents(db)
    before_rows, before_catalog = database_rows(engine), schema_snapshot(engine)
    before_bytes = path.read_bytes()

    def fail(_connection, _cursor, statement, _parameters, _context, _many):
        if statement.lower().replace('"', '').strip().startswith(failure_point):
            raise RuntimeError("Injected table replacement failure")

    event.listen(Engine, "before_cursor_execute", fail)
    try:
        with pytest.raises(RuntimeError, match="replacement failure"):
            run_alembic_upgrade(backup=False, run_repairs=False)
    finally:
        event.remove(Engine, "before_cursor_execute", fail)
    try:
        assert database_rows(engine) == before_rows
        assert schema_snapshot(engine) == before_catalog
        assert path.read_bytes() == before_bytes
        with sqlite3.connect(path) as db:
            assert db.execute("SELECT version_num FROM alembic_version").fetchone()[0] == "20261007_0008"
        run_alembic_upgrade(backup=False, run_repairs=False)
    finally:
        engine.dispose()


@pytest.mark.sqlite
def test_direct_upgrade_preserves_enabled_foreign_keys(tmp_path, configure_database):
    _, engine = legacy_store(tmp_path, configure_database)
    try:
        with engine.begin() as db:
            seed_dependents(db)
        with engine.connect() as db:
            db.exec_driver_sql("PRAGMA foreign_keys=ON")
            db.commit()
            command.upgrade(alembic_config(connection=db), "head")
            assert db.exec_driver_sql("PRAGMA foreign_keys").scalar_one() == 1
            assert db.exec_driver_sql("PRAGMA foreign_key_check").fetchall() == []
            assert db.scalar(text("SELECT project_id FROM tasks WHERE id=1")) == 5
    finally:
        engine.dispose()


@pytest.mark.sqlite
def test_direct_upgrade_refuses_to_commit_a_callers_pending_writes(tmp_path, configure_database):
    path, engine = legacy_store(tmp_path, configure_database)
    try:
        with engine.connect() as db:
            insert_legacy_project(db, name="Pending caller state")
            with pytest.raises(RuntimeError, match="pending writes"):
                command.upgrade(alembic_config(connection=db), "head")
            db.rollback()
        with sqlite3.connect(path) as db:
            assert db.execute("SELECT count(*) FROM projects").fetchone()[0] == 0
            assert db.execute("SELECT version_num FROM alembic_version").fetchone()[0] == "20261007_0008"
    finally:
        engine.dispose()
