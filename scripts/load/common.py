"""Shared, fail-closed contracts for the WorkChord load and qualification tools."""

from __future__ import annotations

from datetime import UTC, datetime
from functools import lru_cache
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Mapping
from urllib.parse import urlsplit

from app.autonomy.contracts.postgresql import (
    ContractBundleError,
    PostgreSQLContractBundle,
    load_postgresql_contract_bundle,
)

CAPACITY_CONTRACT_MEMBER = "postgresql-capacity-contract-v1.json"
DATA_LIFECYCLE_POLICY_MEMBER = "postgresql-data-lifecycle-policy-v1.json"
LOAD_RESULT_SCHEMA_MEMBER = "postgresql-load-result-v1.schema.json"
QUALIFICATION_SCHEMA_MEMBER = "postgresql-precutover-qualification-v1.schema.json"
RESILIENCE_SCHEMA_MEMBER = "postgresql-resilience-observations-v1.schema.json"
CAPACITY_CONTRACT_REFERENCE = (
    "backend/app/autonomy/contracts/postgresql/"
    "postgresql-capacity-contract-v1.json"
)
HTTP_TOOL = {"name": "httpx", "version": "0.28.1"}
MCP_TOOL = {"name": "mcp", "version": "1.28.1"}
DOCUMENT_CHECKSUM_FIELD = "document_sha256"


class QualificationInputError(ValueError):
    """A workload or evidence input is unsafe, stale, or incomplete."""


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def seal_document(payload: Mapping[str, Any]) -> dict[str, Any]:
    if DOCUMENT_CHECKSUM_FIELD in payload:
        raise QualificationInputError(
            f"{DOCUMENT_CHECKSUM_FIELD} is reserved"
        )
    document = dict(payload)
    document[DOCUMENT_CHECKSUM_FIELD] = sha256_bytes(
        canonical_json_bytes(document)
    )
    return document


def verify_document(document: Mapping[str, Any]) -> str:
    expected = document.get(DOCUMENT_CHECKSUM_FIELD)
    if not isinstance(expected, str) or len(expected) != 64:
        raise QualificationInputError(
            f"Document is missing {DOCUMENT_CHECKSUM_FIELD}"
        )
    payload = dict(document)
    payload.pop(DOCUMENT_CHECKSUM_FIELD, None)
    actual = sha256_bytes(canonical_json_bytes(payload))
    if actual != expected:
        raise QualificationInputError(
            f"Document checksum mismatch: expected {expected}, calculated {actual}"
        )
    return actual


def read_json_object(path: Path, *, sealed: bool = False) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise QualificationInputError(f"Could not read JSON object {path}") from exc
    if not isinstance(value, dict):
        raise QualificationInputError(f"JSON root must be an object: {path}")
    if sealed:
        verify_document(value)
    return value


@lru_cache(maxsize=1)
def contract_bundle() -> PostgreSQLContractBundle:
    try:
        return load_postgresql_contract_bundle()
    except ContractBundleError as exc:
        raise QualificationInputError(
            "Packaged PostgreSQL contract bundle is unavailable or invalid"
        ) from exc


def contract_member_json(member: str) -> dict[str, Any]:
    try:
        value = contract_bundle().member_json(member)
    except ContractBundleError as exc:
        raise QualificationInputError(
            f"Packaged PostgreSQL contract member is unavailable: {member}"
        ) from exc
    if not isinstance(value, dict):
        raise QualificationInputError(
            f"Packaged PostgreSQL contract member must be an object: {member}"
        )
    return value


def contract_member_sha256(member: str) -> str:
    try:
        payload = contract_bundle().members[member]
    except KeyError as exc:
        raise QualificationInputError(
            f"Packaged PostgreSQL contract member is unavailable: {member}"
        ) from exc
    return sha256_bytes(payload)


def atomic_write_json(
    path: Path,
    payload: Mapping[str, Any],
    *,
    sealed: bool = True,
    mode: int = 0o600,
) -> dict[str, Any]:
    document = seal_document(payload) if sealed else dict(payload)
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
            os.chmod(temporary, mode)
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


def capacity_contract() -> dict[str, Any]:
    contract = contract_member_json(CAPACITY_CONTRACT_MEMBER)
    if (
        contract.get("status") != "approved"
        or contract.get("contract_id") != "workchord-postgresql-capacity-v1"
    ):
        raise QualificationInputError("Capacity contract is not approved v1")
    return contract


def contract_sha256() -> str:
    return contract_member_sha256(CAPACITY_CONTRACT_MEMBER)


def traffic_profile(contract: Mapping[str, Any], profile_id: str) -> dict[str, Any]:
    profiles = contract.get("traffic", {}).get("profiles", [])
    profile = next(
        (item for item in profiles if item.get("id") == profile_id),
        None,
    )
    if not isinstance(profile, dict):
        raise QualificationInputError(f"Unknown traffic profile: {profile_id}")
    if profile.get("operation_mix") == "exactly mixed_peak_v1":
        mixed = traffic_profile(contract, "mixed_peak_v1")
        profile = {**mixed, **profile, "operations": mixed["operations"]}
    return profile


def utc_now_text() -> str:
    return datetime.now(UTC).isoformat()


def authorized_base_url(
    base_url: str,
    *,
    authorize_host: str,
    environment: str,
    production_authorization: str | None,
    change_id: str | None,
) -> str:
    parsed = urlsplit(base_url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise QualificationInputError("Base URL must be absolute HTTP(S)")
    resolved_host = parsed.netloc
    if authorize_host != resolved_host:
        raise QualificationInputError(
            f"Resolved host {resolved_host!r} differs from --authorize-host"
        )
    if parsed.username or parsed.password:
        raise QualificationInputError("Base URL must not contain credentials")
    if environment not in {"test", "rehearsal", "production"}:
        raise QualificationInputError(
            "Environment must be test, rehearsal, or production"
        )
    if environment == "production":
        expected = os.getenv("WORKCHORD_PRODUCTION_LOAD_AUTHORIZATION")
        if (
            not expected
            or production_authorization != expected
            or not change_id
            or len(change_id.strip()) < 3
        ):
            raise QualificationInputError(
                "Production load requires the exact environment authorization and a change ID"
            )
    elif production_authorization is not None:
        raise QualificationInputError(
            "Production authorization must not be supplied outside production"
        )
    return base_url.rstrip("/")
