"""Signed, fail-closed evidence for PostgreSQL rehearsals and cutover.

The coordinator never performs a database or deployment mutation.  It turns
reviewed operator observations into immutable reports only after the complete
cutover contract has been satisfied.  Production automation can therefore use
the reports as gates without giving this module credentials or control-plane
access.
"""

from __future__ import annotations

import base64
from datetime import UTC, datetime, timedelta
import json
import os
from pathlib import Path
import re
import stat
from typing import Any, Mapping

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)

from app.database_migration.manifest import (
    ManifestError,
    canonical_json_bytes,
    read_document,
    sha256_bytes,
    verify_document,
    write_document,
)


SCHEMA_VERSION = 1
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
IMAGE_PATTERN = re.compile(r"^.+@sha256:[0-9a-f]{64}$")
MAX_CUTOVER_SECONDS = 180 * 60
MAX_ROLLBACK_SECONDS = 30 * 60
MAX_RESTORE_RTO_SECONDS = 30 * 60

GATE_IDS = tuple(f"C{index:02d}" for index in range(1, 14))
GATE_HARD_STOPS_SECONDS = {
    "C02": 10 * 60,
    "C03": 20 * 60,
    "C04": 35 * 60,
    "C05": 35 * 60,
    "C06": 50 * 60,
    "C07": 75 * 60,
    "C08": 90 * 60,
    "C09": 120 * 60,
    "C10": 130 * 60,
    "C11": 150 * 60,
    "C12": 155 * 60,
    "C13": 180 * 60,
}
GATE_OWNER_ROLES = {
    "C01": "change_commander",
    "C02": "application_operator",
    "C03": "observer",
    "C04": "database_operator",
    "C05": "database_operator",
    "C06": "database_operator",
    "C07": "database_operator",
    "C08": "observer",
    "C09": "database_operator",
    "C10": "application_operator",
    "C11": "application_operator",
    "C12": "change_commander",
    "C13": "change_commander",
}
OPERATOR_ROLES = frozenset(
    {
        "change_commander",
        "product_owner",
        "database_operator",
        "application_operator",
        "observer",
        "incident_commander",
    }
)
DOCUMENTATION_CHECKS = frozenset(
    {
        "clean_install",
        "source_preflight",
        "target_bootstrap_and_copy",
        "rollback_before_first_write",
        "forward_recovery_after_first_write",
        "backup_restore",
        "validation_smoke",
        "released_command_help",
        "stop_condition_tabletop",
    }
)
QUALIFICATION_GATES = frozenset(
    {
        "three_consecutive_complete_runs",
        "frozen_release_identity",
        "exact_capacity_shape",
        "traffic_and_latency",
        "resource_and_growth",
        "fault_and_recovery",
        "backup_restore_rpo_rto",
        "domain_integrity",
        "final_ci_matrix",
    }
)
CAPACITY_CLAIM = {
    "browser_identities": 1250,
    "active_browser_sessions": 250,
    "concurrent_agent_clients": 200,
    "authenticated_people_claim": False,
}
REHEARSAL_ATTESTATION = (
    "This report was produced from the exact released runbook and artifacts; "
    "it contains no manual or undocumented step and no unexplained difference."
)
SERIES_ATTESTATION = (
    "The abort drill is separate and the listed full rehearsals are the first "
    "two consecutive successful attempts after it; no intervening failed, "
    "deviating, manual, or undocumented attempt is omitted."
)
PRODUCTION_ATTESTATION = (
    "PostgreSQL is the sole writable source of truth, SQLite remains read-only, "
    "and every pre-write gate and authorization was satisfied before writes reopened."
)
QUALIFICATION_ATTESTATION = (
    "The listed attempts are the final three consecutive qualification attempts "
    "for this frozen release, and no failed or excluded attempt is omitted."
)


class CutoverEvidenceError(ValueError):
    """A cutover input is unsafe, stale, incomplete, or internally inconsistent."""


def _exact_keys(
    value: Mapping[str, Any],
    required: set[str] | frozenset[str],
    *,
    context: str,
    optional: set[str] | frozenset[str] = frozenset(),
) -> None:
    missing = set(required) - set(value)
    extra = set(value) - set(required) - set(optional)
    if missing or extra:
        raise CutoverEvidenceError(
            f"{context} fields differ: missing={sorted(missing)}, extra={sorted(extra)}"
        )


def _text(value: object, *, field: str, minimum: int = 3) -> str:
    if not isinstance(value, str) or len(value.strip()) < minimum:
        raise CutoverEvidenceError(f"{field} must be nonempty text")
    return value.strip()


def _sha256(value: object, *, field: str) -> str:
    if not isinstance(value, str) or SHA256_PATTERN.fullmatch(value) is None:
        raise CutoverEvidenceError(f"{field} must be a lowercase SHA-256")
    return value


def _time(value: object, *, field: str) -> datetime:
    if not isinstance(value, str):
        raise CutoverEvidenceError(f"{field} must be an ISO-8601 timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise CutoverEvidenceError(f"{field} must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None:
        raise CutoverEvidenceError(f"{field} must include a timezone")
    return parsed.astimezone(UTC)


def _number(value: object, *, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CutoverEvidenceError(f"{field} must be numeric")
    result = float(value)
    if result < 0:
        raise CutoverEvidenceError(f"{field} must not be negative")
    return result


def _require_new_output(path: Path) -> None:
    if path.exists() or path.is_symlink():
        raise CutoverEvidenceError(
            f"Cutover output already exists and will not be overwritten: {path}"
        )


def _read_json_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise CutoverEvidenceError(f"Could not read JSON object {path}") from exc
    if not isinstance(value, dict):
        raise CutoverEvidenceError(f"JSON root must be an object: {path}")
    return value


def _reject_secret_material(value: object, *, path: str = "<root>") -> None:
    sensitive_keys = {
        "password",
        "access_token",
        "refresh_token",
        "session_token",
        "api_key",
        "private_key",
        "database_url",
        "connection_url",
        "dsn",
        "authorization_header",
        "cookie",
    }
    if isinstance(value, Mapping):
        for key, item in value.items():
            normalized = str(key).strip().lower().replace("-", "_")
            if normalized in sensitive_keys:
                raise CutoverEvidenceError(
                    f"Secret-bearing field {path}.{key} is prohibited"
                )
            _reject_secret_material(item, path=f"{path}.{key}")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_secret_material(item, path=f"{path}[{index}]")
    elif isinstance(value, str):
        if "PRIVATE KEY-----" in value:
            raise CutoverEvidenceError(f"Private key material is prohibited at {path}")
        if "://" in value:
            from urllib.parse import urlsplit

            parsed = urlsplit(value)
            if parsed.username is not None or parsed.password is not None:
                raise CutoverEvidenceError(
                    f"Credential-bearing URL is prohibited at {path}"
                )


def _private_key(path: Path) -> Ed25519PrivateKey:
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode & 0o077:
        raise CutoverEvidenceError(
            "Signing key must not be readable or writable by group/other"
        )
    password_text = os.getenv("WORKCHORD_CUTOVER_SIGNING_PASSWORD")
    password = password_text.encode("utf-8") if password_text else None
    key = serialization.load_pem_private_key(path.read_bytes(), password=password)
    if not isinstance(key, Ed25519PrivateKey):
        raise CutoverEvidenceError("Signing key must be Ed25519")
    return key


def _canonical_public_key(value: bytes) -> tuple[Ed25519PublicKey, bytes]:
    key = serialization.load_pem_public_key(value)
    if not isinstance(key, Ed25519PublicKey):
        raise CutoverEvidenceError("Trusted key must be an Ed25519 public key")
    encoded = key.public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return key, encoded


def _sign_document(
    output: Path,
    payload: Mapping[str, Any],
    *,
    signing_key: Path,
    signer: str,
) -> dict[str, Any]:
    _require_new_output(output)
    signer_name = _text(signer, field="signer")
    if "signature" in payload or "document_sha256" in payload:
        raise CutoverEvidenceError("Unsigned payload contains reserved signature fields")
    key = _private_key(signing_key)
    public_pem = key.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    signed_bytes = canonical_json_bytes(payload)
    document = {
        **payload,
        "signature": {
            "algorithm": "Ed25519",
            "signer": signer_name,
            "public_key_pem": public_pem.decode("ascii"),
            "public_key_sha256": sha256_bytes(public_pem),
            "signed_payload_sha256": sha256_bytes(signed_bytes),
            "value_base64": base64.b64encode(key.sign(signed_bytes)).decode("ascii"),
        },
    }
    return write_document(output, document)


def verify_signed_document(
    document: Mapping[str, Any],
    *,
    trusted_public_key: Path,
    expected_kind: str | None = None,
) -> str:
    """Verify the checksum, Ed25519 signature, and external trust-key pin."""

    try:
        verify_document(document)
    except ManifestError as exc:
        raise CutoverEvidenceError(str(exc)) from exc
    if expected_kind is not None and document.get("kind") != expected_kind:
        raise CutoverEvidenceError(
            f"Signed document kind must be {expected_kind!r}"
        )
    signature = document.get("signature")
    if not isinstance(signature, Mapping):
        raise CutoverEvidenceError("Signed document has no signature object")
    _exact_keys(
        signature,
        {
            "algorithm",
            "signer",
            "public_key_pem",
            "public_key_sha256",
            "signed_payload_sha256",
            "value_base64",
        },
        context="signature",
    )
    if signature.get("algorithm") != "Ed25519":
        raise CutoverEvidenceError("Signature algorithm must be Ed25519")
    trusted_key, trusted_pem = _canonical_public_key(trusted_public_key.read_bytes())
    try:
        _, embedded_pem = _canonical_public_key(
            _text(signature.get("public_key_pem"), field="signature.public_key_pem").encode(
                "ascii"
            )
        )
    except UnicodeEncodeError as exc:
        raise CutoverEvidenceError("Embedded public key must be ASCII PEM") from exc
    if embedded_pem != trusted_pem:
        raise CutoverEvidenceError("Signed document key is not the trusted public key")
    if signature.get("public_key_sha256") != sha256_bytes(trusted_pem):
        raise CutoverEvidenceError("Signed document public-key digest differs")
    base = dict(document)
    base.pop("document_sha256", None)
    base.pop("signature", None)
    signed_bytes = canonical_json_bytes(base)
    if signature.get("signed_payload_sha256") != sha256_bytes(signed_bytes):
        raise CutoverEvidenceError("Signed payload digest differs")
    try:
        encoded_signature = base64.b64decode(
            _text(signature.get("value_base64"), field="signature.value_base64"),
            validate=True,
        )
        trusted_key.verify(encoded_signature, signed_bytes)
    except (InvalidSignature, ValueError) as exc:
        raise CutoverEvidenceError("Ed25519 signature is invalid") from exc
    return _text(signature.get("signer"), field="signature.signer")


def _release_identity(release: Mapping[str, Any]) -> dict[str, Any]:
    if (
        release.get("kind") != "workchord-postgresql-frozen-release"
        or release.get("schema_version") != 1
        or release.get("status") != "frozen"
    ):
        raise CutoverEvidenceError("Release manifest is not frozen release v1")
    commit = _text(release.get("commit"), field="release.commit", minimum=40)
    if COMMIT_PATTERN.fullmatch(commit) is None:
        raise CutoverEvidenceError("Frozen release commit must be a full lowercase SHA")
    images = release.get("images")
    if (
        not isinstance(images, list)
        or len(set(images)) < 3
        or any(not isinstance(item, str) or IMAGE_PATTERN.fullmatch(item) is None for item in images)
    ):
        raise CutoverEvidenceError("Frozen release images must be unique digest pins")
    body = dict(release)
    body.pop("document_sha256", None)
    fingerprint = _sha256(body.pop("fingerprint", None), field="release.fingerprint")
    if fingerprint != sha256_bytes(canonical_json_bytes(body)):
        raise CutoverEvidenceError("Frozen release fingerprint differs")
    return {
        "fingerprint": fingerprint,
        "manifest_sha256": _sha256(
            release.get("document_sha256"), field="release.document_sha256"
        ),
        "commit": commit,
        "images": sorted(images),
    }


def _validate_release_reference(
    reference: object,
    expected: Mapping[str, Any],
    *,
    context: str,
) -> dict[str, Any]:
    if not isinstance(reference, Mapping):
        raise CutoverEvidenceError(f"{context} release reference must be an object")
    _exact_keys(
        reference,
        {"fingerprint", "manifest_sha256", "commit", "images"},
        context=f"{context}.release",
    )
    actual = {
        "fingerprint": _sha256(reference.get("fingerprint"), field=f"{context}.fingerprint"),
        "manifest_sha256": _sha256(
            reference.get("manifest_sha256"), field=f"{context}.manifest_sha256"
        ),
        "commit": _text(reference.get("commit"), field=f"{context}.commit", minimum=40),
        "images": sorted(reference.get("images", []))
        if isinstance(reference.get("images"), list)
        else None,
    }
    if actual != dict(expected):
        raise CutoverEvidenceError(f"{context} release identity differs")
    return actual


def _validate_unbound_release_reference(
    reference: object,
    *,
    context: str,
) -> dict[str, Any]:
    if not isinstance(reference, Mapping):
        raise CutoverEvidenceError(f"{context} release reference must be an object")
    _exact_keys(
        reference,
        {"fingerprint", "manifest_sha256", "commit", "images"},
        context=f"{context}.release",
    )
    commit = _text(
        reference.get("commit"), field=f"{context}.release.commit", minimum=40
    )
    if COMMIT_PATTERN.fullmatch(commit) is None:
        raise CutoverEvidenceError(f"{context} release commit is invalid")
    images = reference.get("images")
    if (
        not isinstance(images, list)
        or len(set(images)) < 3
        or any(
            not isinstance(item, str) or IMAGE_PATTERN.fullmatch(item) is None
            for item in images
        )
    ):
        raise CutoverEvidenceError(f"{context} release images are invalid")
    return {
        "fingerprint": _sha256(
            reference.get("fingerprint"), field=f"{context}.release.fingerprint"
        ),
        "manifest_sha256": _sha256(
            reference.get("manifest_sha256"),
            field=f"{context}.release.manifest_sha256",
        ),
        "commit": commit,
        "images": sorted(images),
    }


def _validate_qualification(
    document: Mapping[str, Any],
    *,
    release: Mapping[str, Any],
    trusted_public_key: Path,
) -> None:
    verify_signed_document(
        document,
        trusted_public_key=trusted_public_key,
        expected_kind="workchord-postgresql-precutover-qualification",
    )
    if document.get("schema_version") != 1 or document.get("status") != "qualified":
        raise CutoverEvidenceError("Pre-cutover qualification is not qualified v1")
    if document.get("capacity_claim") != CAPACITY_CLAIM:
        raise CutoverEvidenceError("Qualification capacity claim differs")
    release_contract = release.get("capacity_contract")
    if not isinstance(release_contract, Mapping) or document.get(
        "capacity_contract"
    ) != dict(release_contract):
        raise CutoverEvidenceError("Qualification capacity contract differs")
    frozen = document.get("frozen_release")
    if not isinstance(frozen, Mapping):
        raise CutoverEvidenceError("Qualification frozen release is missing")
    expected_release = _release_identity(release)
    if {
        "fingerprint": frozen.get("fingerprint"),
        "manifest_sha256": frozen.get("manifest_sha256"),
        "commit": frozen.get("commit"),
        "images": sorted(frozen.get("images", []))
        if isinstance(frozen.get("images"), list)
        else None,
    } != expected_release:
        raise CutoverEvidenceError("Qualification was signed for another release")
    runs = document.get("consecutive_runs")
    if not isinstance(runs, list) or len(runs) != 3:
        raise CutoverEvidenceError("Qualification must contain exactly three runs")
    attempts = [item.get("attempt_number") for item in runs if isinstance(item, Mapping)]
    if (
        len(attempts) != 3
        or any(not isinstance(item, int) or isinstance(item, bool) for item in attempts)
        or attempts != list(range(attempts[0], attempts[0] + 3))
        or len({item.get("run_id") for item in runs}) != 3
    ):
        raise CutoverEvidenceError("Qualification runs are not unique and consecutive")
    run_times: list[tuple[datetime, datetime]] = []
    for index, item in enumerate(runs):
        if not isinstance(item, Mapping):
            raise CutoverEvidenceError("Qualification run reference is invalid")
        _sha256(
            item.get("bundle_sha256"),
            field=f"qualification.runs[{index}].bundle_sha256",
        )
        started = _time(
            item.get("started_at"), field=f"qualification.runs[{index}].started_at"
        )
        completed = _time(
            item.get("completed_at"),
            field=f"qualification.runs[{index}].completed_at",
        )
        if started >= completed:
            raise CutoverEvidenceError("Qualification run timing is invalid")
        run_times.append((started, completed))
    if any(
        first[1] > second[0]
        for first, second in zip(run_times, run_times[1:])
    ):
        raise CutoverEvidenceError("Qualification runs overlap")
    if _time(document.get("created_at"), field="qualification.created_at") < run_times[
        -1
    ][1]:
        raise CutoverEvidenceError("Qualification report predates its final run")
    gates = document.get("qualification_gates")
    if not isinstance(gates, Mapping) or set(gates) != QUALIFICATION_GATES or any(
        not isinstance(item, Mapping) or item.get("status") != "passed"
        for item in gates.values()
    ):
        raise CutoverEvidenceError("Qualification does not pass every exact gate")
    if document.get("attestation") != QUALIFICATION_ATTESTATION:
        raise CutoverEvidenceError("Qualification omission attestation differs")


def _validate_documentation(
    document: Mapping[str, Any],
    *,
    expected_release: Mapping[str, Any] | None,
    trusted_public_key: Path | None,
    signed: bool,
) -> None:
    required = {
        "kind",
        "schema_version",
        "walkthrough_id",
        "completed_at",
        "status",
        "release",
        "reviewer",
        "checks",
        "unresolved_steps",
        "evidence_sha256",
    }
    optional = {"signature", "document_sha256"} if signed else frozenset()
    _exact_keys(document, required, optional=optional, context="documentation walkthrough")
    if (
        document.get("kind") != "workchord-postgresql-documentation-walkthrough"
        or document.get("schema_version") != 1
        or document.get("status") != "passed"
    ):
        raise CutoverEvidenceError("Documentation walkthrough is not passed v1")
    _text(document.get("walkthrough_id"), field="walkthrough_id", minimum=8)
    walkthrough_completed = _time(
        document.get("completed_at"), field="walkthrough.completed_at"
    )
    if walkthrough_completed > datetime.now(UTC) + timedelta(minutes=1):
        raise CutoverEvidenceError("Documentation walkthrough is future-dated")
    reviewer = document.get("reviewer")
    if not isinstance(reviewer, Mapping):
        raise CutoverEvidenceError("Documentation reviewer is required")
    _exact_keys(reviewer, {"identity", "independent"}, context="documentation reviewer")
    _text(reviewer.get("identity"), field="reviewer.identity")
    if reviewer.get("independent") is not True:
        raise CutoverEvidenceError("Documentation reviewer must be independent")
    checks = document.get("checks")
    if not isinstance(checks, Mapping) or set(checks) != DOCUMENTATION_CHECKS or any(
        value != "passed" for value in checks.values()
    ):
        raise CutoverEvidenceError("Documentation walkthrough does not pass every check")
    if document.get("unresolved_steps") != []:
        raise CutoverEvidenceError("Documentation walkthrough has unresolved steps")
    evidence = document.get("evidence_sha256")
    if (
        not isinstance(evidence, list)
        or not evidence
        or len(evidence) != len(set(evidence))
        or any(SHA256_PATTERN.fullmatch(str(item)) is None for item in evidence)
    ):
        raise CutoverEvidenceError("Documentation evidence checksums are invalid")
    reference = document.get("release")
    if expected_release is None:
        _validate_unbound_release_reference(reference, context="documentation")
    else:
        _validate_release_reference(reference, expected_release, context="documentation")
    _reject_secret_material(document)
    if signed:
        if trusted_public_key is None:
            raise CutoverEvidenceError("Trusted documentation public key is required")
        verify_signed_document(
            document,
            trusted_public_key=trusted_public_key,
            expected_kind="workchord-postgresql-documentation-walkthrough",
        )


def attest_documentation(
    *,
    input_path: Path,
    release_manifest_path: Path,
    signing_key: Path,
    signer: str,
    output_path: Path,
) -> dict[str, Any]:
    release = read_document(release_manifest_path)
    release_identity = _release_identity(release)
    payload = _read_json_object(input_path)
    _validate_documentation(
        payload,
        expected_release=release_identity,
        trusted_public_key=None,
        signed=False,
    )
    return _sign_document(output_path, payload, signing_key=signing_key, signer=signer)


def _validate_source(value: object, *, context: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise CutoverEvidenceError(f"{context} source must be an object")
    _exact_keys(
        value,
        {
            "deployment_id",
            "sqlite_identifier",
            "revision",
            "snapshot_sha256",
            "manifest_sha256",
        },
        context=f"{context}.source",
    )
    return {
        "deployment_id": _text(value.get("deployment_id"), field=f"{context}.source.deployment_id"),
        "sqlite_identifier": _text(
            value.get("sqlite_identifier"), field=f"{context}.source.sqlite_identifier"
        ),
        "revision": _text(value.get("revision"), field=f"{context}.source.revision"),
        "snapshot_sha256": _sha256(
            value.get("snapshot_sha256"), field=f"{context}.source.snapshot_sha256"
        ),
        "manifest_sha256": _sha256(
            value.get("manifest_sha256"), field=f"{context}.source.manifest_sha256"
        ),
    }


def _source_scope(source: Mapping[str, Any]) -> dict[str, str]:
    return {
        "deployment_id": str(source["deployment_id"]),
        "sqlite_identifier": str(source["sqlite_identifier"]),
        "revision": str(source["revision"]),
    }


def _validate_source_scope(value: object, *, context: str) -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise CutoverEvidenceError(f"{context} source scope must be an object")
    _exact_keys(
        value,
        {"deployment_id", "sqlite_identifier", "revision"},
        context=f"{context}.source_scope",
    )
    return {
        key: _text(value.get(key), field=f"{context}.source_scope.{key}")
        for key in ("deployment_id", "sqlite_identifier", "revision")
    }


def _validate_target(value: object, *, context: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        raise CutoverEvidenceError(f"{context} target must be an object")
    _exact_keys(
        value,
        {"identifier", "identity_sha256", "managed_resource_id", "revision"},
        context=f"{context}.target",
    )
    return {
        "identifier": _text(value.get("identifier"), field=f"{context}.target.identifier"),
        "identity_sha256": _sha256(
            value.get("identity_sha256"), field=f"{context}.target.identity_sha256"
        ),
        "managed_resource_id": _text(
            value.get("managed_resource_id"),
            field=f"{context}.target.managed_resource_id",
        ),
        "revision": _text(value.get("revision"), field=f"{context}.target.revision"),
    }


def _validate_operators(value: object, *, context: str) -> dict[str, str]:
    if not isinstance(value, Mapping) or set(value) != OPERATOR_ROLES:
        raise CutoverEvidenceError(f"{context} must name every exact operator role")
    operators = {
        key: _text(item, field=f"{context}.{key}") for key, item in value.items()
    }
    if operators["change_commander"] == operators["observer"]:
        raise CutoverEvidenceError("Change commander and observer must be independent")
    if operators["database_operator"] == operators["application_operator"]:
        raise CutoverEvidenceError(
            "Database and application operators must be independently identified"
        )
    return operators


def _validate_execution(document: Mapping[str, Any], *, sealed: bool) -> dict[str, Any]:
    required = {
        "kind",
        "schema_version",
        "execution_id",
        "change_id",
        "environment",
        "mode",
        "sequence_number",
        "started_at",
        "completed_at",
        "release",
        "dependencies",
        "source",
        "target",
        "operators",
        "gates",
        "decision",
        "point_of_no_return",
        "outcome",
    }
    optional = {"document_sha256"} if sealed else frozenset()
    _exact_keys(document, required, optional=optional, context="cutover execution")
    if (
        document.get("kind") != "workchord-postgresql-cutover-execution"
        or document.get("schema_version") != 1
    ):
        raise CutoverEvidenceError("Execution record must be cutover execution v1")
    if sealed:
        try:
            verify_document(document)
        except ManifestError as exc:
            raise CutoverEvidenceError(str(exc)) from exc
    _reject_secret_material(document)
    _text(document.get("execution_id"), field="execution_id", minimum=8)
    _text(document.get("change_id"), field="change_id")
    environment = document.get("environment")
    mode = document.get("mode")
    if environment not in {"rehearsal", "production"}:
        raise CutoverEvidenceError("Execution environment must be rehearsal or production")
    if mode not in {"abort_drill", "full"}:
        raise CutoverEvidenceError("Execution mode must be abort_drill or full")
    if environment == "production" and mode != "full":
        raise CutoverEvidenceError("Production execution must be a full cutover")
    sequence = document.get("sequence_number")
    if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 0:
        raise CutoverEvidenceError("Execution sequence number must be a nonnegative integer")
    if mode == "abort_drill" and sequence != 0:
        raise CutoverEvidenceError("Abort drill sequence number must be zero")
    if mode == "full" and sequence < 1:
        raise CutoverEvidenceError("Full execution sequence number must be positive")

    started_at = _time(document.get("started_at"), field="execution.started_at")
    completed_at = _time(document.get("completed_at"), field="execution.completed_at")
    if completed_at < started_at:
        raise CutoverEvidenceError("Execution completion predates its start")
    if completed_at > datetime.now(UTC) + timedelta(minutes=1):
        raise CutoverEvidenceError("Execution record is future-dated")
    release_reference = document.get("release")
    if not isinstance(release_reference, Mapping):
        raise CutoverEvidenceError("Execution release reference is missing")
    _exact_keys(
        release_reference,
        {"fingerprint", "manifest_sha256", "commit", "images"},
        context="execution.release",
    )
    _sha256(release_reference.get("fingerprint"), field="execution.release.fingerprint")
    _sha256(
        release_reference.get("manifest_sha256"),
        field="execution.release.manifest_sha256",
    )
    commit = _text(release_reference.get("commit"), field="execution.release.commit", minimum=40)
    if COMMIT_PATTERN.fullmatch(commit) is None:
        raise CutoverEvidenceError("Execution release commit is invalid")
    images = release_reference.get("images")
    if (
        not isinstance(images, list)
        or len(set(images)) < 3
        or any(not isinstance(item, str) or IMAGE_PATTERN.fullmatch(item) is None for item in images)
    ):
        raise CutoverEvidenceError("Execution release images are invalid")

    dependencies = document.get("dependencies")
    if not isinstance(dependencies, Mapping):
        raise CutoverEvidenceError("Execution dependencies are missing")
    _exact_keys(
        dependencies,
        {
            "qualification_report_sha256",
            "documentation_walkthrough_sha256",
            "authorization_sha256",
        },
        context="execution.dependencies",
    )
    _sha256(
        dependencies.get("qualification_report_sha256"),
        field="execution.dependencies.qualification_report_sha256",
    )
    _sha256(
        dependencies.get("documentation_walkthrough_sha256"),
        field="execution.dependencies.documentation_walkthrough_sha256",
    )
    authorization_sha = dependencies.get("authorization_sha256")
    if environment == "production":
        _sha256(authorization_sha, field="execution.dependencies.authorization_sha256")
    elif authorization_sha is not None:
        raise CutoverEvidenceError("Rehearsal execution cannot carry production authorization")

    source = _validate_source(document.get("source"), context="execution")
    target = _validate_target(document.get("target"), context="execution")
    operators = _validate_operators(document.get("operators"), context="execution.operators")

    gates = document.get("gates")
    if not isinstance(gates, Mapping) or set(gates) != set(GATE_IDS):
        raise CutoverEvidenceError("Execution must contain ordered gates C01 through C13")
    gate_times: dict[str, tuple[datetime | None, datetime | None]] = {}
    statuses: list[str] = []
    previous_completed: datetime | None = None
    for gate_id in GATE_IDS:
        gate = gates[gate_id]
        if not isinstance(gate, Mapping):
            raise CutoverEvidenceError(f"{gate_id} must be an object")
        _exact_keys(
            gate,
            {"status", "started_at", "completed_at", "evidence_sha256", "signed_by"},
            context=gate_id,
        )
        status_value = gate.get("status")
        if status_value not in {"passed", "abort", "not_started"}:
            raise CutoverEvidenceError(f"{gate_id} status is invalid")
        statuses.append(str(status_value))
        if status_value == "not_started":
            if any(gate.get(name) is not None for name in ("started_at", "completed_at", "evidence_sha256", "signed_by")):
                raise CutoverEvidenceError(f"{gate_id} not_started fields must be null")
            gate_times[gate_id] = (None, None)
            continue
        gate_started = _time(gate.get("started_at"), field=f"{gate_id}.started_at")
        gate_completed = _time(gate.get("completed_at"), field=f"{gate_id}.completed_at")
        if gate_completed < gate_started:
            raise CutoverEvidenceError(f"{gate_id} completion predates its start")
        if previous_completed is not None and gate_started < previous_completed:
            raise CutoverEvidenceError(f"{gate_id} overlaps the previous gate")
        _sha256(gate.get("evidence_sha256"), field=f"{gate_id}.evidence_sha256")
        expected_gate_owner = operators[GATE_OWNER_ROLES[gate_id]]
        if gate.get("signed_by") != expected_gate_owner:
            raise CutoverEvidenceError(
                f"{gate_id} must be signed by its named "
                f"{GATE_OWNER_ROLES[gate_id]}"
            )
        gate_times[gate_id] = (gate_started, gate_completed)
        previous_completed = gate_completed
    if gate_times["C01"][0] is None or gate_times["C01"][0] < started_at:
        raise CutoverEvidenceError("C01 must start within the execution window")

    if mode == "full":
        if statuses != ["passed"] * len(GATE_IDS):
            raise CutoverEvidenceError("Full execution must pass every gate C01-C13")
    else:
        abort_indexes = [index for index, status in enumerate(statuses) if status == "abort"]
        if len(abort_indexes) != 1 or not 1 <= abort_indexes[0] <= 11:
            raise CutoverEvidenceError("Abort drill must abort exactly once at C02-C12")
        abort_index = abort_indexes[0]
        if statuses[:abort_index] != ["passed"] * abort_index or statuses[abort_index + 1 :] != ["not_started"] * (12 - abort_index):
            raise CutoverEvidenceError("Abort drill gate states must be a passed prefix, one abort, then not_started")

    c02_start = gate_times["C02"][0]
    if c02_start is None:
        raise CutoverEvidenceError("C02 must start before an execution can be accepted")
    for gate_id, hard_stop in GATE_HARD_STOPS_SECONDS.items():
        gate_completed = gate_times[gate_id][1]
        if gate_completed is not None and (gate_completed - c02_start).total_seconds() > hard_stop:
            raise CutoverEvidenceError(f"{gate_id} crossed its cumulative hard stop")

    decision = document.get("decision")
    if not isinstance(decision, Mapping):
        raise CutoverEvidenceError("Execution decision is missing")
    _exact_keys(
        decision,
        {
            "value",
            "decided_at",
            "change_commander",
            "database_operator",
            "application_operator",
            "stop_conditions_read",
            "evidence_sha256",
        },
        context="execution.decision",
    )
    expected_decision = "GO" if mode == "full" else "ABORT"
    if decision.get("value") != expected_decision or decision.get("stop_conditions_read") is not True:
        raise CutoverEvidenceError("Execution decision or stop-condition attestation differs")
    for role in ("change_commander", "database_operator", "application_operator"):
        if decision.get(role) != operators[role]:
            raise CutoverEvidenceError(f"Execution decision {role} differs")
    decision_at = _time(decision.get("decided_at"), field="decision.decided_at")
    _sha256(decision.get("evidence_sha256"), field="decision.evidence_sha256")
    if mode == "full":
        c12_completed = gate_times["C12"][1]
        c13_started = gate_times["C13"][0]
        assert c12_completed is not None and c13_started is not None
        if not c12_completed <= decision_at <= c13_started:
            raise CutoverEvidenceError("GO decision must be after C12 and before C13")
    else:
        abort_gate = GATE_IDS[statuses.index("abort")]
        abort_started = gate_times[abort_gate][0]
        assert abort_started is not None
        if decision_at < abort_started:
            raise CutoverEvidenceError("Abort decision predates the abort gate")

    point = document.get("point_of_no_return")
    if not isinstance(point, Mapping):
        raise CutoverEvidenceError("Point-of-no-return record is missing")
    _exact_keys(
        point,
        {
            "postgresql_write_accepted",
            "accepted_at",
            "correlation_id",
            "writer_identity",
            "observer",
            "change_commander",
        },
        context="execution.point_of_no_return",
    )
    if mode == "abort_drill":
        if point.get("postgresql_write_accepted") is not False or any(
            point.get(name) is not None
            for name in (
                "accepted_at",
                "correlation_id",
                "writer_identity",
                "observer",
                "change_commander",
            )
        ):
            raise CutoverEvidenceError("Abort drill must prove no PostgreSQL write was accepted")
        point_at = None
    else:
        if point.get("postgresql_write_accepted") is not True:
            raise CutoverEvidenceError("Full execution must record the first PostgreSQL write")
        point_at = _time(point.get("accepted_at"), field="point_of_no_return.accepted_at")
        for name in ("correlation_id", "writer_identity"):
            _text(point.get(name), field=f"point_of_no_return.{name}")
        if point.get("observer") != operators["observer"] or point.get(
            "change_commander"
        ) != operators["change_commander"]:
            raise CutoverEvidenceError("Point-of-no-return observers differ")
        c13_started, c13_completed = gate_times["C13"]
        assert c13_started is not None and c13_completed is not None
        if not max(decision_at, c13_started) <= point_at <= c13_completed:
            raise CutoverEvidenceError("First PostgreSQL write must occur inside C13 after GO")

    outcome = document.get("outcome")
    if not isinstance(outcome, Mapping):
        raise CutoverEvidenceError("Execution outcome is missing")
    _exact_keys(
        outcome,
        {
            "status",
            "downtime_seconds",
            "restore_rto_seconds",
            "rollback_seconds",
            "unexplained_reconciliation_differences",
            "critical_smoke_passed",
            "steady_smoke_passed",
            "burst_smoke_passed",
            "rollback_demonstrated",
            "sqlite_state",
            "postgresql_state",
            "writes_reopened_after_signoff",
            "stabilization_started_at",
            "manual_steps",
            "deviations",
            "final_evidence_index_sha256",
        },
        context="execution.outcome",
    )
    if outcome.get("manual_steps") != [] or outcome.get("deviations") != []:
        raise CutoverEvidenceError("Manual or undocumented deviations reset rehearsal/cutover eligibility")
    if outcome.get("unexplained_reconciliation_differences") != 0:
        raise CutoverEvidenceError("Execution has unexplained reconciliation differences")
    downtime = _number(outcome.get("downtime_seconds"), field="outcome.downtime_seconds")
    restore_rto = _number(
        outcome.get("restore_rto_seconds"), field="outcome.restore_rto_seconds"
    )
    if downtime > MAX_CUTOVER_SECONDS or restore_rto > MAX_RESTORE_RTO_SECONDS:
        raise CutoverEvidenceError("Execution downtime or restore RTO exceeds the contract")
    _sha256(
        outcome.get("final_evidence_index_sha256"),
        field="outcome.final_evidence_index_sha256",
    )
    expected_downtime_end = completed_at if mode == "abort_drill" else gate_times["C13"][1]
    assert expected_downtime_end is not None
    measured_downtime = (expected_downtime_end - c02_start).total_seconds()
    if abs(downtime - measured_downtime) > 1:
        raise CutoverEvidenceError("Reported downtime differs from gate timestamps")

    if mode == "abort_drill":
        rollback_seconds = _number(
            outcome.get("rollback_seconds"), field="outcome.rollback_seconds"
        )
        if (
            outcome.get("status") != "aborted_as_planned"
            or rollback_seconds > MAX_ROLLBACK_SECONDS
            or outcome.get("rollback_demonstrated") is not True
            or outcome.get("critical_smoke_passed") is not True
            or outcome.get("sqlite_state") != "sole_writable"
            or outcome.get("postgresql_state") != "closed"
            or outcome.get("writes_reopened_after_signoff") is not True
            or outcome.get("stabilization_started_at") is not None
        ):
            raise CutoverEvidenceError("Abort drill did not prove bounded pre-write rollback")
    else:
        if outcome.get("rollback_seconds") is not None:
            raise CutoverEvidenceError("Successful full execution cannot report rollback")
        expected_status = "cutover_complete" if environment == "production" else "passed"
        if (
            outcome.get("status") != expected_status
            or outcome.get("rollback_demonstrated") is not False
            or outcome.get("critical_smoke_passed") is not True
            or outcome.get("sqlite_state") != "frozen_read_only"
            or outcome.get("postgresql_state") != "sole_writable"
            or outcome.get("writes_reopened_after_signoff") is not True
        ):
            raise CutoverEvidenceError("Full execution did not prove the post-write state")
        if environment == "rehearsal" and (
            outcome.get("steady_smoke_passed") is not True
            or outcome.get("burst_smoke_passed") is not True
        ):
            raise CutoverEvidenceError("Full rehearsal must pass steady and burst smoke")
        stabilization = _time(
            outcome.get("stabilization_started_at"),
            field="outcome.stabilization_started_at",
        )
        assert point_at is not None
        if not point_at <= stabilization <= completed_at:
            raise CutoverEvidenceError("Stabilization must start after first write within the execution")

    if completed_at < (previous_completed or started_at):
        raise CutoverEvidenceError("Execution completed before its final gate")
    return {
        "environment": environment,
        "mode": mode,
        "sequence_number": sequence,
        "started_at": started_at,
        "completed_at": completed_at,
        "release": dict(release_reference),
        "dependencies": dict(dependencies),
        "source": source,
        "target": target,
        "operators": operators,
        "downtime_seconds": downtime,
    }


def seal_execution(*, input_path: Path, output_path: Path) -> dict[str, Any]:
    _require_new_output(output_path)
    payload = _read_json_object(input_path)
    _validate_execution(payload, sealed=False)
    return write_document(output_path, payload)


def _cross_validate_dependencies(
    execution: Mapping[str, Any],
    *,
    release_identity: Mapping[str, Any],
    qualification: Mapping[str, Any],
    documentation: Mapping[str, Any],
) -> None:
    _validate_release_reference(execution.get("release"), release_identity, context="execution")
    dependencies = execution["dependencies"]
    if dependencies.get("qualification_report_sha256") != qualification.get(
        "document_sha256"
    ):
        raise CutoverEvidenceError("Execution qualification checksum differs")
    if dependencies.get("documentation_walkthrough_sha256") != documentation.get(
        "document_sha256"
    ):
        raise CutoverEvidenceError("Execution documentation checksum differs")


def _rehearsal_payload(execution: Mapping[str, Any]) -> dict[str, Any]:
    mode = execution["mode"]
    return {
        "kind": "workchord-postgresql-migration-rehearsal",
        "schema_version": SCHEMA_VERSION,
        "report_id": f"{execution['execution_id']}-report",
        "created_at": datetime.now(UTC).isoformat(),
        "status": "abort_drill_passed" if mode == "abort_drill" else "rehearsal_passed",
        "release": dict(execution["release"]),
        "dependencies": dict(execution["dependencies"]),
        "execution": dict(execution),
        "attestation": REHEARSAL_ATTESTATION,
    }


def finalize_rehearsal(
    *,
    execution_path: Path,
    release_manifest_path: Path,
    qualification_report_path: Path,
    qualification_public_key: Path,
    documentation_walkthrough_path: Path,
    documentation_public_key: Path,
    signing_key: Path,
    signer: str,
    output_path: Path,
) -> dict[str, Any]:
    release = read_document(release_manifest_path)
    release_identity = _release_identity(release)
    qualification = read_document(qualification_report_path)
    _validate_qualification(
        qualification,
        release=release,
        trusted_public_key=qualification_public_key,
    )
    documentation = read_document(documentation_walkthrough_path)
    _validate_documentation(
        documentation,
        expected_release=release_identity,
        trusted_public_key=documentation_public_key,
        signed=True,
    )
    execution = read_document(execution_path)
    details = _validate_execution(execution, sealed=True)
    if details["environment"] != "rehearsal":
        raise CutoverEvidenceError("Rehearsal report cannot finalize production execution")
    _cross_validate_dependencies(
        execution,
        release_identity=release_identity,
        qualification=qualification,
        documentation=documentation,
    )
    return _sign_document(
        output_path,
        _rehearsal_payload(execution),
        signing_key=signing_key,
        signer=signer,
    )


def _validate_rehearsal_report(
    document: Mapping[str, Any],
    *,
    trusted_public_key: Path,
) -> dict[str, Any]:
    verify_signed_document(
        document,
        trusted_public_key=trusted_public_key,
        expected_kind="workchord-postgresql-migration-rehearsal",
    )
    _exact_keys(
        document,
        {
            "kind",
            "schema_version",
            "report_id",
            "created_at",
            "status",
            "release",
            "dependencies",
            "execution",
            "attestation",
            "signature",
            "document_sha256",
        },
        context="rehearsal report",
    )
    if document.get("schema_version") != 1 or document.get("attestation") != REHEARSAL_ATTESTATION:
        raise CutoverEvidenceError("Rehearsal report contract differs")
    report_created = _time(document.get("created_at"), field="rehearsal.created_at")
    execution = document.get("execution")
    if not isinstance(execution, Mapping):
        raise CutoverEvidenceError("Rehearsal report execution is missing")
    details = _validate_execution(execution, sealed=True)
    if details["environment"] != "rehearsal":
        raise CutoverEvidenceError("Rehearsal report embeds non-rehearsal execution")
    expected_status = (
        "abort_drill_passed" if details["mode"] == "abort_drill" else "rehearsal_passed"
    )
    if document.get("status") != expected_status:
        raise CutoverEvidenceError("Rehearsal report status differs from execution")
    if document.get("release") != execution.get("release") or document.get(
        "dependencies"
    ) != execution.get("dependencies"):
        raise CutoverEvidenceError("Rehearsal report identities differ from execution")
    if report_created < details["completed_at"]:
        raise CutoverEvidenceError("Rehearsal report predates execution completion")
    return details


def finalize_rehearsal_series(
    *,
    abort_report_path: Path,
    rehearsal_report_paths: list[Path],
    rehearsal_public_key: Path,
    signing_key: Path,
    signer: str,
    output_path: Path,
) -> dict[str, Any]:
    if len(rehearsal_report_paths) != 2:
        raise CutoverEvidenceError("Exactly two successful rehearsal reports are required")
    paths = [abort_report_path, *rehearsal_report_paths]
    reports = [read_document(path) for path in paths]
    details = [
        _validate_rehearsal_report(item, trusted_public_key=rehearsal_public_key)
        for item in reports
    ]
    abort, first, second = details
    if abort["mode"] != "abort_drill" or any(
        item["mode"] != "full" for item in (first, second)
    ):
        raise CutoverEvidenceError("Series requires one abort drill followed by two full rehearsals")
    if [first["sequence_number"], second["sequence_number"]] != [1, 2]:
        raise CutoverEvidenceError("Successful rehearsal sequence must be exactly 1 then 2")
    if not abort["completed_at"] <= first["started_at"] <= first["completed_at"] <= second[
        "started_at"
    ]:
        raise CutoverEvidenceError("Abort drill and successful rehearsals are not consecutive")
    for field in ("release", "dependencies"):
        if any(item[field] != abort[field] for item in (first, second)):
            raise CutoverEvidenceError(f"Rehearsal series {field} identities differ")
    payload = {
        "kind": "workchord-postgresql-migration-rehearsal-series",
        "schema_version": SCHEMA_VERSION,
        "report_id": f"rehearsal-series-{reports[2]['report_id']}",
        "created_at": datetime.now(UTC).isoformat(),
        "status": "qualified_for_production_cutover",
        "release": dict(reports[0]["release"]),
        "dependencies": dict(reports[0]["dependencies"]),
        "abort_drill": {
            "report_id": reports[0]["report_id"],
            "sha256": reports[0]["document_sha256"],
            "completed_at": abort["completed_at"].isoformat(),
        },
        "successful_rehearsals": [
            {
                "report_id": report["report_id"],
                "sequence_number": detail["sequence_number"],
                "sha256": report["document_sha256"],
                "source": detail["source"],
                "target": detail["target"],
                "started_at": detail["started_at"].isoformat(),
                "completed_at": detail["completed_at"].isoformat(),
                "downtime_seconds": detail["downtime_seconds"],
            }
            for report, detail in zip(reports[1:], details[1:], strict=True)
        ],
        "attestation": SERIES_ATTESTATION,
    }
    return _sign_document(output_path, payload, signing_key=signing_key, signer=signer)


def _validate_rehearsal_series(
    document: Mapping[str, Any],
    *,
    trusted_public_key: Path,
) -> None:
    verify_signed_document(
        document,
        trusted_public_key=trusted_public_key,
        expected_kind="workchord-postgresql-migration-rehearsal-series",
    )
    if (
        document.get("schema_version") != 1
        or document.get("status") != "qualified_for_production_cutover"
        or document.get("attestation") != SERIES_ATTESTATION
    ):
        raise CutoverEvidenceError("Rehearsal series is not qualified v1")
    _validate_unbound_release_reference(
        document.get("release"), context="rehearsal series"
    )
    dependencies = document.get("dependencies")
    if not isinstance(dependencies, Mapping):
        raise CutoverEvidenceError("Rehearsal series dependencies are missing")
    _exact_keys(
        dependencies,
        {
            "qualification_report_sha256",
            "documentation_walkthrough_sha256",
            "authorization_sha256",
        },
        context="rehearsal series dependencies",
    )
    _sha256(
        dependencies.get("qualification_report_sha256"),
        field="series.dependencies.qualification_report_sha256",
    )
    _sha256(
        dependencies.get("documentation_walkthrough_sha256"),
        field="series.dependencies.documentation_walkthrough_sha256",
    )
    if dependencies.get("authorization_sha256") is not None:
        raise CutoverEvidenceError(
            "Rehearsal series cannot carry production authorization"
        )
    successful = document.get("successful_rehearsals")
    if not isinstance(successful, list) or len(successful) != 2:
        raise CutoverEvidenceError("Rehearsal series must contain exactly two successes")
    if [item.get("sequence_number") for item in successful] != [1, 2]:
        raise CutoverEvidenceError("Rehearsal series sequence differs")
    checksums = [item.get("sha256") for item in successful]
    abort = document.get("abort_drill")
    if not isinstance(abort, Mapping):
        raise CutoverEvidenceError("Rehearsal series abort drill is missing")
    checksums.append(abort.get("sha256"))
    if len(set(checksums)) != 3 or any(SHA256_PATTERN.fullmatch(str(item)) is None for item in checksums):
        raise CutoverEvidenceError("Rehearsal series checksums are invalid")
    abort_completed = _time(abort.get("completed_at"), field="series.abort.completed_at")
    first_started = _time(successful[0].get("started_at"), field="series.first.started_at")
    first_completed = _time(successful[0].get("completed_at"), field="series.first.completed_at")
    second_started = _time(successful[1].get("started_at"), field="series.second.started_at")
    second_completed = _time(successful[1].get("completed_at"), field="series.second.completed_at")
    if not abort_completed <= first_started < first_completed <= second_started < second_completed:
        raise CutoverEvidenceError("Rehearsal series timing is invalid")
    if _time(document.get("created_at"), field="series.created_at") < second_completed:
        raise CutoverEvidenceError("Rehearsal series predates its second success")


def _validate_authorization(
    document: Mapping[str, Any],
    *,
    trusted_public_key: Path | None,
    signed: bool,
) -> None:
    required = {
        "kind",
        "schema_version",
        "authorization_id",
        "change_id",
        "created_at",
        "status",
        "valid_from",
        "expires_at",
        "release",
        "dependencies",
        "source_scope",
        "target",
        "authorities",
        "decision",
    }
    optional = {"signature", "document_sha256"} if signed else frozenset()
    _exact_keys(document, required, optional=optional, context="production authorization")
    if (
        document.get("kind") != "workchord-postgresql-production-cutover-authorization"
        or document.get("schema_version") != 1
        or document.get("status") != "authorized"
    ):
        raise CutoverEvidenceError("Production authorization is not authorized v1")
    _validate_unbound_release_reference(
        document.get("release"), context="production authorization"
    )
    _text(document.get("authorization_id"), field="authorization_id", minimum=8)
    _text(document.get("change_id"), field="authorization.change_id")
    created_at = _time(document.get("created_at"), field="authorization.created_at")
    valid_from = _time(document.get("valid_from"), field="authorization.valid_from")
    expires_at = _time(document.get("expires_at"), field="authorization.expires_at")
    if not created_at <= expires_at or not valid_from < expires_at:
        raise CutoverEvidenceError("Production authorization window is invalid")
    if expires_at - valid_from > timedelta(days=7):
        raise CutoverEvidenceError("Production authorization window exceeds seven days")
    if created_at > datetime.now(UTC) + timedelta(minutes=1):
        raise CutoverEvidenceError("Production authorization is future-dated")
    _validate_source_scope(document.get("source_scope"), context="authorization")
    _validate_target(document.get("target"), context="authorization")
    _validate_operators(document.get("authorities"), context="authorization.authorities")
    dependencies = document.get("dependencies")
    if not isinstance(dependencies, Mapping):
        raise CutoverEvidenceError("Authorization dependencies are missing")
    _exact_keys(
        dependencies,
        {
            "qualification_report_sha256",
            "documentation_walkthrough_sha256",
            "rehearsal_series_sha256",
        },
        context="authorization.dependencies",
    )
    for key, item in dependencies.items():
        _sha256(item, field=f"authorization.dependencies.{key}")
    decision = document.get("decision")
    if not isinstance(decision, Mapping):
        raise CutoverEvidenceError("Authorization decision is missing")
    _exact_keys(
        decision,
        {
            "approved",
            "downtime_budget_minutes",
            "rollback_before_first_write",
            "reverse_sync_available",
            "sqlite_retention",
            "evidence_sha256",
        },
        context="authorization.decision",
    )
    if (
        decision.get("approved") is not True
        or decision.get("downtime_budget_minutes") != 180
        or decision.get("rollback_before_first_write") is not True
        or decision.get("reverse_sync_available") is not False
        or decision.get("sqlite_retention") != "read_only"
    ):
        raise CutoverEvidenceError("Production authorization boundaries differ")
    _sha256(decision.get("evidence_sha256"), field="authorization.decision.evidence_sha256")
    _reject_secret_material(document)
    if signed:
        if trusted_public_key is None:
            raise CutoverEvidenceError("Trusted authorization public key is required")
        verify_signed_document(
            document,
            trusted_public_key=trusted_public_key,
            expected_kind="workchord-postgresql-production-cutover-authorization",
        )


def authorize_production(
    *,
    intent_path: Path,
    release_manifest_path: Path,
    qualification_report_path: Path,
    qualification_public_key: Path,
    documentation_walkthrough_path: Path,
    documentation_public_key: Path,
    rehearsal_series_path: Path,
    rehearsal_public_key: Path,
    signing_key: Path,
    signer: str,
    output_path: Path,
) -> dict[str, Any]:
    release = read_document(release_manifest_path)
    release_identity = _release_identity(release)
    qualification = read_document(qualification_report_path)
    _validate_qualification(
        qualification,
        release=release,
        trusted_public_key=qualification_public_key,
    )
    documentation = read_document(documentation_walkthrough_path)
    _validate_documentation(
        documentation,
        expected_release=release_identity,
        trusted_public_key=documentation_public_key,
        signed=True,
    )
    series = read_document(rehearsal_series_path)
    _validate_rehearsal_series(series, trusted_public_key=rehearsal_public_key)
    payload = _read_json_object(intent_path)
    _validate_authorization(payload, trusted_public_key=None, signed=False)
    _validate_release_reference(payload.get("release"), release_identity, context="authorization")
    expected_dependencies = {
        "qualification_report_sha256": qualification["document_sha256"],
        "documentation_walkthrough_sha256": documentation["document_sha256"],
        "rehearsal_series_sha256": series["document_sha256"],
    }
    if payload.get("dependencies") != expected_dependencies:
        raise CutoverEvidenceError("Authorization dependencies differ from trusted evidence")
    expected_series_dependencies = {
        "qualification_report_sha256": qualification["document_sha256"],
        "documentation_walkthrough_sha256": documentation["document_sha256"],
        "authorization_sha256": None,
    }
    if series.get("release") != payload.get("release") or series.get(
        "dependencies"
    ) != expected_series_dependencies:
        raise CutoverEvidenceError("Rehearsal series does not bind the authorized release")
    if _time(payload["expires_at"], field="authorization.expires_at") <= datetime.now(UTC):
        raise CutoverEvidenceError("Production authorization is already expired")
    return _sign_document(output_path, payload, signing_key=signing_key, signer=signer)


def finalize_production(
    *,
    execution_path: Path,
    release_manifest_path: Path,
    qualification_report_path: Path,
    qualification_public_key: Path,
    documentation_walkthrough_path: Path,
    documentation_public_key: Path,
    rehearsal_series_path: Path,
    rehearsal_public_key: Path,
    authorization_path: Path,
    authorization_public_key: Path,
    signing_key: Path,
    signer: str,
    output_path: Path,
) -> dict[str, Any]:
    release = read_document(release_manifest_path)
    release_identity = _release_identity(release)
    qualification = read_document(qualification_report_path)
    _validate_qualification(
        qualification,
        release=release,
        trusted_public_key=qualification_public_key,
    )
    documentation = read_document(documentation_walkthrough_path)
    _validate_documentation(
        documentation,
        expected_release=release_identity,
        trusted_public_key=documentation_public_key,
        signed=True,
    )
    series = read_document(rehearsal_series_path)
    _validate_rehearsal_series(series, trusted_public_key=rehearsal_public_key)
    authorization = read_document(authorization_path)
    _validate_authorization(
        authorization,
        trusted_public_key=authorization_public_key,
        signed=True,
    )
    execution = read_document(execution_path)
    details = _validate_execution(execution, sealed=True)
    if details["environment"] != "production" or details["mode"] != "full":
        raise CutoverEvidenceError("Production report requires one full production execution")
    _cross_validate_dependencies(
        execution,
        release_identity=release_identity,
        qualification=qualification,
        documentation=documentation,
    )
    dependencies = authorization["dependencies"]
    expected_dependencies = {
        "qualification_report_sha256": qualification["document_sha256"],
        "documentation_walkthrough_sha256": documentation["document_sha256"],
        "rehearsal_series_sha256": series["document_sha256"],
    }
    if dependencies != expected_dependencies:
        raise CutoverEvidenceError("Authorization dependencies differ from final evidence")
    if execution["dependencies"]["authorization_sha256"] != authorization[
        "document_sha256"
    ]:
        raise CutoverEvidenceError("Execution did not bind the trusted authorization")
    if execution["change_id"] != authorization["change_id"]:
        raise CutoverEvidenceError("Execution change ID differs from authorization")
    if execution["release"] != authorization["release"]:
        raise CutoverEvidenceError("Execution release differs from authorization")
    if _source_scope(details["source"]) != authorization["source_scope"]:
        raise CutoverEvidenceError("Execution source scope differs from authorization")
    if details["target"] != authorization["target"]:
        raise CutoverEvidenceError("Execution target differs from authorization")
    if details["operators"] != authorization["authorities"]:
        raise CutoverEvidenceError("Execution authorities differ from authorization")
    valid_from = _time(authorization["valid_from"], field="authorization.valid_from")
    expires_at = _time(authorization["expires_at"], field="authorization.expires_at")
    authorization_created = _time(
        authorization["created_at"], field="authorization.created_at"
    )
    if authorization_created > details["started_at"]:
        raise CutoverEvidenceError(
            "Production authorization was signed after execution began"
        )
    if not valid_from <= details["started_at"] < expires_at:
        raise CutoverEvidenceError("Production execution started outside authorization window")
    if series.get("release") != execution.get("release"):
        raise CutoverEvidenceError("Production execution release differs from rehearsal series")
    payload = {
        "kind": "workchord-postgresql-production-cutover",
        "schema_version": SCHEMA_VERSION,
        "report_id": f"{execution['change_id']}-production-cutover",
        "created_at": datetime.now(UTC).isoformat(),
        "status": "completed",
        "release": dict(execution["release"]),
        "dependencies": {
            "qualification_report_sha256": qualification["document_sha256"],
            "documentation_walkthrough_sha256": documentation["document_sha256"],
            "rehearsal_series_sha256": series["document_sha256"],
            "authorization_sha256": authorization["document_sha256"],
        },
        "execution": dict(execution),
        "attestation": PRODUCTION_ATTESTATION,
    }
    return _sign_document(output_path, payload, signing_key=signing_key, signer=signer)


def _validate_production_report(
    document: Mapping[str, Any],
    *,
    trusted_public_key: Path,
) -> None:
    verify_signed_document(
        document,
        trusted_public_key=trusted_public_key,
        expected_kind="workchord-postgresql-production-cutover",
    )
    if (
        document.get("schema_version") != 1
        or document.get("status") != "completed"
        or document.get("attestation") != PRODUCTION_ATTESTATION
    ):
        raise CutoverEvidenceError("Production cutover report is not completed v1")
    _exact_keys(
        document,
        {
            "kind",
            "schema_version",
            "report_id",
            "created_at",
            "status",
            "release",
            "dependencies",
            "execution",
            "attestation",
            "signature",
            "document_sha256",
        },
        context="production cutover report",
    )
    execution = document.get("execution")
    if not isinstance(execution, Mapping):
        raise CutoverEvidenceError("Production report execution is missing")
    details = _validate_execution(execution, sealed=True)
    if details["environment"] != "production" or details["mode"] != "full":
        raise CutoverEvidenceError("Production report embeds non-production execution")
    if document.get("release") != execution.get("release"):
        raise CutoverEvidenceError("Production report release differs from execution")
    dependencies = document.get("dependencies")
    if not isinstance(dependencies, Mapping):
        raise CutoverEvidenceError("Production report dependencies are missing")
    _exact_keys(
        dependencies,
        {
            "qualification_report_sha256",
            "documentation_walkthrough_sha256",
            "rehearsal_series_sha256",
            "authorization_sha256",
        },
        context="production report dependencies",
    )
    for key, item in dependencies.items():
        _sha256(item, field=f"production.dependencies.{key}")
    if (
        dependencies["qualification_report_sha256"]
        != execution["dependencies"]["qualification_report_sha256"]
        or dependencies["documentation_walkthrough_sha256"]
        != execution["dependencies"]["documentation_walkthrough_sha256"]
        or dependencies["authorization_sha256"]
        != execution["dependencies"]["authorization_sha256"]
    ):
        raise CutoverEvidenceError(
            "Production report dependencies differ from execution"
        )
    if _time(document.get("created_at"), field="production.created_at") < details[
        "completed_at"
    ]:
        raise CutoverEvidenceError("Production report predates execution completion")


def verify_report(*, report_path: Path, trusted_public_key: Path) -> str:
    document = read_document(report_path)
    kind = document.get("kind")
    if kind == "workchord-postgresql-documentation-walkthrough":
        _validate_documentation(
            document,
            expected_release=None,
            trusted_public_key=trusted_public_key,
            signed=True,
        )
    elif kind == "workchord-postgresql-migration-rehearsal":
        _validate_rehearsal_report(document, trusted_public_key=trusted_public_key)
    elif kind == "workchord-postgresql-migration-rehearsal-series":
        _validate_rehearsal_series(document, trusted_public_key=trusted_public_key)
    elif kind == "workchord-postgresql-production-cutover-authorization":
        _validate_authorization(
            document,
            trusted_public_key=trusted_public_key,
            signed=True,
        )
    elif kind == "workchord-postgresql-production-cutover":
        _validate_production_report(document, trusted_public_key=trusted_public_key)
    elif kind == "workchord-postgresql-precutover-qualification":
        verify_signed_document(
            document,
            trusted_public_key=trusted_public_key,
            expected_kind="workchord-postgresql-precutover-qualification",
        )
    else:
        raise CutoverEvidenceError(f"Unsupported signed report kind: {kind!r}")
    return _sha256(document.get("document_sha256"), field="report.document_sha256")
