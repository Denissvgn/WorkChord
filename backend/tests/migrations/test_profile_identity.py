"""Person lifetime migration retains history and never rewinds numeric identities."""

from datetime import UTC, datetime, date
from uuid import UUID

from alembic import command
import pytest
from sqlalchemy import create_engine, MetaData, Table, select
from sqlalchemy.engine import make_url

from app.models.calendar import Calendar
from app.models.identity import Principal, CommandAudit
from app.models.iteration import Iteration
from app.models.recovery import ApplicationSnapshot
from app.models.team_member import TeamMemberProfile
from app.services.upgrade_service import alembic_config


@pytest.mark.parametrize("dialect", [pytest.param("sqlite", marks=pytest.mark.sqlite),
    pytest.param("postgresql", marks=[pytest.mark.postgresql, pytest.mark.allow_network])])
def test_profile_history_floor_lifetime_backfill_and_nonreuse(dialect, request, tmp_path, configure_database):
    url = f"sqlite+aiosqlite:///{tmp_path / 'person.db'}"
    if dialect == "postgresql":url = request.getfixturevalue("postgres_database").url
    configure_database(url)
    command.upgrade(alembic_config(), "20261009_0010")
    engine = create_engine(make_url(url).set(drivername="sqlite" if dialect == "sqlite" else "postgresql+psycopg"))
    try:
        legacy = Table("team_member_profiles", MetaData(), autoload_with=engine)
        with engine.begin() as db:
            db.execute(legacy.insert().values(id=2, display_name="Live person", automation_enabled=True,
                profile_kind="human", assignment_modes=[], created_at=datetime(2026, 1, 1, tzinfo=UTC), updated_at=datetime(2026, 1, 1, tzinfo=UTC)))
            db.execute(Calendar.__table__.insert().values(id=1, name="Calendar", year=2026))
            db.execute(Iteration.__table__.insert().values(id=1, name="Plan", calendar_id=1,
                start_date=date(2026, 1, 1), end_date=date(2026, 1, 31)))
            db.execute(Principal.__table__.insert().values(id=1, kind="human", display_name="Owner"))
            db.execute(CommandAudit.__table__.insert().values(principal_id=1, action="team_member_profiles:edit",
                source="rest", correlation_id="retained-person", details={"entity_id": 901}))
            db.execute(ApplicationSnapshot.__table__.insert().values(iteration_id=1, filename="person.json",
                schema_version=2, input_revision=1, payload={"team_members": [{"id": 3, "profile_id": 900}]}, checksum="a" * 64))
        command.upgrade(alembic_config(), "head")
        with engine.begin() as db:
            token = db.scalar(select(TeamMemberProfile.profile_token).where(TeamMemberProfile.id == 2))
            assert str(UUID(token)) == token
            assert db.scalar(select(TeamMemberProfile.display_name).where(TeamMemberProfile.id == 2)) == "Live person"
            assert db.execute(select(ApplicationSnapshot.payload, ApplicationSnapshot.checksum)).one() == ({"team_members": [{"id": 3, "profile_id": 900}]}, "a" * 64)
            created = db.execute(TeamMemberProfile.__table__.insert().values(display_name="New person")).inserted_primary_key[0]
            assert created > 901
            db.execute(TeamMemberProfile.__table__.delete().where(TeamMemberProfile.id == created))
            assert db.execute(TeamMemberProfile.__table__.insert().values(display_name="Next person")).inserted_primary_key[0] > created
        command.upgrade(alembic_config(), "head")
        with engine.connect() as db:
            assert db.scalar(select(TeamMemberProfile.profile_token).where(TeamMemberProfile.id == 2)) == token
            if dialect == "sqlite":assert not db.exec_driver_sql("PRAGMA foreign_key_check").all()
    finally:
        engine.dispose()
