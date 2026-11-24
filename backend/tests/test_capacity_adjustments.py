"""Dated capacity adjustments change capacity on their dates only and leave issued work current."""

import json
from contextlib import asynccontextmanager
from datetime import date

import httpx
import pytest
from sqlalchemy import func, select

from app import database, mcp_server
from app.config import get_settings
from app.main import app
from app.models.agent import AgentTaskAssignment
from app.models.calendar import Calendar
from app.models.capacity import PlanningState
from app.models.identity import CommandAudit, ProjectMembership, WorkspaceMembership
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.recovery import ApplicationSnapshot
from app.models.task import Task
from app.models.team_member import TeamMember, TeamMemberCapacityAdjustment
from app.services.agent_service import hash_api_key
from app.services.identity_service import IdentityService, initialize_control_plane
from app.services.scheduler_service import SchedulerService
from app.services.team_service import TeamService
from tests.test_review_provenance import database_engines
from tests.test_team_pm_dispatch import db_session_factory as db_session_factory  # noqa: F401

ADMIN = "capacity-adjustment-operator"
FIRST, SECOND, THIRD = date(2027, 1, 4), date(2027, 1, 5), date(2027, 1, 6)


@pytest.fixture(autouse=True)
def restore_settings_cache():
    yield
    get_settings.cache_clear()


async def managed(db, db_session_factory, monkeypatch):
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("WORKCHORD_ADMIN_API_KEY", ADMIN)
    monkeypatch.setattr(database, "async_session_maker", db_session_factory)
    get_settings.cache_clear()
    await initialize_control_plane(db)


async def shared_person(db, profile_factory, team_member_factory):
    """Two projects' iteration rows each reserve the whole of one person's day."""
    profile = await profile_factory(profile_kind="human", display_name="Argon", assignment_modes=[])
    projects, rows = [], []
    for name in ("Pi", "Library"):
        project = Project(name=name)
        db.add(project)
        await db.flush()
        iteration = Iteration(name=f"{name} January", start_date=date(2027, 1, 4), end_date=date(2027, 1, 15),
                              calendar=Calendar(name=f"{name} 2027", year=2027), project_id=project.id)
        db.add(iteration)
        await db.flush()
        projects.append(project)
        rows.append(await team_member_factory(profile=profile, iteration=iteration,
                                              availability_percent=100, operational_utilization=0))
    return profile, projects, rows


def headers(context=None, **extra):
    values = {"X-Admin-API-Key": ADMIN, **extra}
    if context is not None:
        values["X-Expected-Revisions"] = json.dumps(context)
    return values


def reduce_two_days(percent=0, **extra):
    return {"adjustments": [{"start_date": str(FIRST), "end_date": str(SECOND), "availability_percent": percent}],
            "reason": "Move the overlapping days to the other project", **extra}


@asynccontextmanager
async def client():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as value:
        yield value


async def person_days(api, profile_id, start=FIRST, end=THIRD):
    response = await api.get(f"/api/team-member-profiles/{profile_id}/capacity",
                             params={"start": str(start), "end": str(end)}, headers=headers())
    assert response.status_code == 200, response.text
    return {row["date"]: (row["available_hours"], row["allocated_hours"], row["overallocated_hours"])
            for row in response.json()["days"]}


@database_engines
async def test_preview_then_apply_lowers_one_row_on_two_dates_only(
    db_session, db_session_factory, profile_factory, team_member_factory, actor_factory, monkeypatch
):
    db = db_session
    await managed(db, db_session_factory, monkeypatch)
    profile, projects, (pi_row, other_row) = await shared_person(db, profile_factory, team_member_factory)
    worker = await actor_factory(profile=await profile_factory())
    issued = Task(title="Library release", iteration_id=other_row.iteration_id, project_id=projects[1].id,
                  assignee_id=other_row.id, status="active", start_date=FIRST, end_date=SECOND, effort_hours=16)
    planned = Task(title="Pi follow-up", iteration_id=pi_row.iteration_id, project_id=projects[0].id, status="planned")
    db.add_all([issued, planned])
    await db.flush()
    db.add(AgentTaskAssignment(task_id=issued.id, actor_id=worker.id, state="accepted", task_version=issued.version))
    await db.commit()
    task_versions = {issued.id: issued.version, planned.id: planned.version}
    pid, mid, other_id = profile.id, pi_row.id, other_row.id
    iterations = sorted([pi_row.iteration_id, other_row.iteration_id])

    async with client() as api:
        assert (await person_days(api, pid))[str(FIRST)] == (8.0, 16.0, 8.0)
        context = await api.get(f"/api/tasks/planning-inputs/member/{mid}/context", headers=headers())
        assert context.status_code == 200, context.text
        observed = context.json()["expected_revisions"]
        assert sorted(map(int, observed)) == iterations
        assert context.json()["resource"]["capacity_adjustments"] == []
        async with db_session_factory() as read:
            planning_before = await read.scalar(select(PlanningState.revision))

        preview = await api.post(f"/api/team-members/{mid}/capacity-adjustments/preview", json=reduce_two_days(),
                                 headers=headers())
        assert preview.status_code == 200, preview.text
        body = preview.json()
        assert body["applied"] is False and body["created"][0]["id"] is None
        assert body["reduced_dates"] == [str(FIRST), str(SECOND)]
        assert [(day["date"], day["availability_percent_before"], day["availability_percent_after"],
                 day["allocated_hours_before"], day["allocated_hours_after"],
                 day["overallocated_hours_before"], day["overallocated_hours_after"]) for day in body["effective_capacity"]] == [
            (str(FIRST), 100.0, 0.0, 16.0, 8.0, 8.0, 0.0),
            (str(SECOND), 100.0, 0.0, 16.0, 8.0, 8.0, 0.0),
        ]
        async with db_session_factory() as read:
            assert await read.scalar(select(func.count()).select_from(TeamMemberCapacityAdjustment)) == 0
            assert await read.scalar(select(PlanningState.revision)) == planning_before
            assert dict((await read.execute(select(Iteration.id, Iteration.revision))).all()) == {
                int(key): value for key, value in observed.items()}

        stale = {**observed, str(iterations[1]): observed[str(iterations[1])] + 1}
        conflict = await api.post(f"/api/team-members/{mid}/capacity-adjustments", json=reduce_two_days(),
                                  headers=headers(stale))
        assert conflict.status_code == 409 and conflict.json()["detail"]["code"] == "iteration_version_conflict"
        partial = await api.post(f"/api/team-members/{mid}/capacity-adjustments", json=reduce_two_days(),
                                 headers=headers({str(iterations[0]): observed[str(iterations[0])]}))
        assert partial.status_code == 409 and partial.json()["detail"]["code"] == "planning_scope_changed"

        applied = await api.post(f"/api/team-members/{mid}/capacity-adjustments", json=reduce_two_days(),
                                 headers=headers(observed))
        assert applied.status_code == 200, applied.text
        result = applied.json()
        assert result["applied"] and result["created"][0]["id"] and result["created"][0]["base_availability_percent"] == 100
        assert result["resulting_revisions"] == {key: value + 1 for key, value in observed.items()}
        days = await person_days(api, pid, FIRST, date(2027, 1, 7))
        assert days == {str(FIRST): (8.0, 8.0, 0.0), str(SECOND): (8.0, 8.0, 0.0),
                        str(THIRD): (8.0, 16.0, 8.0), "2027-01-07": (8.0, 16.0, 8.0)}
        capacity = await api.get(f"/api/team-members/{mid}/capacity", headers=headers())
        other = await api.get(f"/api/team-members/{other_id}/capacity", headers=headers())
        # Ten working days of eight hours; the Pi row loses only its two adjusted days.
        assert (capacity.json()["hours"], capacity.json()["available_days"]) == (64.0, 8.0)
        assert (other.json()["hours"], other.json()["available_days"]) == (80.0, 10.0)
        workload = await api.get(f"/api/team-members/{mid}/workload", headers=headers())
        assert workload.json()["capacity_hours"] == 64.0

        replay = await api.post(f"/api/team-members/{mid}/capacity-adjustments", json=reduce_two_days(),
                                headers=headers(observed))
        assert replay.status_code == 409 and replay.json()["detail"]["code"] == "iteration_version_conflict"
        fresh = (await api.get(f"/api/tasks/planning-inputs/member/{mid}/context", headers=headers())).json()
        assert [row["id"] for row in fresh["resource"]["capacity_adjustments"]] == [result["created"][0]["id"]]
        overlap = await api.post(f"/api/team-members/{mid}/capacity-adjustments",
                                 json=reduce_two_days(50), headers=headers(fresh["expected_revisions"]))
        assert overlap.status_code == 409 and overlap.json()["detail"]["code"] == "capacity_adjustment_overlap"
        restored = await api.post(f"/api/team-members/{mid}/capacity-adjustments", headers=headers(fresh["expected_revisions"]),
                                  json={"withdraw_adjustment_ids": [result["created"][0]["id"]],
                                        "reason": "The other project no longer needs those days"})
        assert restored.status_code == 200, restored.text
        assert restored.json()["active_adjustments"] == [] and restored.json()["reduced_dates"] == []
        assert (await person_days(api, pid))[str(FIRST)] == (8.0, 16.0, 8.0)
        history = await api.get(f"/api/team-members/{mid}/capacity-adjustments", params={"include_withdrawn": "true"},
                                headers=headers())
        [record] = history.json()
        assert record["active"] is False and record["withdrawn_at"] and record["availability_percent"] == 0
        assert record["withdrawal_reason"] == "The other project no longer needs those days"
        assert (await api.get(f"/api/team-members/{mid}/capacity-adjustments", headers=headers())).json() == []

    async with db_session_factory() as current:
        assert dict((await current.execute(select(Task.id, Task.version).where(Task.id.in_(task_versions)))).all()) == task_versions
        assignment = await current.scalar(select(AgentTaskAssignment))
        assert (assignment.state, assignment.task_version) == ("accepted", task_versions[issued.id])
        assert await current.scalar(select(PlanningState.revision)) == (planning_before or 0) + 2
        audits = (await current.scalars(select(CommandAudit).where(CommandAudit.action == "team_member_capacity_adjusted")
                                        .order_by(CommandAudit.id))).all()
        assert [(len(row.details["created"]), len(row.details["withdrawn"])) for row in audits] == [(1, 0), (0, 1)]
        assert audits[0].project_id == projects[0].id and audits[0].reason.startswith("Move the overlapping")
        snapshots = (await current.execute(select(ApplicationSnapshot.iteration_id, ApplicationSnapshot.filename))).all()
        assert {iteration for iteration, name in snapshots if name.endswith("_before_planning_input_change.json")} == set(iterations)


@database_engines
async def test_reducing_dates_of_issued_work_is_refused_without_staling_it(
    db_session, db_session_factory, profile_factory, team_member_factory, actor_factory, monkeypatch
):
    db = db_session
    await managed(db, db_session_factory, monkeypatch)
    profile, projects, (_, row) = await shared_person(db, profile_factory, team_member_factory)
    worker = await actor_factory(profile=await profile_factory())
    task = Task(title="Library release", iteration_id=row.iteration_id, project_id=projects[1].id,
                assignee_id=row.id, status="planned", start_date=SECOND, end_date=THIRD, effort_hours=16)
    db.add(task)
    await db.flush()
    db.add(AgentTaskAssignment(task_id=task.id, actor_id=worker.id, state="queued", task_version=task.version))
    await db.commit()
    version, mid = task.version, row.id
    async with client() as api:
        observed = (await api.get(f"/api/tasks/planning-inputs/member/{mid}/context", headers=headers())).json()["expected_revisions"]
        refused = await api.post(f"/api/team-members/{mid}/capacity-adjustments", json=reduce_two_days(),
                                 headers=headers(observed))
        assert refused.status_code == 409 and refused.json()["detail"]["code"] == "capacity_adjustment_in_use"
        assert f"{task.id} (" in refused.json()["detail"]["message"]
        preview = await api.post(f"/api/team-members/{mid}/capacity-adjustments/preview", json=reduce_two_days(),
                                 headers=headers())
        assert preview.status_code == 409 and preview.json()["detail"]["code"] == "capacity_adjustment_in_use"
        # Raising capacity on the issued dates and lowering a date without issued work are both allowed.
        allowed = await api.post(f"/api/team-members/{mid}/capacity-adjustments", headers=headers(observed), json={
            "adjustments": [{"start_date": str(FIRST), "end_date": str(FIRST), "availability_percent": 0}],
            "reason": "Lend the first day"})
        assert allowed.status_code == 200, allowed.text
    async with db_session_factory() as current:
        assert (await current.get(Task, task.id)).version == version
        assignment = await current.scalar(select(AgentTaskAssignment))
        assert (assignment.state, assignment.task_version) == ("queued", version)
        assert await current.scalar(select(func.count()).select_from(TeamMemberCapacityAdjustment)) == 1


@database_engines
async def test_scheduler_and_capacity_honour_dated_adjustments(
    db_session, db_session_factory, profile_factory, team_member_factory
):
    db = db_session
    profile = await profile_factory(profile_kind="human", assignment_modes=[])
    iteration = Iteration(name="January", start_date=date(2027, 1, 4), end_date=date(2027, 1, 15),
                          calendar=Calendar(name="Forecast 2027", year=2027))
    db.add(iteration)
    await db.flush()
    row = await team_member_factory(profile=profile, iteration=iteration, availability_percent=100, operational_utilization=0)
    first = Task(title="Two days of work", iteration_id=iteration.id, assignee_id=row.id, status="planned",
                 effort_hours=16, effort_days=2, priority=1)
    db.add(first)
    db.add_all([
        TeamMemberCapacityAdjustment(team_member_id=row.id, start_date=FIRST, end_date=FIRST, availability_percent=0,
                                     base_availability_percent=100, reason="Lent to another project", group_token="a" * 36),
        TeamMemberCapacityAdjustment(team_member_id=row.id, start_date=SECOND, end_date=SECOND, availability_percent=50,
                                     base_availability_percent=100, reason="Half day", group_token="a" * 36),
    ])
    await db.commit()
    iteration_id, task_id, mid = iteration.id, first.id, row.id
    async with db_session_factory() as session:
        result = await SchedulerService(session).schedule_iteration(iteration_id)
        assert result.success, result
    async with db_session_factory() as session:
        scheduled = await session.get(Task, task_id)
        # Nothing on the 4th, four hours on the 5th, the remaining twelve hours from the 6th.
        assert (scheduled.start_date, scheduled.end_date) == (SECOND, date(2027, 1, 7))
        capacity = await TeamService(session).calculate_capacity(mid)
        assert (capacity.available_days, capacity.hours) == (8.5, 68.0)
        from app.services.agent_routing_service import AgentRoutingService
        loaded_iteration = await session.get(Iteration, iteration_id)
        await session.refresh(loaded_iteration, ["calendar"])
        members = await TeamService(session).get_by_iteration(iteration_id)
        routing = await AgentRoutingService(session)._capacity_inputs(
            task=scheduled, iteration=loaded_iteration, members=members)
        assert routing[mid]["available_capacity_days"] == 8.5
        assert routing[mid]["dated_availability"] == [(str(FIRST), str(FIRST), 0.0), (str(SECOND), str(SECOND), 50.0)]


@database_engines
async def test_mcp_planning_tools_preview_and_apply_one_receipt(
    db_session, db_session_factory, profile_factory, team_member_factory, actor_factory, monkeypatch
):
    db = db_session
    await managed(db, db_session_factory, monkeypatch)
    monkeypatch.setattr(mcp_server, "_session_factory", db_session_factory)
    profile, projects, (pi_row, _) = await shared_person(db, profile_factory, team_member_factory)
    pm = await actor_factory(role="pm", scopes=json.dumps(["team:write", "team:read", "planning:read"]),
                             api_key_hash=hash_api_key("capacity-adjustment-pm"))
    identity = await IdentityService(db).actor_context(pm)
    db.add(WorkspaceMembership(principal_id=identity.principal_id, role="member"))
    db.add_all([ProjectMembership(project_id=project.id, principal_id=identity.principal_id, role="manager")
                for project in projects])
    await db.commit()
    mid = pi_row.id
    server = mcp_server.create_mcp_server()
    application = mcp_server.MCPAgentKeyMiddleware(server.streamable_http_app())
    async with server.session_manager.run(), httpx.AsyncClient(
        transport=httpx.ASGITransport(app=application), base_url="http://localhost:8001"
    ) as api:
        async def call(name, arguments):
            response = await api.post("/", headers={"X-Agent-API-Key": "capacity-adjustment-pm",
                                                     "Accept": "application/json, text/event-stream"},
                                      json={"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                                            "params": {"name": name, "arguments": arguments}})
            assert response.status_code == 200, response.text
            result = response.json()["result"]
            assert not result["isError"], result
            return json.loads(result["content"][0]["text"])

        preview = await call("agent_preview_capacity_adjustment", {"member_id": mid, "payload": reduce_two_days()})
        assert preview["applied"] is False and preview["effective_capacity"][0]["allocated_hours_after"] == 8.0
        async with db_session_factory() as read:
            observed = dict((await read.execute(select(Iteration.id, Iteration.revision))).all())
            assert await read.scalar(select(func.count()).select_from(TeamMemberCapacityAdjustment)) == 0
        command = {"member_id": mid, "payload": reduce_two_days(expected_revisions={str(k): v for k, v in observed.items()}),
                   "idempotency_key": "lend-two-days", "rationale": "Free the shared days", "correlation_id": "lend-two-days"}
        receipt = await call("agent_apply_capacity_adjustment", command)
        again = await call("agent_apply_capacity_adjustment", command)
        assert receipt == again and receipt["result"]["applied"] and receipt["operation"] == "planning.team_member.capacity_adjustment"
    async with db_session_factory() as read:
        [row] = (await read.scalars(select(TeamMemberCapacityAdjustment))).all()
        assert (row.start_date, row.end_date, row.availability_percent, row.created_by_principal_id) == (
            FIRST, SECOND, 0.0, identity.principal_id)


@database_engines
async def test_adjustment_bounds_and_unused_allocation_removal(
    db_session, db_session_factory, profile_factory, team_member_factory, monkeypatch
):
    db = db_session
    await managed(db, db_session_factory, monkeypatch)
    profile, _, (pi_row, other_row) = await shared_person(db, profile_factory, team_member_factory)
    await db.commit()
    mid, other_id = pi_row.id, other_row.id
    async with client() as api:
        async def context():
            return (await api.get(f"/api/tasks/planning-inputs/member/{mid}/context", headers=headers())).json()["expected_revisions"]

        outside = await api.post(f"/api/team-members/{mid}/capacity-adjustments", headers=headers(await context()), json={
            "adjustments": [{"start_date": "2027-01-15", "end_date": "2027-01-18", "availability_percent": 0}], "reason": "Late"})
        assert outside.status_code == 409 and outside.json()["detail"]["code"] == "capacity_adjustment_outside_iteration"
        overlapping = await api.post(f"/api/team-members/{mid}/capacity-adjustments", headers=headers(await context()), json={
            "adjustments": [{"start_date": str(FIRST), "end_date": str(SECOND), "availability_percent": 0},
                            {"start_date": str(SECOND), "end_date": str(THIRD), "availability_percent": 50}], "reason": "Both"})
        assert overlapping.status_code == 409 and overlapping.json()["detail"]["code"] == "capacity_adjustment_overlap"
        invalid = await api.post(f"/api/team-members/{mid}/capacity-adjustments", headers=headers(await context()),
                                 json={"adjustments": [], "reason": "Nothing"})
        assert invalid.status_code == 422
        first = await api.post(f"/api/team-members/{mid}/capacity-adjustments", headers=headers(await context()),
                               json=reduce_two_days())
        assert first.status_code == 200, first.text
        replaced = await api.post(f"/api/team-members/{mid}/capacity-adjustments", headers=headers(await context()), json={
            "withdraw_adjustment_ids": [first.json()["created"][0]["id"]],
            "adjustments": [{"start_date": str(FIRST), "end_date": str(FIRST), "availability_percent": 25}],
            "reason": "Keep part of the first day only"})
        assert replaced.status_code == 200, replaced.text
        assert replaced.json()["reduced_dates"] == [] and [
            (day["date"], day["availability_percent_before"], day["availability_percent_after"])
            for day in replaced.json()["effective_capacity"]] == [(str(FIRST), 0.0, 25.0), (str(SECOND), 0.0, 100.0)]
        removed = await api.delete(f"/api/team-members/{mid}", params={"unused_only": "true"},
                                   headers=headers(await context()))
        assert removed.status_code == 200, removed.text
    async with db_session_factory() as current:
        assert await current.get(TeamMember, mid) is None and await current.get(TeamMember, other_id) is not None
        assert await current.scalar(select(func.count()).select_from(TeamMemberCapacityAdjustment)) == 0
        assert await current.scalar(select(func.count()).select_from(CommandAudit).where(
            CommandAudit.action == "team_member_capacity_adjusted")) == 2


@database_engines
async def test_restoring_the_prior_snapshot_withdraws_the_adjustment_and_keeps_its_record(
    db_session, db_session_factory, profile_factory, team_member_factory, monkeypatch
):
    db = db_session
    await managed(db, db_session_factory, monkeypatch)
    profile, _, (pi_row, _) = await shared_person(db, profile_factory, team_member_factory)
    await db.commit()
    pid, mid, iteration_id = profile.id, pi_row.id, pi_row.iteration_id
    async with client() as api:
        observed = (await api.get(f"/api/tasks/planning-inputs/member/{mid}/context", headers=headers())).json()["expected_revisions"]
        applied = await api.post(f"/api/team-members/{mid}/capacity-adjustments", json=reduce_two_days(), headers=headers(observed))
        assert applied.status_code == 200, applied.text
        async with db_session_factory() as read:
            [prior] = await read.scalars(select(ApplicationSnapshot.filename).where(
                ApplicationSnapshot.iteration_id == iteration_id,
                ApplicationSnapshot.filename.like("%_before_planning_input_change.json")))
        assert (await person_days(api, pid))[str(FIRST)] == (8.0, 8.0, 0.0)
        restored = await api.post(f"/api/iterations/{iteration_id}/snapshots/{prior}/restore",
                                  json={"confirm": True}, headers=headers())
        assert restored.status_code == 200, restored.text
        assert (await person_days(api, pid))[str(FIRST)] == (8.0, 16.0, 8.0)
        [record] = (await api.get(f"/api/team-members/{mid}/capacity-adjustments", params={"include_withdrawn": "true"},
                                  headers=headers())).json()
        assert record["active"] is False and record["withdrawal_reason"] == f"Restored recovery snapshot {prior}"
        # The restore first saved the adjusted state as its own recovery point; restoring that brings it back.
        recovery = restored.json()["pre_restore_snapshot"]
        again = await api.post(f"/api/iterations/{iteration_id}/snapshots/{recovery}/restore",
                               json={"confirm": True}, headers=headers())
        assert again.status_code == 200, again.text
        assert (await person_days(api, pid))[str(FIRST)] == (8.0, 8.0, 0.0)
        active = (await api.get(f"/api/team-members/{mid}/capacity-adjustments", headers=headers())).json()
        assert [(row["start_date"], row["availability_percent"]) for row in active] == [(str(FIRST), 0.0)]
