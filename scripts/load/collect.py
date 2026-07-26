#!/usr/bin/env python3
"""Collect sealed PostgreSQL evidence and derive qualification metrics."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta
from decimal import Decimal
import os
from pathlib import Path
import sys
from typing import Any, Iterable, Mapping
from uuid import uuid4

import psycopg
from psycopg.rows import dict_row
from sqlalchemy.engine import make_url

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.load.common import (
    DATA_LIFECYCLE_POLICY_MEMBER,
    QualificationInputError,
    atomic_write_json,
    capacity_contract,
    contract_member_sha256,
    contract_sha256,
    read_json_object,
    utc_now_text,
    verify_document,
)


MINIMUM_HORIZON_SAMPLE_SECONDS = 8 * 60 * 60
DERIVATION_PHASES = (
    "small",
    "warmup",
    "steady",
    "burst",
    "soak",
    "external_wait",
)


INTEGRITY_QUERIES: tuple[tuple[str, str], ...] = (
    (
        "task_dependency_orphans",
        """
        SELECT count(*)::bigint
        FROM task_dependencies dependency
        LEFT JOIN tasks task ON task.id = dependency.task_id
        LEFT JOIN tasks required ON required.id = dependency.depends_on_id
        WHERE task.id IS NULL OR required.id IS NULL
        """,
    ),
    (
        "duplicate_live_task_assignments",
        """
        SELECT count(*)::bigint FROM (
          SELECT task_id
          FROM agent_task_assignments
          WHERE state IN ('queued', 'accepted')
          GROUP BY task_id HAVING count(*) > 1
        ) duplicates
        """,
    ),
    (
        "duplicate_running_assignment_runs",
        """
        SELECT count(*)::bigint FROM (
          SELECT assignment_id
          FROM agent_runs
          WHERE assignment_id IS NOT NULL AND status = 'running'
          GROUP BY assignment_id HAVING count(*) > 1
        ) duplicates
        """,
    ),
    (
        "task_event_orphans",
        """
        SELECT count(*)::bigint
        FROM task_events event
        LEFT JOIN tasks task ON task.id = event.task_id
        WHERE task.id IS NULL
        """,
    ),
    (
        "agent_run_event_orphans",
        """
        SELECT count(*)::bigint
        FROM agent_run_events event
        LEFT JOIN agent_runs run ON run.id = event.run_id
        WHERE run.id IS NULL
        """,
    ),
    (
        "outbound_delivery_event_orphans",
        """
        SELECT count(*)::bigint
        FROM outbound_webhook_deliveries delivery
        LEFT JOIN outbound_webhook_events event ON event.id = delivery.event_id
        WHERE event.id IS NULL
        """,
    ),
)


EXPLAIN_QUERIES: tuple[tuple[str, str], ...] = (
    (
        "hot_iteration_tasks",
        """
        SELECT id, parent_id, assignee_id, status, priority, sort_order
        FROM tasks
        WHERE iteration_id = %s
        ORDER BY parent_id NULLS FIRST, sort_order, id
        LIMIT 2500
        """,
    ),
    (
        "hot_iteration_dependencies",
        """
        SELECT dependency.id, dependency.task_id, dependency.depends_on_id
        FROM task_dependencies dependency
        JOIN tasks task ON task.id = dependency.task_id
        WHERE task.iteration_id = %s
        ORDER BY dependency.task_id, dependency.depends_on_id, dependency.id
        LIMIT 10000
        """,
    ),
    (
        "ready_delivery_claim",
        """
        SELECT id
        FROM outbound_webhook_deliveries
        WHERE status = 'pending'
          AND attempt_count < max_attempts
          AND (next_retry_at IS NULL OR next_retry_at <= clock_timestamp())
        ORDER BY next_retry_at NULLS FIRST, created_at NULLS LAST, id
        LIMIT 50
        """,
    ),
)


def _authorized_database_url(args: argparse.Namespace) -> tuple[str, dict[str, Any]]:
    url = make_url(args.database_url)
    if url.get_backend_name() != "postgresql" or url.drivername not in {
        "postgresql",
        "postgresql+psycopg",
    }:
        raise QualificationInputError(
            "Metrics collection requires a PostgreSQL Psycopg URL"
        )
    resolved_host = url.host or ""
    if url.port:
        resolved_host = f"{resolved_host}:{url.port}"
    if resolved_host != args.authorize_host:
        raise QualificationInputError(
            f"Resolved database host {resolved_host!r} differs from --authorize-host"
        )
    if args.environment == "production":
        expected = os.getenv("WORKCHORD_PRODUCTION_LOAD_AUTHORIZATION")
        if (
            not expected
            or args.production_authorization != expected
            or not args.change_id
            or len(args.change_id.strip()) < 3
        ):
            raise QualificationInputError(
                "Production collection requires exact authorization and a change ID"
            )
    elif args.production_authorization is not None:
        raise QualificationInputError(
            "Production authorization must not be supplied outside production"
        )
    if not url.database:
        raise QualificationInputError("Database URL must name a database")
    rendered = url.set(drivername="postgresql").render_as_string(
        hide_password=False
    )
    return rendered, {
        "host": resolved_host,
        "database": url.database,
        "environment": args.environment,
        "change_id": args.change_id,
    }


def _one(cursor: psycopg.Cursor[Any], query: str, params: Iterable[Any] = ()) -> dict[str, Any]:
    cursor.execute(query, tuple(params))
    row = cursor.fetchone()
    if not isinstance(row, dict):
        raise QualificationInputError("PostgreSQL evidence query returned no row")
    return dict(row)


def _int(value: Any) -> int:
    return int(value or 0)


def _float(value: Any) -> float:
    return float(value or 0)


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, Decimal):
        return float(value)
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return value


def _snapshot(args: argparse.Namespace) -> int:
    database_url, target = _authorized_database_url(args)
    contract = capacity_contract()
    with psycopg.connect(
        database_url,
        row_factory=dict_row,
        options="-c statement_timeout=30000 -c lock_timeout=5000",
    ) as connection:
        connection.read_only = True
        with connection.cursor() as cursor:
            facts = _one(
                cursor,
                """
                SELECT current_database() AS database_name,
                       current_setting('server_version') AS server_version,
                       current_setting('server_version_num')::integer AS server_version_num,
                       current_setting('server_encoding') AS encoding,
                       current_setting('TimeZone') AS timezone,
                       current_setting('search_path') AS search_path,
                       current_setting('max_connections')::integer AS max_connections,
                       current_setting('shared_preload_libraries') AS shared_preload_libraries,
                       current_setting('track_io_timing') AS track_io_timing,
                       current_setting('track_wal_io_timing') AS track_wal_io_timing,
                       pg_database_size(current_database())::bigint AS database_size_bytes,
                       clock_timestamp() AS database_clock
                """,
            )
            database = _one(
                cursor,
                """
                SELECT numbackends, xact_commit, xact_rollback, blks_read,
                       blks_hit, temp_files, temp_bytes, deadlocks,
                       checksum_failures, stats_reset
                FROM pg_stat_database WHERE datname = current_database()
                """,
            )
            wal = _one(
                cursor,
                """
                SELECT wal_records, wal_fpi, wal_bytes, wal_buffers_full,
                       stats_reset
                FROM pg_stat_wal
                """,
            )
            extension = _one(
                cursor,
                """
                SELECT EXISTS (
                    SELECT 1 FROM pg_extension WHERE extname = 'pg_stat_statements'
                ) AS installed
                """,
            )
            cursor.execute(
                """
                SELECT schemaname, relname,
                       n_live_tup::bigint, n_dead_tup::bigint,
                       seq_scan::bigint, idx_scan::bigint,
                       last_vacuum, last_autovacuum, last_analyze, last_autoanalyze,
                       pg_relation_size(relid)::bigint AS table_bytes,
                       pg_indexes_size(relid)::bigint AS index_bytes,
                       pg_total_relation_size(relid)::bigint AS total_bytes
                FROM pg_stat_user_tables
                ORDER BY pg_total_relation_size(relid) DESC, schemaname, relname
                """
            )
            tables = [dict(row) for row in cursor.fetchall()]

            statements: list[dict[str, Any]] = []
            if extension["installed"]:
                cursor.execute(
                    """
                    SELECT queryid::text, calls::bigint, rows::bigint,
                           round(total_exec_time::numeric, 3) AS total_exec_time_ms,
                           round(mean_exec_time::numeric, 3) AS mean_exec_time_ms,
                           shared_blks_read::bigint, shared_blks_hit::bigint,
                           temp_blks_written::bigint, wal_bytes::bigint
                    FROM public.pg_stat_statements
                    WHERE dbid = (SELECT oid FROM pg_database WHERE datname = current_database())
                    ORDER BY total_exec_time DESC, queryid
                    LIMIT 100
                    """
                )
                statements = [dict(row) for row in cursor.fetchall()]

            checks: list[dict[str, Any]] = []
            for name, query in INTEGRITY_QUERIES:
                count = _int(_one(cursor, query).get("count"))
                checks.append(
                    {
                        "name": name,
                        "failures": count,
                        "passed": count == 0,
                    }
                )

            explains: list[dict[str, Any]] = []
            if args.include_explain:
                cursor.execute(
                    """
                    SELECT iteration_id, count(*)::bigint AS task_count
                    FROM tasks WHERE iteration_id IS NOT NULL
                    GROUP BY iteration_id ORDER BY count(*) DESC, iteration_id LIMIT 1
                    """,
                )
                hot_iteration = cursor.fetchone() or {}
                hot_iteration_id = hot_iteration.get("iteration_id")
                if hot_iteration_id is not None:
                    for name, query in EXPLAIN_QUERIES:
                        params = (
                            (hot_iteration_id,)
                            if "%s" in query
                            else ()
                        )
                        cursor.execute(
                            "EXPLAIN (ANALYZE, BUFFERS, WAL, SETTINGS, FORMAT JSON) "
                            + query,
                            params,
                        )
                        row = cursor.fetchone()
                        plan = next(iter(row.values())) if isinstance(row, dict) else None
                        explains.append({"name": name, "plan": plan})

    facts = _json_safe(facts)
    database = _json_safe(database)
    wal = _json_safe(wal)
    tables = _json_safe(tables)
    statements = _json_safe(statements)
    explains = _json_safe(explains)

    document = atomic_write_json(
        args.output,
        {
            "kind": "workchord-postgresql-metrics-snapshot",
            "schema_version": 1,
            "snapshot_id": args.snapshot_id,
            "label": args.label,
            "created_at": utc_now_text(),
            "target": target,
            "capacity_contract": {
                "id": contract["contract_id"],
                "sha256": contract_sha256(),
            },
            "lifecycle_policy_sha256": contract_member_sha256(
                DATA_LIFECYCLE_POLICY_MEMBER
            ),
            "facts": facts,
            "database": database,
            "wal": wal,
            "pg_stat_statements": {
                "installed": bool(extension["installed"]),
                "preloaded": "pg_stat_statements"
                in str(facts["shared_preload_libraries"]).split(","),
                "ranked_without_query_text": statements,
            },
            "tables": tables,
            "integrity": {
                "failures": sum(item["failures"] for item in checks),
                "checks": checks,
            },
            "explain_analyze": explains,
        },
    )
    print(
        f"PostgreSQL snapshot {document['snapshot_id']} "
        f"sha256={document['document_sha256']}"
    )
    return 0


def _timestamp(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise QualificationInputError("Evidence timestamps must be timezone-aware")
    return parsed


def _table_map(snapshot: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {
        f"{row['schemaname']}.{row['relname']}": row
        for row in snapshot.get("tables", [])
    }


def _evidence_metrics(paths: list[Path]) -> tuple[dict[str, float], list[dict[str, str]]]:
    merged: dict[str, float] = {}
    sources: list[dict[str, str]] = []
    for path in paths:
        document = read_json_object(path, sealed=True)
        values = document.get("metrics", document)
        if not isinstance(values, dict):
            raise QualificationInputError(f"Evidence metrics are not an object: {path}")
        for key, value in values.items():
            if key in {"schema_version", "document_sha256"}:
                continue
            if not isinstance(value, (int, float)):
                continue
            if key in merged and float(value) != merged[key]:
                raise QualificationInputError(
                    f"Conflicting external metric {key!r} across evidence inputs"
                )
            merged[key] = float(value)
        sources.append(
            {"path": str(path), "sha256": str(document["document_sha256"])}
        )
    return merged, sources


def _derive(args: argparse.Namespace) -> int:
    before = read_json_object(args.before, sealed=True)
    after = read_json_object(args.after, sealed=True)
    load_result = read_json_object(args.load_result, sealed=True)
    for document in (before, after):
        if document.get("kind") != "workchord-postgresql-metrics-snapshot":
            raise QualificationInputError("Derivation inputs must be PostgreSQL snapshots")
    if load_result.get("kind") != "workchord-postgresql-load-result":
        raise QualificationInputError("Derivation load input is not a load result")
    load_traffic = load_result.get("traffic")
    if not isinstance(load_traffic, dict) or load_traffic.get("phase") != args.phase:
        raise QualificationInputError("Load result phase differs from metric derivation")
    if before["target"] != after["target"]:
        raise QualificationInputError("Before/after snapshots target different databases")
    if before["capacity_contract"] != after["capacity_contract"]:
        raise QualificationInputError("Before/after capacity contracts differ")
    elapsed = (
        _timestamp(str(after["created_at"]))
        - _timestamp(str(before["created_at"]))
    ).total_seconds()
    if elapsed <= 0:
        raise QualificationInputError("After snapshot must be newer than before snapshot")
    load_completed = _timestamp(str(load_result["created_at"]))
    load_started = load_completed - timedelta(
        seconds=float(load_traffic["actual_duration_seconds"])
    )
    if _timestamp(str(before["created_at"])) > load_started:
        raise QualificationInputError(
            "Before snapshot was not captured before the measured load interval"
        )
    if _timestamp(str(after["created_at"])) < load_completed:
        raise QualificationInputError(
            "After snapshot was not captured after the measured load interval"
        )

    load_reference = {
        "run_id": str(load_result["run_id"]),
        "sha256": str(load_result["document_sha256"]),
        "created_at": str(load_result["created_at"]),
    }

    metrics, sources = _evidence_metrics(args.evidence)
    database_size_before = _int(before["facts"]["database_size_bytes"])
    database_size_after = _int(after["facts"]["database_size_bytes"])
    database_growth = database_size_after - database_size_before
    wal_growth = _int(after["wal"]["wal_bytes"]) - _int(before["wal"]["wal_bytes"])
    deadlocks = _int(after["database"]["deadlocks"]) - _int(
        before["database"]["deadlocks"]
    )
    if deadlocks < 0:
        raise QualificationInputError("PostgreSQL statistics reset during measurement")
    metrics.setdefault("deadlocks", float(deadlocks))

    reference_bytes = (
        int(capacity_contract()["reference_hardware"]["postgresql_primary"]["storage_gib"])
        * 1024**3
    )
    storage_percent = database_size_after / reference_bytes * 100
    phase_storage_key = {
        "small": "storage_used_steady_percent",
        "warmup": "storage_used_steady_percent",
        "steady": "storage_used_steady_percent",
        "burst": "storage_used_burst_percent",
        "soak": "storage_used_steady_percent",
        "external_wait": "storage_used_steady_percent",
    }[args.phase]
    metrics.setdefault(phase_storage_key, storage_percent)

    after_tables = _table_map(after)
    before_tables = _table_map(before)
    positive_table_growth = sum(
        max(
            0,
            _int(row["total_bytes"])
            - _int(before_tables.get(name, {}).get("total_bytes")),
        )
        for name, row in after_tables.items()
    )
    effective_growth = max(database_growth, positive_table_growth)
    horizon_months: float | None = None
    if elapsed >= MINIMUM_HORIZON_SAMPLE_SECONDS and effective_growth > 0:
        bytes_per_second = effective_growth / elapsed
        bytes_until_threshold = max(
            0.0,
            (reference_bytes * 0.70) - database_size_after,
        )
        horizon_months = bytes_until_threshold / bytes_per_second / (30 * 24 * 3600)
        metrics.setdefault("capacity_horizon_months", horizon_months)

    bloat_values = [
        _int(row["n_dead_tup"])
        / max(1, _int(row["n_live_tup"]) + _int(row["n_dead_tup"]))
        * 100
        for row in after.get("tables", [])
    ]
    metrics.setdefault(
        "dead_tuple_or_bloat_percent_maximum",
        max(bloat_values, default=0.0),
    )
    created_after = _timestamp(str(after["created_at"]))
    analyze_lags = []
    for row in after.get("tables", []):
        timestamps = [
            _timestamp(str(row[key]))
            for key in ("last_analyze", "last_autoanalyze")
            if row.get(key)
        ]
        if timestamps:
            analyze_lags.append(
                max(0.0, (created_after - max(timestamps)).total_seconds())
            )
    if len(analyze_lags) == len(after.get("tables", [])):
        metrics.setdefault(
            "statistics_refresh_after_bulk_load_seconds",
            max(analyze_lags, default=0.0),
        )

    integrity_checks = list(after["integrity"]["checks"])
    integrity = atomic_write_json(
        args.integrity_output,
        {
            "kind": "workchord-domain-integrity-evidence",
            "schema_version": 1,
            "created_at": utc_now_text(),
            "load_result": load_reference,
            "snapshot_sha256": after["document_sha256"],
            "failures": _int(after["integrity"]["failures"]),
            "checks": integrity_checks,
        },
    )
    result = atomic_write_json(
        args.external_output,
        {
            "kind": "workchord-external-qualification-metrics",
            "schema_version": 1,
            "created_at": utc_now_text(),
            "phase": args.phase,
            "load_result": load_reference,
            "sample_seconds": elapsed,
            "snapshot_sources": {
                "before": before["document_sha256"],
                "after": after["document_sha256"],
                "additional": sources,
            },
            "database_growth_bytes": database_growth,
            "positive_table_growth_bytes": positive_table_growth,
            "wal_growth_bytes": wal_growth,
            "projected_capacity_horizon_months": horizon_months,
            "metrics": metrics,
        },
    )
    print(
        f"Derived metrics sha256={result['document_sha256']} "
        f"integrity_sha256={integrity['document_sha256']}"
    )
    return 0


def _add_target_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--database-url", required=True)
    parser.add_argument("--authorize-host", required=True)
    parser.add_argument(
        "--environment",
        choices=("test", "rehearsal", "production"),
        required=True,
    )
    parser.add_argument("--production-authorization")
    parser.add_argument("--change-id")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Collect fail-closed PostgreSQL qualification evidence."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    snapshot = subparsers.add_parser("snapshot")
    _add_target_arguments(snapshot)
    snapshot.add_argument("--label", required=True)
    snapshot.add_argument("--snapshot-id", default=f"pg-{uuid4().hex}")
    snapshot.add_argument("--include-explain", action="store_true")
    snapshot.add_argument("--output", type=Path, required=True)
    snapshot.set_defaults(handler=_snapshot)

    derive = subparsers.add_parser("derive")
    derive.add_argument("--before", type=Path, required=True)
    derive.add_argument("--after", type=Path, required=True)
    derive.add_argument("--load-result", type=Path, required=True)
    derive.add_argument("--phase", choices=DERIVATION_PHASES, required=True)
    derive.add_argument("--evidence", type=Path, action="append", default=[])
    derive.add_argument("--external-output", type=Path, required=True)
    derive.add_argument("--integrity-output", type=Path, required=True)
    derive.set_defaults(handler=_derive)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        return int(args.handler(args))
    except (QualificationInputError, psycopg.Error, OSError) as exc:
        print(f"Evidence collection refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
