"""The scheduler says which planned tasks it left without dates, and readiness says how to fix it."""

import pytest
from sqlalchemy import select

from app.models.task import Task
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
