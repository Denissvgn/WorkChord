"""Independent synthetic counterexamples for read-model and inherited policy parity."""
from datetime import UTC, date, datetime

import pytest
from sqlalchemy import select

from app.commands import PlanningConflict, command_transaction
from app.models.calendar import Calendar
from app.models.iteration import Iteration
from app.models.project import Project
from app.models.task import Task
from app.models.team_member import TeamMemberProfile, Vacation
from app.services import project_service, work_metrics
from app.services.capacity_service import CapacityService
from app.services.iteration_service import IterationService
from app.services.project_service import ProjectService
from app.services.scheduler_service import IncrementalScheduler, SchedulerService
from app.services.team_service import TeamService
from tests.test_profile_capacity import allocation, db_session


async def test_iteration_readiness_uses_actual_person_hours(db_session):
    member = await allocation(db_session, profile=TeamMemberProfile(display_name="Availability owner"))
    db_session.add_all([
        Vacation(team_member_id=member.id, start_date=date(2026, 9, 28), end_date=date(2026, 9, 29)),
        Vacation(team_member_id=member.id, start_date=date(2026, 9, 29), end_date=date(2026, 9, 30)),
    ])
    await db_session.commit()
    service = IterationService(db_session)
    capacity = await TeamService(db_session).calculate_capacity(member.id)
    assert capacity.hours == 11
    readiness = await service.get_planning_readiness_summary(member.iteration_id)
    assert readiness.team_capacity_hours == capacity.hours
    summary = await service.get_summary(member.iteration_id)
    # A legacy day remains explicitly normalized using the declared person calendar.
    assert summary.team_capacity_days == pytest.approx(capacity.hours / 6, abs=.05)


async def deferred_leaf(db):
    member = await allocation(db, profile=TeamMemberProfile(display_name="Scheduled owner"))
    parent = Task(title="Deferred grouping", iteration_id=member.iteration_id, is_summary=True,
        is_deferred=True, effort_hours=0, nominal_day_hours=6)
    db.add(parent)
    await db.flush()
    leaf = Task(title="Unflagged child", iteration_id=member.iteration_id, parent_id=parent.id,
        assignee_id=member.id, is_deferred=False, effort_hours=6, nominal_day_hours=6)
    db.add(leaf)
    await db.commit()
    return member.id, member.profile_id, member.iteration_id, leaf.id


async def test_schedule_preview_does_not_allocate_inherited_deferred_leaf(db_session):
    _, _, iteration_id, leaf_id = await deferred_leaf(db_session)
    before = (await db_session.get(Task, leaf_id)).version
    async with command_transaction(db_session, mode="preview"):
        result = await SchedulerService(db_session).schedule_iteration(iteration_id, commit=False)
        leaf = await db_session.get(Task, leaf_id)
        assert leaf.start_date is None and leaf.end_date is None
        assert leaf_id not in {decision.task_id for decision in result.decisions}
    assert (await db_session.get(Task, leaf_id)).version == before


async def test_capacity_projection_does_not_count_inherited_deferred_baseline(db_session):
    member_id, profile_id, _, leaf_id = await deferred_leaf(db_session)
    leaf = await db_session.get(Task, leaf_id)
    leaf.baseline_start_date = leaf.baseline_end_date = date(2026, 9, 28)
    await db_session.commit()
    projection = await CapacityService(db_session).projection(profile_id, date(2026, 9, 28), date(2026, 9, 28))
    assert projection["days"][0]["committed_effort_hours"] == 0
    workload = await TeamService(db_session).get_workload(member_id)
    assert workload.allocated_days == 0


async def test_incremental_schedule_excludes_inherited_deferred_work(db_session):
    _, _, iteration_id, leaf_id = await deferred_leaf(db_session)
    result = await IncrementalScheduler(SchedulerService(db_session))._reschedule_subset(iteration_id, {leaf_id})
    assert result.rescheduled_count == 0 and not result.decisions
    assert (await db_session.get(Task, leaf_id)).start_date is None


async def test_yaml_schedule_orders_inherited_optional_after_required_work(db_session):
    member = await allocation(db_session, profile=TeamMemberProfile(display_name="Scheduled owner"))
    parent = Task(title="Optional grouping", iteration_id=member.iteration_id, is_summary=True, is_optional=True)
    db_session.add(parent)
    await db_session.flush()
    optional = Task(title="Optional leaf", iteration_id=member.iteration_id, parent_id=parent.id,
        assignee_id=member.id, priority=0, effort_hours=6, nominal_day_hours=6)
    required = Task(title="Required leaf", iteration_id=member.iteration_id, assignee_id=member.id,
        priority=100, effort_hours=6, nominal_day_hours=6)
    db_session.add_all([optional, required])
    await db_session.commit()
    async with command_transaction(db_session, mode="preview"):
        await SchedulerService(db_session).schedule_iteration(member.iteration_id, commit=False)
        assert required.start_date < optional.start_date


async def test_readiness_reports_shared_booking_risk_without_private_task_details(db_session):
    profile = TeamMemberProfile(display_name="Shared person")
    first = await allocation(db_session, profile=profile)
    await allocation(db_session, profile=profile)
    summary = await IterationService(db_session).get_planning_readiness_summary(first.iteration_id)
    assert summary.task_count == 0 and summary.risk_count > 0


async def test_capacity_refuses_incomplete_ancestry_but_ignores_unrelated_scope(db_session):
    member = await allocation(db_session, profile=TeamMemberProfile(display_name="Capacity owner"))
    unrelated = await allocation(db_session, profile=TeamMemberProfile(display_name="Other owner"))
    broken = Task(title="Broken unrelated ancestry", iteration_id=unrelated.iteration_id)
    db_session.add(broken)
    await db_session.flush()
    broken.parent_id = broken.id
    await db_session.commit()
    assert (await IterationService(db_session).get_planning_readiness_summary(member.iteration_id)).task_count == 0
    with pytest.raises(PlanningConflict, match="ancestry"):
        await IterationService(db_session).get_planning_readiness_summary(unrelated.iteration_id)


@pytest.mark.parametrize("zone, expected_days", [("Asia/Tokyo", -1), ("America/Los_Angeles", 0)])
def test_project_target_risk_uses_declared_working_date(monkeypatch, zone, expected_days):
    instant = datetime(2026, 1, 20, 23, 30, tzinfo=UTC)
    class ServerDate(date):
        @classmethod
        def today(cls):
            return cls(2026, 1, 20)
    monkeypatch.setattr(project_service, "date", ServerDate)
    monkeypatch.setattr(work_metrics, "utc_now", lambda: instant)
    project = Project(name="Zoned delivery", timezone=zone, target_date=date(2026, 1, 20),
        start_date=date(2026, 1, 10), status="active")
    risk = ProjectService(None)._calculate_target_date_risk(project, total_tasks=1, completed_tasks=0,
        completion_percent=0, blocked_tasks=0, overdue_tasks=0, remaining_effort_days=1,
        task_start_date=date(2026, 1, 10), task_end_date=date(2026, 1, 20))
    assert risk[3] == expected_days
