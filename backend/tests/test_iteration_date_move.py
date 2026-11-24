"""A proposed iteration period is checked against each person's bookings elsewhere and saves nothing."""

import json
from contextlib import asynccontextmanager
from datetime import date, timedelta

import httpx
import pytest
from sqlalchemy import func, select

from app import database, mcp_server
from app.config import get_settings
from app.main import app
from app.models.calendar import Calendar
from app.models.capacity import PlanningState
from app.models.identity import CommandAudit, IdentitySubject, Principal, ProjectMembership, WorkspaceMembership
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.recovery import ApplicationSnapshot
from app.models.task import Task
from app.models.team_member import TeamMemberCapacityAdjustment
from app.models.user_session import UserSession
from app.services.agent_service import hash_api_key
from app.services.identity_service import IdentityService, digest, initialize_control_plane
from app.utils.time import utc_now
from tests.test_review_provenance import database_engines
from tests.test_team_pm_dispatch import db_session_factory as db_session_factory  # noqa: F401

ADMIN = "date-move-operator"
ORIGIN = "https://test"
PROPOSED_START, PROPOSED_END = date(2026, 11, 19), date(2026, 12, 2)
LENT = (date(2026, 11, 19), date(2026, 11, 20))


@pytest.fixture(autouse=True)
def restore_settings_cache():
    yield
    get_settings.cache_clear()


async def managed(db, db_session_factory, monkeypatch):
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "managed")
    monkeypatch.setenv("WORKCHORD_ADMIN_API_KEY", ADMIN)
    monkeypatch.setenv("CORS_ORIGINS", json.dumps([ORIGIN]))
    monkeypatch.setattr(database, "async_session_maker", db_session_factory)
    get_settings.cache_clear()
    await initialize_control_plane(db)


async def staffed_iteration(db, profile_factory, team_member_factory):
    """Ten agent profiles staff a later Pi iteration; nine are fully booked by another project in November."""
    shared_2026 = Calendar(name="Shared 2026", year=2026)
    pi, library = Project(name="Pi"), Project(name="Library")
    db.add_all([shared_2026, pi, library])
    await db.flush()
    iteration = Iteration(name="Pi iteration", start_date=date(2027, 1, 28), end_date=date(2027, 2, 10),
                          calendar=Calendar(name="Pi 2027", year=2027), project_id=pi.id)
    booked = Iteration(name="Library autumn", start_date=date(2026, 11, 16), end_date=date(2026, 12, 31),
                       calendar=shared_2026, project_id=library.id)
    db.add_all([iteration, booked])
    await db.flush()
    profiles, booked_rows = [], []
    for index in range(10):
        profile = await profile_factory(display_name=f"Pi agent {index}")
        profiles.append(profile)
        await team_member_factory(profile=profile, iteration=iteration, availability_percent=100, operational_utilization=0)
        if index < 9:
            booked_rows.append(await team_member_factory(profile=profile, iteration=booked, availability_percent=100,
                                                         operational_utilization=0))
    # The other project lends one person's first two proposed days back.
    db.add(TeamMemberCapacityAdjustment(team_member_id=booked_rows[0].id, start_date=LENT[0], end_date=LENT[1],
                                        availability_percent=0, base_availability_percent=100,
                                        reason="Lent back", group_token="d" * 36))
    planned = Task(title="Pi follow-up", iteration_id=iteration.id, project_id=pi.id, status="planned")
    db.add(planned)
    await db.commit()
    return {"iteration": iteration.id, "booked": booked.id, "pi": pi.id, "library": library.id,
            "calendar": shared_2026.id, "profiles": [profile.id for profile in profiles], "task": planned.id}


def proposal(scenario, **extra):
    return {"start_date": str(PROPOSED_START), "end_date": str(PROPOSED_END),
            "calendar_id": scenario["calendar"], **extra}


async def human(db, project_roles, *, workspace_member=True):
    """A signed-in person with the given project roles; returns a cookie client factory."""
    principal = Principal(kind="human", display_name="Planner")
    db.add(principal)
    await db.flush()
    if workspace_member:
        db.add(WorkspaceMembership(principal_id=principal.id, role="member"))
    token = f"{principal.id:0>43}"
    db.add(IdentitySubject(principal_id=principal.id, issuer="https://issuer.example", subject=f"planner-{principal.id}"))
    db.add_all([ProjectMembership(principal_id=principal.id, project_id=project_id, role=role)
                for project_id, role in project_roles.items()])
    db.add(UserSession(principal_id=principal.id, session_token_hash=digest(token), csrf_token=f"csrf-{principal.id}",
                       ip_address="192.0.2.1", user_agent="browser", authenticated_at=utc_now(),
                       expires_at=utc_now() + timedelta(hours=1)))
    await db.commit()
    return lambda: httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url=ORIGIN,
                                     cookies={"workchord_session": token},
                                     headers={"X-CSRF-Token": f"csrf-{principal.id}", "Origin": ORIGIN})


@asynccontextmanager
async def operator():
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test",
                                 headers={"X-Admin-API-Key": ADMIN}) as value:
        yield value


async def persisted_state(factory, scenario):
    async with factory() as read:
        iteration = await read.get(Iteration, scenario["iteration"])
        return {
            "period": (iteration.start_date, iteration.end_date, iteration.calendar_id),
            "revisions": dict((await read.execute(select(Iteration.id, Iteration.revision))).all()),
            "planning": await read.scalar(select(PlanningState.revision)),
            "task_version": (await read.get(Task, scenario["task"])).version,
            "snapshots": await read.scalar(select(func.count()).select_from(ApplicationSnapshot)),
            "audits": await read.scalar(select(func.count()).select_from(CommandAudit)),
            "adjustments": await read.scalar(select(func.count()).select_from(TeamMemberCapacityAdjustment)),
        }


def assert_pi_shortfalls(body, scenario):
    profiles = {row["profile_id"]: row for row in body["profiles"]}
    ids = scenario["profiles"]
    assert [profiles[pid]["shortfall_days"] for pid in ids] == [8] + [10] * 8 + [0]
    assert profiles[ids[0]]["first_shortfall_date"] == "2026-11-23"
    assert all(profiles[pid]["first_shortfall_date"] == str(PROPOSED_START) for pid in ids[1:9])
    assert profiles[ids[9]]["shortfall_hours"] == 0 and profiles[ids[9]]["first_shortfall_date"] is None
    assert sum(1 for row in body["shortfalls"] if row["date"] == str(PROPOSED_START)) == 8
    first = next(row for row in body["shortfalls"] if row["profile_id"] == ids[1])
    assert (first["date"], first["available_hours"], first["requested_hours"], first["booked_elsewhere_hours"],
            first["overallocated_hours"], first["shortfall_hours"], first["current_overallocated_hours"]) == (
        str(PROPOSED_START), 8.0, 8.0, 8.0, 8.0, 8.0, 0.0)
    assert body["proposed"] == {"start_date": str(PROPOSED_START), "end_date": str(PROPOSED_END),
                                "calendar_id": scenario["calendar"], "additional_calendar_ids": [],
                                "working_days": 10, "missing_calendar_years": []}
    assert body["current"]["start_date"] == "2027-01-28" and body["applied"] is False
    assert body["shortfalls_truncated"] is False and body["unlinked_member_ids"] == []
    return first


@database_engines
async def test_rest_preview_reports_each_booked_profile_and_apply_is_fenced(
    db_session, db_session_factory, profile_factory, team_member_factory, monkeypatch
):
    db = db_session
    await managed(db, db_session_factory, monkeypatch)
    scenario = await staffed_iteration(db, profile_factory, team_member_factory)
    pi_manager = await human(db, {scenario["pi"]: "manager"})
    before = await persisted_state(db_session_factory, scenario)
    url = f"/api/iterations/{scenario['iteration']}/date-move/preview"

    async with operator() as api:
        preview = await api.post(url, json=proposal(scenario))
        assert preview.status_code == 200, preview.text
        body = preview.json()
        first = assert_pi_shortfalls(body, scenario)
        # The operator may read the other project, so the booking names its iteration.
        assert first["bookings"] == [{"iteration_id": scenario["booked"], "project_id": scenario["library"], "hours": 8.0}]
        assert first["private_booked_hours"] == 0
        assert body["expected_revisions"] == {str(scenario["iteration"]): before["revisions"][scenario["iteration"]]}
        assert body["planning_revision"] == (before["planning"] or 0)
    assert await persisted_state(db_session_factory, scenario) == before

    async with pi_manager() as api:
        own = await api.post(url, json=proposal(scenario))
        assert own.status_code == 200, own.text
        mine = own.json()
        first = assert_pi_shortfalls(mine, scenario)
        # A Pi manager learns how many hours are booked elsewhere, not where.
        assert first["bookings"] == [] and first["private_booked_hours"] == 8.0
        assert "Library" not in own.text
        observed = mine["expected_revisions"]
        stale = {key: value + 1 for key, value in observed.items()}
        conflict = await api.put(f"/api/iterations/{scenario['iteration']}",
                                 json=proposal(scenario, expected_revisions=stale))
        assert conflict.status_code == 409 and conflict.json()["detail"]["code"] == "iteration_version_conflict"
        assert await persisted_state(db_session_factory, scenario) == before

        applied = await api.put(f"/api/iterations/{scenario['iteration']}",
                                json=proposal(scenario, expected_revisions=observed))
        assert applied.status_code == 200, applied.text
        assert (applied.json()["start_date"], applied.json()["end_date"]) == (str(PROPOSED_START), str(PROPOSED_END))
        replay = await api.put(f"/api/iterations/{scenario['iteration']}",
                               json=proposal(scenario, expected_revisions=observed))
        assert replay.status_code == 409 and replay.json()["detail"]["code"] == "iteration_version_conflict"
        # After the move the saved plan shows the same overallocation the preview reported.
        capacity = await api.get(f"/api/team-member-profiles/{scenario['profiles'][1]}/capacity",
                                 params={"start": str(PROPOSED_START), "end": str(PROPOSED_START)})
        assert capacity.status_code == 200, capacity.text
        assert capacity.json()["days"][0]["overallocated_hours"] == 8.0
        assert capacity.json()["days"][0]["private_busy_hours"] == 8.0
    after = await persisted_state(db_session_factory, scenario)
    assert after["period"] == (PROPOSED_START, PROPOSED_END, scenario["calendar"])
    assert after["revisions"][scenario["iteration"]] == observed[str(scenario["iteration"])] + 1


@database_engines
async def test_preview_requires_edit_permission_on_the_iteration(
    db_session, db_session_factory, profile_factory, team_member_factory, monkeypatch
):
    db = db_session
    await managed(db, db_session_factory, monkeypatch)
    scenario = await staffed_iteration(db, profile_factory, team_member_factory)
    elsewhere = Project(name="Elsewhere")
    db.add(elsewhere)
    await db.commit()
    viewer = await human(db, {scenario["pi"]: "viewer", scenario["library"]: "viewer"}, workspace_member=False)
    other_manager = await human(db, {elsewhere.id: "manager"})
    before = await persisted_state(db_session_factory, scenario)
    url = f"/api/iterations/{scenario['iteration']}/date-move/preview"
    async with viewer() as api:
        refused = await api.post(url, json=proposal(scenario))
        assert refused.status_code == 403, refused.text
    async with other_manager() as api:
        refused = await api.post(url, json=proposal(scenario))
        assert refused.status_code in {403, 404}, refused.text
        assert "shortfalls" not in refused.text
    async with operator() as api:
        invalid = await api.post(url, json={"start_date": "2026-11-19", "end_date": "2028-01-01"})
        assert invalid.status_code == 409 and invalid.json()["detail"]["code"] == "date_move_range_invalid"
        empty = await api.post(url, json={})
        assert empty.status_code == 422
        null = await api.post(url, json={"start_date": None})
        assert null.status_code == 422
        missing = await api.post(url, json={"calendar_id": 999999})
        assert missing.status_code == 400
        absent = await api.post("/api/iterations/999999/date-move/preview", json=proposal(scenario))
        assert absent.status_code == 404
    assert await persisted_state(db_session_factory, scenario) == before


@database_engines
async def test_mcp_preview_then_update_with_returned_revisions(
    db_session, db_session_factory, profile_factory, team_member_factory, actor_factory, monkeypatch
):
    db = db_session
    await managed(db, db_session_factory, monkeypatch)
    monkeypatch.setattr(mcp_server, "_session_factory", db_session_factory)
    scenario = await staffed_iteration(db, profile_factory, team_member_factory)
    pm = await actor_factory(role="pm", scopes=json.dumps(["planning:write", "planning:read", "tasks:read"]),
                             api_key_hash=hash_api_key("date-move-pm"))
    reader = await actor_factory(role="pm", scopes=json.dumps(["planning:read", "tasks:read"]),
                                 api_key_hash=hash_api_key("date-move-reader"))
    for actor in (pm, reader):
        identity = await IdentityService(db).actor_context(actor)
        db.add(WorkspaceMembership(principal_id=identity.principal_id, role="member"))
        db.add(ProjectMembership(project_id=scenario["pi"], principal_id=identity.principal_id, role="manager"))
    await db.commit()
    before = await persisted_state(db_session_factory, scenario)
    server = mcp_server.create_mcp_server()
    application = mcp_server.MCPAgentKeyMiddleware(server.streamable_http_app())
    async with server.session_manager.run(), httpx.AsyncClient(
        transport=httpx.ASGITransport(app=application), base_url="http://localhost:8001"
    ) as api:
        async def call(key, name, arguments):
            response = await api.post("/", headers={"X-Agent-API-Key": key,
                                                     "Accept": "application/json, text/event-stream"},
                                      json={"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                                            "params": {"name": name, "arguments": arguments}})
            assert response.status_code == 200, response.text
            return response.json()["result"]

        result = await call("date-move-pm", "agent_preview_iteration_date_move",
                            {"iteration_id": scenario["iteration"], "payload": proposal(scenario)})
        assert not result["isError"], result
        body = json.loads(result["content"][0]["text"])
        first = assert_pi_shortfalls(body, scenario)
        assert first["bookings"] == [] and first["private_booked_hours"] == 8.0
        assert await persisted_state(db_session_factory, scenario) == before

        denied = await call("date-move-reader", "agent_preview_iteration_date_move",
                            {"iteration_id": scenario["iteration"], "payload": proposal(scenario)})
        assert denied["isError"]

        command = {"iteration_id": scenario["iteration"],
                   "payload": proposal(scenario, expected_revisions=body["expected_revisions"]),
                   "idempotency_key": "advance-pi", "rationale": "Advance the iteration", "correlation_id": "advance-pi"}
        receipt = await call("date-move-pm", "agent_update_iteration", command)
        assert not receipt["isError"], receipt
        stale = await call("date-move-pm", "agent_update_iteration", {**command, "idempotency_key": "advance-pi-again"})
        assert stale["isError"] and "iteration_version_conflict" in stale["content"][0]["text"]
    after = await persisted_state(db_session_factory, scenario)
    assert after["period"] == (PROPOSED_START, PROPOSED_END, scenario["calendar"])
