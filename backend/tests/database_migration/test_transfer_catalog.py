"""Versioned transfer catalog invariants."""

from __future__ import annotations

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
