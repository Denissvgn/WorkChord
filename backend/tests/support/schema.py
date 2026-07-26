"""Stable schema snapshots for the SQLite/PostgreSQL migration matrix."""

from __future__ import annotations

from typing import Any

from sqlalchemy import inspect
from sqlalchemy.engine import Connection, Engine


def _type_contract(column_type: Any) -> dict[str, Any]:
    class_name = type(column_type).__name__.lower()
    if "timestamp" in class_name or "datetime" in class_name:
        family = "datetime"
    elif "bool" in class_name:
        family = "boolean"
    elif "json" in class_name:
        family = "json"
    elif "char" in class_name or "text" in class_name or "string" in class_name:
        family = "text"
    elif "int" in class_name or "serial" in class_name:
        family = "integer"
    elif "float" in class_name or "real" in class_name or "double" in class_name:
        family = "float"
    elif "date" in class_name:
        family = "date"
    else:
        family = class_name
    contract: dict[str, Any] = {"family": family}
    if family == "datetime":
        contract["timezone"] = bool(getattr(column_type, "timezone", False))
    return contract


def schema_snapshot(bind: Connection | Engine) -> dict[str, Any]:
    """Return deterministic live schema facts without dialect object reprs."""

    inspector = inspect(bind)
    snapshot: dict[str, Any] = {}
    for table_name in sorted(
        set(inspector.get_table_names()) - {"alembic_version"}
    ):
        columns = {
            column["name"]: {
                "type": _type_contract(column["type"]),
                "nullable": bool(column["nullable"]),
            }
            for column in inspector.get_columns(table_name)
        }
        primary_key = tuple(
            inspector.get_pk_constraint(table_name).get("constrained_columns") or ()
        )
        foreign_keys = sorted(
            {
                (
                    tuple(foreign_key.get("constrained_columns") or ()),
                    foreign_key.get("referred_table"),
                    tuple(foreign_key.get("referred_columns") or ()),
                    (foreign_key.get("options") or {}).get("ondelete"),
                )
                for foreign_key in inspector.get_foreign_keys(table_name)
            }
        )
        unique_constraints = sorted(
            {
                tuple(constraint.get("column_names") or ())
                for constraint in inspector.get_unique_constraints(table_name)
            }
        )
        indexes = sorted(
            {
                (
                    index.get("name"),
                    tuple(index.get("column_names") or ()),
                    bool(index.get("unique")),
                )
                for index in inspector.get_indexes(table_name)
                if not index.get("duplicates_constraint")
            }
        )
        checks = sorted(
            constraint.get("name")
            for constraint in inspector.get_check_constraints(table_name)
            if constraint.get("name")
        )
        snapshot[table_name] = {
            "columns": columns,
            "primary_key": primary_key,
            "foreign_keys": foreign_keys,
            "unique_constraints": unique_constraints,
            "indexes": indexes,
            "checks": checks,
        }
    return snapshot


def cross_dialect_schema_diff(
    sqlite_snapshot: dict[str, Any],
    postgresql_snapshot: dict[str, Any],
) -> dict[str, Any]:
    """Describe only reviewed physical differences between logical schemas."""

    sqlite_tables = set(sqlite_snapshot)
    postgresql_tables = set(postgresql_snapshot)
    differences: dict[str, Any] = {
        "missing_from_sqlite": sorted(postgresql_tables - sqlite_tables),
        "missing_from_postgresql": sorted(sqlite_tables - postgresql_tables),
        "column_type_differences": [],
        "structural_differences": [],
    }
    for table_name in sorted(sqlite_tables & postgresql_tables):
        sqlite_table = sqlite_snapshot[table_name]
        postgresql_table = postgresql_snapshot[table_name]
        if set(sqlite_table["columns"]) != set(postgresql_table["columns"]):
            differences["structural_differences"].append(
                {
                    "table": table_name,
                    "kind": "columns",
                    "sqlite": sorted(sqlite_table["columns"]),
                    "postgresql": sorted(postgresql_table["columns"]),
                }
            )
        for column_name in sorted(
            set(sqlite_table["columns"]) & set(postgresql_table["columns"])
        ):
            sqlite_column = sqlite_table["columns"][column_name]
            postgresql_column = postgresql_table["columns"][column_name]
            if sqlite_column["nullable"] != postgresql_column["nullable"]:
                differences["structural_differences"].append(
                    {
                        "table": table_name,
                        "column": column_name,
                        "kind": "nullable",
                        "sqlite": sqlite_column["nullable"],
                        "postgresql": postgresql_column["nullable"],
                    }
                )
            if sqlite_column["type"] != postgresql_column["type"]:
                differences["column_type_differences"].append(
                    {
                        "table": table_name,
                        "column": column_name,
                        "sqlite": sqlite_column["type"],
                        "postgresql": postgresql_column["type"],
                    }
                )
        for key in (
            "primary_key",
            "foreign_keys",
            "unique_constraints",
            "indexes",
            "checks",
        ):
            if sqlite_table[key] != postgresql_table[key]:
                differences["structural_differences"].append(
                    {
                        "table": table_name,
                        "kind": key,
                        "sqlite": sqlite_table[key],
                        "postgresql": postgresql_table[key],
                    }
                )
    return differences
