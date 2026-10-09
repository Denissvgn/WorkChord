"""Preserve legacy absence identities and report conflicting person calendars."""

from datetime import UTC, date, datetime

from alembic import command
import pytest
from sqlalchemy import MetaData, Table, create_engine, select
from sqlalchemy.engine import make_url

from app.models.calendar import Calendar
from app.models.iteration import Iteration
from app.models.team_member import TeamMember, TeamMemberProfile, Vacation
from app.services.upgrade_service import alembic_config


@pytest.mark.parametrize("dialect", [pytest.param("sqlite", marks=pytest.mark.sqlite),
    pytest.param("postgresql", marks=[pytest.mark.postgresql, pytest.mark.allow_network])])
def test_legacy_backfill_retains_ids_deduplicates_and_reports_conflict(dialect, request, tmp_path, configure_database):
    url = f"sqlite+aiosqlite:///{tmp_path / 'availability.db'}"
    if dialect == "postgresql":
        url = request.getfixturevalue("postgres_database").url
    configure_database(url)
    config = alembic_config()
    command.upgrade(config, "20260928_0001")
    engine = create_engine(make_url(url).set(drivername="sqlite" if dialect == "sqlite" else "postgresql+psycopg"))
    try:
        legacy_profiles = Table("team_member_profiles", MetaData(), autoload_with=engine)
        legacy_members = Table("team_members", MetaData(), autoload_with=engine)
        with engine.begin() as connection:
            connection.execute(legacy_profiles.insert().values(id=1, display_name="Shared person", automation_enabled=True, profile_kind="human", assignment_modes=[], created_at=datetime(2026, 1, 1, tzinfo=UTC), updated_at=datetime(2026, 1, 1, tzinfo=UTC)))
            for number, hours in [(1, 8), (2, 6)]:
                connection.execute(Calendar.__table__.insert().values(id=number, name="Calendar", year=2026, nominal_day_hours=hours))
                connection.execute(Iteration.__table__.insert().values(id=number, name="Plan", calendar_id=number,
                    start_date=date(2026, 1, 1), end_date=date(2026, 12, 31)))
                connection.execute(legacy_members.insert().values(id=number, name="Person", position="Developer",
                    profile_id=1, iteration_id=number, availability_percent=100, professionalism_coefficient=1, operational_utilization=20))
                connection.execute(Vacation.__table__.insert().values(id=number, team_member_id=number,
                    start_date=date(2026, 10, 1), end_date=date(2026, 10, 2)))
        command.upgrade(config, "head")
        metadata = MetaData()
        absence = Table("profile_absences", metadata, autoload_with=engine)
        setting = Table("profile_availability", metadata, autoload_with=engine)
        vacation = Table("vacations", metadata, autoload_with=engine)
        with engine.connect() as connection:
            row = connection.execute(select(absence)).mappings().one()
            assert row["provenance"] == [{"legacy_vacation_ids": [1, 2]}]
            assert connection.execute(select(vacation.c.id, vacation.c.profile_absence_id).order_by(vacation.c.id)).all() == [(1, row["id"]), (2, row["id"])]
            availability = connection.execute(select(setting)).mappings().one()
            assert availability["calendar_id"] is None
            assert availability["calendar_conflicts"] == [1, 2]
        command.upgrade(config, "head")
        with engine.connect() as connection:
            assert len(connection.execute(select(absence)).all()) == 1
    finally:
        engine.dispose()
