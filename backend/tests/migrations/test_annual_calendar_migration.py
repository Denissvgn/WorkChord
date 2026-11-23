"""Annual selections are explicit and reversibly migrate from the actual predecessor."""

from datetime import date

import pytest
from alembic import command
from sqlalchemy import create_engine, inspect, select

from app.models.calendar import Calendar, iteration_annual_calendars, profile_annual_calendars
from app.models.iteration import Iteration
from app.models.team_member import TeamMemberProfile
from app.models.capacity import ProfileAvailability
from app.services.upgrade_service import alembic_config


@pytest.mark.parametrize(
    "dialect",
    [
        pytest.param("sqlite", marks=pytest.mark.sqlite),
        pytest.param(
            "postgresql", marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network]
        ),
    ],
)
def test_annual_migration_preserves_existing_owners_and_refuses_loss(
    dialect, request, tmp_path, configure_database
):
    if dialect == "postgresql":
        url = request.getfixturevalue("postgres_database").url
        configure_database(url)
    else:
        path = tmp_path / "workchord_test_calendar_upgrade.db"
        configure_database(f"sqlite+aiosqlite:///{path}")
        url = f"sqlite:///{path}"
    engine = create_engine(url)
    try:
        with engine.connect() as db:
            config = alembic_config(connection=db)
            command.upgrade(config, "20261121_0019")
            primary, following = [
                db.execute(
                    Calendar.__table__.insert().values(name=f"Annual {year}", year=year)
                ).inserted_primary_key[0]
                for year in (2026, 2027)
            ]
            iteration = db.execute(
                Iteration.__table__.insert().values(
                    name="Existing winter iteration",
                    calendar_id=primary,
                    start_date=date(2026, 12, 23),
                    end_date=date(2027, 1, 5),
                    revision=9,
                )
            ).inserted_primary_key[0]
            owner = db.execute(
                TeamMemberProfile.__table__.insert().values(display_name="Existing owner")
            ).inserted_primary_key[0]
            db.execute(
                ProfileAvailability.__table__.insert().values(
                    profile_id=owner, calendar_id=primary, version=5
                )
            )
            db.commit()
            for attempt in range(2):
                command.upgrade(config, "20261121_0020")
                assert not db.execute(select(iteration_annual_calendars)).all()
                assert not db.execute(select(profile_annual_calendars)).all()
                assert db.execute(
                    select(Iteration.__table__.c.calendar_id, Iteration.__table__.c.revision)
                ).one() == (primary, 9)
                assert db.execute(
                    select(
                        ProfileAvailability.__table__.c.calendar_id, ProfileAvailability.__table__.c.version
                    )
                ).one() == (primary, 5)
                db.execute(
                    iteration_annual_calendars.insert().values(
                        iteration_id=iteration, calendar_id=following
                    )
                )
                db.execute(
                    profile_annual_calendars.insert().values(profile_id=owner, calendar_id=following)
                )
                db.commit()
                with pytest.raises(RuntimeError, match="clear additional"):
                    command.downgrade(config, "20261121_0019")
                db.rollback()
                assert db.execute(select(profile_annual_calendars)).one() == (owner, following)
                assert db.execute(select(iteration_annual_calendars)).one() == (iteration, following)
                if attempt == 0:
                    db.execute(profile_annual_calendars.delete())
                    db.execute(iteration_annual_calendars.delete())
                    db.commit()
                    command.downgrade(config, "20261121_0019")
                    assert not inspect(db).has_table("iteration_annual_calendars")
                    db.commit()
    finally:
        engine.dispose()
