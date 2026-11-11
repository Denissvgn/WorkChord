"""The "needs an assignee" and "missing effort" rule shared by counts and filters."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from app.services.planning_issues import (
    agent_working_without_capacity,
    missing_effort,
    needs_assignee,
)


def _task(**overrides):
    values = dict(status="planned", assignee=None, effort_days=2, is_deferred=False,
                  effective_is_deferred=None, is_composite=False, children=[], agent_working=False)
    values.update(overrides)
    return SimpleNamespace(**values)


def test_planned_leaf_without_assignee_needs_one() -> None:
    assert needs_assignee(_task())


@pytest.mark.parametrize("status", ["active", "resolved", "closed"])
def test_started_or_finished_work_is_not_a_scheduling_gap(status) -> None:
    assert not needs_assignee(_task(status=status))
    assert not missing_effort(_task(status=status, effort_days=None))


@pytest.mark.parametrize("overrides", [{"is_deferred": True}, {"effective_is_deferred": True}, {"is_composite": True}, {"children": [object()]}])
def test_deferred_and_parent_tasks_are_excluded(overrides) -> None:
    assert not needs_assignee(_task(**overrides))


def test_agent_held_work_is_not_unassigned() -> None:
    task = _task(agent_working=True)
    assert not needs_assignee(task)
    assert agent_working_without_capacity(task)


@pytest.mark.parametrize("effort", [None, 0, -1, float("nan"), True])
def test_missing_effort(effort) -> None:
    assert missing_effort(_task(effort_days=effort))


def test_loaded_orm_tasks_read_the_attached_agent_flag() -> None:
    # TaskService.load_owner_names attaches the flag as __dict__["_agent_working"], not as an attribute.
    class LoadedTask:
        status, is_deferred, effective_is_deferred, is_composite, children, assignee = "planned", False, None, False, [], None
    task = LoadedTask()
    task.__dict__["_agent_working"] = True
    assert not needs_assignee(task)
    assert agent_working_without_capacity(task)
