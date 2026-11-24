"""Dated capacity adjustments migrate reversibly and keep existing capacity rows unchanged."""

from datetime import date, datetime, timezone

import pytest
from alembic import command
from sqlalchemy import create_engine, event, inspect, select

from app.models.calendar import Calendar
from app.models.iteration import Iteration
from app.models.team_member import TeamMember, TeamMemberCapacityAdjustment
from app.services.upgrade_service import alembic_config

PREVIOUS, CURRENT = "20261124_0021", "20261124_0022"


@pytest.mark.parametrize(
    "dialect",
    [
        pytest.param("sqlite", marks=pytest.mark.sqlite),
        pytest.param(
            "postgresql", marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network]
        ),
    ],
)
def test_adjustment_migration_preserves_rows_and_refuses_losing_active_adjustments(
    dialect, request, tmp_path, configure_database
):
    if dialect == "postgresql":
        url = request.getfixturevalue("postgres_database").url
        configure_database(url)
    else:
        path = tmp_path / "workchord_test_capacity_adjustment_upgrade.db"
        configure_database(f"sqlite+aiosqlite:///{path}")
        url = f"sqlite:///{path}"
    engine = create_engine(url)
    adjustments = TeamMemberCapacityAdjustment.__table__
    try:
        with engine.connect() as db:
            config = alembic_config(connection=db)
            command.upgrade(config, PREVIOUS)
            calendar = db.execute(Calendar.__table__.insert().values(name="Annual 2027", year=2027)).inserted_primary_key[0]
            iteration = db.execute(Iteration.__table__.insert().values(
                name="Existing iteration", calendar_id=calendar, start_date=date(2027, 1, 4),
                end_date=date(2027, 1, 15), revision=4)).inserted_primary_key[0]
            member = db.execute(TeamMember.__table__.insert().values(
                name="Existing row", position="Engineer", iteration_id=iteration, availability_percent=60,
                allocation_token="00000000-0000-4000-8000-000000000001")).inserted_primary_key[0]
            db.commit()
            for attempt in range(2):
                command.upgrade(config, CURRENT)
                assert db.execute(select(adjustments)).all() == []
                assert db.execute(select(TeamMember.__table__.c.availability_percent)).scalar_one() == 60
                assert db.execute(select(Iteration.__table__.c.revision)).scalar_one() == 4
                checks = {check["name"] for check in inspect(db).get_check_constraints("team_member_capacity_adjustments")}
                assert {"ck_team_member_capacity_adjustments_dates", "ck_team_member_capacity_adjustments_percent"} <= checks
                db.execute(adjustments.insert().values(
                    team_member_id=member, start_date=date(2027, 1, 4), end_date=date(2027, 1, 5),
                    availability_percent=0, base_availability_percent=60, reason="Lend two days",
                    group_token="00000000-0000-4000-8000-000000000002", created_at=datetime(2026, 11, 24, tzinfo=timezone.utc)))
                db.commit()
                with pytest.raises(RuntimeError, match="Withdraw active capacity adjustments"):
                    command.downgrade(config, PREVIOUS)
                db.rollback()
                assert len(db.execute(select(adjustments)).all()) == 1
                db.execute(adjustments.update().values(withdrawn_at=datetime(2026, 11, 25, tzinfo=timezone.utc)))
                db.commit()
                if attempt == 0:
                    command.downgrade(config, PREVIOUS)
                    assert not inspect(db).has_table("team_member_capacity_adjustments")
                    assert db.execute(select(TeamMember.__table__.c.availability_percent)).scalar_one() == 60
                    db.commit()
    finally:
        engine.dispose()
    # The adjustment belongs to its row and is removed with it.
    engine = create_engine(url)
    if dialect == "sqlite":
        event.listen(engine, "connect", lambda connection, _: connection.execute("PRAGMA foreign_keys=ON"))
    try:
        with engine.connect() as db:
            db.execute(TeamMember.__table__.delete())
            db.commit()
            assert db.execute(select(adjustments)).all() == []
    finally:
        engine.dispose()
