"""Existing projects start refusing inconsistent routing, and the setting round-trips a downgrade."""

import pytest
from alembic import command
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError

from app.services.upgrade_service import alembic_config

CURRENT = "20261127_0033"


@pytest.mark.parametrize(
    "dialect",
    [
        pytest.param("sqlite", marks=pytest.mark.sqlite),
        pytest.param(
            "postgresql", marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network]
        ),
    ],
)
def test_upgrade_defaults_existing_projects_to_refuse_and_downgrade_removes_the_setting(
    dialect, request, tmp_path, configure_database
):
    if dialect == "postgresql":
        url = request.getfixturevalue("postgres_database").url
        configure_database(url)
    else:
        path = tmp_path / "workchord_test_routing_conflict_mode.db"
        configure_database(f"sqlite+aiosqlite:///{path}")
        url = f"sqlite:///{path}"
    engine = create_engine(url)
    try:
        with engine.connect() as db:
            config = alembic_config(connection=db)
            previous = ScriptDirectory.from_config(config).get_revision(CURRENT).down_revision
            command.upgrade(config, previous)
            db.execute(text("INSERT INTO projects (name, timezone, status, health, sort_order, created_at, updated_at)"
                            " VALUES ('Existing', 'UTC', 'planned', 'unknown', 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"))
            db.commit()

            command.upgrade(config, CURRENT)
            assert db.execute(text("SELECT name, routing_conflict_mode FROM projects")).one() == ("Existing", "refuse")
            if dialect == "sqlite":
                assert "AUTOINCREMENT" in db.execute(text("SELECT sql FROM sqlite_master WHERE name = 'projects'")).scalar_one()
            db.execute(text("UPDATE projects SET routing_conflict_mode = 'warn'"))
            db.commit()
            with pytest.raises(IntegrityError):
                db.execute(text("UPDATE projects SET routing_conflict_mode = 'ignore'"))
            db.rollback()

            command.downgrade(config, previous)
            assert "routing_conflict_mode" not in {column["name"] for column in inspect(db).get_columns("projects")}
            assert db.execute(text("SELECT name FROM projects")).scalar_one() == "Existing"
            if dialect == "sqlite":
                assert "AUTOINCREMENT" in db.execute(text("SELECT sql FROM sqlite_master WHERE name = 'projects'")).scalar_one()
            db.commit()
            command.upgrade(config, CURRENT)
            assert db.execute(text("SELECT routing_conflict_mode FROM projects")).scalar_one() == "refuse"
    finally:
        engine.dispose()
