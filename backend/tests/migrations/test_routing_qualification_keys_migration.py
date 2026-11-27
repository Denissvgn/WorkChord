"""The qualification key upgrade keeps a populated catalog and never drops declared keys silently."""

import json

import pytest
from alembic import command
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError

from app.models.agent import AgentActor, AgentModelBinding
from app.services.upgrade_service import alembic_config

CURRENT = "20261127_0031"

_CATALOG_ROW = text(
    "INSERT INTO agent_model_catalog_entries (key, provider, configured_model_alias, reasoning_tier, effort,"
    " context_tier, modality_tags, cost_tier, latency_tier, enabled, revision, created_at, updated_at)"
    " VALUES (:key, 'provider', 'shared-runtime', 2, :effort, 'medium', '[\"text\"]', 'medium', 'balanced',"
    " :enabled, 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
)
_KEY_ROW = text(
    "INSERT INTO routing_qualification_keys (key, label, state, revision, created_at, updated_at)"
    " VALUES (:key, 'Schema review', 'active', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)"
)


def _decoded(value):
    return json.loads(value) if isinstance(value, str) else value


@pytest.mark.parametrize(
    "dialect",
    [
        pytest.param("sqlite", marks=pytest.mark.sqlite),
        pytest.param(
            "postgresql", marks=[pytest.mark.postgresql, pytest.mark.integration, pytest.mark.allow_network]
        ),
    ],
)
def test_upgrade_gives_existing_entries_no_keys_and_downgrade_refuses_to_lose_them(
    dialect, request, tmp_path, configure_database
):
    if dialect == "postgresql":
        url = request.getfixturevalue("postgres_database").url
        configure_database(url)
    else:
        path = tmp_path / "workchord_test_qualification_keys_upgrade.db"
        configure_database(f"sqlite+aiosqlite:///{path}")
        url = f"sqlite:///{path}"
    engine = create_engine(url)
    actors, bindings = AgentActor.__table__, AgentModelBinding.__table__
    try:
        with engine.connect() as db:
            config = alembic_config(connection=db)
            previous = ScriptDirectory.from_config(config).get_revision(CURRENT).down_revision
            command.upgrade(config, previous)
            # One runtime model at two effort settings, one disabled, one bound.
            db.execute(_CATALOG_ROW, {"key": "shared-high", "effort": "high", "enabled": True})
            db.execute(_CATALOG_ROW, {"key": "shared-low", "effort": "low", "enabled": False})
            actor = db.execute(
                actors.insert().values(name="qualified-worker", display_name="Qualified Worker", api_key_hash="q-hash")
            ).inserted_primary_key[0]
            catalog_id = db.execute(
                text("SELECT id FROM agent_model_catalog_entries WHERE key = 'shared-high'")
            ).scalar_one()
            db.execute(
                bindings.insert().values(
                    actor_id=actor, model_catalog_id=catalog_id, is_default=True, tool_tags=["qualified.schema-review"]
                )
            )
            db.commit()

            command.upgrade(config, CURRENT)
            rows = db.execute(
                text("SELECT key, effort, revision, qualification_keys FROM agent_model_catalog_entries ORDER BY key")
            ).all()
            # Nothing is guessed from tool tags; every entry starts with no keys and keeps its revision.
            assert [(row.key, row.effort, row.revision, _decoded(row.qualification_keys)) for row in rows] == [
                ("shared-high", "high", 4, []),
                ("shared-low", "low", 4, []),
            ]
            binding = db.execute(text("SELECT model_catalog_id, tool_tags FROM agent_model_bindings")).one()
            assert (binding.model_catalog_id, _decoded(binding.tool_tags)) == (catalog_id, ["qualified.schema-review"])
            tables = set(inspect(db).get_table_names())
            assert {"routing_qualification_keys", "routing_qualification_key_revisions"} <= tables

            db.execute(_KEY_ROW, {"key": "qualified.schema-review"})
            db.commit()
            # The database keeps key names canonical and states governed.
            with pytest.raises(IntegrityError):
                db.execute(_KEY_ROW, {"key": "Qualified.Other"})
            db.rollback()
            with pytest.raises(IntegrityError):
                db.execute(text("UPDATE routing_qualification_keys SET state = 'paused'"))
            db.rollback()

            with pytest.raises(RuntimeError, match="Downgrade is unsupported once a qualification key"):
                command.downgrade(config, previous)
            db.rollback()
            db.execute(text("DELETE FROM routing_qualification_keys"))
            db.execute(
                text("UPDATE agent_model_catalog_entries SET qualification_keys = '[\"backend-python\"]'"
                     " WHERE key = 'shared-high'")
            )
            db.commit()
            with pytest.raises(RuntimeError, match="Downgrade is unsupported once a qualification key"):
                command.downgrade(config, previous)
            db.rollback()
            db.execute(text("UPDATE agent_model_catalog_entries SET qualification_keys = '[]'"))
            db.commit()

            command.downgrade(config, previous)
            assert "qualification_keys" not in {
                column["name"] for column in inspect(db).get_columns("agent_model_catalog_entries")
            }
            assert "routing_qualification_keys" not in set(inspect(db).get_table_names())
            assert db.execute(text("SELECT count(*) FROM agent_model_catalog_entries")).scalar_one() == 2
            assert db.execute(text("SELECT count(*) FROM agent_model_bindings")).scalar_one() == 1
    finally:
        engine.dispose()
