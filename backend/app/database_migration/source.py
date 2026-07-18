"""Read-only SQLite snapshot creation and source preflight."""

from __future__ import annotations

from contextlib import contextmanager
from datetime import UTC, datetime, timedelta
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
from typing import Any, Iterator, Mapping
from urllib.parse import quote

from sqlalchemy import Index, UniqueConstraint
from sqlalchemy.dialects import sqlite as sqlite_dialect
from sqlalchemy.sql.schema import Table

from app.database_migration.canonical import canonical_value, digest_rows
from app.database_migration.catalog import (
    TEXT_JSON_COLUMNS,
    TRANSFER_CATALOG_VERSION,
    application_tables,
    catalog_entries,
    column_family,
    column_max_length,
    transfer_order,
    transfer_tables,
)
from app.database_migration.manifest import (
    ManifestError,
    canonical_json_bytes,
    read_document,
    sha256_bytes,
    verify_document,
    write_document,
)
from app.services.upgrade_service import head_revision


SOURCE_MANIFEST_SCHEMA_VERSION = 1
DRAIN_EVIDENCE_SCHEMA_VERSION = 1
DRAIN_EVIDENCE_MAX_AGE = timedelta(minutes=15)
MINIMUM_FREE_SPACE_BYTES = 64 * 1024 * 1024


class MigrationDataError(RuntimeError):
    """A fail-closed source, transfer, or reconciliation condition."""

    def __init__(self, code: str, message: str):
        self.code = code
        super().__init__(message)


def _quoted(identifier: str) -> str:
    return '"' + identifier.replace('"', '""') + '"'


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def _source_file_set(path: Path) -> dict[str, dict[str, Any]]:
    files: dict[str, dict[str, Any]] = {}
    for suffix in ("", "-wal"):
        candidate = Path(str(path) + suffix)
        if candidate.exists():
            stat = candidate.stat()
            files[suffix or "database"] = {
                "size_bytes": stat.st_size,
                "sha256": _file_sha256(candidate),
            }
    return files


@contextmanager
def read_only_sqlite(path: Path) -> Iterator[sqlite3.Connection]:
    """Open an existing SQLite database with URI-enforced read-only access."""

    resolved = path.resolve(strict=True)
    uri = f"file:{quote(str(resolved), safe='/')}?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    connection.row_factory = sqlite3.Row
    try:
        connection.execute("PRAGMA query_only=ON")
        connection.execute("PRAGMA foreign_keys=ON")
        yield connection
    finally:
        connection.close()


def _parse_utc(value: Any, *, field: str) -> datetime:
    if not isinstance(value, str):
        raise MigrationDataError("invalid_writer_drain_evidence", f"{field} must be text")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise MigrationDataError(
            "invalid_writer_drain_evidence", f"{field} must be ISO-8601"
        ) from exc
    if parsed.tzinfo is None:
        raise MigrationDataError(
            "invalid_writer_drain_evidence", f"{field} must include a timezone"
        )
    return parsed.astimezone(UTC)


def validate_writer_drain_evidence(
    document: Mapping[str, Any], *, now: datetime | None = None
) -> str:
    """Validate controller plus all-replica writer-drain evidence."""

    try:
        checksum = verify_document(document)
    except ManifestError as exc:
        raise MigrationDataError("invalid_writer_drain_evidence", str(exc)) from exc
    if document.get("kind") != "workchord-writer-drain-evidence":
        raise MigrationDataError(
            "invalid_writer_drain_evidence", "Writer-drain evidence kind is unsupported"
        )
    if document.get("schema_version") != DRAIN_EVIDENCE_SCHEMA_VERSION:
        raise MigrationDataError(
            "invalid_writer_drain_evidence", "Writer-drain evidence schema is unsupported"
        )
    captured_at = _parse_utc(document.get("captured_at"), field="captured_at")
    current = (now or datetime.now(UTC)).astimezone(UTC)
    if captured_at > current + timedelta(minutes=1) or current - captured_at > DRAIN_EVIDENCE_MAX_AGE:
        raise MigrationDataError(
            "stale_writer_drain_evidence",
            "Writer-drain evidence must be captured within the previous 15 minutes",
        )

    controller = document.get("controller")
    if not isinstance(controller, dict):
        raise MigrationDataError(
            "invalid_writer_drain_evidence", "Controller evidence is required"
        )
    if controller.get("sqlite_owners_stopped") is not True:
        raise MigrationDataError(
            "source_may_be_writable", "Deployment controller has not stopped SQLite owners"
        )
    if controller.get("source_connection_count") != 0:
        raise MigrationDataError(
            "source_may_be_writable", "Source connection count must be exactly zero"
        )

    replicas = document.get("replicas")
    if not isinstance(replicas, list) or not replicas:
        raise MigrationDataError(
            "invalid_writer_drain_evidence", "At least one replica observation is required"
        )
    fingerprints: set[str] = set()
    replica_ids: set[str] = set()
    revisions: set[str] = set()
    for replica in replicas:
        if not isinstance(replica, dict):
            raise MigrationDataError(
                "invalid_writer_drain_evidence", "Replica observations must be objects"
            )
        maintenance = replica.get("maintenance")
        writer_drain = replica.get("writer_drain")
        if not isinstance(maintenance, dict) or not isinstance(writer_drain, dict):
            raise MigrationDataError(
                "invalid_writer_drain_evidence",
                "Every replica requires maintenance and writer_drain payloads",
            )
        if maintenance.get("mode") not in {"read-only-maintenance", "validation-only"}:
            raise MigrationDataError(
                "source_may_be_writable", "Every replica must use a fenced maintenance mode"
            )
        if writer_drain.get("drained") is not True:
            raise MigrationDataError(
                "source_may_be_writable", "Every replica must report writer_drain.drained=true"
            )
        if writer_drain.get("replica_agreement_required") is not True:
            raise MigrationDataError(
                "invalid_writer_drain_evidence",
                "Replica agreement must remain explicitly required",
            )
        fingerprint = maintenance.get("configuration_fingerprint")
        replica_id = maintenance.get("replica_id")
        revision = maintenance.get("revision")
        if not all(isinstance(value, str) and value for value in (fingerprint, replica_id, revision)):
            raise MigrationDataError(
                "invalid_writer_drain_evidence", "Replica identities are incomplete"
            )
        if writer_drain.get("configuration_fingerprint") != fingerprint:
            raise MigrationDataError(
                "invalid_writer_drain_evidence", "Readiness fingerprint fields disagree"
            )
        fingerprints.add(fingerprint)
        replica_ids.add(replica_id)
        revisions.add(revision)
    if len(replica_ids) != len(replicas):
        raise MigrationDataError(
            "invalid_writer_drain_evidence", "Replica identifiers must be unique"
        )
    if len(fingerprints) != 1 or len(revisions) != 1:
        raise MigrationDataError(
            "replica_configuration_disagreement",
            "Every replica must report one maintenance revision and fingerprint",
        )
    return checksum


def _snapshot_database(source: Path, destination: Path) -> None:
    if destination.exists():
        raise MigrationDataError(
            "snapshot_exists", "Refusing to overwrite an existing SQLite snapshot"
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(f".{destination.name}.{os.getpid()}.tmp")
    if temporary.exists():
        temporary.unlink()
    try:
        with read_only_sqlite(source) as source_connection:
            target_connection = sqlite3.connect(temporary)
            try:
                source_connection.backup(target_connection, pages=4096)
                target_connection.commit()
            finally:
                target_connection.close()
        with temporary.open("rb") as handle:
            os.fsync(handle.fileno())
        os.replace(temporary, destination)
        directory_fd = os.open(destination.parent, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    finally:
        if temporary.exists():
            temporary.unlink()


def _table_names(connection: sqlite3.Connection) -> set[str]:
    return {
        str(row[0])
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        if not str(row[0]).startswith("sqlite_")
    }


def _rows(
    connection: sqlite3.Connection, table: Table
) -> Iterator[Mapping[str, Any]]:
    columns = ", ".join(_quoted(column.name) for column in table.columns)
    order_columns = [column.name for column in table.primary_key.columns]
    if not order_columns:
        order_columns = [column.name for column in table.columns]
    order = ", ".join(_quoted(name) for name in order_columns)
    cursor = connection.execute(
        f"SELECT {columns} FROM {_quoted(table.name)} ORDER BY {order}"
    )
    while batch := cursor.fetchmany(1000):
        for row in batch:
            yield dict(row)


def _validate_inventory(connection: sqlite3.Connection) -> str:
    expected = set(application_tables()) | {"alembic_version"}
    actual = _table_names(connection)
    if actual != expected:
        raise MigrationDataError(
            "unknown_table_inventory",
            f"SQLite inventory differs; missing={sorted(expected - actual)}, "
            f"unexpected={sorted(actual - expected)}",
        )
    revisions = [
        str(row[0])
        for row in connection.execute(
            "SELECT version_num FROM alembic_version ORDER BY version_num"
        )
    ]
    expected_head = head_revision()
    if revisions != [expected_head]:
        raise MigrationDataError(
            "unsupported_source_revision",
            f"Source revision must be {expected_head}; found {revisions or ['none']}",
        )
    for name, table in application_tables().items():
        actual_columns = {
            str(row[1]) for row in connection.execute(f"PRAGMA table_info({_quoted(name)})")
        }
        expected_columns = {column.name for column in table.columns}
        if actual_columns != expected_columns:
            raise MigrationDataError(
                "source_column_inventory_mismatch",
                f"Column inventory differs for {name}: "
                f"missing={sorted(expected_columns - actual_columns)}, "
                f"unexpected={sorted(actual_columns - expected_columns)}",
            )
    target_owned_count = connection.execute(
        "SELECT COUNT(*) FROM database_migration_gates"
    ).fetchone()[0]
    if target_owned_count:
        raise MigrationDataError(
            "target_owned_source_rows",
            "Source contains target-owned database migration gate rows",
        )
    return expected_head


def _validate_integrity(connection: sqlite3.Connection) -> None:
    result = [str(row[0]) for row in connection.execute("PRAGMA integrity_check")]
    if result != ["ok"]:
        raise MigrationDataError("sqlite_integrity_failure", "; ".join(result[:10]))
    foreign_key_rows = list(connection.execute("PRAGMA foreign_key_check"))
    if foreign_key_rows:
        raise MigrationDataError(
            "sqlite_foreign_key_failure",
            f"SQLite foreign_key_check reported {len(foreign_key_rows)} row(s)",
        )


def _validate_orphans(connection: sqlite3.Connection) -> None:
    for table in transfer_tables().values():
        for constraint in table.foreign_key_constraints:
            child_columns = [element.parent.name for element in constraint.elements]
            parent_columns = [element.column.name for element in constraint.elements]
            parent = constraint.referred_table.name
            child_nonnull = " AND ".join(
                f"c.{_quoted(column)} IS NOT NULL" for column in child_columns
            )
            join = " AND ".join(
                f"c.{_quoted(child)} = p.{_quoted(parent_column)}"
                for child, parent_column in zip(child_columns, parent_columns, strict=True)
            )
            statement = (
                f"SELECT COUNT(*) FROM {_quoted(table.name)} c "
                f"LEFT JOIN {_quoted(parent)} p ON {join} "
                f"WHERE {child_nonnull} AND p.{_quoted(parent_columns[0])} IS NULL"
            )
            count = int(connection.execute(statement).fetchone()[0])
            if count:
                raise MigrationDataError(
                    "explicit_orphan_failure",
                    f"{table.name} has {count} orphan row(s) for {constraint.name}",
                )


def _validate_keys(connection: sqlite3.Connection) -> None:
    for table in transfer_tables().values():
        primary_key = [column.name for column in table.primary_key.columns]
        if not primary_key:
            raise MigrationDataError(
                "uncatalogued_primary_key", f"{table.name} has no stable primary key"
            )
        null_predicate = " OR ".join(
            f"{_quoted(column)} IS NULL" for column in primary_key
        )
        null_count = int(
            connection.execute(
                f"SELECT COUNT(*) FROM {_quoted(table.name)} WHERE {null_predicate}"
            ).fetchone()[0]
        )
        if null_count:
            raise MigrationDataError(
                "null_primary_key", f"{table.name} has {null_count} null primary key(s)"
            )
        unique_specs: list[tuple[list[str], str | None]] = [
            ([column.name for column in constraint.columns], None)
            for constraint in table.constraints
            if isinstance(constraint, UniqueConstraint)
        ]
        unique_specs.extend(
            (
                [column.name for column in index.columns],
                (
                    str(
                        predicate.compile(
                            dialect=sqlite_dialect.dialect(),
                            compile_kwargs={"literal_binds": True},
                        )
                    )
                    if (predicate := index.dialect_options["sqlite"].get("where"))
                    is not None
                    else None
                ),
            )
            for index in table.indexes
            if isinstance(index, Index) and index.unique
        )
        checked: set[tuple[tuple[str, ...], str | None]] = set()
        for columns, predicate in unique_specs:
            if not columns:
                continue
            signature = (tuple(columns), predicate)
            if signature in checked:
                continue
            checked.add(signature)
            names = ", ".join(_quoted(column) for column in columns)
            nonnull = " AND ".join(
                f"{_quoted(column)} IS NOT NULL" for column in columns
            )
            if predicate:
                nonnull += f" AND ({predicate})"
            duplicate = connection.execute(
                f"SELECT 1 FROM {_quoted(table.name)} WHERE {nonnull} "
                f"GROUP BY {names} HAVING COUNT(*) > 1 LIMIT 1"
            ).fetchone()
            if duplicate is not None:
                raise MigrationDataError(
                    "duplicate_unique_key",
                    f"{table.name} duplicates unique columns {columns}",
                )


def _validate_task_graphs(connection: sqlite3.Connection) -> None:
    parent_cycle = connection.execute(
        """
        WITH RECURSIVE ancestry(start_id, node_id) AS (
            SELECT id, parent_id FROM tasks WHERE parent_id IS NOT NULL
            UNION
            SELECT ancestry.start_id, tasks.parent_id
            FROM ancestry
            JOIN tasks ON tasks.id = ancestry.node_id
            WHERE tasks.parent_id IS NOT NULL
        )
        SELECT 1 FROM ancestry WHERE start_id = node_id LIMIT 1
        """
    ).fetchone()
    if parent_cycle is not None:
        raise MigrationDataError(
            "task_parent_cycle", "Task parent relationships contain a cycle"
        )

    dependency_cycle = connection.execute(
        """
        WITH RECURSIVE paths(start_id, node_id) AS (
            SELECT task_id, depends_on_id FROM task_dependencies
            UNION
            SELECT paths.start_id, dependencies.depends_on_id
            FROM paths
            JOIN task_dependencies dependencies ON dependencies.task_id = paths.node_id
        )
        SELECT 1 FROM paths WHERE start_id = node_id LIMIT 1
        """
    ).fetchone()
    if dependency_cycle is not None:
        raise MigrationDataError(
            "task_dependency_cycle", "Task dependency relationships contain a cycle"
        )


def _validate_values(connection: sqlite3.Connection) -> None:
    for table in transfer_tables().values():
        for column in table.columns:
            family = column_family(column)
            maximum_length = column_max_length(column)
            if maximum_length is not None:
                count = int(
                    connection.execute(
                        f"SELECT COUNT(*) FROM {_quoted(table.name)} "
                        f"WHERE {_quoted(column.name)} IS NOT NULL "
                        f"AND length({_quoted(column.name)}) > ?",
                        (maximum_length,),
                    ).fetchone()[0]
                )
                if count:
                    raise MigrationDataError(
                        "string_length_overflow",
                        f"{table.name}.{column.name} has values longer than "
                        f"the PostgreSQL limit of {maximum_length} characters",
                    )
            if family == "boolean":
                count = int(
                    connection.execute(
                        f"SELECT COUNT(*) FROM {_quoted(table.name)} "
                        f"WHERE {_quoted(column.name)} IS NOT NULL "
                        f"AND {_quoted(column.name)} NOT IN (0, 1)"
                    ).fetchone()[0]
                )
                if count:
                    raise MigrationDataError(
                        "invalid_boolean", f"{table.name}.{column.name} has invalid values"
                    )
            if family in {"datetime", "date", "json"}:
                cursor = connection.execute(
                    f"SELECT {_quoted(column.name)} FROM {_quoted(table.name)} "
                    f"WHERE {_quoted(column.name)} IS NOT NULL"
                )
                for row in cursor:
                    try:
                        canonical_value(column, row[0])
                    except ValueError as exc:
                        raise MigrationDataError(
                            f"invalid_{family}",
                            f"{table.name}.{column.name}: {exc}",
                        ) from exc
            if (table.name, column.name) in TEXT_JSON_COLUMNS:
                cursor = connection.execute(
                    f"SELECT {_quoted(column.name)} FROM {_quoted(table.name)} "
                    f"WHERE {_quoted(column.name)} IS NOT NULL"
                )
                for row in cursor:
                    try:
                        json.loads(row[0])
                    except (TypeError, json.JSONDecodeError) as exc:
                        raise MigrationDataError(
                            "invalid_text_json",
                            f"{table.name}.{column.name} contains malformed JSON",
                        ) from exc

    for row in connection.execute(
        "SELECT is_secret, value_json, secret_ciphertext FROM system_settings"
    ):
        is_secret, value_json, ciphertext = row
        if is_secret:
            if value_json is not None or not isinstance(ciphertext, str) or not ciphertext.startswith("gAAAA"):
                raise MigrationDataError(
                    "invalid_encrypted_setting_shape",
                    "Secret system settings must contain only a Fernet-shaped ciphertext",
                )
        elif ciphertext is not None:
            raise MigrationDataError(
                "invalid_encrypted_setting_shape",
                "Non-secret system settings cannot contain secret ciphertext",
            )


def _inspect_snapshot(connection: sqlite3.Connection) -> tuple[str, dict[str, Any]]:
    revision = _validate_inventory(connection)
    _validate_integrity(connection)
    _validate_orphans(connection)
    _validate_keys(connection)
    _validate_task_graphs(connection)
    _validate_values(connection)

    table_results: dict[str, Any] = {}
    tables = transfer_tables()
    for table_name in transfer_order():
        count, digest = digest_rows(tables[table_name], _rows(connection, tables[table_name]))
        table_results[table_name] = {"row_count": count, "canonical_sha256": digest}
    return revision, table_results


def preflight_source(
    *,
    source_path: Path,
    snapshot_path: Path,
    writer_drain_evidence_path: Path,
    manifest_path: Path,
    now: datetime | None = None,
) -> dict[str, Any]:
    """Create, validate, and manifest a stable SQLite migration snapshot."""

    source = source_path.resolve(strict=True)
    if not source.is_file():
        raise MigrationDataError("invalid_source", "SQLite source must be a file")
    if Path(str(source) + "-journal").exists():
        raise MigrationDataError(
            "active_rollback_journal", "SQLite rollback journal is still present"
        )
    try:
        evidence = read_document(writer_drain_evidence_path)
    except ManifestError as exc:
        raise MigrationDataError("invalid_writer_drain_evidence", str(exc)) from exc
    evidence_sha256 = validate_writer_drain_evidence(evidence, now=now)

    before_files = _source_file_set(source)
    source_size = sum(int(item["size_bytes"]) for item in before_files.values())
    required_free = max(MINIMUM_FREE_SPACE_BYTES, source_size * 4)
    snapshot_path.parent.mkdir(parents=True, exist_ok=True)
    available_free = shutil.disk_usage(snapshot_path.parent).free
    if available_free < required_free:
        raise MigrationDataError(
            "insufficient_free_space",
            f"Snapshot filesystem requires {required_free} free bytes",
        )

    try:
        _snapshot_database(source, snapshot_path)
    except sqlite3.DatabaseError as exc:
        raise MigrationDataError(
            "sqlite_snapshot_failure",
            "SQLite rejected the source while creating the backup-API snapshot",
        ) from exc
    after_files = _source_file_set(source)
    if before_files != after_files:
        raise MigrationDataError(
            "source_changed_during_snapshot",
            "SQLite database or WAL changed while the backup API was running",
        )

    snapshot_sha256 = _file_sha256(snapshot_path)
    try:
        with read_only_sqlite(snapshot_path) as connection:
            revision, table_results = _inspect_snapshot(connection)
    except sqlite3.DatabaseError as exc:
        raise MigrationDataError(
            "sqlite_snapshot_recheck_failure",
            "SQLite rejected the completed snapshot during its read-only recheck",
        ) from exc

    catalog = [
        {
            "table": entry.table_name,
            "disposition": entry.disposition,
            "primary_key": list(entry.primary_key),
            "staged_reference_columns": list(entry.staged_reference_columns),
        }
        for entry in catalog_entries()
    ]
    stable_identity = {
        "database": before_files.get("database"),
        "wal": before_files.get("-wal"),
    }
    manifest_id = sha256_bytes(
        canonical_json_bytes(
            {
                "catalog_version": TRANSFER_CATALOG_VERSION,
                "snapshot_sha256": snapshot_sha256,
                "source_revision": revision,
                "tables": table_results,
            }
        )
    )
    payload = {
        "kind": "workchord-sqlite-source-manifest",
        "schema_version": SOURCE_MANIFEST_SCHEMA_VERSION,
        "manifest_id": manifest_id,
        "migration_run_id": manifest_id[:32],
        "transfer_catalog_version": TRANSFER_CATALOG_VERSION,
        "source_revision": revision,
        "target_revision": revision,
        "source_identity": stable_identity,
        "snapshot": {
            "sha256": snapshot_sha256,
            "size_bytes": snapshot_path.stat().st_size,
            "fsynced": True,
            "read_only_recheck": True,
        },
        "writer_drain_evidence_sha256": evidence_sha256,
        "catalog": catalog,
        "transfer_order": list(transfer_order()),
        "tables": table_results,
        "totals": {
            "rows": sum(int(item["row_count"]) for item in table_results.values()),
            "estimated_transfer_bytes": source_size,
            "estimated_seconds_at_25_mib_per_second": round(
                source_size / (25 * 1024 * 1024), 3
            ),
            "required_free_space_bytes": required_free,
        },
        "repair_policy": {
            "version": "fail-closed-no-source-repair-v1",
            "automatic_source_repairs": [],
            "anomalies": [],
        },
    }
    return write_document(manifest_path, payload)
