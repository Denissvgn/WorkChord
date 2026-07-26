"""Canonical serialization and secret-boundary helpers."""

from __future__ import annotations

import json
import math
import re
from collections.abc import Mapping, Sequence
from datetime import date, datetime
from enum import Enum
from hashlib import sha256
from typing import Any

from pydantic import BaseModel, ConfigDict


MAX_CONTRACT_DEPTH = 32
MAX_CONTRACT_ITEMS = 20_000
MAX_STRING_BYTES = 1_048_576


class StrictContractModel(BaseModel):
    """Base class shared by immutable, extra-forbidden contracts."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        str_strip_whitespace=True,
        validate_default=True,
        allow_inf_nan=False,
    )


def _json_value(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json", by_alias=True, exclude_none=False)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, datetime | date):
        return value.isoformat()
    if isinstance(value, Mapping):
        return {str(key): _json_value(item) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, str | bytes | bytearray):
        return [_json_value(item) for item in value]
    return value


def canonical_json_bytes(value: Any) -> bytes:
    """Serialize one contract using stable UTF-8 JSON bytes.

    Floats that JSON would otherwise spell as NaN or Infinity are rejected.
    The serializer intentionally does not omit null/default fields; a digest is
    over the complete validated contract, not a caller-selected projection.
    """

    return json.dumps(
        _json_value(value),
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_hex(value: bytes | str | Any) -> str:
    """Return a lowercase SHA-256 digest for bytes, text, or canonical data."""

    if isinstance(value, bytes):
        payload = value
    elif isinstance(value, str):
        payload = value.encode("utf-8")
    else:
        payload = canonical_json_bytes(value)
    return sha256(payload).hexdigest()


_SECRET_FIELD_NAMES = {
    "api_key",
    "api_token",
    "authorization",
    "authorization_header",
    "client_secret",
    "credential",
    "credentials",
    "database_url",
    "password",
    "private_key",
    "private_key_pem",
    "secret",
    "secret_key",
    "token",
}
_SECRET_VALUE_PATTERNS = (
    re.compile(r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----"),
    re.compile(r"(?i)\bbearer\s+[a-z0-9._~+/=-]{12,}"),
    re.compile(r"\bpmag_[A-Za-z0-9_-]{20,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"[a-z][a-z0-9+.-]*://[^/@\s:]+:[^/@\s]+@", re.IGNORECASE),
)


class SecretMaterialError(ValueError):
    """Raised when a portable/evidence contract contains credential material."""


def ensure_secret_free(value: Any) -> None:
    """Reject credential-shaped fields/values and pathological contract sizes."""

    item_count = 0

    def visit(item: Any, *, path: str, depth: int) -> None:
        nonlocal item_count
        item_count += 1
        if item_count > MAX_CONTRACT_ITEMS:
            raise ValueError(f"Contract exceeds {MAX_CONTRACT_ITEMS} nested items")
        if depth > MAX_CONTRACT_DEPTH:
            raise ValueError(f"Contract exceeds nesting depth {MAX_CONTRACT_DEPTH}")
        if isinstance(item, BaseModel):
            visit(item.model_dump(mode="json"), path=path, depth=depth + 1)
            return
        if isinstance(item, Mapping):
            for raw_key, nested in item.items():
                key = str(raw_key).strip().lower()
                child_path = f"{path}.{key}" if path else key
                if key in _SECRET_FIELD_NAMES:
                    raise SecretMaterialError(
                        f"Secret-bearing field is forbidden at {child_path}"
                    )
                visit(nested, path=child_path, depth=depth + 1)
            return
        if isinstance(item, Sequence) and not isinstance(
            item, str | bytes | bytearray
        ):
            for index, nested in enumerate(item):
                visit(nested, path=f"{path}[{index}]", depth=depth + 1)
            return
        if isinstance(item, float) and not math.isfinite(item):
            raise ValueError(f"Non-finite number is forbidden at {path or '$'}")
        if isinstance(item, str):
            if len(item.encode("utf-8")) > MAX_STRING_BYTES:
                raise ValueError(f"String exceeds {MAX_STRING_BYTES} bytes at {path}")
            for pattern in _SECRET_VALUE_PATTERNS:
                if pattern.search(item):
                    raise SecretMaterialError(
                        f"Credential-shaped value is forbidden at {path or '$'}"
                    )

    visit(value, path="", depth=0)
