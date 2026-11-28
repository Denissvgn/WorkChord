"""The scheduler says which planned tasks it left without dates, and readiness says how to fix it."""

from datetime import date, timedelta

import httpx
import pytest
from sqlalchemy import select

from app.main import app
from app.models.iteration import Iteration
from app.models.task import Task, TaskDependency
from app.models.team_member import TeamMember, TeamMemberProfile
from app.services.agent_readiness import evaluate_agent_readiness
from app.services.scheduler_service import SchedulerService
from tests.test_delivery_scenarios import delivery_store


def _schedule_reason(task: Task) -> tuple[bool, str]:
    readiness = evaluate_agent_readiness(task, tags=["agent"], children=[], dependencies=[])
    criterion = next(item for item in readiness.criteria if item.key == "schedule")
    return criterion.passed, criterion.reason


@pytest.mark.parametrize(("iteration_id", "assignee_id", "expected"), [
    (None, None, "add it to an iteration"),
    (1, None, "Assign it to a capacity row in this iteration"),
    (1, 7, "run the scheduler for this iteration"),
])
def test_readiness_names_the_missing_scheduling_step(iteration_id, assignee_id, expected):
    task = Task(title="Agent work", status="planned", iteration_id=iteration_id, assignee_id=assignee_id,
                priority=5, effort_days=1, effort_hours=8)
    passed, reason = _schedule_reason(task)
    assert passed is False
    assert expected in reason


async def test_scheduler_reports_unassigned_and_outside_assignee_tasks(delivery_store):
    factory, scenario, _ = delivery_store
    iteration_id = scenario.iterations[0]
    async with factory() as db:
        unassigned = Task(title="Unassigned leaf", status="planned", priority=3, iteration_id=iteration_id,
                          project_id=scenario.projects[0], effort_days=1, effort_hours=8)
        # A capacity row from the other iteration does not make this one schedulable.
        outside = Task(title="Outside assignee leaf", status="planned", priority=3, iteration_id=iteration_id,
                       project_id=scenario.projects[0], assignee_id=scenario.capacity_rows[1],
                       effort_days=1, effort_hours=8)
        db.add_all([unassigned, outside])
        await db.commit()
        result = await SchedulerService(db).schedule_iteration(iteration_id)

    reasons = {item.task_id: item.reason for item in result.unscheduled}
    assert reasons[unassigned.id] == "no_assignee"
    assert reasons[outside.id] == "assignee_not_in_iteration"
    assert scenario.tasks["planned"] not in reasons
    explained = {decision.task_id for decision in result.decisions if decision.decision_type == "unavailable"}
    assert {unassigned.id, outside.id} <= explained
    message = next(item.message for item in result.unscheduled if item.task_id == unassigned.id)
    assert "capacity row" in message


async def test_agent_capacity_row_assignment_and_apply_schedule_an_unassigned_task(delivery_store):
    from app.models.agent import AgentActor
    from app.schemas.agent_planning import AgentPlanningCommandContext, AgentScheduleCommand
    from app.services.agent_planning_service import AgentPlanningService

    factory, scenario, _ = delivery_store
    iteration_id = scenario.iterations[0]
    async with factory() as db:
        actor = await db.get(AgentActor, scenario.actors[0])
        actor.scopes, actor.role = '["planning:write"]', "pm"
        profile = TeamMemberProfile(seed_key="unscheduled-agent-lane", display_name="Agent lane",
                                    profile_kind="agent", automation_enabled=True)
        lane = TeamMember(name="Agent lane", position="Agent", profile=profile, iteration_id=iteration_id)
        task = Task(title="Agent-ready leaf", status="planned", priority=3, iteration_id=iteration_id,
                    project_id=scenario.projects[0], effort_days=1, effort_hours=8)
        db.add_all([profile, lane, task])
        await db.commit()
        # The preview rolls back and expires loaded objects; keep plain ids from here on.
        task_id, lane_id = task.id, lane.id
        service = AgentPlanningService(db)

        before = await service.preview_schedule(iteration_id, actor, command=AgentPlanningCommandContext(
            idempotency_key="unscheduled-before", rationale="See what stays unscheduled", correlation_id="unscheduled-before"))
        assert {row["task_id"]: row["reason"] for row in before.result["unscheduled"]}[task_id] == "no_assignee"

        assigned = await db.get(Task, task_id, populate_existing=True)
        assigned.assignee_id = lane_id
        await db.commit()
        await db.refresh(actor)
        preview = await service.preview_schedule(iteration_id, actor, command=AgentPlanningCommandContext(
            idempotency_key="unscheduled-preview", rationale="Observe schedule inputs", correlation_id="unscheduled-preview"))
        assert task_id not in {row["task_id"] for row in preview.result["unscheduled"]}
        data = AgentScheduleCommand(
            expected_task_versions={row["task_id"]: row["version"] for row in preview.result["task_states"]},
            expected_input_digest=preview.result["input_digest"])
        await db.refresh(actor)
        await service.apply_schedule(iteration_id, actor, data, command=AgentPlanningCommandContext(
            idempotency_key="unscheduled-apply", rationale="Schedule the agent lane", correlation_id="unscheduled-apply"))

    async with factory() as db:
        scheduled = (await db.scalars(select(Task).where(Task.id == task_id))).one()
        assert scheduled.start_date is not None and scheduled.end_date is not None
        passed, _ = _schedule_reason(scheduled)
        assert passed is True


async def test_schedule_omits_undated_deferred_work_on_apply(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        task = Task(title="Deferred work", status="planned", priority=3,
                    iteration_id=scenario.iterations[0], is_deferred=True)
        db.add(task)
        await db.commit()
        result = await SchedulerService(db).schedule_iteration(scenario.iterations[0])
        assert task.id not in {item.task_id for item in result.unscheduled}
        assert task.id not in {item.task_id for item in result.decisions}
        assert task.start_date is None and task.end_date is None


async def _ownerless_chain(db, scenario):
    """A task without a capacity owner, an owned dependent, an ownerless dependent and a dependent of that."""
    iteration_id = scenario.iterations[0]
    saved = date(2026, 1, 27)
    common = dict(status="planned", priority=3, iteration_id=iteration_id, project_id=scenario.projects[0],
                  effort_days=1, effort_hours=8, start_date=saved, end_date=saved)
    root = Task(title="Ownerless root", **common)
    # Small efforts keep the owner's saved dates within one day's productive hours.
    owner = {**common, "effort_hours": 2}
    owned = Task(title="Owned dependent", assignee_id=scenario.capacity_rows[0], **owner)
    ownerless = Task(title="Ownerless dependent", **common)
    tail = Task(title="Dependent of the ownerless dependent", assignee_id=scenario.capacity_rows[0],
                **{**owner, "start_date": date(2026, 1, 28), "end_date": date(2026, 1, 28)})
    db.add_all([root, owned, ownerless, tail])
    await db.flush()
    db.add_all([TaskDependency(task_id=owned.id, depends_on_id=root.id),
                TaskDependency(task_id=ownerless.id, depends_on_id=root.id),
                TaskDependency(task_id=tail.id, depends_on_id=ownerless.id)])
    await db.commit()
    return iteration_id, root.id, owned.id, ownerless.id, tail.id


def _assert_chain_reported(kept_dates, root, owned, ownerless, tail):
    by_id = {item["task_id"]: item for item in kept_dates}
    assert set(by_id) == {root, owned, ownerless, tail}
    assert by_id[root]["reason"] == "no_assignee"
    for task_id in (root, owned, ownerless, tail):
        day = "2026-01-28" if task_id == tail else "2026-01-27"
        assert by_id[task_id]["start_date"] == by_id[task_id]["end_date"] == day
        assert "were kept" in by_id[task_id]["message"]
    for task_id in (owned, ownerless, tail):
        assert by_id[task_id]["reason"] == "predecessor_unscheduled"
    assert by_id[owned]["also"] == []
    assert by_id[tail]["also"] == []
    # The dependent without an owner keeps its own cause visible behind the predecessor.
    assert by_id[ownerless]["also"] == ["no_assignee"]
    assert "capacity row" in by_id[ownerless]["message"]
    assert "Ownerless root" in by_id[owned]["message"]
    assert "Ownerless dependent" in by_id[tail]["message"]


async def test_schedule_keeps_the_valid_dates_of_ownerless_task_and_every_dependent_it_cannot_place(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        iteration_id, *ids = await _ownerless_chain(db, scenario)
        result = await SchedulerService(db).schedule_iteration(iteration_id)
        _assert_chain_reported([item.model_dump(mode="json") for item in result.kept_dates], *ids)
        assert result.unscheduled == []
        # The causes found only after placing (no assignee) explain themselves as decisions for kept tasks too.
        explained = {decision.task_id for decision in result.decisions if decision.decision_type == "unavailable"}
        assert {ids[0], ids[2]} <= explained
        rows = (await db.scalars(select(Task).where(Task.id.in_(ids)))).all()
        assert all(row.start_date == row.end_date == date(2026, 1, 28 if row.id == ids[3] else 27) for row in rows)


async def test_a_task_that_never_had_dates_is_not_reported_as_cleared(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        task = Task(title="Never dated", status="planned", priority=3, iteration_id=scenario.iterations[0],
                    project_id=scenario.projects[0], effort_days=1, effort_hours=8)
        db.add(task)
        await db.commit()
        result = await SchedulerService(db).schedule_iteration(scenario.iterations[0])
        item = next(item for item in result.unscheduled if item.task_id == task.id)
        assert item.reason == "no_assignee" and item.dates_cleared is False


async def _separate_shared_owner_iterations(db, scenario):
    """The seeded owner sits in two overlapping iterations; move the second so a baseline commit is accepted."""
    other = await db.get(Iteration, scenario.iterations[1])
    other.start_date, other.end_date = date(2026, 2, 2), date(2026, 2, 27)
    # Seeded finished and running work stays within one day's productive hours.
    for offset, key in enumerate(("active", "resolved", "closed_urgent", "closed_low")):
        task = await db.get(Task, scenario.tasks[key])
        task.start_date = task.end_date = date(2026, 1, 12 + offset)
        task.effort_hours = 2
    await db.commit()


async def test_rest_schedule_and_preview_responses_name_tasks_that_keep_their_dates(delivery_store, monkeypatch):
    # Forecasts start at the working date; pin it inside the seeded iteration.
    monkeypatch.setattr("app.services.work_metrics.working_today", lambda *_: date(2026, 1, 5))
    factory, scenario, _ = delivery_store
    async with factory() as db:
        await _separate_shared_owner_iterations(db, scenario)
        iteration_id, *ids = await _ownerless_chain(db, scenario)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        preview = await client.post(f"/api/iterations/{iteration_id}/schedule/preview", json={"changes": []})
        assert preview.status_code == 200, preview.text
        _assert_chain_reported(preview.json()["schedule_result"]["kept_dates"], *ids)
        applied = await client.post(f"/api/iterations/{iteration_id}/schedule")
        assert applied.status_code == 200, applied.text
        _assert_chain_reported(applied.json()["kept_dates"], *ids)
    async with factory() as db:
        rows = (await db.scalars(select(Task).where(Task.id.in_(ids)))).all()
        assert len(rows) == 4
        assert all(row.start_date == row.end_date == date(2026, 1, 28 if row.id == ids[3] else 27) for row in rows)


async def test_agent_schedule_preview_names_tasks_that_keep_their_dates(delivery_store):
    from app.models.agent import AgentActor
    from app.schemas.agent_planning import AgentPlanningCommandContext
    from app.services.agent_planning_service import AgentPlanningService

    factory, scenario, _ = delivery_store
    async with factory() as db:
        iteration_id, *ids = await _ownerless_chain(db, scenario)
        actor = await db.get(AgentActor, scenario.actors[0])
        actor.scopes, actor.role = '["planning:write"]', "pm"
        await db.commit()
        receipt = await AgentPlanningService(db).preview_schedule(iteration_id, actor, command=AgentPlanningCommandContext(
            idempotency_key="kept-preview", rationale="See which tasks keep their dates", correlation_id="kept-preview"))
        _assert_chain_reported(receipt.result["kept_dates"], *ids)


async def _imported_plan_with_unplaceable_tasks(db, scenario):
    """Imported dates on tasks the scheduler cannot place: valid ones, and one for each rule they can break."""
    iteration = await db.get(Iteration, scenario.iterations[0])
    common = dict(status="planned", priority=3, iteration_id=iteration.id, project_id=scenario.projects[0],
                  effort_days=1, effort_hours=8)
    inside = (date(2026, 1, 27), date(2026, 1, 28))
    tasks = {
        "valid": Task(title="Valid imported dates", start_date=inside[0], end_date=inside[1], **common),
        "no_estimate": Task(title="Imported without estimate", assignee_id=scenario.capacity_rows[0],
                            start_date=inside[0], end_date=inside[1], **{**common, "effort_days": None, "effort_hours": None}),
        "inverted": Task(title="Inverted dates", start_date=inside[1], end_date=inside[0], **common),
        "outside": Task(title="Dates after the iteration", start_date=iteration.end_date + timedelta(days=3),
                        end_date=iteration.end_date + timedelta(days=4), **common),
        "half": Task(title="Only a start date", start_date=inside[0], **common),
        "too_early": Task(title="Starts before its earliest start", start_date=inside[0], end_date=inside[1],
                          min_start_date=date(2026, 1, 29), **common),
    }
    db.add_all(tasks.values())
    await db.commit()
    return iteration.id, {key: task.id for key, task in tasks.items()}


async def test_schedule_keeps_imported_dates_and_names_the_rule_they_break(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        iteration_id, ids = await _imported_plan_with_unplaceable_tasks(db, scenario)
        result = await SchedulerService(db).schedule_iteration(iteration_id)
        rows = {key: await db.get(Task, task_id, populate_existing=True) for key, task_id in ids.items()}
        saved = {"valid": (date(2026, 1, 27), date(2026, 1, 28)), "no_estimate": (date(2026, 1, 27), date(2026, 1, 28)),
                 "inverted": (date(2026, 1, 28), date(2026, 1, 27)),
                 "outside": (date(2026, 2, 2), date(2026, 2, 3)), "too_early": (date(2026, 1, 27), date(2026, 1, 28))}

    kept = {item.task_id: item for item in result.kept_dates}
    assert kept[ids["valid"]].reason == "no_assignee" and kept[ids["valid"]].date_rule is None
    assert kept[ids["no_estimate"]].reason == "no_estimate" and kept[ids["no_estimate"]].date_rule is None
    # Dates that break a rule stay too: the run never leaves a task it cannot place without dates.
    expected = {"inverted": "dates_inverted", "outside": "outside_iteration", "too_early": "before_min_start_date"}
    for key, rule in expected.items():
        item = kept[ids[key]]
        assert item.date_rule == rule and f"rule {rule}" in item.message
        assert (item.start_date, item.end_date) == saved[key]
    for key, dates in saved.items():
        assert (rows[key].start_date, rows[key].end_date) == dates

    # Only a half-dated task has no period to keep: it is the one task whose dates the run removes.
    removed = {item.task_id: item for item in result.unscheduled}
    assert set(removed) == {ids["half"]}
    assert removed[ids["half"]].date_rule == "dates_incomplete" and removed[ids["half"]].dates_cleared is True
    assert "rule dates_incomplete" in removed[ids["half"]].message
    assert rows["half"].start_date is None and rows["half"].end_date is None
    assert ids["half"] not in kept


async def test_kept_dates_say_when_they_start_before_the_planning_start_or_a_placed_prerequisite(delivery_store, monkeypatch):
    monkeypatch.setattr("app.services.work_metrics.working_today", lambda *_: date(2026, 1, 20))
    factory, scenario, _ = delivery_store
    async with factory() as db:
        common = dict(status="planned", priority=3, iteration_id=scenario.iterations[0], project_id=scenario.projects[0],
                      effort_days=1, effort_hours=2)
        placed = Task(title="Placed prerequisite", assignee_id=scenario.capacity_rows[0], **common)
        past = Task(title="Imported in the past", start_date=date(2026, 1, 6), end_date=date(2026, 1, 7), **common)
        early = Task(title="Imported before its prerequisite", start_date=date(2026, 1, 21), end_date=date(2026, 1, 22), **common)
        db.add_all([placed, past, early])
        await db.flush()
        db.add(TaskDependency(task_id=early.id, depends_on_id=placed.id))
        await db.commit()
        result = await SchedulerService(db).schedule_iteration(scenario.iterations[0])
        placed_end = (await db.get(Task, placed.id)).end_date

    kept = {item.task_id: item for item in result.kept_dates}
    assert "start before the planning start (2026-01-20)" in kept[past.id].message
    assert f"start on or before the end of its prerequisite 'Placed prerequisite' ({placed_end})" in kept[early.id].message
    assert placed.id not in kept


async def test_following_actual_dates_restores_a_half_dated_task_without_failing(delivery_store):
    factory, scenario, _ = delivery_store
    async with factory() as db:
        common = dict(status="planned", priority=3, iteration_id=scenario.iterations[0], project_id=scenario.projects[0],
                      effort_days=1, effort_hours=8)
        half = Task(title="Half dated", start_date=date(2026, 1, 27), **common)
        full = Task(title="Fully dated", start_date=date(2026, 1, 27), end_date=date(2026, 1, 28), **common)
        db.add_all([half, full])
        await db.commit()
        result = await SchedulerService(db).schedule_iteration(
            scenario.iterations[0], commit=False, follow_date=date(2026, 1, 12))
        assert result.success
        # Following actual dates restores every date and judges none; only a complete period is listed as kept.
        assert (half.start_date, half.end_date) == (date(2026, 1, 27), None)
        assert (full.start_date, full.end_date) == (date(2026, 1, 27), date(2026, 1, 28))
        kept = {item.task_id: item for item in result.kept_dates}
        assert half.id not in kept
        assert kept[full.id].date_rule is None


async def test_schedule_preview_and_apply_agree_on_an_imported_plan(delivery_store, monkeypatch):
    monkeypatch.setattr("app.services.work_metrics.working_today", lambda *_: date(2026, 1, 5))
    factory, scenario, _ = delivery_store
    async with factory() as db:
        await _separate_shared_owner_iterations(db, scenario)
        iteration_id, ids = await _imported_plan_with_unplaceable_tasks(db, scenario)
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        preview = await client.post(f"/api/iterations/{iteration_id}/schedule/preview", json={"changes": []})
        assert preview.status_code == 200, preview.text
        applied = await client.post(f"/api/iterations/{iteration_id}/schedule")
        assert applied.status_code == 200, applied.text
    previewed, result = preview.json(), applied.json()
    for key in ("kept_dates", "unscheduled"):
        assert previewed["schedule_result"][key] == result[key]
        assert result[key], key
    shown = {task["id"]: (task["start_date"], task["end_date"]) for task in previewed["tasks"]}
    async with factory() as db:
        rows = (await db.scalars(select(Task).where(Task.iteration_id == iteration_id))).all()
        applied_dates = {row.id: (row.start_date, row.end_date) for row in rows}
    for task_id, dates in shown.items():
        applied_value = tuple(value.isoformat() if value else None for value in applied_dates[task_id])
        assert tuple(value[:10] if value else None for value in dates) == applied_value
    # A task the run could not place is never left without the dates it had, except one that had only one date.
    undated = {task_id for task_id, dates in applied_dates.items() if dates == (None, None)}
    assert undated & set(ids.values()) == {ids["half"]}
    assert {item["task_id"] for item in result["unscheduled"]} == {ids["half"]}


async def test_a_baseline_commit_does_not_commit_the_dates_it_kept(delivery_store, monkeypatch):
    monkeypatch.setattr("app.services.work_metrics.working_today", lambda *_: date(2026, 1, 5))
    factory, scenario, _ = delivery_store
    async with factory() as db:
        await _separate_shared_owner_iterations(db, scenario)
        day = date(2026, 1, 5)
        common = dict(status="planned", priority=3, iteration_id=scenario.iterations[0], project_id=scenario.projects[0],
                      effort_days=1, effort_hours=8, start_date=day, end_date=day)
        root = Task(title="Ownerless root", **common)
        kept = Task(title="Kept dependent", assignee_id=scenario.capacity_rows[0], **common)
        db.add_all([root, kept])
        await db.flush()
        db.add(TaskDependency(task_id=kept.id, depends_on_id=root.id))
        await db.commit()
    async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
        applied = await client.post(f"/api/iterations/{scenario.iterations[0]}/schedule")
        assert applied.status_code == 200, applied.text
        assert {item["task_id"] for item in applied.json()["kept_dates"]} == {root.id, kept.id}
    async with factory() as db:
        for task_id in (root.id, kept.id):
            row = await db.get(Task, task_id)
            assert row.start_date == day and row.end_date == day
            assert row.baseline_revision == 0 and row.baseline_start_date is None
        placed = await db.get(Task, scenario.tasks["planned"])
        assert placed.baseline_revision == 1
