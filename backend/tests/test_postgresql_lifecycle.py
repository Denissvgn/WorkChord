"""Real-server smoke for create, migrate, exercise, and drop lifecycle."""

from __future__ import annotations

from pathlib import Path

from alembic import command
from alembic.config import Config
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool


MIGRATIONS = Path(__file__).parent / "fixtures/postgresql_migrations"


@pytest.mark.postgresql
@pytest.mark.integration
@pytest.mark.destructive
@pytest.mark.allow_network
def test_postgresql_database_lifecycle_from_empty_database(postgres_database) -> None:
    config = Config()
    config.set_main_option("script_location", str(MIGRATIONS))
    config.set_main_option("sqlalchemy.url", postgres_database.url)
    command.upgrade(config, "head")

    engine = create_engine(postgres_database.url, poolclass=NullPool)
    try:
        with engine.begin() as connection:
            assert connection.execute(text("SELECT count(*) FROM alembic_version")).scalar_one() == 1
            connection.execute(
                text(
                    "INSERT INTO wave0_database_probe (id, value) "
                    "VALUES (1, 'postgresql-real-server')"
                )
            )
        with engine.connect() as connection:
            assert connection.execute(
                text("SELECT value FROM wave0_database_probe WHERE id = 1")
            ).scalar_one() == "postgresql-real-server"
            assert connection.execute(text("SHOW timezone")).scalar_one() in {
                "UTC",
                "Etc/UTC",
            }
            assert connection.execute(text("SHOW search_path")).scalar_one().replace(
                " ", ""
            ) == "workchord,pg_catalog"
    finally:
        engine.dispose()

