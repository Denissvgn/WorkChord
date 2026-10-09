"""Versioned transfer catalog invariants."""

from __future__ import annotations

import pytest

from app.database_migration.catalog import (
    TARGET_OWNED_TABLES,
    application_tables,
    catalog_entries,
    staged_reference_columns,
    transfer_order,
    transfer_tables,
)


def test_catalog_disposes_every_packaged_table_exactly_once() -> None:
    entries = catalog_entries()

    expected = set(application_tables()) | {"alembic_version"}
    assert {entry.table_name for entry in entries} == expected
    assert len(entries) == len(expected)
    assert {
        entry.table_name for entry in entries if entry.disposition == "target_owned"
    } == TARGET_OWNED_TABLES
    assert set(transfer_order()) == set(transfer_tables())


def test_nullable_cycles_are_staged_without_weakening_required_foreign_keys() -> None:
    tables = transfer_tables()

    assert "parent_id" in staged_reference_columns(tables["tasks"])
    assert "duplicate_of_id" in staged_reference_columns(tables["triage_items"])
    assert "iteration_id" not in staged_reference_columns(tables["tasks"])
    assert transfer_order().index("iterations") < transfer_order().index("tasks")
    assert staged_reference_columns(tables["delivery_dependencies"]) == ()
    assert transfer_order().index("tasks") < transfer_order().index("delivery_dependencies")
    assert transfer_order().index("project_milestones") < transfer_order().index("delivery_dependencies")

@pytest.mark.parametrize("fault", ["negative", "noninteger", "duplicate"])
def test_source_allocation_reader_refuses_corrupt_sequence_metadata_without_writes(tmp_path, fault):
    import hashlib
    import sqlite3
    from app.database_migration.source import MigrationDataError
    from app.database_migration.transfer import _source_sequence_floors

    path = tmp_path / "allocation-source.db"
    with sqlite3.connect(path) as connection:
        connection.execute("CREATE TABLE tasks(id INTEGER PRIMARY KEY AUTOINCREMENT)")
        connection.execute("INSERT INTO tasks(id) VALUES(350)")
        connection.execute("DELETE FROM tasks")
    assert _source_sequence_floors(path)["tasks"] == 350
    with sqlite3.connect(path) as connection:
        if fault == "duplicate":
            connection.execute("INSERT INTO sqlite_sequence(name,seq) VALUES('tasks',351)")
        else:
            connection.execute("UPDATE sqlite_sequence SET seq=? WHERE name='tasks'", (-1 if fault == "negative" else "unknown",))
    before = hashlib.sha256(path.read_bytes()).hexdigest()
    with pytest.raises(MigrationDataError) as error:
        _source_sequence_floors(path)
    assert error.value.code == "allocation_identity_invalid"
    assert hashlib.sha256(path.read_bytes()).hexdigest() == before
