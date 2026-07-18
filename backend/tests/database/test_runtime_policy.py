"""DBM-RUN-002/003 retry, ordering, and comparison contract tests."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from sqlalchemy import Column, Integer, MetaData, String, Table, create_engine, select

from app.database_runtime import (
    DatabaseConflictError,
    DatabaseFailureKind,
    DatabaseRetryPolicy,
    classify_database_failure,
    run_database_retry,
)
from app.query_limits import (
    MAX_BOUNDED_LIST_ITEMS,
    MAX_ITERATION_TREE_TASKS,
)
from app.sql_semantics import portable_contains


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


class SqlStateFailure(RuntimeError):
    """Minimal Psycopg-shaped fault used without a database server."""

    def __init__(self, sqlstate: str):
        self.sqlstate = sqlstate
        super().__init__(f"injected SQLSTATE {sqlstate}")


@pytest.mark.parametrize(
    ("sqlstate", "kind"),
    [
        ("40001", DatabaseFailureKind.SERIALIZATION),
        ("40P01", DatabaseFailureKind.DEADLOCK),
        ("08006", DatabaseFailureKind.CONNECTION),
        ("57P01", DatabaseFailureKind.CONNECTION),
    ],
)
def test_retry_classifier_uses_sqlstate_not_messages(
    sqlstate: str,
    kind: DatabaseFailureKind,
) -> None:
    assert classify_database_failure(SqlStateFailure(sqlstate)) is kind
    assert classify_database_failure(RuntimeError("database is locked")) is None
    assert classify_database_failure(RuntimeError("deadlock detected")) is None


@pytest.mark.asyncio
async def test_safe_transaction_recovers_within_bounded_attempts() -> None:
    attempts: list[int] = []
    delays: list[float] = []
    rollbacks = 0

    async def operation(attempt: int) -> str:
        attempts.append(attempt)
        if attempt < 3:
            raise SqlStateFailure("40001")
        return "committed"

    async def rollback() -> None:
        nonlocal rollbacks
        rollbacks += 1

    async def sleep(delay: float) -> None:
        delays.append(delay)

    result = await run_database_retry(
        operation,
        operation_name="test_safe_command",
        safe_to_retry=True,
        rollback=rollback,
        sleep=sleep,
        random_value=lambda: 0.0,
    )

    assert result == "committed"
    assert attempts == [1, 2, 3]
    assert rollbacks == 2
    assert len(delays) == 2
    assert all(0 <= delay <= 0.250 for delay in delays)


@pytest.mark.asyncio
async def test_unsafe_transaction_is_never_replayed() -> None:
    attempts = 0

    async def operation(_attempt: int) -> None:
        nonlocal attempts
        attempts += 1
        raise SqlStateFailure("40P01")

    with pytest.raises(DatabaseConflictError):
        await run_database_retry(
            operation,
            operation_name="unsafe_external_side_effect",
            safe_to_retry=False,
        )

    assert attempts == 1


@pytest.mark.asyncio
async def test_retry_after_durable_command_record_does_not_duplicate_effect() -> None:
    command_records: set[str] = set()
    published_events: list[str] = []

    async def operation(attempt: int) -> str:
        if "command-1" in command_records:
            return "replayed"
        command_records.add("command-1")
        published_events.append("task.updated")
        if attempt == 1:
            # Simulate an acknowledgement/commit-boundary failure. Replay sees
            # the durable command record and cannot append a second event.
            raise SqlStateFailure("08007")
        return "committed"

    result = await run_database_retry(
        operation,
        operation_name="recorded_command",
        safe_to_retry=True,
        sleep=lambda _delay: _completed_sleep(),
    )

    assert result == "replayed"
    assert command_records == {"command-1"}
    assert published_events == ["task.updated"]


async def _completed_sleep() -> None:
    return None


@pytest.mark.asyncio
async def test_retry_deadline_and_attempt_storm_are_bounded() -> None:
    attempts = 0

    async def operation(_attempt: int) -> None:
        nonlocal attempts
        attempts += 1
        raise SqlStateFailure("40001")

    with pytest.raises(DatabaseConflictError):
        await run_database_retry(
            operation,
            operation_name="bounded_storm",
            safe_to_retry=True,
            policy=DatabaseRetryPolicy(
                max_attempts=5,
                base_delay_seconds=0.25,
                max_delay_seconds=0.25,
                deadline_seconds=0.01,
            ),
            sleep=lambda _delay: _completed_sleep(),
            random_value=lambda: 1.0,
        )

    assert attempts == 1


def test_ascii_unicode_null_and_tie_ordering_golden_case() -> None:
    metadata = MetaData()
    values = Table(
        "runtime_semantics",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String, nullable=False),
        Column("due", Integer, nullable=True),
    )
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    try:
        with engine.begin() as connection:
            connection.execute(
                values.insert(),
                [
                    {"id": 1, "name": "Alpha", "due": None},
                    {"id": 2, "name": "alpha", "due": 10},
                    {"id": 3, "name": "Бета", "due": 10},
                    {"id": 4, "name": "бета", "due": None},
                    {"id": 5, "name": "100%", "due": 10},
                ],
            )

            ascii_matches = connection.scalars(
                select(values.c.id)
                .where(portable_contains(values.c.name, "ALP"))
                .order_by(values.c.id)
            ).all()
            unicode_matches = connection.scalars(
                select(values.c.id)
                .where(portable_contains(values.c.name, "Бета"))
                .order_by(values.c.id)
            ).all()
            escaped_matches = connection.scalars(
                select(values.c.id).where(portable_contains(values.c.name, "%"))
            ).all()
            ordered = connection.scalars(
                select(values.c.id).order_by(
                    values.c.due.asc().nulls_first(),
                    values.c.id.asc(),
                )
            ).all()

        assert ascii_matches == [1, 2]
        assert unicode_matches == [3]
        assert escaped_matches == [5]
        assert ordered == [1, 4, 2, 3, 5]
    finally:
        engine.dispose()


def test_response_bounds_match_the_approved_capacity_contract() -> None:
    contract = json.loads(
        (REPOSITORY_ROOT / "docs/contracts/postgresql-capacity-contract-v1.json")
        .read_text(encoding="utf-8")
    )
    response_profiles = contract["traffic"]["response_profiles"]

    assert MAX_BOUNDED_LIST_ITEMS == response_profiles["bounded_list"][
        "cardinality_p50_p95_max"
    ][-1]
    assert MAX_ITERATION_TREE_TASKS == response_profiles["task_tree"][
        "cardinality_p50_p95_max"
    ][-1]
