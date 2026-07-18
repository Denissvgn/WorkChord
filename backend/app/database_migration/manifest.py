"""Deterministic, checksummed, secret-free operational documents."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Mapping


CHECKSUM_FIELD = "document_sha256"


class ManifestError(ValueError):
    """A migration document is malformed or has lost integrity."""


def canonical_json_bytes(value: Any) -> bytes:
    """Encode JSON deterministically without ASCII-destroying Unicode."""

    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def seal_document(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Return a shallow copy carrying a checksum over every other field."""

    if CHECKSUM_FIELD in payload:
        raise ManifestError(f"{CHECKSUM_FIELD} is reserved")
    document = dict(payload)
    document[CHECKSUM_FIELD] = sha256_bytes(canonical_json_bytes(document))
    return document


def verify_document(document: Mapping[str, Any]) -> str:
    """Verify and return the document checksum."""

    expected = document.get(CHECKSUM_FIELD)
    if not isinstance(expected, str) or len(expected) != 64:
        raise ManifestError(f"Document is missing a valid {CHECKSUM_FIELD}")
    payload = dict(document)
    payload.pop(CHECKSUM_FIELD, None)
    actual = sha256_bytes(canonical_json_bytes(payload))
    if actual != expected:
        raise ManifestError(
            f"Document checksum mismatch: expected {expected}, calculated {actual}"
        )
    return actual


def read_document(path: Path) -> dict[str, Any]:
    """Read one checksummed JSON object from disk."""

    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ManifestError(f"Could not read migration document {path.name}") from exc
    if not isinstance(value, dict):
        raise ManifestError("Migration document root must be an object")
    verify_document(value)
    return value


def write_document(path: Path, payload: Mapping[str, Any]) -> dict[str, Any]:
    """Atomically write a checksummed JSON document and fsync its directory."""

    document = seal_document(payload)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    encoded = json.dumps(
        document,
        ensure_ascii=False,
        allow_nan=False,
        indent=2,
        sort_keys=True,
    ).encode("utf-8") + b"\n"
    try:
        with temporary.open("xb") as handle:
            os.chmod(temporary, 0o600)
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary.exists():
            temporary.unlink()
    return document
