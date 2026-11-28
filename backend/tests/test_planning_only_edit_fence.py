"""A planning-only task edit keeps sealed issued work valid; an execution-input edit still stales it."""

import json
from datetime import timedelta
from types import SimpleNamespace

import httpx
import pytest
from sqlalchemy import select

from app.config import get_settings
from app.main import app
from app.models.agent import AgentModelCatalogEntry, AgentRun, AgentTaskAssignment, TaskEvent
from app.models.identity import Principal, ProjectMembership, WorkspaceMembership
from app.models.iteration import Iteration
from app.models.project import Project, ProjectMilestone
from app.models.task import Task
from app.services.agent_work_service import AgentWorkService
from app.services.execution_planning_window import (
    ITERATION_END_EXTENSION,
    PLANNING_ONLY_EDIT,
    PLANNING_ONLY_FIELDS,
    current_window,
    is_planning_only_change,
)
from app.services.identity_service import IdentityService, initialize_control_plane
from tests.test_agent_team_setup_qualification import provision_ready_topology, routing_base
from tests.test_review_provenance_transports import databases, fence
from tests import test_team_pm_dispatch
from tests.test_team_pm_recovery import recovery_api

db_session_factory = test_team_pm_dispatch.db_session_factory

WORK = ("agent_get_my_work", "/api/agent/me/work")
BEGIN = ("agent_begin_my_work", "/api/agent/me/work/begin")
RENEW = ("agent_renew_my_work", "/api/agent/me/work/renew")
SUBMIT = ("agent_submit_my_work", "/api/agent/me/work/submit")
DISPATCH = ("agent_create_assignment", "/api/agent/assignments")
RECOVERY = ("agent_list_recovery_tasks", "/api/agent/recovery")
VERDICT = ("agent_submit_review_verdict", "/api/agent/me/reviews/verdict")


def test_planning_only_fields_are_explicit_and_exclude_execution_inputs():
    assert PLANNING_ONLY_FIELDS == {"milestone_id"}
    assert is_planning_only_change({"milestone_id": {"old": None, "new": 3}})
    assert not is_planning_only_change({})
    for execution_input in (
        "brief_revision",
        "title",
        "description",
        "assignee_id",
        "depends_on",
        "project_id",
        "priority",
        "tags",
        "effort_hours",
        "is_deferred",
        "min_start_date",
        "max_end_date",
        "source_url",
    ):
        assert not is_planning_only_change({execution_input: {}}), execution_input
        assert not is_planning_only_change({"milestone_id": {}, execution_input: {}}), execution_input


async def team_scope(db, task_factory, team_member_factory, *, summary=False):
    """A ready team, one routed task in a strict-review project with two milestones."""
    system = await initialize_control_plane(db)
    await db.commit()
    team = await provision_ready_topology(db)
    member, verifier = team.manifest.workers[0], team.manifest.verifiers[0]
    worker = team.actors[member.actor_key]
    reviewer = team.actors[verifier.actor_key]
    pm = team.actors[team.manifest.controller.actor_key]
    scope = await routing_base(
        db,
        topology=team,
        actor_key=member.actor_key,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        title="Write the operator notes",
    )
    task = scope.task
    project = Project(name="Operator notes", require_different_review_publisher=True)
    db.add(project)
    await db.flush()
    iteration = await db.get(Iteration, task.iteration_id)
    task.project_id = iteration.project_id = project.id
    task.effort_hours = 8
    milestones = [ProjectMilestone(project_id=project.id, name=name) for name in ("Draft", "Release")]
    prerequisite = Task(title="Collect the source notes", project_id=project.id, iteration_id=iteration.id, status="planned")
    db.add_all([*milestones, prerequisite])
    other_capacity = await team_member_factory(
        profile=team.actors[team.manifest.workers[1].actor_key].profile, iteration=iteration
    )
    parent = None
    if summary:
        parent = Task(title="Notes package", project_id=project.id, iteration_id=iteration.id, is_summary=True, status="planned")
        db.add(parent)
        await db.flush()
        task.parent_id = parent.id
    for actor, role in [(pm, "manager"), (worker, "executor"), (reviewer, "reviewer")]:
        principal = await IdentityService(db).actor_context(actor)
        db.add_all(
            [
                WorkspaceMembership(principal_id=principal.principal_id, role="member"),
                ProjectMembership(principal_id=principal.principal_id, project_id=project.id, role=role),
            ]
        )
    for model, publisher in [(member, "first-publisher"), (verifier, "second-publisher")]:
        entry = await db.scalar(
            select(AgentModelCatalogEntry).where(AgentModelCatalogEntry.key == model.default_model_binding_key)
        )
        entry.publisher_key = publisher
    await db.commit()
    return SimpleNamespace(
        system=system,
        pm=pm,
        task=task,
        parent=parent,
        prerequisite=prerequisite,
        other_capacity=other_capacity.id,
        milestones=[row.id for row in milestones],
        member=member,
        verifier=verifier,
        worker=worker,
        reviewer=reviewer,
        wk=team.sink.keys[member.actor_key],
        rk=team.sink.keys[verifier.actor_key],
        pk=team.sink.keys[team.manifest.controller.actor_key],
    )


async def planning_patch(http, pm_key, task_id, expected_version, key, **changes):
    response = await http.patch(
        f"/api/agent/planning/tasks/{task_id}",
        headers={
            "X-Agent-API-Key": pm_key,
            "Idempotency-Key": key,
            "X-Correlation-ID": key,
            "X-Agent-Rationale": "Apply the approved planning change",
        },
        json={"expected_version": expected_version, **changes},
    )
    assert response.status_code == 200, response.text
    return response.json()


async def snapshot(factory, task_id, assignment_id, run_id=None):
    async with factory() as read:
        task = await read.get(Task, task_id)
        assignment = await read.get(AgentTaskAssignment, assignment_id)
        run = await read.get(AgentRun, run_id) if run_id else None
        events = (
            await read.scalars(
                select(TaskEvent)
                .where(TaskEvent.task_id == task_id, TaskEvent.event_type == "task.execution_planning_window")
                .order_by(TaskEvent.id)
            )
        ).all()
        return SimpleNamespace(
            version=task.version,
            milestone_id=task.milestone_id,
            window=current_window(task),
            claim=(task.claim_id, task.claim_generation, task.claimed_by),
            progress=task.progress,
            assignment=(assignment.state, assignment.task_version, assignment.routing_snapshot),
            model_aware=AgentWorkService._is_model_aware_assignment(assignment),
            run=(run.status, run.claim_generation, run.execution_provenance) if run else None,
            events=[json.loads(event.payload) for event in events],
        )


@databases
@pytest.mark.parametrize("transport", ["rest", "mcp"])
@pytest.mark.parametrize(
    "case", ["running", "consecutive", "after_extension", "queued", "summary", "verification", "rework"]
)
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_milestone_change_keeps_issued_work(
    db_session, db_session_factory, task_factory, team_member_factory, monkeypatch, transport, case
):
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    get_settings.cache_clear()
    s = await team_scope(db_session, task_factory, team_member_factory, summary=case == "summary")
    task, wk, rk, pk = s.task, s.wk, s.rk, s.pk
    retained = {
        "summary": "Operator notes complete",
        "observed_model": s.member.default_model_binding_key,
        "evidence": {"criteria": "checked instructions"},
        "artifact_links": ["https://example.test/notes"],
    }
    async with (
        recovery_api(transport, db_session_factory, monkeypatch) as call,
        httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://localhost:8001") as http,
    ):
        assigned = await call(
            *DISPATCH,
            pk,
            payload={
                "actor_id": s.worker.id,
                "task_id": task.id,
                "expected_task_version": task.version,
                "reviewer_profile_id": s.reviewer.profile_id,
            },
            receipt="assign-notes",
        )
        live_id, running, review = assigned["id"], None, None
        if case != "queued":
            queue = await call(*WORK, wk)
            running = await call(
                *BEGIN,
                wk,
                payload={
                    "assignment_id": assigned["id"],
                    "queue_revision": queue["queue_revision"],
                    "model": s.member.default_model_binding_key,
                },
                receipt="begin-notes",
            )
        if case in {"verification", "rework"}:
            submitted = await call(*SUBMIT, wk, payload={**fence(running), **retained}, receipt="submit-notes")
            review = await call(
                *DISPATCH,
                pk,
                payload={
                    "actor_id": s.reviewer.id,
                    "task_id": task.id,
                    "purpose": "verification",
                    "reviewer_profile_id": s.reviewer.profile_id,
                    "expected_task_version": submitted["task"]["version"],
                },
                receipt="assign-review",
            )
            live_id, running = review["id"], None
            if case == "rework":
                rejected = await call(
                    *VERDICT,
                    rk,
                    payload={
                        "assignment_id": review["id"],
                        "verdict": "reject",
                        "reason": "Clarify the operator example",
                        "rework_actor_id": s.worker.id,
                        "observed_model": s.verifier.default_model_binding_key,
                        "reviewed_candidate_digest": review["review_selection"]["candidate"]["digest"],
                        "evidence": {"criterion": "example needs clarification"},
                        "expected_task_version": submitted["task"]["version"],
                    },
                    receipt="reject-notes",
                )
                live_id = rejected["rework_assignment"]["id"]
        run_id = running["run"]["id"] if running else None
        before = await snapshot(db_session_factory, task.id, live_id, run_id)
        assert before.window is None
        # Rework carries routing lineage, so it is a model-aware assignment
        # that a scheduler date rebind would leave alone.
        assert before.model_aware == (case == "rework")

        steps = 1
        if case == "after_extension":
            async with db_session_factory() as read:
                iteration = await read.get(Iteration, task.iteration_id)
                revision, end = iteration.revision, iteration.end_date
            extended = await http.patch(
                f"/api/agent/planning/iterations/{task.iteration_id}",
                headers={
                    "X-Agent-API-Key": pk,
                    "Idempotency-Key": "extend-notes",
                    "X-Correlation-ID": "extend-notes",
                    "X-Agent-Rationale": "Apply the approved planning change",
                },
                json={
                    "expected_revisions": {str(task.iteration_id): revision},
                    "end_date": (end + timedelta(days=7)).isoformat(),
                },
            )
            assert extended.status_code == 200, extended.text
            extension = await snapshot(db_session_factory, task.id, live_id, run_id)
            assert extension.window["kind"] == ITERATION_END_EXTENSION
            assert [event["window_kind"] for event in extension.events] == [ITERATION_END_EXTENSION]
            steps = 2

        edited = s.parent if case == "summary" else task
        async with db_session_factory() as read:
            edited_version = (await read.get(Task, edited.id)).version
        patched = await planning_patch(
            http, pk, edited.id, edited_version, "set-milestone", milestone_id=s.milestones[0]
        )
        assert patched["result"]["milestone_id"] == s.milestones[0]
        if case == "consecutive":
            await planning_patch(
                http, pk, task.id, edited_version + 1, "move-milestone", milestone_id=s.milestones[1]
            )
            steps = 2

        after = await snapshot(db_session_factory, task.id, live_id, run_id)
        assert after.version == before.version + steps
        # The assignment, its routing evidence, the run, the claim and the
        # recorded progress are untouched; only the sealed window explains them.
        assert after.assignment == before.assignment and after.run == before.run
        assert after.claim == before.claim and after.progress == before.progress
        assert after.window["kind"] == PLANNING_ONLY_EDIT
        assert (after.window["from"], after.window["through"]) == (before.version, after.version)
        assert set(after.window["assignments"]) == {str(live_id)}
        assert after.window["evidence"] == {"fields": ["milestone_id"], "edited_task_id": edited.id}
        assert len(after.events) == steps
        recorded = after.events[-1]
        assert {key: recorded.get(key) for key in after.window["evidence"]} == after.window["evidence"]
        assert (recorded["window_kind"], recorded["from"], recorded["through"], recorded["assignment_ids"]) == (
            PLANNING_ONLY_EDIT,
            before.version,
            after.version,
            [live_id],
        )
        if case == "summary":
            assert after.milestone_id is None
        else:
            assert after.milestone_id == s.milestones[1 if case == "consecutive" else 0]
        recovery = await call(*RECOVERY, pk)
        assert all(item["task"]["id"] != task.id for item in recovery["items"]), recovery

        if case == "verification":
            done = await call(
                *VERDICT,
                rk,
                payload={
                    "assignment_id": review["id"],
                    "verdict": "pass",
                    "reason": "Verified the submitted notes",
                    "observed_model": s.verifier.default_model_binding_key,
                    "reviewed_candidate_digest": review["review_selection"]["candidate"]["digest"],
                    "evidence": {"criteria": "complete"},
                    "expected_task_version": after.version,
                },
                receipt="accept-notes",
            )
            assert done["task"]["status"] == "closed"
            return
        if case in {"queued", "rework"}:
            ready = await call(*WORK, wk)
            assert ready["state"] == "start_assigned" and ready["next"]["assignment"]["id"] == live_id
            started = await call(
                *BEGIN,
                wk,
                payload={
                    "assignment_id": live_id,
                    "queue_revision": ready["queue_revision"],
                    "model": s.member.default_model_binding_key,
                },
                receipt="begin-after-milestone",
            )
            assert started["assignment"]["task_version"] == started["task"]["version"] > after.version
            done = await call(*SUBMIT, wk, payload={**fence(started), **retained}, receipt="submit-after-milestone")
            assert done["run"]["id"] == started["run"]["id"] and done["run"]["status"] == "succeeded"
            return
        assert (await call(*WORK, wk))["state"] == "resume"
        renewed = await call(
            *RENEW,
            wk,
            payload={**fence(running), "expected_task_version": after.version},
            receipt="renew-notes",
        )
        assert renewed["run"]["id"] == run_id
        assert renewed["assignment"]["task_version"] == renewed["task"]["version"] == after.version + 1
        done = await call(*SUBMIT, wk, payload={**fence(renewed), **retained}, receipt="submit-notes")
        assert done["run"]["id"] == run_id and done["run"]["status"] == "succeeded"
        assert done["task"]["status"] == "resolved"


@databases
@pytest.mark.parametrize(
    "change",
    ["title", "description", "assignee", "depends_on", "tags", "priority", "max_end_date", "milestone_and_title"],
)
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_execution_input_change_still_stales_running_work(
    db_session, db_session_factory, task_factory, team_member_factory, monkeypatch, change
):
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    get_settings.cache_clear()
    s = await team_scope(db_session, task_factory, team_member_factory)
    task, wk, pk = s.task, s.wk, s.pk
    async with (
        recovery_api("rest", db_session_factory, monkeypatch) as call,
        httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://localhost:8001") as http,
    ):
        assigned = await call(
            *DISPATCH,
            pk,
            payload={
                "actor_id": s.worker.id,
                "task_id": task.id,
                "expected_task_version": task.version,
                "reviewer_profile_id": s.reviewer.profile_id,
            },
            receipt="assign-notes",
        )
        queue = await call(*WORK, wk)
        running = await call(
            *BEGIN,
            wk,
            payload={
                "assignment_id": assigned["id"],
                "queue_revision": queue["queue_revision"],
                "model": s.member.default_model_binding_key,
            },
            receipt="begin-notes",
        )
        before = await snapshot(db_session_factory, task.id, assigned["id"], running["run"]["id"])
        changes = {
            "title": {"title": "Write the revised operator notes"},
            "description": {"description": "Write the operator notes for the new installer as well."},
            "assignee": {"assignee_id": s.other_capacity},
            "depends_on": {"depends_on": [s.prerequisite.id]},
            "tags": {"tags": ["agent", "cap:backend-python", "operator-docs"]},
            "priority": {"priority": 3},
            "max_end_date": {"max_end_date": "2026-07-30"},
            "milestone_and_title": {"milestone_id": s.milestones[0], "title": "Write the revised operator notes"},
        }[change]
        await planning_patch(http, pk, task.id, before.version, "execution-change", **changes)
        after = await snapshot(db_session_factory, task.id, assigned["id"], running["run"]["id"])
        assert after.version == before.version + 1 and after.window is None and after.events == []
        (item,) = [item for item in (await call(*RECOVERY, pk))["items"] if item["task"]["id"] == task.id]
        assert "assignment_task_version_stale" in item["recovery_codes"], item
        await call(
            *RENEW,
            wk,
            payload={**fence(running), "expected_task_version": after.version},
            receipt="renew-stale",
            error="scope changed",
        )


@databases
@pytest.mark.parametrize("then", ["milestone", "depends_on"])
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_one_command_reseals_or_ends_the_fence(
    db_session, db_session_factory, task_factory, team_member_factory, monkeypatch, then
):
    """A bulk edit of a summary and its subtask reserves the subtask's version once."""
    from app.authority import Authority
    from app.commands import command_transaction
    from app.schemas.task import TaskUpdate
    from app.services.task_service import TaskService

    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    get_settings.cache_clear()
    s = await team_scope(db_session, task_factory, team_member_factory, summary=True)
    task, wk, pk = s.task, s.wk, s.pk
    async with recovery_api("rest", db_session_factory, monkeypatch) as call:
        assigned = await call(
            *DISPATCH,
            pk,
            payload={
                "actor_id": s.worker.id,
                "task_id": task.id,
                "expected_task_version": task.version,
                "reviewer_profile_id": s.reviewer.profile_id,
            },
            receipt="assign-notes",
        )
        queue = await call(*WORK, wk)
        running = await call(
            *BEGIN,
            wk,
            payload={
                "assignment_id": assigned["id"],
                "queue_revision": queue["queue_revision"],
                "model": s.member.default_model_binding_key,
            },
            receipt="begin-notes",
        )
        before = await snapshot(db_session_factory, task.id, assigned["id"], running["run"]["id"])
        second = (
            TaskUpdate(milestone_id=s.milestones[1]) if then == "milestone" else TaskUpdate(depends_on=[s.prerequisite.id])
        )
        async with db_session_factory() as session, command_transaction(session):
            session.info["authority"] = Authority(s.system, "system", workspace_role="operator")
            service = TaskService(session)
            await service.update(s.parent.id, TaskUpdate(milestone_id=s.milestones[0]), commit=False)
            await service.update(task.id, second, commit=False)
        after = await snapshot(db_session_factory, task.id, assigned["id"], running["run"]["id"])
        assert after.version == before.version + 1
        assert after.assignment == before.assignment and after.run == before.run and after.claim == before.claim
        if then == "milestone":
            assert after.milestone_id == s.milestones[1]
            assert (after.window["from"], after.window["through"]) == (before.version, after.version)
            assert after.window["evidence"] == {"fields": ["milestone_id"], "edited_task_id": task.id}
            assert [event["edited_task_id"] for event in after.events] == [s.parent.id, task.id]
            assert (await call(*WORK, wk))["state"] == "resume"
            return
        assert after.window is None
        await call(
            *RENEW,
            wk,
            payload={**fence(running), "expected_task_version": after.version},
            receipt="renew-stale",
            error="scope changed",
        )


def all_work_items(decision):
    return [item for item in [decision.get("next"), *decision.get("blocked_assigned", [])] if item]


async def dispatch_and_begin(call, s, *, begin=True):
    assigned = await call(
        *DISPATCH,
        s.pk,
        payload={
            "actor_id": s.worker.id,
            "task_id": s.task.id,
            "expected_task_version": s.task.version,
            "reviewer_profile_id": s.reviewer.profile_id,
        },
        receipt="assign-notes",
    )
    if not begin:
        return assigned, None
    queue = await call(*WORK, s.wk)
    running = await call(
        *BEGIN,
        s.wk,
        payload={
            "assignment_id": assigned["id"],
            "queue_revision": queue["queue_revision"],
            "model": s.member.default_model_binding_key,
        },
        receipt="begin-notes",
    )
    return assigned, running


@databases
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_milestone_change_without_original_receipt_still_stales(
    db_session, db_session_factory, task_factory, team_member_factory, monkeypatch
):
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    get_settings.cache_clear()
    s = await team_scope(db_session, task_factory, team_member_factory)
    # Queued work written without the PM's authenticated dispatch receipt.
    unproven = AgentTaskAssignment(
        task_id=s.task.id,
        actor_id=s.worker.id,
        assigned_by_actor_id=s.pm.id,
        team_member_id=s.task.assignee_id,
        reviewer_profile_id=s.reviewer.profile_id,
        task_version=s.task.version,
        state="queued",
        purpose="execution",
        queue_class="normal",
    )
    db_session.add(unproven)
    await db_session.commit()
    async with (
        recovery_api("rest", db_session_factory, monkeypatch) as call,
        httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://localhost:8001") as http,
    ):
        before = await snapshot(db_session_factory, s.task.id, unproven.id)
        await planning_patch(http, s.pk, s.task.id, before.version, "set-milestone", milestone_id=s.milestones[0])
        after = await snapshot(db_session_factory, s.task.id, unproven.id)
        assert after.version == before.version + 1 and after.window is None and after.events == []
        items = [item for item in all_work_items(await call(*WORK, s.wk)) if item["assignment"]["id"] == unproven.id]
        assert items and all("assignment_task_version_stale" in item["blocker_codes"] for item in items), items


@databases
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_batch_that_changes_a_fenced_task_prerequisite_ends_the_fence(
    db_session, db_session_factory, task_factory, team_member_factory, monkeypatch
):
    """Moving a running task off one milestone and new work into its prerequisite milestone in one batch."""
    from app.authority import Authority
    from app.commands import command_transaction
    from app.models.delivery_dependency import DeliveryDependency
    from app.routers.tasks import apply_batch_update_items
    from app.schemas.task import TaskBatchUpdateItem, TaskUpdate
    from app.services.delivery_dependency_service import DeliveryDependencyService
    from app.services.task_service import TaskService
    from app.utils.time import utc_now

    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    get_settings.cache_clear()
    s = await team_scope(db_session, task_factory, team_member_factory)
    milestone_id = s.milestones[0]
    # Seed the satisfied prerequisite directly, outside any request authority.
    async with db_session_factory() as seed:
        (await seed.get(ProjectMilestone, milestone_id)).status = "completed"
        owner = Principal(kind="human", display_name="Release owner")
        seed.add(owner)
        await seed.flush()
        delivered = Task(
            title="Publish the installer notes",
            project_id=s.task.project_id,
            iteration_id=s.task.iteration_id,
            milestone_id=milestone_id,
            status="closed",
            accepted_at=utc_now(),
            accepted_by_principal_id=owner.id,
        )
        seed.add(delivered)
        await seed.flush()
        delivered.accepted_version = delivered.version
        seed.add(DeliveryDependency(task_id=s.task.id, prerequisite_milestone_id=milestone_id))
        await seed.commit()
    async with recovery_api("rest", db_session_factory, monkeypatch) as call:
        assigned, running = await dispatch_and_begin(call, s)
        before = await snapshot(db_session_factory, s.task.id, assigned["id"], running["run"]["id"])
        async with db_session_factory() as session, command_transaction(session):
            session.info["authority"] = Authority(s.system, "system", workspace_role="operator")
            iteration = await session.get(Iteration, s.task.iteration_id)
            await apply_batch_update_items(
                TaskService(session),
                iteration.id,
                iteration.end_date,
                [
                    TaskBatchUpdateItem(task_id=s.task.id, update=TaskUpdate(milestone_id=s.milestones[1])),
                    TaskBatchUpdateItem(task_id=s.prerequisite.id, update=TaskUpdate(milestone_id=milestone_id)),
                ],
            )
            await DeliveryDependencyService(session).reconcile()
        after = await snapshot(db_session_factory, s.task.id, assigned["id"], running["run"]["id"])
        # The milestone edit alone would be fenced, but the prerequisite it
        # depends on changed in the same command, so the work is not kept.
        assert after.version == before.version + 1 and after.window is None
        assert (await call(*WORK, s.wk))["state"] != "resume"
        await call(
            *RENEW,
            s.wk,
            payload={**fence(running), "expected_task_version": after.version},
            receipt="renew-after-prerequisite-change",
            error="scope changed",
        )


@databases
@pytest.mark.parametrize("then", ["nothing", "delivery_edge"])
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_later_change_in_the_same_command_ends_the_fence(
    db_session, db_session_factory, task_factory, team_member_factory, monkeypatch, then
):
    """A change that does not go through a task update still ends a fence sealed earlier in the command."""
    from app.authority import Authority
    from app.commands import command_transaction
    from app.schemas.task import TaskUpdate
    from app.services.delivery_dependency_service import DeliveryDependencyService
    from app.services.task_service import TaskService

    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    get_settings.cache_clear()
    s = await team_scope(db_session, task_factory, team_member_factory)
    async with recovery_api("rest", db_session_factory, monkeypatch) as call:
        assigned, _ = await dispatch_and_begin(call, s, begin=False)
        before = await snapshot(db_session_factory, s.task.id, assigned["id"])
        async with db_session_factory() as session, command_transaction(session):
            session.info["authority"] = Authority(s.system, "system", workspace_role="operator")
            edited = await TaskService(session).update(
                s.task.id, TaskUpdate(milestone_id=s.milestones[0]), commit=False
            )
            assert current_window(edited)["kind"] == PLANNING_ONLY_EDIT
            if then == "delivery_edge":
                # Inside one command a caller supplies the version it observed before the command.
                await DeliveryDependencyService(session).add(s.task.id, "task", s.prerequisite.id, before.version)
        after = await snapshot(db_session_factory, s.task.id, assigned["id"])
        assert after.version == before.version + 1 and after.assignment == before.assignment
        if then == "nothing":
            assert after.window["kind"] == PLANNING_ONLY_EDIT
            return
        assert after.window is None
        items = [item for item in all_work_items(await call(*WORK, s.wk)) if item["assignment"]["id"] == assigned["id"]]
        assert items and all("assignment_task_version_stale" in item["blocker_codes"] for item in items), items


@databases
@pytest.mark.parametrize("order", ["upstream_first", "dependent_first"])
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_one_command_that_accepts_a_dependency_chain_keeps_acceptance(
    db_session, db_session_factory, task_factory, team_member_factory, monkeypatch, order
):
    """Closing a task and the task it waits for in one command keeps both acceptances."""
    from app.authority import Authority
    from app.commands import command_transaction
    from app.models.delivery_dependency import DeliveryDependency
    from app.models.task import TaskDependency
    from app.schemas.task_brief import TaskReviewWrite
    from app.services.task_brief_service import TaskBriefService

    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    get_settings.cache_clear()
    s = await team_scope(db_session, task_factory, team_member_factory)
    async with db_session_factory() as seed:
        dependent = await seed.get(Task, s.task.id)
        upstream = await seed.get(Task, s.prerequisite.id)
        unrelated = Task(
            title="Unrelated follow-up", project_id=dependent.project_id, iteration_id=dependent.iteration_id, status="planned"
        )
        seed.add(unrelated)
        await seed.flush()
        seed.add(TaskDependency(task_id=dependent.id, depends_on_id=upstream.id))
        # Any delivery prerequisite in the workspace makes the command reconcile delivery.
        seed.add(DeliveryDependency(task_id=unrelated.id, prerequisite_milestone_id=s.milestones[1]))
        (await seed.get(Project, dependent.project_id)).require_different_review_publisher = False
        dependent.status = upstream.status = "resolved"
        await seed.commit()
    ids = [s.prerequisite.id, s.task.id] if order == "upstream_first" else [s.task.id, s.prerequisite.id]
    async with db_session_factory() as session, command_transaction(session):
        session.info["authority"] = Authority(
            s.system, "system", workspace_role="operator", review_override=True, reason="Accept the reviewed notes"
        )
        service = TaskBriefService(session)
        for task_id in ids:
            task = await session.get(Task, task_id)
            await service.review(task_id, TaskReviewWrite(
                expected_version=task.version, brief_revision=task.brief_revision,
                artifact_revision=task.artifact_revision, verdict="accept", reason="Checked the dependency",
            ))
    async with db_session_factory() as read:
        for task_id in ids:
            task = await read.get(Task, task_id)
            assert task.status == "closed" and task.accepted_at is not None, task_id
            assert task.accepted_version == task.version, task_id
