"""DBM-RUN-001 real-PostgreSQL concurrency and invariant matrix."""

from __future__ import annotations

import asyncio
from datetime import date, timedelta
from pathlib import Path

import pytest
import pytest_asyncio
from sqlalchemy import Column, Integer, MetaData, String, Table, func, select, text, update
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import get_settings
from app.database_config import parse_database_configuration
from app.models.agent import (
    AgentActor,
    AgentIdempotencyRecord,
    AgentRun,
    AgentTaskAssignment,
)
from app.models.calendar import Calendar
from app.models.iteration import Iteration
from app.models.outbound_webhook import (
    OutboundWebhookDelivery,
    OutboundWebhookDeliveryStatus,
    OutboundWebhookEvent,
)
from app.models.task import Task
from app.models.triage import TriageItem, TriageItemStatus
from app.services.outbound_webhook_service import OutboundWebhookService
from app.services.agent_planning_service import AgentPlanningService
from app.services.task_service import TaskService, TaskVersionConflictError
from app.services.upgrade_service import bootstrap_database_schema
from app.sql_semantics import portable_contains
from app.utils.time import utc_now
from tests.support import AsyncBarrier


@pytest_asyncio.fixture
async def postgresql_session_factory(
    postgres_database,
    configure_database,
) -> async_sessionmaker[AsyncSession]:
    configure_database(postgres_database.url)
    bootstrap_database_schema()
    configuration = parse_database_configuration(get_settings())
    engine_options = configuration.async_engine_kwargs()
    engine_options.update(pool_size=8, max_overflow=0)
    engine: AsyncEngine = create_async_engine(
        configuration.async_url,
        **engine_options,
    )
    factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    try:
        yield factory
    finally:
        await engine.dispose()


async def _seed_race_workspace(
    factory: async_sessionmaker[AsyncSession],
) -> dict[str, object]:
    async with factory() as db:
        calendar = Calendar(name="Race calendar", year=2026)
        db.add(calendar)
        await db.flush()
        iteration = Iteration(
            name="Race iteration",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 1, 14),
            calendar_id=calendar.id,
        )
        db.add(iteration)
        await db.flush()
        tasks = [
            Task(title=f"Race task {index}", iteration_id=iteration.id)
            for index in range(1, 7)
        ]
        actors = [
            AgentActor(
                name=f"race-actor-{index}",
                display_name=f"Race Actor {index}",
                api_key_hash=str(index) * 64,
                scopes='["tasks:write"]',
            )
            for index in range(1, 3)
        ]
        triage = TriageItem(title="Race triage")
        event = OutboundWebhookEvent(
            event_id="e" * 64,
            event_type="task.updated",
            entity_type="task",
            entity_id=None,
            payload_json={},
        )
        db.add_all([*tasks, *actors, triage, event])
        await db.flush()
        deliveries = [
            OutboundWebhookDelivery(
                event_id=event.id,
                target_name=f"Race target {index}",
                target_url="https://example.test/hook",
                payload_json={},
            )
            for index in range(1, 4)
        ]
        db.add_all(deliveries)
        await db.commit()
        return {
            "iteration_id": iteration.id,
            "task_ids": [task.id for task in tasks],
            "actor_ids": [actor.id for actor in actors],
            "triage_id": triage.id,
            "delivery_ids": [delivery.id for delivery in deliveries],
        }


async def _task_version_attempt(
    factory: async_sessionmaker[AsyncSession],
    task_id: int,
    barrier: AsyncBarrier,
) -> str:
    async with factory() as db:
        task = await db.get(Task, task_id)
        assert task is not None
        await barrier.wait()
        try:
            await TaskService(db).reserve_task_version(task, 1)
            await db.commit()
            return "winner"
        except TaskVersionConflictError:
            await db.rollback()
            return "typed_conflict"


async def _insert_assignment(
    factory: async_sessionmaker[AsyncSession],
    *,
    task_id: int,
    actor_id: int,
    barrier: AsyncBarrier,
) -> str:
    async with factory() as db:
        await barrier.wait()
        db.add(
            AgentTaskAssignment(
                task_id=task_id,
                actor_id=actor_id,
                purpose="execution",
                state="queued",
                task_version=2,
            )
        )
        try:
            await db.commit()
            return "winner"
        except IntegrityError:
            await db.rollback()
            return "unique_conflict"


async def _insert_run(
    factory: async_sessionmaker[AsyncSession],
    *,
    task_id: int,
    actor_id: int,
    assignment_id: int,
    barrier: AsyncBarrier,
) -> str:
    async with factory() as db:
        await barrier.wait()
        db.add(
            AgentRun(
                task_id=task_id,
                actor_id=actor_id,
                assignment_id=assignment_id,
                status="running",
            )
        )
        try:
            await db.commit()
            return "winner"
        except IntegrityError:
            await db.rollback()
            return "unique_conflict"


async def _record_planning_command(
    factory: async_sessionmaker[AsyncSession],
    *,
    actor_id: int,
    task_id: int,
    barrier: AsyncBarrier,
) -> str:
    async with factory() as db:
        await barrier.wait()
        db.add(
            AgentIdempotencyRecord(
                actor_id=actor_id,
                operation="planning_apply",
                target_type="task",
                target_id=task_id,
                idempotency_key="same-planning-command",
                request_hash="f" * 64,
                response_payload="{}",
            )
        )
        try:
            await db.commit()
            return "winner"
        except IntegrityError:
            await db.rollback()
            return "unique_conflict"


@pytest.mark.postgresql
@pytest.mark.integration
@pytest.mark.allow_network
@pytest.mark.asyncio
async def test_postgresql_race_matrix_preserves_all_invariants(
    postgresql_session_factory: async_sessionmaker[AsyncSession],
    postgres_database,
) -> None:
    factory = postgresql_session_factory
    seeded = await _seed_race_workspace(factory)
    task_ids = seeded["task_ids"]
    actor_ids = seeded["actor_ids"]
    delivery_ids = seeded["delivery_ids"]
    assert isinstance(task_ids, list)
    assert isinstance(actor_ids, list)
    assert isinstance(delivery_ids, list)

    # Same-resource optimistic writes have exactly one winner and one typed
    # conflict. Different task rows advance without conflicting.
    version_barrier = AsyncBarrier(2)
    same_task_results = await asyncio.gather(
        _task_version_attempt(factory, task_ids[0], version_barrier),
        _task_version_attempt(factory, task_ids[0], version_barrier),
    )
    assert sorted(same_task_results) == ["typed_conflict", "winner"]

    unrelated_barrier = AsyncBarrier(2)
    unrelated_results = await asyncio.gather(
        _task_version_attempt(factory, task_ids[1], unrelated_barrier),
        _task_version_attempt(factory, task_ids[2], unrelated_barrier),
    )
    assert unrelated_results == ["winner", "winner"]

    # Claim generation is an atomic compare-and-set: no double owner.
    claim_barrier = AsyncBarrier(2)

    async def claim(actor_id: int) -> int | None:
        async with factory() as db:
            await claim_barrier.wait()
            claimed = (
                await db.execute(
                    update(Task)
                    .where(Task.id == task_ids[0], Task.claimed_by.is_(None))
                    .values(
                        claimed_by=actor_id,
                        claim_generation=Task.claim_generation + 1,
                    )
                    .returning(Task.claimed_by)
                )
            ).scalar_one_or_none()
            await db.commit()
            return claimed

    claim_results = await asyncio.gather(claim(actor_ids[0]), claim(actor_ids[1]))
    assert len([result for result in claim_results if result is not None]) == 1

    assignment_barrier = AsyncBarrier(2)
    assignment_results = await asyncio.gather(
        _insert_assignment(
            factory,
            task_id=task_ids[0],
            actor_id=actor_ids[0],
            barrier=assignment_barrier,
        ),
        _insert_assignment(
            factory,
            task_id=task_ids[0],
            actor_id=actor_ids[1],
            barrier=assignment_barrier,
        ),
    )
    assert sorted(assignment_results) == ["unique_conflict", "winner"]

    async with factory() as db:
        assignment = (
            await db.execute(
                select(AgentTaskAssignment).where(
                    AgentTaskAssignment.task_id == task_ids[0],
                    AgentTaskAssignment.state.in_(("queued", "accepted")),
                )
            )
        ).scalar_one()
        assignment_id = assignment.id
        assignment_actor_id = assignment.actor_id

    run_barrier = AsyncBarrier(2)
    run_results = await asyncio.gather(
        _insert_run(
            factory,
            task_id=task_ids[0],
            actor_id=assignment_actor_id,
            assignment_id=assignment_id,
            barrier=run_barrier,
        ),
        _insert_run(
            factory,
            task_id=task_ids[0],
            actor_id=assignment_actor_id,
            assignment_id=assignment_id,
            barrier=run_barrier,
        ),
    )
    assert sorted(run_results) == ["unique_conflict", "winner"]

    command_barrier = AsyncBarrier(2)
    command_results = await asyncio.gather(
        _record_planning_command(
            factory,
            actor_id=actor_ids[0],
            task_id=task_ids[0],
            barrier=command_barrier,
        ),
        _record_planning_command(
            factory,
            actor_id=actor_ids[0],
            task_id=task_ids[0],
            barrier=command_barrier,
        ),
    )
    assert sorted(command_results) == ["unique_conflict", "winner"]

    # Triage conversion reservation admits one target task only.
    triage_barrier = AsyncBarrier(2)

    async def reserve_triage(converted_task_id: int) -> int:
        async with factory() as db:
            await triage_barrier.wait()
            result = await db.execute(
                update(TriageItem)
                .where(
                    TriageItem.id == seeded["triage_id"],
                    TriageItem.status != TriageItemStatus.CONVERTED.value,
                    TriageItem.converted_task_id.is_(None),
                )
                .values(
                    status=TriageItemStatus.CONVERTED.value,
                    converted_task_id=converted_task_id,
                )
            )
            await db.commit()
            return int(result.rowcount or 0)

    triage_results = await asyncio.gather(
        reserve_triage(task_ids[3]),
        reserve_triage(task_ids[4]),
    )
    assert sorted(triage_results) == [0, 1]

    # SKIP LOCKED claiming is exclusive and fair across due rows.
    claimed_at = utc_now()
    queue_barrier = AsyncBarrier(2)

    async def claim_one(worker_id: str) -> list[tuple[int, str]]:
        async with factory() as db:
            await queue_barrier.wait()
            return await OutboundWebhookService(db).claim_due_deliveries(
                limit=1,
                worker_id=worker_id,
                now=claimed_at,
            )

    queue_results = await asyncio.gather(claim_one("worker-a"), claim_one("worker-b"))
    flattened = [claim for result in queue_results for claim in result]
    assert len(flattened) == 2
    assert len({delivery_id for delivery_id, _token in flattened}) == 2
    assert all(len(token) <= 64 for _delivery_id, token in flattened)

    # Process loss is recovered only after expiry; the old token loses authority.
    remaining_delivery_id = next(
        delivery_id for delivery_id in delivery_ids if delivery_id not in {
            item[0] for item in flattened
        }
    )
    async with factory() as db:
        service = OutboundWebhookService(db)
        old_token = await service._claim_delivery_id(
            remaining_delivery_id,
            worker_id="lost-worker",
            now=claimed_at,
        )
    assert old_token is not None
    async with factory() as db:
        new_token = await OutboundWebhookService(db)._claim_delivery_id(
            remaining_delivery_id,
            worker_id="replacement-worker",
            now=claimed_at + timedelta(seconds=121),
        )
    assert new_token is not None
    assert new_token != old_token

    # A lock on one task does not block a mutation of an unrelated task row.
    first_locked = asyncio.Event()
    release_first = asyncio.Event()

    async def hold_first_lock() -> None:
        async with factory() as db:
            await db.execute(
                select(Task.id)
                .where(Task.id == task_ids[1])
                .with_for_update()
            )
            first_locked.set()
            await release_first.wait()
            await db.rollback()

    holder = asyncio.create_task(hold_first_lock())
    await first_locked.wait()
    try:
        async def update_unrelated() -> None:
            async with factory() as db:
                await db.execute(
                    update(Task)
                    .where(Task.id == task_ids[2])
                    .values(title="Unrelated write completed")
                )
                await db.commit()

        await asyncio.wait_for(update_unrelated(), timeout=1.0)
    finally:
        release_first.set()
        await holder

    async with factory() as db:
        task = await db.get(Task, task_ids[0])
        triage = await db.get(TriageItem, seeded["triage_id"])
        assert task is not None and task.claim_generation == 1
        assert task.claimed_by in actor_ids
        assert triage is not None and triage.converted_task_id in task_ids[3:5]
        assert (
            await db.scalar(
                select(func.count(AgentTaskAssignment.id)).where(
                    AgentTaskAssignment.task_id == task_ids[0],
                    AgentTaskAssignment.state.in_(("queued", "accepted")),
                )
            )
        ) == 1
        assert (
            await db.scalar(
                select(func.count(AgentRun.id)).where(
                    AgentRun.assignment_id == assignment_id,
                    AgentRun.status == "running",
                )
            )
        ) == 1
        assert (
            await db.scalar(select(func.count(AgentIdempotencyRecord.id)))
        ) == 1

    # Bind the ordering/comparison golden case to the approved database facts.
    assert postgres_database.encoding == "UTF8"
    assert postgres_database.locale_provider == "builtin"
    assert postgres_database.locale == "PG_UNICODE_FAST"
    assert postgres_database.collation_version == "1"
    assert postgres_database.timezone == "UTC"
    assert postgres_database.role_timezone == "UTC"

    semantics = Table(
        "runtime_semantics_wave2",
        MetaData(),
        Column("id", Integer, primary_key=True),
        Column("name", String, nullable=False),
        Column("due", Integer, nullable=True),
    )
    async with factory() as db:
        connection = await db.connection()
        await connection.run_sync(semantics.create)
        await db.execute(
            semantics.insert(),
            [
                {"id": 1, "name": "Alpha", "due": None},
                {"id": 2, "name": "alpha", "due": 10},
                {"id": 3, "name": "Бета", "due": 10},
                {"id": 4, "name": "бета", "due": None},
                {"id": 5, "name": "100%", "due": 10},
            ],
        )
        ascii_matches = list(
            (
                await db.scalars(
                    select(semantics.c.id)
                    .where(portable_contains(semantics.c.name, "ALP"))
                    .order_by(semantics.c.id)
                )
            ).all()
        )
        unicode_matches = list(
            (
                await db.scalars(
                    select(semantics.c.id)
                    .where(portable_contains(semantics.c.name, "Бета"))
                    .order_by(semantics.c.id)
                )
            ).all()
        )
        escaped_matches = list(
            (
                await db.scalars(
                    select(semantics.c.id).where(
                        portable_contains(semantics.c.name, "%")
                    )
                )
            ).all()
        )
        ordered = list(
            (
                await db.scalars(
                    select(semantics.c.id).order_by(
                        semantics.c.due.asc().nulls_first(),
                        semantics.c.id.asc(),
                    )
                )
            ).all()
        )
        await db.rollback()

    assert ascii_matches == [1, 2]
    assert unicode_matches == [3]
    assert escaped_matches == [5]
    assert ordered == [1, 4, 2, 3, 5]


@pytest.mark.postgresql
@pytest.mark.integration
@pytest.mark.allow_network
@pytest.mark.asyncio
async def test_schedule_locks_are_iteration_scoped(
    postgresql_session_factory: async_sessionmaker[AsyncSession],
) -> None:
    """Different aggregates proceed while the same aggregate is serialized."""
    factory = postgresql_session_factory
    seeded = await _seed_race_workspace(factory)
    first_iteration_id = int(seeded["iteration_id"])
    async with factory() as db:
        first_iteration = await db.get(Iteration, first_iteration_id)
        assert first_iteration is not None
        second_iteration = Iteration(
            name="Independent schedule iteration",
            start_date=date(2026, 2, 1),
            end_date=date(2026, 2, 14),
            calendar_id=first_iteration.calendar_id,
        )
        db.add(second_iteration)
        await db.flush()
        db.add(Task(title="Independent schedule task", iteration_id=second_iteration.id))
        await db.commit()
        second_iteration_id = second_iteration.id

    first_locked = asyncio.Event()
    release_first = asyncio.Event()

    async def hold_first_aggregate() -> None:
        async with factory() as db:
            await AgentPlanningService(db)._lock_schedule_task_set(
                first_iteration_id
            )
            first_locked.set()
            await release_first.wait()
            await db.rollback()

    holder = asyncio.create_task(hold_first_aggregate())
    await first_locked.wait()
    try:
        async with factory() as db:
            await db.execute(text("SET LOCAL lock_timeout = '250ms'"))
            await asyncio.wait_for(
                AgentPlanningService(db)._lock_schedule_task_set(
                    second_iteration_id
                ),
                timeout=1.0,
            )
            await db.rollback()

        async with factory() as db:
            await db.execute(text("SET LOCAL lock_timeout = '250ms'"))
            with pytest.raises(DBAPIError, match="lock timeout"):
                await AgentPlanningService(db)._lock_schedule_task_set(
                    first_iteration_id
                )
            await db.rollback()
    finally:
        release_first.set()
        await holder


def test_schedule_lock_implementation_has_no_global_table_lock() -> None:
    source = (
        Path(__file__).resolve().parents[3]
        / "backend/app/services/agent_planning_service.py"
    ).read_text(encoding="utf-8")

    assert "LOCK TABLE tasks" not in source
    assert ".with_for_update(read=True)" in source
    assert "Schedule inputs changed during apply" in source


def test_global_lock_order_is_documented_and_implemented() -> None:
    repository_root = Path(__file__).resolve().parents[3]
    policy = (repository_root / "docs/database-runtime-policy.md").read_text()
    source = (
        repository_root / "backend/app/services/agent_work_service.py"
    ).read_text()

    assert "Project`, then `Iteration" in policy
    assert "`Task`, ordered by primary key" in policy
    assert "`AgentActor`, ordered by primary key" in policy
    assert "`AgentTaskAssignment`, ordered by primary key" in policy
    assert "`AgentRun`, ordered by primary key" in policy
    assert source.index("async def _lock_task") < source.index("async def _lock_actors")
    assert source.index("async def _lock_actors") < source.index(
        "async def _lock_task_assignments"
    )
    assert source.index("async def _lock_task_assignments") < source.index(
        "async def _lock_task_runs"
    )
