"""Cross-dialect SQL expressions for the supported SQLite/PostgreSQL window."""

from __future__ import annotations

import unicodedata
from typing import Any

from sqlalchemy import JSON, cast, func


def normalize_text(value: str) -> str:
    """Normalize user search input without database-collation assumptions."""

    return unicodedata.normalize("NFKC", value).strip()


def _escaped_like(value: str) -> str:
    return value.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


def portable_contains(column: Any, value: str) -> Any:
    """Return the frozen portable substring contract.

    ASCII input is case-insensitive. Non-ASCII input is NFKC-normalized and
    exact-case/code-point matched. This deliberately avoids pretending that
    SQLite's built-in LOWER and a PostgreSQL locale have equivalent Unicode
    case-folding behavior.
    """

    normalized = normalize_text(value)
    if normalized.isascii():
        return func.lower(column).like(
            f"%{_escaped_like(normalized.lower())}%",
            escape="\\",
        )
    return column.like(f"%{_escaped_like(normalized)}%", escape="\\")


def portable_case_insensitive_equal(column: Any, value: str) -> Any:
    """Match ASCII identifiers case-insensitively and Unicode identifiers exactly."""

    normalized = normalize_text(value)
    if normalized.isascii():
        return func.lower(column) == normalized.lower()
    return column == normalized


def json_text_field(db, column, *path, integer=False):
    """Task event payloads are historical text on both supported databases."""
    if db.get_bind().dialect.name == "sqlite":
        return func.json_extract(column, "$." + ".".join(path))
    value = cast(column, JSON)
    for key in path:
        value = value[key]
    return value.as_integer() if integer else value.as_string()
