#!/usr/bin/env python3
"""Fail closed when the PostgreSQL pre-cutover documentation drifts."""

from __future__ import annotations

from pathlib import Path
import re
import sys


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
DOCUMENTS = (
    Path("README.md"),
    Path("docs/database-portability-policy.md"),
    Path("docs/database-runtime-policy.md"),
    Path("docs/runbooks/postgresql-operations.md"),
    Path("docs/runbooks/postgresql-deployment.md"),
    Path("docs/runbooks/postgresql-security.md"),
    Path("docs/runbooks/postgresql-backup-restore.md"),
    Path("docs/runbooks/postgresql-qualification.md"),
    Path("docs/runbooks/postgresql-rehearsal-cutover-evidence.md"),
    Path("docs/runbooks/postgresql-postcutover-release-and-closeout.md"),
    Path("docs/runbooks/postgresql-troubleshooting.md"),
    Path("docs/runbooks/sqlite-to-postgresql-migration.md"),
    Path("docs/runbooks/sqlite-to-postgresql-cutover.md"),
    Path("docs/runbooks/postgresql-cutover-checklist.md"),
)
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
SHELL_FENCE_PATTERN = re.compile(
    r"(?:```|~~~)(?:bash|sh)\s*\n(.*?)(?:```|~~~)",
    re.DOTALL | re.IGNORECASE,
)
LIVE_SQLITE_COPY_PATTERN = re.compile(
    r"(?:^|\n)\s*(?:sudo\s+)?(?:cp|rsync)\b[^\n]*(?:\.db|\.sqlite)\b",
    re.IGNORECASE,
)


class DocumentationContractError(RuntimeError):
    """Raised when an operator-facing contract is incomplete or unsafe."""


def _read(relative_path: Path) -> str:
    path = REPOSITORY_ROOT / relative_path
    if not path.is_file():
        raise DocumentationContractError(f"Missing required document: {relative_path}")
    return path.read_text(encoding="utf-8")


def _require(relative_path: Path, *snippets: str) -> None:
    text = _read(relative_path)
    normalized_text = " ".join(text.split())
    missing = [
        snippet
        for snippet in snippets
        if snippet not in text and " ".join(snippet.split()) not in normalized_text
    ]
    if missing:
        raise DocumentationContractError(
            f"{relative_path} is missing required contract text: {missing}"
        )


def _local_link_count(relative_path: Path) -> int:
    text = _read(relative_path)
    count = 0
    for raw_target in LINK_PATTERN.findall(text):
        target = raw_target.strip().strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target_path = target.split("#", 1)[0]
        if not target_path:
            continue
        resolved = (REPOSITORY_ROOT / relative_path).parent / target_path
        if not resolved.resolve().exists():
            raise DocumentationContractError(
                f"Broken local link in {relative_path}: {raw_target}"
            )
        count += 1
    return count


def check_documentation() -> tuple[int, int]:
    texts = {path: _read(path) for path in DOCUMENTS}
    combined = "\n".join(texts.values())

    forbidden = {
        "backend/.venv/bin": "commands must use the documented root virtual environment",
        "backend data is stored in the `workchord_data` volume": (
            "the integration topology no longer uses the legacy SQLite volume"
        ),
        "backend with SQLite storage": (
            "the product summary must not describe SQLite as integration storage"
        ),
    }
    for snippet, reason in forbidden.items():
        if snippet.lower() in combined.lower():
            raise DocumentationContractError(f"Forbidden stale text {snippet!r}: {reason}")

    for path, text in texts.items():
        for block in SHELL_FENCE_PATTERN.findall(text):
            if LIVE_SQLITE_COPY_PATTERN.search(block):
                raise DocumentationContractError(
                    f"Unsafe live SQLite copy command in {path}"
                )

    _require(
        Path("README.md"),
        "PostgreSQL 18",
        "postgresql-operations.md",
        "postgresql-backup-restore.md",
        "postgresql-rehearsal-cutover-evidence.md",
        "postgresql-postcutover-release-and-closeout.md",
        "1,250 opaque browser identities, 250 active",
        "Opaque identities are not authenticated people",
        "missing production evidence remains NO-SHIP",
    )
    _require(
        Path(".env.example"),
        "DATABASE_MIGRATION_URL=postgresql+psycopg://",
        "DATABASE_RUNTIME_URL=postgresql+psycopg://",
        "DATABASE_BACKUP_URL=postgresql://",
        "DATABASE_EXTERNAL_BACKUP_REFERENCE=",
        "DATABASE_WEB_POOL_SIZE=15",
        "DATABASE_WORKER_POOL_SIZE=8",
        "DATABASE_TLS_CERT_DIR=",
    )
    _require(
        Path("docs/runbooks/postgresql-operations.md"),
        "DATABASE_POSTGRESQL_REQUIRED=true",
        "PG_UNICODE_FAST",
        "workchord, pg_catalog",
        "40",
        "20",
        "verify-full",
        "docker compose -f docker-compose.prod.yml config --quiet",
        ".venv/bin/python -m app.cli.upgrade --schema-only",
        ".venv/bin/python -m app.cli.upgrade --repairs-only",
        "workchord-worker",
        "/health/ready",
        "MAINTENANCE_MODE",
        "three unique, consecutive, non-overlapping",
        "Do not mark DBM-DOC-001 complete",
    )
    _require(
        Path("docs/runbooks/sqlite-to-postgresql-migration.md"),
        ".venv/bin/workchord-db-migrate preflight",
        ".venv/bin/workchord-db-migrate load",
        "--phase raw",
        "--phase final",
        "A bare online file copy is unsupported",
    )
    _require(
        Path("docs/runbooks/postgresql-backup-restore.md"),
        "docker compose -f docker-compose.prod.yml --profile backup run --rm logical-backup",
        "isolated restore",
        "never uses `--clean`",
    )
    _require(
        Path("docs/runbooks/postgresql-qualification.md"),
        "DBM-QUAL-001 passes only after",
        "seven finalized load results",
        "They must be unique, consecutive, non-overlapping,",
        "PYTHONPATH=backend .venv/bin/python scripts/load/qualify.py verify",
        "does not certify 1,250 authenticated people",
    )
    _require(
        Path("docs/runbooks/postgresql-rehearsal-cutover-evidence.md"),
        "workchord-db-cutover",
        "records and verifies evidence only",
        "independently provisioned public key",
        "postgresql-cutover-execution-v1.schema.json",
        "mode: abort_drill",
        "sequence numbers `1` then `2`",
        "finalize-rehearsal-series",
        "authorize-production",
        "finalize-production",
        "first accepted PostgreSQL application write",
        "never reopen SQLite",
    )
    _require(
        Path("docs/runbooks/postgresql-postcutover-release-and-closeout.md"),
        "DBM-DOC-002",
        "DBM-CLOSE-001",
        "workchord-db-closeout publish-release",
        "workchord-db-closeout finalize-closeout",
        "postgresql-postcutover-publication-input-v1.schema.json",
        "postgresql-closeout-observations-v1.schema.json",
        "Missing production evidence produces `NO-SHIP`",
        "1,250 opaque browser identities, 250 active browser sessions, and",
        "does not certify 1,250 authenticated people",
        "sole writable production system of record",
        "SQLite production support removed",
        "30 consecutive days",
        "G10, G13, G14, G15 are non-waivable",
        "does not accept a requested verdict",
        "leaves the plan and failed tasks open",
    )
    _require(
        Path("docs/runbooks/sqlite-to-postgresql-cutover.md"),
        "postgresql-cutover-checklist.md",
        "180 min total",
        "Mandatory stop conditions",
        "first accepted PostgreSQL application write is the point of no return",
        "There is no reverse synchronization",
    )
    checklist = texts[Path("docs/runbooks/postgresql-cutover-checklist.md")]
    for gate in (f"C{index:02d}" for index in range(1, 14)):
        if gate not in checklist:
            raise DocumentationContractError(f"Cutover checklist is missing {gate}")
    _require(
        Path("docs/runbooks/postgresql-troubleshooting.md"),
        "Never disable `DATABASE_POSTGRESQL_REQUIRED` in production",
        "never fall back from `verify-full`",
        "Never copy the live file",
        "never switch back to SQLite after PostgreSQL writes reopen",
        "Do not improvise a destructive command",
    )

    link_count = sum(_local_link_count(path) for path in DOCUMENTS)
    return len(DOCUMENTS), link_count


def main() -> int:
    try:
        document_count, link_count = check_documentation()
    except DocumentationContractError as exc:
        print(f"PostgreSQL documentation contract failed: {exc}", file=sys.stderr)
        return 1
    print(
        "PostgreSQL documentation contract passed "
        f"({document_count} documents, {link_count} local links)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
