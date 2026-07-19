"""Fail-closed PostgreSQL release publication and contract closeout evidence.

This module never mutates a database, deployment, or public document in place.
It verifies the signed pre-cutover and production evidence chain, creates a
signed post-cutover publication, and lets an independent auditor issue a
derived SHIP or NO-SHIP decision.  Missing production evidence is represented
as an explicit NO-SHIP blocker; it can never be converted into a local pass.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from importlib.metadata import PackageNotFoundError, version as package_version
import ipaddress
import json
import os
from pathlib import Path
import re
import tomllib
from typing import Any, Mapping
from urllib.parse import urlsplit

from app.database_migration.cutover import (
    CAPACITY_CLAIM,
    CutoverEvidenceError,
    _exact_keys,
    _read_json_object,
    _reject_secret_material,
    _release_identity,
    _sha256,
    _sign_document,
    _text,
    _time,
    _validate_production_report,
    _validate_qualification,
    verify_signed_document,
)
from app.database_migration.manifest import (
    read_document,
    sha256_bytes,
)


SCHEMA_VERSION = 1
POSTGRESQL_VERSION_PATTERN = re.compile(r"^18\.[0-9]+$")
SAFE_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/+-]{2,255}$")
APPLICATION_VERSION_PATTERN = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+$")
AVAILABILITY_OBJECTIVE_PERCENT = 99.9
AVAILABILITY_OBSERVATION_DAYS = 30
BACKUP_RPO_SECONDS_MAXIMUM = 300
RESTORE_RTO_SECONDS_MAXIMUM = 1800

CAPACITY_WORDING = (
    "1,250 opaque browser identities, 250 active browser sessions, and 200 "
    "concurrent MCP/agent clients"
)
AUTHENTICATION_BOUNDARY = (
    "This certification does not certify 1,250 authenticated people; "
    "authentication, RBAC, tenancy, and any people-based capacity claim remain "
    "a separate scope."
)
POSTCUTOVER_ATTESTATION = (
    "This publication was produced after the signed production cutover from the "
    "exact frozen release and qualification evidence. It contains no secret or "
    "private production topology and does not claim monthly availability before "
    "a complete 30-day client or gateway observation."
)
CLOSEOUT_INPUT_ATTESTATION = (
    "Every database-migration task, release gate, exception, and required "
    "post-cutover observation known to the auditor is listed; no failed, "
    "missing, expired, or unfavorable evidence is omitted."
)
CLOSEOUT_DECISION_ATTESTATION = (
    "The verdict is derived from the complete independent audit. Missing "
    "external or production evidence is NO-SHIP, and monthly 99.9% availability "
    "is claimed only from a complete 30-day client or gateway denominator."
)

REPOSITORY_DOCUMENTS = {
    "readme": Path("README.md"),
    "database_portability_policy": Path("docs/database-portability-policy.md"),
    "database_runtime_policy": Path("docs/database-runtime-policy.md"),
    "postgresql_operations": Path("docs/runbooks/postgresql-operations.md"),
    "postgresql_deployment": Path("docs/runbooks/postgresql-deployment.md"),
    "postgresql_security": Path("docs/runbooks/postgresql-security.md"),
    "postgresql_backup_restore": Path("docs/runbooks/postgresql-backup-restore.md"),
    "postgresql_qualification": Path("docs/runbooks/postgresql-qualification.md"),
    "postgresql_rehearsal_cutover": Path(
        "docs/runbooks/postgresql-rehearsal-cutover-evidence.md"
    ),
    "postgresql_postcutover_closeout": Path(
        "docs/runbooks/postgresql-postcutover-release-and-closeout.md"
    ),
    "postgresql_troubleshooting": Path("docs/runbooks/postgresql-troubleshooting.md"),
    "sqlite_migration": Path("docs/runbooks/sqlite-to-postgresql-migration.md"),
    "sqlite_cutover": Path("docs/runbooks/sqlite-to-postgresql-cutover.md"),
    "cutover_checklist": Path("docs/runbooks/postgresql-cutover-checklist.md"),
}

DBM_TASK_IDS = (
    "DBM-CON-001",
    "DBM-QA-001",
    "DBM-DEP-001",
    "DBM-CFG-001",
    "DBM-MIG-001",
    "DBM-MIG-002",
    "DBM-QA-002",
    "DBM-RUN-001",
    "DBM-RUN-002",
    "DBM-RUN-003",
    "DBM-PERF-001",
    "DBM-PERF-002",
    "DBM-WORK-001",
    "DBM-OBS-001",
    "DBM-MAINT-001",
    "DBM-DATA-001",
    "DBM-DATA-002",
    "DBM-DATA-003",
    "DBM-DEPLOY-001",
    "DBM-DEPLOY-002",
    "DBM-SEC-001",
    "DBM-BACKUP-001",
    "DBM-CUT-001",
    "DBM-QA-003",
    "DBM-SCALE-001",
    "DBM-RES-001",
    "DBM-DOC-001",
    "DBM-QUAL-001",
    "DBM-REHEARSE-001",
    "DBM-CUT-002",
    "DBM-DOC-002",
)
RELEASE_GATE_IDS = tuple(f"G{index}" for index in range(1, 16))
AUDIT_CHECK_IDS = (
    "application_logs",
    "unexpected_errors",
    "slow_queries",
    "lock_waits_and_deadlocks",
    "pool_pressure",
    "worker_queues",
    "domain_integrity",
)
NON_WAIVABLE_TASKS = frozenset(
    {"DBM-QUAL-001", "DBM-CUT-002", "DBM-DOC-002"}
)
NON_WAIVABLE_GATES = frozenset({"G10", "G13", "G14", "G15"})


class CloseoutEvidenceError(CutoverEvidenceError):
    """A post-cutover publication or closure input is incomplete or unsafe."""


def _optional_time(value: object, *, field: str) -> datetime | None:
    if value is None:
        return None
    return _time(value, field=field)


def _optional_sha256(value: object, *, field: str) -> str | None:
    if value is None:
        return None
    return _sha256(value, field=field)


def _number(value: object, *, field: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CloseoutEvidenceError(f"{field} must be numeric")
    result = float(value)
    if result < 0:
        raise CloseoutEvidenceError(f"{field} must not be negative")
    return result


def _integer(value: object, *, field: str, minimum: int = 0) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise CloseoutEvidenceError(f"{field} must be an integer >= {minimum}")
    return value


def _safe_identifier(value: object, *, field: str) -> str:
    result = _text(value, field=field)
    if SAFE_IDENTIFIER_PATTERN.fullmatch(result) is None:
        raise CloseoutEvidenceError(f"{field} contains unsafe characters")
    return result


def _safe_public_uri(value: object, *, field: str) -> str:
    uri = _text(value, field=field)
    parsed = urlsplit(uri)
    if parsed.scheme == "urn":
        if parsed.query or parsed.fragment or SAFE_IDENTIFIER_PATTERN.fullmatch(uri) is None:
            raise CloseoutEvidenceError(f"{field} must be a stable secret-free URN")
        return uri
    if parsed.scheme != "https" or not parsed.hostname:
        raise CloseoutEvidenceError(f"{field} must use HTTPS or a stable URN")
    if parsed.username is not None or parsed.password is not None or parsed.query:
        raise CloseoutEvidenceError(f"{field} must not contain credentials or a query")
    hostname = parsed.hostname.lower().rstrip(".")
    if hostname in {"localhost", "localhost.localdomain"} or hostname.endswith(
        (".local", ".internal", ".localhost")
    ):
        raise CloseoutEvidenceError(f"{field} exposes a private hostname")
    try:
        address = ipaddress.ip_address(hostname.strip("[]"))
    except ValueError:
        address = None
    if address is not None and not address.is_global:
        raise CloseoutEvidenceError(f"{field} exposes a non-public address")
    return uri


def _installed_application_version() -> str:
    try:
        result = package_version("workchord-backend")
    except PackageNotFoundError as exc:
        raise CloseoutEvidenceError(
            "The released workchord-backend package must be installed"
        ) from exc
    if APPLICATION_VERSION_PATTERN.fullmatch(result) is None:
        raise CloseoutEvidenceError("Installed application version is not x.y.z")
    return result


def _repository_document_set(
    repository_root: Path,
    *,
    expected_application_version: str,
) -> dict[str, dict[str, str]]:
    root = repository_root.resolve()
    if not root.is_dir():
        raise CloseoutEvidenceError("Repository documentation root does not exist")
    result: dict[str, dict[str, str]] = {}
    texts: dict[str, str] = {}
    for name, relative in REPOSITORY_DOCUMENTS.items():
        path = (root / relative).resolve()
        try:
            path.relative_to(root)
        except ValueError as exc:
            raise CloseoutEvidenceError(
                f"Documentation path escaped the release root: {relative}"
            ) from exc
        if not path.is_file():
            raise CloseoutEvidenceError(f"Released documentation is missing: {relative}")
        encoded = path.read_bytes()
        try:
            texts[name] = encoded.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise CloseoutEvidenceError(
                f"Released documentation is not UTF-8: {relative}"
            ) from exc
        result[name] = {
            "path": relative.as_posix(),
            "sha256": sha256_bytes(encoded),
        }

    required_text = {
        "readme": (
            "PostgreSQL is the integration and production target",
            CAPACITY_WORDING,
            "Opaque identities are not authenticated people",
        ),
        "database_portability_policy": (
            "production fallback allowed",
            "PostgreSQL production support is declared only",
        ),
        "postgresql_operations": (
            "DATABASE_POSTGRESQL_REQUIRED=true",
            "Monthly 99.9% availability is a post-release 30-day observation objective",
        ),
        "postgresql_rehearsal_cutover": (
            "The completed report is the DBM-CUT-002 machine record, not DBM-CLOSE-001",
            "never reopen SQLite",
        ),
        "postgresql_postcutover_closeout": (
            "DBM-DOC-002",
            "DBM-CLOSE-001",
            "workchord-db-closeout",
            "Missing production evidence produces `NO-SHIP`",
        ),
        "sqlite_cutover": (
            "There is no reverse synchronization",
            "full 30-day client/gateway SLI window",
        ),
    }
    for name, snippets in required_text.items():
        normalized = " ".join(texts[name].split())
        for snippet in snippets:
            if snippet not in texts[name] and " ".join(snippet.split()) not in normalized:
                raise CloseoutEvidenceError(
                    f"Released document {REPOSITORY_DOCUMENTS[name]} lacks {snippet!r}"
                )

    pyproject_path = root / "backend/pyproject.toml"
    main_path = root / "backend/app/main.py"
    if not pyproject_path.is_file() or not main_path.is_file():
        raise CloseoutEvidenceError("Released backend version sources are missing")
    project = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))
    source_version = project.get("project", {}).get("version")
    match = re.search(
        r"app\s*=\s*FastAPI\s*\(.*?\bversion\s*=\s*[\"']([^\"']+)[\"']",
        main_path.read_text(encoding="utf-8"),
        re.DOTALL,
    )
    api_version = match.group(1) if match else None
    if source_version != expected_application_version or api_version != source_version:
        raise CloseoutEvidenceError(
            "Released pyproject, installed package, and API versions differ"
        )
    return result


def _artifact_references(
    value: object,
    *,
    expected_qualification_sha256: str,
    expected_production_sha256: str,
) -> list[dict[str, str]]:
    if not isinstance(value, list) or len(value) != 2:
        raise CloseoutEvidenceError(
            "Publication requires exactly qualification and production artifact references"
        )
    expected = {
        "precutover_qualification": expected_qualification_sha256,
        "production_cutover": expected_production_sha256,
    }
    normalized: list[dict[str, str]] = []
    for index, item in enumerate(value):
        if not isinstance(item, Mapping):
            raise CloseoutEvidenceError("Publication artifact reference must be an object")
        _exact_keys(
            item,
            {"kind", "public_uri", "sha256"},
            context=f"publication.artifact_references[{index}]",
        )
        kind = _text(item.get("kind"), field=f"artifact[{index}].kind")
        if kind not in expected:
            raise CloseoutEvidenceError(f"Unknown publication artifact kind: {kind}")
        normalized.append(
            {
                "kind": kind,
                "public_uri": _safe_public_uri(
                    item.get("public_uri"), field=f"artifact[{index}].public_uri"
                ),
                "sha256": _sha256(item.get("sha256"), field=f"artifact[{index}].sha256"),
            }
        )
    if {item["kind"] for item in normalized} != set(expected):
        raise CloseoutEvidenceError("Publication artifact kinds are incomplete")
    if any(item["sha256"] != expected[item["kind"]] for item in normalized):
        raise CloseoutEvidenceError("Publication artifact checksum differs from trusted evidence")
    return sorted(normalized, key=lambda item: item["kind"])


def _publication_exceptions(
    value: object,
    *,
    published_at: datetime,
) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise CloseoutEvidenceError("Publication operational_exceptions must be a list")
    normalized: list[dict[str, Any]] = []
    identifiers: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, Mapping):
            raise CloseoutEvidenceError("Publication exception must be an object")
        _exact_keys(
            item,
            {
                "id",
                "summary",
                "owner",
                "approved_at",
                "expires_at",
                "approval_evidence_sha256",
            },
            context=f"publication.operational_exceptions[{index}]",
        )
        identifier = _safe_identifier(item.get("id"), field=f"exception[{index}].id")
        if identifier in identifiers:
            raise CloseoutEvidenceError("Publication exception IDs must be unique")
        identifiers.add(identifier)
        approved_at = _time(item.get("approved_at"), field=f"exception[{index}].approved_at")
        expires_at = _time(item.get("expires_at"), field=f"exception[{index}].expires_at")
        if not approved_at <= published_at < expires_at:
            raise CloseoutEvidenceError(
                "Publication exception must be approved and unexpired at publication"
            )
        normalized.append(
            {
                "id": identifier,
                "summary": _text(item.get("summary"), field=f"exception[{index}].summary"),
                "owner": _text(item.get("owner"), field=f"exception[{index}].owner"),
                "approved_at": approved_at.isoformat(),
                "expires_at": expires_at.isoformat(),
                "approval_evidence_sha256": _sha256(
                    item.get("approval_evidence_sha256"),
                    field=f"exception[{index}].approval_evidence_sha256",
                ),
            }
        )
    return sorted(normalized, key=lambda item: item["id"])


def _release_notes_markdown(
    *,
    publication_id: str,
    published_at: datetime,
    application_version: str,
    postgresql_version: str,
    schema_head: str,
    release_boundary: str,
    release_identity: Mapping[str, Any],
    qualification: Mapping[str, Any],
    production: Mapping[str, Any],
    artifacts: list[dict[str, str]],
    exceptions: list[dict[str, Any]],
) -> str:
    artifact_lines = []
    labels = {
        "precutover_qualification": "Pre-cutover qualification",
        "production_cutover": "Production cutover record",
    }
    for item in artifacts:
        artifact_lines.append(
            f"- [{labels[item['kind']]}]({item['public_uri']}) — SHA-256 "
            f"`{item['sha256']}`"
        )
    if exceptions:
        exception_lines = [
            f"- `{item['id']}` — {item['summary']} Owner: {item['owner']}; "
            f"expires {item['expires_at']}."
            for item in exceptions
        ]
    else:
        exception_lines = ["- None approved for this publication."]
    production_completed = _time(
        production["execution"]["completed_at"], field="production.execution.completed_at"
    )
    return (
        "# WorkChord PostgreSQL production transition\n\n"
        f"Publication `{publication_id}` was approved at {published_at.isoformat()} "
        f"for WorkChord `{application_version}` from commit "
        f"`{release_identity['commit']}`. The production cutover completed at "
        f"{production_completed.isoformat()}.\n\n"
        "## Released database policy\n\n"
        f"PostgreSQL `{postgresql_version}` at Alembic `{schema_head}` is the sole "
        "writable production system of record. SQLite production support is removed "
        f"at release boundary `{release_boundary}`. SQLite remains supported only for "
        "direct local development, tests, and as the frozen read-only migration source; "
        "it is never a production fallback.\n\n"
        "After the first accepted PostgreSQL application write there is no reverse "
        "synchronization. Recovery is forward on PostgreSQL through failover, PITR, or "
        "an isolated validated restore. The frozen SQLite snapshot remains read-only "
        "until its approved retention and secure-disposal gate.\n\n"
        "## Certified capacity boundary\n\n"
        f"The signed pre-cutover qualification certifies **{CAPACITY_WORDING}** "
        "only under its frozen workload, data, configuration, image, and hardware "
        "context. "
        f"{AUTHENTICATION_BOUNDARY}\n\n"
        "Monthly 99.9% availability remains a post-release objective until a complete "
        "30-consecutive-day client or gateway SLI denominator is independently audited.\n\n"
        "## Evidence\n\n"
        + "\n".join(artifact_lines)
        + "\n\n"
        "The qualification report contains exactly three consecutive complete attempts "
        f"and binds capacity contract `{qualification['capacity_contract']['sha256']}`. "
        "Evidence references are public or opaque; this notice contains no credential or "
        "private production topology.\n\n"
        "## Approved operational exceptions\n\n"
        + "\n".join(exception_lines)
        + "\n"
    )


def _validate_publication(
    document: Mapping[str, Any],
    *,
    trusted_public_key: Path | None,
    signed: bool,
) -> None:
    required = {
        "kind",
        "schema_version",
        "publication_id",
        "published_at",
        "status",
        "release",
        "application_version",
        "postgresql_version",
        "postgresql_version_evidence_sha256",
        "schema_head",
        "production_database_policy",
        "capacity_claim",
        "capacity_wording",
        "authentication_boundary",
        "dependencies",
        "artifact_references",
        "operational_exceptions",
        "documents",
        "release_notes",
        "approval",
        "attestation",
    }
    optional = {"signature", "document_sha256"} if signed else frozenset()
    _exact_keys(document, required, optional=optional, context="post-cutover publication")
    if (
        document.get("kind") != "workchord-postgresql-postcutover-publication"
        or document.get("schema_version") != 1
        or document.get("status") != "published"
    ):
        raise CloseoutEvidenceError("Post-cutover publication is not published v1")
    _safe_identifier(document.get("publication_id"), field="publication_id")
    published_at = _time(document.get("published_at"), field="publication.published_at")
    if published_at > datetime.now(UTC) + timedelta(minutes=1):
        raise CloseoutEvidenceError("Post-cutover publication is future-dated")
    application_version = _text(
        document.get("application_version"), field="publication.application_version"
    )
    if APPLICATION_VERSION_PATTERN.fullmatch(application_version) is None:
        raise CloseoutEvidenceError("Publication application version is not x.y.z")
    postgresql_version = _text(
        document.get("postgresql_version"), field="publication.postgresql_version"
    )
    if POSTGRESQL_VERSION_PATTERN.fullmatch(postgresql_version) is None:
        raise CloseoutEvidenceError("Publication PostgreSQL version is not an 18.x minor")
    _sha256(
        document.get("postgresql_version_evidence_sha256"),
        field="publication.postgresql_version_evidence_sha256",
    )
    _text(document.get("schema_head"), field="publication.schema_head")
    release = document.get("release")
    if not isinstance(release, Mapping):
        raise CloseoutEvidenceError("Publication release identity is missing")
    _exact_keys(
        release,
        {"fingerprint", "manifest_sha256", "commit", "images"},
        context="publication.release",
    )
    _sha256(release.get("fingerprint"), field="publication.release.fingerprint")
    _sha256(release.get("manifest_sha256"), field="publication.release.manifest_sha256")
    commit = _text(release.get("commit"), field="publication.release.commit", minimum=40)
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise CloseoutEvidenceError("Publication commit is invalid")
    images = release.get("images")
    if not isinstance(images, list) or len(images) < 3 or len(images) != len(set(images)):
        raise CloseoutEvidenceError("Publication release image pins are incomplete")

    policy = document.get("production_database_policy")
    if not isinstance(policy, Mapping):
        raise CloseoutEvidenceError("Publication production database policy is missing")
    _exact_keys(
        policy,
        {
            "system_of_record",
            "sqlite_production_support",
            "sqlite_allowed_scope",
            "production_fallback_allowed",
            "release_boundary",
            "recovery_after_first_write",
        },
        context="publication.production_database_policy",
    )
    if policy != {
        "system_of_record": "postgresql",
        "sqlite_production_support": "removed",
        "sqlite_allowed_scope": ["development", "test", "read_only_migration_source"],
        "production_fallback_allowed": False,
        "release_boundary": policy.get("release_boundary"),
        "recovery_after_first_write": "forward_on_postgresql_only",
    }:
        raise CloseoutEvidenceError("Publication database policy differs")
    _safe_identifier(policy.get("release_boundary"), field="publication.release_boundary")
    if document.get("capacity_claim") != CAPACITY_CLAIM:
        raise CloseoutEvidenceError("Publication capacity claim differs")
    if document.get("capacity_wording") != CAPACITY_WORDING:
        raise CloseoutEvidenceError("Publication capacity wording differs")
    if document.get("authentication_boundary") != AUTHENTICATION_BOUNDARY:
        raise CloseoutEvidenceError("Publication authentication boundary differs")

    dependencies = document.get("dependencies")
    if not isinstance(dependencies, Mapping):
        raise CloseoutEvidenceError("Publication dependencies are missing")
    _exact_keys(
        dependencies,
        {
            "qualification_report_sha256",
            "production_cutover_sha256",
            "capacity_contract_sha256",
            "hardware_evidence_sha256",
        },
        context="publication.dependencies",
    )
    for key, value in dependencies.items():
        _sha256(value, field=f"publication.dependencies.{key}")
    artifacts = document.get("artifact_references")
    if not isinstance(artifacts, list) or len(artifacts) != 2:
        raise CloseoutEvidenceError("Publication artifact references are incomplete")
    artifact_kinds: set[str] = set()
    for index, item in enumerate(artifacts):
        if not isinstance(item, Mapping):
            raise CloseoutEvidenceError("Publication artifact reference is invalid")
        _exact_keys(item, {"kind", "public_uri", "sha256"}, context=f"artifact[{index}]")
        kind = _text(item.get("kind"), field=f"artifact[{index}].kind")
        artifact_kinds.add(kind)
        _safe_public_uri(item.get("public_uri"), field=f"artifact[{index}].public_uri")
        _sha256(item.get("sha256"), field=f"artifact[{index}].sha256")
    if artifact_kinds != {"precutover_qualification", "production_cutover"}:
        raise CloseoutEvidenceError("Publication artifact kinds differ")

    exceptions = document.get("operational_exceptions")
    if not isinstance(exceptions, list):
        raise CloseoutEvidenceError("Publication exceptions must be a list")
    seen_exception_ids: set[str] = set()
    for index, item in enumerate(exceptions):
        if not isinstance(item, Mapping):
            raise CloseoutEvidenceError("Publication exception is invalid")
        _exact_keys(
            item,
            {
                "id",
                "summary",
                "owner",
                "approved_at",
                "expires_at",
                "approval_evidence_sha256",
            },
            context=f"publication.exception[{index}]",
        )
        identifier = _safe_identifier(item.get("id"), field=f"exception[{index}].id")
        if identifier in seen_exception_ids:
            raise CloseoutEvidenceError("Publication exception IDs must be unique")
        seen_exception_ids.add(identifier)
        if not _time(item.get("approved_at"), field=f"exception[{index}].approved_at") <= published_at < _time(
            item.get("expires_at"), field=f"exception[{index}].expires_at"
        ):
            raise CloseoutEvidenceError("Publication contains an expired exception")
        _text(item.get("summary"), field=f"exception[{index}].summary")
        _text(item.get("owner"), field=f"exception[{index}].owner")
        _sha256(
            item.get("approval_evidence_sha256"),
            field=f"exception[{index}].approval_evidence_sha256",
        )

    documents = document.get("documents")
    if not isinstance(documents, Mapping) or set(documents) != set(REPOSITORY_DOCUMENTS):
        raise CloseoutEvidenceError("Publication document set differs")
    for name, item in documents.items():
        if not isinstance(item, Mapping):
            raise CloseoutEvidenceError(f"Publication document {name} is invalid")
        _exact_keys(item, {"path", "sha256"}, context=f"publication.documents.{name}")
        if item.get("path") != REPOSITORY_DOCUMENTS[name].as_posix():
            raise CloseoutEvidenceError(f"Publication document path differs for {name}")
        _sha256(item.get("sha256"), field=f"publication.documents.{name}.sha256")
    notes = document.get("release_notes")
    if not isinstance(notes, Mapping):
        raise CloseoutEvidenceError("Publication release notes are missing")
    _exact_keys(notes, {"media_type", "sha256", "content"}, context="release_notes")
    if notes.get("media_type") != "text/markdown":
        raise CloseoutEvidenceError("Publication release notes must be Markdown")
    content = notes.get("content")
    if not isinstance(content, str) or len(content.strip()) < 100:
        raise CloseoutEvidenceError("Publication release-note content is incomplete")
    if _sha256(notes.get("sha256"), field="release_notes.sha256") != sha256_bytes(
        content.encode("utf-8")
    ):
        raise CloseoutEvidenceError("Publication release-note checksum differs")
    for snippet in (
        CAPACITY_WORDING,
        "does not certify 1,250 authenticated people",
        "sole writable production system of record",
        "SQLite production support is removed",
        "no reverse synchronization",
        "30-consecutive-day",
    ):
        if snippet not in content:
            raise CloseoutEvidenceError(f"Publication release notes lack {snippet!r}")
    approval = document.get("approval")
    if not isinstance(approval, Mapping):
        raise CloseoutEvidenceError("Publication approval is missing")
    _exact_keys(
        approval,
        {"product_owner", "release_owner", "evidence_sha256"},
        context="publication.approval",
    )
    _text(approval.get("product_owner"), field="publication.approval.product_owner")
    _text(approval.get("release_owner"), field="publication.approval.release_owner")
    _sha256(approval.get("evidence_sha256"), field="publication.approval.evidence_sha256")
    if document.get("attestation") != POSTCUTOVER_ATTESTATION:
        raise CloseoutEvidenceError("Publication attestation differs")
    _reject_secret_material(document)
    if signed:
        if trusted_public_key is None:
            raise CloseoutEvidenceError("Trusted publication public key is required")
        verify_signed_document(
            document,
            trusted_public_key=trusted_public_key,
            expected_kind="workchord-postgresql-postcutover-publication",
        )


def publish_postcutover_release(
    *,
    input_path: Path,
    repository_root: Path,
    release_manifest_path: Path,
    qualification_report_path: Path,
    qualification_public_key: Path,
    production_cutover_path: Path,
    production_public_key: Path,
    signing_key: Path,
    signer: str,
    output_path: Path,
) -> dict[str, Any]:
    """Validate the production chain and sign its public release publication."""

    release = read_document(release_manifest_path)
    release_identity = _release_identity(release)
    qualification = read_document(qualification_report_path)
    _validate_qualification(
        qualification,
        release=release,
        trusted_public_key=qualification_public_key,
    )
    production = read_document(production_cutover_path)
    _validate_production_report(production, trusted_public_key=production_public_key)
    if production.get("release") != release_identity:
        raise CloseoutEvidenceError("Production cutover used another frozen release")
    if production.get("dependencies", {}).get(
        "qualification_report_sha256"
    ) != qualification.get("document_sha256"):
        raise CloseoutEvidenceError("Production cutover qualification differs")

    raw = _read_json_object(input_path)
    _exact_keys(
        raw,
        {
            "kind",
            "schema_version",
            "publication_id",
            "published_at",
            "status",
            "application_version",
            "postgresql_version",
            "postgresql_version_evidence_sha256",
            "release_boundary",
            "artifact_references",
            "operational_exceptions",
            "approval",
        },
        context="post-cutover publication input",
    )
    if (
        raw.get("kind") != "workchord-postgresql-postcutover-publication-input"
        or raw.get("schema_version") != 1
        or raw.get("status") != "approved_for_publication"
    ):
        raise CloseoutEvidenceError("Post-cutover publication input is not approved v1")
    publication_id = _safe_identifier(raw.get("publication_id"), field="publication_id")
    published_at = _time(raw.get("published_at"), field="publication.published_at")
    production_completed = _time(
        production["execution"]["completed_at"], field="production.execution.completed_at"
    )
    if published_at < production_completed or published_at > datetime.now(UTC) + timedelta(
        minutes=1
    ):
        raise CloseoutEvidenceError(
            "Publication time must follow the completed production cutover"
        )
    application_version = _text(
        raw.get("application_version"), field="publication.application_version"
    )
    if application_version != _installed_application_version():
        raise CloseoutEvidenceError(
            "Publication application version differs from the installed release"
        )
    postgresql_version = _text(
        raw.get("postgresql_version"), field="publication.postgresql_version"
    )
    if POSTGRESQL_VERSION_PATTERN.fullmatch(postgresql_version) is None:
        raise CloseoutEvidenceError("Publication PostgreSQL version must be exact 18.x")
    version_evidence = _sha256(
        raw.get("postgresql_version_evidence_sha256"),
        field="publication.postgresql_version_evidence_sha256",
    )
    release_boundary = _safe_identifier(
        raw.get("release_boundary"), field="publication.release_boundary"
    )
    artifacts = _artifact_references(
        raw.get("artifact_references"),
        expected_qualification_sha256=qualification["document_sha256"],
        expected_production_sha256=production["document_sha256"],
    )
    exceptions = _publication_exceptions(
        raw.get("operational_exceptions"), published_at=published_at
    )
    approval = raw.get("approval")
    if not isinstance(approval, Mapping):
        raise CloseoutEvidenceError("Publication approval is missing")
    _exact_keys(
        approval,
        {"product_owner", "release_owner", "evidence_sha256"},
        context="publication.approval",
    )
    normalized_approval = {
        "product_owner": _text(
            approval.get("product_owner"), field="publication.approval.product_owner"
        ),
        "release_owner": _text(
            approval.get("release_owner"), field="publication.approval.release_owner"
        ),
        "evidence_sha256": _sha256(
            approval.get("evidence_sha256"),
            field="publication.approval.evidence_sha256",
        ),
    }
    if signer.strip() != normalized_approval["release_owner"]:
        raise CloseoutEvidenceError(
            "Publication signer must be the named release owner"
        )
    documents = _repository_document_set(
        repository_root,
        expected_application_version=application_version,
    )
    schema_head = _text(release.get("schema_head"), field="release.schema_head")
    notes = _release_notes_markdown(
        publication_id=publication_id,
        published_at=published_at,
        application_version=application_version,
        postgresql_version=postgresql_version,
        schema_head=schema_head,
        release_boundary=release_boundary,
        release_identity=release_identity,
        qualification=qualification,
        production=production,
        artifacts=artifacts,
        exceptions=exceptions,
    )
    capacity_contract = release.get("capacity_contract")
    if not isinstance(capacity_contract, Mapping):
        raise CloseoutEvidenceError("Frozen release capacity contract is missing")
    payload = {
        "kind": "workchord-postgresql-postcutover-publication",
        "schema_version": SCHEMA_VERSION,
        "publication_id": publication_id,
        "published_at": published_at.isoformat(),
        "status": "published",
        "release": release_identity,
        "application_version": application_version,
        "postgresql_version": postgresql_version,
        "postgresql_version_evidence_sha256": version_evidence,
        "schema_head": schema_head,
        "production_database_policy": {
            "system_of_record": "postgresql",
            "sqlite_production_support": "removed",
            "sqlite_allowed_scope": [
                "development",
                "test",
                "read_only_migration_source",
            ],
            "production_fallback_allowed": False,
            "release_boundary": release_boundary,
            "recovery_after_first_write": "forward_on_postgresql_only",
        },
        "capacity_claim": dict(CAPACITY_CLAIM),
        "capacity_wording": CAPACITY_WORDING,
        "authentication_boundary": AUTHENTICATION_BOUNDARY,
        "dependencies": {
            "qualification_report_sha256": qualification["document_sha256"],
            "production_cutover_sha256": production["document_sha256"],
            "capacity_contract_sha256": _sha256(
                capacity_contract.get("sha256"), field="release.capacity_contract.sha256"
            ),
            "hardware_evidence_sha256": _sha256(
                release.get("hardware_evidence_sha256"),
                field="release.hardware_evidence_sha256",
            ),
        },
        "artifact_references": artifacts,
        "operational_exceptions": exceptions,
        "documents": documents,
        "release_notes": {
            "media_type": "text/markdown",
            "sha256": sha256_bytes(notes.encode("utf-8")),
            "content": notes,
        },
        "approval": normalized_approval,
        "attestation": POSTCUTOVER_ATTESTATION,
    }
    _reject_secret_material(payload)
    _validate_publication(payload, trusted_public_key=None, signed=False)
    return _sign_document(
        output_path,
        payload,
        signing_key=signing_key,
        signer=signer,
    )


def _write_public_text(path: Path, content: str) -> None:
    if path.exists() or path.is_symlink():
        raise CloseoutEvidenceError(
            f"Release-note output already exists and will not be overwritten: {path}"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    if temporary.exists() or temporary.is_symlink():
        raise CloseoutEvidenceError("Temporary release-note output already exists")
    encoded = content.encode("utf-8")
    try:
        with temporary.open("xb") as handle:
            os.chmod(temporary, 0o644)
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())
        os.link(temporary, path)
        directory_fd = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary.exists():
            temporary.unlink()


def render_release_notes(
    *,
    publication_path: Path,
    publication_public_key: Path,
    output_path: Path,
) -> str:
    """Verify a signed publication and materialize its immutable Markdown."""

    publication = read_document(publication_path)
    _validate_publication(
        publication,
        trusted_public_key=publication_public_key,
        signed=True,
    )
    content = str(publication["release_notes"]["content"])
    _write_public_text(output_path, content)
    return str(publication["release_notes"]["sha256"])


def _validate_evidence_matrix(
    value: object,
    *,
    expected_ids: tuple[str, ...],
    allowed_statuses: frozenset[str],
    context: str,
    exceptions: Mapping[str, Mapping[str, Any]],
    audited_at: datetime,
    non_waivable: frozenset[str],
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    if not isinstance(value, Mapping) or set(value) != set(expected_ids):
        raise CloseoutEvidenceError(f"{context} must contain every exact contract ID")
    normalized: dict[str, dict[str, Any]] = {}
    blockers: list[str] = []
    for identifier in expected_ids:
        item = value.get(identifier)
        if not isinstance(item, Mapping):
            raise CloseoutEvidenceError(f"{context}.{identifier} must be an object")
        _exact_keys(
            item,
            {"status", "evidence_sha256", "exception_id"},
            context=f"{context}.{identifier}",
        )
        status = _text(item.get("status"), field=f"{context}.{identifier}.status")
        if status not in allowed_statuses:
            raise CloseoutEvidenceError(f"{context}.{identifier} has invalid status")
        evidence = _optional_sha256(
            item.get("evidence_sha256"), field=f"{context}.{identifier}.evidence_sha256"
        )
        exception_id = item.get("exception_id")
        if exception_id is not None:
            exception_id = _safe_identifier(
                exception_id, field=f"{context}.{identifier}.exception_id"
            )
        passing_status = "complete" if "complete" in allowed_statuses else "passed"
        if status == passing_status:
            if evidence is None or exception_id is not None:
                raise CloseoutEvidenceError(
                    f"{context}.{identifier} passing evidence is incomplete"
                )
        elif status == "waived":
            if evidence is None or exception_id is None:
                raise CloseoutEvidenceError(
                    f"{context}.{identifier} waiver evidence is incomplete"
                )
            exception = exceptions.get(exception_id)
            if exception is None or exception.get("status") != "approved_waiver":
                blockers.append(f"{identifier}: waiver is not approved")
            else:
                if identifier not in exception["scope"]:
                    blockers.append(f"{identifier}: waiver scope differs")
                if exception["expires_at"] <= audited_at:
                    blockers.append(f"{identifier}: waiver expired")
            if identifier in non_waivable:
                blockers.append(f"{identifier}: gate is non-waivable")
        else:
            if exception_id is None:
                raise CloseoutEvidenceError(
                    f"{context}.{identifier} unresolved status needs an exception owner"
                )
            exception = exceptions.get(exception_id)
            if exception is None or identifier not in exception["scope"]:
                raise CloseoutEvidenceError(
                    f"{context}.{identifier} unresolved exception scope differs"
                )
            blockers.append(f"{identifier}: {status}")
        normalized[identifier] = {
            "status": status,
            "evidence_sha256": evidence,
            "exception_id": exception_id,
        }
    return normalized, blockers


def _validate_closeout_exceptions(
    value: object,
    *,
    audited_at: datetime,
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    if not isinstance(value, list):
        raise CloseoutEvidenceError("Closeout exceptions must be a list")
    known_scope = set(DBM_TASK_IDS) | set(RELEASE_GATE_IDS)
    normalized: dict[str, dict[str, Any]] = {}
    blockers: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, Mapping):
            raise CloseoutEvidenceError("Closeout exception must be an object")
        _exact_keys(
            item,
            {
                "id",
                "status",
                "owner",
                "expires_at",
                "scope",
                "rationale",
                "approval_evidence_sha256",
            },
            context=f"closeout.exceptions[{index}]",
        )
        identifier = _safe_identifier(item.get("id"), field=f"exception[{index}].id")
        if identifier in normalized:
            raise CloseoutEvidenceError("Closeout exception IDs must be unique")
        status = _text(item.get("status"), field=f"exception[{index}].status")
        if status not in {"approved_waiver", "open"}:
            raise CloseoutEvidenceError("Closeout exception status is invalid")
        scope = item.get("scope")
        if (
            not isinstance(scope, list)
            or not scope
            or len(scope) != len(set(scope))
            or any(entry not in known_scope for entry in scope)
        ):
            raise CloseoutEvidenceError("Closeout exception scope is invalid")
        expires_at = _time(item.get("expires_at"), field=f"exception[{index}].expires_at")
        approval = _optional_sha256(
            item.get("approval_evidence_sha256"),
            field=f"exception[{index}].approval_evidence_sha256",
        )
        if status == "approved_waiver" and approval is None:
            raise CloseoutEvidenceError("Approved waiver lacks approval evidence")
        if status == "open":
            blockers.append(f"{identifier}: unresolved exception remains open")
        if expires_at <= audited_at:
            blockers.append(f"{identifier}: exception expired")
        normalized[identifier] = {
            "id": identifier,
            "status": status,
            "owner": _text(item.get("owner"), field=f"exception[{index}].owner"),
            "expires_at": expires_at,
            "scope": sorted(scope),
            "rationale": _text(
                item.get("rationale"), field=f"exception[{index}].rationale"
            ),
            "approval_evidence_sha256": approval,
        }
    return normalized, blockers


def _dependency_summary(
    *,
    repository_root: Path | None,
    release_manifest_path: Path | None,
    qualification_report_path: Path | None,
    qualification_public_key: Path | None,
    production_cutover_path: Path | None,
    production_public_key: Path | None,
    publication_path: Path | None,
    publication_public_key: Path | None,
) -> dict[str, Any]:
    pairs = (
        (qualification_report_path, qualification_public_key, "qualification"),
        (production_cutover_path, production_public_key, "production cutover"),
        (publication_path, publication_public_key, "post-cutover publication"),
    )
    for report, key, label in pairs:
        if (report is None) != (key is None):
            raise CloseoutEvidenceError(f"{label} report and trusted key must be supplied together")
    if release_manifest_path is None:
        if any(report is not None for report, _, _ in pairs):
            raise CloseoutEvidenceError(
                "The frozen release manifest is required with signed dependency evidence"
            )
        return {
            "release": None,
            "qualification": None,
            "production_cutover": None,
            "postcutover_publication": None,
        }

    release = read_document(release_manifest_path)
    release_identity = _release_identity(release)
    summary: dict[str, Any] = {
        "release": {
            **release_identity,
            "schema_head": _text(release.get("schema_head"), field="release.schema_head"),
        },
        "qualification": None,
        "production_cutover": None,
        "postcutover_publication": None,
    }
    qualification: dict[str, Any] | None = None
    if qualification_report_path is not None:
        qualification = read_document(qualification_report_path)
        assert qualification_public_key is not None
        _validate_qualification(
            qualification,
            release=release,
            trusted_public_key=qualification_public_key,
        )
        summary["qualification"] = {
            "document_sha256": qualification["document_sha256"],
            "created_at": qualification["created_at"],
            "run_bundle_sha256": [
                item["bundle_sha256"] for item in qualification["consecutive_runs"]
            ],
        }
    if production_cutover_path is not None:
        if qualification is None:
            raise CloseoutEvidenceError(
                "Production cutover evidence requires the trusted qualification"
            )
        production = read_document(production_cutover_path)
        assert production_public_key is not None
        _validate_production_report(production, trusted_public_key=production_public_key)
        if production.get("release") != release_identity:
            raise CloseoutEvidenceError("Production cutover release differs")
        if production.get("dependencies", {}).get(
            "qualification_report_sha256"
        ) != qualification["document_sha256"]:
            raise CloseoutEvidenceError("Production cutover qualification differs")
        outcome = production["execution"]["outcome"]
        summary["production_cutover"] = {
            "document_sha256": production["document_sha256"],
            "report_id": production["report_id"],
            "completed_at": production["execution"]["completed_at"],
            "stabilization_started_at": outcome["stabilization_started_at"],
            "sqlite_snapshot_sha256": production["execution"]["source"][
                "snapshot_sha256"
            ],
        }
    if publication_path is not None:
        if summary["production_cutover"] is None or qualification is None:
            raise CloseoutEvidenceError(
                "Post-cutover publication requires the trusted production chain"
            )
        publication = read_document(publication_path)
        assert publication_public_key is not None
        _validate_publication(
            publication,
            trusted_public_key=publication_public_key,
            signed=True,
        )
        if publication.get("release") != release_identity:
            raise CloseoutEvidenceError("Post-cutover publication release differs")
        if publication.get("dependencies", {}).get(
            "qualification_report_sha256"
        ) != qualification["document_sha256"] or publication.get("dependencies", {}).get(
            "production_cutover_sha256"
        ) != summary[
            "production_cutover"
        ][
            "document_sha256"
        ]:
            raise CloseoutEvidenceError("Post-cutover publication dependencies differ")
        if repository_root is None:
            raise CloseoutEvidenceError(
                "Released repository documentation is required with the publication"
            )
        current_documents = _repository_document_set(
            repository_root,
            expected_application_version=publication["application_version"],
        )
        if current_documents != publication["documents"]:
            raise CloseoutEvidenceError(
                "Released documentation changed after post-cutover publication"
            )
        summary["postcutover_publication"] = {
            "document_sha256": publication["document_sha256"],
            "publication_id": publication["publication_id"],
            "published_at": publication["published_at"],
            "release_notes_sha256": publication["release_notes"]["sha256"],
        }
    return summary


def _validate_timed_status(
    value: object,
    *,
    context: str,
    audited_at: datetime,
    production: Mapping[str, Any] | None,
) -> tuple[dict[str, Any], list[str]]:
    if not isinstance(value, Mapping):
        raise CloseoutEvidenceError(f"{context} must be an object")
    _exact_keys(
        value,
        {
            "status",
            "started_at",
            "completed_at",
            "approved_duration_hours",
            "approval_evidence_sha256",
            "evidence_sha256",
        },
        context=context,
    )
    status = _text(value.get("status"), field=f"{context}.status")
    if status not in {"not_started", "pending", "passed", "failed"}:
        raise CloseoutEvidenceError(f"{context}.status is invalid")
    started = _optional_time(value.get("started_at"), field=f"{context}.started_at")
    completed = _optional_time(value.get("completed_at"), field=f"{context}.completed_at")
    duration = value.get("approved_duration_hours")
    approval = _optional_sha256(
        value.get("approval_evidence_sha256"),
        field=f"{context}.approval_evidence_sha256",
    )
    evidence = _optional_sha256(
        value.get("evidence_sha256"), field=f"{context}.evidence_sha256"
    )
    blockers: list[str] = []
    if production is None:
        if any(item is not None for item in (started, completed, duration, approval, evidence)) or status != "not_started":
            raise CloseoutEvidenceError(
                "Stabilization cannot begin without trusted production cutover evidence"
            )
        blockers.append("G14: production stabilization has not started")
        return dict(value), blockers
    expected_start = _time(
        production["stabilization_started_at"],
        field="production.stabilization_started_at",
    )
    if started != expected_start:
        raise CloseoutEvidenceError("Stabilization start differs from production cutover")
    approved_hours = _number(duration, field=f"{context}.approved_duration_hours")
    if approved_hours <= 0 or approval is None:
        raise CloseoutEvidenceError("Stabilization requires an approved positive duration")
    if status == "pending":
        if completed is not None or evidence is not None:
            raise CloseoutEvidenceError("Pending stabilization cannot carry completion evidence")
        blockers.append("G14: approved stabilization window remains pending")
    elif status in {"passed", "failed"}:
        if completed is None or evidence is None or not started < completed <= audited_at:
            raise CloseoutEvidenceError("Completed stabilization timing/evidence is invalid")
        if status == "passed" and completed - started < timedelta(hours=approved_hours):
            raise CloseoutEvidenceError("Stabilization ended before its approved duration")
        if status == "failed":
            blockers.append("G14: stabilization failed")
    else:
        raise CloseoutEvidenceError("Production stabilization cannot be not_started")
    return {
        "status": status,
        "started_at": started.isoformat(),
        "completed_at": completed.isoformat() if completed else None,
        "approved_duration_hours": approved_hours,
        "approval_evidence_sha256": approval,
        "evidence_sha256": evidence,
    }, blockers


def _validate_postcutover_verification(
    value: object,
    *,
    audited_at: datetime,
    production: Mapping[str, Any] | None,
) -> tuple[dict[str, Any], list[str]]:
    if not isinstance(value, Mapping):
        raise CloseoutEvidenceError("post_cutover_verification must be an object")
    _exact_keys(
        value,
        {
            "status",
            "profile_id",
            "started_at",
            "completed_at",
            "result_sha256",
            "production_path",
            "all_applicable_slo_gates_passed",
            "unexplained_integrity_differences",
        },
        context="post_cutover_verification",
    )
    status = _text(value.get("status"), field="post_cutover_verification.status")
    if status not in {"not_started", "passed", "failed"}:
        raise CloseoutEvidenceError("Post-cutover verification status is invalid")
    nullable_fields = (
        value.get("profile_id"),
        value.get("started_at"),
        value.get("completed_at"),
        value.get("result_sha256"),
        value.get("production_path"),
        value.get("all_applicable_slo_gates_passed"),
        value.get("unexplained_integrity_differences"),
    )
    if production is None:
        if status != "not_started" or any(item is not None for item in nullable_fields):
            raise CloseoutEvidenceError(
                "Post-cutover verification cannot exist without production evidence"
            )
        return dict(value), ["G14: post-cutover verification is missing"]
    if status == "not_started":
        if any(item is not None for item in nullable_fields):
            raise CloseoutEvidenceError("Not-started verification must have null observations")
        return dict(value), ["G14: post-cutover verification is missing"]
    profile_id = _safe_identifier(
        value.get("profile_id"), field="post_cutover_verification.profile_id"
    )
    started = _time(value.get("started_at"), field="post_cutover_verification.started_at")
    completed = _time(
        value.get("completed_at"), field="post_cutover_verification.completed_at"
    )
    production_completed = _time(
        production["completed_at"], field="production.completed_at"
    )
    if not production_completed <= started < completed <= audited_at:
        raise CloseoutEvidenceError("Post-cutover verification timing is invalid")
    result_sha = _sha256(
        value.get("result_sha256"), field="post_cutover_verification.result_sha256"
    )
    differences = _integer(
        value.get("unexplained_integrity_differences"),
        field="post_cutover_verification.unexplained_integrity_differences",
    )
    passed = (
        status == "passed"
        and value.get("production_path") is True
        and value.get("all_applicable_slo_gates_passed") is True
        and differences == 0
    )
    blockers = [] if passed else ["G14: post-cutover verification failed"]
    return {
        "status": status,
        "profile_id": profile_id,
        "started_at": started.isoformat(),
        "completed_at": completed.isoformat(),
        "result_sha256": result_sha,
        "production_path": value.get("production_path"),
        "all_applicable_slo_gates_passed": value.get(
            "all_applicable_slo_gates_passed"
        ),
        "unexplained_integrity_differences": differences,
    }, blockers


def _validate_backup_restore(
    value: object,
    *,
    audited_at: datetime,
    production: Mapping[str, Any] | None,
    schema_head: str | None,
) -> tuple[dict[str, Any], list[str]]:
    if not isinstance(value, Mapping):
        raise CloseoutEvidenceError("backup_restore must be an object")
    _exact_keys(
        value,
        {
            "status",
            "backup_completed_at",
            "restore_completed_at",
            "backup_sha256",
            "restore_report_sha256",
            "rpo_seconds",
            "rto_seconds",
            "schema_head",
            "isolated_target",
            "reconciled",
        },
        context="backup_restore",
    )
    status = _text(value.get("status"), field="backup_restore.status")
    if status not in {"not_started", "passed", "failed"}:
        raise CloseoutEvidenceError("Backup/restore status is invalid")
    observed = [item for key, item in value.items() if key != "status"]
    if production is None or status == "not_started":
        if status != "not_started" or any(item is not None for item in observed):
            raise CloseoutEvidenceError("Not-started backup/restore must have null observations")
        return dict(value), ["G14: post-cutover backup and isolated restore are missing"]
    backup_completed = _time(
        value.get("backup_completed_at"), field="backup_restore.backup_completed_at"
    )
    restore_completed = _time(
        value.get("restore_completed_at"), field="backup_restore.restore_completed_at"
    )
    production_completed = _time(production["completed_at"], field="production.completed_at")
    if not production_completed <= backup_completed <= restore_completed <= audited_at:
        raise CloseoutEvidenceError("Backup/restore timing is invalid")
    backup_sha = _sha256(value.get("backup_sha256"), field="backup_restore.backup_sha256")
    restore_sha = _sha256(
        value.get("restore_report_sha256"), field="backup_restore.restore_report_sha256"
    )
    rpo_seconds = _number(value.get("rpo_seconds"), field="backup_restore.rpo_seconds")
    rto_seconds = _number(value.get("rto_seconds"), field="backup_restore.rto_seconds")
    passed = (
        status == "passed"
        and rpo_seconds <= BACKUP_RPO_SECONDS_MAXIMUM
        and rto_seconds <= RESTORE_RTO_SECONDS_MAXIMUM
        and value.get("schema_head") == schema_head
        and value.get("isolated_target") is True
        and value.get("reconciled") is True
    )
    blockers = [] if passed else ["G14: post-cutover backup/restore failed"]
    return {
        "status": status,
        "backup_completed_at": backup_completed.isoformat(),
        "restore_completed_at": restore_completed.isoformat(),
        "backup_sha256": backup_sha,
        "restore_report_sha256": restore_sha,
        "rpo_seconds": rpo_seconds,
        "rto_seconds": rto_seconds,
        "schema_head": value.get("schema_head"),
        "isolated_target": value.get("isolated_target"),
        "reconciled": value.get("reconciled"),
    }, blockers


def _validate_operational_audit(
    value: object,
    *,
    production_present: bool,
) -> tuple[dict[str, dict[str, Any]], list[str]]:
    if not isinstance(value, Mapping) or set(value) != set(AUDIT_CHECK_IDS):
        raise CloseoutEvidenceError("Operational audit must contain every exact check")
    normalized: dict[str, dict[str, Any]] = {}
    blockers: list[str] = []
    for check_id in AUDIT_CHECK_IDS:
        item = value.get(check_id)
        if not isinstance(item, Mapping):
            raise CloseoutEvidenceError(f"Operational audit {check_id} is invalid")
        _exact_keys(item, {"status", "evidence_sha256"}, context=f"audit.{check_id}")
        status = _text(item.get("status"), field=f"audit.{check_id}.status")
        if status not in {"not_started", "passed", "failed"}:
            raise CloseoutEvidenceError(f"Operational audit {check_id} status is invalid")
        evidence = _optional_sha256(
            item.get("evidence_sha256"), field=f"audit.{check_id}.evidence_sha256"
        )
        if status == "not_started" and evidence is not None:
            raise CloseoutEvidenceError(f"Not-started audit {check_id} has evidence")
        if status in {"passed", "failed"} and evidence is None:
            raise CloseoutEvidenceError(f"Completed audit {check_id} lacks evidence")
        if not production_present and status != "not_started":
            raise CloseoutEvidenceError(
                "Production operational audit cannot precede the production cutover"
            )
        if status != "passed":
            blockers.append(f"G14: operational audit {check_id} is {status}")
        normalized[check_id] = {"status": status, "evidence_sha256": evidence}
    return normalized, blockers


def _validate_availability(
    value: object,
    *,
    audited_at: datetime,
    production: Mapping[str, Any] | None,
) -> tuple[dict[str, Any], list[str], str]:
    if not isinstance(value, Mapping):
        raise CloseoutEvidenceError("availability must be an object")
    _exact_keys(
        value,
        {
            "status",
            "observation_started_at",
            "observation_completed_at",
            "eligible_attempts",
            "successful_attempts",
            "objective_percent",
            "objective_claimed",
            "denominator_complete",
            "evidence_sha256",
        },
        context="availability",
    )
    status = _text(value.get("status"), field="availability.status")
    if status not in {"not_started", "pending", "met", "missed"}:
        raise CloseoutEvidenceError("Availability status is invalid")
    if value.get("objective_percent") != AVAILABILITY_OBJECTIVE_PERCENT:
        raise CloseoutEvidenceError("Availability objective differs from 99.9%")
    started = _optional_time(
        value.get("observation_started_at"), field="availability.observation_started_at"
    )
    completed = _optional_time(
        value.get("observation_completed_at"), field="availability.observation_completed_at"
    )
    evidence = _optional_sha256(
        value.get("evidence_sha256"), field="availability.evidence_sha256"
    )
    eligible = value.get("eligible_attempts")
    successful = value.get("successful_attempts")
    if production is None:
        if (
            status != "not_started"
            or any(item is not None for item in (started, completed, eligible, successful, evidence))
            or value.get("objective_claimed") is not False
            or value.get("denominator_complete") is not False
        ):
            raise CloseoutEvidenceError(
                "Availability observation cannot precede production cutover"
            )
        return dict(value), [], "pending"
    expected_start = _time(
        production["stabilization_started_at"], field="production.stabilization_started_at"
    )
    if started != expected_start:
        raise CloseoutEvidenceError("Availability start differs from stabilization start")
    if status == "not_started":
        raise CloseoutEvidenceError("Production availability observation must be pending or complete")
    if status == "pending":
        if (
            completed is not None
            or eligible is not None
            or successful is not None
            or evidence is not None
            or value.get("objective_claimed") is not False
            or value.get("denominator_complete") is not False
        ):
            raise CloseoutEvidenceError(
                "Pending availability cannot contain or claim a completed denominator"
            )
        if audited_at >= started + timedelta(days=AVAILABILITY_OBSERVATION_DAYS):
            return dict(value), ["G14: 30-day availability denominator is overdue"], "pending"
        return dict(value), [], "pending"
    if completed is None or evidence is None:
        raise CloseoutEvidenceError("Completed availability lacks timing/evidence")
    if completed - started < timedelta(days=AVAILABILITY_OBSERVATION_DAYS) or completed > audited_at:
        raise CloseoutEvidenceError("Availability window is not 30 complete days")
    eligible_count = _integer(eligible, field="availability.eligible_attempts", minimum=1)
    successful_count = _integer(successful, field="availability.successful_attempts")
    if successful_count > eligible_count or value.get("denominator_complete") is not True:
        raise CloseoutEvidenceError("Availability denominator is incomplete or inconsistent")
    observed = successful_count * 100.0 / eligible_count
    if status == "met":
        if observed < AVAILABILITY_OBJECTIVE_PERCENT or value.get("objective_claimed") is not True:
            raise CloseoutEvidenceError("Availability objective is claimed without passing")
        blockers: list[str] = []
    else:
        if observed >= AVAILABILITY_OBJECTIVE_PERCENT or value.get("objective_claimed") is not False:
            raise CloseoutEvidenceError("Missed availability observation is inconsistent")
        blockers = ["G14: 30-day availability objective was missed"]
    return {
        "status": status,
        "observation_started_at": started.isoformat(),
        "observation_completed_at": completed.isoformat(),
        "eligible_attempts": eligible_count,
        "successful_attempts": successful_count,
        "objective_percent": AVAILABILITY_OBJECTIVE_PERCENT,
        "objective_claimed": value.get("objective_claimed"),
        "denominator_complete": True,
        "evidence_sha256": evidence,
        "observed_percent": observed,
    }, blockers, status


def _validate_sqlite_snapshot(
    value: object,
    *,
    audited_at: datetime,
    production: Mapping[str, Any] | None,
    stabilization: Mapping[str, Any],
) -> tuple[dict[str, Any], list[str]]:
    if not isinstance(value, Mapping):
        raise CloseoutEvidenceError("sqlite_snapshot must be an object")
    _exact_keys(
        value,
        {
            "state",
            "snapshot_sha256",
            "retention_approval_sha256",
            "retain_until",
            "disposed_at",
            "disposal_evidence_sha256",
            "writable",
        },
        context="sqlite_snapshot",
    )
    state = _text(value.get("state"), field="sqlite_snapshot.state")
    if state not in {"not_created", "retained_read_only", "securely_disposed"}:
        raise CloseoutEvidenceError("SQLite snapshot state is invalid")
    snapshot_sha = _optional_sha256(
        value.get("snapshot_sha256"), field="sqlite_snapshot.snapshot_sha256"
    )
    approval_sha = _optional_sha256(
        value.get("retention_approval_sha256"),
        field="sqlite_snapshot.retention_approval_sha256",
    )
    retain_until = _optional_time(value.get("retain_until"), field="sqlite_snapshot.retain_until")
    disposed_at = _optional_time(value.get("disposed_at"), field="sqlite_snapshot.disposed_at")
    disposal_sha = _optional_sha256(
        value.get("disposal_evidence_sha256"),
        field="sqlite_snapshot.disposal_evidence_sha256",
    )
    if production is None:
        if (
            state != "not_created"
            or any(item is not None for item in (snapshot_sha, approval_sha, retain_until, disposed_at, disposal_sha))
            or value.get("writable") is not None
        ):
            raise CloseoutEvidenceError("Post-cutover SQLite snapshot cannot precede production")
        return dict(value), ["G14: post-cutover SQLite retention state is unavailable"]
    if snapshot_sha != production["sqlite_snapshot_sha256"]:
        raise CloseoutEvidenceError("Retained SQLite snapshot checksum differs from cutover")
    if approval_sha is None or retain_until is None or value.get("writable") is not False:
        raise CloseoutEvidenceError("SQLite snapshot retention is not read-only and approved")
    blockers: list[str] = []
    if state == "retained_read_only":
        if disposed_at is not None or disposal_sha is not None:
            raise CloseoutEvidenceError("Retained SQLite snapshot has disposal evidence")
        if retain_until <= audited_at:
            blockers.append("G14: SQLite snapshot retention expired without secure disposal")
    elif state == "securely_disposed":
        if disposed_at is None or disposal_sha is None:
            raise CloseoutEvidenceError("Disposed SQLite snapshot lacks disposal evidence")
        stabilization_completed = _optional_time(
            stabilization.get("completed_at"), field="stabilization.completed_at"
        )
        if (
            disposed_at < retain_until
            or disposed_at > audited_at
            or stabilization_completed is None
            or disposed_at < stabilization_completed
        ):
            raise CloseoutEvidenceError("SQLite snapshot was disposed before its gates")
    else:
        raise CloseoutEvidenceError("Production cutover requires retained/disposed SQLite state")
    return {
        "state": state,
        "snapshot_sha256": snapshot_sha,
        "retention_approval_sha256": approval_sha,
        "retain_until": retain_until.isoformat(),
        "disposed_at": disposed_at.isoformat() if disposed_at else None,
        "disposal_evidence_sha256": disposal_sha,
        "writable": False,
    }, blockers


def _validate_dependency_summary(value: Mapping[str, Any]) -> dict[str, Any]:
    _exact_keys(
        value,
        {"release", "qualification", "production_cutover", "postcutover_publication"},
        context="closeout.dependencies",
    )
    release = value.get("release")
    qualification = value.get("qualification")
    production = value.get("production_cutover")
    publication = value.get("postcutover_publication")
    if release is None:
        if any(item is not None for item in (qualification, production, publication)):
            raise CloseoutEvidenceError("Closeout dependencies exist without a frozen release")
        return dict(value)
    if not isinstance(release, Mapping):
        raise CloseoutEvidenceError("Closeout frozen release summary is invalid")
    _exact_keys(
        release,
        {"fingerprint", "manifest_sha256", "commit", "images", "schema_head"},
        context="closeout.dependencies.release",
    )
    _sha256(release.get("fingerprint"), field="dependencies.release.fingerprint")
    _sha256(
        release.get("manifest_sha256"), field="dependencies.release.manifest_sha256"
    )
    commit = _text(release.get("commit"), field="dependencies.release.commit", minimum=40)
    if re.fullmatch(r"[0-9a-f]{40}", commit) is None:
        raise CloseoutEvidenceError("Closeout frozen release commit is invalid")
    images = release.get("images")
    if (
        not isinstance(images, list)
        or len(images) < 3
        or len(images) != len(set(images))
        or any(
            not isinstance(item, str)
            or re.fullmatch(r".+@sha256:[0-9a-f]{64}", item) is None
            for item in images
        )
    ):
        raise CloseoutEvidenceError("Closeout frozen release image pins are invalid")
    _text(release.get("schema_head"), field="dependencies.release.schema_head")

    if qualification is not None:
        if not isinstance(qualification, Mapping):
            raise CloseoutEvidenceError("Closeout qualification summary is invalid")
        _exact_keys(
            qualification,
            {"document_sha256", "created_at", "run_bundle_sha256"},
            context="closeout.dependencies.qualification",
        )
        _sha256(
            qualification.get("document_sha256"),
            field="dependencies.qualification.document_sha256",
        )
        _time(qualification.get("created_at"), field="dependencies.qualification.created_at")
        bundles = qualification.get("run_bundle_sha256")
        if (
            not isinstance(bundles, list)
            or len(bundles) != 3
            or len(set(bundles)) != 3
        ):
            raise CloseoutEvidenceError(
                "Closeout qualification must preserve three unique run bundles"
            )
        for index, checksum in enumerate(bundles):
            _sha256(checksum, field=f"dependencies.qualification.bundles[{index}]")
    if production is not None:
        if qualification is None or not isinstance(production, Mapping):
            raise CloseoutEvidenceError(
                "Closeout production summary requires trusted qualification"
            )
        _exact_keys(
            production,
            {
                "document_sha256",
                "report_id",
                "completed_at",
                "stabilization_started_at",
                "sqlite_snapshot_sha256",
            },
            context="closeout.dependencies.production_cutover",
        )
        _sha256(
            production.get("document_sha256"),
            field="dependencies.production.document_sha256",
        )
        _safe_identifier(production.get("report_id"), field="dependencies.production.report_id")
        completed = _time(
            production.get("completed_at"), field="dependencies.production.completed_at"
        )
        stabilization_started = _time(
            production.get("stabilization_started_at"),
            field="dependencies.production.stabilization_started_at",
        )
        if stabilization_started > completed:
            raise CloseoutEvidenceError("Production stabilization starts after cutover completion")
        _sha256(
            production.get("sqlite_snapshot_sha256"),
            field="dependencies.production.sqlite_snapshot_sha256",
        )
    if publication is not None:
        if production is None or not isinstance(publication, Mapping):
            raise CloseoutEvidenceError(
                "Closeout publication summary requires trusted production cutover"
            )
        _exact_keys(
            publication,
            {
                "document_sha256",
                "publication_id",
                "published_at",
                "release_notes_sha256",
            },
            context="closeout.dependencies.postcutover_publication",
        )
        _sha256(
            publication.get("document_sha256"),
            field="dependencies.publication.document_sha256",
        )
        _safe_identifier(
            publication.get("publication_id"), field="dependencies.publication.publication_id"
        )
        published_at = _time(
            publication.get("published_at"), field="dependencies.publication.published_at"
        )
        production_completed = _time(
            production.get("completed_at"), field="dependencies.production.completed_at"
        )
        if published_at < production_completed:
            raise CloseoutEvidenceError("Post-cutover publication predates production")
        _sha256(
            publication.get("release_notes_sha256"),
            field="dependencies.publication.release_notes_sha256",
        )
    return dict(value)


def _evaluate_closeout_input(
    raw: Mapping[str, Any],
    *,
    dependencies: Mapping[str, Any],
) -> tuple[dict[str, Any], list[str], str]:
    dependencies = _validate_dependency_summary(dependencies)
    _exact_keys(
        raw,
        {
            "kind",
            "schema_version",
            "audit_id",
            "audited_at",
            "auditor",
            "task_evidence",
            "release_gates",
            "stabilization",
            "post_cutover_verification",
            "backup_restore",
            "operational_audit",
            "availability",
            "sqlite_snapshot",
            "exceptions",
            "evidence_index_sha256",
            "no_omission_attestation",
        },
        context="closeout observations",
    )
    if (
        raw.get("kind") != "workchord-postgresql-closeout-observations"
        or raw.get("schema_version") != 1
    ):
        raise CloseoutEvidenceError("Closeout observations are not v1")
    audit_id = _safe_identifier(raw.get("audit_id"), field="closeout.audit_id")
    audited_at = _time(raw.get("audited_at"), field="closeout.audited_at")
    if audited_at > datetime.now(UTC) + timedelta(minutes=1):
        raise CloseoutEvidenceError("Closeout audit is future-dated")
    auditor = raw.get("auditor")
    if not isinstance(auditor, Mapping):
        raise CloseoutEvidenceError("Closeout independent auditor is missing")
    _exact_keys(auditor, {"identity", "independent"}, context="closeout.auditor")
    normalized_auditor = {
        "identity": _text(auditor.get("identity"), field="closeout.auditor.identity"),
        "independent": auditor.get("independent"),
    }
    if normalized_auditor["independent"] is not True:
        raise CloseoutEvidenceError("Closeout auditor must be independent")
    if raw.get("no_omission_attestation") != CLOSEOUT_INPUT_ATTESTATION:
        raise CloseoutEvidenceError("Closeout no-omission attestation differs")
    evidence_index = _sha256(
        raw.get("evidence_index_sha256"), field="closeout.evidence_index_sha256"
    )
    exception_map, blockers = _validate_closeout_exceptions(
        raw.get("exceptions"), audited_at=audited_at
    )
    tasks, task_blockers = _validate_evidence_matrix(
        raw.get("task_evidence"),
        expected_ids=DBM_TASK_IDS,
        allowed_statuses=frozenset({"complete", "waived", "incomplete"}),
        context="task_evidence",
        exceptions=exception_map,
        audited_at=audited_at,
        non_waivable=NON_WAIVABLE_TASKS,
    )
    gates, gate_blockers = _validate_evidence_matrix(
        raw.get("release_gates"),
        expected_ids=RELEASE_GATE_IDS,
        allowed_statuses=frozenset({"passed", "waived", "failed", "pending"}),
        context="release_gates",
        exceptions=exception_map,
        audited_at=audited_at,
        non_waivable=NON_WAIVABLE_GATES,
    )
    blockers.extend(task_blockers)
    blockers.extend(gate_blockers)

    qualification = dependencies.get("qualification")
    production = dependencies.get("production_cutover")
    publication = dependencies.get("postcutover_publication")
    exact_evidence = (
        ("DBM-QUAL-001", "G10", qualification),
        ("DBM-CUT-002", "G13", production),
        ("DBM-DOC-002", "G15", publication),
    )
    for task_id, gate_id, evidence in exact_evidence:
        if evidence is None:
            if tasks[task_id]["status"] == "complete" or gates[gate_id]["status"] == "passed":
                raise CloseoutEvidenceError(
                    f"{task_id}/{gate_id} claims completion without trusted external evidence"
                )
            blockers.append(f"{task_id}: trusted external evidence is missing")
        else:
            checksum = evidence["document_sha256"]
            if tasks[task_id] != {
                "status": "complete",
                "evidence_sha256": checksum,
                "exception_id": None,
            } or gates[gate_id] != {
                "status": "passed",
                "evidence_sha256": checksum,
                "exception_id": None,
            }:
                raise CloseoutEvidenceError(
                    f"{task_id}/{gate_id} does not bind the trusted evidence checksum"
                )

    stabilization, section_blockers = _validate_timed_status(
        raw.get("stabilization"),
        context="stabilization",
        audited_at=audited_at,
        production=production,
    )
    blockers.extend(section_blockers)
    verification, section_blockers = _validate_postcutover_verification(
        raw.get("post_cutover_verification"),
        audited_at=audited_at,
        production=production,
    )
    blockers.extend(section_blockers)
    release = dependencies.get("release")
    backup_restore, section_blockers = _validate_backup_restore(
        raw.get("backup_restore"),
        audited_at=audited_at,
        production=production,
        schema_head=release.get("schema_head") if isinstance(release, Mapping) else None,
    )
    blockers.extend(section_blockers)
    operational_audit, section_blockers = _validate_operational_audit(
        raw.get("operational_audit"), production_present=production is not None
    )
    blockers.extend(section_blockers)
    availability, section_blockers, availability_claim = _validate_availability(
        raw.get("availability"), audited_at=audited_at, production=production
    )
    blockers.extend(section_blockers)
    sqlite_snapshot, section_blockers = _validate_sqlite_snapshot(
        raw.get("sqlite_snapshot"),
        audited_at=audited_at,
        production=production,
        stabilization=stabilization,
    )
    blockers.extend(section_blockers)

    if gates["G14"]["status"] == "passed":
        if any(blocker.startswith("G14:") for blocker in blockers):
            raise CloseoutEvidenceError("G14 claims passed while stabilization evidence fails")
    elif not any(blocker.startswith("G14:") for blocker in blockers):
        raise CloseoutEvidenceError("G14 is not passed despite complete stabilization evidence")

    referenced_exceptions = {
        item["exception_id"]
        for item in [*tasks.values(), *gates.values()]
        if item["exception_id"] is not None
    }
    if referenced_exceptions != set(exception_map):
        raise CloseoutEvidenceError("Closeout contains unreferenced or missing exceptions")
    normalized_exceptions = [
        {
            **item,
            "expires_at": item["expires_at"].isoformat(),
        }
        for item in sorted(exception_map.values(), key=lambda entry: entry["id"])
    ]
    normalized = {
        "kind": raw["kind"],
        "schema_version": 1,
        "audit_id": audit_id,
        "audited_at": audited_at.isoformat(),
        "auditor": normalized_auditor,
        "task_evidence": tasks,
        "release_gates": gates,
        "stabilization": stabilization,
        "post_cutover_verification": verification,
        "backup_restore": backup_restore,
        "operational_audit": operational_audit,
        "availability": availability,
        "sqlite_snapshot": sqlite_snapshot,
        "exceptions": normalized_exceptions,
        "evidence_index_sha256": evidence_index,
        "no_omission_attestation": CLOSEOUT_INPUT_ATTESTATION,
    }
    unique_blockers = sorted(set(blockers))
    return normalized, unique_blockers, availability_claim


def _validate_closure_decision(
    document: Mapping[str, Any],
    *,
    trusted_public_key: Path,
) -> None:
    verify_signed_document(
        document,
        trusted_public_key=trusted_public_key,
        expected_kind="workchord-postgresql-closure-decision",
    )
    _exact_keys(
        document,
        {
            "kind",
            "schema_version",
            "decision_id",
            "created_at",
            "status",
            "verdict",
            "plan_status",
            "capacity_claim",
            "availability_claim",
            "dependencies",
            "observations",
            "blockers",
            "closure_task",
            "attestation",
            "signature",
            "document_sha256",
        },
        context="closure decision",
    )
    if document.get("schema_version") != 1 or document.get("capacity_claim") != CAPACITY_CLAIM:
        raise CloseoutEvidenceError("Closure decision contract differs")
    dependencies = document.get("dependencies")
    if not isinstance(dependencies, Mapping):
        raise CloseoutEvidenceError("Closure dependency summary is missing")
    _exact_keys(
        dependencies,
        {"release", "qualification", "production_cutover", "postcutover_publication"},
        context="closure.dependencies",
    )
    observations = document.get("observations")
    if not isinstance(observations, Mapping):
        raise CloseoutEvidenceError("Closure observations are missing")
    normalized, blockers, availability_claim = _evaluate_closeout_input(
        observations, dependencies=dependencies
    )
    if normalized != observations:
        raise CloseoutEvidenceError("Closure observations are not canonical")
    verdict = "SHIP" if not blockers else "NO-SHIP"
    if document.get("verdict") != verdict or document.get("blockers") != blockers:
        raise CloseoutEvidenceError("Closure verdict does not match derived blockers")
    if document.get("status") != ("approved" if verdict == "SHIP" else "blocked"):
        raise CloseoutEvidenceError("Closure status differs from verdict")
    if document.get("plan_status") != ("closed" if verdict == "SHIP" else "open"):
        raise CloseoutEvidenceError("Closure plan status differs from verdict")
    if document.get("availability_claim") != availability_claim:
        raise CloseoutEvidenceError("Closure availability claim differs")
    if document.get("closure_task") != {
        "id": "DBM-CLOSE-001",
        "status": "decision_issued" if verdict == "SHIP" else "audit_blocked",
        "evidence_reference": "this_signed_document",
    }:
        raise CloseoutEvidenceError("Closure task status differs")
    if document.get("attestation") != CLOSEOUT_DECISION_ATTESTATION:
        raise CloseoutEvidenceError("Closure decision attestation differs")
    if _time(document.get("created_at"), field="closure.created_at") < _time(
        observations.get("audited_at"), field="closure.audited_at"
    ):
        raise CloseoutEvidenceError("Closure decision predates its audit")


def finalize_closeout(
    *,
    input_path: Path,
    repository_root: Path | None,
    release_manifest_path: Path | None,
    qualification_report_path: Path | None,
    qualification_public_key: Path | None,
    production_cutover_path: Path | None,
    production_public_key: Path | None,
    publication_path: Path | None,
    publication_public_key: Path | None,
    signing_key: Path,
    signer: str,
    output_path: Path,
) -> dict[str, Any]:
    """Sign an independent verdict derived from complete closeout observations."""

    dependencies = _dependency_summary(
        repository_root=repository_root,
        release_manifest_path=release_manifest_path,
        qualification_report_path=qualification_report_path,
        qualification_public_key=qualification_public_key,
        production_cutover_path=production_cutover_path,
        production_public_key=production_public_key,
        publication_path=publication_path,
        publication_public_key=publication_public_key,
    )
    raw = _read_json_object(input_path)
    observations, blockers, availability_claim = _evaluate_closeout_input(
        raw, dependencies=dependencies
    )
    if signer.strip() != observations["auditor"]["identity"]:
        raise CloseoutEvidenceError(
            "Closure signer must be the named independent auditor"
        )
    verdict = "SHIP" if not blockers else "NO-SHIP"
    payload = {
        "kind": "workchord-postgresql-closure-decision",
        "schema_version": SCHEMA_VERSION,
        "decision_id": f"{observations['audit_id']}-decision",
        "created_at": datetime.now(UTC).isoformat(),
        "status": "approved" if verdict == "SHIP" else "blocked",
        "verdict": verdict,
        "plan_status": "closed" if verdict == "SHIP" else "open",
        "capacity_claim": dict(CAPACITY_CLAIM),
        "availability_claim": availability_claim,
        "dependencies": dependencies,
        "observations": observations,
        "blockers": blockers,
        "closure_task": {
            "id": "DBM-CLOSE-001",
            "status": "decision_issued" if verdict == "SHIP" else "audit_blocked",
            "evidence_reference": "this_signed_document",
        },
        "attestation": CLOSEOUT_DECISION_ATTESTATION,
    }
    _reject_secret_material(payload)
    return _sign_document(
        output_path,
        payload,
        signing_key=signing_key,
        signer=signer,
    )


def verify_closeout_report(*, report_path: Path, trusted_public_key: Path) -> str:
    """Verify a signed post-cutover publication or closure decision."""

    document = read_document(report_path)
    kind = document.get("kind")
    if kind == "workchord-postgresql-postcutover-publication":
        _validate_publication(
            document,
            trusted_public_key=trusted_public_key,
            signed=True,
        )
    elif kind == "workchord-postgresql-closure-decision":
        _validate_closure_decision(document, trusted_public_key=trusted_public_key)
    else:
        raise CloseoutEvidenceError(f"Unsupported closeout report kind: {kind!r}")
    return _sha256(document.get("document_sha256"), field="report.document_sha256")
