"""Cross-dialect value normalization and streaming table digests."""

from __future__ import annotations

import base64
from datetime import UTC, date, datetime
from decimal import Decimal
import hashlib
import json
import math
from typing import Any, Iterable, Mapping

from sqlalchemy.sql.schema import Column, Table

from app.database_migration.catalog import column_family
from app.database_migration.manifest import canonical_json_bytes


def _datetime(value: Any) -> datetime:
    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(f"invalid UTC timestamp {value!r}") from exc
    else:
        raise ValueError(f"invalid timestamp value of type {type(value).__name__}")
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=UTC)
    return parsed.astimezone(UTC)


def _date(value: Any) -> date:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value.strip())
        except ValueError as exc:
            raise ValueError(f"invalid date {value!r}") from exc
    raise ValueError(f"invalid date value of type {type(value).__name__}")


def _json(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError("invalid JSON value") from exc
    return value


def storage_value(column: Column[object], value: Any) -> Any:
    """Convert a raw SQLite value to the target column's Python type."""

    if value is None:
        return None
    family = column_family(column)
    if family == "boolean":
        if value not in (0, 1, False, True):
            raise ValueError(f"invalid Boolean value {value!r}")
        return bool(value)
    if family == "datetime":
        return _datetime(value)
    if family == "date":
        return _date(value)
    if family == "json":
        return _json(value)
    if family == "binary":
        return bytes(value)
    if family == "integer":
        return int(value)
    if family == "float":
        converted = float(value)
        if not math.isfinite(converted):
            raise ValueError("non-finite floats are not transferable")
        return converted
    if family == "numeric":
        return Decimal(str(value))
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite floats are not transferable")
    return value


def canonical_value(column: Column[object], value: Any) -> Any:
    """Convert a value to its dialect-independent JSON representation."""

    converted = storage_value(column, value)
    if converted is None or isinstance(converted, (bool, int, str)):
        return converted
    if isinstance(converted, datetime):
        return converted.isoformat(timespec="microseconds").replace("+00:00", "Z")
    if isinstance(converted, date):
        return converted.isoformat()
    if isinstance(converted, Decimal):
        return format(converted, "f")
    if isinstance(converted, float):
        return converted
    if isinstance(converted, (bytes, bytearray, memoryview)):
        return {"base64": base64.b64encode(bytes(converted)).decode("ascii")}
    if isinstance(converted, (list, dict)):
        return converted
    raise ValueError(f"unsupported value type {type(converted).__name__}")


def canonical_row(table: Table, row: Mapping[str, Any]) -> list[Any]:
    return [canonical_value(column, row[column.name]) for column in table.columns]


def row_sha256(table: Table, row: Mapping[str, Any]) -> str:
    return hashlib.sha256(canonical_json_bytes(canonical_row(table, row))).hexdigest()


def digest_rows(table: Table, rows: Iterable[Mapping[str, Any]]) -> tuple[int, str]:
    digest = hashlib.sha256()
    count = 0
    for row in rows:
        digest.update(canonical_json_bytes(canonical_row(table, row)))
        digest.update(b"\n")
        count += 1
    return count, digest.hexdigest()
