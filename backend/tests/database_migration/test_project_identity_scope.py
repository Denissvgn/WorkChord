"""Ambiguous legacy identities stop before writes and never expose private records."""

from datetime import UTC, datetime
import json

import pytest
from sqlalchemy import event
from sqlalchemy.engine import Engine

from app.database_migration.project_identity import ProjectIdentityError, inspect_project_identity
from app.database_migration.source import MigrationDataError, preflight_source
from app.models.identity import CommandAudit
from app.models.project import Project
from app.models.time_entry import TimeEntry, TimeEntryRevision
from app.services.upgrade_service import UpgradeError, run_alembic_upgrade
from tests.database_migration.test_source_preflight import _drain_evidence
from tests.migrations.test_project_identity import legacy_store, retained_entry, seed_dependents


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
            db.execute(Project.__table__.insert().values(id=5, name="Current identity"))
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
