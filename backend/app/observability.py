"""Database-backed readiness, drain state, and low-cardinality instrumentation."""

from __future__ import annotations

import asyncio
from datetime import datetime
import logging
from pathlib import Path
from time import monotonic
from typing import Any

from sqlalchemy import event, func, or_, select, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from app.config import get_settings
from app.database_runtime import classify_database_failure
from app.maintenance import maintenance_state
from app.runtime_telemetry import activity, correlation_id_context, metrics
from app.services.upgrade_service import head_revision
from app.utils.time import as_utc, utc_now


logger = logging.getLogger(__name__)


def _query_operation(statement: str) -> str:
    stripped = statement.lstrip()
    return (stripped.split(None, 1)[0].upper() if stripped else "UNKNOWN")[:16]


def install_database_instrumentation(async_engine: AsyncEngine) -> None:
    """Attach one credential/parameter-free instrumentation set to an engine."""

    engine: Engine = async_engine.sync_engine
    if getattr(engine, "_workchord_instrumented", False):
        return
    setattr(engine, "_workchord_instrumented", True)

    @event.listens_for(engine.pool, "checkout")
    def connection_checked_out(*_args: Any) -> None:
        activity.connection_checked_out()
        metrics.increment("workchord_database_pool_checkouts_total")

    @event.listens_for(engine.pool, "checkin")
    def connection_checked_in(
        _dbapi_connection: Any,
        connection_record: Any,
    ) -> None:
        if connection_record.info.pop("workchord_transaction_active", False):
            activity.transaction_finished()
        activity.connection_checked_in()

    @event.listens_for(engine, "begin")
    def transaction_started(connection: Any) -> None:
        if not connection.info.get("workchord_transaction_active", False):
            connection.info["workchord_transaction_active"] = True
            activity.transaction_started()

    @event.listens_for(engine, "commit")
    @event.listens_for(engine, "rollback")
    def transaction_finished(connection: Any) -> None:
        if connection.info.pop("workchord_transaction_active", False):
            activity.transaction_finished()

    @event.listens_for(engine, "before_cursor_execute")
    def before_cursor_execute(
        connection: Any,
        _cursor: Any,
        statement: str,
        _parameters: Any,
        _context: Any,
        _executemany: bool,
    ) -> None:
        stack = connection.info.setdefault("workchord_query_started", [])
        stack.append((monotonic(), _query_operation(statement)))

    @event.listens_for(engine, "after_cursor_execute")
    def after_cursor_execute(
        connection: Any,
        _cursor: Any,
        _statement: str,
        _parameters: Any,
        _context: Any,
        _executemany: bool,
    ) -> None:
        stack = connection.info.get("workchord_query_started", [])
        if not stack:
            return
        started, operation = stack.pop()
        elapsed = monotonic() - started
        metrics.observe(
            "workchord_database_query_duration_seconds",
            elapsed,
            labels={"operation": operation},
        )
        threshold = get_settings().database_slow_query_threshold_ms / 1000
        if elapsed >= threshold:
            metrics.increment(
                "workchord_database_slow_queries_total",
                labels={"operation": operation},
            )
            logger.warning(
                "Slow database query",
                extra={
                    "correlation_id": correlation_id_context.get(),
                    "duration_seconds": round(elapsed, 6),
                    "operation": operation,
                },
            )

    @event.listens_for(engine, "handle_error")
    def handle_database_error(exception_context: Any) -> None:
        connection = exception_context.connection
        if connection is not None:
            stack = connection.info.get("workchord_query_started", [])
            if stack:
                started, operation = stack.pop()
                metrics.observe(
                    "workchord_database_query_duration_seconds",
                    monotonic() - started,
                    labels={"operation": operation},
                )
        failure = classify_database_failure(exception_context.original_exception)
        if failure is not None:
            metrics.increment(
                "workchord_database_errors_total",
                labels={"kind": failure.value},
            )


def _resident_set_size_bytes() -> int | None:
    """Read current Linux RSS without introducing a monitoring dependency."""

    try:
        fields = Path("/proc/self/statm").read_text(encoding="ascii").split()
        resident_pages = int(fields[1])
        return resident_pages * 4096
    except (IndexError, OSError, ValueError):
        return None


async def _queue_snapshot(db: AsyncSession) -> dict[str, Any]:
    from app.models.outbound_webhook import (
        OutboundWebhookDelivery,
        OutboundWebhookDeliveryStatus,
    )

    now = utc_now()
    conditions = (
        OutboundWebhookDelivery.status
        == OutboundWebhookDeliveryStatus.PENDING.value,
        OutboundWebhookDelivery.attempt_count
        < OutboundWebhookDelivery.max_attempts,
        or_(
            OutboundWebhookDelivery.next_retry_at.is_(None),
            OutboundWebhookDelivery.next_retry_at <= now,
        ),
    )
    row = (
        await db.execute(
            select(
                func.count(OutboundWebhookDelivery.id),
                func.min(OutboundWebhookDelivery.created_at),
            ).where(*conditions)
        )
    ).one()
    active_leases = int(
        (
            await db.execute(
                select(func.count(OutboundWebhookDelivery.id)).where(
                    OutboundWebhookDelivery.lease_token.is_not(None),
                    OutboundWebhookDelivery.lease_expires_at > now,
                )
            )
        ).scalar_one()
    )
    oldest: datetime | None = row[1]
    oldest_age_seconds = (
        max(0.0, (now - as_utc(oldest)).total_seconds())
        if oldest is not None
        else 0.0
    )
    snapshot = {
        "ready_depth": int(row[0] or 0),
        "oldest_ready_age_seconds": oldest_age_seconds,
        "active_leases": active_leases,
    }
    metrics.set_gauge("workchord_delivery_queue_ready", snapshot["ready_depth"])
    metrics.set_gauge(
        "workchord_delivery_queue_oldest_ready_age_seconds",
        snapshot["oldest_ready_age_seconds"],
    )
    metrics.set_gauge(
        "workchord_delivery_queue_active_leases",
        snapshot["active_leases"],
    )
    return snapshot


async def _postgresql_snapshot(db: AsyncSession) -> dict[str, Any]:
    if db.get_bind().dialect.name != "postgresql":
        return {"backend": db.get_bind().dialect.name}

    database_row = (
        await db.execute(
            text(
                "SELECT pg_database_size(current_database()), deadlocks, "
                "temp_files, temp_bytes FROM pg_stat_database "
                "WHERE datname = current_database()"
            )
        )
    ).one()
    table_row = (
        await db.execute(
            text(
                "SELECT COALESCE(sum(n_dead_tup), 0), "
                "COALESCE(max(EXTRACT(EPOCH FROM (clock_timestamp() - "
                "COALESCE(last_analyze, last_autoanalyze)))), 0) "
                "FROM pg_stat_user_tables"
            )
        )
    ).one()
    values = {
        "backend": "postgresql",
        "database_size_bytes": int(database_row[0]),
        "deadlocks": int(database_row[1]),
        "temp_files": int(database_row[2]),
        "temp_bytes": int(database_row[3]),
        "dead_tuples": int(table_row[0]),
        "analyze_lag_seconds": float(table_row[1]),
    }
    for key in (
        "database_size_bytes",
        "deadlocks",
        "temp_files",
        "temp_bytes",
        "dead_tuples",
        "analyze_lag_seconds",
    ):
        metrics.set_gauge(f"workchord_database_{key}", values[key])
    return values


async def readiness_snapshot() -> tuple[bool, dict[str, Any]]:
    """Check connectivity, a short query, schema head, and drain evidence."""

    # Import lazily to avoid a database -> observability -> database cycle.
    from app.database import async_session_maker, database_runtime_summary

    settings = get_settings()
    expected_head = head_revision()
    schema_error_kind: str | None = None
    queue_error_kind: str | None = None
    database_metrics_error_kind: str | None = None
    try:
        async with asyncio.timeout(settings.database_readiness_timeout_seconds):
            async with async_session_maker() as db:
                await db.execute(text("SELECT 1"))
                try:
                    revisions = list(
                        (
                            await db.execute(
                                text(
                                    "SELECT version_num FROM alembic_version "
                                    "ORDER BY version_num"
                                )
                            )
                        ).scalars()
                    )
                except SQLAlchemyError as exc:
                    schema_error_kind = type(exc).__name__
                    revisions = []
                    await db.rollback()

                try:
                    queue = await _queue_snapshot(db)
                except SQLAlchemyError as exc:
                    queue_error_kind = type(exc).__name__
                    queue = {
                        "ready_depth": None,
                        "oldest_ready_age_seconds": None,
                        "active_leases": None,
                    }
                    await db.rollback()

                try:
                    database_metrics = await _postgresql_snapshot(db)
                except SQLAlchemyError as exc:
                    # Optional statistics permissions must not turn a healthy,
                    # current application database into an unavailable one.
                    database_metrics_error_kind = type(exc).__name__
                    database_metrics = {
                        "backend": db.get_bind().dialect.name,
                        "error_kind": database_metrics_error_kind,
                    }
                    await db.rollback()
                await db.rollback()
    except Exception as exc:
        metrics.increment(
            "workchord_database_readiness_failures_total",
            labels={"kind": type(exc).__name__},
        )
        return False, {
            "status": "not_ready",
            "database": {
                **database_runtime_summary(),
                "connected": False,
                "schema_current": False,
                "error_kind": type(exc).__name__,
            },
            "maintenance": maintenance_state(),
            "writer_drain": {"drained": False, "reason": "database_unavailable"},
        }

    current_revision = revisions[0] if len(revisions) == 1 else ",".join(revisions)
    schema_current = schema_error_kind is None and current_revision == expected_head
    queue_available = queue_error_kind is None
    process = activity.snapshot()
    mode_state = maintenance_state()
    drained = bool(
        mode_state["mode"] != "off"
        and process.active_mutations == 0
        and process.active_transactions == 0
        and process.worker_in_flight == 0
        and queue_available
        and queue["active_leases"] == 0
    )
    metrics.set_gauge("workchord_writer_drained", int(drained))
    rss = _resident_set_size_bytes()
    if rss is not None:
        metrics.set_gauge("workchord_process_resident_memory_bytes", rss)
    ready = schema_current and queue_available
    return ready, {
        "status": "ready" if ready else "not_ready",
        "database": {
            **database_runtime_summary(),
            "connected": True,
            "schema_current": schema_current,
            "schema_error_kind": schema_error_kind,
            "current_revision": current_revision or None,
            "expected_revision": expected_head,
            "metrics": database_metrics,
            "metrics_error_kind": database_metrics_error_kind,
        },
        "maintenance": mode_state,
        "process": {
            "active_requests": process.active_requests,
            "active_mutations": process.active_mutations,
            "active_transactions": process.active_transactions,
            "checked_out_connections": process.checked_out_connections,
            "worker_running": process.worker_running,
            "worker_in_flight": process.worker_in_flight,
            "resident_memory_bytes": rss,
        },
        "queue": {**queue, "error_kind": queue_error_kind},
        "writer_drain": {
            "drained": drained,
            "replica_agreement_required": True,
            "configuration_fingerprint": mode_state["configuration_fingerprint"],
        },
    }


async def collect_metrics() -> None:
    """Refresh database/queue gauges for a scrape without failing the scrape."""

    try:
        await readiness_snapshot()
    except Exception:  # pragma: no cover - scrape must retain process telemetry
        logger.warning("Could not refresh database metrics", exc_info=True)
