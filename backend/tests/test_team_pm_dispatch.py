"""Authenticated PM queue commands across the REST and MCP transports."""

from contextlib import asynccontextmanager, nullcontext
import json

import httpx
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app import database, mcp_server
from app.authority import AuthorityError
from app.commands import command_transaction
from app.config import get_settings
from app.main import app
from app.models.agent import AgentActor, AgentTaskAssignment, TaskEvent
from app.models.identity import ProjectMembership, WorkspaceMembership
from app.models.iteration import Iteration
from app.models.project import Project
from app.services.identity_service import IdentityService, initialize_control_plane
from tests.test_agent_team_setup_qualification import provision_ready_topology, routing_base


@pytest.fixture
async def db_session_factory(request, db_session_factory):
    if getattr(request, "param", "sqlite") == "sqlite":
        yield db_session_factory
        return
    database_target = request.getfixturevalue("postgres_database")
    engine = create_async_engine(database_target.url)
    try:
        async with engine.begin() as connection:
            await connection.run_sync(database.Base.metadata.create_all)
        yield async_sessionmaker(engine, expire_on_commit=False)
    finally:
        await engine.dispose()


@asynccontextmanager
async def assignment_api(transport, db_session_factory, monkeypatch):
    monkeypatch.setattr(database, "async_session_maker", db_session_factory)
    monkeypatch.setattr(mcp_server, "_session_factory", db_session_factory)
    server = mcp_server.create_mcp_server() if transport == "mcp" else None
    application = mcp_server.MCPAgentKeyMiddleware(server.streamable_http_app()) if server else app
    async with server.session_manager.run() if server else nullcontext():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application),
                                     base_url="http://localhost:8001") as client:
            async def send(key, payload, receipt, *, assignment_id=None, error=None):
                headers = {"X-Agent-API-Key": key}
                rationale = "Schedule a ready team member"
                if server:
                    headers["Accept"] = "application/json, text/event-stream"
                    arguments = dict(payload=payload, idempotency_key=receipt,
                                     rationale=rationale, correlation_id=receipt)
                    name = "agent_create_assignment"
                    if assignment_id is not None:
                        name = "agent_update_assignment"
                        arguments["assignment_id"] = assignment_id
                    response = await client.post("/", headers=headers, json={
                        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
                        "params": {"name": name, "arguments": arguments},
                    })
                    assert response.status_code == 200, response.text
                    result = response.json()["result"]
                    if error:
                        assert result["isError"] and error in result["content"][0]["text"], result
                        return
                    assert not result["isError"], result
                    return json.loads(result["content"][0]["text"])
                headers.update({"Idempotency-Key": receipt, "X-Agent-Rationale": rationale,
                                "X-Correlation-ID": receipt})
                path = "/api/agent/assignments"
                if assignment_id is None:
                    response = await client.post(path, headers=headers, json=payload)
                else:
                    response = await client.patch(f"{path}/{assignment_id}", headers=headers, json=payload)
                if error:
                    assert response.status_code == (403 if error == "permission_denied" else 409), response.text
                    assert response.json()["detail"]["code"] == error
                    return
                assert response.status_code == (201 if assignment_id is None else 200), response.text
                return response.json()

            yield send


@pytest.mark.usefixtures("deployed_agent_skill_release")
@pytest.mark.parametrize("transport", ["rest", "mcp"])
@pytest.mark.parametrize("auth_mode", ["trusted_local", "managed"])
@pytest.mark.parametrize("db_session_factory", [
    pytest.param("sqlite", marks=pytest.mark.sqlite),
    pytest.param("postgresql", marks=[pytest.mark.postgresql, pytest.mark.allow_network]),
], indirect=True)
async def test_pm_dispatch_changes_only_the_selected_team_queues(
    db_session, db_session_factory, team_member_factory, task_factory, transport, auth_mode, monkeypatch,
):
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", auth_mode)
    get_settings.cache_clear()
    if auth_mode == "managed":
        await initialize_control_plane(db_session)
        await db_session.commit()
    team = await provision_ready_topology(db_session)
    other = await provision_ready_topology(db_session, two_workers=False, prefix="other")
    worker_key, replacement_key = (member.actor_key for member in team.manifest.workers)
    base = await routing_base(db_session, topology=team, actor_key=worker_key,
                              team_member_factory=team_member_factory, task_factory=task_factory,
                              title="Prepare the release")
    if auth_mode == "managed":
        project = Project(name="Release tools")
        db_session.add(project)
        await db_session.flush()
        iteration = await db_session.get(Iteration, base.task.iteration_id)
        iteration.project_id = base.task.project_id = project.id
        for roster in (team, other):
            controller = roster.actors[roster.manifest.controller.actor_key]
            authority = await IdentityService(db_session).actor_context(controller)
            db_session.add_all([
                WorkspaceMembership(principal_id=authority.principal_id, role="member"),
                ProjectMembership(principal_id=authority.principal_id, project_id=project.id, role="manager"),
            ])
        await db_session.commit()
    pm_key = team.sink.keys[team.manifest.controller.actor_key]
    worker, replacement = team.actors[worker_key], team.actors[replacement_key]
    outsider = other.actors[other.manifest.workers[0].actor_key]
    reviewer = team.actors[team.manifest.verifiers[0].actor_key]
    payload = dict(task_id=base.task.id, expected_task_version=base.task.version,
                   actor_id=worker.id, team_member_id=base.member.id,
                   reviewer_profile_id=reviewer.profile_id, purpose="execution")
    outside = "agent_team_actor_outside_topology"
    async with assignment_api(transport, db_session_factory, monkeypatch) as send:
        await send(pm_key, {**payload, "actor_id": outsider.id}, "outside-create", error=outside)
        created = await send(pm_key, payload, "dispatch-worker")
        assert created["actor_id"] == worker.id and created["state"] == "queued"
        assert created["assigned_by_actor_id"] == base.pm.id
        assert await send(pm_key, payload, "dispatch-worker") == created

        move = dict(actor_id=replacement.id, expected_queue_revision=worker.queue_revision + 1)
        await send(pm_key, {**move, "actor_id": outsider.id}, "outside-move",
                   assignment_id=created["id"], error=outside)
        await send(other.sink.keys[other.manifest.controller.actor_key],
                   {**move, "actor_id": outsider.id}, "outside-source",
                   assignment_id=created["id"], error=outside)
        moved = await send(pm_key, move, "move-worker", assignment_id=created["id"])
        assert moved["actor_id"] == replacement.id
        if auth_mode == "managed":
            pm = await IdentityService(db_session).actor_context(base.pm)
            grant = await db_session.get(ProjectMembership, (pm.principal_id, project.id))
            grant.role = "viewer"
            await db_session.commit()
            await send(pm_key, payload, "read-only-project", error="permission_denied")

    async with db_session_factory() as db:
        assignment = (await db.scalars(select(AgentTaskAssignment))).one()
        assert assignment.id == created["id"] and assignment.actor_id == replacement.id
        for actor, increments in ((base.pm, 0), (worker, 2), (replacement, 1), (outsider, 0), (reviewer, 0)):
            assert (await db.get(AgentActor, actor.id)).queue_revision == actor.queue_revision + increments
        events = (await db.scalars(select(TaskEvent).where(TaskEvent.task_id == base.task.id)
                                   .order_by(TaskEvent.id))).all()
        assert [(event.event_type, event.actor_id) for event in events] == [
            ("agent.assignment_created", base.pm.id), ("agent.assignment_updated", base.pm.id)]


@pytest.mark.sqlite
@pytest.mark.parametrize("change", ["identity", "scopes", "delete", "second_advance"])
async def test_dispatch_queue_permission_is_single_use_and_excludes_actor_administration(
    db_session, db_session_factory, actor_factory, change,
):
    pm = await actor_factory(role="pm", scopes=json.dumps(["assignments:write", "planning:write"]))
    worker = await actor_factory()
    await db_session.commit()
    async with db_session_factory() as db:
        with pytest.raises(AuthorityError) as denied:
            async with command_transaction(db) as command:
                db.info["authority"] = await IdentityService(db).actor_context(pm, source="agent_rest")
                target = await db.get(AgentActor, worker.id)
                target.queue_revision += 1
                command.dispatch_queue_revisions.add((pm.id, target.id, target.queue_revision))
                if change == "identity":
                    target.display_name = "Renamed actor"
                elif change == "scopes":
                    target.scopes = json.dumps(["planning:read"])
                elif change == "delete":
                    await db.delete(target)
                else:
                    await db.flush()
                    target.queue_revision += 1
        assert denied.value.code == "operator_required"
    async with db_session_factory() as db:
        target = await db.get(AgentActor, worker.id)
        assert (target.queue_revision, target.display_name, target.scopes) == (
            worker.queue_revision, worker.display_name, worker.scopes)
