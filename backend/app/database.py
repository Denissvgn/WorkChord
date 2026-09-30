from collections.abc import AsyncGenerator
from fastapi import Request

from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings
from app.database_config import parse_database_configuration
from app.observability import install_database_instrumentation

settings = get_settings()
database_configuration = parse_database_configuration(settings)

engine = create_async_engine(
    database_configuration.async_url,
    **database_configuration.async_engine_kwargs(echo=settings.debug),
)
install_database_instrumentation(engine)

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


async def request_command_mode(request: Request) -> str:
    """Match DTO preview defaults before creating the root transaction."""
    if request.url.path.endswith("/schedule/preview"):
        return "preview"
    if request.method == "POST" and request.url.path.endswith(("/bulk-operations", "/import-legacy")):
        from pydantic import TypeAdapter, ValidationError
        payload = await request.json()
        if isinstance(payload, dict):
            try:
                if TypeAdapter(bool).validate_python(payload.get("dry_run", True)):
                    return "preview"
            except ValidationError:
                pass  # Normal request-body validation reports the invalid field.
    return "apply"


async def get_db(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """Own each HTTP transaction before its response is sent (function-scoped dependency)."""
    from app.commands import command_transaction
    mode = await request_command_mode(request)
    async with async_session_maker() as session:
        async with command_transaction(session, mode=mode):
            yield session


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
