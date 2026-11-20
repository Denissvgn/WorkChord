"""Authenticated recovery and claim-fenced blocker reporting."""

from contextlib import asynccontextmanager, nullcontext
import json

import httpx
import pytest
from sqlalchemy import select

from app import database, mcp_server
from app.config import get_settings
from app.main import app
from app.models.agent import AgentActor, AgentRun, AgentTaskAssignment, TaskEvent
from app.models.capacity import PlanningState
from app.models.identity import ProjectMembership, WorkspaceMembership
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.task import Task
from app.services.identity_service import IdentityService, initialize_control_plane
from tests.test_agent_team_setup_qualification import provision_ready_topology, routing_base
from tests.test_team_pm_dispatch import db_session_factory


@asynccontextmanager
async def recovery_api(transport, factory, monkeypatch):
    monkeypatch.setattr(database, "async_session_maker", factory)
    monkeypatch.setattr(mcp_server, "_session_factory", factory)
    server = mcp_server.create_mcp_server() if transport == "mcp" else None
    application = mcp_server.MCPAgentKeyMiddleware(server.streamable_http_app()) if server else app
    async with server.session_manager.run() if server else nullcontext():
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=application),
                                     base_url="http://localhost:8001") as client:
            async def call(tool, path, key, *, task_id=None, payload=None, receipt=None, error=None):
                headers = {"X-Agent-API-Key": key}
                args = {}
                if task_id is not None:
                    args["task_id"] = task_id
                if payload is not None:
                    args.update(payload=payload, idempotency_key=receipt)
                    headers["Idempotency-Key"] = receipt
                if tool == "agent_requeue_recovery":
                    rationale = "Resume interrupted work with the selected worker"
                    args.update(rationale=rationale, correlation_id=receipt)
                    headers.update({"X-Agent-Rationale": rationale, "X-Correlation-ID": receipt})
                if server:
                    headers["Accept"] = "application/json, text/event-stream"
                    response = await client.post("/", headers=headers, json={
                        "jsonrpc": "2.0", "id": 1, "method": "tools/call",
                        "params": {"name": tool, "arguments": args},
                    })
                    assert response.status_code == 200, response.text
                    result = response.json()["result"]
                    if error:
                        assert result["isError"] and error in result["content"][0]["text"], result
                        return
                    assert not result["isError"], result
                    return json.loads(result["content"][0]["text"])
                response = await client.request("GET" if payload is None else "POST", path, headers=headers, json=payload)
                if error:
                    assert response.status_code == 409 and error in response.text, response.text
                    return
                assert response.status_code == 200, response.text
                return response.json()

            yield call


@pytest.mark.usefixtures("deployed_agent_skill_release")
@pytest.mark.parametrize("transport", ["rest", "mcp"])
@pytest.mark.parametrize("auth_mode", ["trusted_local", "managed"])
@pytest.mark.parametrize("db_session_factory", [
    pytest.param("sqlite", marks=pytest.mark.sqlite),
    pytest.param("postgresql", marks=[pytest.mark.postgresql, pytest.mark.allow_network]),
], indirect=True)
async def test_controller_recovers_once_and_worker_begins(
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
    worker_key = team.manifest.workers[0].actor_key
    worker = team.actors[worker_key]
    pm = team.actors[team.manifest.controller.actor_key]
    other_pm = other.actors[other.manifest.controller.actor_key]
    outsider = other.actors[other.manifest.workers[0].actor_key]
    base = await routing_base(db_session, topology=team, actor_key=worker_key,
                              team_member_factory=team_member_factory, task_factory=task_factory,
                              title="Resume interrupted deployment")
    task = base.task
    task.status, task.effort_hours = "active", 8
    if auth_mode == "managed":
        project = Project(name="Release tools")
        db_session.add(project)
        await db_session.flush()
        iteration = await db_session.get(Iteration, task.iteration_id)
        iteration.project_id = task.project_id = project.id
        for actor, role in ((pm, "manager"), (worker, "executor"), (other_pm, "manager")):
            identity = await IdentityService(db_session).actor_context(actor)
            db_session.add_all([
                WorkspaceMembership(principal_id=identity.principal_id, role="member"),
                ProjectMembership(principal_id=identity.principal_id, project_id=project.id, role=role),
            ])
    old = AgentTaskAssignment(task_id=task.id, actor_id=worker.id, task_version=task.version,
                              state="cancelled", purpose="execution")
    db_session.add(old)
    db_session.add(TaskEvent(task_id=task.id, actor_id=worker.id, actor_type="agent",
                             event_type="agent.work_recovery_required", payload="{}"))
    await db_session.commit()
    pm_key = team.sink.keys[team.manifest.controller.actor_key]
    outsider_pm_key = other.sink.keys[other.manifest.controller.actor_key]
    worker_secret = team.sink.keys[worker_key]
    requeue = "agent_requeue_recovery", f"/api/agent/recovery/{task.id}/requeue"
    work = "agent_get_my_work", "/api/agent/me/work"
    begin = "agent_begin_my_work", "/api/agent/me/work/begin"
    blocker = "agent_append_task_event", f"/api/agent/tasks/{task.id}/events"
    async with recovery_api(transport, db_session_factory, monkeypatch) as call:
        recovery = await call("agent_list_recovery_tasks", "/api/agent/recovery", pm_key)
        item, = recovery["items"]
        assert item["task"]["id"] == task.id and item["recovery_codes"] == [
            "active_execution_inconsistent", "pending_recovery_signal"]
        payload = dict(actor_id=worker.id, reason="Continue interrupted deployment",
                       expected_task_version=item["task"]["version"], expected_claim_generation=item["claim_generation"],
                       expected_live_assignment_ids=[], expected_running_run_ids=[])
        for caller, target in ((pm_key, outsider.id), (outsider_pm_key, outsider.id)):
            await call(*requeue, caller, task_id=task.id, payload={**payload, "actor_id": target},
                       receipt="outside-team", error="agent_team_actor_outside_topology")
        await call(*requeue, pm_key, task_id=task.id, payload={**payload, "expected_running_run_ids": [1]},
                   receipt="stale-runs", error="Recovery run ownership changed")
        queued = await call(*requeue, pm_key, task_id=task.id, payload=payload, receipt="resume-task")
        async def revisions():
            async with db_session_factory() as db:
                return (await db.scalar(select(PlanningState.revision)),
                        await db.scalar(select(Iteration.revision).where(Iteration.id == task.iteration_id)))

        queued_revisions = await revisions()
        assert queued == await call(*requeue, pm_key, task_id=task.id, payload=payload, receipt="resume-task")
        assert await revisions() == queued_revisions
        assignment = queued["assignment"]
        assert assignment["routing_snapshot"]["source_assignment_ids"] == [old.id]
        assert assignment["actor_id"] == worker.id and assignment["queue_class"] == "recovery"
        assert queued["cancelled_assignment_ids"] == queued["cancelled_run_ids"] == []
        decision = await call(*work, worker_secret)
        assert decision["state"] == "start_assigned" and decision["next"]["assignment"]["id"] == assignment["id"]
        start = dict(assignment_id=assignment["id"], queue_revision=decision["queue_revision"])
        monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "enforced")
        get_settings.cache_clear()
        await call(*begin, worker_secret, payload=start, receipt="enforced-start", error="routing_selection_pending")
        monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
        get_settings.cache_clear()
        receipt = await call(*begin, worker_secret, payload=start, receipt="begin-recovery")
        assert receipt["run"]["status"] == "running" and receipt["claim_generation"] == item["claim_generation"] + 1
        event = dict(event_type="agent.blocker", payload={"blocker": "Waiting for the deployment window"},
                     claim_id=receipt["claim_id"], claim_generation=receipt["claim_generation"])
        await call(*blocker, worker_secret, task_id=task.id, payload={**event, "claim_id": "expired-claim-token"},
                   receipt="stale-blocker", error="fence")
        recorded = await call(*blocker, worker_secret, task_id=task.id, payload=event, receipt="worker-blocker")
        repeated = await call(*blocker, worker_secret, task_id=task.id, payload=event, receipt="worker-blocker")
        assert recorded["id"] == repeated["id"]
    async with db_session_factory() as db:
        current = await db.get(Task, task.id)
        assert current.blocked_reason == event["payload"]["blocker"] and current.version == receipt["task"]["version"]
        assignments = (await db.scalars(select(AgentTaskAssignment).order_by(AgentTaskAssignment.id))).all()
        assert [(row.id, row.state) for row in assignments] == [(old.id, "cancelled"), (assignment["id"], "accepted")]
        assert (await db.scalars(select(AgentRun))).one().id == receipt["run"]["id"]
        assert (await db.get(AgentActor, worker.id)).queue_revision == worker.queue_revision + 2
        events = (await db.scalars(select(TaskEvent).where(TaskEvent.event_type.in_(
            ("agent.recovery_requeued", "agent.blocker"))).order_by(TaskEvent.id))).all()
        assert [(e.event_type, e.actor_id) for e in events] == [("agent.recovery_requeued", pm.id), ("agent.blocker", worker.id)]
        assert json.loads(events[0].payload)["routing_selection_pending"] is False


@pytest.mark.sqlite
@pytest.mark.usefixtures("deployed_agent_skill_release")
@pytest.mark.parametrize("foreign_owner", ["assignment", "run", "claim"])
async def test_recovery_retains_ownership_outside_the_controller_team(
    db_session, db_session_factory, team_member_factory, task_factory, actor_factory, monkeypatch, foreign_owner,
):
    team = await provision_ready_topology(db_session)
    worker_key = team.manifest.workers[0].actor_key
    worker = team.actors[worker_key]
    outsider = await actor_factory()
    base = await routing_base(db_session, topology=team, actor_key=worker_key,
                              team_member_factory=team_member_factory, task_factory=task_factory,
                              title="Recover interrupted work")
    task = base.task
    task.status = "active"
    assignment = AgentTaskAssignment(task_id=task.id, actor_id=outsider.id if foreign_owner == "assignment" else worker.id,
                                     task_version=task.version, state="accepted", purpose="execution")
    db_session.add(assignment)
    await db_session.flush()
    run = AgentRun(task_id=task.id, actor_id=outsider.id if foreign_owner == "run" else worker.id,
                   assignment_id=assignment.id, claim_generation=task.claim_generation)
    db_session.add(run)
    if foreign_owner == "claim":
        task.claimed_by = outsider.id
    await db_session.commit()
    payload = dict(actor_id=worker.id, reason="Reconcile stale ownership", expected_task_version=task.version,
                   expected_live_assignment_ids=[assignment.id], expected_running_run_ids=[run.id],
                   expected_claim_generation=task.claim_generation)
    async with recovery_api("rest", db_session_factory, monkeypatch) as call:
        await call("agent_requeue_recovery", f"/api/agent/recovery/{task.id}/requeue",
                   team.sink.keys[team.manifest.controller.actor_key], task_id=task.id, payload=payload,
                   receipt="reconcile-stale-owner", error="agent_team_actor_outside_topology")
    async with db_session_factory() as db:
        assert (await db.scalars(select(AgentTaskAssignment))).one().state == "accepted"
        assert (await db.scalars(select(AgentRun))).one().status == "running"
        preserved = await db.get(Task, task.id)
        assert (preserved.claimed_by, preserved.version) == (task.claimed_by, task.version)
        assert await db.scalar(select(TaskEvent.id).where(TaskEvent.event_type == "agent.recovery_requeued")) is None


@pytest.mark.sqlite
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_recovery_moves_stale_team_ownership_without_lowering_model_review(
    db_session, db_session_factory, team_member_factory, task_factory, monkeypatch,
):
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    get_settings.cache_clear()
    team = await provision_ready_topology(db_session)
    owner_key, target_key = (member.actor_key for member in team.manifest.workers)
    owner, target = team.actors[owner_key], team.actors[target_key]
    reviewer = team.actors[team.manifest.verifiers[0].actor_key]
    base = await routing_base(db_session, topology=team, actor_key=owner_key,
                              team_member_factory=team_member_factory, task_factory=task_factory,
                              title="Recover model-routed work")
    task = base.task
    task.status, task.effort_hours = "active", 8
    old = AgentTaskAssignment(task_id=task.id, actor_id=owner.id, task_version=task.version,
                              state="accepted", purpose="execution", reviewer_profile_id=reviewer.profile_id,
                              routing_snapshot=json.dumps({
                                  "schema_version": "routing-decision-snapshot-v1", "authority": "agent-routing-service-v1",
                                  "review_mode": "independent", "reviewer_profile_id": reviewer.profile_id,
                              }))
    db_session.add(old)
    await db_session.commit()
    payload = dict(actor_id=target.id, reason="Reassign interrupted work", expected_task_version=task.version,
                   expected_live_assignment_ids=[old.id], expected_running_run_ids=[], expected_claim_generation=task.claim_generation)
    async with recovery_api("rest", db_session_factory, monkeypatch) as call:
        result = await call("agent_requeue_recovery", f"/api/agent/recovery/{task.id}/requeue",
                            team.sink.keys[team.manifest.controller.actor_key], task_id=task.id, payload=payload,
                            receipt="recover-model-work")
        assert result["cancelled_assignment_ids"] == [old.id]
        assignment = result["assignment"]
        lineage = assignment["routing_snapshot"]
        assert lineage["prior_decisions"][0]["source_assignment_id"] == old.id
        assert lineage["review_floor"]["review_mode"] == "independent"
        assert lineage["review_floor"]["reviewer_profile_ids"] == [reviewer.profile_id]
        decision = await call("agent_get_my_work", "/api/agent/me/work", team.sink.keys[target_key])
        assert "routing_selection_pending" in decision["blocked_assigned"][0]["blocker_codes"]
        await call("agent_begin_my_work", "/api/agent/me/work/begin", team.sink.keys[target_key],
                   payload=dict(assignment_id=assignment["id"], queue_revision=decision["queue_revision"]),
                   receipt="begin-governed-work", error="routing_selection_pending")
    async with db_session_factory() as db:
        assert (await db.get(AgentTaskAssignment, old.id)).state == "cancelled"
        assert (await db.get(AgentTaskAssignment, assignment["id"])).state == "queued"
        for actor in (owner, target):
            assert (await db.get(AgentActor, actor.id)).queue_revision == actor.queue_revision + 1
