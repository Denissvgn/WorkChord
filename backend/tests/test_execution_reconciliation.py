"""Operator reconciliation through authenticated REST and registered MCP commands."""

import json
from types import SimpleNamespace
from unittest.mock import AsyncMock

import httpx
import pytest
from sqlalchemy import func, select

from app import database, mcp_server
from app.config import get_settings
from app.main import app
from app.models.agent import AgentRun, TaskEvent
from app.models.identity import CommandAudit, Principal, ProjectMembership, WorkspaceMembership
from app.models.iteration import Iteration
from app.models.project import Project
from app.services import agent_work_service, execution_reconciliation
from app.services.agent_service import hash_api_key
from app.services.execution_reconciliation import ACTION
from app.services.identity_service import IdentityService, initialize_control_plane
from app.utils.time import utc_now
from tests.test_agent_model_catalog_api import _catalog_values, _command_headers
from tests.test_agent_team_setup_qualification import (
    acknowledge_member,
    provision_ready_topology,
    routing_base,
)
from tests.test_team_pm_dispatch import assignment_api, db_session_factory
from tests.test_team_pm_recovery import recovery_api

database_engines = pytest.mark.parametrize(
    "db_session_factory",
    [
        pytest.param("sqlite", marks=pytest.mark.sqlite),
        pytest.param("postgresql", marks=[pytest.mark.postgresql, pytest.mark.allow_network]),
    ],
    indirect=True,
)


@pytest.mark.asyncio
@database_engines
@pytest.mark.usefixtures("deployed_agent_skill_release")
@pytest.mark.parametrize("auth_mode", ["managed", "trusted_local"])
@pytest.mark.parametrize("change_before_begin", [False, True], ids=["historical-match", "changed-at-start"])
async def test_reconciliation_uses_operator_and_archived_catalog(
    db_session,
    db_session_factory,
    actor_factory,
    team_member_factory,
    task_factory,
    monkeypatch,
    auth_mode,
    change_before_begin,
):
    db = db_session
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", auth_mode)
    monkeypatch.setenv("WORKCHORD_ADMIN_API_KEY", "disposable-run-operator")
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    monkeypatch.setattr(database, "async_session_maker", db_session_factory)
    monkeypatch.setattr(mcp_server, "_session_factory", db_session_factory)
    get_settings.cache_clear()
    operator_id = await initialize_control_plane(db)
    admin = await actor_factory(
        role="pm", scopes='["admin"]', api_key_hash=hash_api_key("disposable-catalog-operator")
    )
    operator = Principal(kind="agent", display_name="Technical operator", agent_actor_id=admin.id)
    db.add(operator)
    await db.flush()
    db.add(WorkspaceMembership(principal_id=operator.id, role="operator"))
    limited = await actor_factory(
        role="pm", scopes='["planning:read"]', api_key_hash=hash_api_key("limited-operator-agent")
    )
    limited_principal = Principal(kind="agent", display_name="Read-only operator key", agent_actor_id=limited.id)
    db.add(limited_principal)
    await db.flush()
    db.add(WorkspaceMembership(principal_id=limited_principal.id, role="operator"))
    await db.commit()
    team = await provision_ready_topology(db, two_workers=False)
    member = team.manifest.workers[0]
    worker = team.actors[member.actor_key]
    worker_key = team.sink.keys[member.actor_key]
    pm_key = team.sink.keys[team.manifest.controller.actor_key]
    verifier_key = team.sink.keys[team.manifest.verifiers[0].actor_key]
    base = await routing_base(
        db,
        topology=team,
        actor_key=member.actor_key,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        title="Verified delivery",
    )
    if auth_mode == "managed":
        project = Project(name="Model history")
        db.add(project)
        await db.flush()
        iteration = await db.get(Iteration, base.task.iteration_id)
        iteration.project_id = base.task.project_id = project.id
        for actor, role in ((base.pm, "manager"), (worker, "executor")):
            identity = await IdentityService(db).actor_context(actor)
            db.add_all(
                [
                    WorkspaceMembership(principal_id=identity.principal_id, role="member"),
                    ProjectMembership(principal_id=identity.principal_id, project_id=project.id, role=role),
                ]
            )
        await db.commit()
    sys_headers = {"X-Admin-API-Key": "disposable-run-operator"}
    agent_headers = {"X-Agent-API-Key": "disposable-catalog-operator"}
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://localhost:8001"
    ) as http:

        async def mutate(method, path, body, key, headers=sys_headers):
            response = await http.request(
                method, "/api/agent/" + path, json=body, headers={**headers, **_command_headers(key)}
            )
            assert response.is_success, response.text
            return response.json()["result"]

        created = await mutate(
            "POST", "model-catalog", _catalog_values("spare", publisher_key="third-studio"), "new-catalog"
        )
        extra = await mutate(
            "POST", "model-bindings", {"actor_id": admin.id, "model_catalog_id": created["id"]}, "new-binding"
        )
        assert extra["model_catalog"]["publisher_key"] == "third-studio"
        lookup = await http.get(
            "/api/agent/model-bindings", params={"actor_id": worker.id}, headers=sys_headers
        )
        assert lookup.is_success, lookup.text
        selected = next(
            item for item in lookup.json() if item["model_catalog"]["key"] == member.model_binding_keys[0]
        )
        catalog = await mutate(
            "PATCH",
            "model-catalog/" + str(selected["model_catalog_id"]),
            {"expected_revision": selected["model_catalog"]["revision"], "publisher_key": "original-studio"},
            "name-publisher",
        )
        # Catalog updates cascade the binding revision. Capture the resulting
        # binding through its normal operator command before runtime acknowledgment.
        current = (
            await http.get("/api/agent/model-bindings/" + str(selected["id"]), headers=sys_headers)
        ).json()
        binding = await mutate(
            "PATCH",
            "model-bindings/" + str(selected["id"]),
            {"expected_revision": current["revision"], "tool_tags": ["terminal"]},
            "bind-current-publisher",
            agent_headers,
        )
        assert binding["model_catalog"]["publisher_key"] == "original-studio"
        if change_before_begin:
            await mutate(
                "PATCH",
                "model-catalog/" + str(catalog["id"]),
                {"expected_revision": catalog["revision"], "publisher_key": "intervening-studio"},
                "intervening-publisher",
            )
        await db.rollback()
        await acknowledge_member(
            team.service,
            topology_key=team.manifest.topology_key,
            actor_key=member.actor_key,
            api_key=worker_key,
        )
        await db.refresh(base.task)
        await db.refresh(base.member)
        await db.refresh(worker)
        db_actor_id, task_id, member_id = worker.id, base.task.id, base.member.id
        async with assignment_api("rest", db_session_factory, monkeypatch) as assign:
            assignment = await assign(
                pm_key,
                {
                    "task_id": task_id,
                    "expected_task_version": base.task.version,
                    "actor_id": db_actor_id,
                    "team_member_id": member_id,
                    "purpose": "execution",
                },
                "plan-work",
            )
        # Reproduce an older recorder, while retaining genuine authenticated
        # begin/submit requests, fences, database writes and native receipts.
        with monkeypatch.context() as old:
            old.setattr(agent_work_service, "actor_provenance", AsyncMock(return_value={}))
            async with recovery_api("rest", db_session_factory, monkeypatch) as call:
                queue = await call("agent_get_my_work", "/api/agent/me/work", worker_key)
                begun = await call(
                    "agent_begin_my_work",
                    "/api/agent/me/work/begin",
                    worker_key,
                    receipt="claim-work",
                    payload={
                        "assignment_id": assignment["id"],
                        "queue_revision": queue["queue_revision"],
                        "lease_seconds": 300,
                        "model": catalog["configured_model_alias"],
                    },
                )
        async with recovery_api("rest", db_session_factory, monkeypatch) as call:
            await call(
                "agent_submit_my_work",
                "/api/agent/me/work/submit",
                worker_key,
                receipt="record-delivery",
                payload={
                    "assignment_id": assignment["id"],
                    "run_id": begun["run"]["id"],
                    "claim_id": begun["claim_id"],
                    "claim_generation": begun["claim_generation"],
                    "expected_task_version": begun["task"]["version"],
                    "summary": "Ready for review",
                    "observed_model": catalog["configured_model_alias"],
                    "evidence": {"check": "passing"},
                    "commit_urls": ["https://github.com/example/project/commit/" + "a" * 40],
                },
            )
        run_id = begun["run"]["id"]
        path = f"/api/agent/model-catalog/execution-provenance/{run_id}/reconcile"

        async def inspect(**kwargs):
            return await http.post(path, headers=sys_headers, **kwargs)

        for key in (pm_key, worker_key, verifier_key, "limited-operator-agent"):
            denied = await http.post(path, headers={"X-Agent-API-Key": key})
            assert denied.status_code == 403 and denied.json()["detail"]["code"] == "operator_required", (
                denied.text
            )
        # A later catalog change cannot rewrite the publisher for a terminal run.
        if not change_before_begin:
            await mutate(
                "PATCH",
                "model-catalog/" + str(catalog["id"]),
                {"expected_revision": catalog["revision"], "publisher_key": "later-studio"},
                "later-publisher",
            )
        monkeypatch.setattr(execution_reconciliation, "MAX_BOUNDED_LIST_ITEMS", 1)

        response = await inspect()
        assert response.is_success, response.text
        preview = response.json()
        assert not preview["applied"], preview
        if change_before_begin:
            assert {"catalog_revision_at_start", "publisher_key"} <= set(preview["missing"]), preview
            assert preview["provenance"].get("publisher_key") is None
            assert preview["provenance"]["submitted_commit_urls"] == [
                "https://github.com/example/project/commit/" + "a" * 40
            ]
            return
        assert not preview["missing"], preview
        assert preview["provenance"]["publisher_key"] == "original-studio"
        assert {"begin", "runtime_ack_event", "model_binding_event", "model_catalog_event"} <= preview[
            "source_receipts"
        ].keys()
        command_url = path + "?apply=true&expected_evidence_digest=" + preview["evidence_digest"]
        assert (await http.post(command_url, headers=sys_headers)).status_code == 422
        stale = await http.post(
            path + "?apply=true&expected_evidence_digest=" + "0" * 64,
            headers={**sys_headers, **_command_headers("stale")},
        )
        assert stale.status_code == 409 and stale.json()["detail"]["code"] == "reconciliation_evidence_stale"
        async with db_session_factory() as observed:
            assert (await observed.get(AgentRun, run_id)).execution_provenance.get("publisher_key") is None
            assert not await observed.scalar(
                select(func.count()).select_from(CommandAudit).where(CommandAudit.action == ACTION)
            )
        params = {"run_id": run_id}

        async def rpc(client, key, args):
            response = await client.post(
                "/",
                headers={"X-Agent-API-Key": key, "Accept": "application/json, text/event-stream"},
                json={
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "tools/call",
                    "params": {"name": "agent_reconcile_run_provenance", "arguments": args},
                },
            )
            assert response.status_code == 200, response.text
            return response.json()["result"]

        server = mcp_server.create_mcp_server()
        mcp_app = mcp_server.MCPAgentKeyMiddleware(server.streamable_http_app())
        async with (
            server.session_manager.run(),
            httpx.AsyncClient(
                transport=httpx.ASGITransport(app=mcp_app), base_url="http://localhost:8001"
            ) as mcp,
        ):
            assert (await rpc(mcp, pm_key, params))["isError"]
            result = await rpc(mcp, "disposable-catalog-operator", params)
            assert (
                not result["isError"]
                and json.loads(result["content"][0]["text"])["evidence_digest"] == preview["evidence_digest"]
            ), result
        headers = {**sys_headers, **_command_headers("apply-history")}
        applied = await http.post(command_url, headers=headers)
        assert applied.is_success, applied.text
        receipt = applied.json()
        assert receipt["applied"] and receipt["principal_id"] == operator_id
        assert (await http.post(command_url, headers=headers)).json() == receipt
        mismatch = await http.post(
            command_url, headers={**headers, "X-Agent-Rationale": "A different command"}
        )
        assert (
            mismatch.status_code == 409
            and mismatch.json()["detail"]["code"] == "reconciliation_idempotency_conflict"
        )
        async with db_session_factory() as observed:
            committed = await observed.get(AgentRun, run_id)
            assert (
                committed.execution_provenance["publisher_key"] == "original-studio"
                and committed.model_trust_state == "unverifiable"
            )
            assert committed.execution_provenance["submitted_commit_urls"] == [
                "https://github.com/example/project/commit/" + "a" * 40
            ]
            audit = (await observed.scalars(select(CommandAudit).where(CommandAudit.action == ACTION))).one()
            assert audit.principal_id == operator_id and audit.details["response"] == receipt
            event = (await observed.scalars(select(TaskEvent).where(TaskEvent.event_type == ACTION))).one()
            assert (
                event.id == receipt["event_id"] and json.loads(event.payload)["principal_id"] == operator_id
            )
        # MCP also commits a receipt under the authenticated operator agent's
        # principal, even if the terminal facts have already been reconciled.
        next_preview = (await inspect()).json()
        server = mcp_server.create_mcp_server()
        mcp_app = mcp_server.MCPAgentKeyMiddleware(server.streamable_http_app())
        async with (
            server.session_manager.run(),
            httpx.AsyncClient(
                transport=httpx.ASGITransport(app=mcp_app), base_url="http://localhost:8001"
            ) as mcp,
        ):
            args = {
                **params,
                "apply": True,
                "expected_evidence_digest": next_preview["evidence_digest"],
                "idempotency_key": "apply-history",
                "rationale": "Confirm the recorded facts",
                "correlation_id": "confirm-mcp",
            }
            final = await rpc(mcp, "disposable-catalog-operator", args)
            assert not final["isError"], final
            confirmed = json.loads(final["content"][0]["text"])
            assert not confirmed["applied"] and confirmed["principal_id"] == operator.id
            assert (
                json.loads((await rpc(mcp, "disposable-catalog-operator", args))["content"][0]["text"])
                == confirmed
            )
        async with db_session_factory() as observed:
            assert (
                await observed.scalar(
                    select(func.count()).select_from(CommandAudit).where(CommandAudit.action == ACTION)
                )
                == 2
            )
        # Other actors' bindings, repeated writes to a single binding and config
        # changes after the run cannot exhaust this actor's original history.
        await mutate(
            "POST",
            "model-bindings",
            {"actor_id": db_actor_id, "model_catalog_id": created["id"]},
            "second-local-binding",
        )
        async with db_session_factory() as observed:
            ids, reason = await execution_reconciliation._actor_binding_ids(
                observed, SimpleNamespace(actor_id=db_actor_id, started_at=utc_now())
            )
            assert ids == [] and reason == "receipt_history_exceeds_bound"
            original_run = await observed.get(AgentRun, run_id)
            assert await execution_reconciliation._actor_binding_ids(observed, original_run) == (
                [binding["id"]],
                None,
            )
    get_settings.cache_clear()


@pytest.mark.asyncio
async def test_legacy_acknowledgement_without_binding_revisions_stays_unknown():
    facts, receipts, _ = await execution_reconciliation._model_at_begin(
        None, None, {"model": "reported"}, {}, {"profile_revision": "p1"}
    )
    assert not facts and not receipts
