"""Separate-process protocol simulation; no provider or pilot acceptance implied."""

import asyncio
from datetime import date, timedelta
import json
import os
import sys

import httpx
import pytest
from sqlalchemy import select

from app.main import app
from app.models.agent import AgentActor, AgentTaskAssignment, AgentRun
from app.models.task import Task
from app.schemas.task import TaskCreate
from app.schemas.task import TaskUpdate
from app.schemas.task_brief import BriefCriterion, BriefWrite, TaskBrief
from app.services.task_brief_service import TaskBriefService
from app.services.task_service import TaskService
from app.services.agent_service import hash_api_key
from app.utils.time import utc_now
from tests.test_delivery_scenarios import delivery_store


async def peer(factory, key, action, *, body=None, idempotency_key=None, **extra):
    database_url = factory.kw["bind"].url.render_as_string(hide_password=False)
    process = await asyncio.create_subprocess_exec(
        sys.executable, "-m", "tests.support.runtime_peer",
        stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE, env={**os.environ, "WORKCHORD_AUTH_MODE": "trusted_local", "MODEL_AWARE_ROUTING_MODE": "off"},
    )
    packet = dict(database_url=database_url, key=key, action=action, body=body,
                  idempotency_key=idempotency_key, **extra)
    try:
        stdout, stderr = await asyncio.wait_for(process.communicate(json.dumps(packet).encode()), timeout=45)
    except BaseException:
        if process.returncode is None:
            process.kill()
            await process.communicate()
        raise
    assert process.returncode == 0, stderr.decode()[-2000:]
    return json.loads(stdout)


def fence(receipt):
    return dict(assignment_id=receipt["assignment"]["id"], run_id=receipt["run"]["id"],
                claim_id=receipt["claim_id"], claim_generation=receipt["claim_generation"],
                expected_task_version=receipt["task"]["version"])


async def seed_work(factory, scenario):
    async with factory() as db:
        worker = await db.get(AgentActor, scenario.actors[0])
        verifier = await db.get(AgentActor, scenario.actors[1])
        worker.scopes = json.dumps(["work:execute", "assignments:read", "tasks:read"])
        verifier.scopes = json.dumps(["verification:write", "verification:read", "assignments:read", "tasks:read"])
        db.add(AgentActor(name="protocol-pm", display_name="Protocol PM", role="pm",
            api_key_hash=hash_api_key("disposable-protocol-pm-key"), scopes=json.dumps([
                "assignments:write", "assignments:read", "tasks:read", "recovery:write", "recovery:read"])))
        task = await TaskService(db).create(scenario.iterations[0], TaskCreate(
            title="Bounded deliverable", project_id=scenario.projects[0], effort_hours=2,
            tags=["agent", "cap:inspection"], brief=TaskBrief(goal="Deliver result", scope="One bounded result",
            verification="Inspect result independently", acceptance_criteria=[BriefCriterion(id="result", text="Correct result")]),
        ))
        task.start_date, task.end_date = date(2026, 1, 5), date(2026, 1, 6)
        assignment = AgentTaskAssignment(task_id=task.id, actor_id=worker.id,
            purpose="execution", state="queued", task_version=task.version)
        db.add(assignment)
        await db.commit()
        return task.id, assignment.id


async def begin_next(factory, key, logical_key):
    decision = await peer(factory, key, "work")
    assert decision["ok"], decision
    work = decision["response"]
    assert work["state"] == "start_assigned", {"state": work["state"], "blocked": work["blocked_assigned"]}
    item = work["next"]
    body = dict(assignment_id=item["assignment"]["id"], queue_revision=work["queue_revision"], lease_seconds=60)
    begun = await peer(factory, key, "begin", body=body, idempotency_key=logical_key)
    assert begun["ok"], begun
    return begun, body


async def nest_assigned_work(factory, scenario, task_id):
    async with factory() as db:
        parent = await TaskService(db).create(scenario.iterations[0], TaskCreate(
            title="Assigned work group", project_id=scenario.projects[0]))
        task = await db.get(Task, task_id)
        task.parent_id = parent.id
        await db.commit()
        return parent.id


async def test_ancestor_deferral_blocks_assigned_begin_over_rest_and_mcp(delivery_store):
    from app import mcp_agent_tools
    from app.services.agent_work_service import AgentConflictError

    factory, scenario, _ = delivery_store
    task_id, assignment_id = await seed_work(factory, scenario)
    parent_id = await nest_assigned_work(factory, scenario, task_id)
    async with factory() as db:
        parent = await TaskService(db).get_by_id(parent_id)
        await TaskService(db).update(parent_id, TaskUpdate(is_deferred=True, expected_version=parent.version))
        actor = await db.get(AgentActor, scenario.actors[0])
        body = dict(assignment_id=assignment_id, queue_revision=actor.queue_revision, lease_seconds=60)
        leaf = await TaskService(db).get_by_id(task_id)
        before = (leaf.status, leaf.version, leaf.claim_id, leaf.claim_generation)
    decision = await peer(factory, scenario.actor_keys[0], "work")
    assert decision["ok"] and decision["response"]["state"] == "wait", decision
    blocked = decision["response"]["blocked_assigned"]
    assert any("task_deferred" in item["blocker_codes"] for item in blocked)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/api/agent/me/work/begin", headers={
            "X-Agent-API-Key": scenario.actor_keys[0], "Idempotency-Key": "deferred-rest-begin"}, json=body)
        assert response.status_code == 409, response.text
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        with pytest.raises(AgentConflictError):
            await mcp_agent_tools.begin_my_work(db, actor, body, idempotency_key="deferred-mcp-begin")
    async with factory() as db:
        leaf = await db.get(Task, task_id)
        assert (leaf.status, leaf.version, leaf.claim_id, leaf.claim_generation) == before


async def test_ancestor_edit_invalidates_live_worker_renew_submit_and_begin_replay(delivery_store):
    factory, scenario, _ = delivery_store
    task_id, _ = await seed_work(factory, scenario)
    parent_id = await nest_assigned_work(factory, scenario, task_id)
    begun, begin_body = await begin_next(factory, scenario.actor_keys[0], "begin-before-ancestor-edit")
    receipt = begun["response"]
    async with factory() as db:
        parent = await TaskService(db).get_by_id(parent_id)
        assert parent.children
        await TaskService(db).update(parent_id, TaskUpdate(is_deferred=True, expected_version=parent.version))
        leaf = await TaskService(db).get_by_id(task_id)
        assert leaf.version > receipt["task"]["version"]
        claim = (leaf.claim_id, leaf.claim_generation, leaf.claimed_by)
    renewal = await peer(factory, scenario.actor_keys[0], "renew", body=fence(receipt), idempotency_key="renew-after-ancestor-edit")
    assert not renewal["ok"] and renewal["error_type"] == "AgentConflictError", renewal
    submission = dict(**fence(receipt), summary="Stale scope result", evidence={"inspection": "old context"},
        criterion_progress=[dict(criterion_id="result", criterion_revision=1, state="completed", evidence="Old scope")])
    submitted = await peer(factory, scenario.actor_keys[0], "submit", body=submission, idempotency_key="submit-after-ancestor-edit")
    assert not submitted["ok"] and submitted["error_type"] == "AgentConflictError", submitted
    replayed = await peer(factory, scenario.actor_keys[0], "begin", body=begin_body, idempotency_key="begin-before-ancestor-edit")
    assert not replayed["ok"] and replayed["error_type"] == "AgentConflictError", replayed
    async with factory() as db:
        leaf = await db.get(Task, task_id)
        assert (leaf.claim_id, leaf.claim_generation, leaf.claimed_by) == claim
        assert leaf.status == "active"


async def review_assignment(factory, task_id, actor_id):
    async with factory() as db:
        task = await db.get(Task, task_id)
        review = AgentTaskAssignment(task_id=task.id, actor_id=actor_id,
            purpose="verification", state="queued", task_version=task.version)
        db.add(review)
        await db.commit()
        return review.id, task.version


async def supervised_refresh(factory, scenario, task_id):
    """A worker pauses; an explicit PM replaces provisional lineage in off mode."""
    decision = await peer(factory, scenario.actor_keys[0], "work")
    assert decision["ok"] and decision["response"]["state"] == "wait", decision
    item = decision["response"]["next"]
    assert "routing_selection_pending" in item["blocker_codes"]
    updated = await peer(factory, "disposable-protocol-pm-key", "assignment_update",
        assignment_id=item["assignment"]["id"], body=dict(state="cancelled",
        expected_queue_revision=decision["response"]["queue_revision"], reason="Accountable PM reviewed supervised recovery"), idempotency_key=f"cancel-provisional-{item['assignment']['id']}")
    assert updated["ok"], updated
    created = await peer(factory, "disposable-protocol-pm-key", "assignment_create", body=dict(task_id=task_id,
        actor_id=scenario.actors[0], expected_task_version=item["task"]["version"], purpose="execution",
        queue_class=item["assignment"]["queue_class"], reason="Explicit supervised exact assignment"), idempotency_key=f"supervised-refresh-{item['assignment']['id']}")
    assert created["ok"], created


async def test_process_restart_ambiguous_replay_and_independent_rework(delivery_store):
    factory, scenario, _ = delivery_store
    task_id, _ = await seed_work(factory, scenario)
    worker_key, reviewer_key = scenario.actor_keys
    begun, begin_body = await begin_next(factory, worker_key, "begin-result")
    receipt = begun["response"]
    resumed = await peer(factory, worker_key, "work")
    assert resumed["ok"] and resumed["response"]["state"] == "resume"
    assert resumed["pid"] != begun["pid"]
    replay = await peer(factory, worker_key, "begin", body=begin_body, idempotency_key="begin-result")
    assert replay["ok"] and replay["response"]["run"]["id"] == receipt["run"]["id"]
    changed = await peer(factory, worker_key, "begin", body={**begin_body, "lease_seconds": 120}, idempotency_key="begin-result")
    assert not changed["ok"] and changed["error_type"] == "AgentConflictError"
    renewed = await peer(factory, worker_key, "renew", body=fence(receipt), idempotency_key="renew-result")
    assert renewed["ok"], renewed
    receipt = renewed["response"]
    submission = dict(**fence(receipt), summary="Implemented result", evidence={"inspection": "Worker observation"},
        criterion_progress=[dict(criterion_id="result", criterion_revision=1, state="completed", evidence="Artifact inspected")])
    submitted = await peer(factory, worker_key, "submit", body=submission, idempotency_key="submit-result")
    assert submitted["ok"], submitted
    repeated = await peer(factory, worker_key, "submit", body=submission, idempotency_key="submit-result")
    assert repeated["ok"] and repeated["response"] == submitted["response"]
    review_id, version = await review_assignment(factory, task_id, scenario.actors[1])
    verdict = dict(assignment_id=review_id, expected_task_version=version, verdict="reject",
        reason="Independent check found an incorrect result", evidence={"inspection": "Correction required"}, rework_actor_id=scenario.actors[0])
    wrong_actor = await peer(factory, worker_key, "review", body=verdict, idempotency_key="self-review")
    assert not wrong_actor["ok"] and wrong_actor["error_type"] == "AgentPermissionError", wrong_actor
    rejected = await peer(factory, reviewer_key, "review", body=verdict, idempotency_key="reject-result")
    assert rejected["ok"] and rejected["response"]["task"]["status"] == "active", rejected
    await supervised_refresh(factory, scenario, task_id)
    corrected, _ = await begin_next(factory, worker_key, "begin-correction")
    submission.update(fence(corrected["response"]))
    submission["summary"] = "Corrected result"
    submitted = await peer(factory, worker_key, "submit", body=submission, idempotency_key="submit-correction")
    assert submitted["ok"], submitted
    review_id, version = await review_assignment(factory, task_id, scenario.actors[1])
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        bypass = await client.put(f"/api/tasks/{task_id}/status", headers={"X-Agent-API-Key": worker_key},
                                  json={"status": "closed", "expected_version": version})
    assert bypass.status_code in {403, 409}, bypass.text
    accepted = await peer(factory, reviewer_key, "review", body=dict(assignment_id=review_id,
        expected_task_version=version, verdict="pass", evidence={"inspection": "Corrected artifact independently verified"}), idempotency_key="accept-result")
    assert accepted["ok"] and accepted["response"]["task"]["status"] == "closed", accepted
    async with factory() as db:
        task = await db.get(Task, task_id)
        assert task.accepted_version == task.version
        runs = (await db.scalars(select(AgentRun).where(AgentRun.task_id == task_id))).all()
        assert len(runs) == 2 and all(run.status == "succeeded" for run in runs)


async def test_process_restart_expired_fence_requeue_and_failure(delivery_store):
    factory, scenario, _ = delivery_store
    task_id, _ = await seed_work(factory, scenario)
    key = scenario.actor_keys[0]
    begun, _ = await begin_next(factory, key, "begin-expiry")
    receipt = begun["response"]
    async with factory() as db:
        task = await db.get(Task, task_id)
        task.claim_expires_at = utc_now() - timedelta(seconds=1)
        await db.commit()
    expired = await peer(factory, key, "renew", body=fence(receipt), idempotency_key="renew-expired")
    assert not expired["ok"], expired
    decision = await peer(factory, key, "work")
    assert decision["ok"] and decision["response"]["state"] == "attention_required"
    requeued = await peer(factory, "disposable-protocol-pm-key", "requeue", task_id=task_id, body=dict(actor_id=scenario.actors[0],
        expected_task_version=receipt["task"]["version"], expected_live_assignment_ids=[receipt["assignment"]["id"]],
        expected_running_run_ids=[receipt["run"]["id"]], expected_claim_generation=receipt["claim_generation"], reason="Recover expired process"), idempotency_key="requeue-expiry")
    assert requeued["ok"], requeued
    await supervised_refresh(factory, scenario, task_id)
    recovered, _ = await begin_next(factory, key, "begin-recovery")
    old = await peer(factory, key, "submit", body=dict(**fence(receipt), summary="Stale process result", evidence={"inspection": "Old evidence"}), idempotency_key="stale-submit")
    assert not old["ok"] and old["error_type"] in {"AgentConflictError", "TaskVersionConflictError"}, old
    failed = await peer(factory, key, "fail", body=dict(**fence(recovered["response"]), status="failed",
        error="Controlled external interruption", evidence={"interruption": "Simulated process failure"}), idempotency_key="fail-recovery")
    assert failed["ok"] and failed["response"]["recovery_required"], failed


async def test_changed_criterion_invalidates_restarted_worker_evidence(delivery_store):
    factory, scenario, _ = delivery_store
    task_id, _ = await seed_work(factory, scenario)
    key = scenario.actor_keys[0]
    begun, _ = await begin_next(factory, key, "begin-criterion")
    receipt = begun["response"]
    context = await peer(factory, key, "context", task_id=task_id, assignment_id=receipt["assignment"]["id"])
    assert context["ok"] and context["response"]["brief_source"] == "canonical", context
    async with factory() as db:
        task = await db.get(Task, task_id)
        brief = TaskBrief.model_validate(task.brief)
        brief.acceptance_criteria[0].text = "Correct result with clarified behavior"
        task = await TaskBriefService(db).write(task_id, BriefWrite(expected_version=task.version, brief=brief))
        assert task.brief["acceptance_criteria"][0]["revision"] == 2
        await db.commit()
        current_version = task.version
    old = await peer(factory, key, "submit", body=dict(**fence(receipt), summary="Old criterion evidence",
        evidence={"inspection": "Old packet"}, criterion_progress=[dict(criterion_id="result", criterion_revision=1,
        state="completed", evidence="Old result inspected")]), idempotency_key="submit-old-criterion")
    assert not old["ok"]
    forged_version = fence(receipt)
    forged_version["expected_task_version"] = current_version
    still_old = await peer(factory, key, "submit", body=dict(**forged_version, summary="Old criterion with new task version",
        evidence={"inspection": "Old packet"}, criterion_progress=[dict(criterion_id="result", criterion_revision=1,
        state="completed", evidence="Old result inspected")]), idempotency_key="submit-old-criterion-current-version")
    assert not still_old["ok"] and still_old["error_type"] in {"AgentConflictError", "TaskVersionConflictError"}, still_old
    decision = await peer(factory, key, "work")
    assert decision["ok"] and decision["response"]["state"] == "attention_required", decision
    async with factory() as db:
        task = await db.get(Task, task_id)
        assert task.status == "active" and task.progress is None and task.accepted_version is None
