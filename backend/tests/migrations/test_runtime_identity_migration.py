"""The runtime instance columns migrate reversibly and are never dropped silently."""

from datetime import datetime, timezone

import pytest
from alembic import command
from sqlalchemy import create_engine, inspect, select

from app.models.agent import AgentTeamTopology, AgentTeamTopologyMember
from app.services.upgrade_service import alembic_config

PREVIOUS, CURRENT = "20261124_0024", "20261126_0025"
COLUMNS = {
    "acknowledged_runtime_instance_id",
    "previous_runtime_instance_id",
    "runtime_identity_changed_at",
    "rejected_runtime_instance_id",
    "rejected_runtime_instance_at",
}


def filled(table, **values):
    """One row with a placeholder for every column that must be set, and the given values."""
    placeholders = {"integer": 1, "string": "x", "text": "x", "utcdatetime": datetime.now(timezone.utc)}
    row = {
        column.name: placeholders[type(column.type).__name__.lower()]
        for column in table.columns
        if not column.nullable and column.default is None and column.server_default is None
    }
    return {**row, **values, "id": 1}


@pytest.mark.parametrize(
    "dialect",
    [
        pytest.param("sqlite", marks=pytest.mark.sqlite),
        pytest.param(
            "postgresql", marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network]
        ),
    ],
)
def test_runtime_identity_migration_reads_as_unknown_and_refuses_losing_an_identity(
    dialect, request, tmp_path, configure_database
):
    if dialect == "postgresql":
        url = request.getfixturevalue("postgres_database").url
        configure_database(url)
    else:
        path = tmp_path / "workchord_test_runtime_identity.db"
        configure_database(f"sqlite+aiosqlite:///{path}")
        url = f"sqlite:///{path}"
    engine = create_engine(url)
    members, topologies = AgentTeamTopologyMember.__table__, AgentTeamTopology.__table__
    try:
        with engine.connect() as db:
            config = alembic_config(connection=db)
            command.upgrade(config, PREVIOUS)
            assert not COLUMNS & {column["name"] for column in inspect(db).get_columns(members.name)}
            command.upgrade(config, CURRENT)
            assert COLUMNS <= {column["name"] for column in inspect(db).get_columns(members.name)}
            assert db.execute(select(members.c.id)).scalars().all() == []
            db.commit()
            db.execute(topologies.insert().values(**filled(topologies)))
            db.execute(
                members.insert().values(
                    **filled(members, role="worker", acknowledged_runtime_instance_id="rti-" + "a" * 32)
                )
            )
            db.commit()
            with pytest.raises(RuntimeError, match="clear them before downgrading"):
                command.downgrade(config, PREVIOUS)
            db.rollback()
            db.execute(members.update().values(acknowledged_runtime_instance_id=None))
            db.commit()
            command.downgrade(config, PREVIOUS)
            assert not COLUMNS & {column["name"] for column in inspect(db).get_columns(members.name)}
            assert db.execute(select(members.c.id)).scalars().all() == [1]
            command.upgrade(config, CURRENT)
            assert db.execute(select(members.c.acknowledged_runtime_instance_id)).scalars().all() == [None]
    finally:
        engine.dispose()
