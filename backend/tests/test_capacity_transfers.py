"""A temporary capacity transfer lends availability between rows of one person and returns it after its dates."""

import json
from datetime import date

import httpx
import pytest
from sqlalchemy import func, select, update

from app import mcp_server
from app.config import get_settings
from app.models.agent import AgentTaskAssignment
from app.models.calendar import Calendar
from app.models.identity import CommandAudit, ProjectMembership, WorkspaceMembership
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.task import Task
from app.models.team_member import TeamMemberCapacityAdjustment
from app.services import capacity_transfers
from app.services.agent_service import hash_api_key
from app.services.capacity_adjustments import load_dated_availability
from app.services.identity_service import IdentityService
from tests.test_capacity_adjustments import client, headers, managed
from tests.test_review_provenance import database_engines
from tests.test_team_pm_dispatch import db_session_factory as db_session_factory  # noqa: F401

# Pi's iteration ends on the 15th; the lending projects' iterations run to the end of January.
BEFORE, START, MIDDLE, END, AFTER = date(2027, 1, 5), date(2027, 1, 6), date(2027, 1, 7), date(2027, 1, 8), date(2027, 1, 11)
SOURCES = ("Interface", "Harvester", "Dashboard")


@pytest.fixture(autouse=True)
def restore_settings_cache():
    yield
    get_settings.cache_clear()


async def shared_agent(db, profile_factory, team_member_factory):
    """One person holds a quarter of each day in Pi and in each of three lending projects."""
    profile = await profile_factory(profile_kind="human", display_name="Shared agent", assignment_modes=[])
    projects, rows = {}, {}
    for name, end in (("Pi", date(2027, 1, 15)), *((source, date(2027, 1, 29)) for source in SOURCES)):
        project = Project(name=name)
        db.add(project)
        await db.flush()
        iteration = Iteration(name=f"{name} January", start_date=date(2027, 1, 4), end_date=end,
                              calendar=Calendar(name=f"{name} 2027", year=2027), project_id=project.id)
        db.add(iteration)
        await db.flush()
        projects[name] = project
        rows[name] = await team_member_factory(profile=profile, iteration=iteration,
                                               availability_percent=25, operational_utilization=0)
    return profile, projects, rows


def lend(rows, percent=10, start=START, end=END, **extra):
    return {"target_member_id": rows["Pi"],
            "sources": [{"member_id": rows[name], "transferred_percent": percent} for name in SOURCES],
            "start_date": str(start), "end_date": str(end),
            "reason": "Approved loan of shared capacity to Pi until its release window closes", **extra}


async def percents(factory, rows, days=(BEFORE, START, MIDDLE, END, AFTER)):
    """Each row's effective percentage on each date, as every capacity calculation reads it."""
    async with factory() as read:
        from app.models.team_member import TeamMember
        members = {name: await read.get(TeamMember, member_id) for name, member_id in rows.items()}
        dated = await load_dated_availability(read, list(rows.values()))
        return {name: [dated.percent(member, day) for day in days] for name, member in members.items()}


async def revisions(factory):
    async with factory() as read:
        return {str(key): value for key, value in (await read.execute(select(Iteration.id, Iteration.revision))).all()}


@database_engines
async def test_lending_from_three_projects_to_pi_returns_after_the_window(
    db_session, db_session_factory, profile_factory, team_member_factory, actor_factory, monkeypatch
):
    db = db_session
    await managed(db, db_session_factory, monkeypatch)
    profile, projects, members = await shared_agent(db, profile_factory, team_member_factory)
    worker = await actor_factory(profile=await profile_factory())
    # Issued Pi work on the lent dates: the target gains capacity, so the work stays current.
    issued = Task(title="Pi release", iteration_id=members["Pi"].iteration_id, project_id=projects["Pi"].id,
                  assignee_id=members["Pi"].id, status="active", start_date=START, end_date=END, effort_hours=8)
    db.add(issued)
    await db.flush()
    db.add(AgentTaskAssignment(task_id=issued.id, actor_id=worker.id, state="accepted", task_version=issued.version))
    await db.commit()
    rows = {name: member.id for name, member in members.items()}
    pid, issued_id, version = profile.id, issued.id, issued.version

    assert await percents(db_session_factory, rows) == {name: [25.0] * 5 for name in rows}
    async with client() as api:
        preview = await api.post("/api/team-capacity-transfers/preview", json=lend(rows), headers=headers())
        assert preview.status_code == 200, preview.text
        body = preview.json()
        assert body["applied"] is False and body["group_token"] is None and body["returns_on"] == "2027-01-09"
        assert body["target"]["member_id"] == rows["Pi"] and body["target"]["transferred_percent"] == 30
        assert [(day["date"], day["availability_percent_before"], day["availability_percent_after"],
                 day["row_hours_before"], day["row_hours_after"]) for day in body["target"]["effective_capacity"]] == [
            (str(day), 25.0, 55.0, 2.0, 4.4) for day in (START, MIDDLE, END)]
        assert sorted(side["member_id"] for side in body["sources"]) == sorted(rows[name] for name in SOURCES)
        for side in body["sources"]:
            assert side["adjustment"]["id"] is None and side["availability_percent"] == 15
            assert [(day["availability_percent_after"], day["row_hours_after"]) for day in side["effective_capacity"]] == [(15.0, 1.2)] * 3
        # The person's total is unchanged: the lent hours move between rows.
        assert [(day["allocated_hours_before"], day["allocated_hours_after"]) for day in body["person_capacity"]] == [(8.0, 8.0)] * 3
        observed = {str(key): value for key, value in body["observed_revisions"].items()}
        assert observed == await revisions(db_session_factory) and len(observed) == 4
        async with db_session_factory() as read:
            assert await read.scalar(select(func.count()).select_from(TeamMemberCapacityAdjustment)) == 0

        stale = {**observed, str(members["Harvester"].iteration_id): observed[str(members["Harvester"].iteration_id)] + 1}
        conflict = await api.post("/api/team-capacity-transfers", json=lend(rows), headers=headers(stale))
        assert conflict.status_code == 409 and conflict.json()["detail"]["code"] == "iteration_version_conflict"
        partial = await api.post("/api/team-capacity-transfers", json=lend(rows),
                                 headers=headers({str(members["Pi"].iteration_id): observed[str(members["Pi"].iteration_id)]}))
        assert partial.status_code == 409 and partial.json()["detail"]["code"] == "planning_scope_changed"
        too_much = await api.post("/api/team-capacity-transfers", json=lend(rows, percent=30), headers=headers(observed))
        assert too_much.status_code == 409 and too_much.json()["detail"]["code"] == "capacity_transfer_out_of_range"
        late = await api.post("/api/team-capacity-transfers", json=lend(rows, end=date(2027, 1, 18)), headers=headers(observed))
        assert late.status_code == 409 and late.json()["detail"]["code"] == "capacity_adjustment_outside_iteration"

        applied = await api.post("/api/team-capacity-transfers", json=lend(rows), headers=headers(observed))
        assert applied.status_code == 200, applied.text
        result = applied.json()
        token = result["group_token"]
        assert result["applied"] and token and result["resulting_revisions"] == {key: value + 1 for key, value in observed.items()}
        assert {side["adjustment"]["group_token"] for side in [result["target"], *result["sources"]]} == {token}

        replay = await api.post("/api/team-capacity-transfers", json=lend(rows), headers=headers(observed))
        assert replay.status_code == 409 and replay.json()["detail"]["code"] == "iteration_version_conflict"
        # Before, during and after the window; the shares return on the 9th without any further command.
        assert await percents(db_session_factory, rows) == {
            "Pi": [25.0, 55.0, 55.0, 55.0, 25.0], **{name: [25.0, 15.0, 15.0, 15.0, 25.0] for name in SOURCES}}
        pi = (await api.get(f"/api/team-members/{rows['Pi']}/capacity", headers=headers())).json()
        lender = (await api.get(f"/api/team-members/{rows['Interface']}/capacity", headers=headers())).json()
        # Ten Pi working days at two hours plus three days of 2.4 more; twenty lending days less three of 0.8.
        assert pi["hours"] == pytest.approx(27.2) and lender["hours"] == pytest.approx(37.6)
        person = await api.get(f"/api/team-member-profiles/{pid}/capacity",
                               params={"start": str(BEFORE), "end": str(AFTER)}, headers=headers())
        assert {row["allocated_hours"] for row in person.json()["days"] if row["available_hours"]} == {8.0}
        record = await api.get(f"/api/team-capacity-transfers/{token}", headers=headers())
        assert record.status_code == 200, record.text
        assert record.json()["active"] and record.json()["target"]["availability_percent"] == 55
        assert len(record.json()["sources"]) == 3

        # One side cannot be withdrawn alone, and its row cannot be removed while the transfer is unfinished.
        context = (await api.get(f"/api/tasks/planning-inputs/member/{rows['Interface']}/context", headers=headers())).json()
        [side] = context["resource"]["capacity_adjustments"]
        alone = await api.post(f"/api/team-members/{rows['Interface']}/capacity-adjustments",
                               headers=headers(context["expected_revisions"]),
                               json={"withdraw_adjustment_ids": [side["id"]], "reason": "Return only this one"})
        assert alone.status_code == 409 and alone.json()["detail"]["code"] == "capacity_transfer_side"
        removed = await api.delete(f"/api/team-members/{rows['Interface']}", headers=headers(context["expected_revisions"]))
        assert removed.status_code == 409 and removed.json()["detail"]["code"] == "capacity_transfer_active"
        overlap = await api.post("/api/team-capacity-transfers", json=lend(rows, percent=5, start=END, end=AFTER),
                                 headers=headers(context["expected_revisions"]))
        assert overlap.status_code == 409 and overlap.json()["detail"]["code"] == "capacity_adjustment_overlap"

        reason = {"reason": "Pi finished early; return the capacity"}
        # Returning the capacity would shrink Pi's row under its issued work, so it waits until that work is done.
        busy = await api.post(f"/api/team-capacity-transfers/{token}/withdraw", json=reason,
                              headers=headers(await revisions(db_session_factory)))
        assert busy.status_code == 409 and busy.json()["detail"]["code"] == "capacity_adjustment_in_use"
        async with db_session_factory() as write:
            await write.execute(update(Task).where(Task.id == issued_id).values(status="closed"))
            await write.commit()
        current = await revisions(db_session_factory)
        back = await api.post(f"/api/team-capacity-transfers/{token}/withdraw/preview", json=reason, headers=headers())
        assert back.status_code == 200, back.text
        assert back.json()["applied"] is False and back.json()["restored_from"] == str(START)
        assert [day["availability_percent_after"] for day in back.json()["target"]["effective_capacity"]] == [25.0] * 3
        assert await percents(db_session_factory, rows) != {name: [25.0] * 5 for name in rows}
        withdrawn = await api.post(f"/api/team-capacity-transfers/{token}/withdraw", json=reason, headers=headers(current))
        assert withdrawn.status_code == 200, withdrawn.text
        assert withdrawn.json()["withdrawal_group_token"] and all(
            side["retained"] is None for side in [withdrawn.json()["target"], *withdrawn.json()["sources"]])
        assert await percents(db_session_factory, rows) == {name: [25.0] * 5 for name in rows}
        again = await api.post(f"/api/team-capacity-transfers/{token}/withdraw", json=reason,
                               headers=headers(await revisions(db_session_factory)))
        assert again.status_code == 409 and again.json()["detail"]["code"] == "capacity_transfer_unavailable"
        history = (await api.get(f"/api/team-capacity-transfers/{token}", headers=headers())).json()
        assert history["active"] is False and history["withdrawal_reason"] == reason["reason"]
        assert history["withdrawn_group_token"] == withdrawn.json()["withdrawal_group_token"]

    async with db_session_factory() as read:
        task = await read.get(Task, issued_id)
        assignment = await read.scalar(select(AgentTaskAssignment).where(AgentTaskAssignment.task_id == issued_id))
        assert (task.version, task.assignee_id, assignment.state, assignment.task_version) == (version, rows["Pi"], "accepted", version)
        adjustments = (await read.scalars(select(TeamMemberCapacityAdjustment))).all()
        assert len(adjustments) == 4 and {row.group_token for row in adjustments} == {token}
        assert {row.withdrawn_group_token for row in adjustments} == {withdrawn.json()["withdrawal_group_token"]}
        audits = (await read.scalars(select(CommandAudit).where(CommandAudit.action.in_([
            capacity_transfers.TRANSFER_AUDIT_ACTION, capacity_transfers.WITHDRAWAL_AUDIT_ACTION])).order_by(CommandAudit.id))).all()
        assert [(row.action, row.details["role"]) for row in audits].count((capacity_transfers.TRANSFER_AUDIT_ACTION, "source")) == 3
        assert {row.details["group_token"] for row in audits} == {token}
        assert {row.project_id for row in audits} == {project.id for project in projects.values()}
        # Each side's entry names only its own row.
        assert all(row.details["member_id"] in rows.values() and "sources" not in row.details for row in audits)


@database_engines
async def test_lending_under_issued_work_is_refused_and_withdrawing_under_target_work_too(
    db_session, db_session_factory, profile_factory, team_member_factory, actor_factory, monkeypatch
):
    db = db_session
    await managed(db, db_session_factory, monkeypatch)
    _, projects, members = await shared_agent(db, profile_factory, team_member_factory)
    worker = await actor_factory(profile=await profile_factory())
    lender = Task(title="Harvester fix", iteration_id=members["Harvester"].iteration_id, project_id=projects["Harvester"].id,
                  assignee_id=members["Harvester"].id, status="planned", start_date=MIDDLE, end_date=MIDDLE, effort_hours=2)
    db.add(lender)
    await db.flush()
    lent_assignment = AgentTaskAssignment(task_id=lender.id, actor_id=worker.id, state="queued", task_version=lender.version)
    db.add(lent_assignment)
    await db.commit()
    rows = {name: member.id for name, member in members.items()}
    lender_id, lender_version = lender.id, lender.version
    async with client() as api:
        observed = await revisions(db_session_factory)
        refused = await api.post("/api/team-capacity-transfers", json=lend(rows), headers=headers(observed))
        assert refused.status_code == 409 and refused.json()["detail"]["code"] == "capacity_adjustment_in_use"
        assert f"{lender_id} (" in refused.json()["detail"]["message"]
        preview = await api.post("/api/team-capacity-transfers/preview", json=lend(rows), headers=headers())
        assert preview.status_code == 409 and preview.json()["detail"]["code"] == "capacity_adjustment_in_use"
        assert await revisions(db_session_factory) == observed

        # Without the Harvester row, the remaining two lend; then Pi work is issued on the lent dates.
        two = {**lend(rows), "sources": [{"member_id": rows[name], "transferred_percent": 10} for name in ("Interface", "Dashboard")]}
        applied = await api.post("/api/team-capacity-transfers", json=two, headers=headers(observed))
        assert applied.status_code == 200, applied.text
        token = applied.json()["group_token"]
        async with db_session_factory() as write:
            target = Task(title="Pi release", iteration_id=members["Pi"].iteration_id, project_id=projects["Pi"].id,
                          assignee_id=rows["Pi"], status="planned", start_date=END, end_date=END, effort_hours=4)
            write.add(target)
            await write.flush()
            write.add(AgentTaskAssignment(task_id=target.id, actor_id=worker.id, state="queued", task_version=target.version))
            await write.commit()
            target_id, target_version = target.id, target.version
        back = await api.post(f"/api/team-capacity-transfers/{token}/withdraw", json={"reason": "Return it"},
                              headers=headers(await revisions(db_session_factory)))
        assert back.status_code == 409 and back.json()["detail"]["code"] == "capacity_adjustment_in_use"
        assert f"{target_id} (" in back.json()["detail"]["message"]
    async with db_session_factory() as read:
        assert (await read.get(Task, lender_id)).version == lender_version
        assert (await read.get(Task, target_id)).version == target_version
        assert {row.state for row in (await read.scalars(select(AgentTaskAssignment))).all()} == {"queued"}
        active = (await read.scalars(select(TeamMemberCapacityAdjustment).where(
            TeamMemberCapacityAdjustment.withdrawn_at.is_(None)))).all()
        assert len(active) == 3 and {row.team_member_id for row in active} == {rows["Pi"], rows["Interface"], rows["Dashboard"]}


@database_engines
async def test_returning_a_started_transfer_keeps_its_elapsed_dates(
    db_session, db_session_factory, profile_factory, team_member_factory, monkeypatch
):
    db = db_session
    await managed(db, db_session_factory, monkeypatch)
    _, _, members = await shared_agent(db, profile_factory, team_member_factory)
    await db.commit()
    rows = {name: member.id for name, member in members.items()}
    async with client() as api:
        applied = await api.post("/api/team-capacity-transfers", json=lend(rows), headers=headers(await revisions(db_session_factory)))
        assert applied.status_code == 200, applied.text
        token = applied.json()["group_token"]

        monkeypatch.setattr(capacity_transfers, "working_today", lambda zone=None: MIDDLE)
        past = await api.post("/api/team-capacity-transfers/preview", json=lend(rows, start=BEFORE, end=BEFORE), headers=headers())
        assert past.status_code == 409 and past.json()["detail"]["code"] == "capacity_transfer_in_past"
        back = await api.post(f"/api/team-capacity-transfers/{token}/withdraw", json={"reason": "Return the rest early"},
                              headers=headers(await revisions(db_session_factory)))
        assert back.status_code == 200, back.text
        result = back.json()
        assert result["restored_from"] == str(MIDDLE)
        kept = result["withdrawal_group_token"]
        for side in [result["target"], *result["sources"]]:
            assert (side["retained"]["start_date"], side["retained"]["end_date"], side["retained"]["group_token"]) == (
                str(START), str(START), kept)
        assert await percents(db_session_factory, rows) == {
            "Pi": [25.0, 55.0, 25.0, 25.0, 25.0], **{name: [25.0, 15.0, 25.0, 25.0, 25.0] for name in SOURCES}}
        # The elapsed day is itself recorded as a transfer, and it can no longer be withdrawn.
        assert (await api.get(f"/api/team-capacity-transfers/{kept}", headers=headers())).json()["active"] is True
        ended = await api.post(f"/api/team-capacity-transfers/{kept}/withdraw", json={"reason": "Rewrite history"},
                               headers=headers(await revisions(db_session_factory)))
        assert ended.status_code == 409 and ended.json()["detail"]["code"] == "capacity_transfer_ended"
        context = (await api.get(f"/api/tasks/planning-inputs/member/{rows['Interface']}/context", headers=headers())).json()
        removed = await api.delete(f"/api/team-members/{rows['Interface']}", headers=headers(context["expected_revisions"]))
        assert removed.status_code == 200, removed.text


@database_engines
async def test_transfer_needs_edit_access_to_every_row_and_does_not_reveal_others(
    db_session, db_session_factory, profile_factory, team_member_factory, monkeypatch
):
    from tests.test_iteration_date_move import human

    db = db_session
    monkeypatch.setenv("CORS_ORIGINS", json.dumps(["https://test"]))
    await managed(db, db_session_factory, monkeypatch)
    _, projects, members = await shared_agent(db, profile_factory, team_member_factory)
    other = await profile_factory(profile_kind="human", display_name="Someone else", assignment_modes=[])
    stranger = await team_member_factory(profile=other, iteration=await db.get(Iteration, members["Pi"].iteration_id),
                                         availability_percent=50, operational_utilization=0)
    await db.commit()
    rows = {name: member.id for name, member in members.items()}
    stranger_id = stranger.id
    pi_manager = await human(db, {projects["Pi"].id: "manager"})
    viewer_elsewhere = await human(db, {projects["Pi"].id: "manager", **{projects[name].id: "viewer" for name in SOURCES}})
    async with client() as api:
        observed = await revisions(db_session_factory)
        mismatch = await api.post("/api/team-capacity-transfers/preview", headers=headers(), json={
            **lend(rows), "sources": [{"member_id": stranger_id, "transferred_percent": 10}]})
        assert mismatch.status_code == 409 and mismatch.json()["detail"]["code"] == "capacity_transfer_profile_mismatch"
        applied = await api.post("/api/team-capacity-transfers", json=lend(rows), headers=headers(observed))
        assert applied.status_code == 200, applied.text
        token = applied.json()["group_token"]
    revision_header = {"X-Expected-Revisions": json.dumps(await revisions(db_session_factory))}
    for factory in (pi_manager, viewer_elsewhere):
        async with factory() as api:
            for response in (
                await api.post("/api/team-capacity-transfers/preview", json=lend(rows, start=AFTER, end=AFTER)),
                await api.post("/api/team-capacity-transfers", json=lend(rows, start=AFTER, end=AFTER), headers=revision_header),
                await api.post(f"/api/team-capacity-transfers/{token}/withdraw/preview", json={"reason": "Take it back"}),
                await api.post(f"/api/team-capacity-transfers/{token}/withdraw", json={"reason": "Take it back"},
                               headers=revision_header),
            ):
                assert response.status_code in {403, 404}, response.text
                assert "availability_percent" not in response.text
        async with factory() as api:
            record = await api.get(f"/api/team-capacity-transfers/{token}")
            if factory is pi_manager:
                assert record.status_code == 404 and "availability_percent" not in record.text
            else:
                assert record.status_code == 200, record.text
    async with db_session_factory() as read:
        assert await read.scalar(select(func.count()).select_from(TeamMemberCapacityAdjustment).where(
            TeamMemberCapacityAdjustment.withdrawn_at.is_(None))) == 4
        assert {str(key): value for key, value in (await read.execute(select(Iteration.id, Iteration.revision))).all()} == json.loads(
            revision_header["X-Expected-Revisions"])


@database_engines
async def test_mcp_tools_preview_apply_and_withdraw_a_transfer(
    db_session, db_session_factory, profile_factory, team_member_factory, actor_factory, monkeypatch
):
    db = db_session
    await managed(db, db_session_factory, monkeypatch)
    monkeypatch.setattr(mcp_server, "_session_factory", db_session_factory)
    _, projects, members = await shared_agent(db, profile_factory, team_member_factory)
    pm = await actor_factory(role="pm", scopes=json.dumps(["team:write", "team:read", "planning:read"]),
                             api_key_hash=hash_api_key("capacity-transfer-pm"))
    identity = await IdentityService(db).actor_context(pm)
    db.add(WorkspaceMembership(principal_id=identity.principal_id, role="member"))
    db.add_all([ProjectMembership(project_id=project.id, principal_id=identity.principal_id, role="manager")
                for project in projects.values()])
    await db.commit()
    rows = {name: member.id for name, member in members.items()}
    server = mcp_server.create_mcp_server()
    application = mcp_server.MCPAgentKeyMiddleware(server.streamable_http_app())
    async with server.session_manager.run(), httpx.AsyncClient(
        transport=httpx.ASGITransport(app=application), base_url="http://localhost:8001"
    ) as api:
        async def call(name, arguments, *, error=False):
            response = await api.post("/", headers={"X-Agent-API-Key": "capacity-transfer-pm",
                                                     "Accept": "application/json, text/event-stream"},
                                      json={"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                                            "params": {"name": name, "arguments": arguments}})
            assert response.status_code == 200, response.text
            result = response.json()["result"]
            assert result["isError"] is error, result
            return result["content"][0]["text"] if error else json.loads(result["content"][0]["text"])

        preview = await call("agent_preview_capacity_transfer", {"payload": lend(rows)})
        assert preview["applied"] is False and preview["target"]["effective_capacity"][0]["availability_percent_after"] == 55
        observed = {str(key): value for key, value in preview["observed_revisions"].items()}
        stale = await call("agent_apply_capacity_transfer", {
            "payload": lend(rows, expected_revisions={**observed, str(members["Dashboard"].iteration_id): 99}),
            "idempotency_key": "lend-stale", "rationale": "Lend", "correlation_id": "lend-stale"}, error=True)
        assert "iteration_version_conflict" in stale
        command = {"payload": lend(rows, expected_revisions=observed), "idempotency_key": "lend-to-pi",
                   "rationale": "Approved loan to Pi", "correlation_id": "lend-to-pi"}
        receipt = await call("agent_apply_capacity_transfer", command)
        again = await call("agent_apply_capacity_transfer", command)
        assert receipt == again and receipt["operation"] == "planning.capacity_transfer.apply"
        assert receipt["target_id"] == rows["Pi"] and receipt["result"]["applied"]
        token = receipt["result"]["group_token"]
        back = await call("agent_preview_capacity_transfer_withdrawal", {"group_token": token, "payload": {"reason": "Return"}})
        assert back["applied"] is False and back["group_token"] == token
        current = await revisions(db_session_factory)
        withdrawn = await call("agent_withdraw_capacity_transfer", {
            "group_token": token, "payload": {"reason": "Return", "expected_revisions": current},
            "idempotency_key": "return-to-lenders", "rationale": "Pi no longer needs it", "correlation_id": "return-to-lenders"})
        assert withdrawn["operation"] == "planning.capacity_transfer.withdraw" and withdrawn["result"]["applied"]
    assert await percents(db_session_factory, rows) == {name: [25.0] * 5 for name in rows}
    async with db_session_factory() as read:
        adjustments = (await read.scalars(select(TeamMemberCapacityAdjustment))).all()
        assert len(adjustments) == 4 and all(row.withdrawn_at is not None for row in adjustments)
        assert {row.created_by_principal_id for row in adjustments} == {identity.principal_id}
