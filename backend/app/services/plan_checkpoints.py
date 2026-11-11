"""The six plan checkpoints people and the PM read, derived once on the server.

The plan page and the PM role skill use these ids, in this order. Each
checkpoint is ``done``, ``warn`` (usable but needs attention), ``todo`` (the
next thing to do), or ``blocked`` (an earlier checkpoint must be done first).
"""

from __future__ import annotations

from typing import Any

PLAN_CHECKPOINT_IDS = ("iteration", "team", "work", "blockers", "schedule", "review")


def plan_checkpoints(
    *,
    team_member_count: int,
    team_members_no_capacity: int,
    task_count: int,
    tasks_without_assignee: int,
    tasks_without_effort: int,
    has_schedule: bool,
    risk_count: int,
) -> list[dict[str, Any]]:
    """Return the ordered checkpoints for one existing planning period."""

    def checkpoint(identifier: str, state: str, *codes: str, **counts: int) -> dict[str, Any]:
        return {
            "id": identifier,
            "state": state,
            "reason_codes": list(codes),
            "counts": {key: value for key, value in counts.items() if value},
        }

    # The summary is always for an existing iteration, so its period is set.
    items = [checkpoint("iteration", "done")]
    if team_member_count == 0:
        items.append(checkpoint("team", "todo", "no_people"))
    elif team_members_no_capacity > 0:
        items.append(checkpoint("team", "warn", "people_without_capacity", people_without_capacity=team_members_no_capacity))
    else:
        items.append(checkpoint("team", "done", people=team_member_count))
    items.append(checkpoint("work", "todo", "no_tasks") if task_count == 0 else checkpoint("work", "done", tasks=task_count))
    if task_count == 0:
        items.append(checkpoint("blockers", "blocked", "add_work_first"))
    elif tasks_without_assignee or tasks_without_effort:
        codes = [code for code, count in (("unassigned_tasks", tasks_without_assignee), ("tasks_without_effort", tasks_without_effort)) if count]
        items.append(checkpoint("blockers", "warn", *codes, unassigned_tasks=tasks_without_assignee, tasks_without_effort=tasks_without_effort))
    else:
        items.append(checkpoint("blockers", "done"))
    if not all(item["state"] == "done" for item in items):
        items.append(checkpoint("schedule", "blocked", "complete_earlier_checkpoints"))
    elif not has_schedule:
        items.append(checkpoint("schedule", "todo", "schedule_not_built"))
    else:
        items.append(checkpoint("schedule", "done"))
    if items[-1]["state"] != "done":
        items.append(checkpoint("review", "blocked", "build_schedule_first"))
    elif risk_count > 0:
        items.append(checkpoint("review", "warn", "risks_to_acknowledge", risks=risk_count))
    else:
        items.append(checkpoint("review", "done"))
    return items
