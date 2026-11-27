"""End-to-end service coverage for authoritative Wave 3 routing."""

from __future__ import annotations

import asyncio
from datetime import UTC, date, datetime
import json
from types import SimpleNamespace

import pytest
from tests.support.transactions import reload_session_fixture
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent import (
    AgentActor,
    AgentModelBinding,
    AgentModelCatalogEntry,
    AgentRun,
    AgentTaskAssignment,
    TaskEvent,
    TaskRoutingAssessment,
)
from app.models.routing_qualification import RoutingQualificationKey
from app.models.team_member import TeamMember, TeamMemberProfile, TeamMemberProfileSkill
from app.schemas.agent import (
    AgentTaskAssignmentCreate,
    AgentReviewVerdict,
    ModelAwareAgentTaskAssignmentCreate,
    ModelAwareAgentTaskAssignmentUpdate,
    ModelAwareAgentWorkBegin,
)
from app.schemas.agent_planning import AgentPlanningCommandContext
from app.schemas.agent_routing import (
    AgentRoutingPreviewCreate,
    TaskRoutingAssessmentCommand,
)
from app.services.agent_routing_service import (
    AgentRoutingConflictError,
    AgentRoutingService,
)
from app.schemas.routing_qualification import (
    RoutingQualificationKeyDeclare,
    RoutingQualificationKeyRetire,
)
from app.services.agent_model_catalog_service import AgentModelConflictError
from app.services.agent_routing_policy import ROUTING_POLICY_VERSION, UnknownRoutingKeyError
from app.services.routing_qualification_key_service import RoutingQualificationKeyService
from app.services.agent_routing_rollout import (
    AgentRoutingRolloutService,
    AgentRoutingTopologyReadiness,
)
from app.services.agent_work_service import AgentWorkService


pytestmark = pytest.mark.usefixtures(
    "qualified_model_aware_routing_test_context"
)


_TASK_BRIEF = """## Goal
Implement the bounded change.

## Context and sources
Use the repository contracts.

## Scope
Change the requested component.

## Out of scope
Unrelated behavior.

## Acceptance criteria
The deterministic contract is satisfied.

## Verification
Run focused checks.

## Open questions
None
"""


def _assessment_command(
    *,
    task_version: int,
    minimum_effort: str | None = None,
    qualification_keys: list[str] | None = None,
) -> TaskRoutingAssessmentCommand:
    required_model = {
        "minimum_reasoning_tier": 1,
        "minimum_context_tier": "small",
        "modality_tags": ["text"],
        "tool_tags": [],
        "data_policy_tags": [],
    }
    if minimum_effort is not None:
        required_model["minimum_effort"] = minimum_effort
    if qualification_keys is not None:
        required_model["qualification_keys"] = qualification_keys
    return TaskRoutingAssessmentCommand(
        expected_task_version=task_version,
        band="routine",
        axes={
            "reasoning": 1,
            "ambiguity": 1,
            "context_breadth": 1,
            "risk": 1,
            "verification_burden": 1,
        },
        required_skill_levels={"backend-python": 3},
        required_model=required_model,
        review_mode="none",
        confidence=0.9,
        reason_codes=[],
        rationale="A bounded low-risk task with deterministic verification.",
    )


def _command_context(key: str) -> AgentPlanningCommandContext:
    return AgentPlanningCommandContext(
        idempotency_key=key,
        rationale="Record the current authoritative routing decision.",
        correlation_id=f"corr-{key}",
    )


def _rollout(mode: str) -> AgentRoutingRolloutService:
    return AgentRoutingRolloutService(
        settings_override=SimpleNamespace(model_aware_routing_mode=mode),
        topology_readiness=AgentRoutingTopologyReadiness.ready(
            topology_id="routing-test-topology",
            topology_revision=1,
        ),
    )


async def _routing_fixture(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
):
    profile = await profile_factory(
        assignment_modes=["execution"],
    )
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
    member = await team_member_factory(profile=profile)
    task = await task_factory(
        assignee=member,
        description=_TASK_BRIEF,
        effort_hours=8.0,
        estimate_provenance="estimated",
        tags=json.dumps(["agent", "cap:backend-python"]),
        start_date=date(2026, 7, 20),
        end_date=date(2026, 7, 24),
    )
    worker = await actor_factory(
        profile=profile,
        scopes=json.dumps(
            ["work:execute", "assignments:read", "tasks:read"]
        ),
    )
    pm = await actor_factory(
        role="pm",
        scopes=json.dumps(
            [
                "planning:read",
                "planning:write",
                "assignments:read",
                "assignments:write",
            ]
        ),
    )
    catalog = AgentModelCatalogEntry(
        key="routine-python",
        provider="test-provider",
        configured_model_alias="runtime-routine-python",
        reasoning_tier=1,
        context_tier="small",
        modality_tags=["text"],
        cost_tier="low",
        latency_tier="fast",
        enabled=True,
        revision=1,
    )
    db_session.add(catalog)
    await db_session.flush()
    binding = AgentModelBinding(
        actor_id=worker.id,
        model_catalog_id=catalog.id,
        is_default=True,
        enabled=True,
        tool_tags=[],
        data_policy_tags=[],
        revision=1,
    )
    db_session.add(binding)
    await db_session.commit()
    return pm, worker, task, binding, catalog


@pytest.mark.asyncio
async def test_assessment_lifecycle_is_replay_safe_and_version_bound(
    db_session: AsyncSession,
    actor_factory,
    task_factory,
) -> None:
    pm = await actor_factory(
        role="pm",
        scopes=json.dumps(["planning:read", "planning:write"]),
    )
    task = await task_factory()
    await db_session.commit()
    service = AgentRoutingService(db_session)
    command = _assessment_command(task_version=task.version)
    context = _command_context("assessment-1")

    created = await service.create_assessment(task.id, pm, command, context)
    replay = await service.create_assessment(task.id, pm, command, context)
    rollback_replay = await AgentRoutingService(
        db_session,
        rollout_service=_rollout("off"),
    ).create_assessment(task.id, pm, command, context)

    assert replay == created
    assert rollback_replay == created
    assert created.assessment.assessor == pm.name
    assert created.assessment.assessor_actor_id == pm.id
    assert (await service.get_assessment_state(task.id, pm)).state == "current"

    task.version += 1
    await db_session.commit()
    stale = await service.get_assessment_state(task.id, pm)
    assert stale.state == "stale"
    assert stale.assessment is not None
    assert stale.assessment.id == created.assessment.id

    db_session.add(
        AgentTaskAssignment(
            task_id=task.id,
            actor_id=pm.id,
            purpose="execution",
            queue_class="rework",
            state="queued",
            task_version=task.version,
            routing_snapshot=json.dumps(
                {
                    "schema_version": "routing-lineage-snapshot-v1",
                    "authority": "agent-work-service-v1",
                    "selection_pending": True,
                    "review_floor": {"review_mode": "independent"},
                }
            ),
        )
    )
    await db_session.commit()
    with pytest.raises(AgentRoutingConflictError) as review_floor:
        await service.create_assessment(
            task.id,
            pm,
            _assessment_command(task_version=task.version),
            _command_context("assessment-review-floor"),
        )
    assert review_floor.value.code == "routing_review_floor_not_met"


@pytest.mark.asyncio
async def test_untrusted_legacy_lineage_cannot_raise_assessment_review_floor(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    pm, worker, task, _, _ = await _routing_fixture(
        db_session,
        profile_factory,
        actor_factory,
        team_member_factory,
        task_factory,
    )
    db_session.add(
        AgentTaskAssignment(
            task_id=task.id,
            actor_id=worker.id,
            purpose="execution",
            queue_class="rework",
            state="queued",
            task_version=task.version,
            routing_snapshot=json.dumps(
                {
                    "schema_version": "caller-lineage-v1",
                    "selection_pending": True,
                    "review_floor": {"review_mode": "independent"},
                }
            ),
        )
    )
    await db_session.commit()

    receipt = await AgentRoutingService(db_session).create_assessment(
        task.id,
        pm,
        _assessment_command(task_version=task.version),
        _command_context("assessment-untrusted-review-floor"),
    )

    assert receipt.assessment.review_mode == "none"


@pytest.mark.asyncio
async def test_selection_input_fence_serializes_sqlite_routing_transactions(
    db_session: AsyncSession,
    db_session_factory,
    task_factory,
) -> None:
    task = await task_factory()
    await db_session.commit()
    await AgentRoutingService(db_session).lock_selection_inputs(task.id)

    async def acquire_competing_fence() -> None:
        async with db_session_factory() as competing_session:
            await AgentRoutingService(
                competing_session
            ).lock_selection_inputs(task.id)
            await competing_session.rollback()

    competing = asyncio.create_task(acquire_competing_fence())
    await asyncio.sleep(0.05)
    assert not competing.done()

    await db_session.rollback()
    await reload_session_fixture(db_session)
    await asyncio.wait_for(competing, timeout=2)


@pytest.mark.asyncio
async def test_assessment_history_trims_deterministic_tail_to_packet_limit(
    db_session: AsyncSession,
    actor_factory,
    task_factory,
) -> None:
    pm = await actor_factory(
        role="pm",
        scopes=json.dumps(["planning:read", "planning:write"]),
    )
    task = await task_factory()
    await db_session.commit()
    service = AgentRoutingService(db_session)
    for index in range(5):
        values = _assessment_command(
            task_version=task.version
        ).model_dump(mode="json")
        values["rationale"] = str(index) + ("x" * 7_999)
        await service.create_assessment(
            task.id,
            pm,
            TaskRoutingAssessmentCommand.model_validate(values),
            _command_context(f"assessment-history-{index}"),
        )
        if index < 4:
            task.version += 1
            await db_session.commit()

    history = await service.list_assessments(task.id, pm, limit=100)

    assert history.total_count == 5
    assert len(history.assessments) < history.total_count
    assert history.omitted_count == history.total_count - len(
        history.assessments
    )
    assert len(history.canonical_json_bytes()) <= 32_768
    assert history.assessments == sorted(
        history.assessments,
        key=lambda item: (item.created_at, item.id),
        reverse=True,
    )


@pytest.mark.asyncio
async def test_preview_is_deterministic_and_relevant_mutation_invalidates_it(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    pm, worker, task, binding, _ = await _routing_fixture(
        db_session,
        profile_factory,
        actor_factory,
        team_member_factory,
        task_factory,
    )
    service = AgentRoutingService(db_session)
    receipt = await service.create_assessment(
        task.id,
        pm,
        _assessment_command(task_version=task.version),
        _command_context("assessment-preview"),
    )
    request = AgentRoutingPreviewCreate(
        purpose="execution",
        assessment_id=receipt.assessment.id,
        expected_task_version=task.version,
    )
    now = datetime(2026, 7, 22, 12, 0, tzinfo=UTC)

    first = await service.preview_task_routing(task.id, pm, request, now=now)
    second = await service.preview_task_routing(task.id, pm, request, now=now)

    assert first == second
    assert first.recommended_candidate is not None
    assert first.recommended_candidate.actor_id == worker.id
    assert first.recommended_candidate.model_binding_id == binding.id

    original_binding_revision = binding.revision
    binding.revision += 1
    await db_session.commit()
    changed = await service.preview_task_routing(task.id, pm, request, now=now)
    assert changed.input_digest != first.input_digest
    assert changed.preview_id != first.preview_id
    with pytest.raises(AgentRoutingConflictError) as stale:
        await service.validate_assignment_selection(
            task=task,
            selected_actor=worker,
            data=ModelAwareAgentTaskAssignmentCreate(
                task_id=task.id,
                actor_id=worker.id,
                expected_task_version=task.version,
                purpose="execution",
                assessment_id=receipt.assessment.id,
                model_binding_id=binding.id,
                model_binding_revision=original_binding_revision,
                routing_preview_id=first.preview_id,
                routing_preview_digest=first.preview_digest,
            ),
            assignment_created_by_actor=pm,
            now=now,
        )
    assert stale.value.code == "routing_preview_stale"

    with pytest.raises(AgentRoutingConflictError) as expired:
        await service.validate_assignment_selection(
            task=task,
            selected_actor=worker,
            data=ModelAwareAgentTaskAssignmentCreate(
                task_id=task.id,
                actor_id=worker.id,
                expected_task_version=task.version,
                purpose="execution",
                assessment_id=receipt.assessment.id,
                model_binding_id=binding.id,
                model_binding_revision=original_binding_revision,
                routing_preview_id=first.preview_id,
                routing_preview_digest=first.preview_digest,
            ),
            assignment_created_by_actor=pm,
            now=datetime(2026, 7, 22, 12, 5, 1, tzinfo=UTC),
        )
    assert expired.value.code == "routing_preview_expired"

    worker.enabled = False
    await db_session.commit()
    no_candidate = await service.preview_task_routing(
        task.id,
        pm,
        request,
        now=now,
    )
    assert no_candidate.recommended_candidate is None
    assert no_candidate.eligible_candidates == []
    assert "no_eligible_candidate" in no_candidate.hard_blocker_codes


async def _extra_worker(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    *,
    key: str,
    cost_tier: str,
    local_first: bool,
    reasoning_tier: int = 1,
    effort: str = "unknown",
    alias: str | None = None,
    qualification_keys: list[str] | None = None,
    profile=None,
):
    if profile is None:
        profile = await profile_factory(assignment_modes=["execution"])
    worker = await actor_factory(
        profile=profile,
        scopes=json.dumps(["work:execute", "assignments:read", "tasks:read"]),
    )
    catalog = AgentModelCatalogEntry(
        key=key,
        provider="test-provider",
        configured_model_alias=alias or f"runtime-{key}",
        reasoning_tier=reasoning_tier,
        effort=effort,
        qualification_keys=qualification_keys or [],
        context_tier="small",
        modality_tags=["text"],
        cost_tier=cost_tier,
        local_first=local_first,
        latency_tier="fast",
        enabled=True,
        revision=1,
    )
    db_session.add(catalog)
    await db_session.flush()
    binding = AgentModelBinding(
        actor_id=worker.id,
        model_catalog_id=catalog.id,
        is_default=True,
        enabled=True,
        tool_tags=[],
        data_policy_tags=[],
        revision=1,
    )
    db_session.add(binding)
    await db_session.commit()
    return worker, binding


@pytest.mark.asyncio
async def test_local_first_preference_breaks_ties_but_never_overrides_a_gate(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    pm, hosted_worker, task, hosted_binding, _ = await _routing_fixture(
        db_session,
        profile_factory,
        actor_factory,
        team_member_factory,
        task_factory,
    )
    local_worker, local_binding = await _extra_worker(
        db_session,
        profile_factory,
        actor_factory,
        team_member_factory,
        key="local-python",
        cost_tier="high",
        local_first=True,
        profile=await db_session.get(TeamMemberProfile, hosted_worker.profile_id),
    )
    # A local-first entry on another profile fails the capacity gate.
    blocked_worker, _ = await _extra_worker(
        db_session,
        profile_factory,
        actor_factory,
        team_member_factory,
        key="blocked-local",
        cost_tier="low",
        local_first=True,
    )
    service = AgentRoutingService(db_session)
    receipt = await service.create_assessment(
        task.id,
        pm,
        _assessment_command(task_version=task.version),
        _command_context("assessment-local-first"),
    )
    request = AgentRoutingPreviewCreate(
        purpose="execution",
        assessment_id=receipt.assessment.id,
        expected_task_version=task.version,
    )
    now = datetime(2026, 7, 22, 12, 0, tzinfo=UTC)

    preview = await service.preview_task_routing(task.id, pm, request, now=now)

    by_actor = {c.actor_id: c for c in preview.eligible_candidates}
    assert hosted_worker.id in by_actor and local_worker.id in by_actor
    assert by_actor[hosted_worker.id].adequacy_class == by_actor[local_worker.id].adequacy_class
    assert preview.recommended_candidate is not None
    assert preview.recommended_candidate.model_binding_id == local_binding.id
    assert by_actor[local_worker.id].rank < by_actor[hosted_worker.id].rank
    assert by_actor[local_worker.id].local_first is True
    assert "local-first model is preferred" in by_actor[local_worker.id].rationale
    assert "local-first model is preferred" not in by_actor[hosted_worker.id].rationale
    # The hard blocker still excludes the local-first entry.
    assert blocked_worker.id not in by_actor
    assert any(e.actor_id == blocked_worker.id and e.hard_blocker_codes for e in preview.exclusions)


@pytest.mark.asyncio
async def test_required_effort_gates_and_orders_entries_of_one_runtime_model(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    pm, unrecorded_worker, task, _, _ = await _routing_fixture(
        db_session, profile_factory, actor_factory, team_member_factory, task_factory
    )
    shared_profile = await db_session.get(TeamMemberProfile, unrecorded_worker.profile_id)
    workers = {}
    for effort in ("low", "medium", "xhigh"):
        worker, binding = await _extra_worker(
            db_session,
            profile_factory,
            actor_factory,
            team_member_factory,
            key=f"shared-model-{effort}",
            alias="runtime-shared-model",
            cost_tier="medium",
            local_first=False,
            effort=effort,
            profile=shared_profile,
        )
        workers[effort] = (worker, binding)
    service = AgentRoutingService(db_session)
    now = datetime(2026, 7, 22, 12, 0, tzinfo=UTC)

    member = await db_session.get(TeamMember, task.assignee_id)

    async def preview(minimum_effort: str | None, key: str):
        # An assessment is immutable per task version, so each case gets a task.
        task = await task_factory(
            assignee=member,
            description=_TASK_BRIEF,
            effort_hours=8.0,
            estimate_provenance="estimated",
            tags=json.dumps(["agent", "cap:backend-python"]),
            start_date=date(2026, 7, 20),
            end_date=date(2026, 7, 24),
        )
        receipt = await service.create_assessment(
            task.id,
            pm,
            _assessment_command(task_version=task.version, minimum_effort=minimum_effort),
            _command_context(key),
        )
        return await service.preview_task_routing(
            task.id,
            pm,
            AgentRoutingPreviewCreate(
                purpose="execution",
                assessment_id=receipt.assessment.id,
                expected_task_version=task.version,
            ),
            now=now,
        )

    # No stated requirement: every entry stays eligible, the preview shows the
    # recorded effort, and the unrecorded entry is still routable.
    open_preview = await preview(None, "assessment-effort-none")
    by_actor = {c.actor_id: c for c in open_preview.eligible_candidates}
    assert {by_actor[w.id].effort for w, _ in workers.values()} == {"low", "medium", "xhigh"}
    assert by_actor[unrecorded_worker.id].effort == "unknown"
    assert len({c.adequacy_class for c in by_actor.values()}) == 1

    # A stated requirement excludes lower and unrecorded efforts with a named blocker.
    required = await preview("medium", "assessment-effort-medium")
    eligible = {c.actor_id: c for c in required.eligible_candidates}
    assert set(eligible) == {workers["medium"][0].id, workers["xhigh"][0].id}
    excluded = {e.actor_id: e for e in required.exclusions}
    for blocked in (workers["low"][0], unrecorded_worker):
        assert "model_effort_insufficient" in excluded[blocked.id].hard_blocker_codes
    assert excluded[workers["low"][0].id].effort == "low"
    # The lowest setting that satisfies the requirement ranks first.
    assert required.recommended_candidate.actor_id == workers["medium"][0].id
    assert eligible[workers["xhigh"][0].id].adequacy_class == eligible[workers["medium"][0].id].adequacy_class + 2
    assert "requires effort medium or higher" in eligible[workers["medium"][0].id].rationale


@pytest.mark.asyncio
async def test_declared_qualification_key_is_a_requirement_the_candidate_must_hold(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    pm, unqualified_worker, task, _, _ = await _routing_fixture(
        db_session, profile_factory, actor_factory, team_member_factory, task_factory
    )
    operator = await actor_factory(role="pm", scopes=json.dumps(["admin"]))
    registry = RoutingQualificationKeyService(db_session)
    await registry.declare(
        operator,
        RoutingQualificationKeyDeclare(key="qualified.schema-review", label="Schema review"),
        command=_command_context("declare-schema-review"),
    )
    shared_profile = await db_session.get(TeamMemberProfile, unqualified_worker.profile_id)
    qualified_worker, _ = await _extra_worker(
        db_session,
        profile_factory,
        actor_factory,
        team_member_factory,
        key="schema-reviewer-high",
        cost_tier="high",
        local_first=False,
        effort="high",
        qualification_keys=["qualified.schema-review"],
        profile=shared_profile,
    )
    service = AgentRoutingService(db_session)
    # A refused command rolls the session back, so keep plain identities.
    task_id, task_version = task.id, task.version
    unqualified_id, qualified_id = unqualified_worker.id, qualified_worker.id

    # An undeclared key is refused with the error routing always gave.
    with pytest.raises(UnknownRoutingKeyError, match="Unknown routing skill key: qualified.undeclared"):
        await service.create_assessment(
            task_id,
            pm,
            _assessment_command(task_version=task_version, qualification_keys=["qualified.undeclared"]),
            _command_context("assessment-undeclared-key"),
        )
    await db_session.refresh(pm)

    receipt = await service.create_assessment(
        task_id,
        pm,
        _assessment_command(task_version=task_version, qualification_keys=["qualified.schema-review"]),
        _command_context("assessment-declared-key"),
    )
    assert receipt.assessment.required_model.qualification_keys == ["qualified.schema-review"]
    preview = await service.preview_task_routing(
        task_id,
        pm,
        AgentRoutingPreviewCreate(
            purpose="execution",
            assessment_id=receipt.assessment.id,
            expected_task_version=task_version,
        ),
        now=datetime(2026, 7, 22, 12, 0, tzinfo=UTC),
    )
    # Only the entry holding the key is eligible, although it costs more.
    assert [c.actor_id for c in preview.eligible_candidates] == [qualified_id]
    candidate = preview.recommended_candidate
    assert candidate.qualification_keys == ["qualified.schema-review"]
    assert "requires qualification keys qualified.schema-review" in candidate.rationale
    excluded = {e.actor_id: e for e in preview.exclusions}[unqualified_id]
    assert "model_qualification_missing" in excluded.hard_blocker_codes
    assert excluded.missing_qualification_keys == ["qualified.schema-review"]
    assert excluded.model_dump(mode="json")["missing_qualification_keys"] == ["qualified.schema-review"]

    # Retiring the key while an entry holds it and a task requires it is refused, naming both.
    detail = await registry.get_key(operator, "qualified.schema-review")
    assert [entry.key for entry in detail.usage.catalog_entries] == ["schema-reviewer-high"]
    assert detail.usage.task_ids == [task_id]
    with pytest.raises(AgentModelConflictError) as refused:
        await registry.retire(
            "qualified.schema-review",
            operator,
            RoutingQualificationKeyRetire(expected_revision=1),
            command=_command_context("retire-in-use"),
        )
    assert refused.value.code == "routing_qualification_key_in_use"
    assert refused.value.context["task_ids"] == [task_id]
    assert refused.value.context["catalog_entries"][0]["key"] == "schema-reviewer-high"
    assert "Required qualification keys" not in excluded.rationale

    # A key retired outside the guarded command is named as retired in the exclusion.
    assessment_id = receipt.assessment.id
    await db_session.execute(
        update(RoutingQualificationKey).values(state="retired")
    )
    await db_session.commit()
    await db_session.refresh(pm)
    retired_preview = await service.preview_task_routing(
        task_id,
        pm,
        AgentRoutingPreviewCreate(
            purpose="execution",
            assessment_id=assessment_id,
            expected_task_version=task_version,
        ),
        now=datetime(2026, 7, 22, 12, 0, tzinfo=UTC),
    )
    retired_exclusion = {e.actor_id: e for e in retired_preview.exclusions}[unqualified_id]
    assert "Required qualification keys qualified.schema-review are retired" in retired_exclusion.rationale


@pytest.mark.asyncio
async def test_assessments_without_qualification_keys_keep_their_stored_shape(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    pm, _, task, _, _ = await _routing_fixture(
        db_session, profile_factory, actor_factory, team_member_factory, task_factory
    )
    receipt = await AgentRoutingService(db_session).create_assessment(
        task.id,
        pm,
        _assessment_command(task_version=task.version),
        _command_context("assessment-no-qualification"),
    )
    stored = await db_session.get(TaskRoutingAssessment, receipt.assessment.id)
    assert "qualification_keys" not in stored.required_model


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("snapshot_authority", "run_receipt", "expected_blocker"),
    (
        (
            "agent-routing-service-v1",
            None,
            "verification_profile_not_independent",
        ),
        # A compatibility assignment without a run has no recorded profile.
        (None, None, "verification_independence_unverifiable"),
        # Its run's authenticated begin names the historical profile, even
        # though the implementation actor now holds another profile.
        (None, "historical", "verification_profile_not_independent"),
        (None, "current", None),
        # A profile change before the terminal command counts both profiles.
        (None, "changed_to_historical", "verification_profile_not_independent"),
        # A receipt that names another actor is not the run's own evidence.
        (None, "foreign_actor", "verification_independence_unverifiable"),
        # A begin receipt without the profile's revision is not evidence.
        (None, "missing_revision", "verification_independence_unverifiable"),
        # A run the server ended may have changed profile before it stopped;
        # without its recorded terminal profile, that profile is unknown.
        (None, "server_ended_unrecorded", "verification_independence_unverifiable"),
        (None, "server_ended_recorded", None),
    ),
)
async def test_verification_independence_requires_authoritative_profile_history(
    snapshot_authority: str | None,
    run_receipt: str | None,
    expected_blocker: str | None,
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    historical_profile = await profile_factory(
        assignment_modes=["execution", "verification"],
    )
    current_implementation_profile = await profile_factory(
        assignment_modes=["execution"],
    )
    db_session.add(
        TeamMemberProfileSkill(
            profile_id=historical_profile.id,
            skill_key="backend-python",
            skill_name="Python Backend",
            category="engineering",
            level=4,
            interest=4,
            is_weakness=False,
        )
    )
    implementation_member = await team_member_factory(
        profile=current_implementation_profile,
    )
    task = await task_factory(
        assignee=implementation_member,
        description=_TASK_BRIEF,
        effort_hours=8.0,
        estimate_provenance="estimated",
        tags=json.dumps(["agent", "cap:backend-python"]),
        status="resolved",
        start_date=date(2026, 7, 20),
        end_date=date(2026, 7, 24),
    )
    await team_member_factory(
        profile=historical_profile,
        iteration=task.iteration,
    )
    implementation_actor = await actor_factory(
        profile=current_implementation_profile,
    )
    verifier = await actor_factory(
        profile=historical_profile,
        role="verifier",
        scopes=json.dumps(["verification:write", "assignments:read"]),
    )
    pm = await actor_factory(
        role="pm",
        scopes=json.dumps(
            ["planning:read", "planning:write", "assignments:write"]
        ),
    )
    catalog = AgentModelCatalogEntry(
        key="verification-python",
        provider="test-provider",
        configured_model_alias="runtime-verification-python",
        reasoning_tier=1,
        context_tier="small",
        modality_tags=["text"],
        cost_tier="low",
        latency_tier="fast",
        enabled=True,
        revision=1,
    )
    db_session.add(catalog)
    await db_session.flush()
    binding = AgentModelBinding(
        actor_id=verifier.id,
        model_catalog_id=catalog.id,
        is_default=True,
        enabled=True,
        tool_tags=[],
        data_policy_tags=[],
        revision=1,
    )
    db_session.add_all(
        [
            binding,
            AgentTaskAssignment(
                task_id=task.id,
                actor_id=implementation_actor.id,
                purpose="execution",
                queue_class="normal",
                state="fulfilled",
                task_version=task.version,
                routing_snapshot=json.dumps(
                    {
                        "schema_version": "routing-decision-snapshot-v1",
                        "profile_id": historical_profile.id,
                        **(
                            {"authority": snapshot_authority}
                            if snapshot_authority is not None
                            else {}
                        ),
                    }
                ),
            ),
        ]
    )
    await db_session.commit()
    if run_receipt is not None:
        execution = await db_session.scalar(
            select(AgentTaskAssignment).where(
                AgentTaskAssignment.task_id == task.id,
                AgentTaskAssignment.purpose == "execution",
            )
        )
        begun, terminal = {
            "historical": (historical_profile.id, historical_profile.id),
            "current": (
                current_implementation_profile.id,
                current_implementation_profile.id,
            ),
            "changed_to_historical": (
                current_implementation_profile.id,
                historical_profile.id,
            ),
            "foreign_actor": (historical_profile.id, historical_profile.id),
            "missing_revision": (historical_profile.id, historical_profile.id),
            "server_ended_unrecorded": (
                current_implementation_profile.id,
                current_implementation_profile.id,
            ),
            "server_ended_recorded": (
                current_implementation_profile.id,
                current_implementation_profile.id,
            ),
        }[run_receipt]
        receipt = {
            "actor_id": (
                verifier.id
                if run_receipt == "foreign_actor"
                else implementation_actor.id
            ),
            "profile_id": begun,
            "profile_revision": (
                None if run_receipt == "missing_revision" else f"p{begun}-recorded"
            ),
            "source": "authenticated_work_begin",
            "terminal_profile_id": terminal,
        }
        if run_receipt == "server_ended_unrecorded":
            del receipt["terminal_profile_id"]
        db_session.add(
            AgentRun(
                task_id=task.id,
                actor_id=implementation_actor.id,
                assignment_id=execution.id,
                status=(
                    "canceled"
                    if run_receipt.startswith("server_ended")
                    else "succeeded"
                ),
                execution_provenance=receipt,
            )
        )
        await db_session.commit()
    routing = AgentRoutingService(db_session)
    command_values = _assessment_command(
        task_version=task.version
    ).model_dump(mode="json")
    command_values["review_mode"] = "independent"
    receipt = await routing.create_assessment(
        task.id,
        pm,
        TaskRoutingAssessmentCommand.model_validate(command_values),
        _command_context("assessment-verification-independence"),
    )

    preview = await routing.preview_task_routing(
        task.id,
        pm,
        AgentRoutingPreviewCreate(
            purpose="verification",
            assessment_id=receipt.assessment.id,
            expected_task_version=task.version,
            reviewer_profile_id=historical_profile.id,
        ),
    )

    verifier_row = next(
        item
        for item in [*preview.eligible_candidates, *preview.exclusions]
        if item.actor_id == verifier.id
        and item.model_binding_id == binding.id
    )
    independence_codes = {
        "verification_actor_not_independent",
        "verification_profile_not_independent",
        "verification_independence_unverifiable",
    }
    if expected_blocker is None:
        assert not independence_codes & set(verifier_row.hard_blocker_codes)
    else:
        assert preview.recommended_candidate is None
        assert expected_blocker in verifier_row.hard_blocker_codes


@pytest.mark.asyncio
async def test_model_aware_assignment_and_begin_enforce_observed_model(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    pm, worker, task, binding, catalog = await _routing_fixture(
        db_session,
        profile_factory,
        actor_factory,
        team_member_factory,
        task_factory,
    )
    routing = AgentRoutingService(db_session)
    with pytest.raises(AgentRoutingConflictError) as legacy_bypass:
        await AgentWorkService(db_session).create_assignment(
            pm,
            AgentTaskAssignmentCreate(
                task_id=task.id,
                actor_id=worker.id,
                expected_task_version=task.version,
            ),
            idempotency_key="assignment-legacy-bypass",
            rationale="Attempt an unbound assignment without opting in.",
            correlation_id="corr-assignment-legacy-bypass",
        )
    assert legacy_bypass.value.code == "model_aware_assignment_required"
    await reload_session_fixture(db_session)

    receipt = await routing.create_assessment(
        task.id,
        pm,
        _assessment_command(task_version=task.version),
        _command_context("assessment-assignment"),
    )
    preview = await routing.preview_task_routing(
        task.id,
        pm,
        AgentRoutingPreviewCreate(
            purpose="execution",
            assessment_id=receipt.assessment.id,
            expected_task_version=task.version,
        ),
    )
    assignment_command = ModelAwareAgentTaskAssignmentCreate(
        task_id=task.id,
        actor_id=worker.id,
        expected_task_version=task.version,
        purpose="execution",
        assessment_id=receipt.assessment.id,
        model_binding_id=binding.id,
        model_binding_revision=binding.revision,
        routing_preview_id=preview.preview_id,
        routing_preview_digest=preview.preview_digest,
    )
    assignment = await AgentWorkService(db_session).create_assignment(
        pm,
        assignment_command,
        idempotency_key="assignment-model-aware",
        rationale="Dispatch the preview-selected worker and binding.",
        correlation_id="corr-assignment-model-aware",
    )
    assert assignment.model_binding_status == "current"
    assert assignment.routing_snapshot["schema_version"] == (
        "routing-decision-snapshot-v1"
    )
    assert assignment.routing_snapshot["eligible_candidate_summaries"][0][
        "model_binding_id"
    ] == binding.id
    assert "exclusion_summaries" in assignment.routing_snapshot

    work = AgentWorkService(db_session)
    with pytest.raises(AgentRoutingConflictError) as mismatch:
        await work.begin(
            worker,
            ModelAwareAgentWorkBegin(
                assignment_id=assignment.id,
                queue_revision=worker.queue_revision,
                model_binding_id=binding.id,
                model_binding_revision=binding.revision,
                resolved_model_id="wrong-model",
            ),
            idempotency_key="begin-wrong-model",
        )
    assert mismatch.value.code == "resolved_model_mismatch"
    await reload_session_fixture(db_session)

    begun = await work.begin(
        worker,
        ModelAwareAgentWorkBegin(
            assignment_id=assignment.id,
            queue_revision=worker.queue_revision,
            model_binding_id=binding.id,
            model_binding_revision=binding.revision,
            resolved_model_id=catalog.key,
        ),
        idempotency_key="begin-matched-model",
    )
    assert begun.run.configured_model_alias == catalog.configured_model_alias
    assert begun.run.resolved_model_id == catalog.key
    assert begun.run.model_trust_state == "matched"
    assert begun.run.model_match_basis == "catalog_key"
    assert begun.assignment.model_binding_status == "current"

    rollback_replay = await AgentWorkService(
        db_session,
        rollout_service=_rollout("off"),
    ).create_assignment(
        pm,
        assignment_command,
        idempotency_key="assignment-model-aware",
        rationale="Dispatch the preview-selected worker and binding.",
        correlation_id="corr-assignment-model-aware",
    )
    assert rollback_replay == assignment


@pytest.mark.asyncio
async def test_completed_rework_update_persists_prior_and_new_routing_lineage(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    pm, worker, task, binding, catalog = await _routing_fixture(
        db_session,
        profile_factory,
        actor_factory,
        team_member_factory,
        task_factory,
    )
    routing = AgentRoutingService(db_session)
    receipt = await routing.create_assessment(
        task.id,
        pm,
        _assessment_command(task_version=task.version),
        _command_context("assessment-rework"),
    )
    task.status = "active"
    prior_snapshot = {
        "schema_version": "routing-decision-snapshot-v1",
        "authority": "agent-routing-service-v1",
        "policy_version": "model-aware-routing-v1",
        "task_id": task.id,
        "task_version": task.version,
        "assessment_id": receipt.assessment.id,
        "assessment_task_version": task.version,
        "assessment_band": "routine",
        "purpose": "execution",
        "actor_id": worker.id,
        "profile_id": worker.profile_id,
        "model_binding_id": binding.id,
        "model_binding_revision": binding.revision,
        "model_catalog_id": catalog.id,
        "model_catalog_key": catalog.key,
        "model_catalog_revision": catalog.revision,
        "configured_model_alias": catalog.configured_model_alias,
        "selected_reasoning_tier": catalog.reasoning_tier,
        "selected_context_tier": catalog.context_tier,
        "review_mode": "none",
        "routing_preview_id": "prior-preview",
        "routing_preview_digest": "d" * 64,
        "input_digest": "e" * 64,
        "selected_rank": 1,
        "adequacy_class": 0,
        "selection_reason_codes": ["eligible"],
        "confidence": 0.9,
    }
    source = AgentTaskAssignment(
        task_id=task.id,
        actor_id=worker.id,
        purpose="execution",
        queue_class="normal",
        state="fulfilled",
        task_version=task.version,
        model_binding_id=binding.id,
        model_binding_revision=binding.revision,
        routing_snapshot=json.dumps(prior_snapshot),
    )
    db_session.add(source)
    await db_session.flush()
    pending_snapshot = AgentWorkService._routing_lineage_snapshot(
        task=task,
        source_assignments=[source],
        transition="rework",
        provisional_actor_id=worker.id,
        reason="The original execution lacked a required tool capability.",
        evidence={"failure_category": "tool_insufficiency"},
    )
    pending = AgentTaskAssignment(
        task_id=task.id,
        actor_id=worker.id,
        purpose="execution",
        queue_class="rework",
        state="queued",
        task_version=task.version,
        routing_snapshot=json.dumps(pending_snapshot),
    )
    db_session.add(pending)
    await db_session.commit()
    preview = await routing.preview_task_routing(
        task.id,
        pm,
        AgentRoutingPreviewCreate(
            purpose="execution",
            assessment_id=receipt.assessment.id,
            expected_task_version=task.version,
        ),
    )
    assert preview.recommended_candidate is not None

    updated = await AgentWorkService(db_session).update_assignment(
        pending.id,
        pm,
        ModelAwareAgentTaskAssignmentUpdate(
            expected_queue_revision=worker.queue_revision,
            assessment_id=receipt.assessment.id,
            model_binding_id=binding.id,
            model_binding_revision=binding.revision,
            routing_preview_id=preview.preview_id,
            routing_preview_digest=preview.preview_digest,
            actor_id=worker.id,
        ),
        idempotency_key="reroute-model-aware",
        rationale="Complete the governed rework selection.",
        correlation_id="corr-reroute-model-aware",
    )

    assert updated.routing_snapshot["selection_pending"] is False
    prior_lineage = updated.routing_snapshot["prior_lineage"]
    assert prior_lineage["cause"]["category"] == "tool_insufficiency"
    assert prior_lineage["prior_decisions"][0]["model_binding_id"] == binding.id
    assert prior_lineage["selection_result"] == {
        "completed_by_snapshot": True,
        "assignment_id": pending.id,
    }


@pytest.mark.asyncio
async def test_rejection_telemetry_normalizes_adversarial_legacy_lineage(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    task_factory,
) -> None:
    verifier_profile = await profile_factory(
        assignment_modes=["verification"]
    )
    verifier = await actor_factory(
        profile=verifier_profile,
        role="verifier",
        scopes=json.dumps(["verification:write"]),
    )
    rework_worker = await actor_factory()
    task = await task_factory(status="resolved")
    review_assignment = AgentTaskAssignment(
        task_id=task.id,
        actor_id=verifier.id,
        purpose="verification",
        queue_class="normal",
        state="queued",
        queue_rank=1000,
        task_version=task.version,
        routing_snapshot=json.dumps(
            {
                "policy_version": "legacy-policy-v999",
                "review_mode": "caller-authored-review-mode",
            }
        ),
    )
    db_session.add(review_assignment)
    await db_session.commit()

    response = await AgentWorkService(db_session).review(
        verifier,
        AgentReviewVerdict(
            assignment_id=review_assignment.id,
            verdict="reject",
            expected_task_version=task.version,
            evidence={"failure_category": "external_service"},
            reason="The external dependency did not return usable evidence.",
            rework_actor_id=rework_worker.id,
        ),
        idempotency_key="legacy-review-rejection",
        rationale="Record rejection and create governed rework ownership.",
        correlation_id="corr-legacy-review-rejection",
    )

    assert response.review_assignment.state == "fulfilled"
    assert response.rework_assignment is not None
    assert response.rework_assignment.state == "queued"
    assert response.task.status == "active"
    events = (
        await db_session.execute(
            select(TaskEvent)
            .where(
                TaskEvent.task_id == task.id,
                TaskEvent.event_type.in_(
                    (
                        "agent.routing.verifier_rejected",
                        "agent.routing.rework_created",
                    )
                ),
            )
            .order_by(TaskEvent.id)
        )
    ).scalars().all()
    assert [event.event_type for event in events] == [
        "agent.routing.verifier_rejected",
        "agent.routing.rework_created",
    ]
    payloads = [json.loads(event.payload) for event in events]
    assert all(
        payload["policy_version"] == ROUTING_POLICY_VERSION
        for payload in payloads
    )
    assert payloads[0]["review_mode"] == "none"
    assert payloads[0]["failure_category"] == (
        "non_model_or_unclassified"
    )
    assert payloads[1]["failure_category"] == (
        "non_model_or_unclassified"
    )
