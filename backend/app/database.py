from collections.abc import AsyncGenerator

from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings
from app.database_config import parse_database_configuration

settings = get_settings()
database_configuration = parse_database_configuration(settings)

engine = create_async_engine(
    database_configuration.async_url,
    **database_configuration.async_engine_kwargs(echo=settings.debug),
)

if database_configuration.backend == "sqlite":

    @event.listens_for(engine.sync_engine, "connect")
    def enable_sqlite_foreign_keys(dbapi_connection, _connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """Base class for all models."""
    pass


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting database session."""
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db() -> None:
    """Verify the database schema is Alembic-current before serving traffic."""
    from app.services.upgrade_service import assert_database_current

    assert_database_current()


async def close_database() -> None:
    """Release every pooled connection during process shutdown."""

    await engine.dispose()


def database_runtime_summary() -> dict[str, object]:
    """Return restart-bound pool policy without exposing credentials."""

    return database_configuration.summary()
