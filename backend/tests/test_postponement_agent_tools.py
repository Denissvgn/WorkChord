"""A PM agent postpones, reactivates and reads postponed work with exactly the REST authority."""

import json
from contextlib import asynccontextmanager
from datetime import timedelta

import httpx
import pytest
from sqlalchemy import select

from app import mcp_server
from app.models.agent import AgentActor, TaskEvent
from app.models.identity import Principal, ProjectMembership
from app.models.project import Project
from app.models.task import Task
from app.services.agent_readiness import DEFAULT_AGENT_CAPABILITY_SLUGS
from app.services.agent_service import hash_api_key
from app.utils.time import utc_now
from tests.test_delivery_scenarios import delivery_store  # noqa: F401
from tests.test_managed_authority import client, managed_store  # noqa: F401

PM_KEY = "postpone-tools-pm-key"
OTHER_PM_KEY = "postpone-tools-other-pm-key"
VIEWER_KEY = "postpone-tools-viewer-key"
READER_KEY = "postpone-tools-read-scope-key"
WORKER_KEY = "postpone-tools-worker-key"
VERIFIER_KEY = "postpone-tools-verifier-key"
WRITE = ["planning:read", "planning:write", "tasks:read"]
NEW_TOOLS = {
    "agent_get_task_postponement": {"task_id"},
    "agent_postpone_task": {"task_id", "payload", "idempotency_key", "rationale", "correlation_id"},
    "agent_reactivate_task": {"task_id", "payload", "idempotency_key", "rationale", "correlation_id"},
}


async def _agent(db, key, name, *, role="pm", scopes=WRITE, memberships):
    actor = AgentActor(name=name, display_name=name, role=role, api_key_hash=hash_api_key(key), scopes=json.dumps(scopes))
    db.add(actor)
    await db.flush()
    principal = Principal(kind="agent", display_name=name, agent_actor_id=actor.id)
    db.add(principal)
    await db.flush()
    db.add_all([ProjectMembership(principal_id=principal.id, project_id=project, role=membership)
                for project, membership in memberships.items()])


@pytest.fixture
async def team(managed_store):  # noqa: F811
    """One PM manages the work; every other credential differs in exactly one way."""
    factory, scenario, _, _ = managed_store
    manage = {project: "manager" for project in scenario.projects}
    async with factory() as db:
        elsewhere = Project(name="Elsewhere")
        db.add(elsewhere)
        await db.flush()
        await _agent(db, PM_KEY, "Postpone PM", memberships=manage)
        await _agent(db, OTHER_PM_KEY, "Other team PM", memberships={elsewhere.id: "manager"})
        await _agent(db, VIEWER_KEY, "Viewing PM", memberships={p: "viewer" for p in scenario.projects})
        await _agent(db, READER_KEY, "Read-scoped PM", scopes=["planning:read"], memberships=manage)
        # Manage permission on the project is not enough: the actor's role decides.
        await _agent(db, WORKER_KEY, "Managing worker", role="worker", memberships=manage)
        await _agent(db, VERIFIER_KEY, "Managing reviewer", role="verifier", memberships=manage)
        await db.commit()
    return factory, scenario


@asynccontextmanager
async def _nothing():
    yield


@asynccontextmanager
async def transport_api(transport, factory, monkeypatch):
    """Call one command through REST or MCP; a refusal returns the error text instead of the result."""
    monkeypatch.setattr(mcp_server, "_session_factory", factory)
    server = mcp_server.create_mcp_server() if transport == "mcp" else None
    application = mcp_server.MCPAgentKeyMiddleware(server.streamable_http_app()) if server else None
    async with server.session_manager.run() if server else _nothing():
        async with (httpx.AsyncClient(transport=httpx.ASGITransport(app=application), base_url="http://localhost:8001")
                    if server else client()) as http:
            async def call(key, tool, method, path, *, arguments=None, body=None, receipt=None):
                headers = {"X-Agent-API-Key": key}
                if server:
                    args = dict(arguments or {})
                    if body is not None:
                        args.update(payload=body, idempotency_key=receipt, rationale="Work must stop for now",
                                    correlation_id=receipt)
                    headers["Accept"] = "application/json, text/event-stream"
                    response = await http.post("/", headers=headers, json={
                        "jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": tool, "arguments": args}})
                    assert response.status_code == 200, response.text
                    result = response.json()["result"]
                    if result["isError"]:
                        return False, result["content"][0]["text"]
                    value = result.get("structuredContent")
                    value = value.get("result", value) if isinstance(value, dict) and set(value) == {"result"} else value
                    if value is None:
                        value = json.loads(result["content"][0]["text"])
                    if tool in {"agent_postpone_task", "agent_reactivate_task"}:
                        assert value["operation"] == ("planning.task.postpone" if "postpone" in tool
                                                      else "planning.task.reactivate")
                        value = value["result"]
                    return True, value
                response = await http.request(method, path, headers=headers, json=body)
                if response.status_code >= 400:
                    return False, f"{response.status_code} {response.text}"
                return True, response.json()
            yield call


def _later(days=30):
    return (utc_now().date() + timedelta(days=days)).isoformat()


def _postpone(call, key, task_id, version, receipt):
    body = {"expected_version": version, "reason": "Waiting for the platform decision",
            "requirements": [{"kind": "date", "on_date": _later()},
                             {"kind": "owner_decision", "description": "Does the scope stay?"}]}
    return call(key, "agent_postpone_task", "POST", f"/api/tasks/{task_id}/postpone",
                arguments={"task_id": task_id}, body=body, receipt=receipt)


def _reactivate(call, key, task_id, version, receipt):
    return call(key, "agent_reactivate_task", "POST", f"/api/tasks/{task_id}/reactivate",
                arguments={"task_id": task_id}, body={"expected_version": version, "reason": "Decision made"},
                receipt=receipt)


def _read(call, key, task_id):
    return call(key, "agent_get_task_postponement", "GET", f"/api/tasks/{task_id}/postponement",
                arguments={"task_id": task_id})


async def _state(factory, task_id):
    async with factory() as db:
        task = await db.get(Task, task_id)
        return task.status, task.version


async def test_new_tools_declare_their_inputs_and_features_and_no_owner_decision_tool():
    from app.agent_contract import agent_contract_features
    from app.server_features import SERVER_FEATURES

    tools = {tool.name: tool for tool in await mcp_server.mcp.list_tools()}
    for name, fields in NEW_TOOLS.items():
        schema = tools[name].inputSchema
        assert set(schema["properties"]) == fields, name
        assert set(schema["required"]) == fields, name
        assert schema["properties"]["task_id"]["type"] == "integer"
    assert tools["agent_get_task_postponement"].annotations.readOnlyHint
    assert not tools["agent_postpone_task"].annotations.readOnlyHint
    assert not tools["agent_reactivate_task"].annotations.readOnlyHint
    assert "agent-task-postponement-v1" in agent_contract_features(include_skill_bundles=False)
    assert "postponement-agent-tools-v1" in SERVER_FEATURES
    # Only the workspace owner records a decision; no tool takes it for an agent.
    assert not [name for name in tools if "decision" in name and "postpone" in name]
    status = tools["workspace_list_project_tasks"].inputSchema["properties"]["status"]
    assert "postponed" in json.dumps(status)


@pytest.mark.parametrize("transport", ["rest", "mcp"])
async def test_pm_postpones_reads_each_requirement_and_reactivates(team, transport, monkeypatch):
    factory, scenario = team
    task_id = scenario.tasks["planned"]
    _, version = await _state(factory, task_id)
    async with transport_api(transport, factory, monkeypatch) as call:
        ok, postponed = await _postpone(call, PM_KEY, task_id, version, "postpone-1")
        assert ok, postponed
        assert postponed["task"]["status"] == "postponed" and postponed["task"]["version"] == version + 1
        record = postponed["postponement"]
        assert record["open"] and record["from_status"] == "planned"
        assert record["reason"] == "Waiting for the platform decision"
        assert [(r["kind"], r["met"]) for r in record["requirements"]] == [("date", False), ("owner_decision", False)]

        ok, read = await _read(call, PM_KEY, task_id)
        assert ok and read["postponement"] == postponed["postponement"]
        assert (read["task"]["id"], read["task"]["status"], read["task"]["version"]) == (
            task_id, "postponed", version + 1)

        ok, stale = await _reactivate(call, PM_KEY, task_id, version, "reactivate-stale")
        assert not ok and "version" in stale
        ok, reactivated = await _reactivate(call, PM_KEY, task_id, version + 1, "reactivate-1")
        assert ok, reactivated
        assert reactivated["task"]["status"] == "planned"
        closed = reactivated["postponement"]
        assert not closed["open"] and closed["reactivated_to_status"] == "planned"
        assert closed["reactivation_trigger"] == "command" and closed["reactivation_reason"] == "Decision made"
    assert await _state(factory, task_id) == ("planned", version + 2)
    async with factory() as db:
        events = (await db.scalars(select(TaskEvent).where(
            TaskEvent.task_id == task_id, TaskEvent.event_type.in_(["task_postponed", "task_reactivated"])
        ).order_by(TaskEvent.id))).all()
    assert [event.event_type for event in events] == ["task_postponed", "task_reactivated"]
    assert {event.actor_type for event in events} == {"agent"}


async def test_rest_and_mcp_return_the_same_record_shape(team, monkeypatch):
    factory, scenario = team
    results = {}
    for transport, task_id in (("rest", scenario.tasks["planned"]), ("mcp", scenario.tasks["active"])):
        _, version = await _state(factory, task_id)
        async with transport_api(transport, factory, monkeypatch) as call:
            ok, results[transport] = await _postpone(call, PM_KEY, task_id, version, "shape")
            assert ok, results[transport]
    rest, mcp = results["rest"], results["mcp"]
    assert set(rest) == set(mcp) and set(rest["task"]) == set(mcp["task"])
    assert set(rest["postponement"]) == set(mcp["postponement"])
    assert rest["postponement"]["requirements"][0].keys() == mcp["postponement"]["requirements"][0].keys()
    assert (rest["task"]["status"], mcp["task"]["status"]) == ("postponed", "postponed")
    assert rest["postponement"]["from_status"] == "planned" and mcp["postponement"]["from_status"] == "active"


async def test_an_mcp_retry_with_the_same_key_replays_the_receipt(team, monkeypatch):
    factory, scenario = team
    task_id = scenario.tasks["planned"]
    _, version = await _state(factory, task_id)
    async with transport_api("mcp", factory, monkeypatch) as call:
        first = await _postpone(call, PM_KEY, task_id, version, "postpone-once")
        again = await _postpone(call, PM_KEY, task_id, version, "postpone-once")
    assert first[0] and first == again
    assert await _state(factory, task_id) == ("postponed", version + 1)


REFUSED = {
    OTHER_PM_KEY: ("not_found", "inaccessible"),
    VIEWER_KEY: ("permission_denied",),
    READER_KEY: ("scope",),
    WORKER_KEY: ("postpone_decider_required",),
    VERIFIER_KEY: ("postpone_decider_required",),
}


@pytest.mark.parametrize("transport", ["rest", "mcp"])
@pytest.mark.parametrize("key", [OTHER_PM_KEY, VIEWER_KEY, READER_KEY, WORKER_KEY, VERIFIER_KEY])
async def test_other_credentials_cannot_postpone_or_reactivate(team, transport, key, monkeypatch):
    factory, scenario = team
    planned, held = scenario.tasks["planned"], scenario.tasks["active"]
    _, planned_version = await _state(factory, planned)
    _, held_version = await _state(factory, held)
    async with transport_api(transport, factory, monkeypatch) as call:
        ok, seeded = await _postpone(call, PM_KEY, held, held_version, "seed")
        assert ok, seeded
        postponed_version = seeded["task"]["version"]
        refusals = [
            await _postpone(call, key, planned, planned_version, "refused-postpone"),
            await _reactivate(call, key, held, postponed_version, "refused-reactivate"),
        ]
    for ok, detail in refusals:
        assert not ok, detail
    assert await _state(factory, planned) == ("planned", planned_version)
    assert await _state(factory, held) == ("postponed", postponed_version)
    assert all(any(marker in detail for marker in REFUSED[key]) for _, detail in refusals), refusals


@pytest.mark.parametrize("transport", ["rest", "mcp"])
async def test_reading_a_postponement_needs_read_access_to_the_project(team, transport, monkeypatch):
    factory, scenario = team
    task_id = scenario.tasks["planned"]
    _, version = await _state(factory, task_id)
    async with transport_api(transport, factory, monkeypatch) as call:
        ok, _ = await _postpone(call, PM_KEY, task_id, version, "seed")
        assert ok
        assert (await _read(call, READER_KEY, task_id))[0]
        assert (await _read(call, VIEWER_KEY, task_id))[0]
        ok, detail = await _read(call, OTHER_PM_KEY, task_id)
        assert not ok, detail
        ok, never = await _read(call, PM_KEY, scenario.tasks["active"])
        assert not ok and "never been postponed" in never


async def _tool(factory, monkeypatch, name, **arguments):
    monkeypatch.setattr(mcp_server, "_session_factory", factory)
    server = mcp_server.create_mcp_server()
    application = mcp_server.MCPAgentKeyMiddleware(server.streamable_http_app())
    async with server.session_manager.run():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application),
                                     base_url="http://localhost:8001") as http:
            response = await http.post("/", headers={"X-Agent-API-Key": PM_KEY,
                                                     "Accept": "application/json, text/event-stream"},
                                       json={"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                                             "params": {"name": name, "arguments": arguments}})
    result = response.json()["result"]
    assert not result["isError"], result
    value = result["structuredContent"]
    return value.get("result", value) if isinstance(value, dict) and set(value) == {"result"} else value


def _rows(tree):
    for row in tree:
        yield row
        yield from _rows(row.get("children") or [])


async def test_postponed_work_is_listed_filtered_and_never_queued(team, monkeypatch):
    factory, scenario = team
    task_id = scenario.tasks["planned"]
    async with factory() as db:
        task = await db.get(Task, task_id)
        project_id = task.project_id
        # Agent-ready: labelled and scheduled, so only the postponed status can remove it from the queue.
        capability = sorted(DEFAULT_AGENT_CAPABILITY_SLUGS)[0]
        task.tags = json.dumps(["agent", capability])
        task.description = "Implement the change described by the brief, with tests, and report the result clearly."
        task.start_date, task.end_date = utc_now().date(), utc_now().date() + timedelta(days=2)
        await db.commit()
        version = task.version

    queued = await _tool(factory, monkeypatch, "agent_list_ready_tasks", limit=200)
    assert task_id in [row["id"] for row in queued]
    async with transport_api("mcp", factory, monkeypatch) as call:
        ok, held = await _postpone(call, PM_KEY, task_id, version, "list-seed")
        assert ok, held

    queued = await _tool(factory, monkeypatch, "agent_list_ready_tasks", limit=200)
    assert task_id not in [row["id"] for row in queued]
    listed = await _tool(factory, monkeypatch, "workspace_list_project_tasks", project_id=project_id)
    assert {row["id"]: row["status"] for row in _rows(listed)}[task_id] == "postponed"
    only = await _tool(factory, monkeypatch, "workspace_list_project_tasks", project_id=project_id, status="postponed")
    assert task_id in [row["id"] for row in _rows(only)]
    assert {row["status"] for row in _rows(only) if not row.get("children")} == {"postponed"}
    closed = await _tool(factory, monkeypatch, "workspace_list_project_tasks", project_id=project_id, status="closed")
    assert task_id not in [row["id"] for row in _rows(closed)]
