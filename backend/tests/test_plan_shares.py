"""Plan-share ownership and immutable snapshot behavior."""

from datetime import date

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.calendar import Calendar
from app.models.iteration import Iteration
from app.models.task import Task
from app.models.team_member import TeamMember
from app.models.user_session import UserSession
from app.services.plan_share_service import PlanShareService


@pytest.mark.asyncio
async def test_plan_share_replaces_owner_link_with_new_immutable_snapshot(
    db_session: AsyncSession,
) -> None:
    calendar = Calendar(name="Delivery", year=2026)
    iteration = Iteration(
        name="August launch",
        start_date=date(2026, 8, 3),
        end_date=date(2026, 8, 14),
        calendar=calendar,
    )
    owner = UserSession(
        public_id="shareowner01",
        ip_address="127.0.0.1",
        user_agent="pytest",
    )
    other_session = UserSession(
        public_id="shareviewer1",
        ip_address="127.0.0.2",
        user_agent="pytest",
    )
    member = TeamMember(
        name="Ada Lovelace",
        position="Engineer",
        iteration=iteration,
    )
    task = Task(
        title="Prepare launch",
        iteration=iteration,
        assignee=member,
        priority=2,
        effort_days=2,
        effort_hours=16,
        start_date=date(2026, 8, 3),
        end_date=date(2026, 8, 4),
    )
    db_session.add_all([calendar, iteration, owner, other_session, member, task])
    await db_session.commit()

    service = PlanShareService(db_session)
    first = await service.create(iteration.id, owner)
    assert first is not None
    first_public_id = first.public_id
    assert first.snapshot_data["iteration"]["name"] == "August launch"
    assert first.snapshot_data["tasks"][0]["title"] == "Prepare launch"
    assert first.snapshot_data["tasks"][0]["assignee_name"] == "Ada Lovelace"
    assert "description" not in first.snapshot_data["tasks"][0]
    assert "professionalism_coefficient" not in first.snapshot_data["team_members"][0]

    task.title = "Prepare launch checklist"
    await db_session.commit()
    second = await service.create(iteration.id, owner)

    assert second is not None
    assert second.public_id != first_public_id
    assert second.snapshot_data["tasks"][0]["title"] == "Prepare launch checklist"
    assert await service.get_active_by_public_id(first_public_id) is None
    assert (
        await service.get_owned_current(iteration.id, owner.id)
    ).id == second.id
    assert await service.revoke(second.id, other_session.id) is False
    assert await service.revoke(second.id, owner.id) is True
    assert await service.get_active_by_public_id(second.public_id) is None


@pytest.mark.asyncio
async def test_plan_share_missing_iteration_returns_none(
    db_session: AsyncSession,
) -> None:
    owner = UserSession(
        public_id="missingowner",
        ip_address="127.0.0.3",
        user_agent="pytest",
    )
    db_session.add(owner)
    await db_session.commit()

    assert await PlanShareService(db_session).create(999_999, owner) is None
