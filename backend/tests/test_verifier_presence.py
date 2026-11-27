"""Verification needs the selected verifier present, not every declared team actor."""

from datetime import timedelta

import pytest

from app.config import get_settings
from app.models.agent import AgentTaskAssignment
from app.models.iteration import Iteration
from app.schemas.agent import AgentTaskAssignmentCreate
from app.schemas.agent_routing import AgentRoutingPreviewCreate
from app.services.agent_routing_service import AgentRoutingConflictError, AgentRoutingService
from app.services.agent_work_service import AgentWorkService
from app.services.agent_team_setup_service import AgentTeamSetupConflictError, AgentTeamSetupService
from app.utils.time import utc_now
from tests.support.transactions import reload_session_fixture
from tests.test_agent_routing_service import _command_context
from tests.test_agent_routing_wave6_qualification import _assessment_command, _dispatch
from tests.test_agent_team_setup_qualification import default_candidate, provision_ready_topology, routing_base
from tests.test_review_provenance import database_engines


@pytest.fixture(autouse=True)
def restore_settings_cache():
    yield
    get_settings.cache_clear()


async def resolved_task_with_team(db, team_member_factory, task_factory):
    team = await provision_ready_topology(db)
    worker = team.actors["operations-worker"]
    reviewer = team.actors["independent-verifier"]
    base = await routing_base(
        db, topology=team, actor_key="operations-worker", team_member_factory=team_member_factory,
        task_factory=task_factory, title="Review the bounded change", skill_key="security-review",
    )
    iteration = await db.get(Iteration, base.task.iteration_id)
    await team_member_factory(profile=reviewer.profile, iteration=iteration)
    service = AgentRoutingService(db)
    assessment = (await service.create_assessment(
        base.task.id, base.pm, _assessment_command(
            task_version=base.task.version,
            required_skill_levels={"security-review": 3},
            minimum_reasoning_tier=3,
            minimum_context_tier="large",
            axes={"reasoning": 3, "ambiguity": 2, "context_breadth": 2, "risk": 3, "verification_burden": 3},
            reason_codes=("security", "specialist-verification"),
        ), _command_context("assess-presence"),
    )).assessment
    preview = await service.preview_task_routing(
        base.task.id, base.pm,
        AgentRoutingPreviewCreate(purpose="execution", assessment_id=assessment.id, expected_task_version=base.task.version),
    )
    execution = await _dispatch(
        db, base=base, assessment=assessment, preview=preview, candidate=default_candidate(worker), key="presence-execution",
    )
    (await db.get(AgentTaskAssignment, execution.id)).state = "fulfilled"
    base.task.status = "resolved"
    await db.commit()
    return team, base, assessment, worker, reviewer


async def verification_preview(db, base, assessment, reviewer):
    return await AgentRoutingService(db).preview_task_routing(
        base.task.id, base.pm,
        AgentRoutingPreviewCreate(
            purpose="verification", assessment_id=assessment.id, expected_task_version=base.task.version,
            reviewer_profile_id=reviewer.profile_id, focus_actor_id=reviewer.id,
        ),
    )


async def go_quiet(db, actor):
    actor.last_seen_at = utc_now() - timedelta(days=2)
    await db.commit()
    await reload_session_fixture(db)


def unrelated_actor(team, base, worker, reviewer):
    return next(actor for actor in team.actors.values() if actor.id not in {worker.id, reviewer.id, base.pm.id})


@database_engines
@pytest.mark.usefixtures("deployed_agent_skill_release", "qualified_model_aware_routing_test_context")
async def test_present_verifier_is_assignable_while_an_unrelated_actor_is_not(
    db_session, team_member_factory, task_factory,
):
    db = db_session
    team, base, assessment, worker, reviewer = await resolved_task_with_team(db, team_member_factory, task_factory)
    spare = unrelated_actor(team, base, worker, reviewer)
    await go_quiet(db, spare)
    boundary = await AgentTeamSetupService(db).membership_boundary(base.pm.id)
    assert reviewer.id in boundary.runtime_ready_actor_ids and spare.id not in boundary.runtime_ready_actor_ids

    preview = await verification_preview(db, base, assessment, reviewer)
    assert preview.recommended_candidate is not None and preview.recommended_candidate.actor_id == reviewer.id
    verification = await _dispatch(
        db, base=base, assessment=assessment, preview=preview, candidate=default_candidate(reviewer),
        key="presence-verification", purpose="verification", reviewer_profile_id=reviewer.profile_id,
    )
    assert verification.state == "queued" and verification.actor_id == reviewer.id


@database_engines
@pytest.mark.usefixtures("deployed_agent_skill_release", "qualified_model_aware_routing_test_context")
async def test_absent_verifier_is_refused_with_the_non_ready_actors_and_the_rule(
    db_session, team_member_factory, task_factory,
):
    db = db_session
    team, base, assessment, worker, reviewer = await resolved_task_with_team(db, team_member_factory, task_factory)
    preview = await verification_preview(db, base, assessment, reviewer)
    candidate = default_candidate(reviewer)
    reviewer_id, profile_id = reviewer.id, reviewer.profile_id
    task_id, task_version, pm = base.task.id, base.task.version, base.pm
    spare = unrelated_actor(team, base, worker, reviewer)
    spare_id = spare.id
    await go_quiet(db, reviewer)
    await go_quiet(db, spare)

    with pytest.raises(AgentRoutingConflictError) as unavailable:
        await verification_preview(db, base, assessment, reviewer)
    detail = unavailable.value.detail()
    assert detail["code"] == "model_aware_routing_preview_unavailable"
    assert detail["topology_readiness"]["blocker_codes"] == ["verifier_not_runtime_ready"]
    assert "polled its queue within the last" in detail["readiness_rule"]
    rows = {row["actor_id"]: row for row in detail["non_ready_actors"]}
    assert set(rows) == {reviewer_id, spare_id}
    assert rows[reviewer_id]["blocks_this_request"] is True and rows[spare_id]["blocks_this_request"] is False
    assert rows[spare_id]["blocker_codes"] == ["runtime_stale"]
    assert rows[spare_id]["last_ready_at"] == rows[spare_id]["last_seen_at"] is not None

    with pytest.raises(AgentRoutingConflictError) as enforced:
        await _dispatch(
            db, base=base, assessment=assessment, preview=preview, candidate=candidate,
            key="presence-absent-verifier", purpose="verification", reviewer_profile_id=profile_id,
        )
    assert enforced.value.code == "model_aware_routing_enforcement_unavailable"
    assert {row["actor_id"] for row in enforced.value.context["non_ready_actors"]} == {reviewer_id, spare_id}
    assert "polled its queue within the last" in enforced.value.context["readiness_rule"]
    await reload_session_fixture(db)

    # The supervised path refuses the same absent verifier by its own presence.
    with pytest.raises(AgentTeamSetupConflictError) as outside:
        await AgentWorkService(db).create_assignment(
            pm,
            AgentTaskAssignmentCreate(
                task_id=task_id, actor_id=reviewer_id, expected_task_version=task_version,
                purpose="verification",
            ),
            idempotency_key="presence-supervised", rationale="Assign the absent verifier",
            correlation_id="presence-supervised",
        )
    detail = outside.value.detail()
    assert detail["code"] == "agent_team_actor_outside_topology"
    assert detail["target_actor_id"] == reviewer_id
    assert "polled its queue within the last" in detail["readiness_rule"]
    assert detail["maximum_runtime_staleness_seconds"] > 0
    assert {row["actor_id"]: row["blocks_this_request"] for row in detail["non_ready_actors"]} == {
        reviewer_id: True, spare_id: False,
    }
