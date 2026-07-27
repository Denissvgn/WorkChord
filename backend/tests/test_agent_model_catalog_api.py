"""Focused Wave 2 model administration and actor-roster qualification."""

from __future__ import annotations

import json
import importlib.util
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx
import pytest
from fastapi import FastAPI, HTTPException
from sqlalchemy import event, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from app import mcp_agent_tools
from app.agent_contract import MODEL_AWARE_ROUTING_FEATURE
from app.config import get_settings
from app.database import get_db
from app.main import app as main_app
from app.mcp_server import _structured_tool_error, mcp
from app.models.agent import (
    AgentActor,
    AgentModelBinding,
    AgentModelCatalogEntry,
    AgentRun,
    AgentTaskAssignment,
    TaskEvent,
)
from app.models.team_member import TeamMemberProfile, TeamMemberProfileSkill
from app.routers import agent as agent_router
from app.routers import agent_planning
from app.schemas.agent import (
    AgentActorCreate,
    AgentTaskAssignmentCreate,
    AgentTaskAssignmentUpdate,
    AgentWorkBegin,
    ModelAwareAgentTaskAssignmentCreate,
    ModelAwareAgentTaskAssignmentUpdate,
    ModelAwareAgentWorkBegin,
)
from app.schemas.agent_planning import AgentPlanningCommandContext
from app.schemas.agent_routing import (
    AgentModelBindingDisable,
    AgentModelBindingUpdate,
    AgentModelCatalogUpdate,
)
from app.services.agent_model_catalog_service import (
    AgentModelCatalogService,
    AgentModelConflictError,
)
from app.services.agent_routing_service import AgentRoutingConflictError
from app.services.agent_service import AgentPermissionError, AgentService, hash_api_key
from app.services.agent_work_service import AgentWorkService
from app.utils.time import utc_now

_PROVISION_SCRIPT = (
    Path(__file__).resolve().parents[2]
    / "scripts"
    / "api_keys"
    / "create_agent_actor.py"
)
_PROVISION_SPEC = importlib.util.spec_from_file_location(
    "workchord_create_agent_actor",
    _PROVISION_SCRIPT,
)
assert _PROVISION_SPEC is not None and _PROVISION_SPEC.loader is not None
provision_actor = importlib.util.module_from_spec(_PROVISION_SPEC)
_PROVISION_SPEC.loader.exec_module(provision_actor)


def _catalog_values(key: str = "balanced-code", **overrides: Any) -> dict[str, Any]:
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


def _command(key: str) -> AgentPlanningCommandContext:
    return AgentPlanningCommandContext(
        idempotency_key=key,
        rationale="Operator-approved model configuration change.",
        correlation_id=f"correlation-{key}",
    )


def _headers(api_key: str, command_key: str | None = None) -> dict[str, str]:
    headers = {"X-Agent-API-Key": api_key}
    if command_key is not None:
        headers.update(
            {
                "Idempotency-Key": command_key,
                "X-Agent-Rationale": "Operator-approved model configuration change.",
                "X-Correlation-ID": f"correlation-{command_key}",
            }
        )
    return headers


def _assert_secret_free(value: Any) -> None:
    forbidden = ("secret", "password", "token", "api_key", "credential")
    if isinstance(value, dict):
        for key, item in value.items():
            assert not any(marker in key.lower() for marker in forbidden)
            _assert_secret_free(item)
    elif isinstance(value, list):
        for item in value:
            _assert_secret_free(item)


@pytest.mark.parametrize(
    ("schema", "payload"),
    (
        (
            AgentModelCatalogUpdate,
            {"expected_revision": 1, "provider": None},
        ),
        (
            AgentModelBindingUpdate,
            {"expected_revision": 1, "tool_tags": None},
        ),
    ),
)
def test_model_updates_reject_null_for_non_nullable_fields(
    schema,
    payload: dict[str, Any],
) -> None:
    with pytest.raises(ValueError, match="fields cannot be null"):
        schema.model_validate(payload)


async def _http_client(
    app: FastAPI,
    db: AsyncSession,
) -> httpx.AsyncClient:
    async def override_db():
        yield db

    app.dependency_overrides[get_db] = override_db
    return httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app),
        base_url="http://workchord.test",
    )


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_rest_and_mcp_model_authorization_idempotency_and_conflicts(
    db_session: AsyncSession,
) -> None:
    pm_key = "pm-model-read-key"
    admin_key = "admin-model-write-key"
    pm = AgentActor(
        name="model-read-pm",
        display_name="Model Read PM",
        api_key_hash=hash_api_key(pm_key),
        scopes='["planning:read"]',
        enabled=True,
        role="pm",
    )
    admin = AgentActor(
        name="model-admin",
        display_name="Model Admin",
        api_key_hash=hash_api_key(admin_key),
        scopes='["admin"]',
        enabled=True,
        role="pm",
    )
    db_session.add_all([pm, admin])
    await db_session.commit()
    pm_id = pm.id

    payload = _catalog_values()
    client = await _http_client(main_app, db_session)
    try:
        denied = await client.post(
            "/api/agent/model-catalog",
            headers=_headers(pm_key, "pm-denied"),
            json=payload,
        )
        assert denied.status_code == 403

        created = await client.post(
            "/api/agent/model-catalog",
            headers=_headers(admin_key, "catalog-create"),
            json=payload,
        )
        assert created.status_code == 201
        receipt = created.json()
        assert receipt["authoritative_revision"] == 1
        assert receipt["result"]["key"] == "balanced-code"

        replay = await client.post(
            "/api/agent/model-catalog",
            headers=_headers(admin_key, "catalog-create"),
            json=payload,
        )
        assert replay.status_code == 201
        assert replay.json() == receipt

        read = await client.get(
            "/api/agent/model-catalog",
            headers=_headers(pm_key),
        )
        assert read.status_code == 200
        assert read.json() == [receipt["result"]]
        _assert_secret_free(read.json())

        updated = await client.patch(
            f"/api/agent/model-catalog/{receipt['target_id']}",
            headers=_headers(admin_key, "catalog-update"),
            json={"expected_revision": 1, "cost_tier": "high"},
        )
        assert updated.status_code == 200
        assert updated.json()["authoritative_revision"] == 2

        stale = await client.patch(
            f"/api/agent/model-catalog/{receipt['target_id']}",
            headers=_headers(admin_key, "catalog-stale"),
            json={
                "expected_revision": 1,
                "configured_model_alias": "stale-alias",
            },
        )
        assert stale.status_code == 409
        assert stale.json()["detail"] == {
            "code": "agent_model_revision_conflict",
            "message": "model_catalog revision is stale",
            "resource": "model_catalog",
            "resource_id": receipt["target_id"],
            "expected_revision": 1,
            "current_revision": 2,
        }

        pm = await db_session.get(AgentActor, pm_id)
        assert pm is not None
        mcp_read = await mcp_agent_tools.list_agent_model_catalog(
            db_session,
            pm,
        )
        assert mcp_read == read.json()[:0] + [updated.json()["result"]]
        with pytest.raises(AgentPermissionError):
            await mcp_agent_tools.create_agent_model_catalog_entry(
                db_session,
                pm,
                _catalog_values("pm-forbidden"),
                idempotency_key="mcp-pm-forbidden",
                rationale="PM may read but not mutate model metadata.",
                correlation_id="mcp-pm-forbidden-correlation",
            )
    finally:
        await client.aclose()
        main_app.dependency_overrides.clear()


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_binding_disable_requires_explicit_reconciliation_and_marks_queue_stale(
    db_session: AsyncSession,
    actor_factory,
    task_factory,
) -> None:
    admin = await actor_factory(
        scopes='["admin"]',
        role="pm",
        name="binding-admin",
        display_name="Binding Admin",
    )
    worker = await actor_factory(
        scopes='["assignments:read","work:execute"]',
        role="worker",
        name="binding-worker",
        display_name="Binding Worker",
    )
    catalog = AgentModelCatalogEntry(**_catalog_values())
    db_session.add(catalog)
    await db_session.flush()
    binding = AgentModelBinding(
        actor_id=worker.id,
        model_catalog_id=catalog.id,
        is_default=True,
        enabled=True,
        tool_tags=["code-edit", "shell"],
        data_policy_tags=["workspace-source"],
        revision=1,
    )
    db_session.add(binding)
    await db_session.flush()
    task = await task_factory()
    assignment = AgentTaskAssignment(
        task_id=task.id,
        actor_id=worker.id,
        purpose="execution",
        queue_class="normal",
        state="queued",
        queue_rank=1000,
        task_version=task.version,
        model_binding_id=binding.id,
        model_binding_revision=binding.revision,
        routing_snapshot="{}",
    )
    db_session.add(assignment)
    await db_session.flush()
    run = AgentRun(
        task_id=task.id,
        actor_id=worker.id,
        assignment_id=assignment.id,
        status="succeeded",
        model_binding_id=binding.id,
        model_binding_revision=binding.revision,
        configured_model_alias=catalog.configured_model_alias,
        resolved_model_id=catalog.configured_model_alias,
    )
    db_session.add(run)
    await db_session.commit()
    admin_id = admin.id
    binding_id = binding.id
    task_id = task.id
    assignment_id = assignment.id
    run_id = run.id

    service = AgentModelCatalogService(db_session)
    with pytest.raises(AgentModelConflictError) as blocked:
        await service.disable_binding(
            binding_id,
            admin,
            AgentModelBindingDisable(
                expected_revision=1,
                reconcile_live_assignments=False,
            ),
            command=_command("binding-disable-blocked"),
        )
    assert blocked.value.detail()["code"] == "agent_model_live_assignments"
    assert blocked.value.detail()["live_assignment_ids"] == [assignment_id]

    admin = await db_session.get(AgentActor, admin_id)
    assert admin is not None
    receipt = await service.disable_binding(
        binding_id,
        admin,
        AgentModelBindingDisable(
            expected_revision=1,
            reconcile_live_assignments=True,
        ),
        command=_command("binding-disable-reconciled"),
    )
    assert receipt.authoritative_revision == 2
    assert receipt.invalidated_assignment_ids == [assignment_id]
    assert receipt.result["enabled"] is False
    assert receipt.result["run_reference_count"] == 1

    queued = await AgentWorkService(db_session).list_assignments(
        admin,
        task_id=task_id,
    )
    assert len(queued) == 1
    assert queued[0].model_binding_status == "stale"
    assert queued[0].model_binding_stale_reasons == [
        "model_binding_disabled",
        "model_binding_revision_mismatch",
    ]

    persisted_binding = await db_session.get(AgentModelBinding, binding_id)
    persisted_assignment = await db_session.get(
        AgentTaskAssignment,
        assignment_id,
    )
    persisted_run = await db_session.get(AgentRun, run_id)
    assert persisted_binding is not None
    assert persisted_assignment is not None
    assert persisted_run is not None
    events = (
        await db_session.execute(
            select(TaskEvent)
            .where(
                TaskEvent.event_type.in_(
                    (
                        "agent.model_configuration_changed",
                        "agent.model_binding_invalidated",
                    )
                )
            )
            .order_by(TaskEvent.id)
        )
    ).scalars().all()
    assert [event.id for event in events] == receipt.audit_event_ids
    invalidated = next(
        event
        for event in events
        if event.event_type == "agent.model_binding_invalidated"
    )
    assert json.loads(invalidated.payload)["assignment_id"] == assignment_id


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_rest_and_mcp_rosters_are_identical_and_secret_free(
    db_session: AsyncSession,
) -> None:
    pm_key = "roster-pm-key"
    pm = AgentActor(
        name="roster-pm",
        display_name="Roster PM",
        api_key_hash=hash_api_key(pm_key),
        scopes='["planning:read"]',
        enabled=True,
        role="pm",
    )
    profile = TeamMemberProfile(
        seed_key="roster-worker-profile",
        display_name="Roster Worker Profile",
        automation_enabled=True,
        profile_kind="agent",
        assignment_modes=["execution"],
    )
    profile.skills.append(
        TeamMemberProfileSkill(
            skill_key="backend-python",
            skill_name="Backend Python",
            category="implementation",
            level=4,
            interest=5,
            is_weakness=False,
            keywords_json=["python"],
        )
    )
    worker = AgentActor(
        name="roster-worker",
        display_name="Roster Worker",
        api_key_hash=hash_api_key("roster-worker-key"),
        scopes='["assignments:read","work:execute"]',
        enabled=True,
        role="worker",
        profile=profile,
        queue_revision=3,
        last_seen_at=datetime(2026, 7, 27, 9, 30, tzinfo=UTC),
    )
    disabled_actor = AgentActor(
        name="disabled-roster-worker",
        display_name="Disabled Roster Worker",
        api_key_hash=hash_api_key("disabled-roster-worker-key"),
        scopes='["assignments:read","work:execute"]',
        enabled=False,
        role="worker",
    )
    catalog = AgentModelCatalogEntry(**_catalog_values())
    disabled_catalog = AgentModelCatalogEntry(
        **_catalog_values("disabled-code", enabled=False)
    )
    db_session.add_all(
        [pm, worker, disabled_actor, catalog, disabled_catalog]
    )
    await db_session.flush()
    active_binding = AgentModelBinding(
        actor_id=worker.id,
        model_catalog_id=catalog.id,
        is_default=True,
        enabled=True,
        tool_tags=["code-edit"],
        data_policy_tags=["workspace-source"],
        revision=4,
    )
    disabled_binding = AgentModelBinding(
        actor_id=worker.id,
        model_catalog_id=disabled_catalog.id,
        is_default=False,
        enabled=True,
        tool_tags=["shell"],
        data_policy_tags=[],
        revision=2,
    )
    disabled_actor_binding = AgentModelBinding(
        actor_id=disabled_actor.id,
        model_catalog_id=catalog.id,
        is_default=True,
        enabled=True,
        tool_tags=[],
        data_policy_tags=[],
        revision=1,
    )
    db_session.add_all(
        [active_binding, disabled_binding, disabled_actor_binding]
    )
    await db_session.commit()

    client = await _http_client(main_app, db_session)
    try:
        response = await client.get(
            "/api/agent/actors",
            headers=_headers(pm_key),
        )
        assert response.status_code == 200
        rest_roster = response.json()
        mcp_roster = await mcp_agent_tools.list_agent_actor_roster(
            db_session,
            pm,
        )
        assert rest_roster == mcp_roster
        _assert_secret_free(rest_roster)
    finally:
        await client.aclose()
        main_app.dependency_overrides.clear()

    worker_item = next(item for item in rest_roster if item["id"] == worker.id)
    assert worker_item["actor_revision"] == 3
    assert worker_item["profile_revision"].startswith(f"p{profile.id}-")
    assert worker_item["profile"]["assignment_modes"] == ["execution"]
    assert worker_item["profile"]["skills"][0]["skill_key"] == "backend-python"
    assert [item["id"] for item in worker_item["eligible_model_bindings"]] == [
        active_binding.id
    ]
    assert (
        worker_item["eligible_model_bindings"][0]["model_catalog"]["key"]
        == "balanced-code"
    )

    audit_bindings = await AgentModelCatalogService(db_session).list_bindings(
        pm,
        actor_id=worker.id,
        include_disabled=True,
    )
    assert [item.id for item in audit_bindings] == [
        active_binding.id,
        disabled_binding.id,
    ]
    assert audit_bindings[1].selectable is False

    audit_roster = await AgentWorkService(db_session).list_actor_roster(
        pm,
        include_disabled=True,
    )
    disabled_item = next(
        item for item in audit_roster if item.id == disabled_actor.id
    )
    assert disabled_item.enabled is False
    assert disabled_item.eligible_model_bindings == []


async def _seed_roster_actors(
    db: AsyncSession,
    *,
    catalog_id: int,
    start: int,
    count: int,
) -> None:
    for index in range(start, start + count):
        profile = TeamMemberProfile(
            seed_key=f"bounded-profile-{index}",
            display_name=f"Bounded Profile {index}",
            automation_enabled=True,
            profile_kind="agent",
            assignment_modes=["execution"],
        )
        profile.skills.append(
            TeamMemberProfileSkill(
                skill_key=f"bounded-skill-{index}",
                skill_name=f"Bounded Skill {index}",
                level=3,
                interest=3,
                is_weakness=False,
                keywords_json=[],
            )
        )
        actor = AgentActor(
            name=f"bounded-actor-{index}",
            display_name=f"Bounded Actor {index}",
            api_key_hash=f"bounded-hash-{index}",
            scopes='["assignments:read"]',
            enabled=True,
            role="worker",
            profile=profile,
        )
        db.add(actor)
        await db.flush()
        db.add(
            AgentModelBinding(
                actor_id=actor.id,
                model_catalog_id=catalog_id,
                is_default=True,
                enabled=True,
                tool_tags=[],
                data_policy_tags=[],
                revision=1,
            )
        )
    await db.commit()


async def _roster_query_count(
    factory: async_sessionmaker[AsyncSession],
    engine: AsyncEngine,
) -> tuple[int, int]:
    query_count = 0

    def count_query(*_args: Any) -> None:
        nonlocal query_count
        query_count += 1

    event.listen(engine.sync_engine, "before_cursor_execute", count_query)
    try:
        async with factory() as db:
            principal = AgentActor(
                id=999_999,
                name="query-count-reader",
                display_name="Query Count Reader",
                api_key_hash="query-count-reader",
                scopes='["planning:read"]',
                enabled=True,
                role="pm",
                created_at=utc_now(),
            )
            roster = await AgentWorkService(db).list_actor_roster(principal)
            return query_count, len(roster)
    finally:
        event.remove(engine.sync_engine, "before_cursor_execute", count_query)


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_roster_query_count_is_cardinality_constant(
    db_session_factory: async_sessionmaker[AsyncSession],
    sqlite_engine: AsyncEngine,
) -> None:
    async with db_session_factory() as db:
        catalog = AgentModelCatalogEntry(**_catalog_values())
        db.add(catalog)
        await db.flush()
        catalog_id = catalog.id
        await _seed_roster_actors(
            db,
            catalog_id=catalog_id,
            start=0,
            count=1,
        )

    small_queries, small_count = await _roster_query_count(
        db_session_factory,
        sqlite_engine,
    )

    async with db_session_factory() as db:
        await _seed_roster_actors(
            db,
            catalog_id=catalog_id,
            start=1,
            count=24,
        )

    large_queries, large_count = await _roster_query_count(
        db_session_factory,
        sqlite_engine,
    )

    assert small_count == 1
    assert large_count == 25
    assert large_queries == small_queries
    assert large_queries <= 8


def test_actor_provisioning_payload_accepts_catalog_key_and_rejects_secrets(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, Any] = {}

    class Response:
        def __enter__(self):
            return self

        def __exit__(self, *_args: Any) -> None:
            return None

        def read(self) -> bytes:
            return json.dumps(
                {
                    "id": 17,
                    "name": "catalog-worker",
                    "api_key": "one-time-key",
                    "model_binding_id": 23,
                    "model_binding_revision": 1,
                    "model_catalog_key": "balanced-code",
                }
            ).encode("utf-8")

    def urlopen(req, *, timeout: float):
        captured["payload"] = json.loads(req.data.decode("utf-8"))
        captured["timeout"] = timeout
        return Response()

    monkeypatch.setattr(provision_actor.request, "urlopen", urlopen)
    response = provision_actor.create_actor(
        url="http://workchord.test/api/agent/actors",
        bootstrap_key="bootstrap-key",
        name="catalog-worker",
        display_name="Catalog Worker",
        scopes=["assignments:read", "work:execute"],
        role="worker",
        profile_id=None,
        work_policy="assigned_only",
        max_parallel_work=1,
        enabled=True,
        model_catalog_key="balanced-code",
        model_tool_tags=["code-edit", "shell"],
        model_data_policy_tags=["workspace-source"],
        model_binding_is_default=True,
        timeout=5.0,
    )

    assert response["model_binding_id"] == 23
    assert captured["payload"]["model_binding"] == {
        "model_catalog_key": "balanced-code",
        "is_default": True,
        "tool_tags": ["code-edit", "shell"],
        "data_policy_tags": ["workspace-source"],
    }
    _assert_secret_free(captured["payload"])
    with pytest.raises(ValueError):
        AgentActorCreate.model_validate(
            {
                "name": "unsafe-worker",
                "display_name": "Unsafe Worker",
                "provider_api_key": "must-not-be-accepted",
            }
        )


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_actor_provisioning_creates_binding_and_audit_atomically(
    db_session: AsyncSession,
    actor_factory,
) -> None:
    admin = await actor_factory(
        scopes='["admin"]',
        role="pm",
        name="provision-admin",
        display_name="Provision Admin",
    )
    catalog = AgentModelCatalogEntry(**_catalog_values())
    db_session.add(catalog)
    await db_session.commit()

    actor, api_key, binding = await AgentService(db_session).create_actor(
        AgentActorCreate.model_validate(
            {
                "name": "provisioned-model-worker",
                "display_name": "Provisioned Model Worker",
                "scopes": ["assignments:read", "work:execute"],
                "role": "worker",
                "model_binding": {
                    "model_catalog_key": "balanced-code",
                    "tool_tags": ["shell", "code-edit"],
                    "data_policy_tags": ["workspace-source"],
                },
            }
        ),
        principal=admin,
    )

    assert api_key.startswith("pmag_")
    assert binding is not None
    assert binding.actor_id == actor.id
    assert binding.model_catalog_id == catalog.id
    assert binding.revision == 1
    event_row = await db_session.execute(
        select(TaskEvent).where(
            TaskEvent.event_type == "agent.model_configuration_changed",
            TaskEvent.actor_id == admin.id,
        )
    )
    audit = event_row.scalar_one()
    payload = json.loads(audit.payload)
    assert payload["target_id"] == binding.id
    assert payload["model_catalog_key"] == "balanced-code"


@pytest.mark.contract
def test_wave3_surfaces_advertise_model_aware_routing() -> None:
    from app.agent_contract import agent_contract_features

    assert MODEL_AWARE_ROUTING_FEATURE in agent_contract_features(
        include_skill_bundles=True
    )
    api_prefix = get_settings().api_prefix
    registered_routes = {
        (f"{api_prefix}{route.path}", method)
        for router in (agent_router.router, agent_planning.router)
        for route in router.routes
        for method in (getattr(route, "methods", None) or ())
    }
    assert (
        "/api/agent/planning/tasks/{task_id}/routing-assessment",
        "GET",
    ) in registered_routes
    assert (
        "/api/agent/planning/tasks/{task_id}/routing-assessment",
        "POST",
    ) in registered_routes
    assert (
        "/api/agent/tasks/{task_id}/routing-preview",
        "POST",
    ) in registered_routes

    openapi_paths = main_app.openapi()["paths"]
    expected_request_unions = {
        ("/api/agent/assignments", "post"): (
            "ModelAwareAgentTaskAssignmentCreate",
            "AgentTaskAssignmentCreate",
        ),
        ("/api/agent/assignments/{assignment_id}", "patch"): (
            "ModelAwareAgentTaskAssignmentUpdate",
            "AgentTaskAssignmentUpdate",
        ),
        ("/api/agent/me/work/begin", "post"): (
            "ModelAwareAgentWorkBegin",
            "AgentWorkBegin",
        ),
    }
    for (path, method), expected_models in expected_request_unions.items():
        body_schema = openapi_paths[path][method]["requestBody"]["content"][
            "application/json"
        ]["schema"]
        assert [
            entry["$ref"].removeprefix("#/components/schemas/")
            for entry in body_schema["anyOf"]
        ] == list(expected_models)


@pytest.mark.contract
@pytest.mark.asyncio
async def test_mcp_registers_roster_catalog_resources_and_admin_tools() -> None:
    tool_names = {tool.name for tool in await mcp.list_tools()}
    resource_uris = {str(resource.uri) for resource in await mcp.list_resources()}
    resource_templates = {
        str(template.uriTemplate)
        for template in await mcp.list_resource_templates()
    }

    assert {
        "agent_list_actor_roster",
        "agent_list_model_catalog",
        "agent_get_model_catalog_entry",
        "agent_list_model_bindings",
        "agent_get_model_binding",
        "agent_create_model_catalog_entry",
        "agent_update_model_catalog_entry",
        "agent_disable_model_catalog_entry",
        "agent_create_model_binding",
        "agent_update_model_binding",
        "agent_disable_model_binding",
        "agent_get_task_routing_assessment",
        "agent_create_task_routing_assessment",
        "agent_preview_task_routing",
    }.issubset(tool_names)
    assert "workchord://agent/actors" in resource_uris
    assert "workchord://agent/model-catalog" in resource_uris
    assert (
        "workchord://agent/tasks/{task_id}/routing-assessment"
        in resource_templates
    )


@pytest.mark.contract
def test_mcp_assignment_and_begin_payloads_preserve_additive_legacy_union() -> None:
    digest = "a" * 64
    legacy_create = mcp_agent_tools._AGENT_ASSIGNMENT_CREATE_ADAPTER.validate_python(
        {"task_id": 1, "actor_id": 2, "expected_task_version": 3}
    )
    aware_create = mcp_agent_tools._AGENT_ASSIGNMENT_CREATE_ADAPTER.validate_python(
        {
            "task_id": 1,
            "actor_id": 2,
            "expected_task_version": 3,
            "purpose": "execution",
            "assessment_id": 4,
            "model_binding_id": 5,
            "model_binding_revision": 6,
            "routing_preview_id": "preview-7",
            "routing_preview_digest": digest,
        }
    )
    legacy_update = mcp_agent_tools._AGENT_ASSIGNMENT_UPDATE_ADAPTER.validate_python(
        {"expected_queue_revision": 1, "queue_rank": 10}
    )
    aware_update = mcp_agent_tools._AGENT_ASSIGNMENT_UPDATE_ADAPTER.validate_python(
        {
            "expected_queue_revision": 1,
            "assessment_id": 4,
            "model_binding_id": 5,
            "model_binding_revision": 6,
            "routing_preview_id": "preview-7",
            "routing_preview_digest": digest,
        }
    )
    legacy_begin = mcp_agent_tools._AGENT_WORK_BEGIN_ADAPTER.validate_python(
        {"assignment_id": 8, "queue_revision": 2}
    )
    aware_begin = mcp_agent_tools._AGENT_WORK_BEGIN_ADAPTER.validate_python(
        {
            "assignment_id": 8,
            "queue_revision": 2,
            "model_binding_id": 5,
            "model_binding_revision": 6,
            "resolved_model_id": "resolved-model",
        }
    )

    assert isinstance(legacy_create, AgentTaskAssignmentCreate)
    assert isinstance(aware_create, ModelAwareAgentTaskAssignmentCreate)
    assert isinstance(legacy_update, AgentTaskAssignmentUpdate)
    assert isinstance(aware_update, ModelAwareAgentTaskAssignmentUpdate)
    assert isinstance(legacy_begin, AgentWorkBegin)
    assert isinstance(aware_begin, ModelAwareAgentWorkBegin)


@pytest.mark.contract
def test_routing_conflicts_keep_structured_detail_across_rest_and_mcp() -> None:
    conflict = AgentRoutingConflictError(
        "routing_preview_stale",
        "Routing preview no longer matches authoritative inputs",
        task_id=17,
        expected_task_version=4,
    )
    expected = {
        "code": "routing_preview_stale",
        "message": "Routing preview no longer matches authoritative inputs",
        "task_id": 17,
        "expected_task_version": 4,
    }

    with pytest.raises(HTTPException) as agent_error:
        agent_router._handle_agent_error(conflict, structured=True)
    with pytest.raises(HTTPException) as planning_error:
        agent_planning._handle_agent_error(conflict)

    assert agent_error.value.status_code == 409
    assert agent_error.value.detail == expected
    assert planning_error.value.status_code == 409
    assert planning_error.value.detail == expected
    assert json.loads(_structured_tool_error(conflict)) == expected
