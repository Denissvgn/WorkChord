"""Annual planning inputs and execution authority are independently fenced."""

from datetime import date
import asyncio
import json

import httpx
import pytest
from sqlalchemy import select, text

from app.config import get_settings
from app import mcp_server
from app.authority import internal_authority
from app.commands import AggregateVersionConflict, PlanningConflict, command_transaction, lock_planning
from app.main import app
from app.models.agent import AgentModelCatalogEntry, AgentRun, AgentTaskAssignment
from app.models.calendar import Calendar
from app.models.identity import Principal, ProjectMembership, WorkspaceMembership
from app.models.capacity import ProfileAvailability
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.task import Task
from app.services.identity_service import IdentityService, initialize_control_plane
from app.services.iteration_service import IterationService
from app.services.agent_planning_service import AgentPlanningService
from app.services.agent_service import AgentService
from app.services.agent_work_service import AgentWorkService
from app.services.capacity_service import CapacityService
from app.schemas.agent import AgentTaskAssignmentCreate
from app.schemas.agent_planning import AgentPlanningCommandContext
from app.schemas.iteration import IterationUpdate
from tests.test_agent_team_setup_qualification import provision_ready_topology, routing_base
from tests.test_execution_planning_window import planning_patch
from tests.test_review_provenance_transports import databases, fence
from tests import test_team_pm_dispatch
from tests.test_team_pm_recovery import recovery_api

db_session_factory = test_team_pm_dispatch.db_session_factory


def pm_headers(key, receipt):
    return {
        "X-Agent-API-Key": key,
        "Idempotency-Key": receipt,
        "X-Correlation-ID": receipt,
        "X-Agent-Rationale": "Plan the agreed annual delivery window",
    }


def apply_inputs(receipt):
    return {
        "expected_input_digest": receipt["input_digest"],
        "expected_task_versions": {
            str(task["task_id"]): task["version"] for task in receipt["task_states"]
        },
    }


async def calendar_edit(http, transport, key, iteration, revision, label, *, refused=False, **changes):
    if transport == "rest":
        response = await planning_patch(http, key, iteration, revision, label, **changes)
        if refused:
            assert (
                response.status_code == 409
                and response.json()["detail"]["code"] == "annual_calendar_change_in_use"
            ), response.text
            return response.json()["detail"]
        assert response.status_code == 200, response.text
        return response.json()["result"]
    server = mcp_server.create_mcp_server()
    application = mcp_server.MCPAgentKeyMiddleware(server.streamable_http_app())
    async with (
        server.session_manager.run(),
        httpx.AsyncClient(
            transport=httpx.ASGITransport(app=application), base_url="http://localhost:8001"
        ) as client,
    ):
        response = await client.post(
            "/",
            headers={"X-Agent-API-Key": key, "Accept": "application/json, text/event-stream"},
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "tools/call",
                "params": {
                    "name": "agent_update_iteration",
                    "arguments": {
                        "iteration_id": iteration,
                        "idempotency_key": label,
                        "rationale": "Update the planned annual calendar",
                        "correlation_id": label,
                        "payload": {"expected_revisions": {str(iteration): revision}, **changes},
                    },
                },
            },
        )
        result = response.json()["result"]
        if not refused:
            assert not result["isError"], result
            return json.loads(result["content"][0]["text"])["result"]
        assert result["isError"], result
        public_message = result["content"][0]["text"].split("agent_update_iteration: ", 1)[1]
        assert public_message.startswith("{"), public_message
        error = json.loads(public_message)
        assert error["code"] == "annual_calendar_change_in_use" and "issued work" in error["message"]
        return error


@databases
@pytest.mark.parametrize("transport", ["rest", "mcp"])
@pytest.mark.parametrize("lane", ["running", "verification", "rework"])
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_annual_selection_and_forecast_preserve_live_ownership(
    db_session,
    db_session_factory,
    team_member_factory,
    task_factory,
    monkeypatch,
    transport,
    lane,
):
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    get_settings.cache_clear()
    db = db_session
    await initialize_control_plane(db)
    await db.commit()
    team = await provision_ready_topology(db)
    member, verifier, controller = (
        team.manifest.workers[0],
        team.manifest.verifiers[0],
        team.manifest.controller,
    )
    worker, reviewer, pm = (team.actors[item.actor_key] for item in (member, verifier, controller))
    worker_key, reviewer_key, pm_key = (
        team.sink.keys[item.actor_key] for item in (member, verifier, controller)
    )
    scope = await routing_base(
        db,
        topology=team,
        actor_key=member.actor_key,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        title="Review the delivery notes",
    )
    task = scope.task
    scope.member.operational_utilization = 0
    scope.member.availability_percent = 100
    primary = Calendar(name="First year", year=2026)
    following = Calendar(name="Following year", year=2027, holidays=["2027-01-01"])
    alternate = Calendar(name="Different primary year policy", year=2026, holidays=["2026-11-20"])
    project = Project(
        name="Delivery", target_date=date(2027, 2, 19), require_different_review_publisher=True
    )
    db.add_all([project, primary, following, alternate])
    await db.flush()
    iteration = await db.get(Iteration, task.iteration_id)
    iteration.project_id = task.project_id = project.id
    iteration.calendar_id = primary.id
    iteration.start_date, iteration.end_date = date(2026, 11, 13), date(2026, 12, 31)
    task.effort_hours, task.start_date, task.end_date = 8, date(2026, 11, 19), date(2026, 11, 20)
    planned = await task_factory(
        iteration=iteration,
        assignee=scope.member,
        project_id=project.id,
        title="Prepare the next delivery",
        effort_hours=8,
        effort_days=1,
        min_start_date=date(2027, 1, 1),
        status="planned",
    )
    for actor, role in ((pm, "manager"), (worker, "executor"), (reviewer, "reviewer")):
        identity = await IdentityService(db).actor_context(actor)
        db.add_all(
            [
                WorkspaceMembership(principal_id=identity.principal_id, role="member"),
                ProjectMembership(principal_id=identity.principal_id, project_id=project.id, role=role),
            ]
        )
    for candidate, publisher in ((member, "worker-publisher"), (verifier, "review-publisher")):
        model = await db.scalar(
            select(AgentModelCatalogEntry).where(
                AgentModelCatalogEntry.key == candidate.default_model_binding_key
            )
        )
        model.publisher_key = publisher
    await db.commit()
    work = ("agent_get_my_work", "/api/agent/me/work")
    begin = ("agent_begin_my_work", "/api/agent/me/work/begin")
    dispatch = ("agent_create_assignment", "/api/agent/assignments")
    submit = ("agent_submit_my_work", "/api/agent/me/work/submit")
    verdict = ("agent_submit_review_verdict", "/api/agent/me/reviews/verdict")
    retained = {
        "summary": "Delivery notes ready",
        "observed_model": member.default_model_binding_key,
        "evidence": {"criterion": "checked examples"},
        "artifact_links": ["https://example.test/notes"],
    }
    async with (
        recovery_api(transport, db_session_factory, monkeypatch) as call,
        httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://localhost:8001") as http,
    ):
        assigned = await call(
            *dispatch,
            pm_key,
            payload={
                "actor_id": worker.id,
                "task_id": task.id,
                "expected_task_version": task.version,
                "reviewer_profile_id": reviewer.profile_id,
            },
            receipt="dispatch",
        )
        ready = await call(*work, worker_key)
        running = await call(
            *begin,
            worker_key,
            payload={
                "assignment_id": assigned["id"],
                "queue_revision": ready["queue_revision"],
                "model": member.default_model_binding_key,
            },
            receipt="begin",
        )
        live_id = assigned["id"]
        if lane != "running":
            submitted = await call(
                *submit, worker_key, payload={**fence(running), **retained}, receipt="submit"
            )
            verification = await call(
                *dispatch,
                pm_key,
                payload={
                    "actor_id": reviewer.id,
                    "task_id": task.id,
                    "reviewer_profile_id": reviewer.profile_id,
                    "purpose": "verification",
                    "expected_task_version": submitted["task"]["version"],
                },
                receipt="assign-review",
            )
            live_id = verification["id"]
            review = {
                "assignment_id": live_id,
                "observed_model": verifier.default_model_binding_key,
                "reviewed_candidate_digest": verification["review_selection"]["candidate"]["digest"],
                "evidence": {"criterion": "inspected attached notes"},
            }
            if lane == "rework":
                rejected = await call(
                    *verdict,
                    reviewer_key,
                    payload={
                        **review,
                        "verdict": "reject",
                        "reason": "Clarify the examples",
                        "rework_actor_id": worker.id,
                        "expected_task_version": submitted["task"]["version"],
                    },
                    receipt="return",
                )
                live_id = rejected["rework_assignment"]["id"]

        async with db_session_factory() as read:
            revision = (await read.get(Iteration, iteration.id)).revision
        extended = await planning_patch(
            http, pm_key, iteration.id, revision, "extend", end_date="2027-01-05"
        )
        assert extended.status_code == 200, extended.text
        revision = extended.json()["result"]["revision"]
        if lane == "running":
            await calendar_edit(
                http,
                transport,
                pm_key,
                iteration.id,
                revision,
                "primary-replacement",
                refused=True,
                calendar_id=alternate.id,
            )
            await calendar_edit(
                http,
                transport,
                pm_key,
                iteration.id,
                revision,
                "mixed-replacement",
                refused=True,
                name="A different plan",
                calendar_id=alternate.id,
                additional_calendar_ids=[following.id],
            )
            await calendar_edit(
                http,
                transport,
                pm_key,
                iteration.id,
                revision,
                "combined-extension",
                refused=True,
                end_date="2027-01-06",
                additional_calendar_ids=[following.id],
            )
            async with db_session_factory() as read:
                held_iteration = await read.get(Iteration, iteration.id)
                assert held_iteration.revision == revision and held_iteration.calendar_id == primary.id
                assert (
                    held_iteration.end_date == date(2027, 1, 5) and not held_iteration.additional_calendars
                )
        planning_path = f"/api/agent/planning/iterations/{iteration.id}"
        readiness = await http.get(planning_path + "/readiness", headers=pm_headers(pm_key, "read"))
        assert readiness.json()["missing_calendar_years"] == [2027]

        async def preview(label):
            response = await http.post(
                planning_path + "/schedule/preview", headers=pm_headers(pm_key, label)
            )
            assert response.status_code == 200, response.text
            return response.json()["result"]

        async def apply(receipt, label):
            return await http.post(
                planning_path + "/schedule/apply",
                headers=pm_headers(pm_key, label),
                json=apply_inputs(receipt),
            )

        # An old held forecast must not become applicable after the annual selection.
        held = await preview("held-forecast")
        assert not held["success"] and any(
            issue["code"] == "calendar_outside_year" for issue in held["capacity_issues"]
        )
        async with db_session_factory() as read:
            original = await read.get(Task, task.id)
            version, window = original.version, original.execution_planning_window
            assert window and str(live_id) in window["assignments"]
            original_assignment = await read.get(AgentTaskAssignment, live_id)
            original_lineage = (
                original_assignment.task_version,
                original_assignment.routing_snapshot,
                original_assignment.review_selection,
            )
        selected = await planning_patch(
            http, pm_key, iteration.id, revision, "bind-year", additional_calendar_ids=[following.id]
        )
        assert selected.status_code == 200, selected.text
        assert selected.json()["result"]["additional_calendar_ids"] == [following.id]
        assert (
            await planning_patch(
                http, pm_key, iteration.id, revision, "bind-year", additional_calendar_ids=[following.id]
            )
        ).json() == selected.json()
        assert (await apply(held, "stale-forecast")).status_code == 409
        readiness = (
            await http.get(planning_path + "/readiness", headers=pm_headers(pm_key, "read-ready"))
        ).json()
        assert readiness["checkpoints"][0]["state"] == "done" and not readiness["missing_calendar_years"]
        forecast = await preview("current-forecast")
        assert forecast["success"] and forecast["input_digest"] != held["input_digest"]
        applied = await apply(forecast, "save-forecast")
        assert applied.status_code == 200, applied.text
        async with db_session_factory() as read:
            original = await read.get(Task, task.id)
            assert (original.version, original.execution_planning_window) == (version, window)
            live = await read.get(AgentTaskAssignment, live_id)
            assert (live.task_version, live.routing_snapshot, live.review_selection) == original_lineage
            assert (await read.get(AgentRun, running["run"]["id"])).assignment_id == assigned["id"]
            scheduled = await read.get(Task, planned.id)
            assert (scheduled.start_date, scheduled.end_date) == (date(2027, 1, 4), date(2027, 1, 4))
            assert (await read.get(Project, project.id)).target_date == date(2027, 2, 19)
        if lane == "verification":
            accepted = await call(
                *verdict,
                reviewer_key,
                payload={
                    **review,
                    "verdict": "pass",
                    "reason": "All examples checked",
                    "expected_task_version": version,
                },
                receipt="accept",
            )
            assert accepted["task"]["status"] == "closed"
            async with db_session_factory() as read:
                previous = (await read.get(Task, planned.id)).version
                revision = (await read.get(Iteration, iteration.id)).revision
            ordinary = await calendar_edit(
                http, transport, pm_key, iteration.id, revision, "later-primary", calendar_id=alternate.id
            )
            assert ordinary["calendar_id"] == alternate.id and ordinary["additional_calendar_ids"] == [
                following.id
            ]
            mixed = await calendar_edit(
                http,
                transport,
                pm_key,
                iteration.id,
                ordinary["revision"],
                "later-mixed",
                name="Confirmed later plan",
                calendar_id=primary.id,
                additional_calendar_ids=[following.id],
            )
            assert mixed["calendar_id"] == primary.id and mixed["name"] == "Confirmed later plan"
            async with db_session_factory() as read:
                assert (await read.get(Task, planned.id)).version == previous + 2
                assert (await read.get(Task, task.id)).status == "closed"
        elif lane == "rework":
            queue = await call(*work, worker_key)
            assert queue["state"] == "start_assigned" and queue["next"]["assignment"]["id"] == live_id
            corrected = await call(
                *begin,
                worker_key,
                payload={
                    "assignment_id": live_id,
                    "queue_revision": queue["queue_revision"],
                    "model": member.default_model_binding_key,
                },
                receipt="correct",
            )
            assert (
                corrected["run"]["execution_provenance"]["supervised_rework"]["reviewer_profile_id"]
                == reviewer.profile_id
            )
        else:
            assert (await call(*work, worker_key))["state"] == "resume"
            renewed = await call(
                "agent_renew_my_work",
                "/api/agent/me/work/renew",
                worker_key,
                payload={**fence(running), "expected_task_version": version},
                receipt="renew",
            )
            done = await call(*submit, worker_key, payload={**fence(renewed), **retained}, receipt="finish")
            assert done["run"]["status"] == "succeeded" and done["run"]["id"] == running["run"]["id"]


@databases
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_mcp_reports_an_existing_issued_year_conflict(
    db_session,
    db_session_factory,
    team_member_factory,
    task_factory,
    monkeypatch,
    record_property,
):
    """Real team dispatch and an already protected supplemental-year removal exercise the error adapter."""
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    get_settings.cache_clear()
    await initialize_control_plane(db_session)
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
        title="Prepare the annual notes",
    )
    project = Project(name="Annual notes")
    following = Calendar(name="Following policy", year=2027)
    db_session.add_all([project, following])
    await db_session.flush()
    iteration = await IterationService(db_session).get_by_id(scope.task.iteration_id)
    iteration.project_id = scope.task.project_id = project.id
    iteration.start_date, iteration.end_date = date(2026, 12, 21), date(2027, 1, 8)
    iteration.additional_calendars = [following]
    scope.task.start_date = scope.task.end_date = date(2027, 1, 5)
    scope.task.effort_hours = 8
    for actor, role in ((pm, "manager"), (worker, "executor")):
        identity = await IdentityService(db_session).actor_context(actor)
        db_session.add_all(
            [
                WorkspaceMembership(principal_id=identity.principal_id, role="member"),
                ProjectMembership(principal_id=identity.principal_id, project_id=project.id, role=role),
            ]
        )
    await db_session.commit()
    pm_key = team.sink.keys[controller.actor_key]
    async with (
        recovery_api("rest", db_session_factory, monkeypatch) as call,
        httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://localhost:8001") as http,
    ):
        issued = await call(
            "agent_create_assignment",
            "/api/agent/assignments",
            pm_key,
            payload={
                "actor_id": worker.id,
                "task_id": scope.task.id,
                "expected_task_version": scope.task.version,
            },
            receipt="queue-annual-notes",
        )
        async with db_session_factory() as read:
            revision = (await read.get(Iteration, iteration.id)).revision
        for transport in ("rest", "mcp"):
            detail = await calendar_edit(
                http,
                transport,
                pm_key,
                iteration.id,
                revision,
                "hold-" + transport,
                refused=True,
                additional_calendar_ids=[],
            )
            assert f"{scope.task.id} ({issued['id']})" in detail["message"]
            record_property(transport + "_public_code", detail["code"])
        async with db_session_factory() as read:
            current = await read.get(Iteration, iteration.id)
            assert current.revision == revision and [row.id for row in current.additional_calendars] == [
                following.id
            ]
            assert (await read.get(AgentTaskAssignment, issued["id"])).state == "queued"


@pytest.mark.parametrize(
    "db_session_factory",
    [pytest.param("postgresql", marks=[pytest.mark.postgresql, pytest.mark.allow_network])],
    indirect=True,
)
@pytest.mark.parametrize("owner", ["iteration", "person"])
@pytest.mark.parametrize("first_writer", ["calendar", "dispatch"])
@pytest.mark.usefixtures("deployed_agent_skill_release")
async def test_postgres_dispatch_serializes_with_supplemental_policy_replacement(
    db_session,
    db_session_factory,
    team_member_factory,
    task_factory,
    monkeypatch,
    owner,
    first_writer,
    record_property,
):
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("MODEL_AWARE_ROUTING_MODE", "shadow")
    get_settings.cache_clear()
    await initialize_control_plane(db_session)
    await db_session.commit()
    team = await provision_ready_topology(db_session)
    controller, member = team.manifest.controller, team.manifest.workers[0]
    pm, worker = (team.actors[row.actor_key] for row in (controller, member))
    scope = await routing_base(
        db_session,
        topology=team,
        actor_key=member.actor_key,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        title="Schedule the next-year handoff",
    )
    project = Project(name="Annual schedule")
    old, new = (
        Calendar(name="Original next year", year=2027),
        Calendar(name="Revised next year", year=2027, holidays=["2027-01-06"]),
    )
    operator = Principal(kind="human", display_name="Scheduling operator")
    db_session.add_all([project, old, new, operator])
    await db_session.flush()
    iteration = await IterationService(db_session).get_by_id(scope.task.iteration_id)
    iteration.project_id = scope.task.project_id = project.id
    iteration.end_date = date(2027, 1, 8)
    iteration.additional_calendars = [old]
    scope.task.start_date = scope.task.end_date = date(2027, 1, 5)
    scope.task.effort_hours = 8
    for actor, role in ((pm, "manager"), (worker, "executor")):
        identity = await IdentityService(db_session).actor_context(actor)
        db_session.add_all(
            [
                WorkspaceMembership(principal_id=identity.principal_id, role="member"),
                ProjectMembership(principal_id=identity.principal_id, project_id=project.id, role=role),
            ]
        )
    db_session.add(WorkspaceMembership(principal_id=operator.id, role="operator"))
    if owner == "person":
        db_session.add(
            ProfileAvailability(
                profile_id=worker.profile_id,
                calendar_id=iteration.calendar_id,
                version=1,
                additional_calendars=[old],
            )
        )
    await db_session.commit()
    tid, version, period = scope.task.id, scope.task.version, iteration.id
    primary, original, replacement, profile = iteration.calendar_id, old.id, new.id, worker.profile_id
    actor_id, operator_id, revision = worker.id, operator.id, iteration.revision
    secret = team.sink.keys[controller.actor_key]
    first_ready, continue_first = asyncio.Event(), asyncio.Event()
    second_pid = asyncio.get_running_loop().create_future()
    pids = {}

    async def selected(session):
        if owner == "person":
            with internal_authority(session):
                setting = await session.get(ProfileAvailability, profile, populate_existing=True)
                return [row.id for row in setting.additional_calendars]
        return [row.id for row in (await IterationService(session).get_by_id(period)).additional_calendars]

    async def writer(kind, *, retry=False):
        async with db_session_factory() as db, command_transaction(db):
            # Observe the backend before binding the actor. No unscoped SQL is
            # needed (or permitted) on the managed actor's connection afterward.
            pid = await db.scalar(text("select pg_backend_pid()"))
            await db.execute(text("SET LOCAL statement_timeout='15s'"))
            await db.execute(text("SET LOCAL deadlock_timeout='200ms'"))
            if not retry:
                pids[kind] = pid
                if kind != first_writer:
                    second_pid.set_result(pid)
            actor = await AgentService(db).authenticate(secret, touch=False)
            assert actor is not None
            if owner == "person" and kind == "calendar":
                principal = await db.get(Principal, operator_id)
                db.info["authority"] = await IdentityService(db).context(principal)
            else:
                # The real agent REST adapter binds this protocol source after
                # authenticating the stored key; an ordinary human REST context
                # cannot authorize an actor's queue revision.
                db.info["authority"] = await IdentityService(db).actor_context(actor, source="agent_rest")
            if kind == "calendar":
                if first_writer == "calendar" and not retry:
                    # Pause immediately after the calendar command's first real
                    # reservation and before its narrower iteration/task access.
                    await lock_planning(db)
                    first_ready.set()
                    await asyncio.wait_for(continue_first.wait(), 12)
                if owner == "person":
                    await CapacityService(db).set_calendar(profile, primary, 1, [replacement])
                else:
                    observed = (
                        (await IterationService(db).get_by_id(period)).revision if retry else revision
                    )
                    key = "replace-after-reread" if retry else "replace-annual"
                    await AgentPlanningService(db).update_iteration(
                        period,
                        actor,
                        IterationUpdate(
                            additional_calendar_ids=[replacement], expected_revisions={period: observed}
                        ),
                        command=AgentPlanningCommandContext(
                            idempotency_key=key,
                            correlation_id=key,
                            rationale="Use the revised annual policy",
                        ),
                    )
                return await selected(db)
            assignment = await AgentWorkService(db).create_assignment(
                actor,
                AgentTaskAssignmentCreate(actor_id=actor_id, task_id=tid, expected_task_version=version),
                idempotency_key="issue-annual",
                correlation_id="issue-annual",
                rationale="Queue the named annual work",
            )
            observed = await selected(db)
            if first_writer == "dispatch":
                first_ready.set()
                await asyncio.wait_for(continue_first.wait(), 12)
            return assignment.id, observed

    started = asyncio.create_task(writer(first_writer))
    reached = asyncio.create_task(first_ready.wait())
    try:
        done, _ = await asyncio.wait({reached, started}, timeout=12, return_when=asyncio.FIRST_COMPLETED)
        if started in done:
            await started
        assert reached in done and first_ready.is_set(), (
            "First writer did not reach its transaction boundary"
        )
    finally:
        reached.cancel()
        await asyncio.gather(reached, return_exceptions=True)
        if not first_ready.is_set():
            started.cancel()
            await asyncio.gather(started, return_exceptions=True)
    second_kind = "dispatch" if first_writer == "calendar" else "calendar"
    waiting = asyncio.create_task(writer(second_kind))
    observed_wait = False
    broad_table_locks = None
    try:
        pid = await asyncio.wait_for(second_pid, 10)
        async with db_session_factory() as monitor:
            for _ in range(240):
                blockers = await monitor.scalar(text("select pg_blocking_pids(:pid)"), {"pid": pid})
                if pids[first_writer] in blockers:
                    observed_wait = True
                    if first_writer == "calendar":
                        broad_table_locks = await monitor.scalar(
                            text(
                                "select count(*) from pg_locks where pid=:pid and granted "
                                "and mode='ShareRowExclusiveLock' and relation in "
                                "('tasks'::regclass,'iterations'::regclass,'agent_task_assignments'::regclass)"
                            ),
                            {"pid": pid},
                        )
                    break
                await asyncio.sleep(0.025)
    finally:
        continue_first.set()
    first_result, second_result = await asyncio.gather(started, waiting, return_exceptions=True)
    for label, result in (("first", first_result), ("second", second_result)):
        cause = getattr(result, "orig", None)
        state = getattr(cause, "sqlstate", None) or getattr(
            getattr(cause, "__cause__", None), "sqlstate", None
        )
        if state:
            record_property(label + "_sqlstate", state)
    record_property("postgres_wait_observed", str(observed_wait).lower())
    if broad_table_locks is not None:
        record_property("broad_table_locks_while_waiting_for_planning", broad_table_locks)
    assert observed_wait, "The competing writer did not wait for the actual first transaction"
    assert not isinstance(first_result, Exception), repr(first_result)
    if first_writer == "calendar":
        assert broad_table_locks == 0
        assert first_result == [replacement] and not isinstance(second_result, Exception), repr(
            second_result
        )
        assignment, observed = second_result
        assert observed == [replacement]
    else:
        assignment, observed = first_result
        assert observed == [original]
        if isinstance(second_result, AggregateVersionConflict):
            # Dispatch advanced the iteration revision. A real fresh observation
            # of that revision must meet the issued-work check on retry.
            with pytest.raises(PlanningConflict) as fresh:
                await writer("calendar", retry=True)
            second_result = fresh.value
        assert (
            isinstance(second_result, PlanningConflict)
            and second_result.code == "annual_calendar_change_in_use"
        ), repr(second_result)
    async with db_session_factory() as final:
        assert (await final.get(Task, tid)).version == version
        issued = await final.get(AgentTaskAssignment, assignment)
        assert issued.task_version == version and issued.state == "queued"
        assert (
            await final.scalars(select(AgentTaskAssignment.id).where(AgentTaskAssignment.task_id == tid))
        ).all() == [assignment]
        assert await selected(final) == ([replacement] if first_writer == "calendar" else [original])
    record_property("competing_writers", "2")
    record_property("unchanged_task_version", version)
    record_property(
        "post_serialization_selection", "replacement" if first_writer == "calendar" else "original"
    )
