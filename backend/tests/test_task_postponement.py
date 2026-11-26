"""Postponed work stops natively, releases live execution under its fence, and resumes with its evidence intact."""

import re
from datetime import timedelta

import httpx
import pytest
from pydantic import ValidationError
from sqlalchemy import func, select

from app.authority import Authority, AuthorityError
from app.commands import PlanningConflict
from app.main import app
from app.models.agent import AgentActor, AgentRun, AgentTaskAssignment, TaskEvent
from app.models.delivery_observation import DeliveryObservation
from app.models.iteration import Iteration
from app.models.task import Task
from app.models.task_brief import TaskProgressRecord
from app.models.task_postponement import TaskPostponement, TaskReactivationRequirement
from app.models.task_status_log import TaskStatusLog
from app.models.triage import TriageItem
from app.schemas.task import TaskCreate, TaskUpdate
from app.schemas.task_brief import BriefCriterion, CriterionProgress, ProgressWrite, TaskBrief, TaskReviewWrite
from app.schemas.task_domain import TaskActionRequest
from app.schemas.task_postponement import TaskPostponeRequest, TaskReactivateRequest
from app.services.task_brief_service import TaskBriefService
from app.services.task_domain_service import TaskDomainService
from app.services.task_postponement_service import TaskPostponementService
from app.services.task_service import TaskService
from app.services.task_status_service import TaskStatusService
from app.utils.time import utc_now
from tests.test_delivery_scenarios import delivery_store
from tests.test_task_domain import human_context

__all__ = ["delivery_store"]


def _later(days=30):
    return (utc_now().date() + timedelta(days=days)).isoformat()


def _postpone(version, *requirements, reason="Waiting for the platform decision", **fence):
    return {"expected_version": version, "reason": reason,
            "requirements": list(requirements) or [{"kind": "date", "on_date": _later()}], **fence}


def _client():
    return httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test")


def _action(actions, name):
    return next(item for item in actions["actions"] if item["action"] == name)


@pytest.mark.parametrize("from_status", ["planned", "active", "resolved"])
async def test_postpone_from_each_open_status_records_reason_requirements_and_history(delivery_store, from_status):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        triage = TriageItem(title="Confirm the vendor contract", project_hint_id=scenario.projects[0])
        db.add(triage)
        await db.commit()
        task = await db.get(Task, scenario.tasks[from_status])
        task_id, version, triage_id = task.id, task.version, triage.id
    requirements = [
        {"kind": "predecessor_accepted", "task_id": scenario.tasks["planned" if from_status != "planned" else "active"]},
        {"kind": "date", "on_date": _later()},
        {"kind": "owner_decision", "description": "The owner decides whether the Android scope stays"},
        {"kind": "linked_resolved", "triage_item_id": triage_id},
    ]
    async with _client() as client:
        before = await client.get(f"/api/tasks/{task_id}/actions")
        assert _action(before.json(), "postpone")["allowed"], before.text
        assert "not_postponed" in {item["code"] for item in _action(before.json(), "reactivate")["blockers"]}
        response = await client.post(f"/api/tasks/{task_id}/postpone", json=_postpone(version, *requirements))
        assert response.status_code == 200, response.text
        body = response.json()
        assert body["task"]["status"] == "postponed" and body["task"]["version"] == version + 1
        record = body["postponement"]
        assert record["open"] and record["from_status"] == from_status
        assert record["reason"] == "Waiting for the platform decision" and record["task_version"] == version + 1
        assert [item["kind"] for item in record["requirements"]] == [item["kind"] for item in requirements]
        assert all(item["met_at"] is None for item in record["requirements"])
        assert record["released"] == {"claim_actor_id": None, "claim_generation": None, "assignment_ids": [], "run_ids": []}
        read = await client.get(f"/api/tasks/{task_id}/postponement")
        assert read.status_code == 200, read.text
        assert read.json()["postponement"] == record
        assert {key: read.json()["task"][key] for key in ("id", "status", "version")} == {
            key: body["task"][key] for key in ("id", "status", "version")}
        after = (await client.get(f"/api/tasks/{task_id}/actions")).json()
        assert _action(after, "reactivate")["allowed"]
        assert "already_postponed" in {item["code"] for item in _action(after, "postpone")["blockers"]}
        assert not _action(after, "record_progress")["allowed"]
        again = await client.post(f"/api/tasks/{task_id}/postpone", json=_postpone(version + 1))
        assert again.status_code == 409 and again.json()["detail"]["code"] == "already_postponed"
    async with factory() as db:
        log = await db.scalar(select(TaskStatusLog).where(TaskStatusLog.task_id == task_id, TaskStatusLog.to_status == "postponed"))
        assert log.from_status == from_status and log.reason == "Waiting for the platform decision"
        event = await db.scalar(select(TaskEvent).where(TaskEvent.task_id == task_id, TaskEvent.event_type == "task_postponed"))
        assert event is not None
        assert await db.scalar(select(func.count()).select_from(TaskReactivationRequirement).where(
            TaskReactivationRequirement.task_id == task_id)) == 4


async def test_other_moves_into_or_out_of_postponed_are_refused(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        closed = await db.get(Task, scenario.tasks["closed_urgent"])
        parent = await db.get(Task, scenario.tasks["parent"])
        planned = await db.get(Task, scenario.tasks["planned"])
        closed_id, closed_version, parent_id, parent_version = closed.id, closed.version, parent.id, parent.version
        planned_id, planned_version = planned.id, planned.version
    async with _client() as client:
        refused = await client.post(f"/api/tasks/{closed_id}/postpone", json=_postpone(closed_version))
        assert refused.status_code == 409 and refused.json()["detail"]["code"] == "postpone_invalid_lifecycle"
        summary = await client.post(f"/api/tasks/{parent_id}/postpone", json=_postpone(parent_version))
        assert summary.status_code == 409 and summary.json()["detail"]["code"] == "postponement_leaf_required"
        missing = await client.post(f"/api/tasks/{planned_id}/postpone", json={**_postpone(planned_version), "requirements": []})
        assert missing.status_code == 422, missing.text
        unreasoned = await client.post(f"/api/tasks/{planned_id}/postpone", json=_postpone(planned_version, reason="  "))
        assert unreasoned.status_code == 422, unreasoned.text
        legacy = await client.put(f"/api/tasks/{planned_id}/status", json={"status": "postponed", "expected_version": planned_version})
        assert legacy.status_code == 422, legacy.text
        bulk = await client.post("/api/tasks/bulk-operations", json={"task_ids": [planned_id], "action": "change_status",
                                                                     "payload": {"status": "postponed"}, "dry_run": False})
        assert bulk.status_code == 400, bulk.text
        assert "Invalid status transition from 'planned' to 'postponed'" in bulk.json()["detail"]["results"][0]["error"]
        not_postponed = await client.post(f"/api/tasks/{planned_id}/reactivate", json={"expected_version": planned_version, "reason": "Resume"})
        assert not_postponed.status_code == 409 and not_postponed.json()["detail"]["code"] == "task_not_postponed"
    async with factory() as db:
        with pytest.raises(ValueError, match="postpone command"):
            await TaskService(db).change_status(planned_id, "postponed", expected_version=planned_version)
    async with factory() as db:
        await TaskPostponementService(db).postpone(planned_id, TaskPostponeRequest(**_postpone(planned_version)))
        with pytest.raises(ValueError, match="reactivate it first"):
            await TaskService(db).change_status(planned_id, "active", expected_version=planned_version + 1)
        task = await db.get(Task, planned_id)
        assert task.status == "postponed" and task.version == planned_version + 1


async def test_requirements_must_be_possible_and_not_already_met(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        planned = await db.get(Task, scenario.tasks["planned"])
        task_id, version = planned.id, planned.version
        canceled = await db.get(Task, scenario.tasks["closed_low"])
        canceled.canceled_at = utc_now()
        (await db.get(Task, scenario.tasks["closed_urgent"])).accepted_at = utc_now()
        triage = {status: TriageItem(title=f"Intake {status}", project_hint_id=scenario.projects[0], status=status)
                  for status in ("new", "snoozed", "accepted", "declined", "duplicate", "converted")}
        db.add_all(triage.values())
        await db.commit()
        triage = {status: item.id for status, item in triage.items()}
    cases = [
        ({"kind": "predecessor_accepted", "task_id": task_id}, "wait for itself"),
        ({"kind": "predecessor_accepted", "task_id": scenario.tasks["closed_urgent"]}, "already accepted"),
        ({"kind": "linked_resolved", "task_id": scenario.tasks["resolved"]}, "already resolved"),
        ({"kind": "linked_resolved", "task_id": scenario.tasks["closed_low"]}, "canceled"),
        ({"kind": "linked_resolved", "triage_item_id": 987654}, "not found"),
        ({"kind": "date", "on_date": (utc_now().date() - timedelta(days=1)).isoformat()}, "after today"),
        ({"kind": "predecessor_accepted", "task_id": 987654}, "not found"),
        *(({"kind": "linked_resolved", "triage_item_id": triage[status]}, "already resolved")
          for status in ("accepted", "declined", "duplicate", "converted")),
    ]
    async with _client() as client:
        for requirement, message in cases:
            response = await client.post(f"/api/tasks/{task_id}/postpone", json=_postpone(version, requirement))
            assert response.status_code == 422, (requirement, response.text)
            assert re.search(message, response.json()["detail"][0]["msg"]), response.text
        duplicate = {"kind": "date", "on_date": _later()}
        response = await client.post(f"/api/tasks/{task_id}/postpone", json=_postpone(version, duplicate, duplicate))
        assert response.status_code == 422 and "once" in response.text
    for shape in ({"kind": "date"}, {"kind": "owner_decision"}, {"kind": "linked_resolved", "task_id": 1, "triage_item_id": 1},
                  {"kind": "predecessor_accepted", "on_date": _later()}, {"kind": "owner_decision", "description": "x", "task_id": 1}):
        with pytest.raises(ValidationError):
            TaskPostponeRequest(**_postpone(1, shape))
    async with factory() as db:
        task = await db.get(Task, task_id)
        assert task.status == "planned" and task.version == version
        assert await db.scalar(select(func.count()).select_from(TaskPostponement)) == 0
        # New and snoozed triage items are still open, so they can be waited for.
        result = await TaskPostponementService(db).postpone(task_id, TaskPostponeRequest(**_postpone(
            version, *({"kind": "linked_resolved", "triage_item_id": triage[status]} for status in ("new", "snoozed")))))
        assert [item["triage_item_id"] for item in result["postponement"]["requirements"]] == [triage["new"], triage["snoozed"]]


async def _live_execution(db, scenario):
    """An active task with an expired claim, a queued execution assignment and a running run."""
    task = await db.get(Task, scenario.tasks["active"])
    worker = scenario.actors[0]
    task.claimed_by, task.claim_id, task.claim_generation = worker, "c" * 32, 6
    task.claim_expires_at = utc_now() - timedelta(hours=2)
    queued = AgentTaskAssignment(task_id=task.id, actor_id=worker, purpose="execution", queue_class="recovery",
                                 state="queued", task_version=task.version)
    db.add(queued)
    await db.flush()
    profile_id = (await db.get(AgentActor, worker)).profile_id
    run = AgentRun(task_id=task.id, actor_id=worker, claim_generation=5, status="running",
                   execution_provenance={"actor_id": worker, "profile_id": profile_id,
                                         "profile_revision": f"p{profile_id}-begin", "source": "authenticated_work_begin"})
    db.add(run)
    await db.commit()
    revision = (await db.get(AgentActor, worker)).queue_revision
    return task.id, task.version, queued.id, run.id, worker, profile_id, revision


async def test_postponing_live_work_releases_claim_assignment_and_run_under_the_fence(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        task_id, version, assignment_id, run_id, worker, profile_id, revision = await _live_execution(db, scenario)
    requirement = {"kind": "owner_decision", "description": "Owner confirms the API contract"}
    async with _client() as client:
        actions = (await client.get(f"/api/tasks/{task_id}/actions")).json()
        assert actions["claim_generation"] == 6 and actions["running_run_ids"] == [run_id]
        assert actions["live_assignment_ids"] == [assignment_id]
        blind = await client.post(f"/api/tasks/{task_id}/postpone", json=_postpone(version, requirement))
        assert blind.status_code == 409 and blind.json()["detail"]["code"] == "execution_ownership_changed", blind.text
        stale = await client.post(f"/api/tasks/{task_id}/postpone", json=_postpone(
            version, requirement, expected_claim_generation=5, expected_running_run_ids=[run_id],
            expected_live_assignment_ids=[assignment_id]))
        assert stale.status_code == 409 and stale.json()["detail"]["code"] == "execution_ownership_changed"
        fenced = await client.post(f"/api/tasks/{task_id}/postpone", json=_postpone(
            version, requirement, expected_claim_generation=actions["claim_generation"],
            expected_running_run_ids=actions["running_run_ids"], expected_live_assignment_ids=actions["live_assignment_ids"]))
        assert fenced.status_code == 200, fenced.text
        record = fenced.json()["postponement"]
        assert record["released"] == {"claim_actor_id": worker, "claim_generation": 7,
                                      "assignment_ids": [assignment_id], "run_ids": [run_id]}
        task = fenced.json()["task"]
        assert task["status"] == "postponed" and task["claimed_by"] is None and task["claim_expires_at"] is None
        timeline = await client.get(f"/api/tasks/{task_id}/timeline/page", params={"limit": 20})
        assert timeline.status_code == 200, timeline.text
        items = timeline.json()["items"]
        released = next(item for item in items if item["title"] == "execution_released")
        assert released["payload"]["run_ids"] == [run_id] and released["payload"]["assignment_ids"] == [assignment_id]
        assert released["payload"]["cause"] == "postponed" and released["payload"]["claim_generation"] == 7
        assert any(item["item_type"] == "status_log" and item["title"] == "active -> postponed" for item in items)
        assert any(item["title"] == "task_postponed" for item in items)
    async with factory() as db:
        task = await db.get(Task, task_id)
        assert (task.claimed_by, task.claim_id, task.claim_expires_at, task.claim_generation) == (None, None, None, 7)
        assignment = await db.get(AgentTaskAssignment, assignment_id)
        assert assignment.state == "cancelled" and assignment.reason.startswith("Postponed:")
        run = await db.get(AgentRun, run_id)
        assert run.status == "cancelled" and run.ended_at is not None
        # The server ended the run, so its execution provenance records the actor's profile.
        assert run.execution_provenance["terminal_profile_id"] == profile_id
        assert run.execution_provenance["source"] == "authenticated_work_begin"
        assert (await db.get(AgentActor, worker)).queue_revision == revision + 1
        # Postponing releases ownership without canceling the task.
        assert task.canceled_at is None
        assert await db.scalar(select(func.count()).select_from(TaskEvent).where(
            TaskEvent.task_id == task_id, TaskEvent.event_type == "execution_canceled")) == 0


async def _evidenced_task(db, scenario, *, resolve):
    worker, reviewer_id = await human_context(db, scenario.projects[0])
    db.info["authority"] = worker
    brief = TaskBrief(goal="Ship the export", acceptance_criteria=[BriefCriterion(id="export", text="The export downloads")])
    task = await TaskService(db).create(None, TaskCreate(title="Export", project_id=scenario.projects[0], brief=brief))
    commands = TaskDomainService(db)
    task = await commands.command(task.id, TaskActionRequest(action="start_manual", expected_version=task.version, reason="Begin"))
    task = await TaskBriefService(db).write_progress(task.id, ProgressWrite(expected_version=task.version, criteria=[
        CriterionProgress(criterion_id="export", criterion_revision=1, state="completed", evidence="Download returns HTTP 200")]))
    if resolve:
        task = await commands.command(task.id, TaskActionRequest(action="resolve_manual", expected_version=task.version, reason="Done"))
    return task, worker, reviewer_id


@pytest.mark.parametrize("from_status, returns_to", [("active", "planned"), ("resolved", "resolved")])
async def test_reactivation_returns_work_with_brief_progress_evidence_and_provenance_intact(delivery_store, from_status, returns_to):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        task, worker, reviewer_id = await _evidenced_task(db, scenario, resolve=from_status == "resolved")
        assert task.status == from_status
        kept = {name: getattr(task, name) for name in ("brief", "brief_revision", "progress", "artifact_revision", "started_at",
                                                      "actual_start_date", "resolved_at", "executed_by_principal_id", "execution_mode")}
        task_id, version = task.id, task.version
        records = await db.scalar(select(func.count()).select_from(TaskProgressRecord).where(TaskProgressRecord.original_task_id == task_id))
        service = TaskPostponementService(db)
        postponed = await service.postpone(task_id, TaskPostponeRequest(**_postpone(version)))
        assert postponed["task"].status == "postponed"
        assert {name: getattr(postponed["task"], name) for name in ("brief_revision", "progress", "artifact_revision")} == {
            name: kept[name] for name in ("brief_revision", "progress", "artifact_revision")}
        with pytest.raises(ValueError, match="open leaf work"):
            await TaskBriefService(db).write_progress(task_id, ProgressWrite(expected_version=version + 1, criteria=[
                CriterionProgress(criterion_id="export", criterion_revision=1, state="completed", evidence="Again")]))
        reactivated = await service.reactivate(task_id, TaskReactivateRequest(expected_version=version + 1, reason="Decision made"))
        assert reactivated["task"].status == returns_to and reactivated["task"].version == version + 2
        record = reactivated["postponement"]
        assert not record["open"] and record["reactivated_to_status"] == returns_to
        assert record["reactivation_trigger"] == "command" and record["reactivation_reason"] == "Decision made"
        assert record["reactivated_by_principal_id"] == worker.principal_id
        task = await db.get(Task, task_id)
        assert {name: getattr(task, name) for name in kept} == kept
        assert await db.scalar(select(func.count()).select_from(TaskProgressRecord).where(TaskProgressRecord.original_task_id == task_id)) == records
        logs = (await db.scalars(select(TaskStatusLog).where(TaskStatusLog.task_id == task_id).order_by(TaskStatusLog.id))).all()
        assert [(log.from_status, log.to_status) for log in logs][-2:] == [(from_status, "postponed"), ("postponed", returns_to)]
        if returns_to == "resolved":
            # The evidence still satisfies independent review after the round trip.
            db.info["authority"] = Authority(reviewer_id, "human", workspace_role="member", projects={scenario.projects[0]: "reviewer"})
            accepted = await TaskBriefService(db).review(task_id, TaskReviewWrite(
                expected_version=task.version, brief_revision=task.brief_revision, artifact_revision=task.artifact_revision,
                verdict="accept", reason="Confirmed independently"))
            assert accepted.status == "closed" and accepted.accepted_version == accepted.version


def _agent(actor_id, role, project_id):
    return Authority(None, "agent", actor_id=actor_id, actor_role=role, projects={project_id: "manager"},
                     scopes=frozenset({"tasks:read", "planning:read", "planning:write"}))


async def test_only_a_pm_project_manager_or_operator_decides(delivery_store):
    factory, scenario, _ = delivery_store
    project = scenario.projects[0]
    async with factory() as db:
        task = await db.get(Task, scenario.tasks["resolved"])
        task_id, version = task.id, task.version
        manager, reviewer_id = await human_context(db, project)
    refused = [
        (Authority(reviewer_id, "human", workspace_role="member", projects={project: "editor"}), "permission_denied"),
        (Authority(reviewer_id, "human", workspace_role="member", projects={project: "reviewer"}), "permission_denied"),
        (_agent(scenario.actors[0], "worker", project), "postpone_decider_required"),
        (_agent(scenario.actors[1], "verifier", project), "postpone_decider_required"),
    ]
    for authority, code in refused:
        async with factory() as db:
            db.info["authority"] = authority
            with pytest.raises(AuthorityError) as caught:
                await TaskPostponementService(db).postpone(task_id, TaskPostponeRequest(**_postpone(version)))
            assert caught.value.code == code
            actions = await TaskDomainService(db).allowed_actions(task_id)
            for name in ("postpone", "reactivate"):
                availability = next(item for item in actions.actions if item.action == name)
                assert not availability.allowed and code in {item.code for item in availability.blockers}
    async with factory() as db:
        # A PM of another project cannot see the task, let alone postpone it.
        db.info["authority"] = _agent(scenario.actors[0], "pm", scenario.projects[1])
        with pytest.raises(LookupError):
            await TaskPostponementService(db).postpone(task_id, TaskPostponeRequest(**_postpone(version)))
    pm = _agent(scenario.actors[0], "pm", project)
    async with factory() as db:
        db.info["authority"] = pm
        result = await TaskPostponementService(db).postpone(task_id, TaskPostponeRequest(**_postpone(version)))
        assert result["postponement"]["postponed_by_actor_id"] == scenario.actors[0]
        log = await db.scalar(select(TaskStatusLog).where(TaskStatusLog.task_id == task_id, TaskStatusLog.to_status == "postponed"))
        assert log.triggered_by == "agent"
    async with factory() as db:
        # Returning work to resolved is the PM's planning decision, not execution.
        db.info["authority"] = pm
        result = await TaskPostponementService(db).reactivate(task_id, TaskReactivateRequest(expected_version=version + 1, reason="Resume"))
        assert result["task"].status == "resolved" and result["postponement"]["reactivated_by_actor_id"] == scenario.actors[0]
    async with factory() as db:
        db.info["authority"] = manager
        result = await TaskPostponementService(db).postpone(task_id, TaskPostponeRequest(**_postpone(version + 2)))
        assert result["task"].status == "postponed"
        assert result["postponement"]["postponed_by_principal_id"] == manager.principal_id


async def test_deferred_and_postponed_are_independent(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        tasks = TaskService(db)
        task = await tasks.update(scenario.tasks["planned"], TaskUpdate(is_deferred=True, expected_version=1))
        assert task.status == "planned" and task.is_deferred
        result = await TaskPostponementService(db).postpone(task.id, TaskPostponeRequest(**_postpone(task.version)))
        assert result["task"].status == "postponed" and result["task"].is_deferred
        task = await tasks.update(task.id, TaskUpdate(is_deferred=False, expected_version=result["task"].version))
        assert task.status == "postponed" and not task.is_deferred
        result = await TaskPostponementService(db).reactivate(task.id, TaskReactivateRequest(expected_version=task.version, reason="Ready"))
        assert result["task"].status == "planned" and not result["task"].is_deferred


async def test_summary_rolls_up_postponed_leaves(delivery_store):
    assert TaskStatusService.derive_parent_status(["postponed", "postponed"]) == "postponed"
    assert TaskStatusService.derive_parent_status(["postponed", "planned"]) == "planned"
    assert TaskStatusService.derive_parent_status(["postponed", "closed"]) == "active"
    assert TaskStatusService.derive_parent_status(["postponed", "active"]) == "active"
    factory, scenario, _ = delivery_store
    async with factory() as db:
        nested = await db.get(Task, scenario.tasks["nested"])
        nested_id, version = nested.id, nested.version
        service = TaskPostponementService(db)
        await service.postpone(nested_id, TaskPostponeRequest(**_postpone(version)))
        assert (await db.get(Task, scenario.tasks["parent"])).status == "postponed"
        await service.reactivate(nested_id, TaskReactivateRequest(expected_version=version + 1, reason="Resume"))
        assert (await db.get(Task, scenario.tasks["parent"])).status == "planned"


async def test_cancel_and_reopen_keep_the_open_postponement(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        task = await db.get(Task, scenario.tasks["resolved"])
        task_id, version = task.id, task.version
        await TaskPostponementService(db).postpone(task_id, TaskPostponeRequest(**_postpone(version)))
        commands = TaskDomainService(db)
        task = await commands.command(task_id, TaskActionRequest(action="cancel", expected_version=version + 1, reason="Drop it"))
        assert task.canceled_at is not None and task.status == "postponed"
        version = task.version
        with pytest.raises(PlanningConflict, match="Reopen canceled work"):
            await TaskPostponementService(db).reactivate(task_id, TaskReactivateRequest(expected_version=version, reason="Resume"))
    async with factory() as db:
        observed = await db.scalar(select(func.count()).select_from(DeliveryObservation).where(DeliveryObservation.original_task_id == task_id))
        task = await TaskDomainService(db).command(task_id, TaskActionRequest(action="reopen", expected_version=version, reason="Keep it"))
        assert task.canceled_at is None and task.status == "postponed"
        # Reopened postponed work stays stopped, so it starts no delivery episode.
        assert await db.scalar(select(func.count()).select_from(DeliveryObservation).where(
            DeliveryObservation.original_task_id == task_id)) == observed
        result = await TaskPostponementService(db).reactivate(task_id, TaskReactivateRequest(expected_version=task.version, reason="Resume"))
        assert result["task"].status == "resolved" and result["postponement"]["from_status"] == "resolved"


async def test_snapshot_restore_cannot_move_work_into_or_out_of_postponed(delivery_store):
    from app.services.snapshot_service import SnapshotService
    factory, scenario, _ = delivery_store
    async with factory() as db:
        task = await db.get(Task, scenario.tasks["planned"])
        await TaskPostponementService(db).postpone(task.id, TaskPostponeRequest(**_postpone(task.version)))
        snapshots = await SnapshotService(db).list_snapshots(scenario.iterations[0])
        before = next(item for item in snapshots if "before_task_postpone" in item["filename"])
        revision = (await db.get(Iteration, scenario.iterations[0])).revision
        with pytest.raises(PlanningConflict) as caught:
            await SnapshotService(db).restore(scenario.iterations[0], before["filename"], expected_revision=revision)
        assert caught.value.code == "restore_conflicts_with_task_postponement"
    async with factory() as db:
        assert (await db.get(Task, scenario.tasks["planned"])).status == "postponed"
        assert await db.scalar(select(func.count()).select_from(TaskPostponement).where(TaskPostponement.reactivated_at.is_(None))) == 1


async def test_work_an_open_postponement_waits_for_cannot_be_deleted(delivery_store):
    from app.services.iteration_service import IterationService
    from app.services.task_postponement_service import require_unreferenced
    factory, scenario, _ = delivery_store
    async with factory() as db:
        triage = TriageItem(title="Vendor answer", project_hint_id=scenario.projects[1])
        db.add(triage)
        await db.commit()
        waiting = await db.get(Task, scenario.tasks["other_project"])
        waiting_id, waiting_version, triage_id = waiting.id, waiting.version, triage.id
        target = await db.get(Task, scenario.tasks["planned"])
        target_id, target_version = target.id, target.version
        await TaskPostponementService(db).postpone(waiting_id, TaskPostponeRequest(**_postpone(
            waiting_version, {"kind": "predecessor_accepted", "task_id": target_id},
            {"kind": "linked_resolved", "triage_item_id": triage_id})))
    async with factory() as db:
        with pytest.raises(PlanningConflict) as caught:
            await TaskService(db).delete(target_id, expected_version=target_version)
        assert caught.value.code == "reactivation_requirement_referenced"
        assert f"postponed task {waiting_id}" in str(caught.value)
    async with factory() as db:
        # Deleting the iteration would delete the awaited task with it.
        with pytest.raises(PlanningConflict) as caught:
            await IterationService(db).delete(scenario.iterations[0])
        assert caught.value.code == "reactivation_requirement_referenced"
    async with factory() as db:
        with pytest.raises(PlanningConflict, match=f"Triage item {triage_id}"):
            await require_unreferenced(db, triage_item_ids=[triage_id])
        # Deleting the postponed task together with what it waits for is allowed.
        await require_unreferenced(db, task_ids=[target_id, waiting_id])
        assert await db.get(Task, target_id) is not None
    async with factory() as db:
        await TaskPostponementService(db).reactivate(waiting_id, TaskReactivateRequest(expected_version=waiting_version + 1, reason="Resume"))
        # Once the postponement is closed, the named work can go; the history keeps the requirement.
        assert await TaskService(db).delete(target_id, expected_version=target_version)
        requirement = await db.scalar(select(TaskReactivationRequirement).where(
            TaskReactivationRequirement.task_id == waiting_id, TaskReactivationRequirement.kind == "predecessor_accepted"))
        assert requirement.target_task_id is None
    async with factory() as db:
        # A deleted postponed task takes its own postponement and requirements with it.
        other = await db.get(Task, scenario.tasks["active"])
        other_id, other_version = other.id, other.version
        await TaskPostponementService(db).postpone(other_id, TaskPostponeRequest(**_postpone(other_version)))
        assert await TaskService(db).delete(other_id, expected_version=other_version + 1)
        assert await db.scalar(select(func.count()).select_from(TaskPostponement).where(TaskPostponement.task_id == other_id)) == 0


async def test_never_postponed_task_has_no_postponement_record(delivery_store):
    _, scenario, _ = delivery_store
    async with _client() as client:
        response = await client.get(f"/api/tasks/{scenario.tasks['planned']}/postponement")
        assert response.status_code == 404, response.text
        capabilities = await client.get("/api/tasks/capabilities")
        assert "task-postponement-v1" in capabilities.json()["features"], capabilities.text
