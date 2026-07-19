"""Deterministic mapped-model and representative legacy-database factories."""

from __future__ import annotations

from datetime import UTC, date, datetime
from pathlib import Path
import sqlite3
from typing import Any

from sqlalchemy import Boolean, Date, DateTime, Float, Integer, JSON, LargeBinary, Numeric
from sqlalchemy import inspect as sa_inspect
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.types import TypeDecorator


class MappedModelFactory:
    """Build any registered SQLAlchemy model with deterministic safe values.

    The generic builder is intentionally model-agnostic so newly mapped tables
    become visible to one coverage test. Callers provide relationship-specific
    overrides when they intend to flush a graph.
    """

    def __init__(self) -> None:
        self._sequence = 0

    def _next(self) -> int:
        self._sequence += 1
        return self._sequence

    def _value_for(self, column: Any) -> Any:
        sequence = self._next()
        column_type = column.type
        if isinstance(column_type, Boolean):
            return False
        if isinstance(column_type, DateTime) or (
            isinstance(column_type, TypeDecorator)
            and isinstance(column_type.impl, DateTime)
        ):
            return datetime(2026, 1, 1, tzinfo=UTC)
        if isinstance(column_type, Date):
            return date(2026, 1, 1)
        if isinstance(column_type, Integer):
            return sequence
        if isinstance(column_type, (Float, Numeric)):
            return float(sequence)
        if isinstance(column_type, JSON):
            return {}
        if isinstance(column_type, LargeBinary):
            return f"test-{sequence}".encode()
        if isinstance(column_type, String):
            return f"test-{column.key}-{sequence}"
        raise TypeError(
            f"No deterministic factory value for {column.key}: {column_type!r}"
        )

    def build(self, model: type[Any], /, **overrides: Any) -> Any:
        """Build, but do not persist, one instance of any mapped model."""

        mapper = sa_inspect(model)
        values: dict[str, Any] = {}
        for column in mapper.columns:
            key = column.key
            if key in overrides:
                values[key] = overrides.pop(key)
                continue
            if column.primary_key and column.autoincrement in {True, "auto"}:
                continue
            if column.default is not None or column.server_default is not None:
                continue
            if column.nullable:
                continue
            values[key] = self._value_for(column)
        if overrides:
            unknown = ", ".join(sorted(overrides))
            raise TypeError(f"Unknown mapped attributes for {model.__name__}: {unknown}")
        return model(**values)


class LegacySQLiteFactory:
    """Create representative pre-Alembic SQLite sources for migration tests."""

    _SCHEMA = """
        PRAGMA foreign_keys = ON;
        CREATE TABLE calendars (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            year INTEGER NOT NULL
        );
        CREATE TABLE iterations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            calendar_id INTEGER NOT NULL REFERENCES calendars(id)
        );
        CREATE TABLE team_members (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            iteration_id INTEGER REFERENCES iterations(id)
        );
        CREATE TABLE vacations (
            id INTEGER PRIMARY KEY,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            team_member_id INTEGER NOT NULL REFERENCES team_members(id)
        );
        CREATE TABLE tasks (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            status TEXT,
            iteration_id INTEGER NOT NULL REFERENCES iterations(id),
            parent_id INTEGER REFERENCES tasks(id),
            assignee_id INTEGER REFERENCES team_members(id)
        );
        CREATE TABLE task_dependencies (
            id INTEGER PRIMARY KEY,
            task_id INTEGER NOT NULL REFERENCES tasks(id),
            depends_on_id INTEGER NOT NULL REFERENCES tasks(id)
        );
        CREATE TABLE task_status_logs (
            id INTEGER PRIMARY KEY,
            task_id INTEGER NOT NULL REFERENCES tasks(id),
            from_status TEXT NOT NULL,
            to_status TEXT NOT NULL,
            changed_at DATETIME NOT NULL
        );
    """

    def create(self, path: Path, *, with_orphan: bool = False) -> Path:
        """Create a valid source, or one deliberately containing an orphan."""

        if path.exists():
            raise FileExistsError(path)
        with sqlite3.connect(path) as connection:
            connection.executescript(self._SCHEMA)
            connection.execute(
                "INSERT INTO calendars (id, name, year) VALUES (1, 'Legacy', 2026)"
            )
            connection.execute(
                """
                INSERT INTO iterations (id, name, start_date, end_date, calendar_id)
                VALUES (1, 'Legacy iteration', '2026-01-01', '2026-01-14', 1)
                """
            )
            connection.execute(
                """
                INSERT INTO tasks (id, title, status, iteration_id)
                VALUES (1, 'Legacy task', 'planned', 1)
                """
            )
            if with_orphan:
                connection.commit()
                connection.execute("PRAGMA foreign_keys = OFF")
                connection.execute(
                    """
                    INSERT INTO task_status_logs
                        (id, task_id, from_status, to_status, changed_at)
                    VALUES (1, 999, 'planned', 'active', '2026-01-02 00:00:00')
                    """
                )
                connection.commit()
        return path
