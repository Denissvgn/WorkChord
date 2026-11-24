"""A deployment with a long retained history migrates to head and can be rolled back.

The project-identity scan once stopped after 10,000 history rows, so a seeded or
short-lived database passed while every deployment that had been used for a while
refused its next migration. These cases build such a history on the revision the
long-running deployments still run, migrate it, and roll it back.
"""

from datetime import UTC, date, datetime, timedelta
import json
import sqlite3
from uuid import uuid4

from alembic import command
import pytest
from sqlalchemy import MetaData, Table, create_engine, func, select

from app import models  # noqa: F401 - register mapped metadata
from app.database import Base
from app.services.upgrade_service import UpgradeError, alembic_config, head_revision, inspect_database, run_alembic_upgrade
from tests.migrations.test_project_identity import insert_legacy_project

PRIOR_REVISION = "20261116_0017"
PROJECTS = 24
AUDIT_ROWS = 12000
TASK_EVENTS = 3000
TIME_ENTRIES = 400
HISTORY_TABLES = ("command_audit", "task_events", "time_entries", "time_entry_revisions")
PROJECTS_CREATED = datetime(2025, 1, 1, tzinfo=UTC)
CHUNK = 2000

DIALECTS = [
    pytest.param("sqlite", marks=pytest.mark.sqlite),
    pytest.param("postgresql", marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network]),
]


def _database(dialect, request, tmp_path, configure_database):
    if dialect == "postgresql":
        url = request.getfixturevalue("postgres_database").url
        configure_database(url)
        return url, None
    path = tmp_path / "populated-history.db"
    configure_database(f"sqlite+aiosqlite:///{path}")
    return f"sqlite:///{path}", path


def _insert(db, name, rows):
    """Insert through the table as the prior revision defines it, filling mapped defaults."""
    legacy = Table(name, MetaData(), autoload_with=db)
    defaults = {}
    for column in Base.metadata.tables[name].columns:
        if column.name in legacy.c and column.default is not None and not column.primary_key:
            default = column.default
            defaults[column.name] = default.arg(None) if default.is_callable else default.arg
    for start in range(0, len(rows), CHUNK):
        db.execute(legacy.insert(), [{**defaults, **row} for row in rows[start:start + CHUNK]])


def _moment(number):
    return datetime(2026, 1, 2, tzinfo=UTC) + timedelta(minutes=number)


def _retain_populated_history(db):
    """Bulk-insert a history shaped like a long-used deployment's: audit, events and time records."""
    _insert(db, "principals", [dict(id=1, kind="human", display_name="Owner")])
    for project_id in range(1, PROJECTS + 1):
        insert_legacy_project(db, id=project_id, name=f"Project {project_id}", created_at=PROJECTS_CREATED,
                              updated_at=PROJECTS_CREATED)
    _insert(db, "command_audit", [
        dict(principal_id=1, project_id=number % PROJECTS + 1,
             action="projects:edit" if number % 5 == 0 else "tasks:edit", source="rest",
             correlation_id=f"history-{number}", created_at=_moment(number),
             details={"entity_id": number % PROJECTS + 1, "changes": {"status": ["active", "done"]},
                      "context": {"project_id": number % PROJECTS + 1}})
        for number in range(AUDIT_ROWS)
    ])
    _insert(db, "task_events", [
        dict(task_id=None, actor_type="user", event_type="task.updated", created_at=_moment(number),
             payload=json.dumps({"project": {"id": number % PROJECTS + 1}, "status": "done"}))
        for number in range(TASK_EVENTS)
    ])
    entry = dict(task_id=None, principal_id=1, work_date=date(2026, 3, 2), timezone="UTC", minutes=45,
                 note="Retained private evidence", version=1, voided=False)
    _insert(db, "time_entries", [
        dict(entry, id=number, project_id=number % PROJECTS + 1, request_id=str(uuid4()),
             creation_digest="a" * 64, created_at=_moment(number), updated_at=_moment(number))
        for number in range(1, TIME_ENTRIES + 1)
    ])
    revision = {key: value for key, value in entry.items() if key != "task_id"}
    _insert(db, "time_entry_revisions", [
        dict(revision, id=number, entry_id=number, project_id=number % PROJECTS + 1, reason="Recorded",
             created_at=_moment(number))
        for number in range(1, TIME_ENTRIES + 1)
    ])


def _history(engine):
    """Every retained history row, keyed by table, in a form that compares across revisions."""
    with engine.connect() as db:
        result = {}
        for name in HISTORY_TABLES:
            history = Table(name, MetaData(), autoload_with=db)
            result[name] = [tuple(row) for row in db.execute(select(history).order_by(history.c.id))]
        projects = Table("projects", MetaData(), autoload_with=db)
        result["projects"] = db.execute(select(projects.c.id, projects.c.name).order_by(projects.c.id)).all()
        return result


def _revision(engine):
    with engine.connect() as db:
        return db.execute(select(Table("alembic_version", MetaData(), autoload_with=db).c.version_num)).scalar_one()


def _populated_prior_database(url):
    engine = create_engine(url)
    with engine.connect() as db:
        command.upgrade(alembic_config(connection=db), PRIOR_REVISION)
    with engine.begin() as db:
        _retain_populated_history(db)
    return engine


def _upgrade(dialect, tmp_path):
    if dialect == "postgresql":
        return run_alembic_upgrade(backup=False, run_repairs=False,
                                   external_backup_reference="isolated-restore-verified")
    return run_alembic_upgrade(backup=True, backup_dir=tmp_path / "backups", run_repairs=False)


@pytest.mark.parametrize("dialect", DIALECTS)
def test_populated_history_migrates_to_head_and_rolls_back(dialect, request, tmp_path, configure_database):
    url, _path = _database(dialect, request, tmp_path, configure_database)
    engine = _populated_prior_database(url)
    try:
        retained = _history(engine)
        assert sum(len(retained[name]) for name in HISTORY_TABLES) > 10000

        before, backup_path, after = _upgrade(dialect, tmp_path)

        assert before.current_revision == PRIOR_REVISION
        assert after.is_current and after.current_revision == head_revision()
        assert _history(engine) == retained

        if dialect == "sqlite":
            # The automatic backup is an independent rollback: the prior revision with every row.
            with sqlite3.connect(f"file:{backup_path}?mode=ro", uri=True) as backup:
                assert backup.execute("SELECT version_num FROM alembic_version").fetchone() == (PRIOR_REVISION,)
                for name in HISTORY_TABLES:
                    assert backup.execute(f'SELECT COUNT(*) FROM "{name}"').fetchone() == (len(retained[name]),)

        with engine.connect() as db:
            command.downgrade(alembic_config(connection=db), PRIOR_REVISION)
        assert _revision(engine) == PRIOR_REVISION
        assert _history(engine) == retained

        # The rolled-back database takes the release again.
        _before, _backup, again = _upgrade(dialect, tmp_path)
        assert again.current_revision == head_revision()
        assert _history(engine) == retained
    finally:
        engine.dispose()


def _predating_audit(db):
    _insert(db, "command_audit", [dict(principal_id=1, project_id=3, action="projects:edit", source="rest",
                                       correlation_id="predates-identity", created_at=datetime(2024, 6, 1, tzinfo=UTC),
                                       details={"entity_id": 3})])
    history = Table("command_audit", MetaData(), autoload_with=db)
    return "project_identity_ambiguous", "command_audit", db.scalar(select(func.max(history.c.id)))


def _unreadable_event(db):
    _insert(db, "task_events", [dict(task_id=None, actor_type="user", event_type="task.updated",
                                     created_at=_moment(1), payload="{not json")])
    history = Table("task_events", MetaData(), autoload_with=db)
    return "project_history_invalid", "task_events", db.scalar(select(func.max(history.c.id)))


@pytest.mark.parametrize("dialect", DIALECTS)
@pytest.mark.parametrize("inconsistency", [_predating_audit, _unreadable_event], ids=["predates-identity", "invalid"])
def test_inconsistent_row_after_a_long_history_still_refuses_the_migration(
        dialect, inconsistency, request, tmp_path, configure_database):
    url, path = _database(dialect, request, tmp_path, configure_database)
    engine = _populated_prior_database(url)
    try:
        with engine.begin() as db:
            code, table, record_id = inconsistency(db)
        retained = _history(engine)
        stored = path.read_bytes() if path else None

        with pytest.raises(UpgradeError) as error:
            _upgrade(dialect, tmp_path)

        detail = error.value.diagnostics
        assert detail["code"] == code and detail["data_changed"] is False
        assert {"table": table, "record_id": record_id}.items() <= detail["diagnostics"][0].items()
        assert "Retained private evidence" not in json.dumps(detail)
        assert inspect_database().current_revision == PRIOR_REVISION
        assert _history(engine) == retained
        if path:
            assert path.read_bytes() == stored
            assert not (tmp_path / "backups").exists()
    finally:
        engine.dispose()
