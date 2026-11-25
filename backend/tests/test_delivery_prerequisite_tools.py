"""Agents read GitHub reconciliation, run catch-up and retarget delivery prerequisites with the REST authority."""

import json
from contextlib import asynccontextmanager
from datetime import timedelta

import httpx
import pytest
from sqlalchemy import select

from app import mcp_server
from app.authority import internal_authority
from app.models.agent import AgentActor, TaskEvent
from app.models.delivery_dependency import DeliveryDependency
from app.models.identity import Principal, ProjectMembership
from app.models.project import Project
from app.models.task import Task
from app.models.user_session import UserSession
from app.services.agent_service import hash_api_key
from app.services.external_link_service import ExternalLinkService
from app.services.identity_service import digest
from app.utils.time import utc_now
from tests.test_delivery_scenarios import delivery_store  # noqa: F401
from tests.test_github_reconciliation import MERGE, REPO, github  # noqa: F401
from tests.test_managed_authority import client, managed_store  # noqa: F401

PM_KEY = "delivery-tools-pm-key"
OTHER_PM_KEY = "delivery-tools-other-pm-key"
VIEWER_KEY = "delivery-tools-viewer-key"
READER_KEY = "delivery-tools-read-scope-key"
OBSERVER_TOKEN = "o" * 43
NEW_TOOLS = {
    "agent_get_github_reconciliation": {"task_id"},
    "agent_run_github_catch_up": {"task_id"},
    "agent_list_delivery_dependencies": {"task_id"},
    "agent_add_delivery_dependency": {"task_id", "payload", "idempotency_key", "rationale", "correlation_id"},
    "agent_retarget_delivery_dependency": {"task_id", "edge_id", "payload", "idempotency_key", "rationale",
                                           "correlation_id"},
}


async def _agent(db, key, name, *, scopes, memberships):
    actor = AgentActor(name=name, display_name=name, role="pm", api_key_hash=hash_api_key(key), scopes=json.dumps(scopes))
    db.add(actor)
    await db.flush()
    principal = Principal(kind="agent", display_name=name, agent_actor_id=actor.id)
    db.add(principal)
    await db.flush()
    db.add_all([ProjectMembership(principal_id=principal.id, project_id=project, role=role)
                for project, role in memberships.items()])


@pytest.fixture
async def team(managed_store):
    """The PM manages both projects; the others are refused for team scope, project role or credential scope."""
    factory, scenario, _, principal_ids = managed_store
    prerequisite, dependent = scenario.tasks["planned"], scenario.tasks["other_project"]
    both = scenario.projects
    async with factory() as db:
        elsewhere = Project(name="Elsewhere")
        db.add(elsewhere)
        await db.flush()
        write = ["planning:read", "planning:write"]
        await _agent(db, PM_KEY, "Delivery PM", scopes=write, memberships={p: "manager" for p in both})
        await _agent(db, OTHER_PM_KEY, "Other team PM", scopes=write, memberships={elsewhere.id: "manager"})
        await _agent(db, VIEWER_KEY, "Viewing PM", scopes=write, memberships={p: "viewer" for p in both})
        await _agent(db, READER_KEY, "Read-scoped PM", scopes=["planning:read"], memberships={p: "manager" for p in both})
        # The person already edits the dependent's project; as an observer they may manage both and change nothing.
        db.add(ProjectMembership(principal_id=principal_ids[1], project_id=both[0], role="manager"))
        db.add(UserSession(principal_id=principal_ids[1], session_token_hash=digest(OBSERVER_TOKEN), access="observe",
                           ip_address="192.0.2.9", user_agent="observer", authenticated_at=utc_now(),
                           expires_at=utc_now() + timedelta(hours=1)))
        with internal_authority(db):
            link = await ExternalLinkService(db).create_task_github_link(prerequisite, f"{REPO}/pull/39", commit=False)
            reviewer = Principal(kind="human", display_name="Independent reviewer")
            db.add(reviewer)
            await db.flush()
            task = await db.get(Task, prerequisite)
            task.status, task.accepted_at, task.accepted_version = "closed", utc_now(), task.version
            task.accepted_by_principal_id = reviewer.id
        await db.commit()
        link_id = link.id
    return factory, prerequisite, dependent, link_id


async def _observe_merge(factory, link_id, base):
    from app.models.external_link import ExternalLink
    async with factory() as db:
        with internal_authority(db):
            link = await db.get(ExternalLink, link_id)
            link.status = "merged"
            link.metadata_json = {**link.metadata_json, "base_ref": base, "merge_commit_sha": MERGE,
                                  "observed_at": "2026-11-24T10:00:00Z"}
        await db.commit()


async def _version(factory, task_id):
    async with factory() as db:
        with internal_authority(db):
            return (await db.get(Task, task_id)).version


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
                        args.update(payload=body, idempotency_key=receipt, rationale="Follow the prerequisite branch",
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
                    if body is not None:
                        value = value["result"]["delivery_dependencies"]
                    return True, value
                response = await http.request(method, path, headers=headers, json=body)
                if response.status_code >= 400:
                    return False, f"{response.status_code} {response.text}"
                return True, response.json()
            yield call


@asynccontextmanager
async def _nothing():
    yield


def _retarget(call, key, task_id, edge_id, version, branch, receipt):
    return call(key, "agent_retarget_delivery_dependency", "PATCH",
                f"/api/tasks/{task_id}/delivery-dependencies/{edge_id}",
                arguments={"task_id": task_id, "edge_id": edge_id},
                body={"expected_version": version, "target_branch": branch}, receipt=receipt)


def _add(call, key, task_id, target_id, version, branch, receipt):
    return call(key, "agent_add_delivery_dependency", "POST", f"/api/tasks/{task_id}/delivery-dependencies",
                arguments={"task_id": task_id},
                body={"kind": "task", "target_id": target_id, "expected_version": version, "target_branch": branch},
                receipt=receipt)


def _list(call, key, task_id):
    return call(key, "agent_list_delivery_dependencies", "GET", f"/api/tasks/{task_id}/delivery-dependencies",
                arguments={"task_id": task_id})


async def test_new_tools_declare_their_inputs_and_contract_features():
    from app.agent_contract import agent_contract_features
    from app.server_features import SERVER_FEATURES

    tools = {tool.name: tool for tool in await mcp_server.mcp.list_tools()}
    for name, fields in NEW_TOOLS.items():
        schema = tools[name].inputSchema
        assert set(schema["properties"]) == fields, name
        assert set(schema["required"]) == fields, name
        assert schema["properties"]["task_id"]["type"] == "integer"
    assert tools["agent_retarget_delivery_dependency"].inputSchema["properties"]["edge_id"]["type"] == "integer"
    assert tools["agent_get_github_reconciliation"].annotations.readOnlyHint
    assert not tools["agent_run_github_catch_up"].annotations.readOnlyHint
    features = agent_contract_features(include_skill_bundles=False)
    assert {"github-reconciliation-v1", "delivery-prerequisite-branches-v1"} <= set(features)
    assert "delivery-prerequisite-retarget-v1" in SERVER_FEATURES


def test_retarget_body_requires_an_explicit_branch_or_null():
    from pydantic import ValidationError
    from app.schemas.delivery_dependency import DeliveryDependencyRetarget

    with pytest.raises(ValidationError):
        DeliveryDependencyRetarget.model_validate({"expected_version": 1})
    with pytest.raises(ValidationError):
        DeliveryDependencyRetarget.model_validate({"expected_version": 1, "target_branch": "main", "kind": "task"})
    assert DeliveryDependencyRetarget.model_validate({"expected_version": 1, "target_branch": None}).target_branch is None


@pytest.mark.parametrize("transport", ["rest", "mcp"])
async def test_retarget_releases_and_holds_dependent_work_and_is_on_the_timeline(team, transport, monkeypatch):
    factory, prerequisite, dependent, link_id = team
    await _observe_merge(factory, link_id, "main")
    async with transport_api(transport, factory, monkeypatch) as call:
        ok, added = await _add(call, PM_KEY, dependent, prerequisite, await _version(factory, dependent), "release", "add-1")
        assert ok, added
        (edge,) = added
        assert edge["target_branch"] == "release" and not edge["ready"]
        assert edge["merge"]["state"] == "merged_on_other_branch" and edge["hold"]["next_owner"] == "pm"

        # Retargeting to the branch the accepted code merged on releases the dependent work.
        ok, released = await _retarget(call, PM_KEY, dependent, edge["id"], await _version(factory, dependent),
                                       "refs/heads/main", "retarget-1")
        assert ok, released
        assert released[0]["ready"] and released[0]["target_branch"] == "main" and released[0]["hold"] is None
        ok, listed = await _list(call, PM_KEY, dependent)
        assert ok and listed == released

        # Another branch holds it again; null keeps only the acceptance gate.
        ok, held = await _retarget(call, PM_KEY, dependent, edge["id"], await _version(factory, dependent),
                                   "release", "retarget-2")
        assert ok and not held[0]["ready"] and held[0]["hold"]["case"] == "merged_on_other_branch"
        ok, cleared = await _retarget(call, PM_KEY, dependent, edge["id"], await _version(factory, dependent),
                                      None, "retarget-3")
        assert ok and cleared[0]["ready"] and cleared[0]["target_branch"] is None and cleared[0]["merge"] is None

        # A stale version is refused; the same branch again is a no-op that keeps the version.
        version = await _version(factory, dependent)
        ok, stale = await _retarget(call, PM_KEY, dependent, edge["id"], version - 1, "main", "retarget-stale")
        assert not ok and "version" in stale
        ok, _ = await _retarget(call, PM_KEY, dependent, edge["id"], version, None, "retarget-same")
        assert ok and await _version(factory, dependent) == version
        ok, missing = await _retarget(call, PM_KEY, dependent, edge["id"] + 999, version, "main", "retarget-missing")
        assert not ok and "not found" in missing
        ok, invalid = await _retarget(call, PM_KEY, dependent, edge["id"], version, "bad branch", "retarget-bad")
        assert not ok and "branch" in invalid

    async with factory() as db:
        events = (await db.scalars(select(TaskEvent).where(TaskEvent.task_id == dependent,
            TaskEvent.event_type == "delivery_prerequisite_retargeted").order_by(TaskEvent.id))).all()
    payloads = [json.loads(event.payload) for event in events]
    assert [(p["previous_target_branch"], p["target_branch"]) for p in payloads] == [
        ("release", "main"), ("main", "release"), ("release", None)]
    assert {event.actor_type for event in events} == {"agent"}
    assert {p["source"] for p in payloads} == {"mcp" if transport == "mcp" else "rest"}
    assert all(p["delivery_dependency_id"] == edge["id"] and p["target_id"] == prerequisite for p in payloads)


async def test_an_mcp_retry_with_the_same_key_replays_the_receipt(team, monkeypatch):
    factory, prerequisite, dependent, _ = team
    async with transport_api("mcp", factory, monkeypatch) as call:
        ok, (edge,) = await _add(call, PM_KEY, dependent, prerequisite, await _version(factory, dependent), None, "add")
        assert ok
        version = await _version(factory, dependent)
        first = await _retarget(call, PM_KEY, dependent, edge["id"], version, "main", "retarget-once")
        again = await _retarget(call, PM_KEY, dependent, edge["id"], version, "main", "retarget-once")
    assert first == again and first[0]
    assert await _version(factory, dependent) == version + 1


REFUSED = {OTHER_PM_KEY: ("404", "not_found", "inaccessible"), VIEWER_KEY: ("403", "permission_denied"),
           READER_KEY: ("403", "scope")}


@pytest.mark.parametrize("transport", ["rest", "mcp"])
@pytest.mark.parametrize("key", [OTHER_PM_KEY, VIEWER_KEY, READER_KEY])
async def test_another_teams_pm_and_read_only_credentials_change_nothing(team, github, transport, key, monkeypatch):
    factory, prerequisite, dependent, _ = team
    async with transport_api(transport, factory, monkeypatch) as call:
        ok, (edge,) = await _add(call, PM_KEY, dependent, prerequisite, await _version(factory, dependent), "main", "seed")
        assert ok
        version = await _version(factory, dependent)
        attempts = [
            await _retarget(call, key, dependent, edge["id"], version, "release", "refused-retarget"),
            await _add(call, key, prerequisite, dependent, await _version(factory, prerequisite), None, "refused-add"),
            await call(key, "agent_run_github_catch_up", "POST",
                       f"/api/tasks/{prerequisite}/github-reconciliation/catch-up", arguments={"task_id": prerequisite}),
        ]
        reads = [
            await call(key, "agent_get_github_reconciliation", "GET",
                       f"/api/tasks/{prerequisite}/github-reconciliation", arguments={"task_id": prerequisite}),
            await _list(call, key, dependent),
        ]
    for ok, detail in attempts:
        assert not ok and any(marker in detail for marker in REFUSED[key]), detail
    if key == OTHER_PM_KEY:
        assert not any(ok for ok, _ in reads)
    else:
        assert all(ok for ok, _ in reads), reads
    assert github.requests == []
    assert await _version(factory, dependent) == version
    async with factory() as db:
        with internal_authority(db):
            stored = (await db.scalars(select(DeliveryDependency).order_by(DeliveryDependency.id))).all()
    assert [(row.task_id, row.target_branch) for row in stored] == [(dependent, "main")]


async def test_an_observer_session_reads_but_cannot_retarget_or_catch_up(team, github):
    factory, prerequisite, dependent, _ = team
    async with client(**{"X-Agent-API-Key": PM_KEY}) as pm:
        added = await pm.post(f"/api/tasks/{dependent}/delivery-dependencies", json={
            "kind": "task", "target_id": prerequisite, "expected_version": await _version(factory, dependent),
            "target_branch": "main"})
        assert added.status_code == 200, added.text
    edge = added.json()[0]["id"]
    async with client(Authorization="Bearer " + OBSERVER_TOKEN) as observer:
        assert (await observer.get(f"/api/tasks/{dependent}/delivery-dependencies")).status_code == 200
        assert (await observer.get(f"/api/tasks/{prerequisite}/github-reconciliation")).status_code == 200
        retarget = await observer.patch(f"/api/tasks/{dependent}/delivery-dependencies/{edge}",
                                        json={"expected_version": await _version(factory, dependent), "target_branch": None})
        catch_up = await observer.post(f"/api/tasks/{prerequisite}/github-reconciliation/catch-up")
    for response in (retarget, catch_up):
        assert response.status_code == 403 and "read_only_credential" in response.text, response.text
    assert github.requests == []


@pytest.mark.parametrize("transport", ["rest", "mcp"])
async def test_catch_up_records_the_missed_merge_and_releases_the_dependent(team, github, transport, monkeypatch):
    factory, prerequisite, dependent, _ = team
    github.pull = github.payload("a" * 40, "2026-11-24T12:00:00Z", state="closed", merged_at="2026-11-24T12:00:00Z")
    async with transport_api(transport, factory, monkeypatch) as call:
        ok, (edge,) = await _add(call, PM_KEY, dependent, prerequisite, await _version(factory, dependent), "main", "add")
        assert ok and not edge["ready"] and "catch-up" in edge["hold"]["next_action"]
        ok, before = await call(PM_KEY, "agent_get_github_reconciliation", "GET",
                                f"/api/tasks/{prerequisite}/github-reconciliation", arguments={"task_id": prerequisite})
        assert ok and before["task_id"] == prerequisite and github.requests == []
        ok, view = await call(PM_KEY, "agent_run_github_catch_up", "POST",
                              f"/api/tasks/{prerequisite}/github-reconciliation/catch-up",
                              arguments={"task_id": prerequisite})
        assert ok, view
        assert view["pull_requests"][0]["state"] == "merged" and github.requests
        ok, again = await call(PM_KEY, "agent_run_github_catch_up", "POST",
                               f"/api/tasks/{prerequisite}/github-reconciliation/catch-up",
                               arguments={"task_id": prerequisite})
        assert ok and [pull["state"] for pull in again["pull_requests"]] == ["merged"]
        ok, (after,) = await _list(call, PM_KEY, dependent)
        assert ok and after["merge"]["state"] == "merged_on_target" and after["merge"]["verified"], json.dumps(after)
        # A recorded observation changes the prerequisite's version, so the merge
        # releases the dependent once the acceptance matches the current version.
        async with factory() as db:
            with internal_authority(db):
                task = await db.get(Task, prerequisite)
                task.accepted_version = task.version
            await db.commit()
        ok, (after,) = await _list(call, PM_KEY, dependent)
    assert ok and after["ready"] and after["hold"] is None, json.dumps(after)
    async with factory() as db:
        merges = (await db.scalars(select(TaskEvent).where(TaskEvent.task_id == prerequisite,
            TaskEvent.event_type.like("%merge%")))).all()
    assert len({event.event_type for event in merges}) == len(merges)


@pytest.mark.parametrize("transport", ["rest", "mcp"])
async def test_catch_up_records_every_linked_pull_requests_own_observation(team, github, transport, monkeypatch):
    from app.models.external_link import ExternalLink

    factory, prerequisite, _, first_link = team
    async with factory() as db:
        with internal_authority(db):
            for number in (40, 41):
                await ExternalLinkService(db).create_task_github_link(prerequisite, f"{REPO}/pull/{number}", commit=False)
        await db.commit()
    merged_at = "2026-11-24T12:00:00Z"
    github.pulls = {
        39: github.payload("1" * 40, "2026-11-24T10:00:00Z", number=39),
        40: github.payload("2" * 40, merged_at, number=40, state="closed", merged_at=merged_at),
        41: github.payload("3" * 40, merged_at, number=41, state="closed"),
    }
    github.pulls[41]["closed_at"] = merged_at
    async with transport_api(transport, factory, monkeypatch) as call:
        for _ in range(2):
            ok, view = await call(PM_KEY, "agent_run_github_catch_up", "POST",
                                  f"/api/tasks/{prerequisite}/github-reconciliation/catch-up",
                                  arguments={"task_id": prerequisite})
            assert ok, view
    seen = {pull["url"].rsplit("/", 1)[-1]: (pull["state"], pull["observed_head_sha"]) for pull in view["pull_requests"]}
    assert seen == {"39": ("open", "1" * 40), "40": ("merged", "2" * 40), "41": ("closed_unmerged", "3" * 40)}
    async with factory() as db:
        with internal_authority(db):
            links = (await db.scalars(select(ExternalLink).where(ExternalLink.entity_id == prerequisite)
                                      .order_by(ExternalLink.id))).all()
            events = (await db.scalars(select(TaskEvent).where(
                TaskEvent.task_id == prerequisite, TaskEvent.event_type.in_(["github_pr_merged", "github_pr_closed"])
            ))).all()
    assert [(link.status, link.metadata_json["head_sha"]) for link in links] == [
        ("open", "1" * 40), ("merged", "2" * 40), ("closed", "3" * 40)]
    assert sorted(event.event_type for event in events) == ["github_pr_closed", "github_pr_merged"]
