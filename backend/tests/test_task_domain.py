"""Domain commands preserve identity, evidence independence and bounded read contracts."""

from dataclasses import replace

import pytest
from sqlalchemy import func, select

from app.authority import Authority, AuthorityError
from app.models.identity import Principal, PrincipalProfileLink, ProjectMembership
from app.models.task import Task
from app.models.task_brief import TaskBriefRevision, TaskProgressRecord, TaskReviewRecord
from app.models.team_member import TeamMemberProfile
from app.schemas.task import TaskCreate, TaskUpdate
from app.schemas.task_brief import BriefConvert, BriefWrite, TaskBrief, BriefCriterion, ProgressWrite, CriterionProgress, TaskReviewWrite
from app.schemas.task_domain import TaskActionRequest
from app.services.task_brief_service import TaskBriefService, import_legacy_brief, render_brief
from app.services.task_domain_service import TaskDomainService, normalize_effort
from app.services.task_detail_service import TaskDetailService
from app.services.task_service import TaskService, TaskVersionConflictError
from app.services.work_metrics import aggregate_metrics
from tests.test_delivery_scenarios import delivery_store


async def human_context(db, project_id):
    worker = Principal(kind="human", display_name="Engineer")
    reviewer = Principal(kind="human", display_name="Reviewer")
    profile = TeamMemberProfile(display_name="Engineer", profile_kind="human")
    db.add_all([worker, reviewer, profile])
    await db.flush()
    db.add_all([PrincipalProfileLink(principal_id=worker.id, profile_id=profile.id, linked_by_principal_id=reviewer.id),
        ProjectMembership(principal_id=worker.id, project_id=project_id, role="manager"),
        ProjectMembership(principal_id=reviewer.id, project_id=project_id, role="reviewer")])
    await db.commit()
    return Authority(worker.id, "human", workspace_role="member", projects={project_id: "manager"}, profile_id=profile.id), reviewer.id


async def test_backlog_manual_execution_independent_review_and_reopen(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        worker, reviewer_id = await human_context(db, scenario.projects[0])
        db.info["authority"] = worker
        tasks = TaskService(db)
        brief = TaskBrief(goal="Restore the endpoint", acceptance_criteria=[BriefCriterion(id="healthy", text="The endpoint returns a healthy response")])
        task = await tasks.create(None, TaskCreate(title="Urgent request", project_id=scenario.projects[0], owner_profile_id=worker.profile_id, brief=brief))
        task_id = task.id
        assert task.iteration_id is None and task.effort_hours is None and task.effort_days is None
        assert task.owner_profile_id == worker.profile_id
        assert (await aggregate_metrics(db, project_id=scenario.projects[0]))["unknown_estimate_tasks"] >= 1
        task = await TaskDomainService(db).command(task_id, TaskActionRequest(action="start_manual", expected_version=task.version, reason="Handle the incident"))
        assert task.status == "active" and task.started_at and task.actual_start_date
        assert task.start_date is None and task.end_date is None
        task = await TaskBriefService(db).write_progress(task_id, ProgressWrite(expected_version=task.version,
            criteria=[CriterionProgress(criterion_id="healthy", criterion_revision=1, state="completed", evidence="Health request returns HTTP 200")]))
        task = await TaskDomainService(db).command(task_id, TaskActionRequest(action="resolve_manual", expected_version=task.version, reason="Implemented"))
        review = TaskReviewWrite(expected_version=task.version, brief_revision=task.brief_revision, artifact_revision=task.artifact_revision, verdict="accept", reason="Confirmed independently")
        with pytest.raises(AuthorityError, match="Another reviewer"):
            await TaskBriefService(db).review(task_id, review)
        db.info["authority"] = Authority(reviewer_id, "human", workspace_role="member", projects={scenario.projects[0]: "reviewer"})
        task = await TaskBriefService(db).review(task_id, review)
        assert task.accepted_by_principal_id == reviewer_id and task.accepted_version == task.version
        db.info["authority"] = worker
        task = await TaskDomainService(db).command(task_id, TaskActionRequest(action="reopen", expected_version=task.version, reason="New failure observed"))
        assert task.status == "active" and task.accepted_version is None
        assert await db.scalar(select(func.count()).select_from(TaskReviewRecord).where(TaskReviewRecord.task_id == task_id)) == 1


async def test_owner_and_ids_survive_commit_uncommit(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        worker, _ = await human_context(db, scenario.projects[0])
        db.info["authority"] = worker
        task = await TaskService(db).create(None, TaskCreate(title="Backlog deliverable", project_id=scenario.projects[0], owner_profile_id=worker.profile_id, effort_hours=2.25))
        task_id = task.id
        task = await TaskDomainService(db).command(task.id, TaskActionRequest(action="commit", expected_version=task.version, iteration_id=scenario.iterations[0], reason="Commit to delivery"))
        assert task.iteration_id == scenario.iterations[0] and task.owner_profile_id == worker.profile_id
        task = await TaskDomainService(db).command(task.id, TaskActionRequest(action="uncommit", expected_version=task.version, reason="Return to backlog"))
        assert task.id == task_id and task.owner_profile_id == worker.profile_id and task.effort_hours == 2.25
        assert task.iteration_id is None and task.assignee_id is None
        task = await TaskService(db).update(task_id, TaskUpdate(expected_version=task.version, owner_profile_id=None))
        response = TaskService(db).task_to_response(task)
        assert response.owner_profile_id is None and response.owner is None


def test_estimates_preserve_unknown_zero_and_nominal_day():
    assert normalize_effort({}, 6)["effort_hours"] is None
    assert normalize_effort({"effort_days": 0}, 6)["effort_hours"] == 0
    assert normalize_effort({"effort_hours": 1.5}, 6)["effort_days"] == 0.25
    assert normalize_effort({"effort_days": 0.25}, 6)["effort_hours"] == 1.5
    with pytest.raises(ValueError, match="disagree"):
        normalize_effort({"effort_days": 1, "effort_hours": 8}, 6)


def test_legacy_brief_conversion_is_stable_and_does_not_accept_checkmarks():
    text = "## Цель\nСохранить данные\n## Критерии приёмки\n- [x] Данные доступны\n  - вложенная проверка\n## Custom section\nKeep this text"
    first, notes = import_legacy_brief(42, text)
    second, _ = import_legacy_brief(42, text)
    assert first == second and len(first.acceptance_criteria) == 1
    assert "вложенная проверка" in first.context and "Keep this text" in first.context
    assert notes and "- [ ] Данные доступны" in render_brief(first)
    assert "[x]" not in render_brief(first)
    fenced, notes = import_legacy_brief(42, "## Acceptance criteria\n```md\n- [x] Example only\n```\n- [ ] Real criterion")
    assert [item.text for item in fenced.acceptance_criteria] == ["Real criterion"]
    assert "- [x] Example only" in fenced.context and notes


async def test_criteria_keep_identity_and_explicit_revisions(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        task = await TaskService(db).create(None, TaskCreate(title="Two criteria", project_id=scenario.projects[0],
            brief=TaskBrief(acceptance_criteria=[BriefCriterion(id="a", text="A"), BriefCriterion(id="b", text="B")])))
        service = TaskBriefService(db)
        before_version, task_id = task.version, task.id
        brief = TaskBrief.model_validate(task.brief)
        brief.acceptance_criteria.reverse()
        task = await service.write(task_id, BriefWrite(expected_version=task.version, brief=brief))
        assert [item["id"] for item in task.brief["acceptance_criteria"]] == ["b", "a"]
        assert [item["revision"] for item in task.brief["acceptance_criteria"]] == [1, 1]
        brief = TaskBrief.model_validate(task.brief)
        brief.acceptance_criteria[1].text = "A, clarified"
        task = await service.write(task_id, BriefWrite(expected_version=task.version, brief=brief))
        assert task.brief["acceptance_criteria"][1]["revision"] == 2
        with pytest.raises(TaskVersionConflictError):
            await service.write(task_id, BriefWrite(expected_version=before_version, brief=brief))
        assert await db.scalar(select(func.count()).select_from(TaskBriefRevision).where(TaskBriefRevision.task_id == task_id)) == 3


async def test_bounded_detail_does_not_populate_execution_children(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        parent = Task(title="Parent", project_id=scenario.projects[0], is_summary=True)
        db.add(parent)
        await db.flush()
        db.add_all([Task(title=f"Child {index}", project_id=scenario.projects[0], parent_id=parent.id) for index in range(120)])
        await db.commit()
        task_id = parent.id
    async with factory() as db:
        detail = await TaskDetailService(db).detail(task_id, limit=10)
        assert len(detail.children.items) == 10 and detail.children.has_more
        assert not detail.execution_context_complete
        assert "children" not in (await db.get(Task, task_id)).__dict__
        complete = await TaskService(db).get_by_id(task_id)
        assert len(complete.children) == 120
        next_page = await TaskDetailService(db).detail(task_id, limit=10, children_after_id=detail.children.next_after_id)
        assert {item.id for item in detail.children.items}.isdisjoint(item.id for item in next_page.children.items)


async def test_backlog_recovery_keeps_ids_and_append_only_brief_history(delivery_store):
    from app.services.backlog_snapshot_service import BacklogSnapshotService
    factory, scenario, _ = delivery_store
    async with factory() as db:
        tasks = TaskService(db)
        task = await tasks.create(None, TaskCreate(title="Original backlog work", project_id=scenario.projects[0],
            brief=TaskBrief(goal="Original goal", acceptance_criteria=[BriefCriterion(id="stable", text="Original result")]), effort_hours=0))
        task_id = task.id
        snapshots = BacklogSnapshotService(db)
        saved = await snapshots.capture(scenario.projects[0])
        await tasks.delete(task_id, expected_version=task.version)
        history = await db.scalar(select(TaskBriefRevision).where(TaskBriefRevision.original_task_id == task_id))
        assert history.task_id is None and history.payload["goal"] == "Original goal"
        newer = await tasks.create(None, TaskCreate(title="New unrelated capture", project_id=scenario.projects[0]))
        assert newer.id > task_id
        restored = await snapshots.restore(scenario.projects[0], saved, {newer.id: newer.version}, reason="Recover the original capture")
        assert [item.id for item in restored] == [task_id]
        assert restored[0].effort_hours == 0 and restored[0].brief.acceptance_criteria[0].id == "stable"
        assert restored[0].brief_revision > history.revision
        assert await db.scalar(select(func.count()).select_from(TaskBriefRevision).where(TaskBriefRevision.original_task_id == task_id)) == 2


async def test_cancel_requires_current_execution_ownership_and_invalidates_fence(delivery_store):
    from datetime import timedelta
    from app.models.agent import AgentRun, AgentTaskAssignment
    from app.utils.time import utc_now
    factory, scenario, _ = delivery_store
    async with factory() as db:
        task = await db.get(Task, scenario.tasks["active"])
        task.claimed_by, task.claim_id, task.claim_generation = scenario.actors[0], "a" * 32, 4
        task.claim_expires_at = utc_now() + timedelta(hours=1)
        assignment = AgentTaskAssignment(task_id=task.id, actor_id=scenario.actors[0], purpose="execution", state="accepted", task_version=task.version)
        db.add(assignment)
        await db.flush()
        run = AgentRun(task_id=task.id, actor_id=scenario.actors[0], assignment_id=assignment.id, claim_generation=4, status="running")
        db.add(run)
        await db.commit()
        task_id, version, assignment_id, run_id = task.id, task.version, assignment.id, run.id
        with pytest.raises(AuthorityError, match="Reload current"):
            await TaskDomainService(db).command(task_id, TaskActionRequest(action="cancel", expected_version=version, reason="Stop this work"))
        task = await TaskDomainService(db).command(task_id, TaskActionRequest(action="cancel", expected_version=version, reason="Stop this work",
            expected_claim_generation=4, expected_running_run_ids=[run_id], expected_live_assignment_ids=[assignment_id]))
        assert task.canceled_at is not None and task.claimed_by is None and task.claim_generation == 5
        assert (await db.get(AgentRun, run_id)).status == "cancelled"
        assert (await db.get(AgentTaskAssignment, assignment_id)).state == "cancelled"
        assert task.status == "active"
        with pytest.raises(AuthorityError):
            await TaskDomainService(db).command(task_id, TaskActionRequest(action="cancel", expected_version=task.version, reason="Replay"))


async def test_shared_actions_rest_mcp_and_explicit_backlog_triage(delivery_store):
    import httpx
    from app.main import app
    from app import mcp_agent_tools
    from app.models.agent import AgentActor
    from app.services.identity_service import IdentityService
    factory, scenario, _ = delivery_store
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        created = await client.post(f"/api/projects/{scenario.projects[0]}/backlog", json={"title": "API backlog"})
        assert created.status_code == 201, created.text
        task = created.json()
        assert task["iteration_id"] is None and task["effort_hours"] is None
        before = await client.get(f"/api/tasks/{task['id']}/detail")
        assert before.status_code == 200 and before.json()["execution_context_complete"] is False
        auth = {"X-Agent-API-Key": scenario.actor_keys[0]}
        rest = await client.get(f"/api/tasks/{task['id']}/actions", headers=auth)
        assert rest.status_code == 200, rest.text
        async with factory() as db:
            actor = await db.get(AgentActor, scenario.actors[0])
            db.info["authority"] = await IdentityService(db).actor_context(actor)
            mcp = await mcp_agent_tools.get_task_actions(db, actor, task["id"])
        assert rest.json() == mcp
        manual = next(item for item in mcp["actions"] if item["action"] == "start_manual")
        assert not manual["allowed"] and "human_execution_required" in {item["code"] for item in manual["blockers"]}
        intake = await client.post("/api/triage", json={"title": "Triage backlog", "project_hint_id": scenario.projects[0]})
        assert intake.status_code == 201, intake.text
        legacy = await client.post(f"/api/triage/{intake.json()['id']}/convert-to-task", json={"project_id": scenario.projects[0]})
        assert legacy.status_code == 422 and legacy.json()["detail"][0]["loc"] == ["body", "iteration_id"]
        converted = await client.post(f"/api/triage/{intake.json()['id']}/convert-to-backlog", json={"project_id": scenario.projects[0], "acceptance_criteria": ["A reviewer can inspect the result"]})
        assert converted.status_code == 200, converted.text
        assert converted.json()["task"]["iteration_id"] is None
        assert converted.json()["task"]["brief"]["acceptance_criteria"][0]["text"] == "A reviewer can inspect the result"


async def test_rework_requires_fresh_progress_and_preserves_prior_evidence(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        worker, reviewer_id = await human_context(db, scenario.projects[0])
        db.info["authority"] = worker
        task = await TaskService(db).create(None, TaskCreate(title="Review and rework", project_id=scenario.projects[0],
            brief=TaskBrief(goal="Deliver", acceptance_criteria=[BriefCriterion(id="result", text="Correct result")])) )
        task_id = task.id
        commands, briefs = TaskDomainService(db), TaskBriefService(db)
        task = await commands.command(task_id, TaskActionRequest(action="start_manual", expected_version=task.version, reason="Begin work"))
        task = await briefs.write_progress(task_id, ProgressWrite(expected_version=task.version, criteria=[CriterionProgress(criterion_id="result", criterion_revision=1, state="completed", evidence="Original evidence")]))
        task = await commands.command(task_id, TaskActionRequest(action="resolve_manual", expected_version=task.version, reason="Ready for review"))
        reviewer = Authority(reviewer_id, "human", workspace_role="member", projects={scenario.projects[0]: "reviewer"})
        db.info["authority"] = reviewer
        task = await briefs.review(task_id, TaskReviewWrite(expected_version=task.version, brief_revision=task.brief_revision, artifact_revision=task.artifact_revision, verdict="reject", reason="The result needs correction"))
        assert task.progress is None and task.executed_by_principal_id == worker.principal_id
        assert await db.scalar(select(func.count()).select_from(TaskProgressRecord).where(TaskProgressRecord.original_task_id == task_id)) == 1
        db.info["authority"] = worker
        task = await commands.command(task_id, TaskActionRequest(action="resolve_manual", expected_version=task.version, reason="Attempt to reuse old evidence"))
        request = TaskReviewWrite(expected_version=task.version, brief_revision=task.brief_revision, artifact_revision=task.artifact_revision, verdict="accept", reason="Review again")
        db.info["authority"] = reviewer
        with pytest.raises(ValueError, match="Current brief evidence"):
            await briefs.review(task_id, request)


async def test_triage_handoff_preserves_canonical_fields_and_criterion_ids(delivery_store):
    from app.schemas.triage import TriageItemCreate, TriageItemResponse, TriageConvertToBacklogRequest
    from app.services.triage_service import TriageService
    factory, scenario, _ = delivery_store
    async with factory() as db:
        worker, _ = await human_context(db, scenario.projects[0])
        db.info["authority"] = replace(worker, workspace_role=None)
        brief = TaskBrief(goal="Retain the draft", context="Original context", acceptance_criteria=[BriefCriterion(id="stable", text="Original criterion")])
        service = TriageService(db)
        item = await service.create(TriageItemCreate(title="Captured work", project_hint_id=scenario.projects[0], metadata_json={"task_brief": brief.model_dump()}))
        assert TriageItemResponse.model_validate(item).brief == brief
        assert "Original context" in item.description
        _, task = await service.convert_to_task(item.id, TriageConvertToBacklogRequest(project_id=scenario.projects[0]))
        assert task.brief["acceptance_criteria"][0]["id"] == "stable"


async def test_managed_assigned_submission_and_independent_rework(delivery_store):
    import json
    from datetime import timedelta
    from app.commands import command_transaction
    from app.models.agent import AgentActor, AgentRun, AgentTaskAssignment
    from app.schemas.agent import AgentWorkSubmit, AgentReviewVerdict
    from app.services.agent_work_service import AgentWorkService
    from app.utils.time import utc_now
    factory, scenario, _ = delivery_store
    async with factory() as db:
        worker = await db.get(AgentActor, scenario.actors[0])
        verifier = await db.get(AgentActor, scenario.actors[1])
        worker.scopes = json.dumps(["work:execute", "tasks:read"])
        verifier.scopes = json.dumps(["verification:write", "verification:read", "tasks:read"])
        principals = [Principal(kind="agent", display_name=actor.display_name, agent_actor_id=actor.id) for actor in (worker, verifier)]
        db.add_all(principals)
        await db.flush()
        task = await TaskService(db).create(scenario.iterations[0], TaskCreate(title="Assigned canonical work", effort_hours=2,
            brief=TaskBrief(goal="Deliver", scope="Bounded change", verification="Inspect result", acceptance_criteria=[BriefCriterion(id="result", text="Correct result")]), project_id=scenario.projects[0]))
        task.status, task.executed_by_principal_id = "active", principals[0].id
        task.claimed_by, task.claim_id, task.claim_generation = worker.id, "a" * 32, 4
        task.claim_expires_at = utc_now() + timedelta(hours=1)
        assignment = AgentTaskAssignment(task_id=task.id, actor_id=worker.id, purpose="execution", state="accepted", task_version=task.version)
        db.add(assignment)
        await db.flush()
        run = AgentRun(task_id=task.id, actor_id=worker.id, assignment_id=assignment.id, claim_generation=4, status="running")
        db.add(run)
        await db.commit()
        task_id = task.id
        db.info["authority"] = Authority(principals[0].id, "agent", projects={scenario.projects[0]: "executor"}, actor_id=worker.id,
            actor_role="worker", source="agent_rest", scopes=frozenset(["work:execute", "tasks:read"]))
        async with command_transaction(db):
            response = await AgentWorkService(db).submit(worker, AgentWorkSubmit(assignment_id=assignment.id, run_id=run.id,
                claim_id="a" * 32, claim_generation=4, expected_task_version=task.version, summary="Implemented the bounded result",
                evidence={"inspection": "Result is available"}, criterion_progress=[CriterionProgress(criterion_id="result", criterion_revision=1, state="completed", evidence="Result inspected")]), idempotency_key="canonical-submit")
        assert response.task.status == "resolved"
        db.info.pop("authority")
        review = AgentTaskAssignment(task_id=task_id, actor_id=verifier.id, purpose="verification", state="queued", task_version=response.task.version)
        db.add(review)
        await db.commit()
        db.info["authority"] = Authority(principals[1].id, "agent", projects={scenario.projects[0]: "reviewer"}, actor_id=verifier.id,
            actor_role="verifier", source="agent_rest", scopes=frozenset(["verification:write", "verification:read", "tasks:read"]))
        async with command_transaction(db):
            result = await AgentWorkService(db).review(verifier, AgentReviewVerdict(assignment_id=review.id, verdict="reject",
                expected_task_version=response.task.version, evidence={"inspection": "Needs one correction"}, reason="Correct the result", rework_actor_id=worker.id),
                idempotency_key="canonical-reject", rationale="Independent inspection", correlation_id="canonical-review")
        assert result.task.status == "active" and result.task.progress is None
        assert result.rework_assignment.actor_id == worker.id
        assert (await db.get(Task, task_id)).executed_by_principal_id == principals[0].id


async def test_progress_availability_matches_open_leaf_execution_permission(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        worker, _ = await human_context(db, scenario.projects[0])
        task = await TaskService(db).create(None, TaskCreate(title="Evidence capture", project_id=scenario.projects[0]))
        await db.commit()
        db.info["authority"] = worker
        service = TaskDomainService(db)
        available = lambda result: next(item for item in result.actions if item.action == "record_progress")
        assert available(await service.allowed_actions(task.id)).allowed is True
        db.info["authority"] = replace(worker, projects={scenario.projects[0]: "viewer"}, workspace_role=None)
        assert available(await service.allowed_actions(task.id)).allowed is False
        db.info["authority"] = worker
        task.status = "closed"
        await db.flush()
        assert available(await service.allowed_actions(task.id)).allowed is False


async def test_current_review_does_not_depend_on_first_history_page(delivery_store):
    import httpx
    from app.main import app
    factory, scenario, _ = delivery_store
    async with factory() as db:
        worker, reviewer = await human_context(db, scenario.projects[0])
        task = await TaskService(db).create(None, TaskCreate(title="Long review history", project_id=scenario.projects[0]))
        task.version = 99
        for version in range(1, 56):
            db.add(TaskReviewRecord(task_id=task.id, original_task_id=task.id, task_version=version,
                brief_revision=0, artifact_revision=0, principal_id=reviewer, verdict="reject", reason="Earlier inspection", evidence="Earlier artifact"))
        db.add(TaskReviewRecord(task_id=task.id, original_task_id=task.id, task_version=99,
            brief_revision=0, artifact_revision=0, principal_id=reviewer, verdict="reject", reason="Current inspection", evidence="Current artifact"))
        await db.commit()
        task_id = task.id
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as reader:
        history = await reader.get(f"/api/tasks/{task_id}/reviews")
        assert len(history.json()) == 50
        current = await reader.get(f"/api/tasks/{task_id}/reviews/current")
        assert current.status_code == 200, current.text
        assert current.json()["task_version"] == 99
        assert current.json()["review"]["reason"] == "Current inspection"
