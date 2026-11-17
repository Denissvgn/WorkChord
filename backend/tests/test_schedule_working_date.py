"""Forecasts respect the working date and readiness rejects stale saved dates."""

from datetime import UTC, date, datetime

import pytest

from app.models.project import Project
from app.models.task import Task
from app.schemas.iteration import IterationUpdate
from app.services import work_metrics
from app.services.iteration_service import IterationService
from app.services.scheduler_service import IncrementalScheduler, SchedulerService
from tests.test_scheduler_dependencies import make_plan


@pytest.fixture(autouse=True)
def fixed_working_date(monkeypatch):
    monkeypatch.setattr(work_metrics, "utc_now", lambda: datetime(2026, 11, 17, 23, 30, tzinfo=UTC))


async def current_plan(db):
    iteration, members, tasks = await make_plan(db, 2, [0, 1], [])
    iteration.start_date = date(2026, 11, 16)
    iteration.end_date = date(2026, 11, 30)
    await db.commit()
    return iteration, members, tasks


@pytest.mark.parametrize("incremental", [False, True], ids=["full", "incremental"])
@pytest.mark.parametrize("project_zone, calendar_zone, expected", [
    (None, "UTC", date(2026, 11, 17)),
    (None, "Asia/Tokyo", date(2026, 11, 18)),
    ("America/Los_Angeles", "Asia/Tokyo", date(2026, 11, 17)),
    ("Asia/Tokyo", "America/Los_Angeles", date(2026, 11, 18)),
])
async def test_unstarted_work_starts_no_earlier_than_workspace_today(
    db_session, incremental, project_zone, calendar_zone, expected,
):
    iteration, _, tasks = await current_plan(db_session)
    iteration.calendar.timezone = calendar_zone
    if project_zone:
        iteration.project = Project(name="Zoned workspace", timezone=project_zone)
    await db_session.commit()
    scheduler = SchedulerService(db_session)
    if incremental:
        await IncrementalScheduler(scheduler)._reschedule_subset(iteration.id, {task.id for task in tasks})
    else:
        result = await scheduler.schedule_iteration(iteration.id)
        assert result.success and not result.unscheduled
    assert all(task.start_date == expected and task.end_date == expected for task in tasks)


@pytest.mark.parametrize("status", ["active", "resolved", "closed"])
async def test_schedule_keeps_started_and_done_dates(db_session, status):
    iteration, _, tasks = await current_plan(db_session)
    locked, planned = tasks
    locked.status = status
    locked.start_date = locked.end_date = iteration.start_date
    await db_session.commit()
    await SchedulerService(db_session).schedule_iteration(iteration.id)
    assert locked.start_date == locked.end_date == date(2026, 11, 16)
    assert planned.start_date == date(2026, 11, 17)
    summary = await IterationService(db_session).get_planning_readiness_summary(iteration.id)
    assert summary.has_schedule and summary.checkpoints_done == 6


async def test_future_iteration_and_nonworking_dates_still_bound_forecasts(db_session):
    iteration, _, tasks = await current_plan(db_session)
    iteration.start_date = date(2026, 11, 21)  # Saturday
    iteration.calendar.holidays = ["2026-11-23"]
    tasks[1].min_start_date = date(2026, 11, 25)
    await db_session.commit()
    await SchedulerService(db_session).schedule_iteration(iteration.id)
    assert tasks[0].start_date == date(2026, 11, 24)
    assert tasks[1].start_date == date(2026, 11, 25)


@pytest.mark.parametrize("changed_dates", [
    {"start_date": date(2026, 11, 18)},
    {"end_date": date(2026, 11, 16)},
], ids=["start_moved_forward", "end_moved_back"])
async def test_moving_iteration_dates_requires_schedule_recalculation(db_session, changed_dates):
    iteration, _, tasks = await current_plan(db_session)
    service = IterationService(db_session)
    await SchedulerService(db_session).schedule_iteration(iteration.id)
    assert (await service.get_planning_readiness_summary(iteration.id)).checkpoints_done == 6
    saved_dates = [(task.start_date, task.end_date) for task in tasks]

    await service.update(iteration.id, IterationUpdate(**changed_dates))

    summary = await service.get_planning_readiness_summary(iteration.id)
    schedule = next(item for item in summary.checkpoints if item.id == "schedule")
    assert summary.has_schedule is False
    assert schedule.state == "todo" and schedule.reason_codes == ["schedule_not_built"]
    assert summary.checkpoints_done == 4
    assert [(task.start_date, task.end_date) for task in tasks] == saved_dates
    if "start_date" in changed_dates:
        await SchedulerService(db_session).schedule_iteration(iteration.id)
        assert (await service.get_planning_readiness_summary(iteration.id)).checkpoints_done == 6


async def test_saved_unstarted_work_before_today_requires_recalculation(db_session):
    iteration, _, tasks = await current_plan(db_session)
    for task in tasks:
        task.start_date = task.end_date = iteration.start_date
    await db_session.commit()
    summary = await IterationService(db_session).get_planning_readiness_summary(iteration.id)
    schedule = next(item for item in summary.checkpoints if item.id == "schedule")
    assert summary.has_schedule is False
    assert schedule.state == "todo" and schedule.reason_codes == ["schedule_not_built"]


async def test_readiness_and_scheduler_use_same_workspace_date(db_session):
    iteration, _, tasks = await current_plan(db_session)
    iteration.calendar.timezone = "Asia/Tokyo"
    for task in tasks:
        task.start_date = task.end_date = date(2026, 11, 17)
    await db_session.commit()
    service = IterationService(db_session)
    assert not (await service.get_planning_readiness_summary(iteration.id)).has_schedule
    await SchedulerService(db_session).schedule_iteration(iteration.id)
    assert (await service.get_planning_readiness_summary(iteration.id)).checkpoints_done == 6


async def test_excluded_and_structural_dates_do_not_invalidate_schedule(db_session):
    iteration, members, _ = await current_plan(db_session)
    for flags in [{"is_deferred": True}, {"canceled_at": datetime(2026, 11, 16, tzinfo=UTC)}, {"is_summary": True}]:
        db_session.add(Task(title="Excluded dates", iteration_id=iteration.id, assignee_id=members[0].id,
            start_date=date(2026, 11, 1), end_date=date(2026, 12, 1), effort_hours=8, **flags))
    await db_session.commit()
    await SchedulerService(db_session).schedule_iteration(iteration.id)
    summary = await IterationService(db_session).get_planning_readiness_summary(iteration.id)
    assert summary.task_count == 2 and summary.checkpoints_done == 6
