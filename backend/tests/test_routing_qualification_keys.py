"""The deployment's governed qualification key registry and the keys catalog entries hold."""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest
from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.database import get_db
from app.main import app as main_app
from app.models.agent import AgentActor, TaskEvent
from app.models.identity import Principal, WorkspaceAuthorityState
from app.models.routing_qualification import RoutingQualificationKeyRevision
from app.schemas.agent_routing import RequiredModelEnvelope
from app.services.agent_routing_policy import (
    ROUTING_SKILL_KEYS,
    UnknownRoutingKeyError,
    evaluate_model_envelope,
    known_routing_keys,
    require_known_routing_keys,
)
from app.services.agent_service import hash_api_key

ADMIN_KEY = "qualification-admin-key"
READER_KEY = "qualification-reader-key"
KEYS = "/api/agent/routing-qualification-keys"


def _catalog_values(key: str, **overrides: Any) -> dict[str, Any]:
    values: dict[str, Any] = {
        "key": key,
        "provider": "configured-provider",
        "configured_model_alias": f"{key}-alias",
        "reasoning_tier": 2,
        "context_tier": "medium",
        "modality_tags": ["text"],
        "cost_tier": "medium",
        "latency_tier": "balanced",
        "enabled": True,
        "revision": 1,
    }
    values.update(overrides)
    return values


def _headers(api_key: str, command_key: str | None = None, reason: str = "Operator qualification change.") -> dict[str, str]:
    headers = {"X-Agent-API-Key": api_key}
    if command_key is not None:
        headers.update(
            {
                "Idempotency-Key": command_key,
                "X-Agent-Rationale": reason,
                "X-Correlation-ID": f"correlation-{command_key}",
            }
        )
    return headers


async def _client(app: FastAPI, db: AsyncSession) -> httpx.AsyncClient:
    async def override_db():
        yield db

    app.dependency_overrides[get_db] = override_db
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://workchord.test")


async def _actors(db: AsyncSession) -> None:
    db.add_all(
        [
            AgentActor(
                name="qualification-admin",
                display_name="Qualification Admin",
                api_key_hash=hash_api_key(ADMIN_KEY),
                scopes='["admin"]',
                enabled=True,
                role="pm",
            ),
            AgentActor(
                name="qualification-reader",
                display_name="Qualification Reader",
                api_key_hash=hash_api_key(READER_KEY),
                scopes='["planning:read"]',
                enabled=True,
                role="pm",
            ),
        ]
    )
    await db.commit()


def test_policy_accepts_declared_keys_beside_the_fixed_built_in_keys() -> None:
    assert known_routing_keys(["qualified.schema-review"]) == ROUTING_SKILL_KEYS | {"qualified.schema-review"}
    assert require_known_routing_keys(["backend-python", "qualified.schema-review"], ["qualified.schema-review"]) == (
        "backend-python",
        "qualified.schema-review",
    )
    with pytest.raises(UnknownRoutingKeyError, match="Unknown routing skill key: qualified.other"):
        require_known_routing_keys(["qualified.other"], ["qualified.schema-review"])

    envelope = {
        "minimum_reasoning_tier": 1,
        "minimum_context_tier": "small",
        "modality_tags": ["text"],
        "tool_tags": [],
        "data_policy_tags": [],
        "qualification_keys": ["qualified.schema-review"],
    }
    actual = {"actual_reasoning_tier": 1, "actual_context_tier": "small", "actual_modality_tags": ["text"]}
    missing = evaluate_model_envelope(envelope, **actual)
    assert missing.hard_blocker_codes == ("model_qualification_missing",)
    assert missing.missing_qualification_keys == ("qualified.schema-review",)
    held = evaluate_model_envelope(envelope, actual_qualification_keys=["qualified.schema-review"], **actual)
    assert held.eligible and held.adequacy_class == 0
    # Without a stated requirement, a held key changes neither eligibility nor adequacy.
    del envelope["qualification_keys"]
    assert evaluate_model_envelope(envelope, actual_qualification_keys=["qualified.schema-review"], **actual).adequacy_class == 0


def test_required_envelope_omits_empty_qualification_keys_from_its_stored_shape() -> None:
    base = {"minimum_reasoning_tier": 1, "minimum_context_tier": "small"}
    assert "qualification_keys" not in RequiredModelEnvelope(**base).model_dump()
    stated = RequiredModelEnvelope(**base, qualification_keys=[" Qualified.Schema-Review "])
    assert stated.model_dump()["qualification_keys"] == ["qualified.schema-review"]
    with pytest.raises(ValueError):
        RequiredModelEnvelope(**base, qualification_keys=["a", "a"])


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_operator_declares_revises_and_retires_a_key_with_audited_revisions(db_session: AsyncSession) -> None:
    await _actors(db_session)
    client = await _client(main_app, db_session)
    try:
        # Reading needs planning:read; changing needs admin authority.
        listed = await client.get(KEYS, headers=_headers(READER_KEY))
        assert listed.status_code == 200
        assert listed.json()["keys"] == []
        assert set(listed.json()["builtin_keys"]) == ROUTING_SKILL_KEYS
        denied = await client.post(
            KEYS,
            headers=_headers(READER_KEY, "reader-declare"),
            json={"key": "qualified.schema-review", "label": "Schema review"},
        )
        assert denied.status_code == 403
        # Authority is checked before the key is looked up, so a missing key reveals nothing.
        for method, path, body in (
            ("PATCH", f"{KEYS}/qualified.absent", {"expected_revision": 1, "label": "Absent"}),
            ("POST", f"{KEYS}/qualified.absent/retire", {"expected_revision": 1}),
        ):
            probe = await client.request(method, path, headers=_headers(READER_KEY, f"probe-{method}"), json=body)
            assert probe.status_code == 403, (method, probe.text)

        declared = await client.post(
            KEYS,
            headers=_headers(ADMIN_KEY, "declare-schema", "Models passed the schema review trial."),
            json={"key": "Qualified.Schema-Review", "label": "Schema review", "description": "Reviews schema changes."},
        )
        assert declared.status_code == 201, declared.text
        receipt = declared.json()
        assert receipt["target_type"] == "routing_qualification_key"
        assert receipt["authoritative_revision"] == 1
        assert receipt["result"]["key"] == "qualified.schema-review"
        assert receipt["result"]["state"] == "active"
        # A retry with the same key and payload replays the same receipt.
        replay = await client.post(
            KEYS,
            headers=_headers(ADMIN_KEY, "declare-schema", "Models passed the schema review trial."),
            json={"key": "Qualified.Schema-Review", "label": "Schema review", "description": "Reviews schema changes."},
        )
        assert replay.status_code == 201 and replay.json() == receipt

        for key, code in (("qualified.schema-review", "routing_qualification_key_exists"),
                          ("backend-python", "routing_qualification_key_builtin")):
            conflict = await client.post(
                KEYS, headers=_headers(ADMIN_KEY, f"declare-{key}"), json={"key": key, "label": "Again"}
            )
            assert conflict.status_code == 409
            assert conflict.json()["detail"]["code"] == code

        stale = await client.patch(
            f"{KEYS}/qualified.schema-review",
            headers=_headers(ADMIN_KEY, "revise-stale"),
            json={"expected_revision": 3, "label": "Schema and migration review"},
        )
        assert stale.status_code == 409
        assert stale.json()["detail"]["current_revision"] == 1
        revised = await client.patch(
            f"{KEYS}/qualified.schema-review",
            headers=_headers(ADMIN_KEY, "revise-label", "Trial now covers migrations."),
            json={"expected_revision": 1, "label": "Schema and migration review"},
        )
        assert revised.status_code == 200, revised.text
        assert revised.json()["authoritative_revision"] == 2

        retired = await client.post(
            f"{KEYS}/qualified.schema-review/retire",
            headers=_headers(ADMIN_KEY, "retire-schema", "The class is no longer routed separately."),
            json={"expected_revision": 2},
        )
        assert retired.status_code == 200, retired.text
        assert retired.json()["result"]["state"] == "retired"
        assert retired.json()["result"]["retired_at"] is not None

        assert (await client.get(KEYS, headers=_headers(READER_KEY))).json()["keys"] == []
        with_retired = (await client.get(KEYS, params={"include_retired": True}, headers=_headers(READER_KEY))).json()
        assert [(key["key"], key["state"], key["revision"]) for key in with_retired["keys"]] == [
            ("qualified.schema-review", "retired", 3)
        ]
        detail = (await client.get(f"{KEYS}/qualified.schema-review", headers=_headers(READER_KEY))).json()
        assert [(item["revision"], item["action"], item["state"], item["reason"]) for item in detail["revisions"]] == [
            (1, "declare", "active", "Models passed the schema review trial."),
            (2, "revise", "active", "Trial now covers migrations."),
            (3, "retire", "retired", "The class is no longer routed separately."),
        ]
        assert detail["usage"] == {"catalog_entries": [], "task_ids": [], "catalog_entries_omitted": 0, "task_ids_omitted": 0}

        # Declaring a retired key again continues its revision sequence.
        again = await client.post(
            KEYS, headers=_headers(ADMIN_KEY, "declare-again"), json={"key": "qualified.schema-review", "label": "Schema review"}
        )
        assert again.status_code == 201 and again.json()["authoritative_revision"] == 4

        events = (await db_session.execute(
            select(TaskEvent).where(TaskEvent.event_type == "agent.routing_qualification_key_changed").order_by(TaskEvent.id)
        )).scalars().all()
        payloads = [json.loads(event.payload) for event in events]
        assert [(p["action"], p["authoritative_revision"]) for p in payloads] == [
            ("declare", 1), ("revise", 2), ("retire", 3), ("declare", 4)
        ]
        assert payloads[2]["rationale"] == "The class is no longer routed separately."
        assert all(event.actor_type == "agent" and event.actor_id is not None for event in events)
        revisions = (await db_session.execute(select(RoutingQualificationKeyRevision))).scalars().all()
        assert len(revisions) == 4
    finally:
        main_app.dependency_overrides.clear()
        await client.aclose()


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_catalog_entries_hold_declared_keys_and_an_effort_change_clears_them(db_session: AsyncSession) -> None:
    await _actors(db_session)
    client = await _client(main_app, db_session)
    try:
        refused = await client.post(
            "/api/agent/model-catalog",
            headers=_headers(ADMIN_KEY, "catalog-undeclared"),
            json=_catalog_values("schema-high", effort="high", qualification_keys=["qualified.schema-review"]),
        )
        assert refused.status_code == 422
        assert refused.json()["detail"] == "Unknown routing skill key: qualified.schema-review"

        await client.post(
            KEYS, headers=_headers(ADMIN_KEY, "declare-schema"), json={"key": "qualified.schema-review", "label": "Schema review"}
        )
        created = await client.post(
            "/api/agent/model-catalog",
            headers=_headers(ADMIN_KEY, "catalog-declared"),
            json=_catalog_values(
                "schema-high", effort="high", qualification_keys=["qualified.schema-review", "backend-python"]
            ),
        )
        assert created.status_code == 201, created.text
        catalog_id = created.json()["target_id"]
        assert created.json()["result"]["qualification_keys"] == ["backend-python", "qualified.schema-review"]

        in_use = await client.post(
            f"{KEYS}/qualified.schema-review/retire",
            headers=_headers(ADMIN_KEY, "retire-in-use"),
            json={"expected_revision": 1},
        )
        assert in_use.status_code == 409
        detail = in_use.json()["detail"]
        assert detail["code"] == "routing_qualification_key_in_use"
        assert detail["catalog_entries"] == [{"id": catalog_id, "key": "schema-high", "enabled": True}]

        async def patch(revision: int, command_key: str, **changes):
            response = await client.patch(
                f"/api/agent/model-catalog/{catalog_id}",
                headers=_headers(ADMIN_KEY, command_key, "Catalog change for qualification evidence."),
                json={"expected_revision": revision, **changes},
            )
            assert response.status_code == 200, response.text
            audit = await db_session.get(TaskEvent, max(response.json()["audit_event_ids"]))
            return response.json()["result"]["qualification_keys"], json.loads(audit.payload)

        # A field that does not change which model runs leaves the keys alone.
        keys, payload = await patch(1, "catalog-cost", cost_tier="high")
        assert keys == ["backend-python", "qualified.schema-review"]
        assert "cleared_qualification_keys" not in payload

        # A new runtime model clears them, and the audit event names what it cleared.
        keys, payload = await patch(2, "catalog-alias", configured_model_alias="schema-high-runtime")
        assert keys == []
        assert payload["cleared_qualification_keys"] == ["backend-python", "qualified.schema-review"]

        # Restating the keys in the same update keeps them.
        keys, payload = await patch(3, "catalog-restate", effort="medium", qualification_keys=["qualified.schema-review"])
        assert keys == ["qualified.schema-review"]
        assert "cleared_qualification_keys" not in payload
        assert payload["configuration"]["effort"] == "medium"

        # Provider, reasoning tier and effort clear them the same way.
        revision = 4
        for field, value in (("provider", "other-provider"), ("reasoning_tier", 3), ("effort", "high")):
            keys, payload = await patch(revision, f"catalog-{field}", **{field: value})
            assert keys == [], field
            assert payload["cleared_qualification_keys"] == ["qualified.schema-review"], field
            revision += 1
            if field != "effort":
                await patch(revision, f"catalog-{field}-restate", qualification_keys=["qualified.schema-review"])
                revision += 1

        retired = await client.post(
            f"{KEYS}/qualified.schema-review/retire",
            headers=_headers(ADMIN_KEY, "retire-free"),
            json={"expected_revision": 1},
        )
        assert retired.status_code == 200
        # A retired key is no longer accepted.
        after = await client.patch(
            f"/api/agent/model-catalog/{catalog_id}",
            headers=_headers(ADMIN_KEY, "catalog-retired-key"),
            json={"expected_revision": revision, "qualification_keys": ["qualified.schema-review"]},
        )
        assert after.status_code == 422
        assert after.json()["detail"] == "Unknown routing skill key: qualified.schema-review"
    finally:
        main_app.dependency_overrides.clear()
        await client.aclose()


@pytest.mark.postgresql
@pytest.mark.integration
@pytest.mark.allow_network
@pytest.mark.asyncio
async def test_usage_and_share_locked_validation_work_on_postgresql(postgres_database, configure_database) -> None:
    from alembic import command as alembic_command
    from sqlalchemy import create_engine
    from sqlalchemy.ext.asyncio import AsyncSession as Session, create_async_engine

    from app.models.agent import AgentModelCatalogEntry, TaskRoutingAssessment
    from app.models.routing_qualification import RoutingQualificationKey
    from app.models.project import Project
    from app.models.task import Task
    from app.services.routing_qualification_key_service import (
        RoutingQualificationKeyService,
        require_known_qualification_keys,
    )
    from app.services.upgrade_service import alembic_config

    configure_database(postgres_database.url)
    sync_engine = create_engine(postgres_database.url)
    with sync_engine.connect() as connection:
        alembic_command.upgrade(alembic_config(connection=connection), "head")
    sync_engine.dispose()
    engine = create_async_engine(postgres_database.url)
    try:
        async with Session(engine, expire_on_commit=False) as db:
            db.add(RoutingQualificationKey(key="qualified.schema-review", label="Schema review"))
            project = Project(name="Schema work")
            db.add(project)
            await db.flush()
            task = Task(title="Schema change", project_id=project.id)
            closed = Task(title="Closed schema change", status="closed", project_id=project.id)
            db.add_all([task, closed])
            db.add(AgentModelCatalogEntry(
                key="schema-high", provider="p", configured_model_alias="a", reasoning_tier=2, effort="high",
                context_tier="medium", modality_tags=["text"], cost_tier="medium", latency_tier="balanced",
                qualification_keys=["qualified.schema-review"],
            ))
            await db.flush()
            for item in (task, closed):
                db.add(TaskRoutingAssessment(
                    task_id=item.id, task_version=item.version, band="routine", reasoning_axis=1,
                    ambiguity_axis=1, context_breadth_axis=1, risk_axis=1, verification_burden_axis=1,
                    required_skill_levels={}, review_mode="none", confidence=0.9, reason_codes=[],
                    rationale="r", assessor="pm",
                    required_model={"minimum_reasoning_tier": 1, "minimum_context_tier": "small",
                                    "qualification_keys": ["qualified.schema-review"]},
                ))
            await db.commit()

            usage = await RoutingQualificationKeyService(db).usage("qualified.schema-review")
            assert [entry.key for entry in usage.catalog_entries] == ["schema-high"]
            assert usage.task_ids == [task.id]
            assert await require_known_qualification_keys(db, ["qualified.schema-review", "backend-python"]) == (
                "backend-python", "qualified.schema-review"
            )
            with pytest.raises(UnknownRoutingKeyError):
                await require_known_qualification_keys(db, ["qualified.other"])
            await db.rollback()
    finally:
        await engine.dispose()


@pytest.mark.postgresql
@pytest.mark.integration
@pytest.mark.allow_network
@pytest.mark.asyncio
async def test_retire_and_validation_serialize_across_postgresql_sessions(postgres_database, configure_database) -> None:
    import asyncio

    from alembic import command as alembic_command
    from sqlalchemy import create_engine
    from sqlalchemy.ext.asyncio import AsyncSession as Session, create_async_engine

    from app.models.agent import AgentModelCatalogEntry
    from app.models.routing_qualification import RoutingQualificationKey
    from app.schemas.agent_planning import AgentPlanningCommandContext
    from app.schemas.routing_qualification import RoutingQualificationKeyRetire
    from app.services.agent_model_catalog_service import AgentModelConflictError
    from app.services.routing_qualification_key_service import (
        RoutingQualificationKeyService,
        require_known_qualification_keys,
    )
    from app.services.upgrade_service import alembic_config

    configure_database(postgres_database.url)
    sync_engine = create_engine(postgres_database.url)
    with sync_engine.connect() as connection:
        alembic_command.upgrade(alembic_config(connection=connection), "head")
    sync_engine.dispose()
    engine = create_async_engine(postgres_database.url)

    def entry(key: str) -> AgentModelCatalogEntry:
        return AgentModelCatalogEntry(
            key=key, provider="p", configured_model_alias=key, reasoning_tier=2, effort="high",
            context_tier="medium", modality_tags=["text"], cost_tier="medium", latency_tier="balanced",
            qualification_keys=["qualified.race"],
        )

    def command(key: str) -> AgentPlanningCommandContext:
        return AgentPlanningCommandContext(idempotency_key=key, rationale="Retire the race key.", correlation_id=key)

    try:
        async with Session(engine, expire_on_commit=False) as setup:
            admin = AgentActor(name="race-admin", display_name="Race Admin", api_key_hash="race-hash",
                               scopes='["admin"]', enabled=True, role="pm")
            setup.add_all([admin, RoutingQualificationKey(key="qualified.race", label="Race")])
            await setup.commit()

        # Validation first: its share lock makes the retire wait, and the retire then sees the new holder.
        async with Session(engine, expire_on_commit=False) as writer, Session(engine, expire_on_commit=False) as retirer:
            await require_known_qualification_keys(writer, ["qualified.race"])
            retire = asyncio.create_task(RoutingQualificationKeyService(retirer).retire(
                "qualified.race", admin, RoutingQualificationKeyRetire(expected_revision=1), command=command("race-1"),
            ))
            await asyncio.sleep(0.5)
            assert not retire.done()
            writer.add(entry("race-holder"))
            await writer.commit()
            with pytest.raises(AgentModelConflictError) as refused:
                await retire
            assert refused.value.code == "routing_qualification_key_in_use"
            assert [item["key"] for item in refused.value.context["catalog_entries"]] == ["race-holder"]

        async with Session(engine, expire_on_commit=False) as cleanup:
            holder = (await cleanup.execute(select(AgentModelCatalogEntry))).scalar_one()
            holder.qualification_keys = []
            await cleanup.commit()

        # Retire first: its row lock makes the validation wait, and the validation then refuses the key.
        async with Session(engine, expire_on_commit=False) as retirer, Session(engine, expire_on_commit=False) as writer:
            service = RoutingQualificationKeyService(retirer)
            row = await service._key("qualified.race", for_update=True)
            assert row is not None
            validation = asyncio.create_task(require_known_qualification_keys(writer, ["qualified.race"]))
            await asyncio.sleep(0.5)
            assert not validation.done()
            row.state = "retired"
            await retirer.commit()
            with pytest.raises(UnknownRoutingKeyError):
                await validation
            await writer.rollback()
    finally:
        await engine.dispose()


@pytest.mark.sqlite
@pytest.mark.asyncio
@pytest.mark.parametrize("auth_mode", ["managed", "trusted_local"])
async def test_the_operator_admin_key_governs_the_registry_and_no_credential_is_refused(
    db_session: AsyncSession,
    monkeypatch: pytest.MonkeyPatch,
    auth_mode: str,
) -> None:
    if await db_session.get(WorkspaceAuthorityState, 1) is None:
        operator = Principal(kind="system", display_name="Operator API")
        db_session.add(operator)
        await db_session.flush()
        db_session.add(WorkspaceAuthorityState(id=1, operator_principal_id=operator.id))
        await db_session.commit()
    monkeypatch.setenv("WORKCHORD_ADMIN_API_KEY", "qualification-operator-key")
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", auth_mode)
    get_settings.cache_clear()
    client = await _client(main_app, db_session)
    command = {
        "Idempotency-Key": f"operator-declare-{auth_mode}",
        "X-Agent-Rationale": "Operator declares the review class.",
        "X-Correlation-ID": f"operator-{auth_mode}",
    }
    try:
        anonymous = await client.post(KEYS, headers=command, json={"key": "qualified.review", "label": "Review"})
        assert anonymous.status_code == 401
        declared = await client.post(
            KEYS,
            headers={"X-Admin-API-Key": "qualification-operator-key", **command},
            json={"key": "qualified.review", "label": "Review"},
        )
        assert declared.status_code == 201, declared.text
        assert declared.json()["actor_id"] is None
        listed = await client.get(KEYS, headers={"X-Admin-API-Key": "qualification-operator-key"})
        assert [key["key"] for key in listed.json()["keys"]] == ["qualified.review"]
        revision = (await db_session.execute(select(RoutingQualificationKeyRevision))).scalar_one()
        assert (revision.actor_type, revision.actor_id, revision.reason) == (
            "operator", None, "Operator declares the review class."
        )
    finally:
        main_app.dependency_overrides.clear()
        get_settings.cache_clear()
        await client.aclose()
