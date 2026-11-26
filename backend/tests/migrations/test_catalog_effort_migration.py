"""Catalog effort upgrades a populated catalog to an explicit unknown value and is never dropped silently."""

import pytest
from alembic import command
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError

from app.models.agent import AgentActor, AgentModelBinding
from app.services.upgrade_service import alembic_config

CURRENT = "20261126_0029"

_CATALOG_ROW = text(
    "INSERT INTO agent_model_catalog_entries (key, provider, configured_model_alias, reasoning_tier,"
    " context_tier, modality_tags, cost_tier, latency_tier, enabled, revision, created_at, updated_at)"
    " VALUES (:key, 'provider', :alias, 2, 'medium', '[\"text\"]', 'medium', 'balanced', :enabled, 3,"
    " CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
)


@pytest.mark.parametrize(
    "dialect",
    [
        pytest.param("sqlite", marks=pytest.mark.sqlite),
        pytest.param(
            "postgresql", marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network]
        ),
    ],
)
def test_effort_upgrade_marks_existing_entries_unknown_and_refuses_losing_a_setting(
    dialect, request, tmp_path, configure_database
):
    if dialect == "postgresql":
        url = request.getfixturevalue("postgres_database").url
        configure_database(url)
    else:
        path = tmp_path / "workchord_test_catalog_effort_upgrade.db"
        configure_database(f"sqlite+aiosqlite:///{path}")
        url = f"sqlite:///{path}"
    engine = create_engine(url)
    actors, bindings = AgentActor.__table__, AgentModelBinding.__table__
    try:
        with engine.connect() as db:
            config = alembic_config(connection=db)
            previous = ScriptDirectory.from_config(config).get_revision(CURRENT).down_revision
            command.upgrade(config, previous)
            # Two entries for one runtime model, one disabled, one bound to an actor.
            db.execute(_CATALOG_ROW, {"key": "shared-model-a", "alias": "shared-runtime", "enabled": True})
            db.execute(_CATALOG_ROW, {"key": "shared-model-b", "alias": "shared-runtime", "enabled": False})
            actor = db.execute(
                actors.insert().values(name="effort-worker", display_name="Effort Worker", api_key_hash="effort-hash")
            ).inserted_primary_key[0]
            catalog_id = db.execute(
                text("SELECT id FROM agent_model_catalog_entries WHERE key = 'shared-model-a'")
            ).scalar_one()
            db.execute(bindings.insert().values(actor_id=actor, model_catalog_id=catalog_id, is_default=True))
            db.commit()

            command.upgrade(config, CURRENT)
            rows = db.execute(
                text("SELECT key, effort, revision FROM agent_model_catalog_entries ORDER BY key")
            ).all()
            assert [(row.key, row.effort, row.revision) for row in rows] == [
                ("shared-model-a", "unknown", 3),
                ("shared-model-b", "unknown", 3),
            ]
            assert db.execute(text("SELECT model_catalog_id FROM agent_model_bindings")).scalars().all() == [
                catalog_id
            ]

            # The database also refuses a value outside the vocabulary.
            with pytest.raises(IntegrityError):
                db.execute(text("UPDATE agent_model_catalog_entries SET effort = 'extreme' WHERE key = 'shared-model-a'"))
            db.rollback()
            db.execute(text("UPDATE agent_model_catalog_entries SET effort = 'high' WHERE key = 'shared-model-a'"))
            db.commit()

            with pytest.raises(RuntimeError, match="set them to unknown before downgrading"):
                command.downgrade(config, previous)
            db.rollback()
            db.execute(text("UPDATE agent_model_catalog_entries SET effort = 'unknown'"))
            db.commit()
            command.downgrade(config, previous)
            assert "effort" not in {
                column["name"] for column in inspect(db).get_columns("agent_model_catalog_entries")
            }
            assert db.execute(text("SELECT count(*) FROM agent_model_catalog_entries")).scalar_one() == 2
            assert db.execute(text("SELECT count(*) FROM agent_model_bindings")).scalar_one() == 1
    finally:
        engine.dispose()
