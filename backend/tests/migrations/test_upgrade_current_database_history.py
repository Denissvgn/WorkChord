"""However much history a database has retained, it starts when current and migrates when not."""

from datetime import UTC, datetime

import pytest

from app.models.identity import CommandAudit, Principal
from app.services.upgrade_service import UpgradeError, run_alembic_upgrade
from tests.migrations.test_project_identity import insert_legacy_project, legacy_store

# The history scan that guards a project-identity rebuild once stopped after this many rows.
SCAN_BOUND = 10000


def _retain_history(engine, rows):
    with engine.begin() as db:
        db.execute(Principal.__table__.insert().values(id=1, kind="human", display_name="Owner"))
        db.execute(
            CommandAudit.__table__.insert(),
            [
                dict(principal_id=1, action="tasks:edit", source="rest",
                     correlation_id=f"history-{number}", details={"entity_id": number})
                for number in range(rows)
            ],
        )


@pytest.mark.sqlite
def test_current_database_with_long_history_is_started_without_the_identity_scan(tmp_path, configure_database):
    path, engine = legacy_store(tmp_path, configure_database)
    try:
        run_alembic_upgrade(backup=False, run_repairs=False)
        _retain_history(engine, SCAN_BOUND + 1)
        stored = path.read_bytes()

        before, backup_path, after = run_alembic_upgrade(backup=False, run_repairs=False)

        assert before.is_current and after.is_current
        assert backup_path is None
        assert path.read_bytes() == stored
    finally:
        engine.dispose()


@pytest.mark.sqlite
def test_pending_migration_scans_all_of_a_long_history_before_it_rebuilds(tmp_path, configure_database):
    _path, engine = legacy_store(tmp_path, configure_database)
    try:
        _retain_history(engine, SCAN_BOUND + 1)

        before, _backup_path, after = run_alembic_upgrade(backup=False, run_repairs=False)

        assert not before.is_current and after.is_current
    finally:
        engine.dispose()


@pytest.mark.sqlite
def test_pending_migration_refuses_an_ambiguous_row_beyond_the_former_bound(tmp_path, configure_database):
    path, engine = legacy_store(tmp_path, configure_database)
    try:
        _retain_history(engine, SCAN_BOUND + 1)
        with engine.begin() as db:
            insert_legacy_project(db, id=5, name="Current identity", created_at=datetime(2026, 1, 1, tzinfo=UTC))
            db.execute(CommandAudit.__table__.insert().values(
                principal_id=1, action="projects:edit", source="rest", correlation_id="predates-identity",
                details={"entity_id": 5}, created_at=datetime(2025, 1, 1, tzinfo=UTC)))
        stored = path.read_bytes()

        with pytest.raises(UpgradeError) as error:
            run_alembic_upgrade(backup=False, run_repairs=False)

        assert error.value.diagnostics["code"] == "project_identity_ambiguous"
        assert error.value.diagnostics["diagnostics"][0]["record_id"] == SCAN_BOUND + 2
        assert path.read_bytes() == stored
    finally:
        engine.dispose()
