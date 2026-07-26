"""Dual-dialect Boolean/JSON/time/constraint/RETURNING behavior matrix."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from cryptography.fernet import Fernet
import pytest
from sqlalchemy import create_engine, event, insert, inspect, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.pool import NullPool

from app.models.agent import AgentActor
from app.models.saved_view import SavedView
from app.models.system_settings import SystemSetting
from app.models.user_session import UserSession
from app.services.upgrade_service import bootstrap_database_schema
from app.utils.time import utc_now


def behavior_engine(database_url: str, *, sqlite: bool):
    engine = create_engine(database_url, poolclass=NullPool)
    if sqlite:

        @event.listens_for(engine, "connect")
        def enable_foreign_keys(dbapi_connection, _connection_record) -> None:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return engine


def exercise_schema_behavior(engine) -> None:
    encrypted_value = Fernet(Fernet.generate_key()).encrypt(
        "database-matrix-secret".encode()
    ).decode()
    revoked_at = datetime(2026, 7, 18, 10, 30, tzinfo=UTC)

    with Session(engine) as session:
        actor = AgentActor(
            name="matrix-agent",
            display_name="Matrix Agent 東京",
            api_key_hash="a" * 64,
            scopes='["tasks:read", "unicode:Бета"]',
            enabled=False,
        )
        json_setting = SystemSetting(
            key="qa.unicode",
            category="qa",
            value_json={"labels": ["Alpha", "Бета", "東京"], "enabled": True},
            is_secret=False,
        )
        secret_setting = SystemSetting(
            key="qa.secret",
            category="qa",
            secret_ciphertext=encrypted_value,
            is_secret=True,
        )
        anonymous_one = UserSession(
            public_id="matrixpublic01",
            session_token_hash=None,
            ip_address="192.0.2.10",
        )
        anonymous_two = UserSession(
            public_id="matrixpublic02",
            session_token_hash=None,
            ip_address="192.0.2.11",
            revoked_at=revoked_at,
        )
        token_owner = UserSession(
            public_id="matrixpublic03",
            session_token_hash="b" * 64,
            ip_address="192.0.2.12",
        )
        session.add_all(
            [
                actor,
                json_setting,
                secret_setting,
                anonymous_one,
                anonymous_two,
                token_owner,
            ]
        )
        session.commit()

        assert session.get(AgentActor, actor.id).enabled is False
        assert session.get(AgentActor, actor.id).scopes == actor.scopes
        assert session.get(SystemSetting, json_setting.id).value_json == {
            "labels": ["Alpha", "Бета", "東京"],
            "enabled": True,
        }
        assert (
            session.get(SystemSetting, secret_setting.id).secret_ciphertext
            == encrypted_value
        )
        assert session.get(UserSession, anonymous_one.id).created_at.tzinfo == UTC
        assert session.get(UserSession, anonymous_two.id).revoked_at == revoked_at

        ordered_ids = session.scalars(
            select(UserSession.id).order_by(
                UserSession.revoked_at.asc().nulls_last(),
                UserSession.id,
            )
        ).all()
        assert ordered_ids[0] == anonymous_two.id
        assert set(ordered_ids[1:]) == {anonymous_one.id, token_owner.id}

        returned_id = session.execute(
            insert(SystemSetting)
            .values(
                key="qa.returning",
                category="qa",
                value_json=["RETURNING", "✓"],
                secret_ciphertext=None,
                is_secret=False,
                created_at=utc_now(),
                updated_at=utc_now(),
            )
            .returning(SystemSetting.id)
        ).scalar_one()
        session.commit()
        assert isinstance(returned_id, int)

    with Session(engine) as session:
        session.add(
            UserSession(
                public_id="matrixpublic04",
                session_token_hash="b" * 64,
                ip_address="192.0.2.13",
            )
        )
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

    with engine.connect() as connection:
        transaction = connection.begin()
        with pytest.raises(IntegrityError):
            connection.execute(
                insert(SavedView).values(
                    name="Foreign key probe",
                    view_type="tasks",
                    scope="personal",
                    created_by_session_id=999_999,
                    filters_json={},
                    sort_json={},
                    columns_json={},
                    schema_version=1,
                    created_at=utc_now(),
                    updated_at=utc_now(),
                )
            )
        transaction.rollback()

    with Session(engine) as session:
        session.add(
            AgentActor(
                name="invalid-policy-agent",
                display_name="Invalid policy",
                api_key_hash="c" * 64,
                scopes="[]",
                enabled=True,
                work_policy="unrestricted",
            )
        )
        with pytest.raises(IntegrityError):
            session.commit()
        session.rollback()

    inspector = inspect(engine)
    partial_index_names = {
        index["name"]
        for table_name in (
            "agent_task_assignments",
            "agent_runs",
            "agent_run_events",
            "task_events",
            "agent_model_bindings",
        )
        for index in inspector.get_indexes(table_name)
    }
    assert {
        "uq_agent_task_assignments_live_purpose",
        "uq_agent_runs_running_assignment",
        "uq_agent_run_events_run_id_idempotency_key",
        "uq_task_events_agent_idempotency_key",
        "uq_agent_model_bindings_default_enabled",
    }.issubset(partial_index_names)


@pytest.mark.sqlite
def test_sqlite_schema_behavior_matrix(tmp_path: Path, configure_database) -> None:
    path = tmp_path / "behavior.db"
    configure_database(f"sqlite+aiosqlite:///{path}")
    bootstrap_database_schema()
    engine = behavior_engine(f"sqlite:///{path}", sqlite=True)
    try:
        exercise_schema_behavior(engine)
    finally:
        engine.dispose()


@pytest.mark.postgresql
@pytest.mark.integration
@pytest.mark.allow_network
def test_postgresql_schema_behavior_matrix(
    postgres_database,
    configure_database,
) -> None:
    configure_database(postgres_database.url)
    bootstrap_database_schema()
    engine = behavior_engine(postgres_database.url, sqlite=False)
    try:
        exercise_schema_behavior(engine)
    finally:
        engine.dispose()
