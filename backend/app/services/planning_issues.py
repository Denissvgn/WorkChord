"""One rule for the planning gaps people and the PM see: "needs an assignee" and "missing effort".

The scheduler places only planned leaf work, so a task is a scheduling gap only
while it is planned, a leaf, and not deferred. A task an agent is already
working on is "Agent working · no capacity row", not unassigned.
"""

from __future__ import annotations

from math import isfinite
from typing import Any

PLANNING_ISSUE_STATUS = "planned"
LIVE_EXECUTION_ASSIGNMENT_STATES = ("queued", "accepted")


def is_planning_gap_candidate(task: Any) -> bool:
    """A planned, non-deferred leaf: the only work the scheduler places."""
    deferred = getattr(task, "effective_is_deferred", None)
    if deferred is None:
        deferred = getattr(task, "is_deferred", False)
    return (
        getattr(task, "status", None) == PLANNING_ISSUE_STATUS
        and not deferred
        and not getattr(task, "is_composite", False)
        and not getattr(task, "children", None)
    )


def _agent_working(task: Any) -> bool:
    """Whether an agent holds live execution work: a response's ``agent_working`` field,
    or the flag TaskService.load_owner_names attaches to loaded ORM tasks."""
    working = getattr(task, "agent_working", None)
    if working is None:
        working = getattr(task, "__dict__", {}).get("_agent_working")
    return bool(working)


def needs_assignee(task: Any) -> bool:
    return is_planning_gap_candidate(task) and task.assignee is None and not _agent_working(task)


def agent_working_without_capacity(task: Any) -> bool:
    return is_planning_gap_candidate(task) and task.assignee is None and _agent_working(task)


def missing_effort(task: Any) -> bool:
    effort = getattr(task, "effort_days", None)
    invalid = isinstance(effort, bool) or not isinstance(effort, (int, float)) or not isfinite(effort) or effort <= 0
    return is_planning_gap_candidate(task) and invalid
