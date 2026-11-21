"""A prior supervised worker resumes the exact strict handback on its original publisher."""
import json

import pytest
from sqlalchemy import select

from app.config import get_settings
from app.models.agent import AgentIdempotencyRecord, AgentModelCatalogEntry, AgentRun, AgentTaskAssignment, TaskEvent
from app.models.identity import ProjectMembership, WorkspaceMembership
from app.models.iteration import Iteration
from app.models.project import Project
from app.services.identity_service import IdentityService, initialize_control_plane
from tests.test_agent_team_setup_qualification import provision_ready_topology, routing_base
from tests.test_review_provenance_transports import databases, fence
from tests.test_team_pm_dispatch import db_session_factory
from tests.test_team_pm_recovery import recovery_api


@databases
@pytest.mark.parametrize("transport", ["rest", "mcp"])
@pytest.mark.parametrize("case", [
    "same_worker", "alternate_worker", "cross_team", "changed_binding", "missing_verdict",
    "missing_submit", "wrong_rework_event", "model_escalation", "binding_changed_before_begin",
    "off_after_rejection", "enforced_after_rejection",
])
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_authenticated_shadow_handback(db_session, db_session_factory, task_factory,
                                             team_member_factory, monkeypatch, transport, case):
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    get_settings.cache_clear()
    db = db_session
    await initialize_control_plane(db)
    await db.commit()
    team = await provision_ready_topology(db)
    member, other_member = team.manifest.workers[:2]
    verifier = team.manifest.verifiers[0]
    worker, other, reviewer = (team.actors[m.actor_key] for m in (member, other_member, verifier))
    manager = team.actors[team.manifest.controller.actor_key]
    pm_key, worker_key, other_key, reviewer_key = (team.sink.keys[m.actor_key] for m in
        (team.manifest.controller, member, other_member, verifier))
    setup = await routing_base(db, topology=team, actor_key=member.actor_key, task_factory=task_factory,
                               team_member_factory=team_member_factory, title="Revise the release instructions")
    task = setup.task
    project = Project(name="Release tools", require_different_review_publisher=True)
    db.add(project)
    await db.flush()
    task.project_id = (await db.get(Iteration, task.iteration_id)).project_id = project.id
    task.effort_hours = 8
    for actor, role in ((manager, "manager"), (worker, "executor"), (other, "executor"), (reviewer, "reviewer")):
        principal = await IdentityService(db).actor_context(actor)
        db.add_all([WorkspaceMembership(principal_id=principal.principal_id, role="member"),
                    ProjectMembership(principal_id=principal.principal_id, project_id=project.id, role=role)])
    for entry, publisher in ((member, "model-publisher"), (verifier, "independent-publisher")):
        catalog = await db.scalar(select(AgentModelCatalogEntry).where(AgentModelCatalogEntry.key == entry.default_model_binding_key))
        catalog.publisher_key = publisher
    await db.commit()
    if case == "cross_team":
        outside = await provision_ready_topology(db, two_workers=False, prefix="outside")
        foreign = outside.actors[outside.manifest.workers[0].actor_key]
    work = "agent_get_my_work", "/api/agent/me/work"
    begin = "agent_begin_my_work", "/api/agent/me/work/begin"
    dispatch = "agent_create_assignment", "/api/agent/assignments"
    submit = "agent_submit_my_work", "/api/agent/me/work/submit"
    verdict = "agent_submit_review_verdict", "/api/agent/me/reviews/verdict"
    async with recovery_api(transport, db_session_factory, monkeypatch) as call:
        assigned = await call(*dispatch, pm_key, payload={"actor_id": worker.id, "task_id": task.id,
            "reviewer_profile_id": reviewer.profile_id, "expected_task_version": task.version}, receipt="dispatch")
        first_queue = await call(*work, worker_key)
        running = await call(*begin, worker_key, payload={"assignment_id": assigned["id"],
            "queue_revision": first_queue["queue_revision"], "model": member.default_model_binding_key}, receipt="begin")
        submitted = await call(*submit, worker_key, payload={**fence(running), "observed_model": member.default_model_binding_key,
            "evidence": {"check": "read the revised instructions"}, "summary": "Instructions ready",
            "artifact_links": ["https://example.test/guide"]}, receipt="submit")
        review = await call(*dispatch, pm_key, payload={"actor_id": reviewer.id, "task_id": task.id, "purpose": "verification",
            "reviewer_profile_id": reviewer.profile_id, "expected_task_version": submitted["task"]["version"]}, receipt="assign-verifier")
        origin = review["review_selection"]
        assert origin["reviewer"]["publisher_key"] == "independent-publisher"
        assert origin["candidate"]["run_id"] == running["run"]["id"]
        target = other if case == "alternate_worker" else worker
        reject_request = {"assignment_id": review["id"], "expected_task_version": submitted["task"]["version"],
            "verdict": "reject", "reason": "Clarify the verification instructions", "rework_actor_id": target.id,
            "reviewed_candidate_digest": origin["candidate"]["digest"], "observed_model": verifier.default_model_binding_key,
            "evidence": {"criterion": "instructions need clarification"}}
        if case == "cross_team":
            await call(*verdict, reviewer_key, payload={**reject_request, "rework_actor_id": foreign.id},
                       receipt="foreign-revision", error="agent_team_actor_outside_topology")
            async with db_session_factory() as audit:
                assert not await audit.scalar(select(AgentTaskAssignment.id).where(
                    AgentTaskAssignment.task_id == task.id, AgentTaskAssignment.queue_class == "rework"))
            return
        if case == "model_escalation":
            reject_request["evidence"]["routing_failure_category"] = "tool_insufficiency"
        rejected = await call(*verdict, reviewer_key, payload=reject_request, receipt="request-revision")
        assert await call(*verdict, reviewer_key, payload=reject_request, receipt="request-revision") == rejected
        rework = rejected["rework_assignment"]
        assert rework["queue_class"] == "rework" and rework["state"] == "queued" and rework["actor_id"] == target.id
        assert rejected["task"]["status"] == "active" and rework["routing_snapshot"]["selection_pending"]
        assert rework["reviewer_profile_id"] is None and "supervised_rework" not in rework["routing_snapshot"]
        async with db_session_factory() as audit:
            receipt = await audit.scalar(select(AgentIdempotencyRecord).where(
                AgentIdempotencyRecord.actor_id == reviewer.id, AgentIdempotencyRecord.operation == "verification.verdict",
                AgentIdempotencyRecord.target_id == review["id"]))
            original_verdict = receipt.response_payload
            previous = await audit.get(AgentRun, running["run"]["id"])
            original_execution = previous.execution_provenance
            if case == "missing_verdict":
                recorded = json.loads(original_verdict)
                recorded["response"]["rework_assignment"]["id"] += 1
                receipt.response_payload = json.dumps(recorded)
            if case == "changed_binding":
                entry = await audit.get(AgentModelCatalogEntry, original_execution["catalog_id"])
                entry.publisher_key = "independent-publisher"
                entry.revision += 1
            if case == "missing_submit":
                submission = await audit.scalar(select(AgentIdempotencyRecord).where(
                    AgentIdempotencyRecord.actor_id == worker.id, AgentIdempotencyRecord.operation == "work.submit",
                    AgentIdempotencyRecord.target_id == assigned["id"]))
                await audit.delete(submission)
            if case == "wrong_rework_event":
                event = await audit.scalar(select(TaskEvent).where(TaskEvent.task_id == task.id,
                    TaskEvent.event_type == "agent.verification_verdict", TaskEvent.actor_id == reviewer.id))
                changed = json.loads(event.payload)
                changed["rework_assignment_id"] += 1
                event.payload = json.dumps(changed)
            await audit.commit()
        if case in {"off_after_rejection", "enforced_after_rejection"}:
            monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", case.split("_")[0])
            get_settings.cache_clear()
            caps = await call("agent_get_capabilities", "/api/agent/capabilities", worker_key)
            assert caps["model_aware_routing"]["effective_mode"] == case.split("_")[0]
        key = other_key if target.id == other.id else worker_key
        queue = await call(*work, key)
        if case not in {"same_worker", "binding_changed_before_begin"}:
            blocked, = queue["blocked_assigned"]
            assert queue["state"] == "wait" and blocked["assignment"]["id"] == rework["id"]
            assert "routing_selection_pending" in blocked["blocker_codes"]
            return
        assert queue["state"] == "start_assigned" and queue["next"]["assignment"]["id"] == rework["id"]
        assert not queue["next"]["blocker_codes"]
        view = queue["next"]["assignment"]
        assert view["reviewer_profile_id"] == reviewer.profile_id
        assert view["routing_snapshot"]["selection_pending"] and view["routing_snapshot"]["supervised_actor_id"] == worker.id
        context = await call("agent_get_complete_task_context", f"/api/agent/tasks/{task.id}/context", worker_key, task_id=task.id)
        assert context["start_ready"] and context["assignment"]["routing_snapshot"] == view["routing_snapshot"]
        async with db_session_factory() as audit:
            pending = await audit.get(AgentTaskAssignment, rework["id"])
            assert pending.reviewer_profile_id is None and json.loads(pending.routing_snapshot) == rework["routing_snapshot"]
        handback = {"assignment_id": rework["id"], "queue_revision": queue["queue_revision"]}
        if case == "binding_changed_before_begin":
            async with db_session_factory() as audit:
                entry = await audit.get(AgentModelCatalogEntry, original_execution["catalog_id"])
                entry.revision += 1
                await audit.commit()
            await call(*begin, worker_key, payload={**handback, "model": member.default_model_binding_key},
                       receipt="stale-handoff", error="routing_selection_pending")
            async with db_session_factory() as audit:
                assert not await audit.scalar(select(AgentRun.id).where(AgentRun.assignment_id == rework["id"]))
                assert (await audit.get(AgentTaskAssignment, rework["id"])).state == "queued"
            return
        await call(*begin, worker_key, payload={**handback, "model_binding_id": original_execution["binding_id"],
                   "model_binding_revision": original_execution["binding_revision"], "resolved_model_id": member.default_model_binding_key},
                   receipt="enforced-command-in-shadow", error="routing_selection_pending")
        await call(*begin, worker_key, payload={**handback, "model": verifier.default_model_binding_key},
                   receipt="wrong-model", error="execution_publisher_unverifiable")
        next_request = {**handback, "model": member.default_model_binding_key}
        resumed = await call(*begin, worker_key, payload=next_request, receipt="resume")
        repeated = await call(*begin, worker_key, payload=next_request, receipt="resume")
        assert repeated["run"]["id"] == resumed["run"]["id"]
        assert resumed["assignment"]["reviewer_profile_id"] == reviewer.profile_id
        provenance = resumed["run"]["execution_provenance"]
        assert provenance["publisher_key"] == "model-publisher" and provenance["binding_id"] == original_execution["binding_id"]
        lineage = provenance["supervised_rework"]
        assert lineage["rejected_run_id"] == running["run"]["id"] and lineage["review_assignment_id"] == review["id"]
        assert lineage["reviewer_profile_id"] == reviewer.profile_id and lineage["reviewer_publisher_key"] == "independent-publisher"
        assert lineage["reviewed_candidate_digest"] == origin["candidate"]["digest"]
        assert resumed["assignment"]["routing_snapshot"]["source_assignment_ids"] == rework["routing_snapshot"]["source_assignment_ids"]
        assert resumed["assignment"]["routing_snapshot"]["review_floor"] == {
            "review_mode": "independent", "reviewer_profile_ids": [reviewer.profile_id], "independence_must_be_revalidated": True}
        assert (await call(*work, worker_key))["state"] == "resume"
        async with db_session_factory() as audit:
            assert (await audit.get(AgentRun, running["run"]["id"])).execution_provenance == original_execution
            historical = await audit.scalar(select(AgentIdempotencyRecord.response_payload).where(
                AgentIdempotencyRecord.actor_id == reviewer.id, AgentIdempotencyRecord.operation == "verification.verdict",
                AgentIdempotencyRecord.target_id == review["id"]))
            assert historical == original_verdict
        revised = await call(*submit, worker_key, payload={**fence(resumed), "observed_model": member.default_model_binding_key,
            "summary": "Clarified the instructions", "evidence": {"check": "verified the revised explanation"},
            "artifact_links": ["https://example.test/guide/revised"]}, receipt="submit-revision")
        second_review = await call(*dispatch, pm_key, payload={"actor_id": reviewer.id, "task_id": task.id,
            "purpose": "verification", "reviewer_profile_id": reviewer.profile_id, "expected_task_version": revised["task"]["version"]},
            receipt="verify-revision")
        selected = second_review["review_selection"]
        assert {c["run_id"] for c in selected["contributors"]} == {running["run"]["id"], resumed["run"]["id"]}
        rejected_again = await call(*verdict, reviewer_key, payload={**reject_request, "assignment_id": second_review["id"],
            "expected_task_version": revised["task"]["version"], "reviewed_candidate_digest": selected["candidate"]["digest"]},
            receipt="revise-again")
        second_queue = await call(*work, worker_key)
        assert second_queue["state"] == "start_assigned" and second_queue["next"]["assignment"]["id"] == rejected_again["rework_assignment"]["id"]
