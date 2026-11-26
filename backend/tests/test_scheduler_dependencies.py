"""Dependency-ready scheduling across capacity rows and configured passes."""

from datetime import date, datetime, timezone
import random
from time import perf_counter
from types import SimpleNamespace

import pytest

from app.models.calendar import Calendar
from app.models.iteration import Iteration
from app.models.task import Task, TaskDependency
from app.models.team_member import TeamMember, TeamMemberProfile, Vacation
from app.services.scheduler_service import SchedulerService


@pytest.fixture(autouse=True)
def fixed_working_date(monkeypatch):
    from app.services import work_metrics

    monkeypatch.setattr(work_metrics, "utc_now", lambda: datetime(2026, 1, 5, 12, tzinfo=timezone.utc))


async def make_plan(db, rows, assignments, edges, *, end=date(2026, 12, 31)):
    calendar = Calendar(name="Working week", year=2026, nominal_day_hours=8,
                        holidays=[], short_days=[], weekend_days=[5, 6])
    iteration = Iteration(name="Delivery", start_date=date(2026, 1, 5),
                          end_date=end, calendar=calendar)
    members = [TeamMember(name=f"Owner {index}", position="Developer", iteration=iteration,
                          operational_utilization=0,
                          profile=TeamMemberProfile(display_name=f"Owner {index}"))
               for index in range(rows)]
    db.add_all(members)
    await db.flush()
    tasks = [Task(title=f"Work {index}", iteration=iteration, assignee=members[row],
                  effort_hours=8, nominal_day_hours=8, priority=5, status="planned")
             for index, row in enumerate(assignments)]
    db.add_all(tasks)
    await db.flush()
    db.add_all([TaskDependency(task_id=tasks[dependent].id, depends_on_id=tasks[predecessor].id)
                for predecessor, dependent in edges])
    await db.commit()
    return iteration, members, tasks


def assert_dependency_dates(tasks, edges):
    for predecessor, dependent in edges:
        assert tasks[predecessor].end_date is not None
        assert tasks[dependent].start_date is not None
        assert tasks[dependent].start_date > tasks[predecessor].end_date, (predecessor, dependent)


def assert_serial_rows(tasks):
    rows = {}
    for task in tasks:
        assert task.start_date is not None and task.end_date is not None
        rows.setdefault(task.assignee_id, []).append(task)
    for tasks_on_row in rows.values():
        ordered = sorted(tasks_on_row, key=lambda task: task.start_date)
        for previous, following in zip(ordered, ordered[1:]):
            assert following.start_date > previous.end_date, (previous.title, following.title)


@pytest.mark.parametrize("fallback", [False, True])
async def test_two_rows_with_dependencies_in_both_directions(db_session, monkeypatch, fallback):
    edges = [(0, 1), (1, 2), (2, 3)]
    iteration, _, tasks = await make_plan(db_session, 2, [0, 1, 0, 1], edges)
    service = SchedulerService(db_session)
    if fallback:
        monkeypatch.setattr(service.rules_service, "get_scheduling_passes", lambda: [])
    result = await service.schedule_iteration(iteration.id)
    assert result.success and not result.unscheduled
    assert_dependency_dates(tasks, edges)
    assert_serial_rows(tasks)


async def test_dependency_chain_crosses_three_rows(db_session):
    edges = [(index, index + 1) for index in range(5)]
    iteration, _, tasks = await make_plan(db_session, 3, [2, 1, 0, 2, 0, 1], edges)
    await SchedulerService(db_session).schedule_iteration(iteration.id)
    assert_dependency_dates(tasks, edges)
    assert_serial_rows(tasks)


def generated_plan():
    rng = random.Random(491)
    assignments = [index % 10 for index in range(200)]
    edges = [(predecessor, index) for index in range(1, 200)
             for predecessor in sorted(rng.sample(range(index), min(index, 3)))]
    return assignments, edges


async def test_generated_plan_has_no_dependency_or_capacity_overlap(db_session):
    assignments, edges = generated_plan()
    iteration, _, tasks = await make_plan(db_session, 10, assignments, edges)
    for index, task in enumerate(tasks):
        task.effort_hours = [4, 8, 10, 16][index % 4]
        task.priority = index % 7
        if index % 13 == 0:
            task.max_end_date = date(2026, 8, 31)
    await db_session.commit()
    started = perf_counter()
    result = await SchedulerService(db_session).schedule_iteration(iteration.id)
    elapsed = perf_counter() - started
    print(f"200 tasks / 10 rows / {len(edges)} dependencies: {elapsed:.6f}s")
    assert result.success and not result.unscheduled
    assert_dependency_dates(tasks, edges)
    assert_serial_rows(tasks)


@pytest.mark.parametrize("cause", ["unassigned", "no_estimate", "blocked", "deferred", "active"])
async def test_undated_predecessor_leaves_dependents_unplaced_with_their_dates_and_named(db_session, cause):
    iteration, _, tasks = await make_plan(db_session, 2, [0, 1, 0], [(0, 1), (1, 2)])
    predecessor = tasks[0]
    if cause == "unassigned":
        predecessor.assignee_id = None
    elif cause == "no_estimate":
        predecessor.effort_hours = None
    elif cause == "blocked":
        predecessor.blocked_reason = "Waiting for input"
    elif cause == "deferred":
        predecessor.is_deferred = True
    else:
        predecessor.status = "active"
    for task in tasks[1:]:
        task.start_date = task.end_date = date(2026, 1, 5)
    await db_session.commit()
    result = await SchedulerService(db_session).schedule_iteration(iteration.id)
    not_placed = {item.task_id: item for item in result.not_placed}
    for index in [1, 2]:
        assert tasks[index].start_date == tasks[index].end_date == date(2026, 1, 5)
        item = not_placed[tasks[index].id]
        assert item.start_date == item.end_date == date(2026, 1, 5)
        assert item.reason == "predecessor_unscheduled"
        assert tasks[index - 1].title in item.message
        assert any(decision.task_id == tasks[index].id and tasks[index - 1].title in decision.reason
                   for decision in result.decisions)


@pytest.mark.parametrize("status", ["resolved", "closed", "canceled"])
@pytest.mark.parametrize("saved_dates", [
    (None, None),
    (date(2026, 2, 2), None),
    (None, date(2026, 2, 3)),
    (date(2026, 2, 2), date(2026, 2, 3)),
], ids=["undated", "start_only", "end_only", "dated"])
@pytest.mark.parametrize("follow_date", [None, date(2026, 1, 12)], ids=["schedule", "follow"])
async def test_finished_predecessor_does_not_delay_dependents(db_session, status, saved_dates, follow_date):
    iteration, _, tasks = await make_plan(db_session, 3, [0, 1, 2], [(0, 1), (1, 2)])
    predecessor, dependent, _ = tasks
    if status == "canceled":
        predecessor.canceled_at = datetime(2026, 1, 4, tzinfo=timezone.utc)
    else:
        predecessor.status = status
    predecessor.start_date, predecessor.end_date = saved_dates
    dependent.min_start_date = date(2026, 1, 6)
    await db_session.commit()

    result = await SchedulerService(db_session).schedule_iteration(iteration.id, follow_date=follow_date)

    assert result.success and not result.unscheduled
    assert (predecessor.start_date, predecessor.end_date) == saved_dates
    assert dependent.start_date == max(dependent.min_start_date, follow_date or iteration.start_date)
    assert_dependency_dates(tasks, [(1, 2)])
    assert_serial_rows(tasks[1:])


async def test_ready_tasks_keep_pass_priority_and_cross_pass_dependencies(db_session):
    iteration, _, tasks = await make_plan(db_session, 2, [0, 1, 0, 1], [(0, 1)])
    tasks[0].priority = 100
    tasks[1].max_end_date = date(2026, 1, 9)
    tasks[2].priority = 0
    tasks[3].priority = 100
    await db_session.commit()
    await SchedulerService(db_session).schedule_iteration(iteration.id)
    assert tasks[2].end_date < tasks[0].start_date
    assert_dependency_dates(tasks, [(0, 1)])
    assert tasks[1].end_date < tasks[3].start_date
    assert tasks[1].end_date <= tasks[1].max_end_date


async def test_row_stays_serial_after_iteration_overflow(db_session):
    iteration, _, tasks = await make_plan(db_session, 1, [0, 0, 0], [], end=date(2026, 1, 5))
    tasks[0].min_start_date = date(2026, 1, 12)
    tasks[0].max_end_date = date(2026, 1, 14)
    tasks[0].effort_hours = 16
    await db_session.commit()
    await SchedulerService(db_session).schedule_iteration(iteration.id)
    assert tasks[1].start_date > tasks[0].end_date
    assert tasks[2].start_date > tasks[1].end_date
    assert_serial_rows(tasks)


async def test_dependencies_preserve_calendars_time_off_modifiers_and_locked_dates(db_session):
    iteration, members, tasks = await make_plan(db_session, 2, [0, 1, 0], [(0, 1), (1, 2)])
    iteration.calendar.weekend_days = [4, 5]
    iteration.calendar.holidays = ["2026-01-07"]
    iteration.calendar.short_days = ["2026-01-08"]
    tasks[0].status = "active"
    tasks[0].start_date = tasks[0].end_date = date(2026, 1, 5)
    tasks[1].min_start_date = date(2026, 1, 6)
    tasks[1].max_end_date = date(2026, 1, 15)
    members[1].availability_percent = 50
    members[1].operational_utilization = 20
    members[1].professionalism_coefficient = 1.25
    db_session.add(Vacation(team_member_id=members[1].id, start_date=date(2026, 1, 6),
                            end_date=date(2026, 1, 6)))
    await db_session.commit()
    await SchedulerService(db_session).schedule_iteration(iteration.id)
    assert tasks[0].start_date == tasks[0].end_date == date(2026, 1, 5)
    assert tasks[1].start_date == date(2026, 1, 8)
    assert tasks[1].end_date == date(2026, 1, 12)
    assert_dependency_dates(tasks, [(0, 1), (1, 2)])
    assert_serial_rows(tasks)


async def test_reassigned_tasks_preview_and_apply_without_capacity_refusal(db_session):
    from app.routers.gantt import preview_iteration_schedule, schedule_iteration
    from app.schemas.gantt import ScheduleApplyRequest, SchedulePreviewRequest

    edges = [(0, 1), (1, 2), (2, 3)]
    iteration, members, tasks = await make_plan(db_session, 2, [0, 1, 0, 1], edges)
    iteration_id = iteration.id
    task_ids = [task.id for task in tasks]
    for index, task in enumerate(tasks):
        task.effort_hours = [10, 8, 10, 8][index]
        task.assignee_id = members[1].id
    await db_session.commit()
    preview = await preview_iteration_schedule(iteration_id, SchedulePreviewRequest(changes=[]),
                                               SchedulerService(db_session), db_session)
    assert set(preview.model_dump()) == {"input_revision", "input_planning_revision", "tasks",
                                         "overdue_task_ids", "schedule_result"}
    expected = {task.id: (task.start_date, task.end_date) for task in preview.tasks}
    assert_serial_rows([SimpleNamespace(id=task.id, title=task.title,
                       assignee_id=task.assignee.id, start_date=task.start_date, end_date=task.end_date)
                       for task in preview.tasks])
    for task_id in task_ids:
        task = await db_session.get(Task, task_id)
        assert task.start_date is None and task.end_date is None
    result = await schedule_iteration(iteration_id, SchedulerService(db_session), db_session,
        ScheduleApplyRequest(expected_revision=preview.input_revision,
                             expected_planning_revision=preview.input_planning_revision))
    assert result.success and not result.capacity_issues
    assert set(result.model_dump()) == {"success", "planning_revision", "capacity_issues", "decisions",
                                        "workload_balanced", "workload_issues", "unscheduled"}
    saved = [await db_session.get(Task, task_id) for task_id in task_ids]
    assert_dependency_dates(saved, edges)
    assert_serial_rows(saved)
    assert {task.id: (task.start_date, task.end_date) for task in saved} == expected
    assert all((task.baseline_start_date, task.baseline_end_date) == expected[task.id] for task in saved)


@pytest.mark.parametrize("missing_child", [False, True])
async def test_summary_predecessor_waits_for_current_child_dates(db_session, missing_child):
    iteration, _, tasks = await make_plan(db_session, 3, [0, 1, 2], [])
    summary = Task(title="Grouped work", iteration=iteration, is_summary=True,
                   start_date=date(2026, 1, 1), end_date=date(2026, 1, 1))
    db_session.add(summary)
    await db_session.flush()
    for task in tasks[:2]:
        task.parent_id = summary.id
        task.min_start_date = date(2026, 1, 12)
    if missing_child:
        tasks[0].effort_hours = None
    db_session.add(TaskDependency(task_id=tasks[2].id, depends_on_id=summary.id))
    await db_session.commit()
    result = await SchedulerService(db_session).schedule_iteration(iteration.id)
    if missing_child:
        assert tasks[2].start_date is None and tasks[2].end_date is None
        assert any(item.task_id == tasks[2].id and summary.title in item.message for item in result.unscheduled)
    else:
        assert tasks[2].start_date > max(task.end_date for task in tasks[:2])


@pytest.mark.parametrize("status", ["resolved", "closed", "canceled"])
@pytest.mark.parametrize("saved_dates", [
    (None, None),
    (date(2026, 2, 2), None),
    (None, date(2026, 2, 3)),
    (date(2026, 2, 2), date(2026, 2, 3)),
], ids=["undated", "start_only", "end_only", "dated"])
@pytest.mark.parametrize("planned_sibling", [False, True], ids=["finished_only", "mixed"])
async def test_finished_child_does_not_block_summary_dependents(
    db_session, status, saved_dates, planned_sibling,
):
    iteration, _, tasks = await make_plan(db_session, 3, [0, 1, 2], [])
    child, dependent, sibling = tasks
    summary = Task(title="Grouped work", iteration=iteration, is_summary=True)
    db_session.add(summary)
    await db_session.flush()
    child.parent_id = summary.id
    if status == "canceled":
        child.canceled_at = datetime(2026, 1, 4, tzinfo=timezone.utc)
    else:
        child.status = status
    child.start_date, child.end_date = saved_dates
    if planned_sibling:
        sibling.parent_id = summary.id
    sibling.min_start_date = date(2026, 1, 12)
    dependent.min_start_date = date(2026, 1, 6)
    db_session.add(TaskDependency(task_id=dependent.id, depends_on_id=summary.id))
    await db_session.commit()

    result = await SchedulerService(db_session).schedule_iteration(iteration.id)

    assert result.success and not result.unscheduled
    assert (child.start_date, child.end_date) == saved_dates
    assert dependent.start_date >= dependent.min_start_date
    assert dependent.end_date is not None
    if planned_sibling:
        assert dependent.start_date > sibling.end_date
    dated_children = [task for task in [child, sibling] if task.parent_id == summary.id
                      and task.start_date is not None and task.end_date is not None]
    if dated_children:
        assert summary.start_date == min(task.start_date for task in dated_children)
        assert summary.end_date == max(task.end_date for task in dated_children)
        assert dependent.start_date > summary.end_date
    else:
        assert summary.start_date is None and summary.end_date is None
        assert dependent.start_date == dependent.min_start_date


@pytest.mark.parametrize("status", ["resolved", "closed", "canceled"])
async def test_finished_undated_child_satisfies_nested_summaries(db_session, status):
    iteration, _, tasks = await make_plan(db_session, 2, [0, 1], [])
    child, dependent = tasks
    outer = Task(title="Outer group", iteration=iteration, is_summary=True)
    inner = Task(title="Inner group", iteration=iteration, is_summary=True, parent=outer)
    db_session.add_all([outer, inner])
    await db_session.flush()
    child.parent_id = inner.id
    if status == "canceled":
        child.canceled_at = datetime(2026, 1, 4, tzinfo=timezone.utc)
    else:
        child.status = status
    db_session.add(TaskDependency(task_id=dependent.id, depends_on_id=outer.id))
    await db_session.commit()

    result = await SchedulerService(db_session).schedule_iteration(iteration.id)

    assert result.success and not result.unscheduled
    assert child.start_date is None and child.end_date is None
    assert dependent.start_date == iteration.start_date
    assert dependent.end_date is not None


async def test_task_dependency_cycle_is_left_unscheduled(db_session):
    iteration, _, tasks = await make_plan(db_session, 2, [0, 1], [(0, 1), (1, 0)])
    result = await SchedulerService(db_session).schedule_iteration(iteration.id)
    assert {item.task_id for item in result.unscheduled} == {task.id for task in tasks}
    assert all(task.start_date is None and task.end_date is None for task in tasks)


async def test_planned_work_does_not_straddle_locked_work_on_short_days(db_session):
    iteration, _, tasks = await make_plan(db_session, 1, [0, 0], [])
    iteration.calendar.short_days = ["2026-01-06"]
    tasks[0].effort_hours = 16
    tasks[1].status = "active"
    tasks[1].start_date = tasks[1].end_date = date(2026, 1, 7)
    await db_session.commit()
    await SchedulerService(db_session).schedule_iteration(iteration.id)
    assert tasks[1].start_date == tasks[1].end_date == date(2026, 1, 7)
    assert tasks[0].start_date == date(2026, 1, 8)
    assert tasks[0].end_date == date(2026, 1, 9)
    assert_serial_rows(tasks)
