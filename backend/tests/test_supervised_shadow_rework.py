"""A prior supervised worker resumes the exact strict handback on its original publisher."""
import json
from copy import deepcopy
from unittest.mock import patch

import httpx
import pytest
from sqlalchemy import event, func, inspect, select, text, update
from sqlalchemy.exc import DBAPIError

from app.config import get_settings
from app.main import app
from app.models.agent import (AgentActor, AgentIdempotencyRecord, AgentModelBinding, AgentModelCatalogEntry, AgentRun,
                              AgentTaskAssignment, AgentTeamTopology, AgentTeamTopologyMember, TaskEvent)
from app.models.identity import ProjectMembership, WorkspaceMembership
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.task import Task
from app.models.team_member import TeamMember
from app.schemas.agent_team_setup import AgentTeamMaster
from app.services import agent_work_service, review_provenance
from app.services.agent_team_setup_service import AgentTeamSetupService
from app.services.identity_service import IdentityService, initialize_control_plane
from tests.test_agent_routing_service import _assessment_command
from tests.test_agent_team_setup import CapturingCredentialSink
from tests.test_agent_team_setup_qualification import (
    ReadyTopology, acknowledge_all, apply_manifest, provision_ready_topology, routing_base, seed_model_catalog,
    topology_actors, topology_payload,
)
from tests.test_review_provenance_transports import databases, fence
from tests.test_team_pm_dispatch import db_session_factory
from tests.test_team_pm_recovery import recovery_api


async def stored_history(factory, rework_id, verdict_id, source_id):
    async with factory() as reader:
        issued = await reader.get(AgentTaskAssignment, rework_id)
        receipts = (await reader.execute(select(AgentIdempotencyRecord.operation, AgentIdempotencyRecord.response_payload)
            .where((AgentIdempotencyRecord.operation == "verification.verdict") & (AgentIdempotencyRecord.target_id == verdict_id)
                 | (AgentIdempotencyRecord.operation == "work.submit") & (AgentIdempotencyRecord.target_id == source_id))
            .order_by(AgentIdempotencyRecord.id))).all()
        return issued.reviewer_profile_id, issued.routing_snapshot, list(receipts)


async def topology_with_two_reviewers(db):
    payload = topology_payload()
    extra = deepcopy(payload["verifiers"][0])
    extra.update(actor_key="alternate-reviewer", actor_name="alternate-reviewer", display_name="Alternate Review",
                 profile_key="security-scope-agent", runtime_ref="runtime://alternate-reviewer",
                 credential_ref="agent-team-secure-sink/alternate-reviewer")
    payload["verifiers"].append(extra)
    manifest = AgentTeamMaster.model_validate(payload)
    await seed_model_catalog(db, manifest)
    sink = CapturingCredentialSink()
    service = AgentTeamSetupService(db, credential_sink=sink)
    await apply_manifest(service, manifest, expected_revision=0, key="multi-verifier-topology")
    await acknowledge_all(service, manifest, sink.keys)
    return ReadyTopology(manifest, sink, service, await topology_actors(db, manifest))


def control_plane_writes(project_id, capacity_id, manager, worker, reviewer, earlier_actor, binding, topology_id):
    writes = {
        "catalog": update(AgentModelCatalogEntry).where(AgentModelCatalogEntry.id == binding["catalog_id"])
                  .values(revision=AgentModelCatalogEntry.revision + 1),
        "binding": update(AgentModelBinding).where(AgentModelBinding.id == binding["binding_id"]).values(revision=AgentModelBinding.revision + 1),
        "project_policy": update(Project).where(Project.id == project_id).values(require_different_review_publisher=False),
        "topology": update(AgentTeamTopology).where(AgentTeamTopology.id == topology_id).values(revision=AgentTeamTopology.revision + 1),
        "capacity_profile": update(TeamMember).where(TeamMember.id == capacity_id).values(profile_id=None),
        "verifier_identity": update(AgentActor).where(AgentActor.id == reviewer.id).values(enabled=False),
    }
    actors = {"worker_membership": worker.id, "verifier_membership": reviewer.id, "manager_membership": manager.id}
    if earlier_actor is not None:
        actors["prior_contributor_membership"] = earlier_actor.id
    for label, actor_id in actors.items():
        writes[label] = update(AgentTeamTopologyMember).where(AgentTeamTopologyMember.actor_id == actor_id).values(lifecycle_state="disabled")
    return writes


async def assert_postgresql_locks(factory, writes):
    blocked_writers = set()
    for name, statement in writes.items():
        async with factory() as competing:
            await competing.execute(text("SET LOCAL lock_timeout = '180ms'"))
            with pytest.raises(DBAPIError) as blocked:
                await competing.execute(statement)
            assert getattr(blocked.value.orig, "sqlstate", None) == "55P03", name
            blocked_writers.add(name)
            await competing.rollback()
    return blocked_writers


async def assert_floor_preview(task_id, task_version, pm_key, reviewer, alternate_verifier):
    command = _assessment_command(task_version=task_version).model_copy(update={
        "review_mode": "independent", "required_skill_levels": {},
    })
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://localhost:8001") as client:
        assessment = await client.post(f"/api/agent/planning/tasks/{task_id}/routing-assessment",
            headers={"X-Agent-API-Key": pm_key, "Idempotency-Key": "assess-revised-instructions",
                     "X-Correlation-ID": "assess-revised-instructions", "X-Agent-Rationale": "Select a qualified independent reviewer"},
            json=command.model_dump(mode="json"))
        assert assessment.status_code == 201, assessment.text
        for actor in (alternate_verifier, reviewer):
            response = await client.post(f"/api/agent/tasks/{task_id}/routing-preview",
                headers={"X-Agent-API-Key": pm_key}, json={"purpose": "verification",
                    "assessment_id": assessment.json()["assessment"]["id"], "expected_task_version": task_version,
                    "reviewer_profile_id": actor.profile_id})
            assert response.status_code == 200, response.text
            snapshot = response.json()
            exclusions = [row for row in snapshot["exclusions"] if row["actor_id"] == actor.id]
            if actor.id == alternate_verifier.id:
                assert exclusions and all("reviewer_profile_mismatch" in row["hard_blocker_codes"] for row in exclusions)
                assert all(row["actor_id"] != actor.id for row in snapshot["eligible_candidates"])
            else:
                assert all("reviewer_profile_mismatch" not in row["hard_blocker_codes"] for row in exclusions)


def assert_lookup_indexes(session):
    schema = inspect(session.connection())
    constraints = schema.get_unique_constraints("agent_idempotency_records") + schema.get_indexes("agent_idempotency_records")
    assert any(tuple(row["column_names"][:4]) == ("actor_id", "operation", "target_type", "target_id") for row in constraints)
    assert any(tuple(row["column_names"]) == ("task_id", "actor_id", "event_type", "idempotency_key")
               for row in schema.get_indexes("task_events"))


@databases
@pytest.mark.parametrize("transport", ["rest", "mcp"])
@pytest.mark.parametrize("case", [
    "same_worker", "alternate_worker", "cross_team", "changed_binding", "missing_verdict",
    "missing_submit", "wrong_rework_event", "model_escalation", "binding_changed_before_begin",
    "off_after_rejection", "enforced_after_rejection", "verifier_disabled", "verifier_rebound",
    "worker_membership_lost", "verifier_membership_lost", "task_changed_before_begin", "previous_canceled_run",
    "identity_revision_during_begin", "identity_publisher_during_begin", "failed_recovery", "canceled_recovery", "two_items",
    "recovered_submitter", "older_contributor", "missing_recovery_receipt", "wrong_recovery_event",
    "wrong_submitted_version", "wrong_issued_version", "legacy_verdict_selection", "legacy_verdict_wrong_candidate",
    "policy_changed_before_begin",
])
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_authenticated_shadow_handback(db_session, db_session_factory, task_factory,
                                             team_member_factory, monkeypatch, transport, case, record_property):
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    get_settings.cache_clear()
    db = db_session
    await initialize_control_plane(db)
    await db.commit()
    multi_reviewer = case in {"same_worker", "recovered_submitter"}
    team = await topology_with_two_reviewers(db) if multi_reviewer else await provision_ready_topology(db)
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
    memberships = [(manager, "manager"), (worker, "executor"), (other, "executor"), (reviewer, "reviewer")]
    if multi_reviewer:
        alternate_verifier = team.actors[team.manifest.verifiers[1].actor_key]
        memberships.append((alternate_verifier, "reviewer"))
    for actor, role in memberships:
        principal = await IdentityService(db).actor_context(actor)
        db.add_all([WorkspaceMembership(principal_id=principal.principal_id, role="member"),
                    ProjectMembership(principal_id=principal.principal_id, project_id=project.id, role=role)])
    recovered_origin = case in {"recovered_submitter", "older_contributor", "missing_recovery_receipt", "wrong_recovery_event",
                                "wrong_submitted_version", "wrong_issued_version"}
    if recovered_origin:
        prior_capacity = await team_member_factory(profile=other.profile, iteration=await db.get(Iteration, task.iteration_id))
        task.assignee_id = prior_capacity.id
    for entry, publisher in ((member, "model-publisher"), (other_member, "model-publisher"), (verifier, "independent-publisher")):
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
        earlier_run = None
        if recovered_origin:
            earlier = await call(*dispatch, pm_key, payload={"actor_id": other.id, "task_id": task.id,
                "reviewer_profile_id": reviewer.profile_id, "expected_task_version": task.version}, receipt="earlier-worker")
            old_queue = await call(*work, other_key)
            earlier_run = await call(*begin, other_key, payload={"assignment_id": earlier["id"], "queue_revision": old_queue["queue_revision"],
                "model": other_member.default_model_binding_key}, receipt="earlier-begin")
            stopped = await call("agent_fail_my_work", "/api/agent/me/work/fail", other_key, payload={**fence(earlier_run),
                "observed_model": other_member.default_model_binding_key, "output_state": "retained", "status": "failed",
                "evidence": {"retained": "the original draft"}, "summary": "The original draft needs completion"}, receipt="retain-draft")
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://localhost:8001") as client:
                changed = await client.patch(f"/api/agent/planning/tasks/{task.id}",
                    headers={"X-Agent-API-Key": pm_key, "Idempotency-Key": "move-capacity", "X-Correlation-ID": "move-capacity",
                             "X-Agent-Rationale": "Move the remaining work to its new capacity owner"},
                    json={"expected_version": stopped["task"]["version"], "assignee_id": setup.member.id})
                assert changed.status_code == 200, changed.text
            recovery_list = await call("agent_list_recovery_tasks", "/api/agent/recovery", pm_key)
            item, = recovery_list["items"]
            recovered = await call("agent_requeue_recovery", f"/api/agent/recovery/{task.id}/requeue", pm_key, task_id=task.id,
                payload={"actor_id": worker.id, "expected_task_version": item["task"]["version"],
                         "expected_claim_generation": item["claim_generation"], "expected_live_assignment_ids": [],
                         "expected_running_run_ids": [], "reason": "Complete the retained draft with its assigned worker"}, receipt="recover-draft")
            assigned = recovered["assignment"]
            assert assigned["queue_class"] == "recovery" and assigned["routing_snapshot"]["supervised_actor_id"] == worker.id
        else:
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
        if earlier_run:
            assert {(c["run_id"],c["actor_id"],c["publisher_key"]) for c in origin["contributors"]} == {
                (earlier_run["run"]["id"],other.id,"model-publisher"), (running["run"]["id"],worker.id,"model-publisher")}
        target = other if case in {"alternate_worker", "older_contributor"} else worker
        reject_request = {"assignment_id": review["id"], "expected_task_version": submitted["task"]["version"],
            "verdict": "reject", "reason": "Clarify the verification instructions", "rework_actor_id": target.id,
            "reviewed_candidate_digest": origin["candidate"]["digest"], "observed_model": verifier.default_model_binding_key,
            "evidence": {"criterion": "instructions need clarification"}}
        if case == "two_items":
            sibling = await task_factory(iteration=await db.get(Iteration, task.iteration_id), assignee=setup.member,
                title="Revise the other guide", description=task.description, tags=task.tags, priority=2, effort_days=1, status="planned",
                start_date=task.start_date, end_date=task.end_date)
            sibling.project_id, sibling.effort_hours = project.id, 8
            await db.commit()
            extra = await call(*dispatch, pm_key, payload={"actor_id": worker.id, "task_id": sibling.id,
                "reviewer_profile_id": reviewer.profile_id, "expected_task_version": sibling.version}, receipt="dispatch-other")
            first = await call(*work, worker_key)
            owner = await call(*begin, worker_key, payload={"assignment_id": extra["id"], "queue_revision": first["queue_revision"],
                               "model": member.default_model_binding_key}, receipt="begin-other")
            delivered = await call(*submit, worker_key, payload={**fence(owner), "observed_model": member.default_model_binding_key,
                "summary": "Second guide ready", "evidence": {"check": "read the second guide"},
                "artifact_links": ["https://example.test/guide/two"]}, receipt="submit-other")
            verification = await call(*dispatch, pm_key, payload={"actor_id": reviewer.id, "task_id": sibling.id, "purpose": "verification",
                "reviewer_profile_id": reviewer.profile_id, "expected_task_version": delivered["task"]["version"]}, receipt="verify-other")
            await call(*verdict, reviewer_key, payload={**reject_request, "assignment_id": verification["id"],
                "reviewed_candidate_digest": verification["review_selection"]["candidate"]["digest"],
                "expected_task_version": delivered["task"]["version"]}, receipt="return-other")
        if case == "cross_team":
            await call(*verdict, reviewer_key, payload={**reject_request, "rework_actor_id": foreign.id},
                       receipt="foreign-revision", error="agent_team_actor_outside_topology")
            async with db_session_factory() as audit:
                assert not await audit.scalar(select(AgentTaskAssignment.id).where(
                    AgentTaskAssignment.task_id == task.id, AgentTaskAssignment.queue_class == "rework"))
            return
        if case == "model_escalation":
            reject_request["evidence"]["routing_failure_category"] = "tool_insufficiency"
        if case in {"legacy_verdict_selection", "legacy_verdict_wrong_candidate"}:
            reject_request.pop("reviewed_candidate_digest")
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
            if case in {"wrong_rework_event", "legacy_verdict_selection", "legacy_verdict_wrong_candidate"}:
                recorded_event = await audit.scalar(select(TaskEvent).where(TaskEvent.task_id == task.id,
                    TaskEvent.event_type == "agent.verification_verdict", TaskEvent.actor_id == reviewer.id))
                changed = json.loads(recorded_event.payload)
                if case == "wrong_rework_event":
                    changed["rework_assignment_id"] += 1
                else:
                    assert changed.get("reviewed_candidate_digest") is None and changed["review_selection"] == origin
                    if case == "legacy_verdict_wrong_candidate":
                        changed["review_selection"]["candidate"]["digest"] = "0" * 64
                if case != "legacy_verdict_selection":
                    recorded_event.payload = json.dumps(changed)
            if case == "verifier_disabled":
                (await audit.get(AgentActor, reviewer.id)).enabled = False
            if case == "verifier_rebound":
                old_catalog = await audit.get(AgentModelCatalogEntry, origin["reviewer"]["catalog_id"])
                old_catalog.publisher_key = original_execution["publisher_key"]
                old_catalog.revision += 1
            if case in {"worker_membership_lost", "verifier_membership_lost"}:
                removed = worker if case == "worker_membership_lost" else reviewer
                row = await audit.scalar(select(AgentTeamTopologyMember).where(AgentTeamTopologyMember.actor_id == removed.id))
                row.lifecycle_state = "disabled"
            if case == "previous_canceled_run":
                audit.add(AgentRun(task_id=task.id, assignment_id=rework["id"], actor_id=worker.id,
                                   status="canceled", claim_generation=running["claim_generation"] + 1))
            if case == "wrong_submitted_version":
                (await audit.get(AgentTaskAssignment, assigned["id"])).task_version += 1
            if case in {"missing_recovery_receipt", "wrong_recovery_event", "wrong_issued_version"}:
                if case in {"missing_recovery_receipt", "wrong_issued_version"}:
                    row = await audit.scalar(select(AgentIdempotencyRecord).where(AgentIdempotencyRecord.actor_id == manager.id,
                        AgentIdempotencyRecord.operation == "recovery.requeue", AgentIdempotencyRecord.target_id == task.id))
                    if case == "missing_recovery_receipt":
                        await audit.delete(row)
                    else:
                        value = json.loads(row.response_payload)
                        value["response"]["task"]["version"] += 1
                        row.response_payload = json.dumps(value)
                else:
                    row = await audit.scalar(select(TaskEvent).where(TaskEvent.task_id == task.id,
                        TaskEvent.actor_id == manager.id, TaskEvent.event_type == "agent.recovery_requeued"))
                    value = json.loads(row.payload)
                    value["routing_selection_pending"] = True
                    row.payload = json.dumps(value)
            await audit.commit()
        previous_history = await stored_history(db_session_factory, rework["id"], review["id"], assigned["id"])
        if case in {"off_after_rejection", "enforced_after_rejection"}:
            monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", case.split("_")[0])
            get_settings.cache_clear()
            caps = await call("agent_get_capabilities", "/api/agent/capabilities", worker_key)
            assert caps["model_aware_routing"]["effective_mode"] == case.split("_")[0]
        key = other_key if target.id == other.id else worker_key
        if case == "two_items":
            # Count the actual statements and authenticated identity reads for two
            # distinct rejected submissions in one managed protocol request.
            selects = []
            engine = db.bind.sync_engine
            def count_sql(_connection, _cursor, statement, _params, _context, _many):
                if statement.lstrip().upper().startswith("SELECT"):
                    selects.append(statement)
            original_boundary = AgentTeamSetupService.membership_boundary
            with patch.object(review_provenance, "actor_provenance", wraps=review_provenance.actor_provenance) as bindings, \
                 patch.object(AgentTeamSetupService, "membership_boundary", autospec=True, side_effect=original_boundary) as topology:
                event.listen(engine, "before_cursor_execute", count_sql)
                try:
                    page = await call(*work, key)
                finally:
                    event.remove(engine, "before_cursor_execute", count_sql)
            assert page["state"] == "start_assigned" and len(page["queue"]) == 2 and not page["blocked_assigned"]
            assert len({row["assignment"]["routing_snapshot"]["supervised_rework"]["verdict_receipt_id"] for row in page["queue"]}) == 2
            assert bindings.await_count == 2  # one worker binding and one reviewer binding for the whole page
            assert topology.await_count == 1  # the rollout and both proofs share one authoritative membership observation
            receipt_joins = [sql for sql in selects if "JOIN agent_task_assignments" in sql and "agent_idempotency_records" in sql]
            assert len(receipt_joins) == 4
            record_property("two_rework_items_selects", str(len(selects)))
            record_property("two_rework_items_indexed_receipt_joins", str(len(receipt_joins)))
            proof_selects = len(selects)
            selects.clear()
            with patch.object(agent_work_service, "supervised_rework_evidence", return_value=None):
                event.listen(engine, "before_cursor_execute", count_sql)
                try:
                    baseline = await call(*work, key)
                finally:
                    event.remove(engine, "before_cursor_execute", count_sql)
            assert baseline["state"] == "wait" and len(baseline["blocked_assigned"]) == 2
            record_property("two_rework_items_without_proof_selects", str(len(selects)))
            record_property("added_proof_selects", str(proof_selects - len(selects)))
            return
        queue = await call(*work, key)
        ready_cases = {"same_worker", "recovered_submitter", "legacy_verdict_selection", "binding_changed_before_begin",
                       "task_changed_before_begin", "policy_changed_before_begin", "identity_revision_during_begin",
                       "identity_publisher_during_begin", "failed_recovery", "canceled_recovery"}
        if case not in ready_cases:
            blocked, = queue["blocked_assigned"]
            assert queue["state"] == "wait" and blocked["assignment"]["id"] == rework["id"]
            assert "routing_selection_pending" in blocked["blocker_codes"]
            context = await call("agent_get_complete_task_context", f"/api/agent/tasks/{task.id}/context", key, task_id=task.id)
            assert context["started"] is False and not context["start_ready"] and "routing_selection_pending" in context["blocker_codes"]
            assert ("model_aware_assignment_inactive" in context["blocker_codes"]) == (case != "enforced_after_rejection")
            denial = "agent_team_actor_outside_topology" if case == "worker_membership_lost" else "routing_selection_pending"
            await call(*begin, key, payload={"assignment_id": rework["id"], "queue_revision": queue["queue_revision"],
                       "model": member.default_model_binding_key}, receipt="unavailable-handback", error=denial)
            async with db_session_factory() as audit:
                count = await audit.scalar(select(func.count(AgentRun.id)).where(AgentRun.assignment_id == rework["id"]))
                assert count == (1 if case == "previous_canceled_run" else 0)
            assert await stored_history(db_session_factory, rework["id"], review["id"], assigned["id"]) == previous_history
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
        if case in {"binding_changed_before_begin", "task_changed_before_begin", "policy_changed_before_begin"}:
            async with db_session_factory() as audit:
                if case == "binding_changed_before_begin":
                    entry = await audit.get(AgentModelCatalogEntry, original_execution["catalog_id"])
                    entry.revision += 1
                elif case == "task_changed_before_begin":
                    (await audit.get(Task, task.id)).version += 1
                else:
                    (await audit.get(Project, project.id)).require_different_review_publisher = False
                await audit.commit()
            await call(*begin, worker_key, payload={**handback, "model": member.default_model_binding_key},
                       receipt="stale-handoff", error="routing_selection_pending")
            async with db_session_factory() as audit:
                assert not await audit.scalar(select(AgentRun.id).where(AgentRun.assignment_id == rework["id"]))
                assert (await audit.get(AgentTaskAssignment, rework["id"])).state == "queued"
            assert (await call(*work, key))["state"] == "wait"
            assert not (await call("agent_get_complete_task_context", f"/api/agent/tasks/{task.id}/context", key, task_id=task.id))["start_ready"]
            assert await stored_history(db_session_factory, rework["id"], review["id"], assigned["id"]) == previous_history
            return
        await call(*begin, worker_key, payload={**handback, "model_binding_id": original_execution["binding_id"],
                   "model_binding_revision": original_execution["binding_revision"], "resolved_model_id": member.default_model_binding_key},
                   receipt="enforced-command-in-shadow", error="routing_selection_pending")
        await call(*begin, worker_key, payload=handback, receipt="missing-observation", error="execution_publisher_unverifiable")
        await call(*begin, worker_key, payload={**handback, "model": verifier.default_model_binding_key},
                   receipt="wrong-model", error="execution_publisher_unverifiable")
        next_request = {**handback, "model": member.default_model_binding_key}
        resolve = agent_work_service.actor_provenance
        is_pg = db.get_bind().dialect.name == "postgresql"
        checked_writers = set()
        writes = {}
        if is_pg and multi_reviewer:
            topology_id = await db.scalar(select(AgentTeamTopologyMember.topology_id).where(AgentTeamTopologyMember.actor_id == worker.id))
            writes = control_plane_writes(project.id, assigned["team_member_id"], manager, worker, reviewer,
                                         other if earlier_run else None, original_execution, topology_id)

        async def final_observation(*args, **kwargs):
            value = await resolve(*args, **kwargs)
            if case == "identity_revision_during_begin":
                return {**value, "catalog_revision": value["catalog_revision"] + 1}
            if case == "identity_publisher_during_begin":
                return {**value, "publisher_key": "independent-publisher"}
            if writes:
                checked_writers.update(await assert_postgresql_locks(db_session_factory, writes))
            return value

        with patch.object(agent_work_service, "actor_provenance", final_observation), \
             patch.object(agent_work_service, "supervised_rework_evidence", wraps=agent_work_service.supervised_rework_evidence) as evaluated:
            if case.startswith("identity_"):
                await call(*begin, worker_key, payload=next_request, receipt="final-binding-drift", error="execution_publisher_unverifiable")
                async with db_session_factory() as audit:
                    assert not await audit.scalar(select(AgentRun.id).where(AgentRun.assignment_id == rework["id"]))
                    unchanged = await audit.get(Task, task.id)
                    assert unchanged.claim_id is None and unchanged.version == rejected["task"]["version"]
                assert await stored_history(db_session_factory, rework["id"], review["id"], assigned["id"]) == previous_history
                return
            resumed = await call(*begin, worker_key, payload=next_request, receipt="resume")
            assert evaluated.await_count == 1 and evaluated.await_args.kwargs["lock"] is True
            record_property("locked_handback_evaluations_per_begin", str(evaluated.await_count))
        repeated = await call(*begin, worker_key, payload=next_request, receipt="resume")
        assert repeated == resumed
        assert resumed["assignment"]["reviewer_profile_id"] == reviewer.profile_id
        provenance = resumed["run"]["execution_provenance"]
        assert provenance["publisher_key"] == "model-publisher" and provenance["binding_id"] == original_execution["binding_id"]
        lineage = provenance["supervised_rework"]
        assert lineage["rejected_run_id"] == running["run"]["id"] and lineage["review_assignment_id"] == review["id"]
        assert lineage["reviewer_profile_id"] == reviewer.profile_id and lineage["reviewer_publisher_key"] == "independent-publisher"
        assert lineage["reviewed_candidate_digest"] == origin["candidate"]["digest"]
        assert lineage["contributors_digest"] == review_provenance.digest(origin["contributors"])
        if earlier_run:
            assert lineage["contributor_count"] == 2 and lineage["source_recovery"]["assignment_id"] == assigned["id"]
            assert lineage["source_recovery"]["receipt_id"] and lineage["source_recovery"]["event_id"]
            assert (lineage["source_recovery"]["issued_task_version"], lineage["source_recovery"]["submitted_task_version"]) == (
                assigned["task_version"], submitted["assignment"]["task_version"])
            assert assigned["task_version"] < submitted["assignment"]["task_version"]
        assert lineage["worker_binding"]["binding_revision"] == original_execution["binding_revision"]
        assert lineage["worker_binding"]["publisher_key"] == original_execution["publisher_key"]
        assert lineage["review_floor"] == resumed["assignment"]["routing_snapshot"]["review_floor"]
        assert resumed["assignment"]["routing_snapshot"]["source_assignment_ids"] == rework["routing_snapshot"]["source_assignment_ids"]
        assert resumed["assignment"]["routing_snapshot"]["review_floor"] == {
            "review_mode": "independent", "reviewer_profile_ids": [reviewer.profile_id], "independence_must_be_revalidated": True}
        assert (await call(*work, worker_key))["state"] == "resume"
        started = await call("agent_get_complete_task_context", f"/api/agent/tasks/{task.id}/context", worker_key, task_id=task.id)
        assert started["started"] is True and started["start_ready"] is False and started["assignment"]["state"] == "accepted"
        assert not {"routing_selection_pending", "model_aware_assignment_inactive", "assignment_not_queued_execution",
                    "foreign_or_unknown_claim", "assignment_actor_ineligible"} & set(started["blocker_codes"])
        if case == "same_worker":
            async with db_session_factory() as audit:
                gone = await audit.get(AgentActor, worker.id)
                gone.enabled = False
                await audit.commit()
            dead = await call("agent_get_complete_task_context", f"/api/agent/tasks/{task.id}/context", pm_key,
                              task_id=task.id, assignment_id=rework["id"])
            assert dead["started"] is False and dead["start_ready"] is False
            assert "assignment_actor_ineligible" in dead["blocker_codes"]
            async with db_session_factory() as audit:
                (await audit.get(AgentActor, worker.id)).enabled = True
                await audit.commit()
        assert await stored_history(db_session_factory, rework["id"], review["id"], assigned["id"]) == previous_history
        async with db_session_factory() as audit:
            assert (await audit.get(AgentRun, running["run"]["id"])).execution_provenance == original_execution
            historical = await audit.scalar(select(AgentIdempotencyRecord.response_payload).where(
                AgentIdempotencyRecord.actor_id == reviewer.id, AgentIdempotencyRecord.operation == "verification.verdict",
                AgentIdempotencyRecord.target_id == review["id"]))
            assert historical == original_verdict
            if case == "same_worker":
                await audit.run_sync(assert_lookup_indexes)
        if case in {"failed_recovery", "canceled_recovery"}:
            outcome = case.split("_")[0]
            stopped = await call("agent_fail_my_work", "/api/agent/me/work/fail", worker_key, payload={
                **fence(resumed), "status": outcome, "observed_model": member.default_model_binding_key,
                "output_state": "retained", "summary": "Correction stopped", "evidence": {"condition": "fixture"}}, receipt="stop-rework")
            assert stopped["run"]["status"] == outcome and stopped["assignment"]["state"] == "cancelled"
            recovery = await call("agent_requeue_recovery", f"/api/agent/recovery/{task.id}/requeue", pm_key, task_id=task.id,
                payload={"actor_id": worker.id, "expected_task_version": stopped["task"]["version"],
                         "expected_claim_generation": resumed["claim_generation"], "expected_live_assignment_ids": [],
                         "expected_running_run_ids": [], "reason": "Preserve rework before choosing a new route"}, receipt="recover-stopped")
            waiting = await call(*work, worker_key)
            assert waiting["state"] == "wait" and waiting["blocked_assigned"][0]["assignment"]["id"] == recovery["assignment"]["id"]
            assert recovery["assignment"]["id"] != rework["id"] and "routing_selection_pending" in waiting["blocked_assigned"][0]["blocker_codes"]
            await call(*begin, worker_key, payload={"assignment_id": recovery["assignment"]["id"], "queue_revision": waiting["queue_revision"],
                       "model": member.default_model_binding_key}, receipt="recovery-needs-selection", error="routing_selection_pending")
            assert await stored_history(db_session_factory, rework["id"], review["id"], assigned["id"]) == previous_history
            return
        revised = await call(*submit, worker_key, payload={**fence(resumed), "observed_model": member.default_model_binding_key,
            "summary": "Clarified the instructions", "evidence": {"check": "verified the revised explanation"},
            "artifact_links": ["https://example.test/guide/revised"]}, receipt="submit-revision")
        if multi_reviewer:
            async with db_session_factory() as audit:
                alternate_binding = await review_provenance.actor_provenance(audit, alternate_verifier)
            assert alternate_verifier.profile_id != reviewer.profile_id
            assert alternate_binding["publisher_key"] == lineage["reviewer_publisher_key"]
            await call(*dispatch, pm_key, payload={"actor_id": alternate_verifier.id, "purpose": "verification", "task_id": task.id,
                "reviewer_profile_id": alternate_verifier.profile_id, "expected_task_version": revised["task"]["version"]},
                receipt="other-independent-profile", error="submitted rework requires its recorded independent reviewer profile")
            await assert_floor_preview(task.id, revised["task"]["version"], pm_key, reviewer, alternate_verifier)
            async with db_session_factory() as audit:
                assert not await audit.scalar(select(AgentTaskAssignment.id).where(AgentTaskAssignment.task_id == task.id,
                    AgentTaskAssignment.purpose == "verification", AgentTaskAssignment.state == "queued"))
        second_review = await call(*dispatch, pm_key, payload={"actor_id": reviewer.id, "task_id": task.id,
            "purpose": "verification", "reviewer_profile_id": reviewer.profile_id, "expected_task_version": revised["task"]["version"]},
            receipt="verify-revision")
        selected = second_review["review_selection"]
        expected_runs = {running["run"]["id"], resumed["run"]["id"]}
        if earlier_run:
            expected_runs.add(earlier_run["run"]["id"])
        assert {c["run_id"] for c in selected["contributors"]} == expected_runs
        rejected_again = await call(*verdict, reviewer_key, payload={**reject_request, "assignment_id": second_review["id"],
            "expected_task_version": revised["task"]["version"], "reviewed_candidate_digest": selected["candidate"]["digest"]},
            receipt="revise-again")
        second_queue = await call(*work, worker_key)
        assert second_queue["state"] == "start_assigned" and second_queue["next"]["assignment"]["id"] == rejected_again["rework_assignment"]["id"]
        second_begin = await call(*begin, worker_key, payload={"assignment_id": rejected_again["rework_assignment"]["id"],
            "queue_revision": second_queue["queue_revision"], "model": member.default_model_binding_key}, receipt="begin-second-revision")
        assert second_begin["claim_generation"] > resumed["claim_generation"] and second_begin["run"]["id"] != resumed["run"]["id"]
        assert second_begin["run"]["execution_provenance"]["supervised_rework"]["rejected_run_id"] == resumed["run"]["id"]
        if checked_writers:
            assert checked_writers == set(writes)
            async with db_session_factory() as competing:
                await competing.execute(text("SET LOCAL lock_timeout = '500ms'"))
                for statement in writes.values():
                    assert (await competing.execute(statement)).rowcount == 1
                await competing.commit()
            record_property("postgres_catalog_writer", "blocked with 55P03 during begin; committed after the fence")
            record_property("postgres_control_plane_writers", ",".join(sorted(checked_writers)))
