"""Forward allocation identity migration preserves history and sequence high water."""

from datetime import date
from uuid import UUID

from alembic import command
import pytest
from sqlalchemy import create_engine, MetaData, Table, select, text
from sqlalchemy.engine import make_url

from app.models.calendar import Calendar
from app.models.identity import Principal, CommandAudit
from app.models.iteration import Iteration
from app.models.recovery import ApplicationSnapshot
from app.models.team_member import TeamMember
from app.services.upgrade_service import alembic_config


@pytest.mark.parametrize("dialect", [pytest.param("sqlite", marks=pytest.mark.sqlite),
    pytest.param("postgresql", marks=[pytest.mark.postgresql, pytest.mark.allow_network])])
def test_lifetimes_backfill_and_retained_ids_are_never_reallocated(dialect, request, tmp_path, configure_database):
    url = f"sqlite+aiosqlite:///{tmp_path / 'allocation.db'}"
    if dialect == "postgresql":url = request.getfixturevalue("postgres_database").url
    configure_database(url)
    command.upgrade(alembic_config(), "20261008_0009")
    engine = create_engine(make_url(url).set(drivername="sqlite" if dialect == "sqlite" else "postgresql+psycopg"))
    try:
        legacy = Table("team_members", MetaData(), autoload_with=engine)
        with engine.begin() as db:
            db.execute(Calendar.__table__.insert().values(id=1, name="Calendar", year=2026))
            db.execute(Iteration.__table__.insert().values(id=1, name="Plan", calendar_id=1,
                start_date=date(2026, 1, 1), end_date=date(2026, 1, 31)))
            db.execute(legacy.insert().values(id=2, name="Live allocation", position="Engineer", iteration_id=1, availability_percent=100, professionalism_coefficient=1, operational_utilization=20))
            db.execute(Principal.__table__.insert().values(id=1, kind="human", display_name="Owner"))
            db.execute(CommandAudit.__table__.insert().values(principal_id=1, action="team_members:edit",
                source="rest", correlation_id="retained-allocation", details={"entity_id": 901}))
            db.execute(ApplicationSnapshot.__table__.insert().values(iteration_id=1, filename="retained.json",
                schema_version=2, input_revision=1, payload={"team_members": [{"id": 900}]}, checksum="a" * 64))
        command.upgrade(alembic_config(), "head")
        with engine.begin() as db:
            live = db.execute(select(TeamMember.__table__).where(TeamMember.id == 2)).mappings().one()
            assert str(UUID(live["allocation_token"])) == live["allocation_token"]
            assert (live["name"], live["iteration_id"]) == ("Live allocation", 1)
            snapshot = db.execute(select(ApplicationSnapshot.payload, ApplicationSnapshot.checksum)).one()
            assert snapshot == ({"team_members": [{"id": 900}]}, "a" * 64)
            created = db.execute(TeamMember.__table__.insert().values(name="New allocation", position="Engineer")).inserted_primary_key[0]
            assert created > 901
            db.execute(TeamMember.__table__.delete().where(TeamMember.id == created))
            assert db.execute(TeamMember.__table__.insert().values(name="Next allocation", position="Engineer")).inserted_primary_key[0] > created
        command.upgrade(alembic_config(), "head")
        with engine.connect() as db:
            assert db.scalar(select(TeamMember.allocation_token).where(TeamMember.id == 2)) == live["allocation_token"]
            if dialect == "sqlite":assert db.exec_driver_sql("PRAGMA foreign_key_check").all() == []
    finally:
        engine.dispose()
