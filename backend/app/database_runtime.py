"""PostgreSQL error classification and bounded transaction retry policy."""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from enum import Enum
import logging
import random
from time import monotonic
from typing import TypeVar

from sqlalchemy.exc import DBAPIError

from app.runtime_telemetry import correlation_id_context, metrics


logger = logging.getLogger(__name__)
T = TypeVar("T")

RETRYABLE_TRANSACTION_SQLSTATES = frozenset({"40001", "40P01"})
RETRYABLE_CONNECTION_SQLSTATES = frozenset(
    {
        "08000",
        "08001",
        "08003",
        "08004",
        "08006",
        "08007",
        "08P01",
        "53300",
        "57P01",
        "57P02",
        "57P03",
    }
)


class DatabaseFailureKind(str, Enum):
    SERIALIZATION = "serialization"
    DEADLOCK = "deadlock"
    CONNECTION = "connection"


class DatabaseConflictError(RuntimeError):
    """A safe mutation exhausted serialization/deadlock retries."""


class DatabaseUnavailableError(RuntimeError):
    """A retryable database availability failure exhausted its budget."""


@dataclass(frozen=True)
class DatabaseRetryPolicy:
    """A short retry budget that cannot outlive the request deadline."""

    max_attempts: int = 3
    base_delay_seconds: float = 0.025
    max_delay_seconds: float = 0.250
    deadline_seconds: float = 1.0

    def __post_init__(self) -> None:
        if not 1 <= self.max_attempts <= 5:
            raise ValueError("Database retry attempts must be between 1 and 5")
        if self.base_delay_seconds < 0 or self.max_delay_seconds < 0:
            raise ValueError("Database retry delays cannot be negative")
        if self.base_delay_seconds > self.max_delay_seconds:
            raise ValueError("Database retry base delay cannot exceed max delay")
        if not 0 < self.deadline_seconds <= 10:
            raise ValueError("Database retry deadline must be between 0 and 10 seconds")


def sqlstate_from_exception(exc: BaseException) -> str | None:
    """Extract a Psycopg/DBAPI SQLSTATE without relying on message text."""

    candidate: object = exc
    if isinstance(exc, DBAPIError) and exc.orig is not None:
        candidate = exc.orig
    for attribute in ("sqlstate", "pgcode"):
        value = getattr(candidate, attribute, None)
        if isinstance(value, str) and len(value) == 5:
            return value
    return None


def classify_database_failure(exc: BaseException) -> DatabaseFailureKind | None:
    """Classify only explicit PostgreSQL transient states.

    SQLite ``database is locked`` messages are deliberately excluded: SQLite's
    busy timeout and serialized write boundary remain its only lock policy.
    """

    sqlstate = sqlstate_from_exception(exc)
    if sqlstate == "40001":
        return DatabaseFailureKind.SERIALIZATION
    if sqlstate == "40P01":
        return DatabaseFailureKind.DEADLOCK
    if sqlstate in RETRYABLE_CONNECTION_SQLSTATES or (
        sqlstate is not None and sqlstate.startswith("08")
    ):
        return DatabaseFailureKind.CONNECTION
    return None


def _exhausted_error(kind: DatabaseFailureKind) -> RuntimeError:
    if kind in {DatabaseFailureKind.SERIALIZATION, DatabaseFailureKind.DEADLOCK}:
        return DatabaseConflictError(
            "Database transaction conflict persisted after bounded retries"
        )
    return DatabaseUnavailableError(
        "Database remained unavailable after bounded retries"
    )


async def run_database_retry(
    operation: Callable[[int], Awaitable[T]],
    *,
    operation_name: str,
    safe_to_retry: bool,
    rollback: Callable[[], Awaitable[object]] | None = None,
    policy: DatabaseRetryPolicy = DatabaseRetryPolicy(),
    sleep: Callable[[float], Awaitable[object]] = asyncio.sleep,
    random_value: Callable[[], float] = random.random,
) -> T:
    """Run one complete transaction boundary with a bounded replay policy.

    Callers must set ``safe_to_retry`` only for idempotent compare-and-set work
    or commands protected by a durable command record.  The callable receives a
    one-based attempt number and must include its commit inside the boundary.
    """

    started = monotonic()
    attempt = 0
    while True:
        attempt += 1
        try:
            return await operation(attempt)
        except Exception as exc:
            kind = classify_database_failure(exc)
            if kind is None:
                raise
            metrics.increment(
                "workchord_database_transaction_failures_total",
                labels={"kind": kind.value, "operation": operation_name},
            )
            if rollback is not None:
                try:
                    await rollback()
                except Exception:
                    logger.warning(
                        "Database rollback failed during retry cleanup",
                        exc_info=True,
                        extra={"operation": operation_name},
                    )

            elapsed = monotonic() - started
            can_retry = safe_to_retry and attempt < policy.max_attempts
            if not can_retry:
                metrics.increment(
                    "workchord_database_retries_exhausted_total",
                    labels={"kind": kind.value, "operation": operation_name},
                )
                raise _exhausted_error(kind) from exc

            exponential = min(
                policy.max_delay_seconds,
                policy.base_delay_seconds * (2 ** (attempt - 1)),
            )
            delay = exponential * (0.5 + max(0.0, min(1.0, random_value())))
            if elapsed + delay >= policy.deadline_seconds:
                metrics.increment(
                    "workchord_database_retries_exhausted_total",
                    labels={"kind": kind.value, "operation": operation_name},
                )
                raise _exhausted_error(kind) from exc

            metrics.increment(
                "workchord_database_retries_total",
                labels={"kind": kind.value, "operation": operation_name},
            )
            logger.warning(
                "Retrying safe database transaction",
                extra={
                    "attempt": attempt,
                    "correlation_id": correlation_id_context.get(),
                    "failure_kind": kind.value,
                    "operation": operation_name,
                },
            )
            await sleep(delay)
