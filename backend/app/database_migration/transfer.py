"""Catalogued PostgreSQL loading, repairs, and two-phase reconciliation."""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping
from contextlib import contextmanager
from datetime import UTC, datetime
import hashlib
import json
import os
from pathlib import Path
from typing import Any

from cryptography.fernet import Fernet, InvalidToken
from sqlalchemy import and_, bindparam, create_engine, func, inspect, select, text, update
from sqlalchemy.engine import Connection, Engine
from sqlalchemy.pool import NullPool

from app.config import get_settings
from app.database_migration.canonical import (
    canonical_value,
    digest_rows,
    row_sha256,
    storage_value,
)
from app.database_migration.catalog import (
    TRANSFER_CATALOG_VERSION,
    application_tables,
    catalog_entries,
    staged_reference_columns,
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
from app.database_migration.source import (
    MigrationDataError,
    _file_sha256,
    _inspect_snapshot,
    _rows,
    read_only_sqlite,
)
from app.models.database_migration import DatabaseMigrationGate
from app.services.upgrade_service import database_configuration, head_revision
from app.utils.time import utc_now


LOAD_REPORT_SCHEMA_VERSION = 1
RECONCILIATION_REPORT_SCHEMA_VERSION = 1
REPAIR_REPORT_SCHEMA_VERSION = 1
MAXIMUM_CHUNK_SIZE = 10_000
MIGRATION_LOADER_LOCK_NAMESPACE = int.from_bytes(b"WCML", "big")
REPAIR_OWNED_TABLES = frozenset(
    {
        "calendars",
        "github_status_automation_rules",
        "label_groups",
        "labels",
        "saved_views",
        "system_settings",
        "work_templates",
    }
)


def _target_engine() -> tuple[Engine, Any]:
    configuration = database_configuration()
    if configuration.backend != "postgresql":
        raise MigrationDataError(
            "invalid_target_dialect", "Migration target must use postgresql+psycopg"
        )
    engine = create_engine(
        configuration.sync_url,
        poolclass=NullPool,
        connect_args=dict(configuration.connect_args),
    )
    return engine, configuration


def _signed_int32(value: int) -> int:
    if not 0 <= value <= 0xFFFFFFFF:
        raise ValueError(f"{value} is outside the unsigned 32-bit range")
    return value if value <= 0x7FFFFFFF else value - 0x100000000


@contextmanager
def _exclusive_loader_connection(engine: Engine) -> Iterator[Connection]:
    with engine.connect() as connection:
        database_oid = _signed_int32(
            int(
                connection.execute(
                    text(
                        "SELECT oid::bigint FROM pg_database "
                        "WHERE datname = current_database()"
                    )
                ).scalar_one()
            )
        )
        acquired = False
        try:
            acquired = bool(
                connection.execute(
                    text(
                        "SELECT pg_try_advisory_lock("
                        "CAST(:namespace AS integer), CAST(:database_oid AS integer))"
                    ),
                    {
                        "namespace": MIGRATION_LOADER_LOCK_NAMESPACE,
                        "database_oid": database_oid,
                    },
                ).scalar_one()
            )
            connection.commit()
            if not acquired:
                raise MigrationDataError(
                    "migration_loader_busy",
                    "Another migration loader is active for this target database",
                )
            yield connection
        finally:
            if acquired:
                try:
                    if connection.in_transaction():
                        connection.rollback()
                except Exception:
                    pass
                if not connection.invalidated:
                    try:
                        connection.execute(
                            text(
                                "SELECT pg_advisory_unlock("
                                "CAST(:namespace AS integer), "
                                "CAST(:database_oid AS integer))"
                            ),
                            {
                                "namespace": MIGRATION_LOADER_LOCK_NAMESPACE,
                                "database_oid": database_oid,
                            },
                        )
                        connection.commit()
                    except Exception:
                        # Closing the physical session is the crash-safe fallback.
                        try:
                            if connection.in_transaction():
                                connection.rollback()
                        except Exception:
                            pass


def target_identifier(configuration: Any) -> str:
    """Return an exact secret-free target identifier for operator confirmation."""

    url = configuration.sync_url
    host = url.host or "local-socket"
    port = url.port or 5432
    return f"{host}:{port}/{url.database}"


def _target_identity_sha256(configuration: Any) -> str:
    url = configuration.sync_url
    return sha256_bytes(
        canonical_json_bytes(
            {
                "database": url.database,
                "host": url.host or "local-socket",
                "port": url.port or 5432,
                "schema": "workchord",
                "username": url.username or "",
            }
        )
    )


def _authorize_target(configuration: Any, authorized_target: str) -> str:
    actual = target_identifier(configuration)
    if authorized_target != actual:
        raise MigrationDataError(
            "unauthorized_target",
            f"Resolved target {actual!r} does not match the explicit authorization",
        )
    return actual


def _load_source_manifest(path: Path, snapshot_path: Path) -> dict[str, Any]:
    try:
        manifest = read_document(path)
    except ManifestError as exc:
        raise MigrationDataError("invalid_source_manifest", str(exc)) from exc
    if manifest.get("kind") != "workchord-sqlite-source-manifest":
        raise MigrationDataError("invalid_source_manifest", "Source manifest kind is unsupported")
    if manifest.get("schema_version") != 1:
        raise MigrationDataError("invalid_source_manifest", "Source manifest schema is unsupported")
    if manifest.get("transfer_catalog_version") != TRANSFER_CATALOG_VERSION:
        raise MigrationDataError("invalid_source_manifest", "Transfer catalog version differs")
    if manifest.get("source_revision") != head_revision():
        raise MigrationDataError(
            "stale_source_manifest", "Source manifest does not target the packaged Alembic head"
        )
    snapshot = manifest.get("snapshot")
    if not isinstance(snapshot, dict) or snapshot.get("sha256") != _file_sha256(snapshot_path):
        raise MigrationDataError(
            "snapshot_checksum_mismatch", "SQLite snapshot does not match its source manifest"
        )
    expected_catalog = [
        {
            "table": entry.table_name,
            "disposition": entry.disposition,
            "primary_key": list(entry.primary_key),
            "staged_reference_columns": list(entry.staged_reference_columns),
        }
        for entry in catalog_entries()
    ]
    if manifest.get("catalog") != expected_catalog:
        raise MigrationDataError(
            "stale_transfer_catalog", "Source manifest catalog differs from the packaged catalog"
        )
    if manifest.get("transfer_order") != list(transfer_order()):
        raise MigrationDataError(
            "stale_transfer_catalog", "Source manifest transfer order differs"
        )
    with read_only_sqlite(snapshot_path) as source:
        revision, live_tables = _inspect_snapshot(source)
    if revision != manifest.get("source_revision") or live_tables != manifest.get("tables"):
        raise MigrationDataError(
            "source_recheck_mismatch", "Read-only source recheck differs from its manifest"
        )
    return manifest


def _optional_evidence(
    path: Path | None,
    *,
    kind: str,
    target: str,
    minimum_bytes: int | None = None,
) -> str | None:
    if path is None:
        return None
    try:
        document = read_document(path)
    except ManifestError as exc:
        raise MigrationDataError("invalid_operational_evidence", str(exc)) from exc
    if document.get("kind") != kind or document.get("target_identifier") != target:
        raise MigrationDataError(
            "invalid_operational_evidence", f"{kind} does not match the resolved target"
        )
    if kind == "workchord-target-capacity-evidence":
        free_space = document.get("free_space_bytes")
        if not isinstance(free_space, dict):
            raise MigrationDataError(
                "invalid_operational_evidence", "Capacity evidence needs free_space_bytes"
            )
        required = int(minimum_bytes or 0)
        for area in ("data", "index", "temporary", "wal", "archive"):
            value = free_space.get(area)
            if not isinstance(value, int) or value < required:
                raise MigrationDataError(
                    "insufficient_target_capacity",
                    f"Target {area} free space must be at least {required} bytes",
                )
    if kind == "workchord-loader-method-evidence":
        if document.get("approved_method") != "bounded-inserts-v1":
            raise MigrationDataError(
                "unapproved_loader_method", "This release implements bounded-inserts-v1"
            )
        benchmark = document.get("benchmark")
        if not isinstance(benchmark, dict) or not all(
            isinstance(benchmark.get(key), (int, float))
            for key in ("copy_rows_per_second", "bounded_insert_rows_per_second", "wal_bytes")
        ):
            raise MigrationDataError(
                "invalid_operational_evidence", "Loader evidence requires comparison metrics"
            )
    return str(document["document_sha256"])


def _assert_postgresql_contract(connection: Connection) -> None:
    database_contract = connection.execute(
        text(
            "SELECT current_setting('server_version_num')::integer AS version_num, "
            "pg_encoding_to_char(encoding) AS encoding, "
            "datlocprovider::text AS locale_provider, datlocale, datcollversion "
            "FROM pg_database WHERE datname = current_database()"
        )
    ).mappings().one()
    if database_contract["version_num"] // 10_000 != 18:
        raise MigrationDataError(
            "target_postgresql_version_mismatch",
            "Migration target must run PostgreSQL major version 18",
        )
    if (
        database_contract["encoding"] != "UTF8"
        or database_contract["locale_provider"] != "b"
        or database_contract["datlocale"] != "PG_UNICODE_FAST"
        or database_contract["datcollversion"] != "1"
    ):
        raise MigrationDataError(
            "target_locale_mismatch",
            "Migration target must use UTF8 and builtin PG_UNICODE_FAST collation version 1",
        )
    actual_tables = set(inspect(connection).get_table_names())
    expected_tables = set(application_tables()) | {"alembic_version"}
    if actual_tables != expected_tables:
        raise MigrationDataError(
            "target_schema_inventory_mismatch",
            f"Target tables differ; missing={sorted(expected_tables - actual_tables)}, "
            f"unexpected={sorted(actual_tables - expected_tables)}",
        )
    revisions = list(
        connection.execute(
            text("SELECT version_num FROM alembic_version ORDER BY version_num")
        ).scalars()
    )
    if revisions != [head_revision()]:
        raise MigrationDataError(
            "target_revision_mismatch", f"Target revision is {revisions or ['none']}"
        )
    timezone = str(connection.execute(text("SHOW TimeZone")).scalar_one()).upper()
    if timezone not in {"UTC", "ETC/UTC"}:
        raise MigrationDataError("target_timezone_mismatch", "Target timezone must be UTC")
    schemas = list(connection.execute(text("SELECT current_schemas(false)")).scalar_one())
    if not schemas or schemas[0] != "workchord" or "public" in schemas:
        raise MigrationDataError(
            "target_search_path_mismatch",
            "Target search_path must begin with workchord and exclude public",
        )
    invalid_constraints = list(
        connection.execute(
            text(
                "SELECT conname FROM pg_constraint c "
                "JOIN pg_namespace n ON n.oid = c.connamespace "
                "WHERE n.nspname = 'workchord' AND NOT c.convalidated "
                "ORDER BY conname"
            )
        ).scalars()
    )
    if invalid_constraints:
        raise MigrationDataError(
            "target_unvalidated_constraints",
            f"Target has unvalidated constraints: {invalid_constraints}",
        )


def _target_rows(connection: Connection, table: Any) -> Iterator[Mapping[str, Any]]:
    ordering = list(table.primary_key.columns) or list(table.columns)
    result = connection.execute(select(table).order_by(*ordering)).mappings()
    while batch := result.fetchmany(1000):
        yield from batch


def _table_count(connection: Connection, table: Any) -> int:
    return int(connection.execute(select(func.count()).select_from(table)).scalar_one())


def _gate(connection: Connection, run_id: str) -> Mapping[str, Any] | None:
    return connection.execute(
        select(DatabaseMigrationGate.__table__).where(
            DatabaseMigrationGate.run_id == run_id
        )
    ).mappings().first()


def _mark_failed(engine: Engine, run_id: str, code: str) -> None:
    try:
        with engine.begin() as connection:
            connection.execute(
                update(DatabaseMigrationGate)
                .where(DatabaseMigrationGate.run_id == run_id)
                .values(status="failed", failure_code=code, updated_at=utc_now())
            )
    except Exception:
        # The original failure remains authoritative; readiness also fails if
        # the gate database itself is unavailable.
        return


def _mark_load_failed(connection: Connection, run_id: str, code: str) -> None:
    if connection.invalidated:
        return
    try:
        if connection.in_transaction():
            connection.rollback()
        with connection.begin():
            connection.execute(
                update(DatabaseMigrationGate)
                .where(DatabaseMigrationGate.run_id == run_id)
                .values(status="failed", failure_code=code, updated_at=utc_now())
            )
    except Exception:
        # Do not reconnect outside the lock-owning session to rewrite the gate.
        try:
            if connection.in_transaction():
                connection.rollback()
        except Exception:
            pass


def _initialize_gate(
    connection: Connection,
    *,
    manifest: Mapping[str, Any],
    target_identity_sha256: str,
) -> Mapping[str, Any]:
    run_id = str(manifest["migration_run_id"])
    all_gates = list(
        connection.execute(select(DatabaseMigrationGate.__table__)).mappings()
    )
    matching = next((gate for gate in all_gates if gate["run_id"] == run_id), None)
    if matching is not None:
        if (
            matching["source_manifest_sha256"] != manifest["document_sha256"]
            or matching["source_snapshot_sha256"] != manifest["snapshot"]["sha256"]
            or matching["target_identity_sha256"] != target_identity_sha256
        ):
            raise MigrationDataError(
                "migration_gate_identity_mismatch", "Existing run gate has different identities"
            )
        return matching
    if all_gates:
        raise MigrationDataError(
            "target_contains_other_migration",
            "Target already contains a different migration run gate",
        )
    populated = [
        table_name
        for table_name, table in transfer_tables().items()
        if _table_count(connection, table) != 0
    ]
    if populated:
        raise MigrationDataError(
            "target_not_empty", f"Approved target has application rows in {populated}"
        )
    connection.execute(
        DatabaseMigrationGate.__table__.insert().values(
            run_id=run_id,
            source_manifest_sha256=manifest["document_sha256"],
            source_snapshot_sha256=manifest["snapshot"]["sha256"],
            target_identity_sha256=target_identity_sha256,
            status="loading",
            completed_tables=[],
            created_at=utc_now(),
            updated_at=utc_now(),
        )
    )
    return _gate(connection, run_id) or {}


def _converted_batch(
    table: Any,
    rows: Iterable[Mapping[str, Any]],
    *,
    staged_columns: set[str],
) -> list[dict[str, Any]]:
    converted: list[dict[str, Any]] = []
    for row in rows:
        item = {
            column.name: storage_value(column, row[column.name])
            for column in table.columns
        }
        for name in staged_columns:
            item[name] = None
        converted.append(item)
    return converted


def _load_table(
    connection: Connection,
    source: Any,
    table: Any,
    *,
    chunk_size: int,
) -> int:
    staged = set(staged_reference_columns(table))
    source_rows = _rows(source, table)
    loaded = 0
    while True:
        raw_batch: list[Mapping[str, Any]] = []
        try:
            for _ in range(chunk_size):
                raw_batch.append(next(source_rows))
        except StopIteration:
            pass
        if not raw_batch:
            break
        connection.execute(
            table.insert(),
            _converted_batch(table, raw_batch, staged_columns=staged),
        )
        loaded += len(raw_batch)
        if len(raw_batch) < chunk_size:
            break
    return loaded


def _restore_staged_references(
    connection: Connection,
    source: Any,
    table: Any,
    *,
    chunk_size: int,
) -> int:
    staged = list(staged_reference_columns(table))
    if not staged:
        return 0
    primary_key = list(table.primary_key.columns)
    preserved_onupdate = [
        column.name
        for column in table.columns
        if column.onupdate is not None and column.name not in staged
    ]
    where = and_(
        *(column == bindparam(f"pk_{column.name}") for column in primary_key)
    )
    statement = update(table).where(where).values(
        {
            name: bindparam(f"value_{name}")
            for name in [*staged, *preserved_onupdate]
        }
    )
    parameters: list[dict[str, Any]] = []
    updated = 0
    for row in _rows(source, table):
        if not any(row[name] is not None for name in staged):
            continue
        item = {
            f"pk_{column.name}": storage_value(column, row[column.name])
            for column in primary_key
        }
        item.update(
            {
                f"value_{name}": storage_value(table.c[name], row[name])
                for name in [*staged, *preserved_onupdate]
            }
        )
        parameters.append(item)
        if len(parameters) == chunk_size:
            connection.execute(statement, parameters)
            updated += len(parameters)
            parameters = []
    if parameters:
        connection.execute(statement, parameters)
        updated += len(parameters)
    return updated


def _repair_sequences(connection: Connection) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for table_name in transfer_order():
        table = transfer_tables()[table_name]
        primary_key = list(table.primary_key.columns)
        if len(primary_key) != 1:
            continue
        column = primary_key[0]
        if not column.autoincrement or "int" not in type(column.type).__name__.lower():
            continue
        sequence = connection.execute(
            text("SELECT pg_get_serial_sequence(:table_name, :column_name)"),
            {"table_name": f"workchord.{table_name}", "column_name": column.name},
        ).scalar_one_or_none()
        if not sequence:
            continue
        maximum = connection.execute(select(func.max(column))).scalar_one()
        if maximum is None:
            connection.execute(
                text("SELECT setval(CAST(:sequence AS regclass), 1, false)"),
                {"sequence": sequence},
            )
            next_value = 1
        else:
            connection.execute(
                text("SELECT setval(CAST(:sequence AS regclass), :maximum, true)"),
                {"sequence": sequence, "maximum": int(maximum)},
            )
            next_value = int(maximum) + 1
        sequence_literal = str(sequence).replace("'", "''")
        savepoint = connection.begin_nested()
        try:
            connection.execute(
                text(
                    "CREATE TEMP TABLE workchord_generated_id_probe "
                    "(id bigint PRIMARY KEY DEFAULT "
                    f"nextval('{sequence_literal}'::regclass)) ON COMMIT DROP"
                )
            )
            generated_id = int(
                connection.execute(
                    text(
                        "INSERT INTO pg_temp.workchord_generated_id_probe "
                        "DEFAULT VALUES RETURNING id"
                    )
                ).scalar_one()
            )
            collision = connection.execute(
                select(func.count()).select_from(table).where(column == generated_id)
            ).scalar_one()
            if collision or (maximum is not None and generated_id <= int(maximum)):
                raise MigrationDataError(
                    "sequence_collision_risk",
                    f"{table_name}.{column.name} generated an existing identifier",
                )
        finally:
            savepoint.rollback()
        increment = int(
            connection.execute(
                text(
                    "SELECT seqincrement FROM pg_sequence "
                    "WHERE seqrelid = CAST(:sequence AS regclass)"
                ),
                {"sequence": sequence},
            ).scalar_one()
        )
        results[table_name] = {
            "column": column.name,
            "maximum": int(maximum) if maximum is not None else None,
            "reset_next_value": next_value,
            "generated_id_probe": generated_id,
            "probe_rolled_back": True,
            "next_value": generated_id + increment,
            "collision_safe": True,
        }
    return results


def load_snapshot(
    *,
    snapshot_path: Path,
    source_manifest_path: Path,
    report_path: Path,
    authorized_target: str,
    capacity_evidence_path: Path | None = None,
    loader_method_evidence_path: Path | None = None,
    chunk_size: int = 1000,
    _failure_after_table: str | None = None,
) -> dict[str, Any]:
    """Load a catalogued snapshot into an empty, Alembic-current target."""

    if not 1 <= chunk_size <= MAXIMUM_CHUNK_SIZE:
        raise MigrationDataError(
            "invalid_chunk_size", f"Chunk size must be between 1 and {MAXIMUM_CHUNK_SIZE}"
        )
    manifest = _load_source_manifest(source_manifest_path, snapshot_path)
    run_id = str(manifest["migration_run_id"])
    engine, configuration = _target_engine()
    target = _authorize_target(configuration, authorized_target)
    target_sha256 = _target_identity_sha256(configuration)
    capacity_sha256 = _optional_evidence(
        capacity_evidence_path,
        kind="workchord-target-capacity-evidence",
        target=target,
        minimum_bytes=int(manifest["totals"]["required_free_space_bytes"]),
    )
    method_sha256 = _optional_evidence(
        loader_method_evidence_path,
        kind="workchord-loader-method-evidence",
        target=target,
    )
    if get_settings().deployment_environment == "production":
        if capacity_sha256 is None or method_sha256 is None:
            raise MigrationDataError(
                "missing_production_loader_evidence",
                "Production loading requires capacity and loader comparison evidence",
            )

    table_results: dict[str, Any] = {}
    sequence_results: dict[str, Any] = {}
    try:
        with _exclusive_loader_connection(engine) as connection:
            try:
                with connection.begin():
                    _assert_postgresql_contract(connection)
                    gate = _initialize_gate(
                        connection,
                        manifest=manifest,
                        target_identity_sha256=target_sha256,
                    )
                    if gate.get("status") == "reconciled":
                        return write_document(
                            report_path,
                            {
                                "kind": "workchord-postgresql-load-report",
                                "schema_version": LOAD_REPORT_SCHEMA_VERSION,
                                "migration_run_id": run_id,
                                "source_manifest_sha256": manifest["document_sha256"],
                                "target_identity_sha256": target_sha256,
                                "status": "already_reconciled",
                                "tables": {},
                            },
                        )
                    completed = set(gate.get("completed_tables") or [])
                    connection.execute(
                        update(DatabaseMigrationGate)
                        .where(DatabaseMigrationGate.run_id == run_id)
                        .values(
                            status="loading",
                            failure_code=None,
                            updated_at=utc_now(),
                        )
                    )

                with read_only_sqlite(snapshot_path) as source:
                    for table_name in transfer_order():
                        table = transfer_tables()[table_name]
                        expected_count = int(
                            manifest["tables"][table_name]["row_count"]
                        )
                        if table_name in completed:
                            with connection.begin():
                                actual_count = _table_count(connection, table)
                            if actual_count != expected_count:
                                raise MigrationDataError(
                                    "resume_checkpoint_mismatch",
                                    f"Completed table {table_name} has {actual_count}, "
                                    f"expected {expected_count}",
                                )
                            table_results[table_name] = {
                                "row_count": actual_count,
                                "resumed": True,
                            }
                            continue
                        with connection.begin():
                            loaded = _load_table(
                                connection, source, table, chunk_size=chunk_size
                            )
                            if loaded != expected_count:
                                raise MigrationDataError(
                                    "loader_count_mismatch",
                                    f"Loaded {loaded} {table_name} rows; "
                                    f"expected {expected_count}",
                                )
                            completed.add(table_name)
                            connection.execute(
                                update(DatabaseMigrationGate)
                                .where(DatabaseMigrationGate.run_id == run_id)
                                .values(
                                    completed_tables=sorted(completed),
                                    updated_at=utc_now(),
                                )
                            )
                        table_results[table_name] = {
                            "row_count": loaded,
                            "resumed": False,
                        }
                        if _failure_after_table == table_name:
                            raise RuntimeError(
                                "injected table-boundary interruption"
                            )

                    staged_results: dict[str, int] = {}
                    for table_name in transfer_order():
                        table = transfer_tables()[table_name]
                        with connection.begin():
                            staged_results[table_name] = (
                                _restore_staged_references(
                                    connection,
                                    source,
                                    table,
                                    chunk_size=chunk_size,
                                )
                            )

                with connection.begin():
                    sequence_results = _repair_sequences(connection)
                for table_name in transfer_order():
                    with connection.begin():
                        connection.exec_driver_sql(f'ANALYZE "{table_name}"')
                with connection.begin():
                    connection.execute(
                        update(DatabaseMigrationGate)
                        .where(DatabaseMigrationGate.run_id == run_id)
                        .values(
                            status="loaded",
                            failure_code=None,
                            updated_at=utc_now(),
                        )
                    )

                if _file_sha256(snapshot_path) != manifest["snapshot"]["sha256"]:
                    raise MigrationDataError(
                        "source_changed_during_load",
                        "Read-only snapshot checksum changed during load",
                    )
                payload = {
                    "kind": "workchord-postgresql-load-report",
                    "schema_version": LOAD_REPORT_SCHEMA_VERSION,
                    "migration_run_id": run_id,
                    "source_manifest_sha256": manifest["document_sha256"],
                    "source_snapshot_sha256": manifest["snapshot"]["sha256"],
                    "target_identity_sha256": target_sha256,
                    "status": "loaded_closed_to_traffic",
                    "loader_method": "bounded-inserts-v1",
                    "chunk_size": chunk_size,
                    "capacity_evidence_sha256": capacity_sha256,
                    "loader_method_evidence_sha256": method_sha256,
                    "tables": table_results,
                    "staged_reference_updates": staged_results,
                    "sequences": sequence_results,
                    "analyze_completed": True,
                }
                return write_document(report_path, payload)
            except Exception as exc:
                code = (
                    exc.code
                    if isinstance(exc, MigrationDataError)
                    else "loader_exception"
                )
                _mark_load_failed(connection, run_id, code)
                if isinstance(exc, MigrationDataError):
                    raise
                raise MigrationDataError(
                    "loader_exception", f"Loader stopped with {type(exc).__name__}"
                ) from exc
    except MigrationDataError:
        raise
    except Exception as exc:
        raise MigrationDataError(
            "loader_exception", f"Loader stopped with {type(exc).__name__}"
        ) from exc
    finally:
        engine.dispose()


def _primary_key_sha256(table: Any, row: Mapping[str, Any]) -> str:
    values = [storage_value(column, row[column.name]) for column in table.primary_key.columns]
    normalized = [
        value.isoformat() if hasattr(value, "isoformat") else value for value in values
    ]
    return sha256_bytes(canonical_json_bytes(normalized))


def _row_hash_map(connection: Connection, table: Any) -> dict[str, str]:
    return {
        _primary_key_sha256(table, row): row_sha256(table, row)
        for row in _target_rows(connection, table)
    }


def _source_row_hash_map(source: Any, table: Any) -> dict[str, str]:
    return {
        _primary_key_sha256(table, row): row_sha256(table, row)
        for row in _rows(source, table)
    }


def _transformations(
    table_name: str,
    before: Mapping[str, str],
    after: Mapping[str, str],
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for primary_key_sha256 in sorted(set(before) | set(after)):
        before_sha256 = before.get(primary_key_sha256)
        after_sha256 = after.get(primary_key_sha256)
        if before_sha256 == after_sha256:
            continue
        if before_sha256 is None:
            operation = "insert"
        elif after_sha256 is None:
            operation = "delete"
        else:
            operation = "update"
        result.append(
            {
                "table": table_name,
                "primary_key_sha256": primary_key_sha256,
                "operation": operation,
                "before_sha256": before_sha256,
                "after_sha256": after_sha256,
            }
        )
    return result


def record_post_copy_repairs(
    *,
    source_manifest_path: Path,
    report_path: Path,
    authorized_target: str,
) -> dict[str, Any]:
    """Run the versioned repair catalog and record its exact row-hash delta."""

    try:
        manifest = read_document(source_manifest_path)
    except ManifestError as exc:
        raise MigrationDataError("invalid_source_manifest", str(exc)) from exc
    if manifest.get("kind") != "workchord-sqlite-source-manifest":
        raise MigrationDataError("invalid_source_manifest", "Source manifest kind is unsupported")
    run_id = str(manifest.get("migration_run_id", ""))
    engine, configuration = _target_engine()
    _authorize_target(configuration, authorized_target)
    target_sha256 = _target_identity_sha256(configuration)
    before_owned: dict[str, dict[str, str]] = {}
    before_other: dict[str, tuple[int, str]] = {}
    try:
        with engine.connect() as connection:
            _assert_postgresql_contract(connection)
            gate = _gate(connection, run_id)
            if gate is None or gate["status"] != "raw_reconciled":
                raise MigrationDataError(
                    "repair_gate_closed",
                    "Post-copy repairs require a successful raw reconciliation gate",
                )
            if gate["source_manifest_sha256"] != manifest["document_sha256"]:
                raise MigrationDataError(
                    "migration_gate_identity_mismatch", "Repair manifest differs from the gate"
                )
            for table_name, table in transfer_tables().items():
                if table_name in REPAIR_OWNED_TABLES:
                    before_owned[table_name] = _row_hash_map(connection, table)
                else:
                    before_other[table_name] = digest_rows(
                        table, _target_rows(connection, table)
                    )

        # Import lazily so the command process has already bound app.database
        # to the explicitly configured target URL.
        from app.services.upgrade_service import run_database_repairs

        run_database_repairs()

        transformations: list[dict[str, Any]] = []
        with engine.connect() as connection:
            for table_name, table in transfer_tables().items():
                if table_name in REPAIR_OWNED_TABLES:
                    after = _row_hash_map(connection, table)
                    changes = _transformations(
                        table_name, before_owned[table_name], after
                    )
                    if any(item["operation"] == "delete" for item in changes):
                        raise MigrationDataError(
                            "unexpected_repair_delete",
                            f"Repair catalog deleted rows from {table_name}",
                        )
                    transformations.extend(changes)
                else:
                    after_digest = digest_rows(table, _target_rows(connection, table))
                    if after_digest != before_other[table_name]:
                        raise MigrationDataError(
                            "repair_scope_escape",
                            f"Post-copy repair changed non-owned table {table_name}",
                        )
        transformations.sort(
            key=lambda item: (item["table"], item["primary_key_sha256"])
        )
        document = write_document(
            report_path,
            {
                "kind": "workchord-post-copy-repair-report",
                "schema_version": REPAIR_REPORT_SCHEMA_VERSION,
                "repair_catalog_version": "workchord-post-copy-repairs-v1",
                "migration_run_id": run_id,
                "source_manifest_sha256": manifest["document_sha256"],
                "target_identity_sha256": target_sha256,
                "allowed_tables": sorted(REPAIR_OWNED_TABLES),
                "transformations": transformations,
                "status": "repairs_recorded_target_still_closed",
            },
        )
        return document
    except Exception as exc:
        code = exc.code if isinstance(exc, MigrationDataError) else "repair_exception"
        _mark_failed(engine, run_id, code)
        if isinstance(exc, MigrationDataError):
            raise
        raise MigrationDataError(
            "repair_exception", f"Post-copy repair stopped with {type(exc).__name__}"
        ) from exc
    finally:
        engine.dispose()


def _repair_report(
    path: Path,
    *,
    manifest: Mapping[str, Any],
    target_identity_sha256: str,
) -> tuple[str, list[dict[str, Any]]]:
    try:
        report = read_document(path)
    except ManifestError as exc:
        raise MigrationDataError("invalid_repair_report", str(exc)) from exc
    if (
        report.get("kind") != "workchord-post-copy-repair-report"
        or report.get("schema_version") != REPAIR_REPORT_SCHEMA_VERSION
        or report.get("migration_run_id") != manifest.get("migration_run_id")
        or report.get("source_manifest_sha256") != manifest.get("document_sha256")
        or report.get("target_identity_sha256") != target_identity_sha256
        or report.get("allowed_tables") != sorted(REPAIR_OWNED_TABLES)
    ):
        raise MigrationDataError(
            "invalid_repair_report", "Repair report does not match this migration run"
        )
    transformations = report.get("transformations")
    if not isinstance(transformations, list) or not all(
        isinstance(item, dict) for item in transformations
    ):
        raise MigrationDataError(
            "invalid_repair_report", "Repair transformations must be an array of objects"
        )
    return str(report["document_sha256"]), transformations


def _sequence_facts(connection: Connection) -> dict[str, Any]:
    results: dict[str, Any] = {}
    preparer = connection.dialect.identifier_preparer
    for table_name in transfer_order():
        table = transfer_tables()[table_name]
        primary_key = list(table.primary_key.columns)
        if len(primary_key) != 1:
            continue
        column = primary_key[0]
        if not column.autoincrement or "int" not in type(column.type).__name__.lower():
            continue
        sequence = connection.execute(
            text("SELECT pg_get_serial_sequence(:table_name, :column_name)"),
            {"table_name": f"workchord.{table_name}", "column_name": column.name},
        ).scalar_one_or_none()
        if not sequence:
            continue
        parts = str(sequence).split(".", 1)
        if len(parts) != 2:
            raise MigrationDataError(
                "sequence_identity_failure", f"Unexpected sequence identity for {table_name}"
            )
        qualified = ".".join(preparer.quote_identifier(part.strip('"')) for part in parts)
        state = connection.execute(
            text(f"SELECT last_value, is_called FROM {qualified}")
        ).one()
        maximum = connection.execute(select(func.max(column))).scalar_one()
        next_value = int(state[0]) + (1 if state[1] else 0)
        safe = maximum is None or next_value > int(maximum)
        results[table_name] = {
            "column": column.name,
            "maximum": int(maximum) if maximum is not None else None,
            "next_value": next_value,
            "collision_safe": safe,
        }
        if not safe:
            raise MigrationDataError(
                "sequence_collision_risk", f"{table_name}.{column.name} sequence can collide"
            )
    return results


def _statistics_facts(connection: Connection) -> dict[str, Any]:
    rows = connection.execute(
        text(
            "SELECT relname, n_live_tup, last_analyze, last_autoanalyze "
            "FROM pg_stat_user_tables WHERE schemaname = 'workchord' "
            "ORDER BY relname"
        )
    ).mappings()
    results: dict[str, Any] = {}
    missing: list[str] = []
    for row in rows:
        table_name = str(row["relname"])
        if table_name in {"alembic_version", "database_migration_gates"}:
            continue
        analyzed = row["last_analyze"] is not None or row["last_autoanalyze"] is not None
        results[table_name] = {
            "estimated_live_rows": int(row["n_live_tup"]),
            "analyzed": analyzed,
        }
        if int(row["n_live_tup"]) > 0 and not analyzed:
            missing.append(table_name)
    if missing:
        raise MigrationDataError(
            "stale_planner_statistics", f"Planner statistics are missing for {missing}"
        )
    return results


def _representative_reads(source: Any, target: Connection) -> dict[str, Any]:
    queries = {
        "tasks_with_iteration": (
            "SELECT COUNT(*) FROM tasks t JOIN iterations i ON i.id = t.iteration_id"
        ),
        "assignments_with_actor": (
            "SELECT COUNT(*) FROM agent_task_assignments a "
            "JOIN agent_actors r ON r.id = a.actor_id"
        ),
        "runs_with_actor": (
            "SELECT COUNT(*) FROM agent_runs r JOIN agent_actors a ON a.id = r.actor_id"
        ),
        "session_identities": "SELECT COUNT(*) FROM user_sessions",
        "task_dependencies": "SELECT COUNT(*) FROM task_dependencies",
        "delivery_rows": "SELECT COUNT(*) FROM outbound_webhook_deliveries",
    }
    results: dict[str, Any] = {}
    for name, statement in queries.items():
        source_value = int(source.execute(statement).fetchone()[0])
        target_value = int(target.execute(text(statement)).scalar_one())
        if source_value != target_value:
            raise MigrationDataError(
                "representative_read_mismatch", f"Representative read {name} differs"
            )
        results[name] = target_value
    return results


def _decrypt_secret_settings(
    source: Any,
    target: Connection,
    *,
    encryption_key: str | None,
) -> int:
    source_values = [
        str(row[0])
        for row in source.execute(
            "SELECT secret_ciphertext FROM system_settings "
            "WHERE is_secret = 1 ORDER BY id"
        )
    ]
    target_values = [
        str(value)
        for value in target.execute(
            text(
                "SELECT secret_ciphertext FROM system_settings "
                "WHERE is_secret = true ORDER BY id"
            )
        ).scalars()
    ]
    if source_values != target_values:
        raise MigrationDataError(
            "encrypted_setting_mismatch", "Encrypted system setting bytes differ"
        )
    if not source_values:
        return 0
    if not encryption_key:
        raise MigrationDataError(
            "missing_settings_encryption_key",
            "SETTINGS_ENCRYPTION_KEY is required to validate encrypted settings",
        )
    try:
        fernet = Fernet(encryption_key.encode("ascii"))
        for ciphertext in target_values:
            fernet.decrypt(ciphertext.encode("ascii"))
    except (ValueError, InvalidToken, UnicodeError) as exc:
        raise MigrationDataError(
            "encrypted_setting_decrypt_failure",
            "An encrypted system setting cannot be decrypted with the approved key",
        ) from exc
    return len(source_values)


def _raw_table_results(source: Any, target: Connection) -> dict[str, Any]:
    results: dict[str, Any] = {}
    for table_name in transfer_order():
        table = transfer_tables()[table_name]
        source_result = digest_rows(table, _rows(source, table))
        target_result = digest_rows(table, _target_rows(target, table))
        passed = source_result == target_result
        results[table_name] = {
            "source_row_count": source_result[0],
            "target_row_count": target_result[0],
            "source_canonical_sha256": source_result[1],
            "target_canonical_sha256": target_result[1],
            "passed": passed,
        }
        if not passed:
            source_rows = {
                _primary_key_sha256(table, row): row for row in _rows(source, table)
            }
            target_rows = {
                _primary_key_sha256(table, row): row
                for row in _target_rows(target, table)
            }
            differing_columns: set[str] = set()
            for key in set(source_rows) & set(target_rows):
                for column in table.columns:
                    if canonical_value(column, source_rows[key][column.name]) != canonical_value(
                        column, target_rows[key][column.name]
                    ):
                        differing_columns.add(column.name)
            raise MigrationDataError(
                "table_reconciliation_mismatch",
                f"Raw reconciliation differs for {table_name}; "
                f"columns={sorted(differing_columns)}, "
                f"missing_rows={len(set(source_rows) - set(target_rows))}, "
                f"unexpected_rows={len(set(target_rows) - set(source_rows))}",
            )
    return results


def _final_table_results(
    source: Any,
    target: Connection,
    transformations: list[dict[str, Any]],
) -> dict[str, Any]:
    expected_by_table: dict[str, list[dict[str, Any]]] = {}
    for transformation in transformations:
        table_name = transformation.get("table")
        if table_name not in REPAIR_OWNED_TABLES:
            raise MigrationDataError(
                "invalid_repair_report", f"Transformation table {table_name!r} is not repair-owned"
            )
        expected_by_table.setdefault(str(table_name), []).append(transformation)

    results: dict[str, Any] = {}
    for table_name in transfer_order():
        table = transfer_tables()[table_name]
        if table_name not in REPAIR_OWNED_TABLES:
            source_result = digest_rows(table, _rows(source, table))
            target_result = digest_rows(table, _target_rows(target, table))
            if source_result != target_result:
                raise MigrationDataError(
                    "unexplained_post_repair_difference",
                    f"Final reconciliation differs for non-repair table {table_name}",
                )
            results[table_name] = {
                "source_row_count": source_result[0],
                "target_row_count": target_result[0],
                "expected_transformations": 0,
                "passed": True,
            }
            continue
        source_map = _source_row_hash_map(source, table)
        target_map = _row_hash_map(target, table)
        actual = _transformations(table_name, source_map, target_map)
        expected = sorted(
            expected_by_table.get(table_name, []),
            key=lambda item: item.get("primary_key_sha256", ""),
        )
        if actual != expected:
            raise MigrationDataError(
                "unexplained_post_repair_difference",
                f"Final repair delta differs for {table_name}",
            )
        results[table_name] = {
            "source_row_count": len(source_map),
            "target_row_count": len(target_map),
            "expected_transformations": len(expected),
            "passed": True,
        }
    return results


def reconcile_snapshot(
    *,
    snapshot_path: Path,
    source_manifest_path: Path,
    report_path: Path,
    authorized_target: str,
    phase: str,
    raw_report_path: Path | None = None,
    repair_report_path: Path | None = None,
    encryption_key: str | None = None,
) -> dict[str, Any]:
    """Reconcile raw or post-repair target state and advance readiness safely."""

    if phase not in {"raw", "final"}:
        raise MigrationDataError("invalid_reconciliation_phase", "Phase must be raw or final")
    manifest = _load_source_manifest(source_manifest_path, snapshot_path)
    run_id = str(manifest["migration_run_id"])
    engine, configuration = _target_engine()
    _authorize_target(configuration, authorized_target)
    target_sha256 = _target_identity_sha256(configuration)
    transformations: list[dict[str, Any]] = []
    repair_sha256: str | None = None
    if phase == "final":
        if raw_report_path is None or repair_report_path is None:
            raise MigrationDataError(
                "missing_final_reconciliation_evidence",
                "Final reconciliation requires raw and repair reports",
            )
        try:
            raw_report = read_document(raw_report_path)
        except ManifestError as exc:
            raise MigrationDataError("invalid_raw_report", str(exc)) from exc
        if (
            raw_report.get("kind") != "workchord-reconciliation-report"
            or raw_report.get("phase") != "raw"
            or raw_report.get("status") != "passed_target_still_closed"
            or raw_report.get("migration_run_id") != run_id
            or raw_report.get("source_manifest_sha256") != manifest["document_sha256"]
        ):
            raise MigrationDataError(
                "invalid_raw_report", "Raw reconciliation report does not match this run"
            )
        repair_sha256, transformations = _repair_report(
            repair_report_path,
            manifest=manifest,
            target_identity_sha256=target_sha256,
        )

    try:
        with engine.begin() as connection:
            _assert_postgresql_contract(connection)
            gate = _gate(connection, run_id)
            allowed_statuses = (
                {"loaded", "failed", "reconciling"}
                if phase == "raw"
                else {"raw_reconciled", "failed", "reconciling"}
            )
            if gate is None or gate["status"] not in allowed_statuses:
                raise MigrationDataError(
                    "reconciliation_gate_closed",
                    f"{phase} reconciliation is not allowed from the current gate state",
                )
            if (
                gate["source_manifest_sha256"] != manifest["document_sha256"]
                or gate["target_identity_sha256"] != target_sha256
            ):
                raise MigrationDataError(
                    "migration_gate_identity_mismatch", "Reconciliation identities differ"
                )
            if (
                phase == "final"
                and gate["raw_report_sha256"] != raw_report["document_sha256"]
            ):
                raise MigrationDataError(
                    "raw_report_gate_mismatch",
                    "Final reconciliation raw report differs from the report sealed in the gate",
                )
            connection.execute(
                update(DatabaseMigrationGate)
                .where(DatabaseMigrationGate.run_id == run_id)
                .values(status="reconciling", failure_code=None, updated_at=utc_now())
            )

        with read_only_sqlite(snapshot_path) as source, engine.connect() as target:
            table_results = (
                _raw_table_results(source, target)
                if phase == "raw"
                else _final_table_results(source, target, transformations)
            )
            representative_reads = _representative_reads(source, target)
            encrypted_settings = _decrypt_secret_settings(
                source,
                target,
                encryption_key=encryption_key or os.environ.get("SETTINGS_ENCRYPTION_KEY"),
            )
            sequences = _sequence_facts(target)
            statistics = _statistics_facts(target)

        payload = {
            "kind": "workchord-reconciliation-report",
            "schema_version": RECONCILIATION_REPORT_SCHEMA_VERSION,
            "phase": phase,
            "migration_run_id": run_id,
            "source_manifest_sha256": manifest["document_sha256"],
            "source_snapshot_sha256": manifest["snapshot"]["sha256"],
            "target_identity_sha256": target_sha256,
            "target_revision": head_revision(),
            "repair_report_sha256": repair_sha256,
            "tables": table_results,
            "sequences": sequences,
            "planner_statistics": statistics,
            "representative_reads": representative_reads,
            "encrypted_settings_decrypted": encrypted_settings,
            "zero_unexplained_differences": True,
            "status": (
                "passed_target_still_closed" if phase == "raw" else "passed_target_ready"
            ),
        }
        document = write_document(report_path, payload)
        with engine.begin() as connection:
            values: dict[str, Any] = {
                "status": "raw_reconciled" if phase == "raw" else "reconciled",
                "failure_code": None,
                "updated_at": utc_now(),
            }
            if phase == "raw":
                values["raw_report_sha256"] = document["document_sha256"]
            else:
                values["reconciliation_report_sha256"] = document["document_sha256"]
            connection.execute(
                update(DatabaseMigrationGate)
                .where(DatabaseMigrationGate.run_id == run_id)
                .values(**values)
            )
        return document
    except Exception as exc:
        code = exc.code if isinstance(exc, MigrationDataError) else "reconciliation_exception"
        _mark_failed(engine, run_id, code)
        if isinstance(exc, MigrationDataError):
            raise
        raise MigrationDataError(
            "reconciliation_exception",
            f"Reconciliation stopped with {type(exc).__name__}",
        ) from exc
    finally:
        engine.dispose()
