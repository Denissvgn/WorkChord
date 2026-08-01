"""Cross-surface qualification scenarios for model-aware agent routing."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime
import hashlib
import json
from typing import Any

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import mcp_agent_tools
from app.models.agent import (
    AgentActor,
    AgentModelBinding,
    AgentModelCatalogEntry,
    AgentRun,
    AgentTaskAssignment,
    TaskEvent,
)
from app.models.task import Task
from app.models.team_member import TeamMember, TeamMemberProfile, TeamMemberProfileSkill
from app.routers import agent as agent_router
from app.routers import agent_planning
from app.schemas.agent import (
    AgentTaskAssignmentUpdate,
    ModelAwareAgentTaskAssignmentCreate,
    ModelAwareAgentTaskAssignmentUpdate,
    ModelAwareAgentWorkBegin,
)
from app.schemas.agent_planning import AgentPlanningCommandContext
from app.schemas.agent_routing import (
    AgentRoutingPreviewCreate,
    AgentRoutingPreviewResponse,
    TaskRoutingAssessmentCommand,
    TaskRoutingAssessmentResponse,
)
from app.services.agent_routing_policy import (
    derive_difficulty_band,
    minimum_review_mode,
)
from app.services.agent_routing_service import (
    AgentRoutingConflictError,
    AgentRoutingService,
)
from app.services.agent_work_service import AgentWorkService
from app.services.assignee_recommendation_service import (
    AssigneeRecommendationService,
)


pytestmark = pytest.mark.usefixtures(
    "qualified_model_aware_routing_test_context"
)


_FIXED_NOW = datetime(2026, 7, 22, 12, tzinfo=UTC)
_TASK_BRIEF = """## Goal
Implement the bounded work.

## Context and sources
Use the repository contracts and current task evidence.

## Scope
Change only the requested component.

## Out of scope
Unrelated behavior.

## Acceptance criteria
The deterministic routing contract is satisfied.

## Verification
Run the focused checks.

## Open questions
None
"""


@dataclass(frozen=True)
class ScenarioBase:
    pm: AgentActor
    task: Task
    profile: TeamMemberProfile
    member: TeamMember


@dataclass(frozen=True)
class Candidate:
    actor: AgentActor
    binding: AgentModelBinding
    catalog: AgentModelCatalogEntry


@dataclass(frozen=True)
class PersistedState:
    task: Task
    assignments: list[AgentTaskAssignment]
    runs: list[AgentRun]
    events: list[TaskEvent]


@pytest.fixture(autouse=True)
def fixed_wave6_clock(monkeypatch: pytest.MonkeyPatch) -> None:
    """Keep preview IDs, expiry checks, and work fences byte-deterministic."""

    monkeypatch.setattr(
        "app.services.agent_routing_service.utc_now",
        lambda: _FIXED_NOW,
    )
    monkeypatch.setattr(
        "app.services.agent_work_service.utc_now",
        lambda: _FIXED_NOW,
    )


async def _seed_base(
    db: AsyncSession,
    *,
    profile_factory: Any,
    actor_factory: Any,
    team_member_factory: Any,
    task_factory: Any,
    skill_key: str = "backend-python",
    skill_level: int = 4,
    status: str = "planned",
    title: str = "Bounded Python change",
) -> ScenarioBase:
    profile = await profile_factory(assignment_modes=["execution"])
    db.add(
        TeamMemberProfileSkill(
            profile_id=profile.id,
            skill_key=skill_key,
            skill_name=skill_key.replace("-", " ").title(),
            category="qualification",
            level=skill_level,
            interest=4,
            is_weakness=False,
        )
    )
    member = await team_member_factory(profile=profile)
    task = await task_factory(
        assignee=member,
        title=title,
        description=_TASK_BRIEF,
        tags=json.dumps(["agent", f"cap:{skill_key}"]),
        priority=2,
        effort_days=1,
        status=status,
        start_date=date(2026, 7, 20),
        end_date=date(2026, 7, 24),
    )
    pm = await actor_factory(
        role="pm",
        scopes=json.dumps(
            [
                "planning:read",
                "planning:write",
                "assignments:read",
                "assignments:write",
                "tasks:read",
            ]
        ),
    )
    await db.commit()
    return ScenarioBase(pm=pm, task=task, profile=profile, member=member)


async def _add_binding(
    db: AsyncSession,
    *,
    actor: AgentActor,
    key: str,
    reasoning_tier: int,
    context_tier: str,
    cost_tier: str,
    latency_tier: str = "balanced",
    tool_tags: tuple[str, ...] = (),
    data_policy_tags: tuple[str, ...] = (),
    is_default: bool = False,
) -> Candidate:
    catalog = AgentModelCatalogEntry(
        key=key,
        provider="qualification-provider",
        configured_model_alias=f"runtime-{key}",
        reasoning_tier=reasoning_tier,
        context_tier=context_tier,
        modality_tags=["text"],
        cost_tier=cost_tier,
        latency_tier=latency_tier,
        enabled=True,
        revision=1,
    )
    db.add(catalog)
    await db.flush()
    binding = AgentModelBinding(
        actor_id=actor.id,
        model_catalog_id=catalog.id,
        is_default=is_default,
        enabled=True,
        tool_tags=list(tool_tags),
        data_policy_tags=list(data_policy_tags),
        revision=1,
    )
    db.add(binding)
    await db.commit()
    return Candidate(actor=actor, binding=binding, catalog=catalog)


async def _add_candidate(
    db: AsyncSession,
    *,
    actor_factory: Any,
    profile: TeamMemberProfile,
    key: str,
    reasoning_tier: int,
    context_tier: str,
    cost_tier: str,
    latency_tier: str = "balanced",
    tool_tags: tuple[str, ...] = (),
    data_policy_tags: tuple[str, ...] = (),
    role: str = "worker",
) -> Candidate:
    scopes = (
        ["verification:write", "assignments:read", "tasks:read"]
        if role == "verifier"
        else ["work:execute", "assignments:read", "tasks:read"]
    )
    actor = await actor_factory(
        profile=profile,
        role=role,
        scopes=json.dumps(scopes),
    )
    return await _add_binding(
        db,
        actor=actor,
        key=key,
        reasoning_tier=reasoning_tier,
        context_tier=context_tier,
        cost_tier=cost_tier,
        latency_tier=latency_tier,
        tool_tags=tool_tags,
        data_policy_tags=data_policy_tags,
        is_default=True,
    )


def _assessment_command(
    *,
    task_version: int,
    required_skill_levels: dict[str, int],
    minimum_reasoning_tier: int = 1,
    minimum_context_tier: str = "small",
    tool_tags: tuple[str, ...] = (),
    data_policy_tags: tuple[str, ...] = (),
    axes: dict[str, int] | None = None,
    reason_codes: tuple[str, ...] = (),
    review_mode: str | None = None,
) -> TaskRoutingAssessmentCommand:
    governed_axes = axes or {
        "reasoning": 1,
        "ambiguity": 1,
        "context_breadth": 1,
        "risk": 1,
        "verification_burden": 1,
    }
    return TaskRoutingAssessmentCommand(
        expected_task_version=task_version,
        band=derive_difficulty_band(governed_axes, reason_codes),
        axes=governed_axes,
        required_skill_levels=required_skill_levels,
        required_model={
            "minimum_reasoning_tier": minimum_reasoning_tier,
            "minimum_context_tier": minimum_context_tier,
            "modality_tags": ["text"],
            "tool_tags": list(tool_tags),
            "data_policy_tags": list(data_policy_tags),
        },
        review_mode=review_mode
        or minimum_review_mode(governed_axes, reason_codes),
        confidence=0.9,
        reason_codes=list(reason_codes),
        rationale="The scenario has explicit bounded routing requirements.",
    )


async def _create_assessment_with_parity(
    db: AsyncSession,
    *,
    base: ScenarioBase,
    data: TaskRoutingAssessmentCommand,
    key: str,
) -> TaskRoutingAssessmentResponse:
    rationale = "Record the scenario routing requirements."
    correlation_id = f"corr-{key}"
    command = AgentPlanningCommandContext(
        idempotency_key=key,
        rationale=rationale,
        correlation_id=correlation_id,
    )
    rest = await agent_planning.create_task_routing_assessment(
        base.task.id,
        data,
        base.pm,
        AgentRoutingService(db),
        command,
    )
    mcp = await mcp_agent_tools.create_task_routing_assessment(
        db,
        base.pm,
        base.task.id,
        data.model_dump(mode="json"),
        idempotency_key=key,
        rationale=rationale,
        correlation_id=correlation_id,
    )
    assert rest.model_dump(mode="json") == mcp
    return rest.assessment


async def _preview_with_parity(
    db: AsyncSession,
    *,
    base: ScenarioBase,
    assessment: TaskRoutingAssessmentResponse,
    purpose: str = "execution",
    reviewer_profile_id: int | None = None,
) -> AgentRoutingPreviewResponse:
    data = AgentRoutingPreviewCreate(
        purpose=purpose,
        assessment_id=assessment.id,
        expected_task_version=base.task.version,
        reviewer_profile_id=reviewer_profile_id,
    )
    rest = await agent_router.preview_task_routing(
        base.task.id,
        data,
        base.pm,
        AgentRoutingService(db),
    )
    mcp = await mcp_agent_tools.preview_task_routing(
        db,
        base.pm,
        base.task.id,
        data.model_dump(mode="json"),
    )
    assert rest.model_dump(mode="json") == mcp
    return rest


async def _dispatch(
    db: AsyncSession,
    *,
    base: ScenarioBase,
    assessment: TaskRoutingAssessmentResponse,
    preview: AgentRoutingPreviewResponse,
    candidate: Candidate,
    key: str,
    purpose: str = "execution",
    queue_class: str = "normal",
    reviewer_profile_id: int | None = None,
):
    selected = preview.recommended_candidate
    assert selected is not None
    assert selected.actor_id == candidate.actor.id
    assert selected.model_binding_id == candidate.binding.id
    return await AgentWorkService(db).create_assignment(
        base.pm,
        ModelAwareAgentTaskAssignmentCreate(
            task_id=base.task.id,
            actor_id=selected.actor_id,
            expected_task_version=base.task.version,
            purpose=purpose,
            queue_class=queue_class,
            reviewer_profile_id=reviewer_profile_id,
            assessment_id=assessment.id,
            model_binding_id=selected.model_binding_id,
            model_binding_revision=selected.model_binding_revision,
            routing_preview_id=preview.preview_id,
            routing_preview_digest=preview.preview_digest,
            reason="Select the current deterministic routing candidate.",
        ),
        idempotency_key=key,
        rationale="Dispatch the selected candidate from the current preview.",
        correlation_id=f"corr-{key}",
    )


async def _persisted_state(db: AsyncSession, task_id: int) -> PersistedState:
    task = await db.get(Task, task_id, populate_existing=True)
    assert task is not None
    assignments = list(
        (
            await db.execute(
                select(AgentTaskAssignment)
                .where(AgentTaskAssignment.task_id == task_id)
                .order_by(AgentTaskAssignment.id)
            )
        )
        .scalars()
        .all()
    )
    runs = list(
        (
            await db.execute(
                select(AgentRun)
                .where(AgentRun.task_id == task_id)
                .order_by(AgentRun.id)
            )
        )
        .scalars()
        .all()
    )
    events = list(
        (
            await db.execute(
                select(TaskEvent)
                .where(TaskEvent.task_id == task_id)
                .order_by(TaskEvent.id)
            )
        )
        .scalars()
        .all()
    )
    return PersistedState(
        task=task,
        assignments=assignments,
        runs=runs,
        events=events,
    )


def _event_payload(event: TaskEvent) -> dict[str, Any]:
    payload = json.loads(event.payload)
    assert isinstance(payload, dict)
    return payload


def _exclusion(
    preview: AgentRoutingPreviewResponse,
    *,
    actor_id: int,
    binding_id: int | None = None,
):
    return next(
        item
        for item in preview.exclusions
        if item.actor_id == actor_id
        and (binding_id is None or item.model_binding_id == binding_id)
    )


def _assert_selected_snapshot(
    snapshot: dict[str, Any],
    *,
    candidate: Candidate,
    assessment: TaskRoutingAssessmentResponse,
) -> None:
    assert snapshot["schema_version"] == "routing-decision-snapshot-v1"
    assert snapshot["selection_pending"] is False
    assert snapshot["assessment_id"] == assessment.id
    assert snapshot["actor_id"] == candidate.actor.id
    assert snapshot["model_binding_id"] == candidate.binding.id
    assert snapshot["model_binding_revision"] == candidate.binding.revision
    assert snapshot["model_catalog_id"] == candidate.catalog.id
    assert snapshot["model_catalog_revision"] == candidate.catalog.revision
    assert snapshot["selection_reason_codes"] == [
        "deterministic-rank",
        "hard-gates-passed",
    ]


def _prior_snapshot(
    *,
    task: Task,
    candidate: Candidate,
    profile: TeamMemberProfile,
    assessment_id: int,
) -> dict[str, Any]:
    return {
        "schema_version": "routing-decision-snapshot-v1",
        "authority": "agent-routing-service-v1",
        "policy_version": "model-aware-routing-v1",
        "selection_pending": False,
        "task_id": task.id,
        "task_version": task.version,
        "assessment_id": assessment_id,
        "assessment_task_version": task.version,
        "assessment_band": "routine",
        "purpose": "execution",
        "actor_id": candidate.actor.id,
        "profile_id": profile.id,
        "model_binding_id": candidate.binding.id,
        "model_binding_revision": candidate.binding.revision,
        "model_catalog_id": candidate.catalog.id,
        "model_catalog_key": candidate.catalog.key,
        "model_catalog_revision": candidate.catalog.revision,
        "configured_model_alias": candidate.catalog.configured_model_alias,
        "selected_reasoning_tier": candidate.catalog.reasoning_tier,
        "selected_context_tier": candidate.catalog.context_tier,
        "review_mode": "none",
        "routing_preview_id": "prior-preview",
        "routing_preview_digest": "d" * 64,
        "input_digest": "e" * 64,
        "selected_rank": 1,
        "adequacy_class": 0,
        "selection_reason_codes": ["hard-gates-passed"],
        "confidence": 0.9,
    }


async def _seed_rework_scenario(
    db: AsyncSession,
    *,
    profile_factory: Any,
    actor_factory: Any,
    team_member_factory: Any,
    task_factory: Any,
    failure_category: str,
    key: str,
):
    base = await _seed_base(
        db,
        profile_factory=profile_factory,
        actor_factory=actor_factory,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        status="active",
        title="Rework a reasoning-limited implementation",
    )
    low = await _add_candidate(
        db,
        actor_factory=actor_factory,
        profile=base.profile,
        key=f"{key}-routine",
        reasoning_tier=1,
        context_tier="small",
        cost_tier="low",
    )
    strong = await _add_binding(
        db,
        actor=low.actor,
        key=f"{key}-standard",
        reasoning_tier=2,
        context_tier="medium",
        cost_tier="medium",
    )
    assessment = await _create_assessment_with_parity(
        db,
        base=base,
        data=_assessment_command(
            task_version=base.task.version,
            required_skill_levels={"backend-python": 3},
            minimum_reasoning_tier=2,
            minimum_context_tier="medium",
            axes={
                "reasoning": 2,
                "ambiguity": 1,
                "context_breadth": 2,
                "risk": 1,
                "verification_burden": 1,
            },
        ),
        key=f"{key}-assessment",
    )
    source = AgentTaskAssignment(
        task_id=base.task.id,
        actor_id=low.actor.id,
        purpose="execution",
        queue_class="normal",
        state="fulfilled",
        task_version=base.task.version,
        model_binding_id=low.binding.id,
        model_binding_revision=low.binding.revision,
        routing_snapshot=json.dumps(
            _prior_snapshot(
                task=base.task,
                candidate=low,
                profile=base.profile,
                assessment_id=assessment.id,
            )
        ),
    )
    db.add(source)
    await db.flush()
    pending_snapshot = AgentWorkService._routing_lineage_snapshot(
        task=base.task,
        source_assignments=[source],
        transition="rework",
        provisional_actor_id=low.actor.id,
        reason="Independent verification rejected the prior execution.",
        evidence={"failure_category": failure_category},
    )
    pending = AgentTaskAssignment(
        task_id=base.task.id,
        actor_id=low.actor.id,
        purpose="execution",
        queue_class="rework",
        state="queued",
        task_version=base.task.version,
        routing_snapshot=json.dumps(pending_snapshot),
        reason="Fresh model-aware selection is required.",
    )
    db.add(pending)
    await db.commit()
    return base, low, strong, assessment, source, pending


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_wave6_scenario_01_routine_task_selects_adequate_low_cost_binding(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    base = await _seed_base(
        db_session,
        profile_factory=profile_factory,
        actor_factory=actor_factory,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
    )
    low = await _add_candidate(
        db_session,
        actor_factory=actor_factory,
        profile=base.profile,
        key="scenario-01-low",
        reasoning_tier=1,
        context_tier="small",
        cost_tier="low",
        latency_tier="fast",
    )
    high = await _add_candidate(
        db_session,
        actor_factory=actor_factory,
        profile=base.profile,
        key="scenario-01-high",
        reasoning_tier=3,
        context_tier="large",
        cost_tier="high",
        latency_tier="slow",
    )
    assessment = await _create_assessment_with_parity(
        db_session,
        base=base,
        data=_assessment_command(
            task_version=base.task.version,
            required_skill_levels={"backend-python": 3},
        ),
        key="scenario-01-assessment",
    )
    preview = await _preview_with_parity(
        db_session,
        base=base,
        assessment=assessment,
    )

    assert preview.recommended_candidate is not None
    assert preview.recommended_candidate.actor_id == low.actor.id
    assert [item.actor_id for item in preview.eligible_candidates] == [
        low.actor.id,
        high.actor.id,
    ]
    assert _exclusion(preview, actor_id=base.pm.id).hard_blocker_codes
    assignment = await _dispatch(
        db_session,
        base=base,
        assessment=assessment,
        preview=preview,
        candidate=low,
        key="scenario-01-assignment",
    )

    _assert_selected_snapshot(
        assignment.routing_snapshot,
        candidate=low,
        assessment=assessment,
    )
    assert {
        item["actor_id"]
        for item in assignment.routing_snapshot["eligible_candidate_summaries"]
    } == {low.actor.id, high.actor.id}
    state = await _persisted_state(db_session, base.task.id)
    assert state.task.status == "planned"
    assert [(item.actor_id, item.state) for item in state.assignments] == [
        (low.actor.id, "queued")
    ]
    assert state.runs == []
    assert [event.event_type for event in state.events] == [
        "agent.routing_assessment_created",
        "agent.routing.assessment_created",
        "agent.assignment_created",
        "agent.routing.assignment_selected",
    ]
    assignment_event = next(
        event
        for event in state.events
        if event.event_type == "agent.assignment_created"
    )
    assert _event_payload(assignment_event)["routing_reason_codes"] == [
        "deterministic-rank",
        "hard-gates-passed",
    ]


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_wave6_scenario_02_advanced_task_excludes_routine_model(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    base = await _seed_base(
        db_session,
        profile_factory=profile_factory,
        actor_factory=actor_factory,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        title="Change several backend modules",
    )
    routine = await _add_candidate(
        db_session,
        actor_factory=actor_factory,
        profile=base.profile,
        key="scenario-02-routine",
        reasoning_tier=1,
        context_tier="small",
        cost_tier="low",
    )
    advanced = await _add_candidate(
        db_session,
        actor_factory=actor_factory,
        profile=base.profile,
        key="scenario-02-advanced",
        reasoning_tier=3,
        context_tier="large",
        cost_tier="high",
        tool_tags=("code-edit",),
        data_policy_tags=("private-source",),
    )
    assessment = await _create_assessment_with_parity(
        db_session,
        base=base,
        data=_assessment_command(
            task_version=base.task.version,
            required_skill_levels={"backend-python": 3},
            minimum_reasoning_tier=3,
            minimum_context_tier="large",
            tool_tags=("code-edit",),
            data_policy_tags=("private-source",),
            axes={
                "reasoning": 3,
                "ambiguity": 2,
                "context_breadth": 3,
                "risk": 2,
                "verification_burden": 2,
            },
        ),
        key="scenario-02-assessment",
    )
    preview = await _preview_with_parity(
        db_session,
        base=base,
        assessment=assessment,
    )

    assert preview.recommended_candidate is not None
    assert preview.recommended_candidate.actor_id == advanced.actor.id
    excluded = _exclusion(
        preview,
        actor_id=routine.actor.id,
        binding_id=routine.binding.id,
    )
    assert {
        "model_reasoning_tier_insufficient",
        "model_context_tier_insufficient",
        "model_tool_missing",
        "model_data_policy_missing",
    }.issubset(excluded.hard_blocker_codes)
    assignment = await _dispatch(
        db_session,
        base=base,
        assessment=assessment,
        preview=preview,
        candidate=advanced,
        key="scenario-02-assignment",
    )

    _assert_selected_snapshot(
        assignment.routing_snapshot,
        candidate=advanced,
        assessment=assessment,
    )
    exclusion_ids = {
        (item["actor_id"], item["model_binding_id"])
        for item in assignment.routing_snapshot["exclusion_summaries"]
    }
    assert (routine.actor.id, routine.binding.id) in exclusion_ids
    state = await _persisted_state(db_session, base.task.id)
    assert [(item.actor_id, item.state) for item in state.assignments] == [
        (advanced.actor.id, "queued")
    ]
    assert state.runs == []


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_wave6_scenario_03_high_risk_migration_routes_independent_specialist(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    base = await _seed_base(
        db_session,
        profile_factory=profile_factory,
        actor_factory=actor_factory,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        skill_key="data-integrity-review",
        title="Migrate a small critical data set",
    )
    implementer = await _add_candidate(
        db_session,
        actor_factory=actor_factory,
        profile=base.profile,
        key="scenario-03-implementer",
        reasoning_tier=3,
        context_tier="large",
        cost_tier="high",
        tool_tags=("shell",),
        data_policy_tags=("restricted-data",),
    )
    verifier_profile = await profile_factory(assignment_modes=["verification"])
    db_session.add(
        TeamMemberProfileSkill(
            profile_id=verifier_profile.id,
            skill_key="data-integrity-review",
            skill_name="Data Integrity Review",
            category="qualification",
            level=5,
            interest=5,
            is_weakness=False,
        )
    )
    await team_member_factory(
        profile=verifier_profile,
        iteration=base.task.iteration,
    )
    verifier = await _add_candidate(
        db_session,
        actor_factory=actor_factory,
        profile=verifier_profile,
        key="scenario-03-verifier",
        reasoning_tier=3,
        context_tier="large",
        cost_tier="high",
        tool_tags=("shell",),
        data_policy_tags=("restricted-data",),
        role="verifier",
    )
    assessment = await _create_assessment_with_parity(
        db_session,
        base=base,
        data=_assessment_command(
            task_version=base.task.version,
            required_skill_levels={"data-integrity-review": 4},
            minimum_reasoning_tier=3,
            minimum_context_tier="large",
            tool_tags=("shell",),
            data_policy_tags=("restricted-data",),
            axes={
                "reasoning": 3,
                "ambiguity": 2,
                "context_breadth": 2,
                "risk": 3,
                "verification_burden": 3,
            },
            reason_codes=(
                "migration",
                "data-integrity",
                "specialist-verification",
            ),
        ),
        key="scenario-03-assessment",
    )
    execution_preview = await _preview_with_parity(
        db_session,
        base=base,
        assessment=assessment,
    )

    assert execution_preview.review_mode == "specialist-independent"
    assert execution_preview.recommended_candidate is not None
    assert execution_preview.recommended_candidate.actor_id == implementer.actor.id
    assert verifier.actor.id in {
        item.actor_id for item in execution_preview.exclusions
    }
    execution = await _dispatch(
        db_session,
        base=base,
        assessment=assessment,
        preview=execution_preview,
        candidate=implementer,
        key="scenario-03-execution",
    )
    execution_row = await db_session.get(AgentTaskAssignment, execution.id)
    assert execution_row is not None
    execution_row.state = "fulfilled"
    base.task.status = "resolved"
    await db_session.commit()

    verification_preview = await _preview_with_parity(
        db_session,
        base=base,
        assessment=assessment,
        purpose="verification",
        reviewer_profile_id=verifier_profile.id,
    )
    assert verification_preview.recommended_candidate is not None
    assert verification_preview.recommended_candidate.actor_id == verifier.actor.id
    implementation_exclusion = _exclusion(
        verification_preview,
        actor_id=implementer.actor.id,
        binding_id=implementer.binding.id,
    )
    assert "verification_actor_not_independent" in (
        implementation_exclusion.hard_blocker_codes
    )
    verification = await _dispatch(
        db_session,
        base=base,
        assessment=assessment,
        preview=verification_preview,
        candidate=verifier,
        key="scenario-03-verification",
        purpose="verification",
        reviewer_profile_id=verifier_profile.id,
    )

    assert verification.routing_snapshot["purpose"] == "verification"
    assert verification.routing_snapshot["review_mode"] == (
        "specialist-independent"
    )
    assert verification.routing_snapshot["reviewer_profile_id"] == (
        verifier_profile.id
    )
    state = await _persisted_state(db_session, base.task.id)
    assert state.task.status == "resolved"
    assert [
        (item.actor_id, item.purpose, item.state)
        for item in state.assignments
    ] == [
        (implementer.actor.id, "execution", "fulfilled"),
        (verifier.actor.id, "verification", "queued"),
    ]
    assert state.runs == []
    assert [event.event_type for event in state.events] == [
        "agent.routing_assessment_created",
        "agent.routing.assessment_created",
        "agent.assignment_created",
        "agent.routing.assignment_selected",
        "agent.assignment_created",
        "agent.routing.assignment_selected",
    ]


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_wave6_scenario_04_large_documentation_prefers_context_adequacy(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    base = await _seed_base(
        db_session,
        profile_factory=profile_factory,
        actor_factory=actor_factory,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        skill_key="documentation",
        title="Apply a repetitive documentation update across the repository",
    )
    context_adequate = await _add_candidate(
        db_session,
        actor_factory=actor_factory,
        profile=base.profile,
        key="scenario-04-context",
        reasoning_tier=1,
        context_tier="large",
        cost_tier="low",
        latency_tier="fast",
    )
    maximum_reasoning = await _add_candidate(
        db_session,
        actor_factory=actor_factory,
        profile=base.profile,
        key="scenario-04-max",
        reasoning_tier=3,
        context_tier="large",
        cost_tier="high",
        latency_tier="slow",
    )
    assessment = await _create_assessment_with_parity(
        db_session,
        base=base,
        data=_assessment_command(
            task_version=base.task.version,
            required_skill_levels={"documentation": 3},
            minimum_reasoning_tier=1,
            minimum_context_tier="large",
            axes={
                "reasoning": 1,
                "ambiguity": 1,
                "context_breadth": 3,
                "risk": 1,
                "verification_burden": 1,
            },
        ),
        key="scenario-04-assessment",
    )
    preview = await _preview_with_parity(
        db_session,
        base=base,
        assessment=assessment,
    )

    assert preview.recommended_candidate is not None
    assert preview.recommended_candidate.actor_id == context_adequate.actor.id
    assert preview.recommended_candidate.reasoning_tier == 1
    assert preview.recommended_candidate.context_tier == "large"
    assert [item.actor_id for item in preview.eligible_candidates] == [
        context_adequate.actor.id,
        maximum_reasoning.actor.id,
    ]
    assignment = await _dispatch(
        db_session,
        base=base,
        assessment=assessment,
        preview=preview,
        candidate=context_adequate,
        key="scenario-04-assignment",
    )

    assert assignment.routing_snapshot["selected_context_tier"] == "large"
    assert assignment.routing_snapshot["selected_reasoning_tier"] == 1
    state = await _persisted_state(db_session, base.task.id)
    assert [(item.actor_id, item.state) for item in state.assignments] == [
        (context_adequate.actor.id, "queued")
    ]
    assert state.runs == []


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_wave6_scenario_05_missing_tool_and_data_policy_fails_closed(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    base = await _seed_base(
        db_session,
        profile_factory=profile_factory,
        actor_factory=actor_factory,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
    )
    inadequate = await _add_candidate(
        db_session,
        actor_factory=actor_factory,
        profile=base.profile,
        key="scenario-05-inadequate",
        reasoning_tier=2,
        context_tier="medium",
        cost_tier="low",
    )
    assessment = await _create_assessment_with_parity(
        db_session,
        base=base,
        data=_assessment_command(
            task_version=base.task.version,
            required_skill_levels={"backend-python": 3},
            minimum_reasoning_tier=2,
            minimum_context_tier="medium",
            tool_tags=("database",),
            data_policy_tags=("regulated-data",),
            axes={
                "reasoning": 2,
                "ambiguity": 1,
                "context_breadth": 2,
                "risk": 2,
                "verification_burden": 2,
            },
        ),
        key="scenario-05-assessment",
    )
    preview = await _preview_with_parity(
        db_session,
        base=base,
        assessment=assessment,
    )

    assert preview.recommended_candidate is None
    assert preview.eligible_candidates == []
    assert preview.hard_blocker_codes == ["no_eligible_candidate"]
    excluded = _exclusion(
        preview,
        actor_id=inadequate.actor.id,
        binding_id=inadequate.binding.id,
    )
    assert {
        "model_tool_missing",
        "model_data_policy_missing",
    }.issubset(excluded.hard_blocker_codes)
    assert excluded.missing_tool_tags == ["database"]
    assert excluded.missing_data_policy_tags == ["regulated-data"]
    state = await _persisted_state(db_session, base.task.id)
    assert state.assignments == []
    assert state.runs == []
    assert [event.event_type for event in state.events] == [
        "agent.routing_assessment_created",
        "agent.routing.assessment_created",
        "agent.routing.no_eligible_candidate",
        "agent.routing.no_eligible_candidate",
    ]


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_wave6_scenario_06_stale_binding_rejects_preview_selection_atomically(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    base = await _seed_base(
        db_session,
        profile_factory=profile_factory,
        actor_factory=actor_factory,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
    )
    worker = await _add_candidate(
        db_session,
        actor_factory=actor_factory,
        profile=base.profile,
        key="scenario-06-worker",
        reasoning_tier=1,
        context_tier="small",
        cost_tier="low",
    )
    assessment = await _create_assessment_with_parity(
        db_session,
        base=base,
        data=_assessment_command(
            task_version=base.task.version,
            required_skill_levels={"backend-python": 3},
        ),
        key="scenario-06-assessment",
    )
    preview = await _preview_with_parity(
        db_session,
        base=base,
        assessment=assessment,
    )
    assert preview.recommended_candidate is not None
    assert preview.recommended_candidate.actor_id == worker.actor.id
    original_revision = preview.recommended_candidate.model_binding_revision
    binding_id = worker.binding.id

    worker.binding.revision += 1
    await db_session.commit()
    with pytest.raises(AgentRoutingConflictError) as conflict:
        await _dispatch(
            db_session,
            base=base,
            assessment=assessment,
            preview=preview,
            candidate=worker,
            key="scenario-06-assignment",
        )
    assert conflict.value.code == "routing_preview_stale"
    assert conflict.value.context["current_input_digest"] != preview.input_digest
    await db_session.rollback()

    state = await _persisted_state(db_session, base.task.id)
    binding = await db_session.get(AgentModelBinding, binding_id)
    assert binding is not None
    assert state.assignments == []
    assert state.runs == []
    assert state.task.status == "planned"
    assert binding.revision == original_revision + 1
    assert [event.event_type for event in state.events] == [
        "agent.routing_assessment_created",
        "agent.routing.assessment_created",
        "agent.routing.stale_conflict",
    ]


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_wave6_scenario_07_material_model_mismatch_blocks_begin_atomically(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    base = await _seed_base(
        db_session,
        profile_factory=profile_factory,
        actor_factory=actor_factory,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
    )
    worker = await _add_candidate(
        db_session,
        actor_factory=actor_factory,
        profile=base.profile,
        key="scenario-07-worker",
        reasoning_tier=1,
        context_tier="small",
        cost_tier="low",
    )
    assessment = await _create_assessment_with_parity(
        db_session,
        base=base,
        data=_assessment_command(
            task_version=base.task.version,
            required_skill_levels={"backend-python": 3},
        ),
        key="scenario-07-assessment",
    )
    preview = await _preview_with_parity(
        db_session,
        base=base,
        assessment=assessment,
    )
    assignment = await _dispatch(
        db_session,
        base=base,
        assessment=assessment,
        preview=preview,
        candidate=worker,
        key="scenario-07-assignment",
    )
    worker_actor_id = worker.actor.id

    with pytest.raises(AgentRoutingConflictError) as conflict:
        await AgentWorkService(db_session).begin(
            worker.actor,
            ModelAwareAgentWorkBegin(
                assignment_id=assignment.id,
                queue_revision=worker.actor.queue_revision,
                model_binding_id=worker.binding.id,
                model_binding_revision=worker.binding.revision,
                resolved_model_id="materially-different-model",
            ),
            idempotency_key="scenario-07-begin",
        )
    assert conflict.value.code == "resolved_model_mismatch"
    assert "observed_model" not in conflict.value.context
    assert conflict.value.context["observed_model_sha256"] == hashlib.sha256(
        b"materially-different-model"
    ).hexdigest(
    )
    await db_session.rollback()

    state = await _persisted_state(db_session, base.task.id)
    assert state.task.status == "planned"
    assert state.task.claimed_by is None
    assert [(item.actor_id, item.state) for item in state.assignments] == [
        (worker_actor_id, "queued")
    ]
    assert state.runs == []
    assert [event.event_type for event in state.events] == [
        "agent.routing_assessment_created",
        "agent.routing.assessment_created",
        "agent.assignment_created",
        "agent.routing.assignment_selected",
        "agent.routing.configured_observed_mismatch",
    ]


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_wave6_scenario_08_reasoning_rejection_permits_explicit_escalation(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    base, low, strong, assessment, source, pending = await _seed_rework_scenario(
        db_session,
        profile_factory=profile_factory,
        actor_factory=actor_factory,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        failure_category="reasoning_insufficiency",
        key="scenario-08",
    )
    preview = await _preview_with_parity(
        db_session,
        base=base,
        assessment=assessment,
    )

    assert preview.recommended_candidate is not None
    assert preview.recommended_candidate.model_binding_id == strong.binding.id
    low_exclusion = _exclusion(
        preview,
        actor_id=low.actor.id,
        binding_id=low.binding.id,
    )
    assert "model_reasoning_tier_insufficient" in (
        low_exclusion.hard_blocker_codes
    )
    updated = await AgentWorkService(db_session).update_assignment(
        pending.id,
        base.pm,
        ModelAwareAgentTaskAssignmentUpdate(
            expected_queue_revision=low.actor.queue_revision,
            actor_id=strong.actor.id,
            assessment_id=assessment.id,
            model_binding_id=strong.binding.id,
            model_binding_revision=strong.binding.revision,
            routing_preview_id=preview.preview_id,
            routing_preview_digest=preview.preview_digest,
        ),
        idempotency_key="scenario-08-update",
        rationale="Apply the explicit governed reasoning-tier escalation.",
        correlation_id="corr-scenario-08-update",
    )

    _assert_selected_snapshot(
        updated.routing_snapshot,
        candidate=strong,
        assessment=assessment,
    )
    lineage = updated.routing_snapshot["prior_lineage"]
    assert lineage["cause"]["category"] == "reasoning_insufficiency"
    assert lineage["model_tier_change"]["eligible"] is True
    assert lineage["model_tier_change"]["applied"] is True
    assert lineage["model_tier_change"]["reason"] == (
        "governed_model_failure_escalation"
    )
    state = await _persisted_state(db_session, base.task.id)
    assert [
        (item.id, item.state, item.model_binding_id)
        for item in state.assignments
    ] == [
        (source.id, "fulfilled", low.binding.id),
        (pending.id, "queued", strong.binding.id),
    ]
    assert state.runs == []
    assignment_event = next(
        event
        for event in reversed(state.events)
        if event.event_type == "agent.assignment_updated"
    )
    assert _event_payload(assignment_event)["routing_reason_codes"] == [
        "deterministic-rank",
        "hard-gates-passed",
    ]


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_wave6_scenario_09_external_blocker_cannot_escalate_model_tier(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    base, low, strong, assessment, source, pending = await _seed_rework_scenario(
        db_session,
        profile_factory=profile_factory,
        actor_factory=actor_factory,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        failure_category="external_service",
        key="scenario-09",
    )
    preview = await _preview_with_parity(
        db_session,
        base=base,
        assessment=assessment,
    )
    assert preview.recommended_candidate is not None
    assert preview.recommended_candidate.model_binding_id == strong.binding.id
    assert "model_reasoning_tier_insufficient" in _exclusion(
        preview,
        actor_id=low.actor.id,
        binding_id=low.binding.id,
    ).hard_blocker_codes
    source_id = source.id
    pending_id = pending.id
    low_binding_id = low.binding.id

    with pytest.raises(AgentRoutingConflictError) as conflict:
        await AgentWorkService(db_session).update_assignment(
            pending.id,
            base.pm,
            ModelAwareAgentTaskAssignmentUpdate(
                expected_queue_revision=low.actor.queue_revision,
                actor_id=strong.actor.id,
                assessment_id=assessment.id,
                model_binding_id=strong.binding.id,
                model_binding_revision=strong.binding.revision,
                routing_preview_id=preview.preview_id,
                routing_preview_digest=preview.preview_digest,
            ),
            idempotency_key="scenario-09-update",
            rationale="Do not convert an external blocker into model escalation.",
            correlation_id="corr-scenario-09-update",
        )
    assert conflict.value.code == "routing_model_escalation_not_allowed"
    assert conflict.value.context["selected_reasoning_tier"] == 2
    await db_session.rollback()

    state = await _persisted_state(db_session, base.task.id)
    assert [
        (item.id, item.state, item.model_binding_id)
        for item in state.assignments
    ] == [
        (source_id, "fulfilled", low_binding_id),
        (pending_id, "queued", None),
    ]
    pending_snapshot = AgentWorkService._routing_snapshot(state.assignments[-1])
    assert pending_snapshot["selection_pending"] is True
    assert pending_snapshot["cause"]["category"] == "non_model_or_unclassified"
    assert state.runs == []
    assert "agent.assignment_updated" not in {
        event.event_type for event in state.events
    }


@pytest.mark.sqlite
@pytest.mark.asyncio
@pytest.mark.parametrize(
    "forged_schema",
    ("routing-lineage-snapshot-v1", "caller-lineage-v1"),
)
async def test_legacy_lineage_cannot_forge_model_escalation_eligibility(
    forged_schema: str,
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    base, low, strong, assessment, _, pending = await _seed_rework_scenario(
        db_session,
        profile_factory=profile_factory,
        actor_factory=actor_factory,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        failure_category="external_service",
        key="legacy-forged-escalation",
    )
    forged = AgentWorkService._routing_snapshot(pending)
    forged.pop("authority", None)
    forged["schema_version"] = forged_schema
    forged["cause"] = {
        "category": "reasoning_insufficiency",
        "reason": "Caller-authored legacy lineage.",
    }
    forged["model_tier_change"] = {
        "eligible": True,
        "applied": False,
        "reason": "caller_claimed_model_failure",
    }
    pending.routing_snapshot = json.dumps(forged)
    await db_session.commit()
    preview = await _preview_with_parity(
        db_session,
        base=base,
        assessment=assessment,
    )

    with pytest.raises(AgentRoutingConflictError) as conflict:
        await AgentWorkService(db_session).update_assignment(
            pending.id,
            base.pm,
            ModelAwareAgentTaskAssignmentUpdate(
                expected_queue_revision=low.actor.queue_revision,
                actor_id=strong.actor.id,
                assessment_id=assessment.id,
                model_binding_id=strong.binding.id,
                model_binding_revision=strong.binding.revision,
                routing_preview_id=preview.preview_id,
                routing_preview_digest=preview.preview_digest,
            ),
            idempotency_key="legacy-forged-escalation-update",
            rationale="Reject caller-authored escalation eligibility.",
            correlation_id="corr-legacy-forged-escalation-update",
        )

    assert conflict.value.code == "routing_lineage_authority_unverified"
    await db_session.rollback()
    persisted = await db_session.get(AgentTaskAssignment, pending.id)
    assert persisted is not None
    assert (
        AgentWorkService._routing_snapshot(persisted)["model_tier_change"][
            "eligible"
        ]
        is True
    )


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_completed_legacy_lineage_drops_arbitrary_private_fields(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    base, low, strong, assessment, _, pending = await _seed_rework_scenario(
        db_session,
        profile_factory=profile_factory,
        actor_factory=actor_factory,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
        failure_category="reasoning_insufficiency",
        key="legacy-private-lineage",
    )
    forged = AgentWorkService._routing_snapshot(pending)
    forged["raw_prompt"] = "PRIVATE-PROMPT-SENTINEL"
    forged["private_log"] = "PRIVATE-LOG-SENTINEL"
    forged["cause"]["private_log"] = "PRIVATE-CAUSE-SENTINEL"
    forged["model_tier_change"]["raw_prompt"] = (
        "PRIVATE-TIER-SENTINEL"
    )
    forged["prior_decisions"][0]["private_log"] = (
        "PRIVATE-DECISION-SENTINEL"
    )
    forged["prior_decisions"][0]["trust_lineage"] = {
        "execution_actor_id": low.actor.id,
        "private_log": "PRIVATE-TRUST-SENTINEL",
    }
    pending.routing_snapshot = json.dumps(forged)
    await db_session.commit()
    preview = await _preview_with_parity(
        db_session,
        base=base,
        assessment=assessment,
    )

    updated = await AgentWorkService(db_session).update_assignment(
        pending.id,
        base.pm,
        ModelAwareAgentTaskAssignmentUpdate(
            expected_queue_revision=low.actor.queue_revision,
            actor_id=strong.actor.id,
            assessment_id=assessment.id,
            model_binding_id=strong.binding.id,
            model_binding_revision=strong.binding.revision,
            routing_preview_id=preview.preview_id,
            routing_preview_digest=preview.preview_digest,
        ),
        idempotency_key="legacy-private-lineage-update",
        rationale="Complete selection without carrying caller-private fields.",
        correlation_id="corr-legacy-private-lineage-update",
    )

    encoded = json.dumps(
        updated.routing_snapshot["prior_lineage"],
        sort_keys=True,
    )
    assert "PRIVATE-" not in encoded
    assert "raw_prompt" not in encoded
    assert "private_log" not in encoded
    lineage = updated.routing_snapshot["prior_lineage"]
    assert lineage["cause"]["category"] == "reasoning_insufficiency"
    assert lineage["model_tier_change"]["eligible"] is True
    assert lineage["model_tier_change"]["applied"] is True


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_wave6_scenario_10_capacity_recommendations_remain_unchanged(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    base = await _seed_base(
        db_session,
        profile_factory=profile_factory,
        actor_factory=actor_factory,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
    )
    alternate_profile = await profile_factory(assignment_modes=["execution"])
    db_session.add(
        TeamMemberProfileSkill(
            profile_id=alternate_profile.id,
            skill_key="backend-python",
            skill_name="Backend Python",
            category="qualification",
            level=3,
            interest=3,
            is_weakness=False,
        )
    )
    await team_member_factory(
        profile=alternate_profile,
        iteration=base.task.iteration,
    )
    await db_session.commit()
    recommendation_service = AssigneeRecommendationService(db_session)
    before = await recommendation_service.recommend_for_task(base.task.id)
    assert before is not None
    before_payload = [item.model_dump(mode="json") for item in before]

    worker = await _add_candidate(
        db_session,
        actor_factory=actor_factory,
        profile=base.profile,
        key="scenario-10-worker",
        reasoning_tier=1,
        context_tier="small",
        cost_tier="low",
    )
    assessment = await _create_assessment_with_parity(
        db_session,
        base=base,
        data=_assessment_command(
            task_version=base.task.version,
            required_skill_levels={"backend-python": 3},
        ),
        key="scenario-10-assessment",
    )
    preview = await _preview_with_parity(
        db_session,
        base=base,
        assessment=assessment,
    )
    after = await recommendation_service.recommend_for_task(base.task.id)
    assert after is not None

    assert preview.recommended_candidate is not None
    assert preview.recommended_candidate.actor_id == worker.actor.id
    assert [item.model_dump(mode="json") for item in after] == before_payload
    state = await _persisted_state(db_session, base.task.id)
    assert state.assignments == []
    assert state.runs == []
    assert [event.event_type for event in state.events] == [
        "agent.routing_assessment_created",
        "agent.routing.assessment_created",
    ]


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_wave6_scenario_11_reassignment_without_fresh_preview_is_rejected(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    base = await _seed_base(
        db_session,
        profile_factory=profile_factory,
        actor_factory=actor_factory,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
    )
    first = await _add_candidate(
        db_session,
        actor_factory=actor_factory,
        profile=base.profile,
        key="scenario-11-first",
        reasoning_tier=1,
        context_tier="small",
        cost_tier="low",
    )
    replacement = await _add_candidate(
        db_session,
        actor_factory=actor_factory,
        profile=base.profile,
        key="scenario-11-replacement",
        reasoning_tier=1,
        context_tier="small",
        cost_tier="low",
    )
    assessment = await _create_assessment_with_parity(
        db_session,
        base=base,
        data=_assessment_command(
            task_version=base.task.version,
            required_skill_levels={"backend-python": 3},
        ),
        key="scenario-11-assessment",
    )
    preview = await _preview_with_parity(
        db_session,
        base=base,
        assessment=assessment,
    )
    assert [item.actor_id for item in preview.eligible_candidates] == [
        first.actor.id,
        replacement.actor.id,
    ]
    assignment = await _dispatch(
        db_session,
        base=base,
        assessment=assessment,
        preview=preview,
        candidate=first,
        key="scenario-11-assignment",
    )
    original_snapshot = assignment.routing_snapshot
    first_actor_id = first.actor.id

    with pytest.raises(AgentRoutingConflictError) as conflict:
        await AgentWorkService(db_session).update_assignment(
            assignment.id,
            base.pm,
            AgentTaskAssignmentUpdate(
                actor_id=replacement.actor.id,
                expected_queue_revision=first.actor.queue_revision,
            ),
            idempotency_key="scenario-11-update",
            rationale="Attempt a reassignment without regenerating the preview.",
            correlation_id="corr-scenario-11-update",
        )
    assert conflict.value.code == "model_aware_assignment_update_required"
    assert conflict.value.context["changed_fields"] == ["actor_id"]
    await db_session.rollback()

    state = await _persisted_state(db_session, base.task.id)
    assert len(state.assignments) == 1
    assert state.assignments[0].actor_id == first_actor_id
    assert AgentWorkService._routing_snapshot(state.assignments[0]) == (
        original_snapshot
    )
    assert state.runs == []
    assert "agent.assignment_updated" not in {
        event.event_type for event in state.events
    }


@pytest.mark.sqlite
@pytest.mark.asyncio
async def test_wave6_scenario_12_matching_self_report_is_unattested_and_mismatch_inert(
    db_session: AsyncSession,
    profile_factory,
    actor_factory,
    team_member_factory,
    task_factory,
) -> None:
    base = await _seed_base(
        db_session,
        profile_factory=profile_factory,
        actor_factory=actor_factory,
        team_member_factory=team_member_factory,
        task_factory=task_factory,
    )
    worker = await _add_candidate(
        db_session,
        actor_factory=actor_factory,
        profile=base.profile,
        key="scenario-12-worker",
        reasoning_tier=1,
        context_tier="small",
        cost_tier="low",
    )
    assessment = await _create_assessment_with_parity(
        db_session,
        base=base,
        data=_assessment_command(
            task_version=base.task.version,
            required_skill_levels={"backend-python": 3},
        ),
        key="scenario-12-assessment",
    )
    preview = await _preview_with_parity(
        db_session,
        base=base,
        assessment=assessment,
    )
    assignment = await _dispatch(
        db_session,
        base=base,
        assessment=assessment,
        preview=preview,
        candidate=worker,
        key="scenario-12-assignment",
    )
    worker_actor_id = worker.actor.id
    worker_binding_id = worker.binding.id
    worker_catalog_key = worker.catalog.key
    worker_configured_alias = worker.catalog.configured_model_alias

    with pytest.raises(AgentRoutingConflictError) as mismatch:
        await AgentWorkService(db_session).begin(
            worker.actor,
            ModelAwareAgentWorkBegin(
                assignment_id=assignment.id,
                queue_revision=worker.actor.queue_revision,
                model_binding_id=worker.binding.id,
                model_binding_revision=worker.binding.revision,
                resolved_model_id="not-the-selected-model",
            ),
            idempotency_key="scenario-12-mismatch",
        )
    assert mismatch.value.code == "resolved_model_mismatch"
    await db_session.rollback()
    inert = await _persisted_state(db_session, base.task.id)
    assert inert.task.status == "planned"
    assert inert.task.claimed_by is None
    assert inert.assignments[0].state == "queued"
    assert inert.runs == []

    actor = await db_session.get(
        AgentActor,
        worker_actor_id,
        populate_existing=True,
    )
    binding = await db_session.get(
        AgentModelBinding,
        worker_binding_id,
        populate_existing=True,
    )
    assert actor is not None
    assert binding is not None
    begun = await AgentWorkService(db_session).begin(
        actor,
        ModelAwareAgentWorkBegin(
            assignment_id=assignment.id,
            queue_revision=actor.queue_revision,
            model_binding_id=binding.id,
            model_binding_revision=binding.revision,
            resolved_model_id=worker_catalog_key,
        ),
        idempotency_key="scenario-12-matched",
    )

    assert begun.assignment.state == "accepted"
    assert begun.task.status == "active"
    assert begun.run.status == "running"
    assert begun.run.configured_model_alias == worker_configured_alias
    assert begun.run.resolved_model_id == worker_catalog_key
    assert begun.run.model_trust_state == "matched"
    assert begun.run.model_match_basis == "catalog_key"
    state = await _persisted_state(db_session, base.task.id)
    assert len(state.runs) == 1
    assert state.runs[0].model_trust_state == "matched"
    assert state.runs[0].model_match_basis == "catalog_key"
    began_event = next(
        event for event in state.events if event.event_type == "agent.work_began"
    )
    began_payload = _event_payload(began_event)
    assert began_payload["model_evidence_source"] == "worker_report"
    assert began_payload["model_attested"] is False
    assert began_payload["model_trust_state"] == "matched"
