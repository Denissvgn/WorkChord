"""End-to-end service coverage for authoritative Wave 3 routing."""

from __future__ import annotations

import asyncio
from datetime import UTC, date, datetime
import json

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.agent import (
    AgentActor,
    AgentModelBinding,
    AgentModelCatalogEntry,
    AgentTaskAssignment,
)
from app.models.team_member import TeamMemberProfileSkill
from app.schemas.agent import (
    AgentTaskAssignmentCreate,
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
from app.services.agent_work_service import AgentWorkService


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


def _assessment_command(*, task_version: int) -> TaskRoutingAssessmentCommand:
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
        required_model={
            "minimum_reasoning_tier": 1,
            "minimum_context_tier": "small",
            "modality_tags": ["text"],
            "tool_tags": [],
            "data_policy_tags": [],
        },
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

    assert replay == created
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


@pytest.mark.asyncio
async def test_verification_independence_uses_historical_execution_profile(
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
                    }
                ),
            ),
        ]
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

    assert preview.recommended_candidate is None
    verifier_exclusion = next(
        item
        for item in preview.exclusions
        if item.actor_id == verifier.id
        and item.model_binding_id == binding.id
    )
    assert (
        "verification_profile_not_independent"
        in verifier_exclusion.hard_blocker_codes
    )


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
    assignment = await AgentWorkService(db_session).create_assignment(
        pm,
        ModelAwareAgentTaskAssignmentCreate(
            task_id=task.id,
            actor_id=worker.id,
            expected_task_version=task.version,
            purpose="execution",
            assessment_id=receipt.assessment.id,
            model_binding_id=binding.id,
            model_binding_revision=binding.revision,
            routing_preview_id=preview.preview_id,
            routing_preview_digest=preview.preview_digest,
        ),
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
