"""Ready lower-ranked work uses an assignee's free days before higher-ranked work that waits."""

from datetime import date, datetime, timezone
import random

import httpx
import pytest
from fastapi import Request

from app.commands import command_transaction
from app.database import get_db
from app.main import app
from app.models.task import Task
from app.services.scheduler_service import SchedulerService
from tests.test_scheduler_dependencies import assert_dependency_dates, assert_serial_rows, make_plan


@pytest.fixture(autouse=True)
def fixed_working_date(monkeypatch):
    from app.services import work_metrics

    monkeypatch.setattr(work_metrics, "utc_now", lambda: datetime(2026, 1, 5, 12, tzinfo=timezone.utc))


async def waiting_plan(db, *, low_hours=24):
    """Row 0: a high-priority task waiting on row 1's five-day prerequisite, and ready low-priority work."""
    iteration, members, tasks = await make_plan(db, 2, [1, 0, 0], [(0, 1)])
    prerequisite, waiting, ready = tasks
    prerequisite.title, prerequisite.effort_hours, prerequisite.priority = "Prerequisite", 40, 5
    waiting.title, waiting.priority = "Waiting work", 1
    ready.title, ready.effort_hours, ready.priority = "Ready work", low_hours, 9
    await db.commit()
    return iteration, members, tasks


def dates(tasks):
    return {task.id: (task.start_date, task.end_date) for task in tasks}


async def test_ready_lower_priority_work_uses_free_days_before_waiting_work(db_session):
    iteration, members, (prerequisite, waiting, ready) = await waiting_plan(db_session)
    result = await SchedulerService(db_session).schedule_iteration(iteration.id)

    assert (prerequisite.start_date, prerequisite.end_date) == (date(2026, 1, 5), date(2026, 1, 9))
    # The higher-priority task still starts the day after its prerequisite ends.
    assert (waiting.start_date, waiting.end_date) == (date(2026, 1, 12), date(2026, 1, 12))
    # The ready task runs in the free days instead of after the waiting task.
    assert (ready.start_date, ready.end_date) == (date(2026, 1, 5), date(2026, 1, 7))
    decision = next(item for item in result.decisions if item.task_id == ready.id)
    assert decision.decision_type == "reordered" and decision.affected_tasks == [waiting.id]

    idle = {row.member_id: row for row in result.idle_days}
    assert set(idle) == {members[0].id}
    row = idle[members[0].id]
    assert row.idle_working_days == 2
    (gap,) = row.gaps
    assert (gap.start_date, gap.end_date, gap.working_days) == (date(2026, 1, 8), date(2026, 1, 9), 2)
    assert gap.task_id == waiting.id and gap.reason == "waits_for_prerequisite"
    assert gap.waiting_on is not None and gap.waiting_on.task_id == prerequisite.id
    assert "Prerequisite" in gap.message and "Waiting work" in gap.message


async def test_work_that_does_not_fit_the_free_days_follows_the_waiting_work(db_session):
    iteration, members, (prerequisite, waiting, ready) = await waiting_plan(db_session, low_hours=48)
    result = await SchedulerService(db_session).schedule_iteration(iteration.id)

    assert waiting.start_date == date(2026, 1, 12)
    assert ready.start_date == date(2026, 1, 13)
    (row,) = result.idle_days
    assert row.member_id == members[0].id and row.idle_working_days == 5
    assert row.gaps[0].task_id == waiting.id


async def test_an_earliest_start_date_is_named_as_the_cause_of_idle_days(db_session):
    iteration, members, tasks = await make_plan(db_session, 1, [0], [])
    tasks[0].min_start_date = date(2026, 1, 7)
    await db_session.commit()
    result = await SchedulerService(db_session).schedule_iteration(iteration.id)
    (row,) = result.idle_days
    (gap,) = row.gaps
    assert (gap.start_date, gap.end_date) == (date(2026, 1, 5), date(2026, 1, 6))
    assert gap.reason == "earliest_start" and gap.waiting_on is None
    assert "2026-01-07" in gap.message


async def test_dates_kept_as_saved_do_not_occupy_the_row(db_session):
    """Kept dates are not part of the plan the run placed: other work may use those days."""
    iteration, members, (prerequisite, waiting, ready) = await waiting_plan(db_session)
    kept = Task(title="Kept work", iteration=iteration, assignee=members[0], effort_hours=None,
                nominal_day_hours=8, priority=1, status="planned",
                start_date=date(2026, 1, 5), end_date=date(2026, 1, 9))
    db_session.add(kept)
    await db_session.commit()
    result = await SchedulerService(db_session).schedule_iteration(iteration.id)

    assert {item.task_id for item in result.kept_dates} == {kept.id}
    assert (kept.start_date, kept.end_date) == (date(2026, 1, 5), date(2026, 1, 9))
    assert (ready.start_date, ready.end_date) == (date(2026, 1, 5), date(2026, 1, 7))
    # The assignee has saved work on the kept days, so they are not reported as idle.
    assert all(row.member_id != members[0].id for row in result.idle_days)


async def test_kept_dates_split_idle_days_that_the_next_task_still_explains(db_session):
    iteration, members, (prerequisite, waiting, ready) = await waiting_plan(db_session, low_hours=48)
    db_session.add(Task(title="Kept work", iteration=iteration, assignee=members[0], effort_hours=None,
                        nominal_day_hours=8, priority=1, status="planned",
                        start_date=date(2026, 1, 7), end_date=date(2026, 1, 7)))
    await db_session.commit()
    result = await SchedulerService(db_session).schedule_iteration(iteration.id)
    (row,) = result.idle_days
    assert row.idle_working_days == 4
    assert [(gap.start_date, gap.end_date) for gap in row.gaps] == [
        (date(2026, 1, 5), date(2026, 1, 6)), (date(2026, 1, 8), date(2026, 1, 9))]
    assert {gap.task_id for gap in row.gaps} == {waiting.id}


@pytest.mark.parametrize(("prerequisite_hours", "min_start", "reason", "starts"), [
    # The earliest start date is later than the day after the prerequisite ends.
    (16, date(2026, 1, 8), "earliest_start", date(2026, 1, 8)),
    # The prerequisite ends after the earliest start date.
    (40, date(2026, 1, 7), "waits_for_prerequisite", date(2026, 1, 12)),
])
async def test_idle_days_name_the_constraint_that_binds(db_session, prerequisite_hours, min_start, reason, starts):
    iteration, members, (prerequisite, waiting) = await make_plan(db_session, 2, [1, 0], [(0, 1)])
    prerequisite.effort_hours = prerequisite_hours
    waiting.min_start_date = min_start
    await db_session.commit()
    result = await SchedulerService(db_session).schedule_iteration(iteration.id)
    assert waiting.start_date == starts
    (row,) = result.idle_days
    (gap,) = row.gaps
    assert gap.reason == reason and gap.task_id == waiting.id
    if reason == "earliest_start":
        assert gap.earliest_start == min_start and gap.waiting_on is None
        assert min_start.isoformat() in gap.message
    else:
        assert gap.earliest_start is None and gap.waiting_on.task_id == prerequisite.id


async def test_free_days_after_the_iteration_end_are_reported_overdue(db_session):
    iteration, _, tasks = await make_plan(db_session, 1, [0, 0, 0], [], end=date(2026, 1, 5))
    tasks[0].min_start_date = date(2026, 1, 12)
    tasks[0].max_end_date = date(2026, 1, 14)
    tasks[0].effort_hours = 16
    await db_session.commit()
    result = await SchedulerService(db_session).schedule_iteration(iteration.id)
    by_task = {item.task_id: item for item in result.decisions}
    assert tasks[1].end_date == date(2026, 1, 5) and by_task[tasks[1].id].decision_type == "reordered"
    assert tasks[2].end_date == date(2026, 1, 6)
    late = by_task[tasks[2].id]
    assert late.decision_type == "overdue"
    assert "beyond iteration by 1 days" in late.reason and "free days" in late.reason


async def test_schedule_preview_lists_idle_days(db_session_factory):
    async with db_session_factory() as db:
        iteration, members, (prerequisite, waiting, _) = await waiting_plan(db)
        iteration_id = iteration.id

    async def isolated_db(request: Request):
        async with db_session_factory() as db:
            async with command_transaction(db, mode="preview" if request.url.path.endswith("/preview") else "write"):
                yield db

    previous = app.dependency_overrides.copy()
    app.dependency_overrides[get_db] = isolated_db
    try:
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            preview = await client.post(f"/api/iterations/{iteration_id}/schedule/preview", json={"changes": []})
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous)
    assert preview.status_code == 200, preview.text
    (row,) = preview.json()["schedule_result"]["idle_days"]
    assert row["member_id"] == members[0].id and row["idle_working_days"] == 2
    gap = row["gaps"][0]
    assert gap["task_id"] == waiting.id and gap["waiting_on"]["task_id"] == prerequisite.id


def random_plan(seed):
    rng = random.Random(seed)
    count, rows = 40, 3
    assignments = [rng.randrange(rows) for _ in range(count)]
    edges = sorted({(predecessor, index) for index in range(1, count) for predecessor in
                    rng.sample(range(index), min(index, rng.choice([0, 0, 1, 2])))})
    efforts = [rng.choice([4, 8, 12, 16, 24, 40]) for _ in range(count)]
    priorities = [rng.randrange(1, 10) for _ in range(count)]
    min_starts = [date(2026, 1, rng.randrange(5, 30)) if rng.random() < .1 else None for _ in range(count)]
    return rows, assignments, edges, efforts, priorities, min_starts


async def schedule_random_plan(db, seed):
    rows, assignments, edges, efforts, priorities, min_starts = random_plan(seed)
    iteration, _, tasks = await make_plan(db, rows, assignments, edges)
    for task, effort, priority, min_start in zip(tasks, efforts, priorities, min_starts):
        task.effort_hours, task.priority, task.min_start_date = effort, priority, min_start
    await db.commit()
    return iteration, tasks, edges


@pytest.mark.parametrize("seed", [3, 17, 29, 41, 58, 73])
async def test_no_task_starts_later_than_under_the_row_cursor_alone(db_session, monkeypatch, seed):
    iteration, tasks, edges = await schedule_random_plan(db_session, seed)
    service = SchedulerService(db_session)
    with monkeypatch.context() as patch:
        # The rule without free-day placement: each task follows its row's last task.
        patch.setattr(SchedulerService, "_place_in_free_days", lambda *args, **kwargs: False)
        cursor_only = await service.schedule_iteration(iteration.id)
    before = dates(tasks)
    result = await service.schedule_iteration(iteration.id)
    assert result.success and cursor_only.success and not result.unscheduled
    after = dates(tasks)
    for task in tasks:
        assert after[task.id][0] <= before[task.id][0], (seed, task.title)
        assert after[task.id][1] <= before[task.id][1], (seed, task.title)
    assert_dependency_dates(tasks, edges)
    assert_serial_rows(tasks)
    # Each generated plan has free days that ready work can use.
    assert any(after[key] != before[key] for key in after)
    assert max(end for _, end in after.values()) <= max(end for _, end in before.values())


async def test_the_same_inputs_give_the_same_dates_on_every_run(db_session):
    iteration, tasks, _ = await schedule_random_plan(db_session, 11)
    runs = []
    for _ in range(3):
        result = await SchedulerService(db_session).schedule_iteration(iteration.id)
        runs.append((dates(tasks), [row.model_dump() for row in result.idle_days],
                     [(item.task_id, item.decision_type) for item in result.decisions]))
    assert runs[0] == runs[1] == runs[2]
