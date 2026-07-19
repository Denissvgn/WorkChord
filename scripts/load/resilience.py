#!/usr/bin/env python3
"""Derive fail-closed resilience metrics from sealed fault observations."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import sys
from typing import Any, Mapping

from jsonschema import Draft202012Validator, FormatChecker

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.load.common import (
    QualificationInputError,
    REPOSITORY_ROOT,
    atomic_write_json,
    capacity_contract,
    read_json_object,
    utc_now_text,
)
from scripts.load.result import percentile


SCHEMA_PATH = (
    REPOSITORY_ROOT
    / "docs/contracts/postgresql-resilience-observations-v1.schema.json"
)


def _time(value: str) -> datetime:
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise QualificationInputError("Fault timestamps must be timezone-aware")
    return parsed


def _elapsed(start: str, end: str, name: str) -> float:
    seconds = (_time(end) - _time(start)).total_seconds()
    if seconds < 0:
        raise QualificationInputError(f"Fault timestamp order is invalid for {name}")
    return seconds


def _gate(actual: float, maximum: float) -> dict[str, Any]:
    return {
        "status": "passed" if actual <= maximum else "failed",
        "actual": actual,
        "required": {"maximum": maximum},
    }


def evaluate(document: Mapping[str, Any]) -> dict[str, Any]:
    schema = read_json_object(SCHEMA_PATH)
    errors = sorted(
        Draft202012Validator(
            schema, format_checker=FormatChecker()
        ).iter_errors(document),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        rendered = "; ".join(
            f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
            for error in errors[:10]
        )
        raise QualificationInputError(
            f"Resilience observation schema validation failed: {rendered}"
        )

    scenarios = document["scenarios"]
    backend = scenarios["backend_replica_loss"]
    worker = scenarios["worker_loss"]
    database = scenarios["database_failover"]
    pool = scenarios["pool_saturation"]
    slow = scenarios["slow_query"]
    restore = scenarios["restore"]

    ranked = set(slow["ranked_query_ids"])
    explained = set(slow["explained_query_ids"])
    if not explained.issubset(ranked):
        raise QualificationInputError(
            "Every EXPLAIN query id must appear in the pg_stat_statements ranking"
        )
    if backend["unexpected_failures"] > backend["eligible_attempts"]:
        raise QualificationInputError("Backend failure count exceeds attempts")
    if database["unexpected_failures"] > database["eligible_attempts"]:
        raise QualificationInputError("Database failure count exceeds attempts")

    metrics = {
        "backend_replica_reroute_seconds": _elapsed(
            backend["fault_at"], backend["first_success_at"], "backend reroute"
        ),
        "backend_replica_unexpected_attempt_failures_percent": (
            float(backend["unexpected_failures"])
            / int(backend["eligible_attempts"])
            * 100
        ),
        "delivery_oldest_ready_burst_seconds": float(
            worker["oldest_ready_seconds_max"]
        ),
        "delivery_ready_backlog_maximum": float(worker["ready_backlog_max"]),
        "delivery_drain_to_steady_seconds": _elapsed(
            worker["replacement_ready_at"],
            worker["queue_drained_at"],
            "worker queue drain",
        ),
        "database_unready_detection_seconds": _elapsed(
            database["fault_at"], database["unready_at"], "database detection"
        ),
        "database_failover_seconds": _elapsed(
            database["fault_at"], database["writer_ready_at"], "database failover"
        ),
        "database_failover_unexpected_attempt_failures_percent": (
            float(database["unexpected_failures"])
            / int(database["eligible_attempts"])
            * 100
        ),
        "pool_checkout_p95_ms": percentile(pool["checkout_samples_ms"], 0.95),
        "pool_checkout_p99_ms": percentile(pool["checkout_samples_ms"], 0.99),
        "pool_timeouts": float(pool["timeouts"]),
        "steady_database_connections_percent": (
            int(pool["database_connections_peak"])
            / int(pool["database_max_connections"])
            * 100
        ),
        "ordinary_lock_wait_p99_ms": percentile(
            slow["ordinary_lock_wait_samples_ms"], 0.99
        ),
        "deadlocks": float(slow["deadlocks"]),
        "backup_rpo_seconds": _elapsed(
            restore["restored_latest_event_at"],
            restore["failure_at"],
            "restored recovery point",
        ),
        "restore_rto_seconds": _elapsed(
            restore["restore_started_at"],
            restore["restore_ready_at"],
            "restore recovery time",
        ),
    }
    slos = capacity_contract()["slos"]
    limits = {
        "backend_replica_reroute_seconds": slos[
            "backend_replica_reroute_seconds_maximum"
        ],
        "backend_replica_unexpected_attempt_failures_percent": slos[
            "total_unexpected_error_percent_maximum"
        ],
        "delivery_oldest_ready_burst_seconds": slos[
            "delivery_oldest_ready_seconds"
        ]["burst_maximum"],
        "delivery_ready_backlog_maximum": slos["delivery_ready_backlog_maximum"],
        "delivery_drain_to_steady_seconds": slos[
            "delivery_drain_to_steady_seconds_maximum"
        ],
        "database_unready_detection_seconds": slos[
            "database_unready_detection_seconds_maximum"
        ],
        "database_failover_seconds": slos["database_failover_seconds_maximum"],
        "database_failover_unexpected_attempt_failures_percent": slos[
            "database_failover_unexpected_attempt_failures_percent_maximum"
        ],
        "pool_checkout_p95_ms": slos["pool_checkout_ms"]["p95"],
        "pool_checkout_p99_ms": slos["pool_checkout_ms"]["p99"],
        "pool_timeouts": slos["pool_checkout_ms"]["timeouts"],
        "steady_database_connections_percent": slos[
            "steady_database_connections_percent_maximum"
        ],
        "ordinary_lock_wait_p99_ms": slos["ordinary_lock_wait_ms"]["p99"],
        "deadlocks": slos["ordinary_lock_wait_ms"]["deadlocks"],
        "backup_rpo_seconds": slos["backup_rpo_seconds_maximum"],
        "restore_rto_seconds": slos["restore_rto_seconds_maximum"],
    }
    gates = {name: _gate(float(value), float(limits[name])) for name, value in metrics.items()}
    gates["restore_integrity"] = _gate(
        float(restore["integrity_failures"]),
        float(slos["integrity_failures"]),
    )
    status = (
        "passed"
        if all(item["status"] == "passed" for item in gates.values())
        else "failed"
    )
    return {
        "kind": "workchord-postgresql-resilience-result",
        "schema_version": 1,
        "created_at": utc_now_text(),
        "status": status,
        "release_fingerprint": document["release_fingerprint"],
        "observations_sha256": document["document_sha256"],
        "metrics": metrics,
        "gates": gates,
        "evidence": {
            "ranked_query_ids": sorted(ranked),
            "explained_query_ids": sorted(explained),
            "backup_artifact_sha256": restore["backup_artifact_sha256"],
            "restore_report_sha256": restore["restore_report_sha256"],
        },
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Evaluate sealed PostgreSQL fault and recovery observations."
    )
    parser.add_argument("--observations", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        observations = read_json_object(args.observations, sealed=True)
        result = atomic_write_json(args.output, evaluate(observations))
        print(
            f"Resilience status={result['status']} "
            f"sha256={result['document_sha256']}"
        )
        return 0 if result["status"] == "passed" else 2
    except (QualificationInputError, OSError) as exc:
        print(f"Resilience evaluation refused: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
