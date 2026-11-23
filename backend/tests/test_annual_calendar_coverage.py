from datetime import date, timedelta
from types import SimpleNamespace

import httpx
import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.commands import PlanningConflict
from app.authority import Authority, AuthorityError
from app.database import get_db
from app.main import app
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.identity import Principal
from app.models.agent import AgentTaskAssignment
from app.models.task import Task
from app.models.team_member import TeamMember, TeamMemberProfile, Vacation
from app.models.capacity import ProfileAbsence, ProfileAvailability
from app.schemas.calendar import CalendarCreate, CalendarUpdate
from app.schemas.iteration import IterationUpdate
from app.services.calendar_service import CalendarService
from app.services.agent_routing_service import AgentRoutingService
from app.services.calendar_rules import AnnualCalendars, YearRules
from app.services.capacity_service import CapacityService, PeriodCommitments, day_hours
from app.services.iteration_service import IterationService
from app.services.planning_input_context import observe_planning_input
from app.services.scheduler_service import SchedulerService
from app.services.snapshot_service import SnapshotService
from app.services.team_service import TeamService
from tests import test_profile_capacity

db_session = test_profile_capacity.db_session


async def calendars(db):
    service = CalendarService(db)
    first = await service.create(
        CalendarCreate(
            name="Early policy",
            year=2026,
            holidays=["2026-12-31"],
            weekend_days=[5, 6],
            short_days=["2026-12-30"],
            nominal_day_hours=8,
        )
    )
    second = await service.create(
        CalendarCreate(
            name="Later policy",
            year=2027,
            holidays=["2027-01-03"],
            weekend_days=[4, 5],
            short_days=["2027-01-04"],
            nominal_day_hours=6,
        )
    )
    return first, second


async def test_explicit_iteration_coverage_is_scoped_and_date_correct(db_session):
    db_session_factory = async_sessionmaker(db_session.bind, expire_on_commit=False)

    async def database_override():
        async with db_session_factory() as db:
            yield db

    original = app.dependency_overrides.get(get_db)
    app.dependency_overrides[get_db] = database_override
    try:
        async with db_session_factory() as db:
            first, second = await calendars(db)
            primary, extension = first.id, second.id
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            body = {
                "name": "Winter interval",
                "calendar_id": primary,
                "start_date": "2026-12-29",
                "end_date": "2027-01-05",
            }
            held = (await client.post("/api/iterations", json=body)).raise_for_status().json()
            ready = (
                (
                    await client.post(
                        "/api/iterations", json={**body, "additional_calendar_ids": [extension]}
                    )
                )
                .raise_for_status()
                .json()
            )
            assert (held["working_days"], held["missing_calendar_years"]) == (2, [2027])
            assert (
                ready["working_days"],
                ready["additional_calendar_ids"],
                ready["missing_calendar_years"],
            ) == (4, [extension], [])
            for iteration, missing in ((held, [2027]), (ready, [])):
                status = (
                    (await client.get(f"/api/iterations/{iteration['id']}/planning-readiness"))
                    .raise_for_status()
                    .json()
                )
                assert status["missing_calendar_years"] == missing
                assert status["checkpoints"][0]["state"] == ("warn" if missing else "done")
            projected = (
                (
                    await client.get(
                        f"/api/calendars/{primary}/working-days",
                        params={
                            "start_date": body["start_date"],
                            "end_date": body["end_date"],
                            "additional_calendar_ids": extension,
                        },
                    )
                )
                .raise_for_status()
                .json()
            )
            assert projected["total_days"] == 8 and projected["working_days"] == 4
            assert projected["holidays"] == ["2026-12-31", "2027-01-03"] and projected["weekends"] == [
                "2027-01-01",
                "2027-01-02",
            ]
            invalid = await client.post(
                "/api/iterations", json={**body, "additional_calendar_ids": [primary, extension]}
            )
            assert invalid.status_code == 400
            assert (await client.get(f"/api/iterations/{held['id']}")).json()["missing_calendar_years"] == [
                2027
            ]
    finally:
        if original is None:
            app.dependency_overrides.pop(get_db, None)
        else:
            app.dependency_overrides[get_db] = original


async def test_capacity_scheduler_and_profile_owner_use_each_selected_day(db_session):
    first, second = await calendars(db_session)
    iteration = Iteration(
        name="Year boundary",
        start_date=date(2026, 12, 29),
        end_date=date(2027, 1, 5),
        calendar=first,
        additional_calendars=[second],
    )
    profile = TeamMemberProfile(display_name="Calendar owner")
    member = TeamMember(
        name="Calendar owner",
        position="Developer",
        profile=profile,
        iteration=iteration,
        availability_percent=100,
        operational_utilization=0,
        professionalism_coefficient=1,
    )
    db_session.add(member)
    await db_session.commit()
    capacity = CapacityService(db_session)
    row = await TeamService(db_session).calculate_capacity(member.id)
    assert (row.working_days, row.hours, row.missing_calendar_years) == (4, 26, [])
    projection = await capacity.projection(profile.id, iteration.start_date, iteration.end_date)
    assert [d["available_hours"] for d in projection["days"]] == [8, 7, 0, 0, 0, 0, 5, 6]
    assert not projection["outside_calendar_year"]
    schedules = await SchedulerService(db_session)._build_member_schedules(iteration, [member])
    assert schedules[member.id].allocate(date(2026, 12, 30), 2, 1, required_hours=12) == (
        date(2026, 12, 30),
        date(2027, 1, 4),
    )
    assert not await capacity.schedule_issues(iteration, [member])

    # An explicit personal calendar cannot borrow another owner's additional year.
    selected = await capacity.set_calendar(profile.id, first.id, 0)
    assert selected["additional_calendar_ids"] == []
    missing = await capacity.projection(profile.id, iteration.start_date, iteration.end_date)
    assert missing["missing_calendar_years"] == [2027] and missing["days"][-1]["available_hours"] is None
    assert missing["days"][-1]["allocated_hours"] is None
    assert "calendar_reconciliation_required" in {
        item["code"] for item in await capacity.schedule_issues(iteration, [member])
    }
    selected = await capacity.set_calendar(profile.id, first.id, selected["version"], [second.id])
    assert selected["additional_calendar_ids"] == [second.id]
    assert (await capacity.projection(profile.id, iteration.start_date, iteration.end_date))["days"][-1][
        "available_hours"
    ] == 6


async def test_invalid_annual_bindings_and_reverse_dependencies(db_session):
    primary, extension = await calendars(db_session)
    svc = CalendarService(db_session)
    other = await svc.create(CalendarCreate(name="Other annual", year=2027))
    other_zone = await svc.create(CalendarCreate(name="Other zone", year=2028, timezone="Europe/Madrid"))
    for ids in ([extension.id, other.id], [extension.id, extension.id], [900000], [other_zone.id]):
        with pytest.raises(ValueError):
            await svc.selected_years(primary, ids)
    iteration = Iteration(
        name="Planned",
        start_date=date(2026, 12, 29),
        end_date=date(2027, 1, 5),
        calendar=primary,
        additional_calendars=[extension],
    )
    db_session.add(iteration)
    await db_session.commit()
    iteration_id = iteration.id
    ext_id = extension.id
    with pytest.raises((PlanningConflict, ValueError), match="annual"):
        await svc.delete(ext_id)
    with pytest.raises(ValueError, match="annual"):
        await svc.update(ext_id, CalendarUpdate(year=2028))
    row = await IterationService(db_session).get_by_id(iteration_id)
    prior = row.revision
    await svc.update(ext_id, CalendarUpdate(short_days=["2027-01-05"]))
    row = await IterationService(db_session).get_by_id(iteration_id)
    assert row.revision > prior
    await IterationService(db_session).update(iteration_id, IterationUpdate(additional_calendar_ids=[]))
    assert (
        await IterationService(db_session).get_planning_readiness_summary(iteration_id)
    ).missing_calendar_years == [2027]


async def test_interior_year_and_snapshot_use_the_explicit_owner(db_session, monkeypatch):
    first, middle = await calendars(db_session)
    late = await CalendarService(db_session).create(CalendarCreate(name="Last policy", year=2028))
    iteration = Iteration(
        name="Extended work",
        start_date=date(2026, 12, 29),
        end_date=date(2028, 1, 3),
        calendar=first,
        additional_calendars=[late],
    )
    person = TeamMemberProfile(display_name="Extended work owner")
    member = TeamMember(
        name="Owner",
        position="Developer",
        profile=person,
        iteration=iteration,
        availability_percent=100,
        operational_utilization=0,
        professionalism_coefficient=1,
    )
    db_session.add(member)
    await db_session.commit()
    service = IterationService(db_session)
    transfer = SnapshotService(db_session)
    saved = await transfer.create_snapshot(iteration.id, "annual-policy")
    assert (await transfer.get_snapshot(iteration.id, saved))["iteration"]["additional_calendar_ids"] == [
        late.id
    ]
    assert (await service.get_planning_readiness_summary(iteration.id)).missing_calendar_years == [2027]
    assert {
        item["code"] for item in await CapacityService(db_session).schedule_issues(iteration, [member])
    } == {"calendar_outside_year", "calendar_reconciliation_required"}
    await service.update(iteration.id, IterationUpdate(additional_calendar_ids=[middle.id, late.id]))
    capacity = CapacityService(db_session)
    queries = []
    calculate = capacity._projection

    async def observed(profile_id, start, end):
        queries.append((profile_id, start, end))
        return await calculate(profile_id, start, end)

    monkeypatch.setattr(capacity, "_projection", observed)
    assert not await capacity.schedule_issues(iteration, [member])
    assert queries == [(person.id, iteration.start_date, iteration.end_date)]
    with pytest.raises(PlanningConflict, match="366 days"):
        await capacity.projection(person.id, iteration.start_date, iteration.end_date)
    context = await observe_planning_input(db_session, "iteration", iteration.id)
    assert context["resource"]["additional_calendar_ids"] == sorted([middle.id, late.id])
    await transfer.restore(iteration.id, saved)
    restored = await service.get_by_id(iteration.id)
    assert [policy.id for policy in restored.additional_calendars] == [late.id]
    assert (await service.get_planning_readiness_summary(iteration.id)).missing_calendar_years == [2027]


async def test_replacing_issued_annual_rules_is_scoped_to_the_affected_tasks(db_session, actor_factory):
    first, second = await calendars(db_session)
    alternative = await CalendarService(db_session).create(
        CalendarCreate(name="Alternative policy", year=2027)
    )
    iteration = Iteration(
        name="Concurrent work",
        start_date=date(2026, 12, 16),
        end_date=date(2027, 1, 5),
        calendar=first,
        additional_calendars=[second],
    )
    affected, unaffected = [
        Task(
            title=f"Check notes {day}", iteration=iteration, status="planned", start_date=day, end_date=day
        )
        for day in (date(2027, 1, 4), date(2026, 12, 18))
    ]
    worker = await actor_factory()
    profile = TeamMemberProfile(display_name="Person with a reserved task")
    member = TeamMember(
        name="Reserved capacity", position="Developer", profile=profile, iteration=iteration
    )
    affected.assignee = member
    db_session.add_all([affected, unaffected])
    await db_session.flush()
    assignments = [
        AgentTaskAssignment(
            task_id=task.id,
            actor_id=worker.id,
            purpose="execution",
            task_version=task.version,
            state="queued",
        )
        for task in (affected, unaffected)
    ]
    db_session.add_all(assignments)
    await db_session.commit()
    period, primary, original_year, alternate, profile_id = (
        iteration.id,
        first.id,
        second.id,
        alternative.id,
        profile.id,
    )
    before = [
        (task.id, task.version, assignment.id)
        for task, assignment in zip((affected, unaffected), assignments)
    ]
    with pytest.raises(PlanningConflict, match="issued work") as caught:
        await IterationService(db_session).update(period, IterationUpdate(additional_calendar_ids=[]))
    assert caught.value.code == "annual_calendar_change_in_use"
    actual, untouched = before
    assert f"{actual[0]} ({actual[2]})" in str(caught.value)
    assert f"{untouched[0]} ({untouched[2]})" not in str(caught.value)
    assert [
        row.id for row in (await IterationService(db_session).get_by_id(period)).additional_calendars
    ] == [original_year]
    capacity = CapacityService(db_session)
    with pytest.raises(PlanningConflict) as private:
        await capacity.set_calendar(profile_id, primary, 0, [alternate])
    assert private.value.code == "annual_calendar_change_in_use"
    assert f"{actual[0]} ({actual[2]})" not in str(private.value)
    assert (await capacity.detail(profile_id))["version"] == 0
    # Becoming the explicit primary owner is a substantive planning reservation,
    # even if the currently inherited annual rules happen to match.
    with pytest.raises(PlanningConflict, match="primary calendar"):
        await capacity.set_calendar(profile_id, primary, 0, [original_year])
    for task_id, version, assignment_id in before:
        assert (await db_session.get(Task, task_id)).version == version
        assert (await db_session.get(AgentTaskAssignment, assignment_id)).state == "queued"


@pytest.mark.parametrize("include_years", [False, True])
async def test_person_primary_change_preserves_the_ordinary_reservation(
    db_session, actor_factory, include_years
):
    first, second = await calendars(db_session)
    other = await CalendarService(db_session).create(CalendarCreate(name="Different primary", year=2026))
    person = TeamMemberProfile(display_name="Policy owner")
    iteration = Iteration(
        name="Two-year allocation",
        calendar=first,
        additional_calendars=[second],
        start_date=date(2026, 12, 29),
        end_date=date(2027, 1, 5),
    )
    member = TeamMember(name="Writer", position="Developer", profile=person, iteration=iteration)
    task = Task(
        title="Prepare handoff",
        assignee=member,
        iteration=iteration,
        start_date=date(2026, 12, 30),
        end_date=date(2026, 12, 30),
        status="planned",
    )
    actor = await actor_factory()
    db_session.add(task)
    await db_session.flush()
    capacity = CapacityService(db_session)
    selected = await capacity.set_calendar(person.id, first.id, 0, [second.id])
    before, profile, prior, alternate, extra, task_id = (
        task.version,
        person.id,
        first.id,
        other.id,
        second.id,
        task.id,
    )
    assignment = AgentTaskAssignment(
        task_id=task.id, actor_id=actor.id, purpose="execution", state="queued", task_version=task.version
    )
    db_session.add(assignment)
    await db_session.commit()
    assignment_id = assignment.id
    years = [extra] if include_years else None
    with pytest.raises(PlanningConflict) as held:
        await capacity.set_calendar(profile, alternate, selected["version"], years)
    assert held.value.code == "annual_calendar_change_in_use"
    assert (await capacity.detail(profile))["calendar_id"] == prior
    assert (await db_session.get(Task, task_id)).version == before
    held_assignment = await db_session.get(AgentTaskAssignment, assignment_id)
    assert held_assignment.state == "queued" and held_assignment.task_version == before
    held_assignment.state = "fulfilled"
    await db_session.commit()
    changed = await capacity.set_calendar(profile, alternate, selected["version"], years)
    assert changed["calendar_id"] == alternate and changed["additional_calendar_ids"] == [extra]
    assert (await db_session.get(Task, task_id)).version == before + 1


async def test_hidden_person_protects_shared_master_without_leaking_their_identity(db_session):
    first, second = await calendars(db_session)
    visible = await CalendarService(db_session).create(
        CalendarCreate(name="Unreferenced shared policy", year=2028)
    )
    owner = TeamMemberProfile(display_name="Private person")
    db_session.add(owner)
    await db_session.flush()
    db_session.add(
        ProfileAvailability(profile_id=owner.id, calendar_id=first.id, additional_calendars=[second])
    )
    await db_session.commit()
    public_id, private_owner, free_id = second.id, owner.id, visible.id
    scoped = Authority(principal_id=None, kind="human", workspace_role="member")
    db_session.info["authority"] = scoped
    assert await db_session.get(ProfileAvailability, private_owner, populate_existing=True) is None
    svc = CalendarService(db_session)
    assert await svc._in_annual_selection(public_id) is True
    assert await svc._in_annual_selection(free_id) is False
    with pytest.raises(AuthorityError):
        await svc.update(public_id, CalendarUpdate(year=2028))
    assert db_session.info["authority"] == scoped and not db_session.info.get("authority_internal")
    db_session.info.pop("authority")
    with pytest.raises(ValueError, match="annual"):
        await svc.update(public_id, CalendarUpdate(year=2028))
    assert (await svc.get_by_id(public_id)).year == 2027


async def test_routing_preserves_single_year_ratios_and_uses_each_annual_nominal(db_session):
    first, second = await calendars(db_session)
    iteration = Iteration(
        name="Routing days", calendar=first, start_date=date(2026, 12, 28), end_date=date(2026, 12, 31)
    )
    person = TeamMemberProfile(display_name="Available writer")
    member = TeamMember(
        name="Writer",
        position="Developer",
        iteration=iteration,
        profile=person,
        availability_percent=100,
        operational_utilization=0,
        professionalism_coefficient=1,
    )
    task = Task(
        title="Estimate the example",
        iteration=iteration,
        assignee=member,
        effort_days=2,
        effort_hours=16,
        start_date=date(2026, 12, 28),
        end_date=date(2026, 12, 28),
    )
    db_session.add(task)
    await db_session.flush()
    db_session.add_all(
        [
            Vacation(team_member_id=member.id, start_date=date(2026, 12, 29), end_date=date(2026, 12, 29)),
            ProfileAbsence(
                profile_id=person.id, start_date=date(2026, 12, 28), end_date=date(2026, 12, 28)
            ),
        ]
    )
    await db_session.commit()
    member = await TeamService(db_session).get_by_id(member.id)
    iteration = await IterationService(db_session).get_by_id(iteration.id)

    async def result():
        return (
            await AgentRoutingService(db_session)._capacity_inputs(
                task=task, iteration=iteration, members=[member]
            )
        )[member.id]

    single = await result()
    assert (single["available_capacity_days"], single["workload_ratio"], single["vacation_conflict"]) == (
        2,
        1,
        False,
    )
    assert "annual_calendar_basis" not in single and "missing_calendar_years" not in single
    iteration.end_date = date(2027, 1, 5)
    iteration.additional_calendars = [second]
    await db_session.commit()
    cross = await result()
    expected = 7 / 8 + 5 / 6 + 1
    assert (cross["available_capacity_days"], cross["workload_ratio"]) == (
        round(expected, 2),
        round(2 / expected, 4),
    )
    assert (
        cross["vacation_conflict"]
        and not cross["missing_calendar_years"]
        and len(cross["annual_calendar_basis"]) == 64
    )
    second.nominal_day_hours = 0
    await db_session.flush()
    invalid = await result()
    assert invalid["missing_calendar_years"] == [2027] and invalid["workload_ratio"] is None


async def test_repeated_long_commitments_are_indexed_by_owner_and_year(
    db_session, monkeypatch, record_property
):
    first, second = await calendars(db_session)
    policy = AnnualCalendars(first, [second])
    owner = SimpleNamespace(
        id=1, availability_percent=100, operational_utilization=0, professionalism_coefficient=1
    )
    tasks = [
        SimpleNamespace(
            assignee_id=1,
            baseline_start_date=date(2026, 1, 1),
            baseline_end_date=date(2027, 12, 31),
            effort_hours=12,
        )
        for _ in range(100)
    ]
    calls = 0
    hours = YearRules.hours

    def count(self, day):
        nonlocal calls
        calls += 1
        return hours(self, day)

    monkeypatch.setattr(YearRules, "hours", count)
    commitments = PeriodCommitments(tasks, [owner], {1: policy}, date(2026, 12, 30), date(2027, 1, 5))
    before = calls
    assert before == 730
    total_hours, _ = policy.period_totals(date(2026, 1, 1), date(2027, 12, 31))
    assert calls == before
    for offset, h in enumerate([7, 0, 0, 0, 0, 5, 6]):
        day = date(2026, 12, 30) + timedelta(days=offset)
        value, unknown = commitments.for_day(day)
        assert value == pytest.approx(1200 * h / total_hours) and not unknown
    assert calls == before + 7 and len(commitments.events) == 1
    record_property("dated_baselines", len(tasks))
    record_property("year_index_day_lookups", before)
    record_property("report_day_lookups", calls - before)
    record_property("event_dates", len(commitments.events))


def test_registered_iteration_summary_retains_its_schema_description():
    from app.schemas.iteration import IterationSummary

    assert IterationSummary.__doc__ == "Summary statistics for an iteration."
    schema = app.openapi()["components"]["schemas"]["IterationSummary"]
    assert (
        schema["description"] == IterationSummary.__doc__
        and "missing_calendar_years" in schema["properties"]
    )


@pytest.mark.parametrize("case", ["leaf_overflow", "active_prior_year"])
async def test_uncovered_forecast_restores_every_task_and_issued_fence(
    db_session, actor_factory, monkeypatch, case
):
    monkeypatch.setattr("app.services.work_metrics.working_today", lambda *_a, **_k: date(2026, 12, 28))
    primary, _ = await calendars(db_session)
    iteration = Iteration(
        name="Covered period", calendar=primary, start_date=date(2026, 12, 28), end_date=date(2026, 12, 31)
    )
    owner = TeamMemberProfile(display_name="Single-year owner")
    member = TeamMember(
        name="Writer",
        position="Developer",
        profile=owner,
        iteration=iteration,
        availability_percent=100,
        operational_utilization=0,
        professionalism_coefficient=1,
    )
    first = Task(
        iteration=iteration,
        assignee=member,
        title="Retain this estimate",
        status="planned",
        priority=1,
        effort_hours=8 if case == "leaf_overflow" else None,
        effort_days=1,
        start_date=date(2026, 12, 29),
        end_date=date(2026, 12, 29),
        calculated_effort_days=1.25,
    )
    second = Task(
        iteration=iteration,
        assignee=member,
        title="Schedule this example",
        priority=2,
        effort_hours=8,
        effort_days=1,
        start_date=date(2026, 12, 30),
        end_date=date(2026, 12, 30),
        calculated_effort_days=2.5,
        status="planned" if case == "leaf_overflow" else "active",
    )
    if case == "leaf_overflow":
        second.min_start_date = date(2027, 1, 4)
    else:
        second.start_date = second.actual_start_date = date(2025, 12, 31)
    actor = await actor_factory()
    db_session.add_all([first, second])
    await db_session.flush()
    assigned = AgentTaskAssignment(
        task_id=second.id,
        actor_id=actor.id,
        task_version=second.version,
        purpose="execution",
        state="queued" if case == "leaf_overflow" else "accepted",
    )
    db_session.add(assigned)
    await db_session.commit()
    before = {
        t.id: (t.start_date, t.end_date, t.calculated_effort_days, t.version) for t in (first, second)
    }
    preserved = (assigned.id, assigned.task_version, assigned.state)
    result = await SchedulerService(db_session).schedule_iteration(iteration.id, protect_issued=True)
    year = 2027 if case == "leaf_overflow" else 2025
    assert not result.success and any(
        row["code"] == "calendar_outside_year" and row["missing_calendar_years"] == [year]
        for row in result.capacity_issues
    )
    for task_id, expected in before.items():
        actual = await db_session.get(Task, task_id, populate_existing=True)
        assert (
            actual.start_date,
            actual.end_date,
            actual.calculated_effort_days,
            actual.version,
        ) == expected
    fresh = await db_session.get(AgentTaskAssignment, preserved[0], populate_existing=True)
    assert (fresh.task_version, fresh.state) == preserved[1:]


@pytest.mark.parametrize("personal_years", [False, True])
async def test_single_year_apply_protects_accepted_work_even_with_personal_annuals(
    db_session, actor_factory, monkeypatch, personal_years
):
    monkeypatch.setattr("app.services.work_metrics.working_today", lambda *_a, **_k: date(2026, 12, 28))
    primary, future = await calendars(db_session)
    iteration = Iteration(
        name="One year", calendar=primary, start_date=date(2026, 12, 28), end_date=date(2026, 12, 31)
    )
    profile = TeamMemberProfile(display_name="Accepted owner")
    member = TeamMember(
        name="Writer",
        position="Developer",
        profile=profile,
        iteration=iteration,
        availability_percent=100,
        operational_utilization=0,
        professionalism_coefficient=1,
    )
    task = Task(
        title="Reserved task",
        assignee=member,
        iteration=iteration,
        status="planned",
        effort_hours=8,
        effort_days=1,
        start_date=date(2026, 12, 30),
        end_date=date(2026, 12, 30),
        calculated_effort_days=2,
    )
    actor = await actor_factory()
    db_session.add(task)
    await db_session.flush()
    if personal_years:
        db_session.add(
            ProfileAvailability(
                profile_id=profile.id, calendar_id=primary.id, version=1, additional_calendars=[future]
            )
        )
    assignment = AgentTaskAssignment(
        task_id=task.id, actor_id=actor.id, task_version=task.version, state="accepted", purpose="execution"
    )
    db_session.add(assignment)
    await db_session.commit()
    task_id, version, period, aid = task.id, task.version, iteration.id, assignment.id
    with pytest.raises(PlanningConflict) as refused:
        await SchedulerService(db_session).schedule_iteration(period, protect_issued=True)
    assert refused.value.code == "issued_task_schedule_conflict"
    current = await db_session.get(Task, task_id)
    assert current.version == version and current.start_date == current.end_date == date(2026, 12, 30)
    retained = await db_session.get(AgentTaskAssignment, aid)
    assert retained.task_version == version and retained.state == "accepted"


async def test_legacy_iteration_entirely_outside_its_primary_year_is_explicitly_held(
    db_session, monkeypatch
):
    monkeypatch.setattr("app.services.work_metrics.working_today", lambda *_a, **_k: date(2026, 11, 20))
    primary, future = await calendars(db_session)
    iteration = Iteration(
        name="Legacy next-year work",
        calendar=primary,
        start_date=date(2027, 1, 3),
        end_date=date(2027, 1, 5),
    )
    profile = TeamMemberProfile(display_name="Person")
    member = TeamMember(
        name="Writer",
        position="Developer",
        profile=profile,
        iteration=iteration,
        availability_percent=100,
        operational_utilization=0,
        professionalism_coefficient=1,
    )
    task = Task(
        title="Delivery notes",
        assignee=member,
        iteration=iteration,
        status="planned",
        effort_hours=4,
        effort_days=0.5,
        start_date=date(2027, 1, 4),
        end_date=date(2027, 1, 4),
    )
    db_session.add(task)
    await db_session.commit()
    service = IterationService(db_session)
    iteration = await service.get_by_id(iteration.id)
    member = await TeamService(db_session).get_by_id(member.id)

    async def check_held():
        summary = await service.get_summary(iteration.id)
        capacity = await TeamService(db_session).calculate_capacity(member.id)
        workload = await TeamService(db_session).get_workload(member.id)
        routing = (
            await AgentRoutingService(db_session)._capacity_inputs(
                task=task, iteration=iteration, members=[member]
            )
        )[member.id]
        for result in (service.to_response(iteration), summary, capacity, workload):
            assert result.missing_calendar_years == [2027]
        assert summary.working_days == 0 and capacity.hours == 0 and workload.capacity_hours == 0
        assert routing["workload_ratio"] is None and routing["missing_calendar_years"] == [2027]
        with pytest.raises(ValueError, match="outside"):
            day_hours(primary, date(2027, 1, 4))

    await check_held()
    before = task.version
    held = await SchedulerService(db_session).schedule_iteration(iteration.id)
    assert not held.success and held.capacity_issues[0]["code"] == "calendar_outside_year"
    assert task.version == before and task.start_date == date(2027, 1, 4)
    restored = await service.update(iteration.id, IterationUpdate(additional_calendar_ids=[future.id]))
    assert (
        service.to_response(restored).working_days == 2
        and not service.to_response(restored).missing_calendar_years
    )
    assert (await TeamService(db_session).calculate_capacity(member.id)).hours == 11
    assert not (await TeamService(db_session).get_workload(member.id)).missing_calendar_years


async def test_private_cross_year_commitment_warns_the_draft_and_holds_only_baseline_commit(
    db_session, monkeypatch
):
    from app.commands import command_transaction

    monkeypatch.setattr("app.services.work_metrics.working_today", lambda *_a, **_k: date(2027, 1, 4))
    first, future = await calendars(db_session)
    visible, hidden = Project(name="Visible deliveries"), Project(name="Private companion project")
    profile = TeamMemberProfile(display_name="Shared writer")
    principal = Principal(kind="human", display_name="Scoped project manager")
    public_iteration = Iteration(
        name="Published delivery",
        calendar=future,
        project=visible,
        start_date=date(2027, 1, 4),
        end_date=date(2027, 1, 10),
    )
    private_iteration = Iteration(
        name="Private prior allocation",
        calendar=future,
        project=hidden,
        start_date=date(2026, 12, 29),
        end_date=date(2027, 1, 6),
    )
    public_member = TeamMember(
        name="Visible writer",
        position="Developer",
        profile=profile,
        iteration=public_iteration,
        availability_percent=50,
        operational_utilization=0,
        professionalism_coefficient=1,
    )
    private_member = TeamMember(
        name="Private writer",
        position="Developer",
        profile=profile,
        iteration=private_iteration,
        availability_percent=50,
        operational_utilization=0,
        professionalism_coefficient=1,
    )
    planned = Task(
        title="Visible guide",
        project=visible,
        iteration=public_iteration,
        assignee=public_member,
        effort_hours=2,
        effort_days=0.25,
        status="planned",
    )
    private_commit = Task(
        title="Secret baseline title",
        project=hidden,
        iteration=private_iteration,
        assignee=private_member,
        effort_hours=12,
        effort_days=2,
        status="active",
        baseline_start_date=date(2026, 12, 30),
        baseline_end_date=date(2027, 1, 6),
    )
    db_session.add_all([principal, planned, private_commit])
    await db_session.commit()
    period, person = public_iteration.id, profile.id
    db_session.info["authority"] = Authority(
        principal_id=principal.id, kind="human", workspace_role="member", projects={visible.id: "manager"}
    )
    service = SchedulerService(db_session)
    async with command_transaction(db_session, mode="preview"):
        before = (await IterationService(db_session).get_by_id(period)).revision
        draft = await service.schedule_iteration(period, commit=False, expected_revision=before)
        assert draft.success
        (issue,) = [i for i in draft.capacity_issues if i["code"] == "commitment_calendar_coverage_missing"]
        assert (
            set(issue) == {"profile_id", "code", "message"}
            and issue["profile_id"] == person
            and "capacity owner" in issue["message"]
        )
        assert "Private companion project" not in str(issue) and "Secret baseline title" not in str(issue)
    before = (await IterationService(db_session).get_by_id(period)).revision
    with pytest.raises(PlanningConflict) as held:
        await service.schedule_iteration(period, expected_revision=before, commit_baseline=True)
    assert held.value.code == "commitment_calendar_coverage_missing"
