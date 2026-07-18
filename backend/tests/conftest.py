"""Shared isolated SQLite and PostgreSQL lifecycle fixtures."""

from __future__ import annotations

from collections.abc import AsyncIterator, Iterator
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
from app import models  # noqa: F401 - register every mapper
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
