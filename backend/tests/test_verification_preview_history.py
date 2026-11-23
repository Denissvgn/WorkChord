"""Verification previews keep assignment-based independence until the stricter policy is enabled."""

import json
from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest
from sqlalchemy import insert

from app.authority import Authority
from app.models.agent import AgentModelBinding, AgentRun, AgentTaskAssignment
from app.models.project import Project
from app.models.team_member import TeamMemberProfileSkill
from app.query_limits import CollectionLimitExceededError, MAX_BOUNDED_LIST_ITEMS
from app.schemas.agent_routing import AgentRoutingPreviewCreate
from app.services import agent_routing_service
from app.services.agent_routing_policy import ROUTING_DECISION_AUTHORITY
from app.services.agent_routing_service import AgentRoutingService
from app.services.identity_service import initialize_control_plane
from tests.test_agent_routing_service import _assessment_command, _command_context, _rollout, _routing_fixture
from tests.test_team_pm_dispatch import db_session_factory


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "db_session_factory",
    [
        pytest.param("sqlite", marks=pytest.mark.sqlite),
        pytest.param("postgresql", marks=[pytest.mark.postgresql, pytest.mark.allow_network]),
    ],
    indirect=True,
)
async def test_verification_preview_applies_execution_history_bound_only_for_strict_projects(
    db_session, profile_factory, actor_factory, team_member_factory, task_factory, monkeypatch
):
    pm, worker, task, _, catalog = await _routing_fixture(
        db_session, profile_factory, actor_factory, team_member_factory, task_factory
    )
    project = Project(name="Release verification")
    db_session.add(project)
    await db_session.flush()
    task.project_id, task.iteration.project_id, task.status = project.id, project.id, "resolved"
    profile = await profile_factory(assignment_modes=["verification"])
    db_session.add(
        TeamMemberProfileSkill(
            profile_id=profile.id,
            skill_key="backend-python",
            skill_name="Python Backend",
            category="engineering",
            level=4,
            interest=4,
            is_weakness=False,
        )
    )
    await team_member_factory(profile=profile, iteration=task.iteration)
    reviewer = await actor_factory(
        profile=profile, role="verifier", scopes=json.dumps(["verification:write", "assignments:read"])
    )
    db_session.add(AgentModelBinding(actor_id=reviewer.id, model_catalog_id=catalog.id, is_default=True))
    assignment = AgentTaskAssignment(
        task_id=task.id,
        actor_id=worker.id,
        task_version=task.version,
        purpose="execution",
        state="fulfilled",
        routing_snapshot=json.dumps(
            {
                "schema_version": "routing-decision-snapshot-v1",
                "authority": ROUTING_DECISION_AUTHORITY,
                "profile_id": worker.profile_id,
            }
        ),
    )
    db_session.add(assignment)
    await db_session.commit()

    routing = AgentRoutingService(db_session, rollout_service=_rollout("shadow"))
    command = _assessment_command(task_version=task.version).model_copy(update={"review_mode": "independent"})
    receipt = await routing.create_assessment(task.id, pm, command, _command_context("assess-task"))
    request = AgentRoutingPreviewCreate(
        purpose="verification",
        assessment_id=receipt.assessment.id,
        expected_task_version=task.version,
        reviewer_profile_id=reviewer.profile_id,
    )
    observed_at = datetime(2026, 7, 20, tzinfo=UTC)
    history = AsyncMock(wraps=agent_routing_service.review_history)
    monkeypatch.setattr(agent_routing_service, "review_history", history)
    before = await routing.preview_task_routing(task.id, pm, request, now=observed_at)
    assert before.recommended_candidate is not None and before.recommended_candidate.actor_id == reviewer.id

    await db_session.execute(
        insert(AgentRun),
        [
            {"task_id": task.id, "actor_id": worker.id, "assignment_id": assignment.id, "status": "failed"}
            for _ in range(MAX_BOUNDED_LIST_ITEMS + 1)
        ],
    )
    await db_session.commit()
    after = await routing.preview_task_routing(task.id, pm, request, now=observed_at)
    assert after.recommended_candidate == before.recommended_candidate
    assert after.input_digest == before.input_digest
    assert after.preview_digest == before.preview_digest
    history.assert_not_awaited()

    operator_id = await initialize_control_plane(db_session)
    db_session.info["authority"] = Authority(operator_id, "system", workspace_role="operator")
    project.require_different_review_publisher = True
    await db_session.commit()
    db_session.info.pop("authority")
    with pytest.raises(CollectionLimitExceededError) as blocked:
        await routing.preview_task_routing(task.id, pm, request, now=observed_at)
    assert blocked.value.detail()["resource"] == "task execution provenance"
    assert blocked.value.detail()["maximum"] == MAX_BOUNDED_LIST_ITEMS
    history.assert_awaited_once()
