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
from app.services.agent_routing_policy import ROUTING_LINEAGE_AUTHORITY
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
            async def call(tool, path, key, *, task_id=None, payload=None, receipt=None, error=None, assignment_id=None):
                headers = {"X-Agent-API-Key": key}
                args = {}
                if assignment_id is not None:
                    args["assignment_id"] = assignment_id
                    path = f"{path}?assignment_id={assignment_id}"
                if task_id is not None:
                    args["task_id"] = task_id
                if payload is not None:
                    args.update(payload=payload, idempotency_key=receipt)
                    headers["Idempotency-Key"] = receipt
                if tool in {"agent_requeue_recovery", "agent_create_assignment", "agent_submit_review_verdict"}:
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
                assert response.status_code in {200, 201}, response.text
                return response.json()

            yield call


DATABASES = pytest.mark.parametrize("db_session_factory", [
    pytest.param("sqlite", marks=pytest.mark.sqlite),
    pytest.param("postgresql", marks=[pytest.mark.postgresql, pytest.mark.allow_network]),
], indirect=True)


def routing_mode(monkeypatch, mode):
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", mode)
    get_settings.cache_clear()


@pytest.mark.usefixtures("deployed_agent_skill_release")
@pytest.mark.parametrize("mode", ["off", "shadow"])
@pytest.mark.parametrize("transport", ["rest", "mcp"])
@pytest.mark.parametrize("auth_mode", ["trusted_local", "managed"])
@DATABASES
async def test_controller_recovers_once_and_worker_begins(
    db_session, db_session_factory, team_member_factory, task_factory, transport, auth_mode, mode, monkeypatch,
):
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", mode)
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
        assert assignment["routing_snapshot"]["supervised_actor_id"] == worker.id
        assert assignment["routing_snapshot"]["selection_pending"] is True
        assert queued["cancelled_assignment_ids"] == queued["cancelled_run_ids"] == []
        decision = await call(*work, worker_secret)
        assert decision["state"] == "start_assigned" and decision["next"]["assignment"]["id"] == assignment["id"]
        assert decision["next"]["blocker_codes"] == [] and decision["blocked_assigned"] == []
        start = dict(assignment_id=assignment["id"], queue_revision=decision["queue_revision"])
        routing_mode(monkeypatch, "enforced")
        await call(*begin, worker_secret, payload=start, receipt="enforced-start", error="routing_selection_pending")
        routing_mode(monkeypatch, mode)
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


async def recovery_events(factory):
    async with factory() as db:
        return (await db.scalars(select(TaskEvent).where(TaskEvent.event_type == "agent.recovery_requeued"))).all()


async def refused_requeue(factory, monkeypatch, task_id, key, payload, receipt):
    monkeypatch.setattr(database, "async_session_maker", factory)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://localhost:8001") as client:
        response = await client.post(f"/api/agent/recovery/{task_id}/requeue", json=payload, headers={
            "X-Agent-API-Key": key, "Idempotency-Key": receipt, "X-Correlation-ID": receipt,
            "X-Agent-Rationale": "Resume interrupted work with the selected worker"})
    assert response.status_code == 409, response.text
    detail = response.json()["detail"]
    assert detail["code"] == "recovery_supervision_unavailable" and detail["effective_mode"] == "shadow"
    return detail


@pytest.mark.usefixtures("deployed_agent_skill_release")
@pytest.mark.parametrize("mode", ["off", "shadow", "enforced"])
@DATABASES
async def test_recovery_moves_stale_team_ownership_without_lowering_model_review(
    db_session, db_session_factory, team_member_factory, task_factory, monkeypatch, mode,
):
    routing_mode(monkeypatch, mode)
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
    pm_key, target_secret = team.sink.keys[team.manifest.controller.actor_key], team.sink.keys[target_key]
    if mode == "shadow":
        # Shadow cannot complete a fresh model-aware selection, so it refuses before anything changes.
        detail = await refused_requeue(db_session_factory, monkeypatch, task.id, pm_key, payload, "recover-model-work")
        assert detail["condition"] == "model_aware_history" and detail["model_aware_assignment_ids"] == [old.id]
        assert "enforced routing" in detail["message"]
        async with db_session_factory() as db:
            assert (await db.get(AgentTaskAssignment, old.id)).state == "accepted"
            assert len((await db.scalars(select(AgentTaskAssignment))).all()) == 1
            assert (await db.get(Task, task.id)).version == task.version
            for actor in (owner, target):
                assert (await db.get(AgentActor, actor.id)).queue_revision == actor.queue_revision
        assert await recovery_events(db_session_factory) == []
        return
    async with recovery_api("rest", db_session_factory, monkeypatch) as call:
        result = await call("agent_requeue_recovery", f"/api/agent/recovery/{task.id}/requeue",
                            pm_key, task_id=task.id, payload=payload, receipt="recover-model-work")
        assert result["cancelled_assignment_ids"] == [old.id]
        assignment = result["assignment"]
        lineage = assignment["routing_snapshot"]
        assert lineage["prior_decisions"][0]["source_assignment_id"] == old.id
        assert lineage["review_floor"]["review_mode"] == "independent"
        assert lineage["review_floor"]["reviewer_profile_ids"] == [reviewer.profile_id]
        decision = await call("agent_get_my_work", "/api/agent/me/work", target_secret)
        start = dict(assignment_id=assignment["id"], queue_revision=decision["queue_revision"])
        if mode == "enforced":
            assert "supervised_actor_id" not in lineage and assignment["reviewer_profile_id"] is None
            assert "routing_selection_pending" in decision["blocked_assigned"][0]["blocker_codes"]
            await call("agent_begin_my_work", "/api/agent/me/work/begin", target_secret,
                       payload=start, receipt="begin-governed-work", error="routing_selection_pending")
        else:
            assert lineage["supervised_actor_id"] == target.id
            assert assignment["reviewer_profile_id"] == reviewer.profile_id
            assert decision["state"] == "start_assigned" and decision["next"]["blocker_codes"] == []
            begun = await call("agent_begin_my_work", "/api/agent/me/work/begin", target_secret,
                               payload=start, receipt="begin-supervised-work")
            assert begun["run"]["status"] == "running" and begun["assignment"]["state"] == "accepted"
    async with db_session_factory() as db:
        assert (await db.get(AgentTaskAssignment, old.id)).state == "cancelled"
        assert (await db.get(AgentTaskAssignment, assignment["id"])).state == (
            "queued" if mode == "enforced" else "accepted")
        assert (await db.get(AgentActor, owner.id)).queue_revision == owner.queue_revision + 1
        assert (await db.get(AgentActor, target.id)).queue_revision == target.queue_revision + (
            1 if mode == "enforced" else 2)
    event, = await recovery_events(db_session_factory)
    assert json.loads(event.payload)["routing_selection_pending"] is (mode == "enforced")


@pytest.mark.usefixtures("deployed_agent_skill_release")
@pytest.mark.parametrize("mode", ["off", "shadow"])
@pytest.mark.parametrize("history", ["several_reviewer_profiles", "target_is_reviewer", "pm_outside_team",
                                     "unsupervised_rework"])
@DATABASES
async def test_recovery_outside_enforcement_is_executable_or_names_its_condition(
    db_session, db_session_factory, team_member_factory, task_factory, actor_factory, monkeypatch, mode, history,
):
    from app.services.agent_service import hash_api_key
    from tests.test_supervised_shadow_rework import topology_with_two_reviewers

    routing_mode(monkeypatch, mode)
    team = await topology_with_two_reviewers(db_session)
    worker_key = team.manifest.workers[0].actor_key
    worker = team.actors[worker_key]
    reviewer, alternate = (team.actors[member.actor_key] for member in team.manifest.verifiers[:2])
    pm = team.actors[team.manifest.controller.actor_key]
    pm_key = team.sink.keys[team.manifest.controller.actor_key]
    if history == "pm_outside_team":
        pm_key = "outside-team-recovery-pm-key"
        pm = await actor_factory(role="pm", api_key_hash=hash_api_key(pm_key), scopes=json.dumps([
            "recovery:write", "recovery:read", "assignments:read", "tasks:read"]))
    base = await routing_base(db_session, topology=team, actor_key=worker_key,
                              team_member_factory=team_member_factory, task_factory=task_factory,
                              title="Recover reviewed work")
    task = base.task
    task.status, task.effort_hours = "active", 8
    reviewer_profile_id = worker.profile_id if history == "target_is_reviewer" else reviewer.profile_id
    old = AgentTaskAssignment(task_id=task.id, actor_id=worker.id, task_version=task.version,
                              state="accepted", purpose="execution", reviewer_profile_id=reviewer_profile_id)
    db_session.add(old)
    if history == "several_reviewer_profiles":
        db_session.add(AgentTaskAssignment(task_id=task.id, actor_id=worker.id, task_version=task.version,
                                           state="cancelled", purpose="execution", reviewer_profile_id=alternate.profile_id))
    rework = None
    if history == "unsupervised_rework":
        # A rework that never began as a supervised handback still waits on a model-aware selection.
        rework = AgentTaskAssignment(task_id=task.id, actor_id=worker.id, task_version=task.version, state="cancelled",
                                     purpose="execution", queue_class="rework", routing_snapshot=json.dumps({
                                         "schema_version": "routing-lineage-snapshot-v1",
                                         "authority": ROUTING_LINEAGE_AUTHORITY, "selection_pending": True}))
        db_session.add(rework)
    await db_session.commit()
    payload = dict(actor_id=worker.id, reason="Resume reviewed work", expected_task_version=task.version,
                   expected_live_assignment_ids=[old.id], expected_running_run_ids=[], expected_claim_generation=task.claim_generation)
    worker_secret = team.sink.keys[worker_key]
    requeue = "agent_requeue_recovery", f"/api/agent/recovery/{task.id}/requeue"
    if mode == "shadow":
        condition = {"several_reviewer_profiles": "reviewer_profile_ambiguous",
                     "target_is_reviewer": "reviewer_profile_not_independent",
                     "pm_outside_team": "primary_pm_required",
                     "unsupervised_rework": "model_aware_history"}[history]
        detail = await refused_requeue(db_session_factory, monkeypatch, task.id, pm_key, payload, "refused-recovery")
        assert detail["condition"] == condition and detail["actor_id"] == worker.id
        if history == "several_reviewer_profiles":
            assert detail["reviewer_profile_ids"] == sorted([reviewer.profile_id, alternate.profile_id])
        if history == "unsupervised_rework":
            assert detail["model_aware_assignment_ids"] == [rework.id]
        async with recovery_api("mcp", db_session_factory, monkeypatch) as call:
            await call(*requeue, pm_key, task_id=task.id, payload=payload, receipt="refused-recovery-mcp", error=condition)
        async with db_session_factory() as db:
            assert (await db.get(AgentTaskAssignment, old.id)).state == "accepted"
            assert (await db.get(Task, task.id)).version == task.version
            assert (await db.get(AgentActor, worker.id)).queue_revision == worker.queue_revision
        assert await recovery_events(db_session_factory) == []
        return
    if history == "pm_outside_team":
        # Off mode does not widen who may move a team's queue.
        monkeypatch.setattr(database, "async_session_maker", db_session_factory)
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://localhost:8001") as client:
            denied = await client.post(f"/api/agent/recovery/{task.id}/requeue", json=payload, headers={
                "X-Agent-API-Key": pm_key, "Idempotency-Key": "outside-recovery", "X-Correlation-ID": "outside-recovery",
                "X-Agent-Rationale": "Resume interrupted work with the selected worker"})
        assert denied.status_code == 403 and denied.json()["detail"]["code"] == "permission_denied", denied.text
        async with db_session_factory() as db:
            assert (await db.get(AgentTaskAssignment, old.id)).state == "accepted"
        assert await recovery_events(db_session_factory) == []
        return
    async with recovery_api("rest", db_session_factory, monkeypatch) as call:
        queued = await call(*requeue, pm_key, task_id=task.id, payload=payload, receipt="supervised-recovery")
        assignment = queued["assignment"]
        assert queued["cancelled_assignment_ids"] == [old.id]
        assert assignment["routing_snapshot"]["supervised_actor_id"] == worker.id
        # Only a single independent reviewer profile carries over; the full floor stays in the lineage.
        assert assignment["reviewer_profile_id"] == (reviewer.profile_id if history == "unsupervised_rework" else None)
        assert set(assignment["routing_snapshot"]["review_floor"]["reviewer_profile_ids"]) == {
            reviewer_profile_id, *([alternate.profile_id] if history == "several_reviewer_profiles" else [])}
        decision = await call("agent_get_my_work", "/api/agent/me/work", worker_secret)
        assert decision["state"] == "start_assigned" and decision["next"]["assignment"]["id"] == assignment["id"]
        assert decision["next"]["blocker_codes"] == []
        start = dict(assignment_id=assignment["id"], queue_revision=decision["queue_revision"])
        receipt = await call("agent_begin_my_work", "/api/agent/me/work/begin", worker_secret,
                             payload=start, receipt="begin-supervised-recovery")
        assert receipt["run"]["status"] == "running" and receipt["claim_generation"] == task.claim_generation + 1
        event = dict(event_type="agent.blocker", payload={"blocker": "Waiting for review notes"},
                     claim_id=receipt["claim_id"], claim_generation=receipt["claim_generation"])
        blocker = "agent_append_task_event", f"/api/agent/tasks/{task.id}/events"
        await call(*blocker, worker_secret, task_id=task.id, payload={**event, "claim_id": "expired-claim-token"},
                   receipt="stale-blocker", error="fence")
        await call(*blocker, worker_secret, task_id=task.id, payload=event, receipt="fenced-blocker")
        # The begun recovery is healthy ownership that a repeated requeue cannot cancel.
        async with db_session_factory() as db:
            current_version = (await db.get(Task, task.id)).version
        await call(*requeue, pm_key, task_id=task.id, receipt="requeue-healthy-work", payload={
            **payload, "expected_task_version": current_version,
            "expected_live_assignment_ids": [assignment["id"]], "expected_running_run_ids": [receipt["run"]["id"]],
            "expected_claim_generation": receipt["claim_generation"]}, error="healthy accepted assignment")
    async with db_session_factory() as db:
        assert (await db.get(AgentTaskAssignment, assignment["id"])).state == "accepted"
        assert (await db.scalars(select(AgentRun))).one().id == receipt["run"]["id"]
    event_row, = await recovery_events(db_session_factory)
    assert event_row.actor_id == pm.id and json.loads(event_row.payload)["routing_selection_pending"] is False
