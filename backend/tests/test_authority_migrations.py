"""Additive authority upgrades preserve legacy attribution and empty transfer targets."""

from datetime import date, timedelta

from alembic import command
import pytest
from sqlalchemy import MetaData, create_engine, event, inspect, select, text
from sqlalchemy.engine import make_url
from sqlalchemy.exc import IntegrityError

from app.database_migration.catalog import transfer_tables
from app.services.upgrade_service import alembic_config
from app.utils.time import utc_now


@pytest.fixture(params=[pytest.param("sqlite", marks=pytest.mark.sqlite),
                       pytest.param("postgresql", marks=[pytest.mark.postgresql, pytest.mark.allow_network])])
def legacy_authority_database(request, tmp_path, configure_database):
    url = f"sqlite+aiosqlite:///{tmp_path / 'workchord_test_authority.db'}"
    if request.param == "postgresql":
        url = request.getfixturevalue("postgres_database").url
    configure_database(url)
    config = alembic_config()
    command.upgrade(config, "20260802_0036")
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


def test_authority_upgrade_preserves_guest_ids_and_does_not_invent_humans(legacy_authority_database):
    config, engine = legacy_authority_database
    legacy = MetaData()
    legacy.reflect(engine)
    now = utc_now()
    with engine.begin() as connection:
        connection.execute(legacy.tables["agent_actors"].insert().values(id=21, name="legacy-agent", display_name="Same name", api_key_hash="a" * 64,
            scopes='["tasks:read"]', enabled=False, role="worker", lifecycle_state="active", work_policy="assigned_only", max_parallel_work=1, queue_revision=1, created_at=now))
        connection.execute(legacy.tables["user_sessions"].insert().values(id=31, public_id="legacyguest31", session_token_hash="b" * 64,
            ip_address="192.0.2.1", user_agent="legacy-browser", created_at=now, last_seen_at=now, expires_at=now + timedelta(days=1)))
        connection.execute(legacy.tables["saved_views"].insert().values(id=41, name="Existing personal view", view_type="tasks", scope="personal",
            created_by_session_id=31, filters_json={"isOverdue": True}, sort_json={}, columns_json={}, schema_version=1, created_at=now, updated_at=now))
    command.upgrade(config, "head")
    current = MetaData()
    current.reflect(engine)
    with engine.connect() as connection:
        principals = connection.execute(select(current.tables["principals"])).mappings().all()
        assert [(row["kind"], row["agent_actor_id"]) for row in principals] == [("agent", 21)]
        assert principals[0]["enabled"] is True
        assert connection.execute(select(current.tables["agent_actors"].c.enabled).where(current.tables["agent_actors"].c.id == 21)).scalar_one() is False
        session = connection.execute(select(current.tables["user_sessions"]).where(current.tables["user_sessions"].c.id == 31)).mappings().one()
        assert session["principal_id"] is None
        assert session["public_id"] == "legacyguest31"
        view = connection.execute(select(current.tables["saved_views"]).where(current.tables["saved_views"].c.id == 41)).mappings().one()
        assert view["created_by_session_id"] == 31 and view["owner_principal_id"] is None
        assert view["filters_json"]["isIterationOverflow"] is True and view["filters_json"]["isOverdue"] is None
        assert view["metric_migration_note"] == "legacy_overdue_means_iteration_overflow"
    with engine.connect() as connection:
        transaction = connection.begin()
        with pytest.raises(IntegrityError):
            connection.execute(current.tables["user_sessions"].update().where(current.tables["user_sessions"].c.id == 31).values(principal_id=999999))
        transaction.rollback()


def test_schema_only_target_remains_empty_for_catalogued_transfer(legacy_authority_database):
    config, engine = legacy_authority_database
    command.upgrade(config, "head")
    with engine.connect() as connection:
        assert all(connection.execute(select(table).limit(1)).first() is None for table in transfer_tables().values())
    assert {"application_snapshots", "principals", "identity_subjects", "ownership_transfers"}.issubset(transfer_tables())


def test_new_foreign_keys_and_uniqueness_are_declared(legacy_authority_database):
    config, engine = legacy_authority_database
    command.upgrade(config, "head")
    inspector = inspect(engine)
    assert any(key["referred_table"] == "principals" for key in inspector.get_foreign_keys("user_sessions"))
    assert any(set(key["column_names"]) == {"issuer", "subject"} for key in inspector.get_unique_constraints("identity_subjects"))
