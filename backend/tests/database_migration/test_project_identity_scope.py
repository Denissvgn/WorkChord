"""Ambiguous legacy identities stop before writes and never expose private records."""

from datetime import UTC, datetime
import json

import pytest
from sqlalchemy import event, select
from sqlalchemy.engine import Engine

from app.database_migration import project_identity
from app.database_migration.project_identity import ProjectIdentityError, inspect_project_identity
from app.database_migration.source import MigrationDataError, preflight_source
from app.models.identity import CommandAudit
from app.models.project import Project
from app.models.time_entry import TimeEntry, TimeEntryRevision
from app.services.upgrade_service import UpgradeError, run_alembic_upgrade
from tests.database_migration.test_source_preflight import _drain_evidence
from tests.migrations.test_project_identity import insert_legacy_project, legacy_store, retained_entry, seed_dependents


@pytest.mark.sqlite
@pytest.mark.parametrize("name", ["Same display name", "Different display name"])
def test_ambiguous_retained_scope_blocks_upgrade_and_snapshot_before_writes(tmp_path, configure_database, name):
    path, engine = legacy_store(tmp_path, configure_database)
    with engine.begin() as db:
        seed_dependents(db)
        db.execute(Project.__table__.update().where(Project.id == 5).values(name=name))
        db.execute(TimeEntry.__table__.update().values(project_id=5, created_at=datetime(2000, 1, 1, tzinfo=UTC)))
        db.execute(TimeEntryRevision.__table__.update().values(project_id=5, created_at=datetime(2000, 1, 1, tzinfo=UTC)))
    before = path.read_bytes()
    statements = []

    def observe(_connection, _cursor, statement, _parameters, _context, _many):
        statements.append(statement.strip().split()[0].upper())

    event.listen(Engine, "before_cursor_execute", observe)
    try:
        with pytest.raises(UpgradeError) as error:
            run_alembic_upgrade(backup=True, backup_dir=tmp_path / "backups", run_repairs=False)
        assert error.value.diagnostics["code"] == "project_identity_ambiguous"
        assert "Retained private evidence" not in str(error.value)
        assert not {"CREATE", "ALTER", "DROP", "INSERT", "UPDATE", "DELETE"}.intersection(statements)
        assert not (tmp_path / "backups").exists()
        assert path.read_bytes() == before
        evidence = _drain_evidence(tmp_path / "drain.json")
        with pytest.raises(MigrationDataError, match="project_identity_ambiguous"):
            preflight_source(source_path=path, snapshot_path=tmp_path / "rejected.db",
                writer_drain_evidence_path=evidence, manifest_path=tmp_path / "rejected.json")
        assert not (tmp_path / "rejected.db").exists()
        assert not (tmp_path / "rejected.json").exists()
        assert path.read_bytes() == before
    finally:
        event.remove(Engine, "before_cursor_execute", observe)
        engine.dispose()


@pytest.mark.sqlite
def test_collision_diagnostics_are_bounded_and_do_not_include_notes(tmp_path, configure_database):
    _, engine = legacy_store(tmp_path, configure_database)
    try:
        with engine.begin() as db:
            insert_legacy_project(db, id=5, name="Current identity")
            for _ in range(102):
                retained_entry(db, 5)
            db.execute(TimeEntry.__table__.update().values(created_at=datetime(2000, 1, 1, tzinfo=UTC)))
            db.execute(TimeEntryRevision.__table__.update().values(created_at=datetime(2000, 1, 1, tzinfo=UTC)))
        with engine.connect() as db, pytest.raises(ProjectIdentityError) as error:
            inspect_project_identity(db)
        detail = error.value.detail()
        assert detail["truncated"] and len(detail["diagnostics"]) == 100
        assert detail["data_changed"] is False
        assert "Retained private evidence" not in json.dumps(detail)
    finally:
        engine.dispose()


@pytest.mark.sqlite
def test_incomplete_history_scan_fails_closed_without_mutation(tmp_path, configure_database):
    path, engine = legacy_store(tmp_path, configure_database)
    try:
        with engine.begin() as db:
            seed_dependents(db)
            db.execute(CommandAudit.__table__.insert().values(principal_id=1, project_id=5,
                action="projects:edit", source="rest", correlation_id="additional", details={"entity_id": 5}))
        before = path.read_bytes()
        with engine.connect() as db, pytest.raises(ProjectIdentityError, match="project_history_scan_limit"):
            inspect_project_identity(db, max_history_rows=1)
        assert path.read_bytes() == before
    finally:
        engine.dispose()


def _audits(db, count, *, predating_at=None):
    """Retain edits of project 5; the one at ``predating_at`` is older than the project."""
    db.execute(Project.__table__.update().where(Project.id == 5).values(created_at=datetime(2026, 1, 1, tzinfo=UTC)))
    db.execute(CommandAudit.__table__.insert(), [
        dict(principal_id=1, project_id=5, action="projects:edit", source="rest", correlation_id=f"edit-{number}",
             details={"entity_id": 5},
             created_at=datetime(2025, 1, 1, tzinfo=UTC) if number == predating_at else datetime(2026, 2, 1, tzinfo=UTC))
        for number in range(count)
    ])


@pytest.mark.sqlite
@pytest.mark.parametrize("position", [0, 9, 10, 29])
def test_history_scan_checks_rows_on_every_page_and_batch_boundary(tmp_path, configure_database, monkeypatch, position):
    _, engine = legacy_store(tmp_path, configure_database)
    try:
        with engine.begin() as db:
            seed_dependents(db)
            db.execute(CommandAudit.__table__.delete())
            _audits(db, 30, predating_at=position)
            record_id = db.scalar(select(CommandAudit.id).where(CommandAudit.correlation_id == f"edit-{position}"))
        # One value per batch, so every row sits on the edge of a batch as well as of its page.
        monkeypatch.setattr(project_identity, "HISTORY_BATCH_CHARACTERS", 1)
        with engine.connect() as db, pytest.raises(ProjectIdentityError) as error:
            inspect_project_identity(db, page_rows=10)
        assert error.value.code == "project_identity_ambiguous"
        assert error.value.diagnostics == [{"table": "command_audit", "record_id": record_id, "project_id": 5,
                                            "reason": "retained_history_predates_current_identity"}]
    finally:
        engine.dispose()


@pytest.mark.sqlite
def test_history_scan_reads_in_pages_rather_than_row_by_row(tmp_path, configure_database):
    _, engine = legacy_store(tmp_path, configure_database)
    statements = []

    def observe(_connection, _cursor, statement, _parameters, _context, _many):
        if "FROM command_audit" in statement:
            statements.append(statement)

    try:
        with engine.begin() as db:
            seed_dependents(db)
            db.execute(CommandAudit.__table__.delete())
            _audits(db, 2500)
        event.listen(engine, "before_cursor_execute", observe)
        with engine.connect() as db:
            assert inspect_project_identity(db)["history_rows_checked"] == 2500
        # Three pages, each read as one page of row metadata and one batch of values,
        # plus the allocation-floor query: never one statement per row.
        assert len(statements) == 7
    finally:
        event.remove(engine, "before_cursor_execute", observe)
        engine.dispose()


@pytest.mark.sqlite
def test_oversized_history_value_is_refused_without_loading_it(tmp_path, configure_database, monkeypatch):
    _, engine = legacy_store(tmp_path, configure_database)
    try:
        with engine.begin() as db:
            seed_dependents(db)
            record_id = db.scalar(select(CommandAudit.id))
        monkeypatch.setattr(project_identity, "HISTORY_VALUE_CHARACTERS", 5)
        with engine.connect() as db, pytest.raises(ProjectIdentityError) as error:
            inspect_project_identity(db)
        assert error.value.code == "project_history_scan_limit"
        assert error.value.diagnostics == [{"table": "command_audit", "record_id": record_id}]
    finally:
        engine.dispose()
