"""Verification needs the selected verifier present, not every declared team actor."""

import json
from datetime import timedelta

import pytest

from app.authority import Authority
from app.config import get_settings
from app.models.agent import AgentActor, AgentTaskAssignment
from app.models.iteration import Iteration
from app.schemas.agent import AgentReviewVerdict, AgentTaskAssignmentCreate, ModelAwareAgentTaskAssignmentCreate
from app.schemas.agent_routing import AgentRoutingPreviewCreate
from app.services.agent_routing_service import AgentRoutingConflictError, AgentRoutingService
from app.services.agent_team_setup_service import AgentTeamSetupConflictError, AgentTeamSetupService
from app.services.agent_work_service import AgentWorkService
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


class Scene:
    """A resolved task, its team, and the ids that stay usable after a rollback."""

    def __init__(self, **values):
        self.__dict__.update(values)


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
        base.task.id, base.pm,
        _assessment_command(
            task_version=base.task.version,
            required_skill_levels={"security-review": 3},
            minimum_reasoning_tier=3,
            minimum_context_tier="large",
            axes={"reasoning": 3, "ambiguity": 2, "context_breadth": 2, "risk": 3, "verification_burden": 3},
            reason_codes=("security", "specialist-verification"),
        ),
        _command_context("assess-presence"),
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
    spare = next(actor for actor in team.actors.values() if actor.id not in {worker.id, reviewer.id, base.pm.id})
    return Scene(
        team=team, base=base, assessment=assessment, worker=worker, reviewer=reviewer, spare=spare,
        candidate=default_candidate(reviewer), pm=base.pm, task_id=base.task.id, task_version=base.task.version,
        reviewer_id=reviewer.id, spare_id=spare.id, pm_id=base.pm.id, profile_id=reviewer.profile_id,
        project_id=base.task.project_id,
    )


async def verification_preview(db, scene, *, actor=None):
    return await AgentRoutingService(db).preview_task_routing(
        scene.task_id, actor or scene.pm,
        AgentRoutingPreviewCreate(
            purpose="verification", assessment_id=scene.assessment.id, expected_task_version=scene.task_version,
            reviewer_profile_id=scene.profile_id, focus_actor_id=scene.reviewer_id,
        ),
    )


async def assign_verifier(db, scene, preview, key, *, principal=None):
    return await AgentWorkService(db).create_assignment(
        principal or scene.pm,
        ModelAwareAgentTaskAssignmentCreate(
            task_id=scene.task_id, actor_id=scene.reviewer_id, expected_task_version=scene.task_version,
            purpose="verification", reviewer_profile_id=scene.profile_id, assessment_id=scene.assessment.id,
            model_binding_id=preview.recommended_candidate.model_binding_id,
            model_binding_revision=preview.recommended_candidate.model_binding_revision,
            routing_preview_id=preview.preview_id, routing_preview_digest=preview.preview_digest,
            reason="Select the current verifier.",
        ),
        idempotency_key=key, rationale="Assign the verifier", correlation_id=f"corr-{key}",
    )


async def set_last_seen(db, actor_id, *, quiet):
    actor = await db.get(AgentActor, actor_id)
    actor.last_seen_at = utc_now() - timedelta(days=2) if quiet else utc_now()
    await db.commit()
    await reload_session_fixture(db)


async def set_enabled(db, actor_id, enabled):
    (await db.get(AgentActor, actor_id)).enabled = enabled
    await db.commit()
    await reload_session_fixture(db)


def pass_verdict(assignment_id, task_version, candidate):
    return AgentReviewVerdict(
        assignment_id=assignment_id, expected_task_version=task_version, verdict="pass",
        evidence={"checks": "passed"}, observed_model=candidate.binding.model_catalog.configured_model_alias,
    )


@database_engines
@pytest.mark.usefixtures("deployed_agent_skill_release", "qualified_model_aware_routing_test_context")
async def test_present_verifier_is_assigned_and_reviews_while_an_unrelated_actor_is_not(
    db_session, team_member_factory, task_factory,
):
    db = db_session
    scene = await resolved_task_with_team(db, team_member_factory, task_factory)
    await set_last_seen(db, scene.spare_id, quiet=True)
    boundary = await AgentTeamSetupService(db).membership_boundary(scene.pm_id)
    assert scene.reviewer_id in boundary.runtime_ready_actor_ids and scene.spare_id not in boundary.runtime_ready_actor_ids

    preview = await verification_preview(db, scene)
    assert preview.recommended_candidate.actor_id == scene.reviewer_id
    verification = await assign_verifier(db, scene, preview, "presence-verification")
    assert verification.state == "queued" and verification.actor_id == scene.reviewer_id

    reviewer = await db.get(AgentActor, scene.reviewer_id)
    response = await AgentWorkService(db).review(
        reviewer, pass_verdict(verification.id, scene.task_version, scene.candidate),
        idempotency_key="presence-verdict", rationale="Pass the review", correlation_id="corr-presence-verdict",
    )
    assert response.review_assignment.state == "fulfilled" and response.task.status == "closed"


@database_engines
@pytest.mark.usefixtures("deployed_agent_skill_release", "qualified_model_aware_routing_test_context")
async def test_verifier_that_goes_stale_after_assignment_is_refused_at_verdict_time(
    db_session, team_member_factory, task_factory,
):
    db = db_session
    scene = await resolved_task_with_team(db, team_member_factory, task_factory)
    preview = await verification_preview(db, scene)
    verification = await assign_verifier(db, scene, preview, "presence-stale-after")
    verification_id = verification.id
    await set_last_seen(db, scene.reviewer_id, quiet=True)
    reviewer = await db.get(AgentActor, scene.reviewer_id)
    with pytest.raises(AgentTeamSetupConflictError) as refused:
        await AgentWorkService(db).review(
            reviewer, pass_verdict(verification_id, scene.task_version, scene.candidate),
            idempotency_key="presence-late-verdict", rationale="Pass the review", correlation_id="corr-late",
        )
    assert refused.value.code == "agent_team_actor_outside_topology"
    assert refused.value.context["target_actor_id"] == scene.reviewer_id


@database_engines
@pytest.mark.usefixtures("deployed_agent_skill_release", "qualified_model_aware_routing_test_context")
async def test_absent_verifier_is_refused_with_the_non_ready_actors_and_the_rule(
    db_session, team_member_factory, task_factory,
):
    db = db_session
    scene = await resolved_task_with_team(db, team_member_factory, task_factory)
    preview = await verification_preview(db, scene)
    await set_last_seen(db, scene.reviewer_id, quiet=True)
    await set_last_seen(db, scene.spare_id, quiet=True)

    with pytest.raises(AgentRoutingConflictError) as unavailable:
        await verification_preview(db, scene)
    detail = unavailable.value.detail()
    assert detail["code"] == "model_aware_routing_preview_unavailable"
    assert detail["topology_readiness"]["blocker_codes"] == ["verifier_not_runtime_ready"]
    assert "role, scopes, profile and model bindings" in detail["readiness_rule"]
    assert "polled its queue within the last" in detail["readiness_rule"]
    rows = {row["actor_id"]: row for row in detail["non_ready_actors"]}
    assert set(rows) == {scene.reviewer_id, scene.spare_id}
    assert rows[scene.reviewer_id]["blocks_this_request"] is True and rows[scene.spare_id]["blocks_this_request"] is False
    assert rows[scene.spare_id]["blocker_codes"] == ["runtime_stale"]
    assert rows[scene.spare_id]["last_ready_at"] == rows[scene.spare_id]["last_seen_at"] is not None

    with pytest.raises(AgentRoutingConflictError) as enforced:
        await assign_verifier(db, scene, preview, "presence-absent-verifier")
    assert enforced.value.code == "model_aware_routing_enforcement_unavailable"
    assert {row["actor_id"] for row in enforced.value.context["non_ready_actors"]} == {scene.reviewer_id, scene.spare_id}
    assert "polled its queue within the last" in enforced.value.context["readiness_rule"]
    await reload_session_fixture(db)

    # The supervised path refuses the same absent verifier by its own presence.
    with pytest.raises(AgentTeamSetupConflictError) as outside:
        await AgentWorkService(db).create_assignment(
            scene.pm,
            AgentTaskAssignmentCreate(
                task_id=scene.task_id, actor_id=scene.reviewer_id, expected_task_version=scene.task_version,
                purpose="verification",
            ),
            idempotency_key="presence-supervised", rationale="Assign the absent verifier",
            correlation_id="presence-supervised",
        )
    detail = outside.value.detail()
    assert detail["code"] == "agent_team_actor_outside_topology"
    assert detail["target_actor_id"] == scene.reviewer_id
    assert detail["maximum_runtime_staleness_seconds"] > 0
    assert {row["actor_id"]: row["blocks_this_request"] for row in detail["non_ready_actors"]} == {
        scene.reviewer_id: True, scene.spare_id: False,
    }


@database_engines
@pytest.mark.usefixtures("deployed_agent_skill_release", "qualified_model_aware_routing_test_context")
async def test_caller_must_hold_its_own_readiness_apart_from_a_recent_poll(
    db_session, team_member_factory, task_factory,
):
    db = db_session
    scene = await resolved_task_with_team(db, team_member_factory, task_factory)
    await set_last_seen(db, scene.spare_id, quiet=True)
    setup = AgentTeamSetupService(db)

    # A drifted caller is refused even though the verifier is present.
    await set_enabled(db, scene.pm_id, False)
    pm = await db.get(AgentActor, scene.pm_id)
    readiness, detail = await setup.readiness_gate(pm, verifier_actor_id=scene.reviewer_id, project_id=scene.project_id)
    assert readiness.blocker_codes == ("caller_not_runtime_ready",)
    flagged = {row["actor_id"] for row in detail["non_ready_actors"] if row["blocks_this_request"]}
    assert scene.pm_id in flagged

    # A caller that only has not polled lately is accepted.
    await set_enabled(db, scene.pm_id, True)
    await set_last_seen(db, scene.pm_id, quiet=True)
    pm = await db.get(AgentActor, scene.pm_id)
    readiness, detail = await setup.readiness_gate(pm, verifier_actor_id=scene.reviewer_id, project_id=scene.project_id)
    assert readiness.status.value == "ready" and detail == {}


@database_engines
@pytest.mark.usefixtures("deployed_agent_skill_release", "qualified_model_aware_routing_test_context")
async def test_verifier_outside_the_callers_team_and_unbound_callers(
    db_session, actor_factory, team_member_factory, task_factory, monkeypatch,
):
    db = db_session
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "trusted_local")
    get_settings.cache_clear()
    scene = await resolved_task_with_team(db, team_member_factory, task_factory)
    other = await provision_ready_topology(db, two_workers=False, prefix="other")
    outsider_id = other.actors[other.manifest.verifiers[0].actor_key].id
    await set_last_seen(db, scene.spare_id, quiet=True)
    setup = AgentTeamSetupService(db)

    # Not in the caller's team: named explicitly, and only the caller's own team is described.
    pm = await db.get(AgentActor, scene.pm_id)
    readiness, detail = await setup.readiness_gate(pm, verifier_actor_id=outsider_id, project_id=scene.project_id)
    assert readiness.blocker_codes == ("verifier_outside_topology",)
    assert {row["actor_id"] for row in detail["non_ready_actors"]} == {scene.spare_id}

    # An actor in no team is judged by the verifier's team only with authority over the project.
    unbound = await actor_factory(role="pm", scopes=json.dumps(["assignments:write", "planning:write"]))
    await db.commit()
    unbound = await db.get(AgentActor, unbound.id)
    present, none = await setup.readiness_gate(unbound, verifier_actor_id=scene.reviewer_id, project_id=scene.project_id)
    assert present.status.value == "ready" and none == {}
    await set_last_seen(db, scene.reviewer_id, quiet=True)
    stale, detail = await setup.readiness_gate(unbound, verifier_actor_id=scene.reviewer_id, project_id=scene.project_id)
    assert stale.blocker_codes == ("verifier_not_runtime_ready",)
    assert {row["actor_id"] for row in detail["non_ready_actors"]} == {scene.reviewer_id, scene.spare_id}
    nobody = await actor_factory(role="verifier", scopes=json.dumps(["verification:write"]))
    await db.commit()
    unbound = await db.get(AgentActor, unbound.id)
    unknown, detail = await setup.readiness_gate(unbound, verifier_actor_id=nobody.id, project_id=scene.project_id)
    assert unknown.status.value == "unavailable" and detail == {}

    # Without authority over the project nothing is narrowed and no roster is described.
    db.info["authority"] = Authority(principal_id=1, kind="human", workspace_role="member", projects={})
    try:
        denied, detail = await setup.readiness_gate(unbound, verifier_actor_id=scene.reviewer_id, project_id=scene.project_id)
    finally:
        db.info.pop("authority")
    assert denied.status.value == "unavailable" and detail == {}


@database_engines
@pytest.mark.usefixtures("deployed_agent_skill_release", "qualified_model_aware_routing_test_context")
async def test_preview_checks_the_caller_and_task_before_describing_any_team(
    db_session, actor_factory, team_member_factory, task_factory, monkeypatch,
):
    db = db_session
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "trusted_local")
    get_settings.cache_clear()
    scene = await resolved_task_with_team(db, team_member_factory, task_factory)
    await set_last_seen(db, scene.reviewer_id, quiet=True)
    await set_last_seen(db, scene.spare_id, quiet=True)
    body = AgentRoutingPreviewCreate(
        purpose="verification", assessment_id=scene.assessment.id, expected_task_version=scene.task_version,
        reviewer_profile_id=scene.profile_id, focus_actor_id=scene.reviewer_id,
    )
    executor = await actor_factory(role="worker", scopes=json.dumps(["work:execute"]))
    reader = await actor_factory(role="pm", scopes=json.dumps(["planning:read"]))
    await db.commit()
    from app.services.agent_service import AgentPermissionError

    with pytest.raises(AgentPermissionError):
        await AgentRoutingService(db).preview_task_routing(999999, await db.get(AgentActor, executor.id), body)
    with pytest.raises(LookupError):
        await AgentRoutingService(db).preview_task_routing(999999, await db.get(AgentActor, reader.id), body)
