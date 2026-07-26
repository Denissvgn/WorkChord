"""Smoke tests for the isolated routing database harness."""

from __future__ import annotations

from collections.abc import Awaitable, Callable
import socket
from typing import Any

import pytest
from sqlalchemy import func, select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent import AgentActor
from app.models.calendar import Calendar
from app.models.iteration import Iteration
from app.models.task import Task
from app.models.team_member import TeamMember, TeamMemberProfile


Factory = Callable[..., Awaitable[Any]]


async def _build_routing_graph(
    *,
    profile_factory: Factory,
    actor_factory: Factory,
    team_member_factory: Factory,
    task_factory: Factory,
) -> tuple[TeamMemberProfile, AgentActor, TeamMember, Task]:
    profile = await profile_factory(
        seed_key="routing-harness-profile",
        display_name="Routing Harness Profile",
    )
    actor = await actor_factory(
        profile=profile,
        name="routing-harness-actor",
        display_name="Routing Harness Actor",
        api_key_hash="routing-harness-key-hash",
    )
    capacity_owner = await team_member_factory(
        profile=profile,
        name="Routing Harness Capacity Owner",
    )
    task = await task_factory(
        assignee=capacity_owner,
        title="Routing Harness Task",
    )
    return profile, actor, capacity_owner, task


@pytest.mark.contract
@pytest.mark.sqlite
@pytest.mark.parametrize("isolated_case", (1, 2))
async def test_routing_factories_build_an_isolated_foreign_key_graph(
    isolated_case: int,
    db_session: AsyncSession,
    profile_factory: Factory,
    actor_factory: Factory,
    team_member_factory: Factory,
    task_factory: Factory,
) -> None:
    profile, actor, capacity_owner, task = await _build_routing_graph(
        profile_factory=profile_factory,
        actor_factory=actor_factory,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
    )

    assert isolated_case in {1, 2}
    assert await db_session.scalar(text("PRAGMA foreign_keys")) == 1
    assert actor.profile_id == profile.id
    assert capacity_owner.profile_id == profile.id
    assert task.assignee_id == capacity_owner.id
    assert task.iteration_id == capacity_owner.iteration_id

    expected_counts = {
        Calendar: 1,
        Iteration: 1,
        TeamMemberProfile: 1,
        AgentActor: 1,
        TeamMember: 1,
        Task: 1,
    }
    for model, expected in expected_counts.items():
        count = await db_session.scalar(
            select(func.count()).select_from(model)
        )
        assert count == expected


@pytest.mark.contract
def test_routing_harness_blocks_unapproved_network() -> None:
    with pytest.raises(AssertionError, match="Network access is disabled"):
        socket.create_connection(("example.invalid", 443))
