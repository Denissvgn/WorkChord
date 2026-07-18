"""Fast unit coverage for the Wave 0 database test infrastructure."""

from __future__ import annotations

import asyncio
from datetime import timedelta
from pathlib import Path
import sqlite3

import pytest
from sqlalchemy import inspect as sa_inspect, select

from app.database import Base
from app.models.calendar import Calendar
from app.models.iteration import Iteration
from tests.support import AsyncBarrier, UnsafeDatabaseTarget
from tests.support.database import assert_safe_test_database_url


@pytest.mark.parametrize(
    "database_url",
    [
        "postgresql+psycopg://postgres:secret@localhost/workchord",
        "postgresql+psycopg://postgres:secret@db.production/workchord_test_0123456789abcdef0123456789abcdef",
        "sqlite+aiosqlite:////mnt/data/projects/WorkChord/workchord_test_bad.db",
    ],
)
def test_safety_fence_rejects_production_like_targets(database_url: str) -> None:
    with pytest.raises(UnsafeDatabaseTarget):
        assert_safe_test_database_url(
            database_url,
            deployment_environment="test",
        )


def test_safety_fence_requires_test_environment() -> None:
    with pytest.raises(UnsafeDatabaseTarget, match="DEPLOYMENT_ENVIRONMENT=test"):
        assert_safe_test_database_url(
            "postgresql+psycopg://postgres:secret@localhost/"
            "workchord_test_0123456789abcdef0123456789abcdef",
            deployment_environment="production",
        )


def test_safety_fence_accepts_only_unique_local_test_target() -> None:
    url = assert_safe_test_database_url(
        "postgresql+psycopg://postgres:secret@localhost/"
        "workchord_test_0123456789abcdef0123456789abcdef",
        deployment_environment="test",
    )
    assert url.database == "workchord_test_0123456789abcdef0123456789abcdef"


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_isolated_sqlite_session_round_trips_representative_graph(
    db_session,
    mapped_model_factory,
) -> None:
    calendar = mapped_model_factory.build(Calendar, name="Test calendar", year=2026)
    db_session.add(calendar)
    await db_session.flush()
    iteration = mapped_model_factory.build(
        Iteration,
        name="Test iteration",
        calendar_id=calendar.id,
    )
    db_session.add(iteration)
    await db_session.commit()

    stored = await db_session.scalar(select(Iteration).where(Iteration.id == iteration.id))
    assert stored is not None
    assert stored.name == "Test iteration"
    assert stored.calendar_id == calendar.id


def test_generic_factory_covers_every_mapped_table(mapped_model_factory) -> None:
    mappers = sorted(Base.registry.mappers, key=lambda mapper: mapper.local_table.name)
    assert len(mappers) == 38
    for mapper in mappers:
        instance = mapped_model_factory.build(mapper.class_)
        assert sa_inspect(instance).mapper is mapper


@pytest.mark.sqlite
def test_legacy_factory_builds_valid_and_orphan_sources(
    tmp_path: Path,
    legacy_sqlite_factory,
) -> None:
    valid = legacy_sqlite_factory.create(tmp_path / "legacy-valid.db")
    orphan = legacy_sqlite_factory.create(
        tmp_path / "legacy-orphan.db",
        with_orphan=True,
    )

    with sqlite3.connect(valid) as connection:
        assert connection.execute("PRAGMA foreign_key_check").fetchall() == []
    with sqlite3.connect(orphan) as connection:
        failures = connection.execute("PRAGMA foreign_key_check").fetchall()
    assert failures == [("task_status_logs", 1, "tasks", 0)]


def test_clock_and_failure_injector_are_deterministic(
    frozen_clock,
    failure_injector,
) -> None:
    start = frozen_clock.now()
    assert frozen_clock.advance(timedelta(seconds=30)) == start + timedelta(seconds=30)
    with pytest.raises(ValueError, match="backwards"):
        frozen_clock.advance(timedelta(seconds=-1))

    failure_injector.fail_next("before-commit", RuntimeError("injected"))
    with pytest.raises(RuntimeError, match="injected"):
        failure_injector.checkpoint("before-commit")
    failure_injector.checkpoint("before-commit")


@pytest.mark.asyncio
async def test_async_barrier_controls_interleaving() -> None:
    barrier = AsyncBarrier(2)
    events: list[str] = []

    async def participant(name: str) -> None:
        events.append(f"{name}-before")
        await barrier.wait()
        events.append(f"{name}-after")

    await asyncio.gather(participant("a"), participant("b"))
    first_after = min(events.index("a-after"), events.index("b-after"))
    assert set(events[:first_after]) == {"a-before", "b-before"}
