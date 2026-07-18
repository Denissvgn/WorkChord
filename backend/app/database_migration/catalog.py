"""Versioned transfer catalog derived from the packaged ORM schema."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    Integer,
    JSON,
    LargeBinary,
    Numeric,
    String,
)
from sqlalchemy.sql.schema import Column, Table
from sqlalchemy.types import TypeDecorator

from app import models  # noqa: F401 - register every mapped table
from app.database import Base


TRANSFER_CATALOG_VERSION = 1
TARGET_OWNED_TABLES = frozenset({"alembic_version", "database_migration_gates"})
TEXT_JSON_COLUMNS = frozenset(
    {
        ("agent_actors", "scopes"),
        ("agent_idempotency_records", "response_payload"),
        ("agent_run_events", "payload"),
        ("agent_runs", "artifact_links"),
        ("agent_runs", "run_metadata"),
        ("agent_task_assignments", "routing_snapshot"),
        ("task_events", "payload"),
        ("task_status_logs", "affected_task_ids"),
    }
)


@dataclass(frozen=True)
class CatalogEntry:
    table_name: str
    disposition: Literal["transfer", "target_owned"]
    primary_key: tuple[str, ...]
    staged_reference_columns: tuple[str, ...]


def _base_type(column: Column[object]) -> object:
    value: object = column.type
    while isinstance(value, TypeDecorator):
        value = value.impl
    return value


def column_family(column: Column[object]) -> str:
    """Return the conversion family used by canonicalization and loading."""

    value = _base_type(column)
    if isinstance(value, Boolean):
        return "boolean"
    if isinstance(value, DateTime):
        return "datetime"
    if isinstance(value, Date):
        return "date"
    if isinstance(value, JSON):
        return "json"
    if isinstance(value, LargeBinary):
        return "binary"
    if isinstance(value, Integer):
        return "integer"
    if isinstance(value, Float):
        return "float"
    if isinstance(value, Numeric):
        return "numeric"
    return "scalar"


def column_max_length(column: Column[object]) -> int | None:
    """Return the target character limit, including decorated string types."""

    value = _base_type(column)
    if not isinstance(value, String):
        return None
    return value.length


def application_tables() -> dict[str, Table]:
    return {table.name: table for table in Base.metadata.tables.values()}


def transfer_tables() -> dict[str, Table]:
    return {
        name: table
        for name, table in application_tables().items()
        if name not in TARGET_OWNED_TABLES
    }


def staged_reference_columns(table: Table) -> tuple[str, ...]:
    """Stage nullable references so cycles never weaken target constraints."""

    columns: set[str] = set()
    for constraint in table.foreign_key_constraints:
        constrained = [element.parent for element in constraint.elements]
        if constrained and all(column.nullable for column in constrained):
            columns.update(column.name for column in constrained)
    return tuple(sorted(columns))


def transfer_order() -> tuple[str, ...]:
    """Topologically order tables by non-nullable foreign-key dependencies."""

    tables = transfer_tables()
    dependencies: dict[str, set[str]] = {name: set() for name in tables}
    for name, table in tables.items():
        for constraint in table.foreign_key_constraints:
            parent_name = constraint.referred_table.name
            if parent_name == name or parent_name not in tables:
                continue
            constrained = [element.parent for element in constraint.elements]
            if constrained and not all(column.nullable for column in constrained):
                dependencies[name].add(parent_name)

    ordered: list[str] = []
    remaining = set(tables)
    while remaining:
        ready = sorted(
            name for name in remaining if dependencies[name].issubset(ordered)
        )
        if not ready:
            detail = ", ".join(
                f"{name}->{sorted(dependencies[name] & remaining)}"
                for name in sorted(remaining)
            )
            raise RuntimeError(f"Non-nullable transfer dependency cycle: {detail}")
        ordered.extend(ready)
        remaining.difference_update(ready)
    return tuple(ordered)


def catalog_entries() -> tuple[CatalogEntry, ...]:
    tables = application_tables()
    entries = [
        CatalogEntry(
            table_name=name,
            disposition=("target_owned" if name in TARGET_OWNED_TABLES else "transfer"),
            primary_key=tuple(column.name for column in table.primary_key.columns),
            staged_reference_columns=(
                () if name in TARGET_OWNED_TABLES else staged_reference_columns(table)
            ),
        )
        for name, table in sorted(tables.items())
    ]
    entries.append(
        CatalogEntry(
            table_name="alembic_version",
            disposition="target_owned",
            primary_key=("version_num",),
            staged_reference_columns=(),
        )
    )
    return tuple(sorted(entries, key=lambda entry: entry.table_name))
