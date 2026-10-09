"""Project allocation floors, dependent preservation and transactional rebuilds."""

from datetime import UTC, datetime
import sqlite3
from uuid import uuid4

from alembic import command
import pytest
from sqlalchemy import create_engine, event, text
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


def retained_entry(db, project_id):
    values = dict(project_id=project_id, task_id=None, principal_id=1, work_date=datetime(2026, 1, 1).date(),
        timezone="UTC", minutes=90, note="Retained private evidence", version=1, voided=False)
    result = db.execute(TimeEntry.__table__.insert().values(**values, request_id=str(uuid4()), creation_digest="a" * 64))
    db.execute(TimeEntryRevision.__table__.insert().values(**{key: value for key, value in values.items() if key != "task_id"},
        entry_id=result.inserted_primary_key[0], reason="Recorded"))


def seed_dependents(db):
    db.execute(Principal.__table__.insert().values(id=1, kind="human", display_name="Owner"))
    db.execute(Project.__table__.insert().values(id=5, name="Current project"))
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
        return {name: db.execute(text(f'SELECT * FROM "{name}"')).fetchall()
                for name in sorted(catalog) if name != "alembic_version"}


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
        assert database_rows(engine) == before_rows
        after_catalog = schema_snapshot(engine)
        allocation = after_catalog["team_members"]
        assert allocation["columns"].pop("allocation_token") == {"type": {"family": "text"}, "nullable": False}
        allocation["unique_constraints"].remove(("allocation_token",))
        profiles = after_catalog["team_member_profiles"]
        assert profiles["columns"].pop("profile_token") == {"type": {"family": "text"}, "nullable": False}
        profiles["unique_constraints"].remove(("profile_token",))
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
            db.execute(Project.__table__.insert().values(name="Pending caller state"))
            with pytest.raises(RuntimeError, match="pending writes"):
                command.upgrade(alembic_config(connection=db), "head")
            db.rollback()
        with sqlite3.connect(path) as db:
            assert db.execute("SELECT count(*) FROM projects").fetchone()[0] == 0
            assert db.execute("SELECT version_num FROM alembic_version").fetchone()[0] == "20261007_0008"
    finally:
        engine.dispose()
