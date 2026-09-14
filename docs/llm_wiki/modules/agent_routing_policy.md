# agent_routing_policy Module

**Path:** `backend/app/services/agent_routing_policy.py`

## Description

Pure, provider-neutral policy for model-aware agent routing.

The module freezes the vocabulary and decision rules shared by persistence,
REST, MCP, and future candidate ranking.  It does not grant actor authority,
infer precise skills from prose, or select a provider/model by name.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `dataclasses` | `dataclass`, `field` |
| `enum` | `IntEnum`, `StrEnum` |
| `json` | `json` |
| `math` | `math` |
| `types` | `MappingProxyType` |
| `typing` | `Any`, `Iterable`, `Mapping` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/agent_routing_policy.py"]
    n0 --> n1
    click n1 "../modules/agent_routing_policy.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (15) |

> All 15 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ReasoningTier](../entities/ReasoningTier.md) | Enum | 101 | `IntEnum` | Closed provider-neutral reasoning capability tiers. |
| [ContextTier](../entities/ContextTier.md) | Enum | 109 | `StrEnum` | Closed context-capacity tiers ordered by increasing capacity. |
| [CostTier](../entities/CostTier.md) | Enum | 117 | `StrEnum` | Closed relative cost tiers; exact prices are deliberately excluded. |
| [LatencyTier](../entities/LatencyTier.md) | Enum | 125 | `StrEnum` | Closed relative latency tiers. |
| [DifficultyAxis](../entities/DifficultyAxis.md) | Enum | 133 | `StrEnum` | The five governed task-difficulty axes. |
| [DifficultyBand](../entities/DifficultyBand.md) | Enum | 143 | `StrEnum` | Derived task-difficulty bands. |
| [ReviewMode](../entities/ReviewMode.md) | Enum | 151 | `StrEnum` | Closed review modes ordered by increasing independence requirements. |
| [AssessmentReasonCode](../entities/agent_routing_policy_AssessmentReasonCode.md) | Enum | 160 | `StrEnum` | Governed reasons that may raise the derived band or review floor. |
| [AssignmentIntent](../entities/AssignmentIntent.md) | Enum | 177 | `StrEnum` | Normalized assignment intents derived from purpose and queue class. |
| [RoutingBlockerCode](../entities/agent_routing_policy_RoutingBlockerCode.md) | Enum | 186 | `StrEnum` | Stable hard blockers shared by preview and assignment enforcement. |
| [ReasonCodeRule](../entities/ReasonCodeRule.md) | Class | 455 | — | Minimum band/review requirements attached to one governed reason. |
| [RoutingProfileEvidence](../entities/RoutingProfileEvidence.md) | Class | 528 | — | Secret-free profile evidence used by compatibility decisions. |
| [RoutingEligibilityDecision](../entities/RoutingEligibilityDecision.md) | Class | 540 | — | Separated authority/compatibility evidence for one candidate. |
| [RoutingSkillDecision](../entities/RoutingSkillDecision.md) | Class | 613 | — | Deterministic required-skill evidence for one profile. |
| [RoutingModelEnvelopeDecision](../entities/RoutingModelEnvelopeDecision.md) | Class | 628 | — | Deterministic binding/catalog capability evidence for one candidate. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `normalize_model_failure_category` | `(value: Any) -> str` | — | Project untrusted failure evidence into the closed escalation taxonomy. |
| `_axis_values` | `(axes: Mapping[str, Any] \| Any) -> dict[str, int]` | — | — |
| `_reason_values` | `(reason_codes: Iterable[str]) -> tuple[str, ...]` | — | — |
| `derive_difficulty_band` | `(axes: Mapping[str, Any] \| Any, reason_codes: Iterable[str] = ()) -> str` | — | Derive the only valid band without averaging decisive axes. |
| `minimum_review_mode` | `(axes: Mapping[str, Any] \| Any, reason_codes: Iterable[str] = ()) -> str` | — | Return the minimum review mode required by axes and governed reasons. |
| `review_mode_meets` | `(actual: str, minimum: str) -> bool` | — | Return whether one closed review mode meets the required floor. |
| `assessment_confidence_meets_minimum` | `(confidence: float) -> bool` | — | Return whether an authoritative assessment meets the frozen v1 floor. |
| `context_tier_meets` | `(actual: str, minimum: str) -> bool` | — | Return whether an actual context tier meets a required tier. |
| `routing_skills_for_capability_labels` | `(labels: Iterable[str]) -> tuple[str, ...]` | — | Return explicit skill choices for known coarse readiness labels. |
| `_normalized_skill_levels` | `(levels: Mapping[str, int], *, label: str, governed_keys_only: bool) -> dict[str, int]` | — | — |
| `evaluate_required_skills` | `(*, required_skill_levels: Mapping[str, int], actual_skill_levels: Mapping[str, int], weakness_keys: Iterable[str] = ()) -> RoutingSkillDecision` | — | Evaluate precise governed skill requirements without prose inference. |
| `_envelope_value` | `(envelope: Mapping[str, Any] \| Any, key: str) -> Any` | — | — |
| `_normalized_tag_set` | `(values: Iterable[str], *, label: str) -> frozenset[str]` | — | — |
| `model_adequacy_class` | `(*, minimum_reasoning_tier: int, actual_reasoning_tier: int, minimum_context_tier: str, actual_context_tier: str) -> int` | — | Return deterministic excess capability steps for an adequate model. |
| `evaluate_model_envelope` | `(required_model: Mapping[str, Any] \| Any, *, binding_present: bool = True, binding_enabled: bool = True, binding_revision_current: bool = True, catalog_present: bool = True, catalog_enabled: bool = True, actual_reasoning_tier: int \| None, actual_context_tier: str \| None, actual_modality_tags: Iterable[str] = (), actual_tool_tags: Iterable[str] = (), actual_data_policy_tags: Iterable[str] = ()) -> RoutingModelEnvelopeDecision` | — | Evaluate one binding/catalog pair against a required model envelope. |
| `routing_candidate_rank_key` | `(*, adequacy_class: int, cost_tier: str, queue_depth: int, schedule_delay_days: float, latency_tier: str, actor_id: int, binding_id: int) -> tuple[int, int, int, float, int, int, int]` | — | Freeze v1 ranking after all hard eligibility gates have passed. |
| `_validate_json_native` | `(value: Any, *, ancestors: set[int] \| None = None, depth: int = 0) -> None` | — | Reject values whose JSON representation would be lossy or unstable. |
| `canonical_routing_json_bytes` | `(value: Any) -> bytes` | — | Serialize JSON-native normalized routing evidence as stable UTF-8. |
| `validate_routing_packet_size` | `(value: Any, *, label: str = 'Routing packet', maximum_bytes: int = MAX_ROUTING_PACKET_BYTES) -> Any` | — | Reject a canonical routing packet that exceeds its storage boundary. |
| `assignment_intent` | `(purpose: str, queue_class: str) -> str` | — | Normalize a valid assignment purpose/queue tuple to one intent. |
| `evaluate_actor_authorization` | `(*, intent: str, enabled: bool, role: str, scopes: Iterable[str]) -> RoutingEligibilityDecision` | — | Evaluate authority only; capability evidence cannot clear these blockers. |
| `evaluate_assignment_compatibility` | `(*, intent: str, actor_id: int, actor_profile: RoutingProfileEvidence \| None, capacity_owner_id: int \| None = None, capacity_owner_profile_id: int \| None = None, reviewer_profile_id: int \| None = None, execution_actor_ids: Iterable[int \| None] = (), execution_profile_ids: Iterable[int \| None] = (), review_mode: str = ReviewMode.NONE.value, required_specialist_skill_levels: Mapping[str, int] \| None = None) -> RoutingEligibilityDecision` | — | Evaluate unattended profile/capacity/verifier compatibility. |
