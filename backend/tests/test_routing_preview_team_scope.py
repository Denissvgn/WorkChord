"""A team-bound PM's routing preview carries only its own team's operational rows."""

import json

import pytest

from app.config import get_settings
from app.models.agent import AgentActor, AgentModelBinding, AgentModelCatalogEntry, AgentTaskAssignment
from app.models.iteration import Iteration
from app.schemas.agent import ModelAwareAgentTaskAssignmentCreate
from app.schemas.agent_routing import AgentRoutingPreviewCreate
from app.services import agent_routing_service
from app.services.agent_routing_service import AgentRoutingConflictError, AgentRoutingService
from app.services.agent_service import hash_api_key
from app.services.agent_team_setup_service import AgentTeamSetupConflictError
from app.services.agent_work_service import AgentWorkService
from app.services.task_service import TaskService
from app.utils.time import utc_now
from tests.support.transactions import reload_session_fixture
from tests.test_agent_routing_service import _command_context
from tests.test_agent_routing_wave6_qualification import _assessment_command, _dispatch
from tests.test_agent_team_setup_qualification import default_candidate, provision_ready_topology, routing_base
from tests.test_review_provenance import database_engines
from tests.test_scoped_review_evidence import through
from tests.test_team_pm_dispatch import db_session_factory as db_session_factory

OUTSIDE_ACTORS = 55
OPERATOR_KEY = "team-scope-test-operator"


@pytest.fixture(autouse=True)
def restore_settings_cache():
    yield
    get_settings.cache_clear()


def rows(preview):
    return [*preview["eligible_candidates"], *preview["exclusions"]]


def pairs(items):
    return {(row["actor_id"], row.get("model_binding_id")) for row in items}


@database_engines
@pytest.mark.usefixtures("deployed_agent_skill_release", "qualified_model_aware_routing_test_context")
async def test_team_pm_preview_excludes_other_teams_rows_on_rest_and_mcp(
    db_session,
    db_session_factory,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
    monkeypatch,
):
    db = db_session
    monkeypatch.setenv("WORKCHORD_AUTH_MODE", "trusted_local")
    get_settings.cache_clear()

    # Other actors exist first, so their lower identifiers sort ahead of the
    # team's own rows and fill the bounded exclusion list when left in.
    outside_catalog = AgentModelCatalogEntry(
        key="outside-runtime",
        provider="test-provider",
        configured_model_alias="outside-alias",
        reasoning_tier=1,
        context_tier="small",
        modality_tags=["text"],
        cost_tier="low",
        latency_tier="balanced",
        enabled=True,
        revision=1,
    )
    db.add(outside_catalog)
    outside_profile = await profile_factory(assignment_modes=["execution"])
    await db.flush()
    outsiders, outside_bindings = [], []
    for index in range(OUTSIDE_ACTORS):
        actor = await actor_factory(
            profile=outside_profile,
            name=f"outside-team-actor-{index}",
            display_name=f"Outside Team Actor {index}",
        )
        binding = AgentModelBinding(
            actor_id=actor.id, model_catalog_id=outside_catalog.id, is_default=True, enabled=True, revision=1
        )
        db.add(binding)
        outsiders.append(actor)
        outside_bindings.append(binding)
    await db.flush()

    team = await provision_ready_topology(db)
    worker = team.actors["operations-worker"]
    reviewer = team.actors["independent-verifier"]
    base = await routing_base(
        db,
        topology=team,
        actor_key="operations-worker",
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        title="Review the bounded security change",
        skill_key="security-review",
    )
    task, pm = base.task, base.pm
    iteration = await db.get(Iteration, task.iteration_id)
    await team_member_factory(profile=reviewer.profile, iteration=iteration)
    reviewer_binding = default_candidate(reviewer).binding

    # An actor outside the team that would otherwise match the named reviewer.
    lookalike = await actor_factory(
        profile=reviewer.profile,
        name="outside-team-lookalike-reviewer",
        display_name="Outside Team Lookalike Reviewer",
        role=reviewer.role,
        scopes=reviewer.scopes,
        lifecycle_state=reviewer.lifecycle_state,
        work_policy=reviewer.work_policy,
        max_parallel_work=reviewer.max_parallel_work,
    )
    lookalike_binding = AgentModelBinding(
        actor_id=lookalike.id,
        model_catalog_id=reviewer_binding.model_catalog_id,
        is_default=True,
        enabled=True,
        tool_tags=list(reviewer_binding.tool_tags or []),
        data_policy_tags=list(reviewer_binding.data_policy_tags or []),
        revision=1,
    )
    db.add(lookalike_binding)
    operator = await actor_factory(
        role="pm",
        name="team-scope-operator",
        display_name="Team Scope Operator",
        scopes=json.dumps(["admin"]),
        api_key_hash=hash_api_key(OPERATOR_KEY),
    )
    await db.commit()
    outside_actor_ids = {actor.id for actor in outsiders} | {lookalike.id, operator.id}
    outside_binding_ids = {binding.id for binding in outside_bindings} | {lookalike_binding.id}
    outside_names = [
        name for actor in (*outsiders, lookalike, operator) for name in (actor.name, actor.display_name)
    ]

    request = _assessment_command(
        task_version=task.version,
        required_skill_levels={"security-review": 3},
        minimum_reasoning_tier=3,
        minimum_context_tier="large",
        axes={"reasoning": 3, "ambiguity": 2, "context_breadth": 2, "risk": 3, "verification_burden": 3},
        reason_codes=("security", "specialist-verification"),
    )
    service = AgentRoutingService(db)
    assessment = (await service.create_assessment(task.id, pm, request, _command_context("assess-team-scope"))).assessment
    execution_preview = await service.preview_task_routing(
        task.id,
        pm,
        AgentRoutingPreviewCreate(
            purpose="execution", assessment_id=assessment.id, expected_task_version=task.version
        ),
    )
    execution = await _dispatch(
        db,
        base=base,
        assessment=assessment,
        preview=execution_preview,
        candidate=default_candidate(worker),
        key="team-scope-execution",
    )
    (await db.get(AgentTaskAssignment, execution.id)).state = "fulfilled"
    task.status = "resolved"
    other_task = await task_factory(iteration=iteration, title="Reviewer's current work")
    busy = AgentTaskAssignment(
        task_id=other_task.id, actor_id=reviewer.id, task_version=other_task.version, state="accepted"
    )
    db.add(busy)
    await db.commit()
    body = {
        "purpose": "verification",
        "assessment_id": assessment.id,
        "expected_task_version": task.version,
        "reviewer_profile_id": reviewer.profile_id,
    }
    now = utc_now().replace(microsecond=0)
    monkeypatch.setattr(agent_routing_service, "utc_now", lambda: now)

    async def read(transport, key):
        return await through(
            transport,
            db_session_factory,
            monkeypatch,
            "agent_preview_task_routing",
            f"/api/agent/tasks/{task.id}/routing-preview",
            key,
            body,
            task_id=task.id,
        )

    pm_key = team.sink.keys[team.manifest.controller.actor_key]
    team_ids = {actor.id for actor in team.actors.values()}

    def assert_team_only(preview):
        returned = rows(preview)
        assert {row["actor_id"] for row in returned} <= team_ids
        for row in returned:
            assert row["actor_id"] not in outside_actor_ids
            assert row["profile_id"] != outside_profile.id
            assert row.get("model_binding_id") not in outside_binding_ids
            assert row.get("model_catalog_id") != outside_catalog.id
        serialized = json.dumps(preview)
        assert not any(name in serialized for name in outside_names)

    async def both(key):
        rest = await read("rest", key)
        assert rest == await read("mcp", key)
        return rest

    # The named reviewer is busy, so its row is an exclusion. Other teams'
    # rows no longer crowd it out of the team PM's bounded response.
    scoped = await both(pm_key)
    full = await both(OPERATOR_KEY)
    assert_team_only(scoped)
    assert scoped["exclusions_omitted"] == 0 and scoped["recommended_candidate"] is None
    reviewer_row = next(row for row in scoped["exclusions"] if row["actor_id"] == reviewer.id)
    assert "current_work_conflict" in reviewer_row["hard_blocker_codes"]
    implementer_row = next(row for row in scoped["exclusions"] if row["actor_id"] == worker.id)
    assert "verification_actor_not_independent" in implementer_row["hard_blocker_codes"]
    # An operator without a team boundary keeps the full view; there the
    # other actors still sort first and the reviewer's row is trimmed.
    assert reviewer.id not in {row["actor_id"] for row in full["exclusions"]}
    assert full["exclusions_omitted"] > 0
    assert {row["actor_id"] for row in full["exclusions"]} & outside_actor_ids
    assert len(full["exclusions"]) + full["exclusions_omitted"] + len(full["eligible_candidates"]) == (
        len(scoped["exclusions"]) + len(outside_actor_ids)
    )
    # Filtering changes no eligibility: the lookalike is eligible only
    # without a team boundary, and no team row becomes eligible.
    assert pairs(scoped["eligible_candidates"]) == set()
    assert pairs(full["eligible_candidates"]) == {(lookalike.id, lookalike_binding.id)}
    assert scoped["preview_digest"] != full["preview_digest"]

    busy.state = "cancelled"
    await db.commit()
    scoped = await both(pm_key)
    full = await both(OPERATOR_KEY)
    assert_team_only(scoped)
    assert scoped["recommended_candidate"]["actor_id"] == reviewer.id
    team_eligible = {pair for pair in pairs(full["eligible_candidates"]) if pair[0] in team_ids}
    assert pairs(scoped["eligible_candidates"]) == team_eligible == {(reviewer.id, reviewer_binding.id)}
    assert (lookalike.id, lookalike_binding.id) in pairs(full["eligible_candidates"])
    implementer_row = next(row for row in scoped["exclusions"] if row["actor_id"] == worker.id)
    assert "verification_actor_not_independent" in implementer_row["hard_blocker_codes"]
    full_by_pair = {(row["actor_id"], row.get("model_binding_id")): row for row in full["exclusions"]}
    for row in scoped["exclusions"]:
        if (row["actor_id"], row.get("model_binding_id")) in full_by_pair:
            assert row["hard_blocker_codes"] == full_by_pair[row["actor_id"], row.get("model_binding_id")][
                "hard_blocker_codes"
            ]

    # The out-of-team lookalike stays unselectable for the team PM, and the
    # preview recomputation names the topology gate although its row is hidden.
    selection = ModelAwareAgentTaskAssignmentCreate(
        task_id=task.id,
        actor_id=lookalike.id,
        expected_task_version=task.version,
        purpose="verification",
        assessment_id=assessment.id,
        model_binding_id=lookalike_binding.id,
        model_binding_revision=lookalike_binding.revision,
        routing_preview_id=scoped["preview_id"],
        routing_preview_digest=scoped["preview_digest"],
        reviewer_profile_id=reviewer.profile_id,
    )
    with pytest.raises(AgentTeamSetupConflictError) as outside:
        await AgentWorkService(db).create_assignment(
            pm,
            selection,
            idempotency_key="team-scope-lookalike",
            rationale="Attempt an out-of-team reviewer",
            correlation_id="team-scope-lookalike",
        )
    assert outside.value.code == "agent_team_actor_outside_topology"
    await reload_session_fixture(db)
    with pytest.raises(AgentRoutingConflictError) as ineligible:
        await AgentRoutingService(db).validate_assignment_selection(
            task=await TaskService(db).get_by_id(task.id),
            selected_actor=await db.get(AgentActor, lookalike.id),
            data=selection,
        )
    assert ineligible.value.code == "routing_selection_ineligible"
    assert ineligible.value.context["hard_blocker_codes"] == ["actor_topology_incompatible"]
