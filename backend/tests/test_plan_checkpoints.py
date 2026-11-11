"""People and the PM read the same six plan checkpoints from the server."""

from __future__ import annotations

import pytest

from app.services.plan_checkpoints import PLAN_CHECKPOINT_IDS, plan_checkpoints

READY = dict(
    team_member_count=3,
    team_members_no_capacity=0,
    task_count=8,
    tasks_without_assignee=0,
    tasks_without_effort=0,
    has_schedule=True,
    risk_count=0,
)


def _states(**overrides):
    return {item["id"]: item["state"] for item in plan_checkpoints(**{**READY, **overrides})}


def test_checkpoints_follow_the_plan_page_order() -> None:
    assert [item["id"] for item in plan_checkpoints(**READY)] == list(PLAN_CHECKPOINT_IDS)
    assert set(_states().values()) == {"done"}


def test_an_empty_iteration_starts_with_people_and_work() -> None:
    states = _states(team_member_count=0, task_count=0, has_schedule=False)
    assert states == {
        "iteration": "done",
        "team": "todo",
        "work": "todo",
        "blockers": "blocked",
        "schedule": "blocked",
        "review": "blocked",
    }


def test_blockers_name_what_is_missing_and_hold_the_schedule() -> None:
    items = {item["id"]: item for item in plan_checkpoints(**{**READY, "tasks_without_assignee": 4, "has_schedule": False})}
    assert items["blockers"]["state"] == "warn"
    assert items["blockers"]["reason_codes"] == ["unassigned_tasks"]
    assert items["blockers"]["counts"] == {"unassigned_tasks": 4}
    assert items["schedule"]["state"] == "blocked"
    assert items["review"]["state"] == "blocked"


@pytest.mark.parametrize(
    ("overrides", "checkpoint", "state"),
    [
        ({"team_members_no_capacity": 1}, "team", "warn"),
        ({"has_schedule": False}, "schedule", "todo"),
        ({"risk_count": 2}, "review", "warn"),
    ],
)
def test_single_gaps_mark_one_checkpoint(overrides, checkpoint, state) -> None:
    assert _states(**overrides)[checkpoint] == state


@pytest.mark.asyncio
async def test_agents_can_read_plan_readiness_over_rest_and_mcp() -> None:
    from app.main import app
    from app.mcp_server import mcp

    paths = app.openapi()["paths"]
    assert "get" in paths["/api/agent/planning/iterations/{iteration_id}/readiness"]
    assert "agent_get_iteration_plan_readiness" in {tool.name for tool in await mcp.list_tools()}
