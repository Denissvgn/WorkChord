"""Shared isolated SQLite and PostgreSQL lifecycle fixtures."""

from __future__ import annotations

from collections.abc import AsyncIterator, Awaitable, Callable, Iterator
from datetime import date
from itertools import count
import json
import os
from pathlib import Path
import socket
from typing import Any

import pytest
import pytest_asyncio
from sqlalchemy import event
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.database import Base
from app.config import get_settings
from app.services.agent_routing_rollout import (
    AgentRoutingTopologyReadiness,
    reset_agent_routing_topology_readiness,
    set_agent_routing_topology_readiness,
)
from app import models  # noqa: F401 - register every mapper
from app.models.agent import AgentActor
from app.models.calendar import Calendar
from app.models.iteration import Iteration
from app.models.task import Task
from app.models.team_member import TeamMember, TeamMemberProfile
from tests.support import (
    FailureInjector,
    FrozenClock,
    LegacySQLiteFactory,
    MappedModelFactory,
    PostgresTestDatabase,
    PostgresTestDatabaseManager,
)


@pytest.fixture(autouse=True)
def no_unapproved_network(
    request: pytest.FixtureRequest,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Fail unit tests that accidentally cross a network boundary."""

    if request.node.get_closest_marker("allow_network") is not None:
        return

    def blocked(*_args: Any, **_kwargs: Any) -> None:
        raise AssertionError(
            "Network access is disabled; mark an explicitly scoped test allow_network"
        )

    monkeypatch.setattr(socket.socket, "connect", blocked)
    monkeypatch.setattr(socket, "create_connection", blocked)


@pytest.fixture
def qualified_model_aware_routing_test_context(
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[None]:
    """Run legacy routing suites behind an explicit server-owned test topology."""

    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "enforced")
    get_settings.cache_clear()
    token = set_agent_routing_topology_readiness(
        AgentRoutingTopologyReadiness.ready(
            topology_id="backend-test-topology",
            topology_revision=1,
        )
    )
    try:
        yield
    finally:
        reset_agent_routing_topology_readiness(token)
        get_settings.cache_clear()


@pytest.fixture
def mapped_model_factory() -> MappedModelFactory:
    return MappedModelFactory()


@pytest.fixture
def legacy_sqlite_factory() -> LegacySQLiteFactory:
    return LegacySQLiteFactory()


@pytest.fixture
def frozen_clock() -> FrozenClock:
    return FrozenClock()


@pytest.fixture
def failure_injector() -> FailureInjector:
    return FailureInjector()


@pytest.fixture
def configure_database(monkeypatch: pytest.MonkeyPatch):
    """Point shared database helpers at one test target and clear caches."""

    def configure(database_url: str, *, ssl_mode: str = "disable") -> str:
        monkeypatch.setenv("DATABASE_URL", database_url)
        monkeypatch.setenv("DEPLOYMENT_ENVIRONMENT", "test")
        monkeypatch.setenv("DATABASE_SSL_MODE", ssl_mode)
        get_settings.cache_clear()
        return database_url

    yield configure
    get_settings.cache_clear()


@pytest.fixture
def sqlite_database_url(tmp_path: Path) -> str:
    path = tmp_path / "workchord_test_unit.db"
    return f"sqlite+aiosqlite:///{path}"


@pytest_asyncio.fixture
async def sqlite_engine(sqlite_database_url: str) -> AsyncIterator[AsyncEngine]:
    engine = create_async_engine(sqlite_database_url)

    @event.listens_for(engine.sync_engine, "connect")
    def enable_foreign_keys(dbapi_connection: Any, _connection_record: Any) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    try:
        yield engine
    finally:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.drop_all)
        await engine.dispose()


@pytest_asyncio.fixture
async def db_session_factory(
    sqlite_engine: AsyncEngine,
) -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    """Yield a factory so concurrency tests can open independent transactions."""

    factory = async_sessionmaker(
        sqlite_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    yield factory


@pytest_asyncio.fixture
async def db_session(
    db_session_factory: async_sessionmaker[AsyncSession],
) -> AsyncIterator[AsyncSession]:
    async with db_session_factory() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def profile_factory(
    db_session: AsyncSession,
) -> AsyncIterator[Callable[..., Awaitable[TeamMemberProfile]]]:
    """Persist deterministic reusable routing profiles."""

    sequence = count(1)

    async def create_profile(**overrides: Any) -> TeamMemberProfile:
        marker = next(sequence)
        values: dict[str, Any] = {
            "seed_key": f"routing-test-profile-{marker}",
            "display_name": f"Routing Test Profile {marker}",
            "automation_enabled": True,
            "profile_kind": "agent",
            "assignment_modes": ["execution"],
        }
        values.update(overrides)
        profile = TeamMemberProfile(**values)
        db_session.add(profile)
        await db_session.flush()
        return profile

    yield create_profile


@pytest_asyncio.fixture
async def actor_factory(
    db_session: AsyncSession,
) -> AsyncIterator[Callable[..., Awaitable[AgentActor]]]:
    """Persist deterministic actors with optional profile bindings."""

    sequence = count(1)

    async def create_actor(
        *,
        profile: TeamMemberProfile | None = None,
        **overrides: Any,
    ) -> AgentActor:
        marker = next(sequence)
        values: dict[str, Any] = {
            "name": f"routing-test-actor-{marker}",
            "display_name": f"Routing Test Actor {marker}",
            "api_key_hash": f"routing-test-key-hash-{marker}",
            "scopes": json.dumps(["work:execute"], separators=(",", ":")),
            "enabled": True,
            "role": "worker",
        }
        if profile is not None:
            if "profile" in overrides or "profile_id" in overrides:
                raise TypeError(
                    "Pass either profile or a profile/profile_id override, not both"
                )
            values["profile"] = profile
        values.update(overrides)
        actor = AgentActor(**values)
        db_session.add(actor)
        await db_session.flush()
        return actor

    yield create_actor


@pytest_asyncio.fixture
async def team_member_factory(
    db_session: AsyncSession,
) -> AsyncIterator[Callable[..., Awaitable[TeamMember]]]:
    """Persist deterministic capacity owners with optional profile/iteration links."""

    sequence = count(1)

    async def create_team_member(
        *,
        profile: TeamMemberProfile | None = None,
        iteration: Iteration | None = None,
        **overrides: Any,
    ) -> TeamMember:
        marker = next(sequence)
        values: dict[str, Any] = {
            "name": f"Routing Test Member {marker}",
            "position": "Routing Test Capacity Owner",
        }
        if profile is not None:
            if "profile" in overrides or "profile_id" in overrides:
                raise TypeError(
                    "Pass either profile or a profile/profile_id override, not both"
                )
            values["profile"] = profile
        if iteration is not None:
            if "iteration" in overrides or "iteration_id" in overrides:
                raise TypeError(
                    "Pass either iteration or an iteration/iteration_id override, "
                    "not both"
                )
            values["iteration"] = iteration
        values.update(overrides)
        team_member = TeamMember(**values)
        db_session.add(team_member)
        await db_session.flush()
        return team_member

    yield create_team_member


@pytest_asyncio.fixture
async def task_factory(
    db_session: AsyncSession,
) -> AsyncIterator[Callable[..., Awaitable[Task]]]:
    """Persist deterministic tasks with an isolated valid calendar/iteration graph."""

    sequence = count(1)

    async def create_task(
        *,
        iteration: Iteration | None = None,
        assignee: TeamMember | None = None,
        **overrides: Any,
    ) -> Task:
        if {
            "iteration",
            "iteration_id",
            "assignee",
            "assignee_id",
        }.intersection(overrides):
            raise TypeError(
                "Pass iteration and assignee as explicit factory arguments"
            )

        marker = next(sequence)
        if (
            iteration is None
            and assignee is not None
            and assignee.iteration_id is not None
        ):
            iteration = await db_session.get(Iteration, assignee.iteration_id)
        if iteration is None:
            calendar = Calendar(
                name=f"Routing Test Calendar {marker}",
                year=2026,
            )
            iteration = Iteration(
                name=f"Routing Test Iteration {marker}",
                start_date=date(2026, 7, 1),
                end_date=date(2026, 7, 31),
                calendar=calendar,
            )
            db_session.add(iteration)
            await db_session.flush()

        if assignee is not None and assignee.iteration_id is None:
            assignee.iteration = iteration

        values: dict[str, Any] = {
            "title": f"Routing Test Task {marker}",
            "iteration": iteration,
        }
        if assignee is not None:
            values["assignee"] = assignee
        values.update(overrides)
        task = Task(**values)
        db_session.add(task)
        await db_session.flush()
        return task

    yield create_task


@pytest.fixture
def postgres_database() -> Iterator[PostgresTestDatabase]:
    admin_url = os.environ.get("POSTGRES_ADMIN_URL")
    if not admin_url:
        pytest.skip("POSTGRES_ADMIN_URL is required for PostgreSQL integration tests")
    manager = PostgresTestDatabaseManager(
        admin_url,
        deployment_environment=os.environ.get("DEPLOYMENT_ENVIRONMENT"),
    )
    try:
        with manager.database() as database:
            yield database
    finally:
        manager.cleanup()
