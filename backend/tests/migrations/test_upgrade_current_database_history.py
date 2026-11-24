"""A database that is already current starts however much history it has retained."""

import pytest

from app.models.identity import CommandAudit, Principal
from app.services.upgrade_service import UpgradeError, run_alembic_upgrade
from tests.migrations.test_project_identity import legacy_store

# The history scan that guards a project-identity rebuild stops after this many rows.
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
def test_pending_migration_still_scans_the_history_it_is_about_to_rebuild(tmp_path, configure_database):
    path, engine = legacy_store(tmp_path, configure_database)
    try:
        _retain_history(engine, SCAN_BOUND + 1)
        stored = path.read_bytes()

        with pytest.raises(UpgradeError) as error:
            run_alembic_upgrade(backup=False, run_repairs=False)

        assert error.value.diagnostics["code"] == "project_history_scan_limit"
        assert path.read_bytes() == stored
    finally:
        engine.dispose()
