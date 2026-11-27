"""The calibration contract upgrade adds governed tables and never drops a submitted contract."""

import pytest
from alembic import command
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError

from app.services.upgrade_service import alembic_config

CURRENT = "20261127_0032"
DIGEST = "a" * 64

_CONTRACT_ROW = text(
    "INSERT INTO routing_calibration_contracts (key, schema_version, state, revision, terms, terms_digest,"
    " submitted_by_actor_type, submitted_at, approved_by_actor_type, approved_at, approval_reason,"
    " created_at, updated_at)"
    " VALUES (:key, 'routing-calibration-contract-v1', :state, 1, '{}', :digest, 'operator', CURRENT_TIMESTAMP,"
    " :approved_by, :approved_at, :reason, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
)


def _row(key: str, *, state: str = "submitted", approved: bool = False, digest: str = DIGEST) -> dict:
    return {
        "key": key,
        "state": state,
        "digest": digest,
        "approved_by": "operator" if approved else None,
        "approved_at": "2026-11-27 10:00:00+00:00" if approved else None,
        "reason": "Approved after review." if approved else None,
    }


@pytest.mark.parametrize(
    "dialect",
    [
        pytest.param("sqlite", marks=pytest.mark.sqlite),
        pytest.param(
            "postgresql", marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network]
        ),
    ],
)
def test_upgrade_adds_contract_tables_and_downgrade_refuses_to_lose_a_contract(
    dialect, request, tmp_path, configure_database
):
    if dialect == "postgresql":
        url = request.getfixturevalue("postgres_database").url
        configure_database(url)
    else:
        path = tmp_path / "workchord_test_calibration_contracts_upgrade.db"
        configure_database(f"sqlite+aiosqlite:///{path}")
        url = f"sqlite:///{path}"
    engine = create_engine(url)
    try:
        with engine.connect() as db:
            config = alembic_config(connection=db)
            previous = ScriptDirectory.from_config(config).get_revision(CURRENT).down_revision
            assert previous == "20261127_0031"
            command.upgrade(config, previous)
            db.execute(
                text("INSERT INTO routing_qualification_keys (key, label, state, revision, created_at, updated_at)"
                     " VALUES ('qualified.schema-review', 'Schema review', 'active', 1, CURRENT_TIMESTAMP,"
                     " CURRENT_TIMESTAMP)")
            )
            db.commit()

            command.upgrade(config, CURRENT)
            tables = set(inspect(db).get_table_names())
            assert {"routing_calibration_contracts", "routing_calibration_contract_revisions"} <= tables
            # The registry the contracts name is untouched.
            assert db.execute(text("SELECT count(*) FROM routing_qualification_keys")).scalar_one() == 1

            db.execute(_CONTRACT_ROW, _row("default"))
            db.execute(_CONTRACT_ROW, _row("approved", state="approved", approved=True))
            db.commit()
            # The database keeps keys canonical, states governed and approvals complete.
            for values in (
                _row("Default.Other"),
                _row("paused", state="paused"),
                _row("half-approved", state="approved"),
                _row("submitted-with-approval", approved=True),
                _row("short-digest", digest="abc"),
            ):
                with pytest.raises(IntegrityError):
                    db.execute(_CONTRACT_ROW, values)
                db.rollback()

            with pytest.raises(RuntimeError, match="Downgrade is unsupported once a calibration contract"):
                command.downgrade(config, previous)
            db.rollback()
            db.execute(text("DELETE FROM routing_calibration_contracts"))
            db.commit()

            command.downgrade(config, previous)
            tables = set(inspect(db).get_table_names())
            assert "routing_calibration_contracts" not in tables
            assert "routing_calibration_contract_revisions" not in tables
            assert db.execute(text("SELECT count(*) FROM routing_qualification_keys")).scalar_one() == 1
    finally:
        engine.dispose()
