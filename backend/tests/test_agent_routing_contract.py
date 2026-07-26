"""Focused contract tests for model-aware routing vocabulary and compatibility."""

from __future__ import annotations

from collections import UserDict
from copy import deepcopy
from datetime import UTC, datetime
import json
from types import MappingProxyType

import pytest
from pydantic import ValidationError

from app.models.agent import AgentActor, TaskRoutingAssessment
from app.schemas.agent import (
    MAX_AGENT_JSON_BYTES,
    AgentTaskAssignmentCreate,
)
from app.schemas.agent_routing import (
    MAX_ROUTING_JSON_BYTES,
    MAX_ROUTING_TAGS,
    AgentModelBindingCreate,
    AgentModelCatalogCreate,
    TaskRoutingAssessmentCreate,
    TaskRoutingAssessmentResponse,
)
from app.services.agent_profile_catalog_service import (
    AgentProfileCatalogService,
    CAPABILITY_SKILLS,
)
from app.services.agent_routing_policy import (
    ASSESSMENT_REASON_CODES,
    CAPABILITY_LABEL_SKILL_KEYS,
    COST_TIER_ORDER,
    LATENCY_TIER_ORDER,
    MAX_ROUTING_PACKET_BYTES,
    MAX_ROUTING_SNAPSHOT_BYTES,
    AssessmentReasonCode,
    AssignmentIntent,
    ContextTier,
    CostTier,
    DifficultyAxis,
    DifficultyBand,
    LatencyTier,
    ROUTING_POLICY_VERSION,
    ROUTING_SKILL_KEYS,
    ReasoningTier,
    ReviewMode,
    RoutingBlockerCode,
    RoutingProfileEvidence,
    assignment_intent,
    canonical_routing_json_bytes,
    context_tier_meets,
    derive_difficulty_band,
    evaluate_actor_authorization,
    evaluate_assignment_compatibility,
    minimum_review_mode,
    routing_skills_for_capability_labels,
    validate_routing_packet_size,
)
from app.services.label_service import CAPABILITY_LABEL_DESCRIPTIONS
from app.services.agent_work_service import AgentWorkService


EXPECTED_REASON_REVIEW_FLOORS = {
    "novel-architecture": "standard",
    "material-ambiguity": "standard",
    "broad-context": "standard",
    "security": "independent",
    "authorization": "independent",
    "migration": "independent",
    "data-integrity": "independent",
    "concurrency": "independent",
    "production": "independent",
    "irreversible-change": "independent",
    "independent-verification": "independent",
    "specialist-verification": "specialist-independent",
}


def _catalog_payload(**overrides):
    payload = {
        "key": "balanced-code",
        "provider": "configured-provider",
        "configured_model_alias": "balanced-code",
        "reasoning_tier": 2,
        "context_tier": "medium",
        "modality_tags": ["text"],
        "cost_tier": "medium",
        "latency_tier": "balanced",
        "enabled": True,
        "revision": 1,
    }
    payload.update(overrides)
    return payload


def _assessment_payload(
    *,
    axes: dict[str, int] | None = None,
    reason_codes: list[str] | None = None,
    **overrides,
):
    axes = axes or {
        "reasoning": 2,
        "ambiguity": 2,
        "context_breadth": 2,
        "risk": 2,
        "verification_burden": 2,
    }
    reason_codes = reason_codes or []
    payload = {
        "task_id": 42,
        "task_version": 7,
        "policy_version": ROUTING_POLICY_VERSION,
        "band": derive_difficulty_band(axes, reason_codes),
        "axes": axes,
        "required_skill_levels": {
            "backend-python": 4,
            "data-integrity-review": 3,
        },
        "required_model": {
            "minimum_reasoning_tier": 2,
            "minimum_context_tier": "medium",
            "modality_tags": ["text"],
            "tool_tags": ["code-edit", "shell"],
            "data_policy_tags": ["workspace-source"],
        },
        "review_mode": minimum_review_mode(axes, reason_codes),
        "confidence": 0.86,
        "reason_codes": reason_codes,
        "rationale": "Bounded routing contract fixture.",
        "assessor": "pm-controller",
    }
    payload.update(overrides)
    return payload


def _profile(
    *,
    profile_id: int = 10,
    profile_kind: str = "agent",
    automation_enabled: bool = True,
    assignment_modes: frozenset[str] = frozenset({"execution"}),
    skill_levels: dict[str, int] | None = None,
    weakness_keys: frozenset[str] = frozenset(),
) -> RoutingProfileEvidence:
    return RoutingProfileEvidence(
        profile_id=profile_id,
        profile_kind=profile_kind,
        automation_enabled=automation_enabled,
        assignment_modes=assignment_modes,
        skill_levels=skill_levels or {},
        weakness_keys=weakness_keys,
    )


@pytest.mark.contract
@pytest.mark.parametrize("tier", list(ReasoningTier))
def test_every_reasoning_tier_is_accepted(tier: ReasoningTier) -> None:
    normalized = AgentModelCatalogCreate.model_validate(
        _catalog_payload(reasoning_tier=tier.value)
    )
    assert normalized.reasoning_tier == tier.value


@pytest.mark.contract
@pytest.mark.parametrize("tier", list(ContextTier))
def test_every_context_tier_is_accepted(tier: ContextTier) -> None:
    catalog = AgentModelCatalogCreate.model_validate(
        _catalog_payload(context_tier=tier.value)
    )
    assessment = TaskRoutingAssessmentCreate.model_validate(
        _assessment_payload(
            required_model={
                "minimum_reasoning_tier": 2,
                "minimum_context_tier": tier.value,
                "modality_tags": ["text"],
                "tool_tags": [],
                "data_policy_tags": [],
            }
        )
    )
    assert catalog.context_tier == tier.value
    assert assessment.required_model.minimum_context_tier == tier.value


@pytest.mark.contract
@pytest.mark.parametrize("tier", list(CostTier))
def test_every_cost_tier_is_accepted(tier: CostTier) -> None:
    assert (
        AgentModelCatalogCreate.model_validate(
            _catalog_payload(cost_tier=tier.value)
        ).cost_tier
        == tier.value
    )


@pytest.mark.contract
@pytest.mark.parametrize("tier", list(LatencyTier))
def test_every_latency_tier_is_accepted(tier: LatencyTier) -> None:
    assert (
        AgentModelCatalogCreate.model_validate(
            _catalog_payload(latency_tier=tier.value)
        ).latency_tier
        == tier.value
    )


@pytest.mark.contract
@pytest.mark.parametrize("review_mode", list(ReviewMode))
def test_every_review_mode_is_accepted_when_it_meets_policy(
    review_mode: ReviewMode,
) -> None:
    axes = {axis.value: 1 for axis in DifficultyAxis}
    normalized = TaskRoutingAssessmentCreate.model_validate(
        _assessment_payload(
            axes=axes,
            review_mode=review_mode.value,
        )
    )
    assert normalized.review_mode == review_mode.value


@pytest.mark.contract
def test_unknown_closed_vocabulary_values_fail_validation() -> None:
    catalog_mutations = (
        {"reasoning_tier": 4},
        {"reasoning_tier": True},
        {"reasoning_tier": "2"},
        {"context_tier": "huge"},
        {"cost_tier": "free"},
        {"latency_tier": "instant"},
    )
    for mutation in catalog_mutations:
        with pytest.raises(ValidationError):
            AgentModelCatalogCreate.model_validate(
                _catalog_payload(**mutation)
            )

    assessment_mutations = (
        {"policy_version": "model-aware-routing-v2"},
        {"band": "expert"},
        {"review_mode": "self-approved"},
    )
    for mutation in assessment_mutations:
        with pytest.raises(ValidationError):
            TaskRoutingAssessmentCreate.model_validate(
                _assessment_payload(**mutation)
            )

    payload = _assessment_payload()
    payload["required_model"]["minimum_reasoning_tier"] = "2"
    with pytest.raises(ValidationError):
        TaskRoutingAssessmentCreate.model_validate(payload)


@pytest.mark.contract
@pytest.mark.parametrize(
    ("reason_code", "expected_review"),
    EXPECTED_REASON_REVIEW_FLOORS.items(),
)
def test_every_governed_reason_code_is_accepted(
    reason_code: str,
    expected_review: str,
) -> None:
    assert set(EXPECTED_REASON_REVIEW_FLOORS) == {
        item.value for item in AssessmentReasonCode
    }
    axes = {axis.value: 1 for axis in DifficultyAxis}
    assert minimum_review_mode(axes, [reason_code]) == expected_review
    normalized = TaskRoutingAssessmentCreate.model_validate(
        _assessment_payload(
            axes=axes,
            reason_codes=[reason_code],
            review_mode=expected_review,
        )
    )
    assert normalized.reason_codes == [reason_code]
    assert normalized.band == DifficultyBand.ADVANCED.value


@pytest.mark.contract
def test_unknown_reason_and_skill_keys_fail_closed() -> None:
    payload = _assessment_payload()
    payload["reason_codes"] = ["invented-reason"]
    with pytest.raises(ValidationError, match="Unknown assessment reason"):
        TaskRoutingAssessmentCreate.model_validate(
            payload
        )
    with pytest.raises(ValidationError, match="Unknown routing skill key"):
        TaskRoutingAssessmentCreate.model_validate(
            _assessment_payload(
                required_skill_levels={"invented-skill": 3}
            )
        )


@pytest.mark.contract
@pytest.mark.parametrize(
    "reason_codes",
    (
        [1],
        [None],
        [b"security"],
        [object()],
        b"security",
        ("migration", "data-integrity"),
    ),
)
def test_malformed_reason_codes_are_normal_validation_failures(
    reason_codes: object,
) -> None:
    payload = _assessment_payload()
    payload["reason_codes"] = reason_codes
    with pytest.raises(ValidationError):
        TaskRoutingAssessmentCreate.model_validate(payload)


@pytest.mark.contract
@pytest.mark.parametrize(
    "required_skill_levels",
    (
        MappingProxyType({"invented-skill": 3}),
        UserDict({"invented-skill": 3}),
    ),
)
def test_mapping_wrappers_cannot_bypass_closed_skill_validation(
    required_skill_levels: object,
) -> None:
    with pytest.raises(ValidationError, match="Unknown routing skill key"):
        TaskRoutingAssessmentCreate.model_validate(
            _assessment_payload(
                required_skill_levels=required_skill_levels,
            )
        )


@pytest.mark.contract
def test_normalized_duplicates_fail_closed() -> None:
    payload = _assessment_payload()
    payload["reason_codes"] = ["migration", " MIGRATION "]
    with pytest.raises(ValidationError, match="reason_codes entries must be unique"):
        TaskRoutingAssessmentCreate.model_validate(
            payload
        )
    with pytest.raises(
        ValidationError,
        match="Required skill keys must be unique after normalization",
    ):
        TaskRoutingAssessmentCreate.model_validate(
            _assessment_payload(
                required_skill_levels={
                    "Backend-Python": 3,
                    "backend-python": 4,
                }
            )
        )

    duplicate_required_model_fields = (
        ("modality_tags", ["text", " TEXT "]),
        ("tool_tags", ["shell", " SHELL "]),
        ("data_policy_tags", ["workspace-source", " WORKSPACE-SOURCE "]),
    )
    for field_name, values in duplicate_required_model_fields:
        payload = _assessment_payload()
        payload["required_model"][field_name] = values
        with pytest.raises(ValidationError, match="entries must be unique"):
            TaskRoutingAssessmentCreate.model_validate(payload)


@pytest.mark.contract
def test_tag_list_and_confidence_bounds_fail_closed() -> None:
    oversized_tags = [f"tag-{index:02d}" for index in range(MAX_ROUTING_TAGS + 1)]
    with pytest.raises(ValidationError, match="at most"):
        AgentModelCatalogCreate.model_validate(
            _catalog_payload(modality_tags=oversized_tags)
        )
    for confidence in (float("nan"), float("inf"), float("-inf")):
        with pytest.raises(ValidationError):
            TaskRoutingAssessmentCreate.model_validate(
                _assessment_payload(confidence=confidence)
            )


@pytest.mark.contract
def test_difficulty_band_is_derived_without_averaging() -> None:
    routine_axes = {axis.value: 1 for axis in DifficultyAxis}
    assert derive_difficulty_band(routine_axes) == "routine"

    for axis in DifficultyAxis:
        standard_axes = dict(routine_axes)
        standard_axes[axis.value] = 2
        assert derive_difficulty_band(standard_axes) == "standard"

        advanced_axes = dict(routine_axes)
        advanced_axes[axis.value] = 3
        assert derive_difficulty_band(advanced_axes) == "advanced"

    assert derive_difficulty_band(
        routine_axes,
        ["migration"],
    ) == "advanced"
    with pytest.raises(
        ValidationError,
        match="band must match deterministic policy derivation",
    ):
        TaskRoutingAssessmentCreate.model_validate(
            _assessment_payload(
                axes=routine_axes,
                band="advanced",
            )
        )


@pytest.mark.contract
def test_high_risk_and_reason_rules_raise_review_floor() -> None:
    axes = {axis.value: 1 for axis in DifficultyAxis}
    axes["risk"] = 3
    assert minimum_review_mode(axes) == "independent"
    with pytest.raises(
        ValidationError,
        match="Advanced risk requires an independent review mode",
    ):
        TaskRoutingAssessmentCreate.model_validate(
            _assessment_payload(
                axes=axes,
                review_mode="standard",
            )
        )

    assert minimum_review_mode(
        {axis.value: 1 for axis in DifficultyAxis},
        ["specialist-verification"],
    ) == "specialist-independent"


@pytest.mark.contract
@pytest.mark.parametrize("actual", list(ContextTier))
@pytest.mark.parametrize("minimum", list(ContextTier))
def test_context_tier_ordering_matrix(
    actual: ContextTier,
    minimum: ContextTier,
) -> None:
    order = {"small": 1, "medium": 2, "large": 3}
    assert context_tier_meets(actual.value, minimum.value) is (
        order[actual.value] >= order[minimum.value]
    )


@pytest.mark.contract
def test_cost_and_latency_tier_orders_are_explicit() -> None:
    assert dict(COST_TIER_ORDER) == {
        "low": 1,
        "medium": 2,
        "high": 3,
    }
    assert dict(LATENCY_TIER_ORDER) == {
        "fast": 1,
        "balanced": 2,
        "slow": 3,
    }


@pytest.mark.contract
def test_canonical_normalization_is_byte_stable_across_boundaries() -> None:
    first_payload = _assessment_payload(
        axes={
            "reasoning": 3,
            "ambiguity": 2,
            "context_breadth": 2,
            "risk": 3,
            "verification_burden": 3,
        },
        reason_codes=["migration", "data-integrity"],
        review_mode="specialist-independent",
    )
    second_payload = deepcopy(first_payload)
    second_payload["reason_codes"] = ["data-integrity", "migration"]
    second_payload["required_skill_levels"] = {
        "data-integrity-review": 3,
        "backend-python": 4,
    }
    second_payload["required_model"]["tool_tags"] = ["shell", "code-edit"]

    first = TaskRoutingAssessmentCreate.model_validate(first_payload)
    second = TaskRoutingAssessmentCreate.model_validate(second_payload)
    assert first.canonical_json_bytes() == second.canonical_json_bytes()
    assert first.model_values() == second.model_values()

    record = TaskRoutingAssessment(
        id=1,
        created_at=datetime(2026, 7, 26, tzinfo=UTC),
        **first.model_values(),
    )
    response = TaskRoutingAssessmentResponse.from_record(
        record,
        current_task_version=first.task_version,
    )
    assert response.policy_conformant is True
    assert response.is_current is True
    assert response.required_model == first.required_model
    assert response.reason_codes == first.reason_codes
    assert response.required_skill_levels == first.required_skill_levels


@pytest.mark.contract
def test_original_v1_assessment_rows_remain_readable() -> None:
    timestamp = datetime(2026, 7, 18, tzinfo=UTC)
    legacy_record = TaskRoutingAssessment(
        id=91,
        task_id=3,
        task_version=4,
        policy_version=ROUTING_POLICY_VERSION,
        band="advanced",
        reasoning_axis=2,
        ambiguity_axis=2,
        context_breadth_axis=2,
        risk_axis=2,
        verification_burden_axis=2,
        required_skill_levels={"legacy-specialty": 3},
        required_model={
            "minimum_reasoning_tier": 2,
            "minimum_context_tier": "medium",
            "modality_tags": ["text"],
            "tool_tags": [],
            "data_policy_tags": [],
        },
        review_mode="none",
        confidence=0.75,
        reason_codes=["legacy-policy-reason"],
        rationale="Accepted by the original v1 persistence contract.",
        assessor="legacy-assessor",
        assessor_actor_id=None,
        created_at=timestamp,
    )

    response = TaskRoutingAssessmentResponse.from_record(
        legacy_record,
        current_task_version=4,
    )

    assert response.policy_conformant is False
    assert response.is_current is False
    assert response.band == "advanced"
    assert response.reason_codes == ["legacy-policy-reason"]
    assert response.required_skill_levels == {"legacy-specialty": 3}
    contradictory = response.model_dump()
    contradictory["is_current"] = True
    with pytest.raises(
        ValidationError,
        match="nonconformant routing assessment cannot be current",
    ):
        TaskRoutingAssessmentResponse.model_validate(contradictory)


@pytest.mark.contract
def test_routing_packets_share_the_agent_snapshot_byte_limit() -> None:
    assert MAX_AGENT_JSON_BYTES == MAX_ROUTING_PACKET_BYTES
    assert MAX_ROUTING_JSON_BYTES == MAX_ROUTING_PACKET_BYTES
    assert MAX_ROUTING_SNAPSHOT_BYTES == MAX_ROUTING_PACKET_BYTES
    oversized = {"evidence": "界" * MAX_ROUTING_PACKET_BYTES}
    assert len(canonical_routing_json_bytes(oversized)) > MAX_ROUTING_PACKET_BYTES
    with pytest.raises(ValueError, match=str(MAX_ROUTING_PACKET_BYTES)):
        validate_routing_packet_size(oversized)
    with pytest.raises(ValidationError, match=str(MAX_ROUTING_PACKET_BYTES)):
        AgentTaskAssignmentCreate(
            task_id=1,
            actor_id=1,
            expected_task_version=1,
            routing_snapshot=oversized,
        )


@pytest.mark.contract
@pytest.mark.parametrize(
    "snapshot",
    (
        {"nested": {"unstable"}},
        {"nested": object()},
        {"nested": (1, 2)},
        {"nested": {1: "integer-key"}},
        {"nested": float("nan")},
    ),
)
def test_routing_snapshot_rejects_non_json_native_evidence(
    snapshot: dict[object, object],
) -> None:
    with pytest.raises(ValidationError):
        AgentTaskAssignmentCreate(
            task_id=1,
            actor_id=1,
            expected_task_version=1,
            routing_snapshot=snapshot,
        )


@pytest.mark.contract
def test_at_limit_routing_snapshot_uses_the_validated_persistence_encoding() -> None:
    empty_envelope_size = len(canonical_routing_json_bytes({"evidence": ""}))
    snapshot = {
        "evidence": "x" * (MAX_ROUTING_SNAPSHOT_BYTES - empty_envelope_size)
    }
    assert len(canonical_routing_json_bytes(snapshot)) == MAX_ROUTING_SNAPSHOT_BYTES

    command = AgentTaskAssignmentCreate(
        task_id=1,
        actor_id=1,
        expected_task_version=1,
        routing_snapshot=snapshot,
    )
    persisted = AgentWorkService._serialize_routing_snapshot(
        command.routing_snapshot
    )

    assert len(persisted.encode("utf-8")) == MAX_ROUTING_SNAPSHOT_BYTES
    assert json.loads(persisted) == snapshot


@pytest.mark.contract
def test_capability_labels_only_expose_explicit_skill_choices() -> None:
    assert set(CAPABILITY_LABEL_SKILL_KEYS) == {
        "cap:code",
        "cap:test",
        "cap:docs",
        "cap:research",
    }
    assert all(
        skill_keys <= ROUTING_SKILL_KEYS
        for skill_keys in CAPABILITY_LABEL_SKILL_KEYS.values()
    )
    assert {item["skill_key"] for item in CAPABILITY_SKILLS} == ROUTING_SKILL_KEYS
    assert set(CAPABILITY_LABEL_DESCRIPTIONS) == set(
        CAPABILITY_LABEL_SKILL_KEYS
    )
    assert routing_skills_for_capability_labels(["cap:code"]) == tuple(
        sorted(CAPABILITY_LABEL_SKILL_KEYS["cap:code"])
    )
    assert routing_skills_for_capability_labels(["python"]) == ()
    assert AgentProfileCatalogService(None).capability_label_skill_map() == {
        label: sorted(skill_keys)
        for label, skill_keys in CAPABILITY_LABEL_SKILL_KEYS.items()
    }


@pytest.mark.contract
@pytest.mark.parametrize(
    ("purpose", "queue_class", "intent"),
    [
        ("execution", "normal", "execution"),
        ("execution", "rework", "rework"),
        ("execution", "recovery", "recovery"),
        ("verification", "normal", "verification"),
    ],
)
def test_assignment_intent_table_is_closed(
    purpose: str,
    queue_class: str,
    intent: str,
) -> None:
    assert assignment_intent(purpose, queue_class) == intent
    normalized = AgentTaskAssignmentCreate(
        task_id=1,
        actor_id=2,
        expected_task_version=3,
        purpose=purpose,
        queue_class=queue_class,
    )
    assert assignment_intent(
        normalized.purpose,
        normalized.queue_class,
    ) == intent


@pytest.mark.contract
@pytest.mark.parametrize("queue_class", ["rework", "recovery"])
def test_verification_rejects_execution_only_queue_classes(
    queue_class: str,
) -> None:
    blocker = (
        RoutingBlockerCode.ASSIGNMENT_PURPOSE_QUEUE_CLASS_INCOMPATIBLE.value
    )
    with pytest.raises(ValueError, match=blocker):
        assignment_intent("verification", queue_class)
    with pytest.raises(ValidationError, match=blocker):
        AgentTaskAssignmentCreate(
            task_id=1,
            actor_id=2,
            expected_task_version=3,
            purpose="verification",
            queue_class=queue_class,
        )


@pytest.mark.contract
@pytest.mark.parametrize(
    ("intent", "enabled", "role", "scopes", "expected"),
    [
        ("execution", True, "worker", {"work:execute"}, ()),
        ("rework", True, "pm", {"work:execute"}, ()),
        ("recovery", True, "worker", {"admin"}, ()),
        ("verification", True, "verifier", {"verification:write"}, ()),
        ("execution", False, "worker", {"work:execute"}, ("actor_disabled",)),
        (
            "execution",
            True,
            "verifier",
            {"work:execute"},
            ("actor_role_incompatible",),
        ),
        (
            "verification",
            True,
            "verifier",
            {"tasks:read"},
            ("actor_scope_missing",),
        ),
    ],
)
def test_actor_authorization_decision_table(
    intent: str,
    enabled: bool,
    role: str,
    scopes: set[str],
    expected: tuple[str, ...],
) -> None:
    decision = evaluate_actor_authorization(
        intent=intent,
        enabled=enabled,
        role=role,
        scopes=reversed(sorted(scopes)),
    )
    assert decision.authority_blocker_codes == expected
    assert decision.authorized is (not expected)
    assert decision.compatible is False
    assert decision.eligible is False


@pytest.mark.contract
@pytest.mark.parametrize(
    "intent",
    [
        AssignmentIntent.EXECUTION.value,
        AssignmentIntent.REWORK.value,
        AssignmentIntent.RECOVERY.value,
    ],
)
def test_execution_intents_share_capacity_profile_rules(intent: str) -> None:
    decision = evaluate_assignment_compatibility(
        intent=intent,
        actor_id=7,
        actor_profile=_profile(profile_id=11),
        capacity_owner_id=5,
        capacity_owner_profile_id=11,
    )
    assert decision.compatible is True
    assert decision.authorized is False
    assert decision.compatibility_blocker_codes == ()


@pytest.mark.contract
@pytest.mark.parametrize(
    ("profile", "owner_id", "owner_profile_id", "expected"),
    [
        (None, 5, 11, "actor_profile_missing"),
        (_profile(profile_kind="human"), 5, 10, "profile_kind_human"),
        (
            _profile(profile_kind="hybrid", automation_enabled=False),
            5,
            10,
            "profile_automation_disabled",
        ),
        (
            _profile(profile_kind="hybrid", assignment_modes=frozenset()),
            5,
            10,
            "profile_assignment_mode_missing",
        ),
        (_profile(), None, None, "capacity_owner_missing"),
        (_profile(), 5, None, "capacity_owner_profile_missing"),
        (_profile(profile_id=10), 5, 12, "actor_capacity_profile_mismatch"),
    ],
)
def test_profile_and_capacity_compatibility_blockers(
    profile: RoutingProfileEvidence | None,
    owner_id: int | None,
    owner_profile_id: int | None,
    expected: str,
) -> None:
    decision = evaluate_assignment_compatibility(
        intent="execution",
        actor_id=7,
        actor_profile=profile,
        capacity_owner_id=owner_id,
        capacity_owner_profile_id=owner_profile_id,
    )
    assert expected in decision.compatibility_blocker_codes
    assert decision.compatible is False


@pytest.mark.contract
def test_hybrid_profile_requires_explicit_automation_and_mode() -> None:
    decision = evaluate_assignment_compatibility(
        intent="execution",
        actor_id=7,
        actor_profile=_profile(
            profile_kind="hybrid",
            automation_enabled=True,
            assignment_modes=frozenset({"execution"}),
        ),
        capacity_owner_id=5,
        capacity_owner_profile_id=10,
    )
    assert decision.compatible is True


@pytest.mark.contract
def test_verifier_must_be_actor_and_profile_independent() -> None:
    same_actor_and_profile = evaluate_assignment_compatibility(
        intent="verification",
        actor_id=7,
        actor_profile=_profile(
            profile_id=20,
            assignment_modes=frozenset({"verification"}),
        ),
        reviewer_profile_id=20,
        execution_actor_ids=[7],
        execution_profile_ids=[20],
        review_mode="independent",
    )
    assert same_actor_and_profile.compatibility_blocker_codes == (
        "verification_actor_not_independent",
        "verification_profile_not_independent",
    )

    unverifiable = evaluate_assignment_compatibility(
        intent="verification",
        actor_id=8,
        actor_profile=_profile(
            profile_id=21,
            assignment_modes=frozenset({"verification"}),
        ),
        reviewer_profile_id=21,
        execution_actor_ids=[7],
        execution_profile_ids=[None],
        review_mode="independent",
    )
    assert unverifiable.compatibility_blocker_codes == (
        "verification_independence_unverifiable",
    )


@pytest.mark.contract
@pytest.mark.parametrize(
    ("execution_actor_ids", "execution_profile_ids"),
    [
        ([7, 8], [20]),
        ([7], [20, 21]),
        ([7, None], [20, 21]),
        ([7, 8], [20, None]),
    ],
)
def test_verifier_independence_requires_complete_paired_execution_evidence(
    execution_actor_ids: list[int | None],
    execution_profile_ids: list[int | None],
) -> None:
    decision = evaluate_assignment_compatibility(
        intent="verification",
        actor_id=9,
        actor_profile=_profile(
            profile_id=22,
            assignment_modes=frozenset({"verification"}),
        ),
        reviewer_profile_id=22,
        execution_actor_ids=execution_actor_ids,
        execution_profile_ids=execution_profile_ids,
        review_mode="independent",
    )
    assert decision.compatibility_blocker_codes == (
        "verification_independence_unverifiable",
    )
    assert decision.compatible is False


@pytest.mark.contract
def test_verifier_independence_accepts_complete_multi_execution_evidence() -> None:
    decision = evaluate_assignment_compatibility(
        intent="verification",
        actor_id=9,
        actor_profile=_profile(
            profile_id=22,
            assignment_modes=frozenset({"verification"}),
        ),
        reviewer_profile_id=22,
        execution_actor_ids=[7, 8],
        execution_profile_ids=[20, 21],
        review_mode="independent",
    )
    assert decision.compatibility_blocker_codes == ()
    assert decision.compatible is True


@pytest.mark.contract
def test_specialist_verification_requires_nonweak_skill_level() -> None:
    eligible = evaluate_assignment_compatibility(
        intent="verification",
        actor_id=8,
        actor_profile=_profile(
            profile_id=21,
            assignment_modes=frozenset({"verification"}),
            skill_levels={"data-integrity-review": 4},
        ),
        reviewer_profile_id=21,
        execution_actor_ids=[7],
        execution_profile_ids=[20],
        review_mode="specialist-independent",
        required_specialist_skill_levels={"data-integrity-review": 3},
    )
    assert eligible.compatible is True

    under_level = evaluate_assignment_compatibility(
        intent="verification",
        actor_id=8,
        actor_profile=_profile(
            profile_id=21,
            assignment_modes=frozenset({"verification"}),
            skill_levels={"data-integrity-review": 2},
        ),
        reviewer_profile_id=21,
        execution_actor_ids=[7],
        execution_profile_ids=[20],
        review_mode="specialist-independent",
        required_specialist_skill_levels={"data-integrity-review": 3},
    )
    assert under_level.compatibility_blocker_codes == (
        "verification_specialist_skill_missing",
    )
    assert under_level.missing_specialist_skills == (
        "data-integrity-review",
    )

    weakness = evaluate_assignment_compatibility(
        intent="verification",
        actor_id=8,
        actor_profile=_profile(
            profile_id=21,
            assignment_modes=frozenset({"verification"}),
            skill_levels={"data-integrity-review": 5},
            weakness_keys=frozenset({"data-integrity-review"}),
        ),
        reviewer_profile_id=21,
        execution_actor_ids=[7],
        execution_profile_ids=[20],
        review_mode="specialist-independent",
        required_specialist_skill_levels={"data-integrity-review": 3},
    )
    assert weakness.compatibility_blocker_codes == (
        "verification_specialist_skill_missing",
    )


@pytest.mark.contract
def test_compatibility_evidence_cannot_bypass_authorization() -> None:
    authorization = evaluate_actor_authorization(
        intent="execution",
        enabled=True,
        role="worker",
        scopes=[],
    )
    compatibility = evaluate_assignment_compatibility(
        intent="execution",
        actor_id=7,
        actor_profile=_profile(profile_id=11),
        capacity_owner_id=5,
        capacity_owner_profile_id=11,
    )
    combined = authorization.merged_with(compatibility)
    assert compatibility.compatible is True
    assert combined.authorized is False
    assert combined.compatible is True
    assert combined.eligible is False
    assert combined.hard_blocker_codes == ("actor_scope_missing",)


@pytest.mark.contract
def test_assignment_service_consumes_the_separate_authority_contract() -> None:
    authorized = AgentActor(
        name="authorized-worker",
        display_name="Authorized Worker",
        api_key_hash="authorized-worker-hash",
        enabled=True,
        role="worker",
        scopes='["work:execute"]',
    )
    AgentWorkService._validate_assignment_actor(authorized, "execution")

    unauthorized = AgentActor(
        name="unauthorized-worker",
        display_name="Unauthorized Worker",
        api_key_hash="unauthorized-worker-hash",
        enabled=True,
        role="worker",
        scopes="[]",
    )
    with pytest.raises(ValueError, match="actor_scope_missing"):
        AgentWorkService._validate_assignment_actor(
            unauthorized,
            "execution",
        )
    with pytest.raises(ValueError, match="Unknown assignment intent"):
        AgentWorkService._validate_assignment_actor(
            authorized,
            "unsupported",
        )


@pytest.mark.contract
def test_contract_collections_are_closed_and_duplicate_free() -> None:
    assert ASSESSMENT_REASON_CODES == {
        reason.value for reason in AssessmentReasonCode
    }
    assert len(ROUTING_SKILL_KEYS) == len(CAPABILITY_SKILLS)
    assert len({blocker.value for blocker in RoutingBlockerCode}) == len(
        RoutingBlockerCode
    )
