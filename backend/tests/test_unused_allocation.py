"""Capacity-row removal reserves planning while preserving unrelated issued work."""

import json
import asyncio
import hashlib
import time
from datetime import date, timedelta

import httpx
import pytest
from sqlalchemy import select, text

from app import database
from app.config import get_settings
from app.commands import AggregateVersionConflict, PlanningConflict, command_transaction
from app.commands import current_command, lock_iterations, lock_planning
from app.services.agent_planning_service import AgentPlanningService
from app.main import app
from app.models.agent import AgentActor, AgentRun, AgentTaskAssignment
from app.models.capacity import PlanningState
from app.models.iteration import Iteration
from app.models.identity import ProjectMembership, WorkspaceMembership
from app.models.project import Initiative, Project
from app.models.recovery import ApplicationSnapshot, TaskScheduleBaseline
from app.models.task import Task
from app.models.team_member import TeamMember, Vacation
from app.models.triage import TriageClassificationSuggestion, TriageItem
from app.services.agent_service import hash_api_key
from app.schemas.agent import AgentTaskAssignmentCreate
from app.services.agent_work_service import AgentWorkService
from app.services.team_service import TeamService
from app.authority import Authority
from app.services.identity_service import IdentityService, initialize_control_plane
from app.services.snapshot_service import SnapshotService
from app.services import allocation_removal
from app.utils.time import utc_now
from tests.test_annual_calendar_work_control import apply_inputs, pm_headers
from tests.test_review_provenance import database_engines
from tests.test_team_pm_dispatch import db_session_factory as db_session_factory
from tests.test_agent_team_setup_qualification import provision_ready_topology, routing_base


@database_engines
@pytest.mark.usefixtures("qualified_model_aware_routing_test_context")
async def test_saved_allocation_uses_typed_decision_and_both_native_lineage_writers(
    db_session, db_session_factory, profile_factory, actor_factory, team_member_factory, task_factory
):
    from app.schemas.agent import ModelAwareAgentTaskAssignmentCreate
    from app.schemas.agent_routing import AgentRoutingPreviewCreate
    from app.services.agent_routing_service import AgentRoutingService
    from tests.test_agent_routing_service import _assessment_command, _command_context, _routing_fixture

    pm, worker, task, binding, _ = await _routing_fixture(
        db_session, profile_factory, actor_factory, team_member_factory, task_factory
    )
    routing = AgentRoutingService(db_session)
    receipt = await routing.create_assessment(
        task.id, pm, _assessment_command(task_version=task.version), _command_context("record-selection")
    )
    data = AgentRoutingPreviewCreate(
        purpose="execution", assessment_id=receipt.assessment.id, expected_task_version=task.version
    )
    preview = await routing.preview_task_routing(task.id, pm, data)
    command = ModelAwareAgentTaskAssignmentCreate(
        task_id=task.id,
        actor_id=worker.id,
        purpose="execution",
        expected_task_version=task.version,
        assessment_id=receipt.assessment.id,
        model_binding_id=binding.id,
        model_binding_revision=binding.revision,
        routing_preview_id=preview.preview_id,
        routing_preview_digest=preview.preview_digest,
    )
    assigned = await AgentWorkService(db_session).create_assignment(
        pm,
        command,
        idempotency_key="record-owner",
        correlation_id="record-owner",
        rationale="Record the package capacity owner.",
    )
    owner = task.assignee_id
    stored = await db_session.get(AgentTaskAssignment, assigned.id)
    assert owner and allocation_removal._routing_ids(stored.routing_snapshot) == {owner}
    pending = AgentWorkService._routing_lineage_snapshot(
        task=task,
        source_assignments=[stored],
        transition="recovery",
        provisional_actor_id=worker.id,
        reason="Resume package work",
    )
    pending["supervised_actor_id"] = worker.id
    assert allocation_removal._routing_ids(json.dumps(pending)) == {owner}
    # The later selection stores a compact, completed projection of this same prior decision.
    pending_assignment = AgentTaskAssignment(
        id=assigned.id,
        task_id=task.id,
        task_version=task.version,
        actor_id=worker.id,
        queue_class="recovery",
        routing_snapshot=json.dumps(pending),
    )
    completed = routing._completed_prior_lineage(
        pending_assignment, selected_reasoning_tier=1, selected_context_tier="small"
    )
    selected = json.loads(stored.routing_snapshot)
    selected["prior_lineage"] = completed
    assert allocation_removal._routing_ids(json.dumps(selected)) == {owner}
    pending["prior_decisions"][0]["member_id"] = owner
    assert allocation_removal._routing_ids(json.dumps(pending)) is None


@database_engines
async def test_fresh_forecasts_apply_before_and_after_allocation_removal(
    db_session,
    db_session_factory,
    task_factory,
    profile_factory,
    team_member_factory,
    actor_factory,
    monkeypatch,
):
    db = db_session
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("WORKCHORD_ADMIN_API_KEY", "forecast-operator-test")
    monkeypatch.setattr(database, "async_session_maker", db_session_factory)
    get_settings.cache_clear()
    await initialize_control_plane(db)
    project = Project(name="Release calendar")
    db.add(project)
    await db.flush()
    task = await task_factory(project_id=project.id, status="planned", effort_days=1, effort_hours=8)
    it = await db.get(Iteration, task.iteration_id)
    it.project_id = project.id
    staff = await team_member_factory(
        iteration=it, profile=await profile_factory(), operational_utilization=0
    )
    empty = await team_member_factory(
        iteration=it, profile=await profile_factory(), operational_utilization=0
    )
    task.assignee_id = staff.id
    pm = await actor_factory(
        role="pm",
        scopes=json.dumps(["planning:read", "planning:write"]),
        api_key_hash=hash_api_key("forecast-manager"),
    )
    identity = await IdentityService(db).actor_context(pm)
    db.add_all(
        [
            WorkspaceMembership(principal_id=identity.principal_id, role="member"),
            ProjectMembership(project_id=project.id, principal_id=identity.principal_id, role="manager"),
        ]
    )
    await db.commit()
    iid, mid = it.id, empty.id
    async with db_session_factory() as inspect_db, command_transaction(inspect_db, mode="preview"):
        planning = AgentPlanningService(inspect_db)
        original = await planning._schedule_input_digest(iid)
        await lock_iterations(inspect_db, [iid])
        assert original == await planning._schedule_input_digest(iid)
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        path = f"/api/agent/planning/iterations/{iid}/schedule"

        async def preview_apply(label):
            preview = await client.post(
                path + "/preview", headers=pm_headers("forecast-manager", "preview-" + label)
            )
            assert preview.status_code == 200 and preview.json()["result"]["success"], preview.text
            result = await client.post(
                path + "/apply",
                json=apply_inputs(preview.json()["result"]),
                headers=pm_headers("forecast-manager", "apply-" + label),
            )
            assert result.status_code == 200 and result.json()["result"]["success"], result.text

        await preview_apply("ordinary")
        headers = {"X-Admin-API-Key": "forecast-operator-test"}
        context = await client.get(f"/api/tasks/planning-inputs/member/{mid}/context", headers=headers)
        assert context.status_code == 200, context.text
        removed = await client.delete(
            f"/api/team-members/{mid}",
            params={"unused_only": "true"},
            headers={**headers, "X-Expected-Revisions": json.dumps(context.json()["expected_revisions"])},
        )
        assert removed.status_code == 200, removed.text
        await preview_apply("after-removal")


@database_engines
async def test_large_retained_history_is_checked_before_reserving_the_planning_writer(
    db_session,
    db_session_factory,
    task_factory,
    profile_factory,
    team_member_factory,
    actor_factory,
    monkeypatch,
    record_property,
):
    db = db_session
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("WORKCHORD_ADMIN_API_KEY", "history-operator-test")
    monkeypatch.setattr(database, "async_session_maker", db_session_factory)
    get_settings.cache_clear()
    await initialize_control_plane(db)
    target_task, other_task = await task_factory(), await task_factory()
    it = await db.get(Iteration, target_task.iteration_id)
    mid = (await team_member_factory(iteration=it, profile=await profile_factory())).id
    payload = {
        "tasks": [
            {
                "assignee_id": None,
                "children": [
                    {
                        "assignee_id": mid + 100,
                        "description": "Package documentation. " * 48,
                        "children": [],
                    }
                    for _ in range(199)
                ],
            }
        ]
    }
    encoded = SnapshotService._encode(payload)
    actor = await actor_factory(profile=await profile_factory())
    lineage = AgentWorkService._routing_lineage_snapshot(
        task=other_task,
        source_assignments=[],
        transition="recovery",
        provisional_actor_id=actor.id,
        reason="Recover the prior package assignment.",
    )
    lineage["supervised_actor_id"] = actor.id
    saved = AgentWorkService._serialize_routing_snapshot(lineage)
    assert allocation_removal._routing_ids(saved) == frozenset()
    runner = json.dumps(
        {
            "schema_version": "workchord-runner-supervised-dispatch-v1",
            "assessment_id": other_task.id,
            "model_catalog_key": "package-runtime",
        }
    )
    assert allocation_removal._routing_ids(runner) == frozenset()
    extra = json.loads(runner)
    extra["member_id"] = mid
    assert allocation_removal._routing_ids(json.dumps(extra)) is None
    db.add_all(
        [
            AgentTaskAssignment(
                task_id=other_task.id,
                actor_id=actor.id,
                state="fulfilled",
                task_version=other_task.version,
                routing_snapshot=saved if i % 2 else runner,
            )
            for i in range(500)
        ]
    )
    db.add_all(
        [
            ApplicationSnapshot(
                iteration_id=other_task.iteration_id,
                filename=f"capacity-{i}.json",
                input_revision=1,
                payload=payload,
                checksum=hashlib.sha256(encoded).hexdigest(),
            )
            for i in range(200)
        ]
    )
    await db.commit()
    measured = []
    locked = []
    classify = allocation_removal.is_unused_allocation

    async def timed_lock(session, member_id, history, *, unused_only):
        assert current_command(session).planning_revision is not None
        at = time.monotonic()
        result = await classify(session, member_id, history, unused_only=unused_only)
        locked.append(time.monotonic() - at)
        return result

    monkeypatch.setattr(allocation_removal, "is_unused_allocation", timed_lock)
    observe = allocation_removal._historical_task_reference

    async def instrument(session, member_id):
        assert current_command(session).planning_revision is None
        start = time.monotonic()
        actual = await observe(session, member_id)
        measured.append(time.monotonic() - start)
        if session.get_bind().dialect.name == "postgresql":
            # This concurrent writer really acquires the planning lock before
            # the historical reader finishes, and then rolls back its reservation.
            async with db_session_factory() as writer, command_transaction(writer, mode="preview"):
                await asyncio.wait_for(lock_planning(writer), 3)
        return actual

    monkeypatch.setattr(allocation_removal, "_historical_task_reference", instrument)
    headers = {
        "X-Admin-API-Key": "history-operator-test",
        "X-Expected-Revisions": json.dumps({it.id: it.revision}),
    }
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        started = time.monotonic()
        response = await client.delete(
            f"/api/team-members/{mid}", headers=headers, params={"unused_only": "true"}
        )
        assert response.status_code == 200, response.text
    assert len(measured) == 1
    record_property("historical_task_nodes", 40000)
    record_property("retained_routing_decisions", 500)
    record_property("historical_json_bytes", 200 * len(encoded))
    record_property("history_read_ms", round(1000 * measured[0]))
    record_property("locked_reference_check_ms", round(1000 * locked[0]))
    record_property("request_ms", round(1000 * (time.monotonic() - started)))


@pytest.fixture(autouse=True)
def restore_settings_cache():
    yield
    get_settings.cache_clear()


@database_engines
async def test_changed_history_epoch_requires_a_fresh_allocation_observation(
    db_session,
    db_session_factory,
    task_factory,
    team_member_factory,
    profile_factory,
    monkeypatch,
):
    db = db_session
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("WORKCHORD_ADMIN_API_KEY", "history-operator-test")
    monkeypatch.setattr(database, "async_session_maker", db_session_factory)
    get_settings.cache_clear()
    await initialize_control_plane(db)
    target, other = await task_factory(), await task_factory()
    iteration = await db.get(Iteration, target.iteration_id)
    member = await team_member_factory(iteration=iteration, profile=await profile_factory())
    await db.commit()
    original = allocation_removal.inspect_allocation_history

    async def interleave(session, mid):
        observation = await original(session, mid)
        assert observation.unused and current_command(session).planning_revision is None
        async with db_session_factory() as writer:
            await SnapshotService(writer).create_snapshot(other.iteration_id, "concurrent_history")
        return observation

    headers = {
        "X-Admin-API-Key": "history-operator-test",
        "X-Expected-Revisions": json.dumps({iteration.id: iteration.revision}),
    }
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        with monkeypatch.context() as different:
            different.setattr(allocation_removal, "inspect_allocation_history", interleave)
            stale = await client.delete(
                f"/api/team-members/{member.id}", params={"unused_only": "true"}, headers=headers
            )
            assert (
                stale.status_code == 409 and stale.json()["detail"]["code"] == "planning_scope_changed"
            ), stale.text
        async with db_session_factory() as fresh:
            assert await fresh.get(TeamMember, member.id) is not None
            assert (await fresh.get(Iteration, iteration.id)).revision == iteration.revision
            assert (await fresh.get(Task, target.id)).version == target.version
        ok = await client.delete(
            f"/api/team-members/{member.id}", params={"unused_only": "true"}, headers=headers
        )
        assert ok.status_code == 200, ok.text


@database_engines
@pytest.mark.parametrize("condition", ["ordinary", "unused"])
async def test_empty_allocation_preserves_issued_work(
    db_session,
    db_session_factory,
    task_factory,
    profile_factory,
    team_member_factory,
    actor_factory,
    monkeypatch,
    condition,
):
    db = db_session
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("WORKCHORD_ADMIN_API_KEY", "capacity-operator-test")
    monkeypatch.setattr(database, "async_session_maker", db_session_factory)
    get_settings.cache_clear()
    await initialize_control_plane(db)
    profile = await profile_factory()
    staff = await actor_factory(profile=await profile_factory())
    projects = [Project(name="Package"), Project(name="Library")]
    db.add_all(projects)
    await db.flush()
    tasks = [await task_factory(project_id=projects[i % 2].id) for i in range(3)]
    iterations = [await db.get(Iteration, t.iteration_id) for t in tasks]
    for t, it in zip(tasks, iterations):
        it.project_id = t.project_id
    members = [await team_member_factory(profile=profile, iteration=it) for it in iterations]
    tasks[0].assignee_id = members[0].id
    tasks[1].status = "active"
    db.add_all(
        [
            AgentTaskAssignment(
                task_id=tasks[i].id, actor_id=staff.id, state=state, task_version=tasks[i].version
            )
            for i, state in ((1, "accepted"), (2, "queued"))
        ]
    )
    baseline = TaskScheduleBaseline(
        task_id=tasks[0].id, revision=1, timezone="UTC", reason="Agreed delivery"
    )
    db.add(baseline)
    await db.commit()
    task_ids = [t.id for t in tasks]
    observed = {t.id: t.version for t in tasks}
    revisions = {it.id: it.revision for it in iterations}
    allocations = {m.id: m.allocation_token for m in members}
    target = members[-1].id
    headers = {"X-Admin-API-Key": "capacity-operator-test"}
    pm = await actor_factory(
        role="pm",
        scopes=json.dumps(["planning:read", "planning:write"]),
        api_key_hash=hash_api_key("capacity-planning-test"),
    )
    identity = await IdentityService(db).actor_context(pm)
    db.add(WorkspaceMembership(principal_id=identity.principal_id, role="member"))
    db.add_all(
        [
            ProjectMembership(project_id=p.id, principal_id=identity.principal_id, role="manager")
            for p in projects
        ]
    )
    editor = await actor_factory(
        role="pm",
        scopes=json.dumps(["team:write", "planning:write", "planning:read"]),
        api_key_hash=hash_api_key("local-project-editor"),
    )
    limited = await IdentityService(db).actor_context(editor)
    db.add_all(
        [
            WorkspaceMembership(principal_id=limited.principal_id, role="member"),
            ProjectMembership(
                project_id=projects[0].id, principal_id=limited.principal_id, role="manager"
            ),
        ]
    )
    await db.commit()
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        held = {}
        for iteration in iterations:
            path = f"/api/agent/planning/iterations/{iteration.id}/schedule"
            prior = await client.post(
                path + "/preview", headers=pm_headers("capacity-planning-test", f"before-{iteration.id}")
            )
            assert prior.status_code == 200, prior.text
            held[path] = prior.json()["result"]
        response = await client.get(
            f"/api/tasks/planning-inputs/member/{target}/context", headers=headers
        )
        assert response.status_code == 200, response.text
        context = response.json()
        assert context["complete"] and context["expected_revisions"] == {
            str(k): v for k, v in revisions.items()
        }
        precondition = {"unused_only": "true"} if condition == "unused" else {}
        protected = await client.delete(
            f"/api/team-members/{target}",
            params=precondition,
            headers={
                "X-Agent-API-Key": "local-project-editor",
                "X-Expected-Revisions": json.dumps(context["expected_revisions"]),
            },
        )
        assert protected.status_code == 403, protected.text
        stale_context = {
            **context["expected_revisions"],
            str(iterations[0].id): revisions[iterations[0].id] + 1,
        }
        stale_row = await client.delete(
            f"/api/team-members/{target}",
            params=precondition,
            headers={**headers, "X-Expected-Revisions": json.dumps(stale_context)},
        )
        assert stale_row.status_code == 409 and "iteration_version_conflict" in stale_row.text
        async with db_session_factory() as read:
            global_before = await read.scalar(select(PlanningState.revision))
        response = await client.delete(
            f"/api/team-members/{target}",
            params={"unused_only": "true"} if condition == "unused" else {},
            headers={**headers, "X-Expected-Revisions": json.dumps(context["expected_revisions"])},
        )
        assert response.status_code == 200, response.text
        async with db_session_factory() as read:
            assert await read.scalar(select(PlanningState.revision)) == (global_before or 0) + 1
        for index, (path, forecast) in enumerate(held.items()):
            stale = await client.post(
                path + "/apply",
                json=apply_inputs(forecast),
                headers=pm_headers("capacity-planning-test", f"held-{index}"),
            )
            assert stale.status_code == 409 and "Schedule inputs changed" in stale.text, stale.text
            latest = await client.post(
                path + "/preview", headers=pm_headers("capacity-planning-test", f"after-{index}")
            )
            assert (
                latest.status_code == 200
                and latest.json()["result"]["input_digest"] != forecast["input_digest"]
            )
    async with db_session_factory() as current:
        actual = dict(
            (await current.execute(select(Task.id, Task.version).where(Task.id.in_(task_ids)))).all()
        )
        assert actual == observed
        assert dict((await current.execute(select(Iteration.id, Iteration.revision))).all()) == {
            k: v + 1 for k, v in revisions.items()
        }
        assert dict(
            (await current.execute(select(TeamMember.id, TeamMember.allocation_token))).all()
        ) == {k: v for k, v in allocations.items() if k != target}
        rows = (await current.scalars(select(AgentTaskAssignment).order_by(AgentTaskAssignment.id))).all()
        assert [(r.state, r.task_version == actual[r.task_id]) for r in rows] == [
            ("accepted", True),
            ("queued", True),
        ]
        assert (await current.get(TaskScheduleBaseline, baseline.id)).reason == "Agreed delivery"
        assert set(await current.scalars(select(ApplicationSnapshot.iteration_id))) == set(revisions)


@database_engines
@pytest.mark.parametrize(
    "reference",
    [
        "closed-task",
        "project",
        "initiative",
        "vacation",
        "suggestion",
        "finished-assignment",
        "captured-route",
        "issued-profile",
        "review-floor",
        "retained-reviewer",
        "running-profile",
        "saved-child",
        "legacy-owner",
        "unassigned-profile-owner",
        "live-accepted-profile",
        "route-malformed",
        "route-nonobject",
        "route-unknown-version",
        "route-nested-other-key",
        "route-float",
        "opaque-legacy-removal",
        "unknown-foreign-key",
        "mixed-case-foreign-key",
        "unknown-backend",
        "history-missing-owner",
        "history-null-children",
        "history-object-children",
        "history-unrelated",
        "history-root-string",
        "history-root-array",
        "history-child-string",
        "history-child-array",
    ],
)
async def test_allocation_guard_preserves_references(
    db_session,
    db_session_factory,
    task_factory,
    team_member_factory,
    actor_factory,
    profile_factory,
    monkeypatch,
    reference,
):
    db = db_session
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("WORKCHORD_ADMIN_API_KEY", "capacity-operator-test")
    monkeypatch.setattr(database, "async_session_maker", db_session_factory)
    get_settings.cache_clear()
    await initialize_control_plane(db)
    root = await task_factory()
    iteration = await db.get(Iteration, root.iteration_id)
    profile = await profile_factory()
    member = await team_member_factory(profile=profile, iteration=iteration)
    project = Project(name="Reference owner")
    db.add(project)
    await db.flush()
    root.project_id = iteration.project_id = project.id
    if reference == "closed-task":
        root.assignee_id, root.status = member.id, "closed"
    elif reference in {"project", "legacy-owner"}:
        project.owner_id = member.id
    elif reference == "initiative":
        db.add(Initiative(name="Capacity request", owner_id=member.id))
    elif reference == "unassigned-profile-owner":
        root.owner_profile_id = member.profile_id
    elif reference == "mixed-case-foreign-key":
        await db.execute(
            text(
                "CREATE TABLE Extra_Allocation_Link (ID INTEGER PRIMARY KEY, Member_ID INTEGER REFERENCES Team_Members(ID))"
            )
        )
    elif reference == "unknown-foreign-key":
        await db.execute(
            text(
                "CREATE TABLE supplementary_allocation_reference (id INTEGER PRIMARY KEY, allocation_id INTEGER REFERENCES team_members(id))"
            )
        )
    elif reference == "unknown-backend":
        original = allocation_removal._history_statement
        monkeypatch.setattr(
            allocation_removal, "_history_statement", lambda _dialect: original("unclassified")
        )
    elif reference.startswith("history-"):
        values = {
            "history-missing-owner": {"children": []},
            "history-null-children": {"assignee_id": None, "children": None},
            "history-object-children": {
                "assignee_id": None,
                "children": {"item": {"assignee_id": member.id}},
            },
            "history-unrelated": {
                "assignee_id": None,
                "children": [{"assignee_id": member.id + 100, "children": []}],
            },
        }
        values.update(
            {
                "history-root-string": "title",
                "history-root-array": ["title"],
                "history-child-string": {"assignee_id": None, "children": ["title"]},
                "history-child-array": {"assignee_id": None, "children": [["title"]]},
            }
        )
        payload = {"tasks": [values[reference]], "team_members": [{"id": member.id}]}
        db.add(
            ApplicationSnapshot(
                iteration_id=iteration.id,
                filename="retained.json",
                input_revision=iteration.revision,
                payload=payload,
                checksum=hashlib.sha256(SnapshotService._encode(payload)).hexdigest(),
                schema_version=2,
            )
        )
    elif reference.startswith("route-") or reference == "opaque-legacy-removal":
        layouts = {
            "route-malformed": "{",
            "route-nonobject": "[1]",
            "route-unknown-version": json.dumps(
                {"schema_version": "future", "member_id": member.id + 20}
            ),
            "route-nested-other-key": json.dumps({"selected": {"assignee_id": member.id}}),
            "route-float": json.dumps(
                {"schema_version": "routing-decision-snapshot-v1", "capacity_owner_id": float(member.id)}
            ),
            "opaque-legacy-removal": json.dumps(
                {"schema_version": "unclassified", "selected": {"owner": member.id}}
            ),
        }
        actor = await actor_factory(profile=await profile_factory())
        db.add(
            AgentTaskAssignment(
                task_id=root.id,
                actor_id=actor.id,
                state="fulfilled",
                task_version=root.version,
                routing_snapshot=layouts[reference],
            )
        )
    elif reference == "live-accepted-profile":
        actor = await actor_factory(profile=profile)
        db.add(
            AgentTaskAssignment(
                task_id=root.id, actor_id=actor.id, state="accepted", task_version=root.version
            )
        )
    elif reference == "vacation":
        db.add(Vacation(team_member_id=member.id, start_date=date(2026, 7, 2), end_date=date(2026, 7, 3)))
    elif reference == "suggestion":
        item = TriageItem(title="Package request")
        db.add(item)
        await db.flush()
        db.add(TriageClassificationSuggestion(triage_item_id=item.id, suggested_assignee_id=member.id))
    elif reference == "saved-child":
        child = await task_factory(
            iteration=iteration, assignee=member, parent_id=root.id, project_id=project.id
        )
        await db.commit()
        await SnapshotService(db).create_snapshot(iteration.id, "prior_allocation")
        child.assignee_id = None
    elif reference == "running-profile":
        actor = await actor_factory(profile=await profile_factory())
        db.add(
            AgentRun(
                task_id=root.id,
                actor_id=actor.id,
                status="running",
                execution_provenance={"profile_id": profile.id},
            )
        )
    else:
        actor = await actor_factory(
            profile=profile if reference == "issued-profile" else await profile_factory()
        )
        db.add(
            AgentTaskAssignment(
                task_id=root.id,
                actor_id=actor.id,
                team_member_id=member.id if reference == "finished-assignment" else None,
                reviewer_profile_id=profile.id if reference == "review-floor" else None,
                review_selection={"reviewer": {"profile_id": profile.id}}
                if reference == "retained-reviewer"
                else None,
                task_version=root.version,
                state="queued"
                if reference in {"issued-profile", "review-floor", "retained-reviewer"}
                else "fulfilled",
                routing_snapshot=json.dumps({"capacity_owner_id": member.id})
                if reference == "captured-route"
                else "{}",
            )
        )
    await db.commit()
    mid, tid, iid, pid = member.id, root.id, iteration.id, project.id
    if reference in {
        "history-root-array",
        "history-root-string",
        "history-child-array",
        "history-child-string",
    }:
        # Observe the actual parser's node type as well as the final refusal.
        # A database's object-key operator alone cannot classify arrays or scalars.
        dialect = db.get_bind().dialect.name
        cte = str(allocation_removal._history_statement(dialect)).rsplit("SELECT EXISTS", 1)[0]
        kind = "jsonb_typeof" if dialect == "postgresql" else "json_type"
        assert set(await db.scalars(text(cte + f"SELECT {kind}(node) FROM saved"))) == {"object"}
    revision = (await db.get(Iteration, iid, populate_existing=True)).revision
    old_version = root.version
    headers = {
        "X-Admin-API-Key": "capacity-operator-test",
        "X-Expected-Revisions": json.dumps({iid: revision}),
    }
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=app), base_url="http://test"
    ) as client:
        if reference in {"legacy-owner", "opaque-legacy-removal"}:
            response = await client.delete(f"/api/team-members/{mid}", headers=headers)
            assert response.status_code == 200, response.text
        elif reference == "history-unrelated":
            response = await client.delete(
                f"/api/team-members/{mid}", params={"unused_only": "true"}, headers=headers
            )
            assert response.status_code == 200, response.text
        else:
            response = await client.delete(
                f"/api/team-members/{mid}", params={"unused_only": "true"}, headers=headers
            )
            assert (
                response.status_code == 409
                and response.json()["detail"]["code"] == "allocation_not_unused"
            ), response.text
    async with db_session_factory() as fresh:
        if reference == "history-unrelated":
            assert await fresh.get(TeamMember, mid) is None
            assert (await fresh.get(Task, tid)).version == old_version
            assert (await fresh.get(Iteration, iid)).revision == revision + 1
        elif reference in {"legacy-owner", "opaque-legacy-removal"}:
            assert (
                await fresh.get(TeamMember, mid) is None
                and (await fresh.get(Project, pid)).owner_id is None
            )
            assert (await fresh.get(Task, tid)).version == old_version + 1 and (
                await fresh.get(Iteration, iid)
            ).revision == revision + 1
        else:
            assert (await fresh.get(TeamMember, mid)).allocation_token == member.allocation_token
            assert (await fresh.get(Iteration, iid)).revision == revision and (
                await fresh.get(Task, tid)
            ).version == old_version


@pytest.mark.parametrize(
    "db_session_factory",
    [pytest.param("postgresql", marks=[pytest.mark.postgresql, pytest.mark.allow_network])],
    indirect=True,
)
@pytest.mark.parametrize("first", ["remove", "issue"])
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_postgres_allocation_removal_serializes_with_dispatch(
    db_session,
    db_session_factory,
    team_member_factory,
    task_factory,
    monkeypatch,
    first,
    record_property,
):
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    get_settings.cache_clear()
    system = await initialize_control_plane(db_session)
    await db_session.commit()
    team = await provision_ready_topology(db_session)
    member, controller = team.manifest.workers[0], team.manifest.controller
    worker, pm = (team.actors[row.actor_key] for row in (member, controller))
    scope = await routing_base(
        db_session,
        topology=team,
        actor_key=member.actor_key,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        title="Prepare package delivery",
    )
    project = Project(name="Package delivery")
    db_session.add(project)
    await db_session.flush()
    it = await db_session.get(Iteration, scope.task.iteration_id)
    it.project_id = scope.task.project_id = project.id
    scope.task.assignee_id = None
    for actor, role in [(pm, "manager"), (worker, "executor")]:
        person = await IdentityService(db_session).actor_context(actor)
        db_session.add_all(
            [
                WorkspaceMembership(principal_id=person.principal_id, role="member"),
                ProjectMembership(principal_id=person.principal_id, project_id=project.id, role=role),
            ]
        )
    await db_session.commit()
    iid, mid, tid, version = it.id, scope.member.id, scope.task.id, scope.task.version
    worker_id, pm_id = worker.id, pm.id
    seen = it.revision
    ready, release = asyncio.Event(), asyncio.Event()
    waiter_pid = asyncio.get_running_loop().create_future()

    async def write(kind, *, retry=False):
        async with db_session_factory() as session, command_transaction(session, commit=True):
            pid = await session.scalar(text("SELECT pg_backend_pid()"))
            if kind != first and not retry:
                waiter_pid.set_result(pid)
            if kind == "remove":
                session.info["authority"] = Authority(system, "system", workspace_role="operator")
                revision = (await session.get(Iteration, iid)).revision if retry else seen
                session.info["request_expected_revisions"] = {iid: revision}
                result = await TeamService(session).delete(mid, unused_only=True)
            else:
                principal = await session.get(AgentActor, pm_id)
                session.info["authority"] = await IdentityService(session).actor_context(
                    principal, source="agent_rest"
                )
                result = await AgentWorkService(session).create_assignment(
                    principal,
                    AgentTaskAssignmentCreate(
                        task_id=tid, actor_id=worker_id, team_member_id=mid, expected_task_version=version
                    ),
                    idempotency_key="dispatch-package",
                    correlation_id="dispatch-package",
                    rationale="Queue the package work",
                )
            if kind == first and not retry:
                ready.set()
                await asyncio.wait_for(release.wait(), 12)
            return result

    second = "issue" if first == "remove" else "remove"
    started = asyncio.create_task(write(first))
    try:
        await asyncio.wait_for(ready.wait(), 12)
        waiting = asyncio.create_task(write(second))
        pid = await asyncio.wait_for(waiter_pid, 8)
        async with db_session_factory() as monitor:
            for _ in range(150):
                blocked = await monitor.scalar(
                    text("SELECT cardinality(pg_blocking_pids(:pid))"), {"pid": pid}
                )
                if blocked:
                    break
                await asyncio.sleep(0.02)
            assert blocked, "The two real operations must overlap at their shared planning fence."
            record_property("postgres_blocked_second_writer", second)
    finally:
        release.set()
        result = await asyncio.gather(
            started, *([waiting] if "waiting" in locals() else []), return_exceptions=True
        )
    assert len(result) == 2 and not isinstance(result[0], BaseException), result
    if first == "issue":
        assert isinstance(result[1], AggregateVersionConflict), result
        with pytest.raises(PlanningConflict) as fresh_conflict:
            await write("remove", retry=True)
        assert fresh_conflict.value.code == "allocation_not_unused"
    else:
        assert isinstance(result[1], ValueError) and "team member" in str(result[1]).lower(), result
    async with db_session_factory() as fresh:
        assignment = await fresh.scalar(
            select(AgentTaskAssignment).where(AgentTaskAssignment.task_id == tid)
        )
        assert (await fresh.get(Task, tid)).version == version
        assert (await fresh.get(TeamMember, mid) is not None) == (first == "issue")
        if first == "issue":
            assert assignment and assignment.team_member_id == mid and assignment.task_version == version
        else:
            assert assignment is None


@pytest.mark.parametrize(
    "db_session_factory",
    [pytest.param("postgresql", marks=[pytest.mark.postgresql, pytest.mark.allow_network])],
    indirect=True,
)
@pytest.mark.parametrize(
    "reference,guarded", [("current", False), ("retained", False), ("current", True), ("unproven", False)]
)
async def test_allocation_removal_queued_behind_unrelated_planning_writer(
    db_session,
    db_session_factory,
    task_factory,
    team_member_factory,
    profile_factory,
    monkeypatch,
    reference,
    guarded,
    record_property,
):
    monitor = db_session
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    get_settings.cache_clear()
    system = await initialize_control_plane(monitor)
    target_task, other_task = await task_factory(), await task_factory()
    iteration = await monitor.get(Iteration, target_task.iteration_id)
    member = await team_member_factory(iteration=iteration, profile=await profile_factory())
    project = Project(name="Package ownership", owner_id=member.id if reference == "current" else None)
    monitor.add(project)
    await monitor.flush()
    iteration.project_id = target_task.project_id = project.id
    if reference == "retained":
        payload = {"tasks": [{"assignee_id": member.id, "children": []}]}
        monitor.add(
            ApplicationSnapshot(
                iteration_id=iteration.id,
                filename="retained-ownership.json",
                input_revision=iteration.revision,
                schema_version=2,
                payload=payload,
                checksum=hashlib.sha256(SnapshotService._encode(payload)).hexdigest(),
            )
        )
    await monitor.commit()
    iid, other, tid, mid, revision, version = (
        iteration.id,
        other_task.iteration_id,
        target_task.id,
        member.id,
        iteration.revision,
        target_task.version,
    )
    pid = asyncio.get_running_loop().create_future()

    async def remove_member():
        async with db_session_factory() as session, command_transaction(session, commit=True):
            session.info["authority"] = Authority(system, "system", workspace_role="operator")
            session.info["request_expected_revisions"] = {iid: revision}
            pid.set_result(await session.scalar(text("SELECT pg_backend_pid()")))
            return await TeamService(session).delete(mid, unused_only=guarded)

    # The other iteration's genuine capture retains the shared planning lock
    # until its transaction commits. The member command uses its original revision.
    async with db_session_factory() as writer, command_transaction(writer, commit=True):
        writer.info["authority"] = Authority(system, "system", workspace_role="operator")
        await SnapshotService(writer).create_snapshot(other, "concurrent_capacity_plan")
        waiting = asyncio.create_task(remove_member())
        waiter = await asyncio.wait_for(pid, 8)
        for _ in range(180):
            blocked = await monitor.scalar(
                text("SELECT cardinality(pg_blocking_pids(:pid))"), {"pid": waiter}
            )
            if blocked:
                break
            await asyncio.sleep(0.02)
        assert blocked, "The ordinary removal must actually wait for the unrelated planning writer."
    record_property("unrelated_planning_writer_blocked_removal", True)
    if guarded:
        with pytest.raises(PlanningConflict) as refused:
            await asyncio.wait_for(waiting, 10)
        assert refused.value.code == "allocation_not_unused"
    else:
        assert await asyncio.wait_for(waiting, 10)
    async with db_session_factory() as fresh:
        assert ((await fresh.get(TeamMember, mid)) is not None) == guarded
        assert (await fresh.get(Task, tid)).version == version + int(not guarded)
        assert (await fresh.get(Iteration, iid)).revision == revision + int(not guarded)
        assert (await fresh.get(Project, project.id)).owner_id == (mid if guarded else None)


@database_engines
async def test_mixed_case_allocation_reference_blocks_snapshot_restore(
    db_session,
    db_session_factory,
    task_factory,
    team_member_factory,
    profile_factory,
    monkeypatch,
):
    db = db_session
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    get_settings.cache_clear()
    principal = await initialize_control_plane(db)
    task = await task_factory()
    it = await db.get(Iteration, task.iteration_id)
    member = await team_member_factory(iteration=it, profile=await profile_factory())
    await db.commit()
    db.info["authority"] = Authority(principal, "system", workspace_role="operator")
    saved = await SnapshotService(db).create_snapshot(it.id, "before_membership")
    await db.execute(
        text(
            "CREATE TABLE Extension_Owner (ID INTEGER PRIMARY KEY, Member_ID INTEGER REFERENCES Team_Members(ID))"
        )
    )
    await db.commit()
    iid, mid, token = it.id, member.id, member.allocation_token
    with pytest.raises(PlanningConflict) as refused:
        await SnapshotService(db).restore(iid, saved)
    assert refused.value.code == "snapshot_reference_inventory_incomplete"
    async with db_session_factory() as read:
        actual = await read.get(TeamMember, mid)
        assert actual.iteration_id == iid and actual.allocation_token == token
