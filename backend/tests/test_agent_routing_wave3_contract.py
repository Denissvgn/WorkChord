"""Focused policy and schema contracts for deterministic Wave 3 routing."""

from datetime import UTC, datetime, timedelta

import pytest
from pydantic import ValidationError

from app.schemas.agent_routing import (
    AgentRoutingCandidate,
    AgentRoutingExclusion,
    AgentRoutingPreviewCreate,
    AgentRoutingPreviewResponse,
    RoutingDecisionSnapshot,
    RoutingTrustLineage,
    TaskRoutingAssessmentCommand,
    TaskRoutingAssessmentListResponse,
    TaskRoutingAssessmentResponse,
    TaskRoutingAssessmentState,
)
from app.services.agent_routing_policy import (
    MAX_ROUTING_CANDIDATES,
    MAX_ROUTING_EXCLUSIONS,
    MIN_ROUTING_ASSESSMENT_CONFIDENCE,
    ROUTING_PREVIEW_TTL_SECONDS,
    RoutingBlockerCode,
    evaluate_model_envelope,
    evaluate_required_skills,
    routing_candidate_rank_key,
)


def _assessment_command(**overrides: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "expected_task_version": 2,
        "band": "routine",
        "axes": {
            "reasoning": 1,
            "ambiguity": 1,
            "context_breadth": 1,
            "risk": 1,
            "verification_burden": 1,
        },
        "required_skill_levels": {"backend-python": 2},
        "required_model": {
            "minimum_reasoning_tier": 1,
            "minimum_context_tier": "small",
            "modality_tags": ["text"],
            "tool_tags": ["shell"],
            "data_policy_tags": ["workspace-source"],
        },
        "review_mode": "none",
        "confidence": 0.8,
        "reason_codes": [],
        "rationale": "Bounded deterministic work.",
    }
    payload.update(overrides)
    return payload


def _assessment_response(*, is_current: bool = True) -> TaskRoutingAssessmentResponse:
    return TaskRoutingAssessmentResponse(
        id=4,
        task_id=1,
        task_version=2,
        policy_version="model-aware-routing-v1",
        band="routine",
        axes={
            "reasoning": 1,
            "ambiguity": 1,
            "context_breadth": 1,
            "risk": 1,
            "verification_burden": 1,
        },
        required_skill_levels={"backend-python": 2},
        required_model={
            "minimum_reasoning_tier": 1,
            "minimum_context_tier": "small",
            "modality_tags": ["text"],
            "tool_tags": ["shell"],
            "data_policy_tags": ["workspace-source"],
        },
        review_mode="none",
        confidence=0.8,
        reason_codes=[],
        rationale="Bounded deterministic work.",
        assessor="pm-agent",
        assessor_actor_id=9,
        created_at=datetime(2026, 7, 27, 10, tzinfo=UTC),
        policy_conformant=True,
        is_current=is_current,
    )


def _candidate(**overrides: object) -> AgentRoutingCandidate:
    payload: dict[str, object] = {
        "actor_id": 11,
        "actor_revision": 2,
        "actor_queue_revision": 3,
        "profile_id": 21,
        "profile_revision": "p21-1234567890abcdef12345678",
        "capacity_owner_id": 31,
        "capacity_owner_profile_id": 21,
        "model_binding_id": 41,
        "model_binding_revision": 4,
        "model_catalog_id": 51,
        "model_catalog_key": "standard-code",
        "model_catalog_revision": 5,
        "configured_model_alias": "configured-code-model",
        "matched_skill_levels": {"backend-python": 3},
        "reasoning_tier": 1,
        "context_tier": "small",
        "modality_tags": ["text"],
        "tool_tags": ["shell"],
        "data_policy_tags": ["workspace-source"],
        "cost_tier": "low",
        "latency_tier": "fast",
        "available_capacity_days": 4.0,
        "committed_effort_days": 1.0,
        "workload_ratio": 0.2,
        "queued_assignments": 0,
        "accepted_assignments": 0,
        "running_runs": 0,
        "schedule_delay_days": 0,
        "adequacy_class": 0,
        "rank": 1,
        "confidence": 0.8,
        "rationale": "Meets every hard gate.",
    }
    payload.update(overrides)
    return AgentRoutingCandidate.model_validate(payload)


@pytest.mark.contract
def test_wave3_policy_limits_and_blocker_vocabulary_are_frozen() -> None:
    assert MIN_ROUTING_ASSESSMENT_CONFIDENCE == 0.60
    assert ROUTING_PREVIEW_TTL_SECONDS == 300
    assert MAX_ROUTING_CANDIDATES == 25
    assert MAX_ROUTING_EXCLUSIONS == 50
    assert {
        "assessment_missing",
        "task_definition_not_ready",
        "required_skill_missing",
        "model_binding_disabled",
        "model_context_tier_insufficient",
        "capacity_unavailable",
        "vacation_conflict",
        "queue_limit_exceeded",
        "current_work_conflict",
        "preview_expired",
        "no_eligible_candidate",
    } <= {code.value for code in RoutingBlockerCode}


@pytest.mark.contract
def test_required_skill_decision_is_deterministic_and_fail_closed() -> None:
    decision = evaluate_required_skills(
        required_skill_levels={
            "security-review": 3,
            "backend-python": 4,
            "data-integrity-review": 2,
        },
        actual_skill_levels={
            "backend-python": 3,
            "security-review": 5,
        },
        weakness_keys=["security-review"],
    )

    assert decision.hard_blocker_codes == (
        "required_skill_missing",
        "required_skill_level_insufficient",
        "required_skill_blocking_weakness",
    )
    assert decision.missing_skill_keys == ("data-integrity-review",)
    assert decision.insufficient_skill_keys == ("backend-python",)
    assert decision.blocking_weakness_keys == ("security-review",)
    assert decision.eligible is False


@pytest.mark.contract
def test_model_envelope_and_rank_inputs_never_trade_eligibility_for_cost() -> None:
    required = {
        "minimum_reasoning_tier": 2,
        "minimum_context_tier": "medium",
        "modality_tags": ["text"],
        "tool_tags": ["shell", "code-edit"],
        "data_policy_tags": ["workspace-source"],
    }
    inadequate = evaluate_model_envelope(
        required,
        actual_reasoning_tier=1,
        actual_context_tier="small",
        actual_modality_tags=["text"],
        actual_tool_tags=["shell"],
        actual_data_policy_tags=[],
    )
    assert inadequate.adequacy_class is None
    assert inadequate.hard_blocker_codes == (
        "model_reasoning_tier_insufficient",
        "model_context_tier_insufficient",
        "model_tool_missing",
        "model_data_policy_missing",
    )

    adequate = evaluate_model_envelope(
        required,
        actual_reasoning_tier=3,
        actual_context_tier="large",
        actual_modality_tags=["text"],
        actual_tool_tags=["code-edit", "shell"],
        actual_data_policy_tags=["workspace-source"],
    )
    assert adequate.eligible is True
    assert adequate.adequacy_class == 2
    assert routing_candidate_rank_key(
        adequacy_class=0,
        cost_tier="high",
        queue_depth=0,
        schedule_delay_days=0,
        latency_tier="fast",
        actor_id=9,
        binding_id=4,
    ) < routing_candidate_rank_key(
        adequacy_class=1,
        cost_tier="low",
        queue_depth=0,
        schedule_delay_days=0,
        latency_tier="fast",
        actor_id=1,
        binding_id=1,
    )


@pytest.mark.contract
def test_assessment_command_owns_only_client_fields_and_rejects_low_confidence() -> None:
    command = TaskRoutingAssessmentCommand.model_validate(_assessment_command())
    assert set(TaskRoutingAssessmentCommand.model_fields) == {
        "expected_task_version",
        "band",
        "axes",
        "required_skill_levels",
        "required_model",
        "review_mode",
        "confidence",
        "reason_codes",
        "rationale",
    }
    with pytest.raises(ValidationError, match="greater than or equal"):
        TaskRoutingAssessmentCommand.model_validate(
            _assessment_command(confidence=0.599)
        )
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        TaskRoutingAssessmentCommand.model_validate(
            _assessment_command(assessor="spoofed")
        )


@pytest.mark.contract
def test_assessment_state_and_history_are_explicit_and_version_bound() -> None:
    current = _assessment_response()
    state = TaskRoutingAssessmentState(
        task_id=1,
        current_task_version=2,
        state="current",
        assessment=current,
    )
    history = TaskRoutingAssessmentListResponse(
        task_id=1,
        current_task_version=2,
        assessments=[current],
        total_count=1,
    )
    assert state.assessment == current
    assert history.omitted_count == 0
    with pytest.raises(ValidationError, match="requires an assessment"):
        TaskRoutingAssessmentState(
            task_id=1,
            current_task_version=2,
            state="stale",
        )


@pytest.mark.contract
def test_preview_contract_accepts_eligible_and_explicit_no_candidate_states() -> None:
    generated_at = datetime(2026, 7, 27, 12, tzinfo=UTC)
    candidate = _candidate()
    preview = AgentRoutingPreviewResponse(
        preview_id="preview-1",
        preview_digest="a" * 64,
        input_digest="b" * 64,
        task_id=1,
        purpose="execution",
        assessment_id=4,
        assessment_task_version=2,
        current_task_version=2,
        review_mode="none",
        generated_at=generated_at,
        expires_at=generated_at + timedelta(seconds=ROUTING_PREVIEW_TTL_SECONDS),
        recommended_candidate=candidate,
        eligible_candidates=[candidate],
    )
    assert preview.recommended_candidate == preview.eligible_candidates[0]

    exclusion = AgentRoutingExclusion(
        actor_id=12,
        actor_revision=1,
        actor_queue_revision=1,
        hard_blocker_codes=["actor_disabled"],
        rationale="Actor is disabled.",
    )
    empty = AgentRoutingPreviewResponse(
        preview_id="preview-2",
        preview_digest="c" * 64,
        input_digest="d" * 64,
        task_id=1,
        purpose="execution",
        assessment_id=4,
        assessment_task_version=2,
        current_task_version=2,
        review_mode="none",
        generated_at=generated_at,
        expires_at=generated_at + timedelta(seconds=ROUTING_PREVIEW_TTL_SECONDS),
        exclusions=[exclusion],
        hard_blocker_codes=["no_eligible_candidate"],
    )
    assert empty.recommended_candidate is None

    with pytest.raises(ValidationError, match="frozen 300-second TTL"):
        AgentRoutingPreviewResponse.model_validate(
            {
                **preview.model_dump(),
                "expires_at": generated_at + timedelta(seconds=301),
            }
        )
    assert AgentRoutingPreviewCreate(
        purpose="verification",
        assessment_id=4,
        expected_task_version=2,
        reviewer_profile_id=21,
    ).purpose == "verification"


@pytest.mark.contract
def test_routing_decision_snapshot_is_immutable_and_preserves_trust_lineage() -> None:
    generated_at = datetime(2026, 7, 27, 12, tzinfo=UTC)
    snapshot = RoutingDecisionSnapshot(
        task_id=1,
        task_version=2,
        assessment_id=4,
        assessment_task_version=2,
        assessment_band="routine",
        assessment_confidence=0.8,
        purpose="execution",
        actor_id=11,
        actor_revision=2,
        actor_queue_revision=3,
        profile_id=21,
        profile_revision="p21-1234567890abcdef12345678",
        capacity_owner_id=31,
        capacity_owner_profile_id=21,
        model_binding_id=41,
        model_binding_revision=4,
        model_catalog_id=51,
        model_catalog_key="standard-code",
        model_catalog_revision=5,
        configured_model_alias="configured-code-model",
        selected_reasoning_tier=1,
        selected_context_tier="small",
        review_mode="none",
        routing_preview_id="preview-1",
        routing_preview_digest="a" * 64,
        input_digest="b" * 64,
        preview_generated_at=generated_at,
        preview_expires_at=generated_at
        + timedelta(seconds=ROUTING_PREVIEW_TTL_SECONDS),
        selected_rank=1,
        adequacy_class=0,
        selection_reason_codes=["lowest-cost-adequate"],
        eligible_candidate_summaries=[
            {
                "actor_id": 11,
                "profile_id": 21,
                "model_binding_id": 41,
                "model_binding_revision": 4,
                "model_catalog_key": "standard-code",
                "rank": 1,
                "adequacy_class": 0,
                "cost_tier": "low",
                "latency_tier": "fast",
            }
        ],
        exclusion_summaries=[
            {
                "actor_id": 12,
                "model_binding_id": None,
                "hard_blocker_codes": ["model_binding_missing"],
            }
        ],
        rationale="Selected by deterministic routing policy.",
        confidence=0.8,
        trust_lineage=RoutingTrustLineage(
            assessment_assessor="pm-agent",
            assessment_assessor_actor_id=9,
            preview_requested_by_actor_id=9,
            assignment_created_by_actor_id=9,
            execution_actor_id=11,
        ),
    )
    assert snapshot.selection_pending is False
    assert snapshot.trust_lineage.execution_actor_id == snapshot.actor_id
    with pytest.raises(ValidationError, match="frozen"):
        snapshot.actor_id = 99
