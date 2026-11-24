"""Saved dependency order: persisted dates that start a dependent before its prerequisite ends."""
from datetime import date, datetime, UTC

import pytest
from sqlalchemy import select

from app import mcp_agent_tools
from app.models.task import Task, TaskDependency, TaskStatus
from app.models.team_member import TeamMemberProfile
from app.routers.gantt import get_gantt_data
from app.services.iteration_service import IterationService
from tests.test_profile_capacity import allocation, db_session  # noqa: F401


def _task(member, title, start, end, **extra):
    return Task(title=title, iteration_id=member.iteration_id, assignee_id=member.id, effort_hours=6,
                nominal_day_hours=6, start_date=start, end_date=end, **extra)


@pytest.fixture(autouse=True)
def _today_inside_the_iteration(monkeypatch):
    monkeypatch.setattr("app.services.work_metrics.working_today", lambda *_args, **_kw: date(2026, 9, 28))


async def _saved_plan(db, *, noise=True):
    member = await allocation(db, profile=TeamMemberProfile(display_name="Owner"))
    first = _task(member, "Verify", date(2026, 9, 28), date(2026, 9, 30))
    ordered = _task(member, "Ordered next", date(2026, 10, 1), date(2026, 10, 1))
    same_day = _task(member, "Starts on its prerequisite's last day", date(2026, 9, 30), date(2026, 10, 1))
    earlier = _task(member, "Starts before its prerequisite", date(2026, 9, 29), date(2026, 9, 29))
    db.add_all([first, ordered, same_day, earlier])
    edges = [(ordered, first), (same_day, first), (earlier, first)]
    if noise:
        backlog = _task(member, "Backlog item", date(2026, 9, 28), date(2026, 9, 28), is_deferred=True)
        canceled = _task(member, "Canceled item", date(2026, 9, 28), date(2026, 9, 28),
                         canceled_at=datetime(2026, 9, 27, tzinfo=UTC))
        finished = _task(member, "Finished prerequisite", date(2026, 9, 29), date(2026, 10, 2),
                         status=TaskStatus.CLOSED.value)
        started = _task(member, "Started dependent", date(2026, 9, 29), date(2026, 9, 29),
                        status=TaskStatus.ACTIVE.value)
        db.add_all([backlog, canceled, finished, started])
        await db.flush()
        edges += [(backlog, first), (first, backlog), (canceled, first), (first, canceled),
                  (ordered, finished), (started, first)]
    await db.flush()
    db.add_all(TaskDependency(task_id=a.id, depends_on_id=b.id) for a, b in edges)
    await db.commit()
    return member, first, same_day, earlier


async def _snapshot(db):
    rows = (await db.scalars(select(Task).order_by(Task.id))).all()
    return [(t.id, t.start_date, t.end_date, t.version) for t in rows]


@pytest.mark.asyncio
async def test_readiness_lists_inverted_pairs_and_the_schedule_checkpoint_waits(db_session):
    member, first, same_day, earlier = await _saved_plan(db_session)
    before = await _snapshot(db_session)

    readiness = await IterationService(db_session).get_planning_readiness_summary(member.iteration_id)

    assert {(p.task_id, p.prerequisite_id) for p in readiness.inverted_dependencies} == {
        (same_day.id, first.id), (earlier.id, first.id)}
    pair = next(p for p in readiness.inverted_dependencies if p.task_id == earlier.id)
    assert (pair.task_start_date, pair.prerequisite_end_date) == (date(2026, 9, 29), date(2026, 9, 30))
    schedule = next(item for item in readiness.checkpoints if item.id == "schedule")
    assert schedule.state == "todo"
    assert schedule.reason_codes == ["saved_dependencies_inverted"]
    assert schedule.counts == {"inverted_dependencies": 2}
    assert await _snapshot(db_session) == before


@pytest.mark.asyncio
async def test_gantt_rest_and_mcp_flag_the_same_pairs_without_writing(db_session):
    member, first, same_day, earlier = await _saved_plan(db_session)
    before = await _snapshot(db_session)

    rest = await get_gantt_data(member.iteration_id, db_session)
    mcp = await mcp_agent_tools.get_iteration_gantt(db_session, member.iteration_id)

    expected = {(same_day.id, first.id), (earlier.id, first.id)}
    assert {(p.task_id, p.prerequisite_id) for p in rest.inverted_dependencies} == expected
    assert {(p["task_id"], p["prerequisite_id"]) for p in mcp["inverted_dependencies"]} == expected
    flagged = {task.id for task in rest.tasks if task.has_inverted_dependency}
    assert flagged == {same_day.id, earlier.id}
    assert {task["id"] for task in mcp["tasks"] if task["has_inverted_dependency"]} == flagged
    assert await _snapshot(db_session) == before


@pytest.mark.asyncio
async def test_correctly_ordered_saved_dates_leave_the_schedule_checkpoint_done(db_session):
    member, first, same_day, earlier = await _saved_plan(db_session, noise=False)
    for task_id, start, end in ((same_day.id, date(2026, 10, 1), date(2026, 10, 1)),
                                (earlier.id, date(2026, 10, 1), date(2026, 10, 2))):
        row = await db_session.get(Task, task_id)
        row.start_date, row.end_date = start, end
    await db_session.commit()

    readiness = await IterationService(db_session).get_planning_readiness_summary(member.iteration_id)
    gantt = await get_gantt_data(member.iteration_id, db_session)

    assert readiness.inverted_dependencies == [] and gantt.inverted_dependencies == []
    assert next(item for item in readiness.checkpoints if item.id == "schedule").state == "done"
    assert not any(task.has_inverted_dependency for task in gantt.tasks)
