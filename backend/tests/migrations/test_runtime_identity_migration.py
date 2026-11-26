"""The runtime instance columns migrate reversibly and are never dropped silently."""

import re
from datetime import datetime, timezone

import pytest
import sqlalchemy as sa
from alembic import command
from sqlalchemy import create_engine, inspect, select

from app.models.agent import AgentTeamTopology, AgentTeamTopologyMember
from app.services.upgrade_service import alembic_config

PREVIOUS, CURRENT = "20261126_0027", "20261126_0028"
COLUMNS = {
    "issued_runtime_instance_id",
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
    return {"id": 1, **row, **values}


def written_before(table, **values):
    """A row as the earlier schema holds it: every required column, with its default, and none of the new ones."""
    row = filled(table, **values)
    for column in table.columns:
        if column.name in COLUMNS or column.name in row or column.nullable:
            continue
        if column.default is not None:
            row[column.name] = column.default.arg(None) if callable(column.default.arg) else column.default.arg
    return {name: value for name, value in row.items() if name not in COLUMNS}


@pytest.mark.parametrize(
    "dialect",
    [
        pytest.param("sqlite", marks=pytest.mark.sqlite),
        pytest.param(
            "postgresql", marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network]
        ),
    ],
)
def test_runtime_identity_migration_issues_random_identities_and_refuses_losing_an_identity(
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
            db.execute(topologies.insert().values(**filled(topologies)))
            # Members that exist before the upgrade are written with only the columns that existed then.
            for member_id in (1, 2):
                row = written_before(members, id=member_id, role="worker", actor_key=f"worker-{member_id}",
                                     runtime_ref=f"runtime-{member_id}", credential_ref=f"credential-{member_id}")
                db.execute(sa.table(members.name, *(sa.column(name) for name in row)).insert().values(**row))
            db.commit()
            command.upgrade(config, CURRENT)
            assert COLUMNS <= {column["name"] for column in inspect(db).get_columns(members.name)}
            issued = db.execute(select(members.c.issued_runtime_instance_id).order_by(members.c.id)).scalars().all()
            # Each existing member is issued its own random identity; none is acknowledged, changed or refused.
            assert all(re.fullmatch(r"rti-[0-9a-f]{32}", value) for value in issued) and len(set(issued)) == 2
            untouched = COLUMNS - {"issued_runtime_instance_id"}
            assert db.execute(select(*(members.c[name] for name in untouched))).all() == [(None,) * len(untouched)] * 2
            db.commit()
            db.execute(members.update().where(members.c.id == 1).values(acknowledged_runtime_instance_id="rti-" + "a" * 32))
            db.commit()
            with pytest.raises(RuntimeError, match="clear them before downgrading"):
                command.downgrade(config, PREVIOUS)
            db.rollback()
            db.execute(members.update().values(acknowledged_runtime_instance_id=None))
            db.commit()
            command.downgrade(config, PREVIOUS)
            assert not COLUMNS & {column["name"] for column in inspect(db).get_columns(members.name)}
            assert db.execute(select(members.c.id).order_by(members.c.id)).scalars().all() == [1, 2]
            command.upgrade(config, CURRENT)
            reissued = db.execute(select(members.c.issued_runtime_instance_id).order_by(members.c.id)).scalars().all()
            assert all(value is not None for value in reissued) and len(set(reissued)) == 2
    finally:
        engine.dispose()
