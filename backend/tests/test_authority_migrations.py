"""Initial authority schema, constraints and empty transfer targets."""

from alembic import command
import pytest
from sqlalchemy import create_engine, event, inspect, select
from sqlalchemy.engine import make_url

from app.database_migration.catalog import transfer_tables
from app.services.upgrade_service import alembic_config


@pytest.fixture(params=[pytest.param("sqlite", marks=pytest.mark.sqlite),
                       pytest.param("postgresql", marks=[pytest.mark.postgresql, pytest.mark.allow_network])])
def initial_database(request, tmp_path, configure_database):
    url = f"sqlite+aiosqlite:///{tmp_path / 'workchord_test_authority.db'}"
    if request.param == "postgresql":
        url = request.getfixturevalue("postgres_database").url
    configure_database(url)
    config = alembic_config()
    command.upgrade(config, "head")
    parsed = make_url(url)
    sync_url = parsed.set(drivername="sqlite" if request.param == "sqlite" else "postgresql+psycopg")
    engine = create_engine(sync_url)
    if request.param == "sqlite":
        @event.listens_for(engine, "connect")
        def foreign_keys(connection, _record):
            connection.execute("PRAGMA foreign_keys=ON")
    try:
        yield config, engine
    finally:
        engine.dispose()


def test_schema_only_target_remains_empty_for_catalogued_transfer(initial_database):
    config, engine = initial_database
    command.upgrade(config, "head")
    with engine.connect() as connection:
        assert all(connection.execute(select(table).limit(1)).first() is None for table in transfer_tables().values())
    assert {"application_snapshots", "principals", "identity_subjects", "ownership_transfers"}.issubset(transfer_tables())


def test_new_foreign_keys_and_uniqueness_are_declared(initial_database):
    config, engine = initial_database
    command.upgrade(config, "head")
    inspector = inspect(engine)
    assert any(key["referred_table"] == "principals" for key in inspector.get_foreign_keys("user_sessions"))
    assert any(set(key["column_names"]) == {"issuer", "subject"} for key in inspector.get_unique_constraints("identity_subjects"))
