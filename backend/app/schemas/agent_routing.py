"""Provider-neutral model-routing boundary contracts.

These schemas deliberately contain no credentials, provider endpoints, prompts,
or runtime logs. They normalize the same bounded vocabulary for persistence,
REST, MCP, and deterministic policy tests.
"""

from __future__ import annotations

from collections.abc import Mapping
import math
import re
from datetime import datetime
from typing import Annotated, Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    ValidationError,
    field_validator,
    model_validator,
)

from app.services.agent_routing_policy import (
    ASSESSMENT_REASON_CODES,
    MAX_ROUTING_CANDIDATES,
    MAX_ROUTING_EXCLUSIONS,
    MAX_ROUTING_PACKET_BYTES,
    MIN_ROUTING_ASSESSMENT_CONFIDENCE,
    ROUTING_PREVIEW_TTL_SECONDS,
    AssessmentReasonCode,
    ContextTier,
    CostTier,
    DifficultyBand,
    LatencyTier,
    ROUTING_POLICY_VERSION,
    ROUTING_SKILL_KEYS,
    ReasoningTier,
    ReviewMode,
    RoutingBlockerCode,
    assessment_confidence_meets_minimum,
    canonical_routing_json_bytes,
    derive_difficulty_band,
    minimum_review_mode,
    review_mode_meets,
    validate_routing_packet_size,
)

MAX_ROUTING_TAGS = 32
MAX_REQUIRED_SKILLS = 50
MAX_REASON_CODES = len(ASSESSMENT_REASON_CODES)
MAX_ROUTING_TEXT_LENGTH = 8_000
MAX_ROUTING_JSON_BYTES = MAX_ROUTING_PACKET_BYTES
MAX_ROUTING_ASSESSMENT_HISTORY = 100

RoutingKey = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        to_lower=True,
        min_length=1,
        max_length=120,
        pattern=r"^[a-z0-9](?:[a-z0-9._-]*[a-z0-9])?$",
    ),
]
DifficultyScore = Annotated[int, Field(strict=True, ge=1, le=3)]
SkillLevel = Annotated[int, Field(strict=True, ge=1, le=5)]
PositiveRevision = Annotated[int, Field(strict=True, ge=1)]
RoutingDigest = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        to_lower=True,
        min_length=64,
        max_length=64,
        pattern=r"^[0-9a-f]{64}$",
    ),
]
ModelContextTier = ContextTier
ModelCostTier = CostTier
ModelLatencyTier = LatencyTier
TaskDifficultyBand = DifficultyBand
TaskReviewMode = ReviewMode


def _normalize_tags(values: list[Any], *, label: str) -> list[str]:
    if len(values) > MAX_ROUTING_TAGS:
        raise ValueError(f"{label} may contain at most {MAX_ROUTING_TAGS} entries")
    normalized: list[str] = []
    for value in values:
        if not isinstance(value, str):
            raise ValueError(f"{label} entries must be strings")
        tag = value.strip().lower()
        if not re.fullmatch(r"[a-z0-9](?:[a-z0-9._-]{0,118}[a-z0-9])?", tag):
            raise ValueError(f"{label} entries must be stable lowercase keys")
        normalized.append(tag)
    if len(normalized) != len(set(normalized)):
        raise ValueError(f"{label} entries must be unique")
    return sorted(normalized)


def _normalize_routing_keys(
    values: list[Any],
    *,
    label: str,
    maximum_entries: int = MAX_REQUIRED_SKILLS,
) -> list[str]:
    if len(values) > maximum_entries:
        raise ValueError(f"{label} may contain at most {maximum_entries} entries")
    normalized: list[str] = []
    for value in values:
        if not isinstance(value, str):
            raise ValueError(f"{label} entries must be strings")
        key = value.strip().lower()
        if not re.fullmatch(r"[a-z0-9](?:[a-z0-9._-]{0,118}[a-z0-9])?", key):
            raise ValueError(f"{label} entries must be stable lowercase keys")
        normalized.append(key)
    if len(normalized) != len(set(normalized)):
        raise ValueError(f"{label} entries must be unique")
    return sorted(normalized)


def _normalize_required_skill_levels(value: Any) -> Any:
    if not isinstance(value, Mapping):
        return value
    skill_levels = dict(value)
    if len(skill_levels) > MAX_REQUIRED_SKILLS:
        raise ValueError(
            f"required_skill_levels may contain at most {MAX_REQUIRED_SKILLS} entries"
        )
    normalized: dict[str, int] = {}
    for raw_key, level in skill_levels.items():
        if not isinstance(raw_key, str):
            raise ValueError("Required skill keys must be strings")
        key = raw_key.strip().lower()
        if not re.fullmatch(r"[a-z0-9](?:[a-z0-9._-]{0,118}[a-z0-9])?", key):
            raise ValueError("Required skill keys must be stable lowercase keys")
        if key in normalized:
            raise ValueError("Required skill keys must be unique after normalization")
        if key not in ROUTING_SKILL_KEYS:
            raise ValueError(f"Unknown routing skill key: {key}")
        if (
            isinstance(level, bool)
            or not isinstance(level, int)
            or not 1 <= level <= 5
        ):
            raise ValueError("Required skill levels must be between 1 and 5")
        normalized[key] = level
    return dict(sorted(normalized.items()))


def _normalize_assessment_reason_codes(value: Any) -> Any:
    if not isinstance(value, list):
        raise ValueError("reason_codes must be a JSON list")
    if len(value) > MAX_REASON_CODES:
        raise ValueError(
            f"reason_codes may contain at most {MAX_REASON_CODES} entries"
        )
    normalized = _normalize_tags(value, label="reason_codes")
    unknown = set(normalized).difference(ASSESSMENT_REASON_CODES)
    if unknown:
        raise ValueError(
            "Unknown assessment reason codes: " + ", ".join(sorted(unknown))
        )
    return normalized


def _strip_nonempty_assessment_text(value: str) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValueError("Assessment text fields must not be blank")
    return normalized


def _validate_assessment_band_and_review(value: Any) -> None:
    derived_band = derive_difficulty_band(value.axes, value.reason_codes)
    if value.band == "routine" and derived_band != "routine":
        raise ValueError(
            "routine requires every governed axis to be 1 and no "
            "escalating reason code"
        )
    if value.band == "standard" and derived_band == "advanced":
        raise ValueError(
            "standard cannot contain an advanced axis or escalating reason code"
        )
    if value.band != derived_band:
        raise ValueError(
            f"band must match deterministic policy derivation: {derived_band}"
        )
    required_review = minimum_review_mode(value.axes, value.reason_codes)
    if value.axes.risk == 3 and not review_mode_meets(
        value.review_mode,
        "independent",
    ):
        raise ValueError("Advanced risk requires an independent review mode")
    if not review_mode_meets(value.review_mode, required_review):
        raise ValueError(
            f"review_mode must meet the policy minimum: {required_review}"
        )


class RoutingContractModel(BaseModel):
    """Strict deterministic base for data crossing a routing boundary."""

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        allow_inf_nan=False,
        use_enum_values=True,
    )

    @model_validator(mode="after")
    def validate_encoded_packet_size(self) -> "RoutingContractModel":
        validate_routing_packet_size(
            self,
            label=self.__class__.__name__,
        )
        return self

    def canonical_json_bytes(self) -> bytes:
        """Return byte-stable normalized JSON for digests and parity checks."""

        return canonical_routing_json_bytes(self)


class AgentModelCatalogFields(RoutingContractModel):
    """Secret-free provider-neutral model catalog fields."""

    key: RoutingKey
    provider: str = Field(..., min_length=1, max_length=120)
    configured_model_alias: str = Field(..., min_length=1, max_length=255)
    reasoning_tier: ReasoningTier
    context_tier: ModelContextTier
    modality_tags: list[str] = Field(default_factory=lambda: ["text"])
    cost_tier: ModelCostTier
    latency_tier: ModelLatencyTier
    enabled: bool = True
    revision: PositiveRevision = 1
    last_verified_at: datetime | None = None

    @field_validator("key", mode="before")
    @classmethod
    def normalize_catalog_key(cls, value: Any) -> Any:
        return value.strip().lower() if isinstance(value, str) else value

    @field_validator("reasoning_tier", mode="before")
    @classmethod
    def require_integer_reasoning_tier(cls, value: Any) -> Any:
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("reasoning_tier must be an integer")
        return value

    @field_validator("provider", "configured_model_alias")
    @classmethod
    def strip_nonempty_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Catalog text fields must not be blank")
        return normalized

    @field_validator("modality_tags")
    @classmethod
    def validate_modality_tags(cls, value: list[str]) -> list[str]:
        normalized = _normalize_tags(value, label="modality_tags")
        if not normalized:
            raise ValueError("modality_tags must contain at least one entry")
        return normalized


class AgentModelCatalogCreate(AgentModelCatalogFields):
    """Create payload for a catalog entry."""

    revision: Literal[1] = 1


class AgentModelCatalogUpdate(RoutingContractModel):
    """Optimistic partial update for one catalog entry."""

    expected_revision: PositiveRevision
    provider: str | None = Field(default=None, min_length=1, max_length=120)
    configured_model_alias: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    reasoning_tier: ReasoningTier | None = None
    context_tier: ModelContextTier | None = None
    modality_tags: list[str] | None = None
    cost_tier: ModelCostTier | None = None
    latency_tier: ModelLatencyTier | None = None
    enabled: Literal[True] | None = None
    last_verified_at: datetime | None = None
    reconcile_live_assignments: bool = False

    @field_validator("reasoning_tier", mode="before")
    @classmethod
    def require_integer_reasoning_tier(cls, value: Any) -> Any:
        if value is not None and (
            isinstance(value, bool) or not isinstance(value, int)
        ):
            raise ValueError("reasoning_tier must be an integer")
        return value

    @field_validator("provider", "configured_model_alias")
    @classmethod
    def strip_optional_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        if not normalized:
            raise ValueError("Catalog text fields must not be blank")
        return normalized

    @field_validator("modality_tags")
    @classmethod
    def validate_modality_tags(
        cls,
        value: list[str] | None,
    ) -> list[str] | None:
        if value is None:
            return None
        normalized = _normalize_tags(value, label="modality_tags")
        if not normalized:
            raise ValueError("modality_tags must contain at least one entry")
        return normalized

    @model_validator(mode="after")
    def require_catalog_change(self) -> "AgentModelCatalogUpdate":
        non_nullable = {
            "provider",
            "configured_model_alias",
            "reasoning_tier",
            "context_tier",
            "modality_tags",
            "cost_tier",
            "latency_tier",
            "enabled",
        }
        invalid = sorted(
            field_name
            for field_name in self.model_fields_set.intersection(non_nullable)
            if getattr(self, field_name) is None
        )
        if invalid:
            raise ValueError(
                "Catalog fields cannot be null: " + ", ".join(invalid)
            )
        mutable_fields = self.model_fields_set.difference(
            {"expected_revision", "reconcile_live_assignments"}
        )
        if not mutable_fields:
            raise ValueError("At least one catalog field must be updated")
        return self


class AgentModelCatalogDisable(RoutingContractModel):
    """Optimistic soft-disable command for a catalog entry."""

    expected_revision: PositiveRevision
    reconcile_live_assignments: bool = False


class AgentModelCatalogResponse(AgentModelCatalogFields):
    """Persisted catalog projection."""

    id: int
    created_at: datetime
    updated_at: datetime


class AgentModelBindingFields(RoutingContractModel):
    """Versioned runtime binding owned by one exact actor."""

    actor_id: int = Field(..., ge=1)
    model_catalog_id: int = Field(..., ge=1)
    is_default: bool = False
    enabled: bool = True
    tool_tags: list[str] = Field(default_factory=list)
    data_policy_tags: list[str] = Field(default_factory=list)
    revision: PositiveRevision = 1

    @field_validator("tool_tags")
    @classmethod
    def validate_tool_tags(cls, value: list[str]) -> list[str]:
        return _normalize_tags(value, label="tool_tags")

    @field_validator("data_policy_tags")
    @classmethod
    def validate_data_policy_tags(cls, value: list[str]) -> list[str]:
        return _normalize_tags(value, label="data_policy_tags")

    @model_validator(mode="after")
    def require_enabled_default(self) -> "AgentModelBindingFields":
        if self.is_default and not self.enabled:
            raise ValueError("A default model binding must be enabled")
        return self


class AgentModelBindingCreate(AgentModelBindingFields):
    """Create payload for an actor-model binding."""

    revision: Literal[1] = 1


class AgentModelBindingUpdate(RoutingContractModel):
    """Optimistic partial update for one actor-model binding."""

    expected_revision: PositiveRevision
    is_default: bool | None = None
    enabled: Literal[True] | None = None
    tool_tags: list[str] | None = None
    data_policy_tags: list[str] | None = None
    reconcile_live_assignments: bool = False

    @field_validator("tool_tags")
    @classmethod
    def validate_tool_tags(
        cls,
        value: list[str] | None,
    ) -> list[str] | None:
        return (
            _normalize_tags(value, label="tool_tags")
            if value is not None
            else None
        )

    @field_validator("data_policy_tags")
    @classmethod
    def validate_data_policy_tags(
        cls,
        value: list[str] | None,
    ) -> list[str] | None:
        return (
            _normalize_tags(value, label="data_policy_tags")
            if value is not None
            else None
        )

    @model_validator(mode="after")
    def require_binding_change(self) -> "AgentModelBindingUpdate":
        non_nullable = {
            "is_default",
            "enabled",
            "tool_tags",
            "data_policy_tags",
        }
        invalid = sorted(
            field_name
            for field_name in self.model_fields_set.intersection(non_nullable)
            if getattr(self, field_name) is None
        )
        if invalid:
            raise ValueError(
                "Binding fields cannot be null: " + ", ".join(invalid)
            )
        mutable_fields = self.model_fields_set.difference(
            {"expected_revision", "reconcile_live_assignments"}
        )
        if not mutable_fields:
            raise ValueError("At least one binding field must be updated")
        return self


class AgentModelBindingDisable(RoutingContractModel):
    """Optimistic soft-disable command for an actor-model binding."""

    expected_revision: PositiveRevision
    reconcile_live_assignments: bool = False


class AgentModelBindingResponse(AgentModelBindingFields):
    """Persisted binding projection."""

    id: int
    model_catalog_key: str | None = None
    selectable: bool = False
    model_catalog: AgentModelCatalogResponse | None = None
    live_assignment_count: int = 0
    historical_assignment_count: int = 0
    run_reference_count: int = 0
    created_at: datetime
    updated_at: datetime


class AgentModelMutationReceipt(RoutingContractModel):
    """Durable, replay-safe receipt for an operator model mutation."""

    operation: str = Field(..., min_length=1, max_length=100)
    actor_id: int = Field(..., ge=1)
    target_type: Literal["model_catalog", "model_binding"]
    target_id: int = Field(..., ge=1)
    idempotency_key: str = Field(..., min_length=1, max_length=255)
    rationale: str = Field(..., min_length=1, max_length=2_000)
    correlation_id: str = Field(..., min_length=1, max_length=255)
    authoritative_revision: PositiveRevision
    invalidated_assignment_ids: list[int] = Field(default_factory=list)
    audit_event_ids: list[int] = Field(default_factory=list)
    result: dict[str, Any]


class TaskDifficultyAxes(RoutingContractModel):
    """Five governed task-difficulty axes on a closed 1..3 scale."""

    reasoning: DifficultyScore
    ambiguity: DifficultyScore
    context_breadth: DifficultyScore
    risk: DifficultyScore
    verification_burden: DifficultyScore

    def values(self) -> tuple[int, ...]:
        return (
            self.reasoning,
            self.ambiguity,
            self.context_breadth,
            self.risk,
            self.verification_burden,
        )


class RequiredModelEnvelope(RoutingContractModel):
    """Minimum provider-neutral runtime capabilities required by a task."""

    minimum_reasoning_tier: ReasoningTier
    minimum_context_tier: ModelContextTier
    modality_tags: list[str] = Field(default_factory=lambda: ["text"])
    tool_tags: list[str] = Field(default_factory=list)
    data_policy_tags: list[str] = Field(default_factory=list)

    @field_validator("minimum_reasoning_tier", mode="before")
    @classmethod
    def require_integer_reasoning_tier(cls, value: Any) -> Any:
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("minimum_reasoning_tier must be an integer")
        return value

    @field_validator("modality_tags", "tool_tags", "data_policy_tags")
    @classmethod
    def validate_tags(cls, value: list[str], info: Any) -> list[str]:
        normalized = _normalize_tags(value, label=info.field_name)
        if info.field_name == "modality_tags" and not normalized:
            raise ValueError("modality_tags must contain at least one entry")
        return normalized


class TaskRoutingAssessmentFields(RoutingContractModel):
    """Immutable assessment bound to one concrete task version."""

    task_id: int = Field(..., ge=1)
    task_version: int = Field(..., ge=1)
    policy_version: Literal["model-aware-routing-v1"] = ROUTING_POLICY_VERSION
    band: TaskDifficultyBand
    axes: TaskDifficultyAxes
    required_skill_levels: dict[str, SkillLevel] = Field(default_factory=dict)
    required_model: RequiredModelEnvelope
    review_mode: TaskReviewMode
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason_codes: list[AssessmentReasonCode] = Field(default_factory=list)
    rationale: str = Field(..., min_length=1, max_length=MAX_ROUTING_TEXT_LENGTH)
    assessor: str = Field(..., min_length=1, max_length=255)
    assessor_actor_id: int | None = Field(default=None, ge=1)

    @field_validator("required_skill_levels", mode="before")
    @classmethod
    def validate_required_skills(cls, value: Any) -> Any:
        return _normalize_required_skill_levels(value)

    @field_validator("reason_codes", mode="before")
    @classmethod
    def validate_reason_codes(cls, value: Any) -> Any:
        return _normalize_assessment_reason_codes(value)

    @field_validator("rationale", "assessor")
    @classmethod
    def strip_assessment_text(cls, value: str) -> str:
        return _strip_nonempty_assessment_text(value)

    @field_validator("confidence")
    @classmethod
    def reject_nonfinite_confidence(cls, value: float) -> float:
        if not math.isfinite(value):
            raise ValueError("confidence must be finite")
        return value

    @model_validator(mode="after")
    def validate_band_and_review_override(self) -> "TaskRoutingAssessmentFields":
        _validate_assessment_band_and_review(self)
        return self

    def model_values(self) -> dict[str, Any]:
        """Return deterministic ORM constructor values without hiding axes."""

        values = self.model_dump(exclude={"axes"})
        values.update(
            reasoning_axis=self.axes.reasoning,
            ambiguity_axis=self.axes.ambiguity,
            context_breadth_axis=self.axes.context_breadth,
            risk_axis=self.axes.risk,
            verification_burden_axis=self.axes.verification_burden,
        )
        values["required_model"] = self.required_model.model_dump()
        return values


class TaskRoutingAssessmentCreate(TaskRoutingAssessmentFields):
    """Create payload for one append-only assessment."""


class TaskRoutingAssessmentCommand(RoutingContractModel):
    """Authorized client input; identity and policy fields are server-owned."""

    expected_task_version: int = Field(..., strict=True, ge=1)
    band: TaskDifficultyBand
    axes: TaskDifficultyAxes
    required_skill_levels: dict[str, SkillLevel] = Field(default_factory=dict)
    required_model: RequiredModelEnvelope
    review_mode: TaskReviewMode
    confidence: float = Field(
        ...,
        ge=MIN_ROUTING_ASSESSMENT_CONFIDENCE,
        le=1.0,
    )
    reason_codes: list[AssessmentReasonCode] = Field(default_factory=list)
    rationale: str = Field(..., min_length=1, max_length=MAX_ROUTING_TEXT_LENGTH)

    @field_validator("required_skill_levels", mode="before")
    @classmethod
    def validate_required_skills(cls, value: Any) -> Any:
        return _normalize_required_skill_levels(value)

    @field_validator("reason_codes", mode="before")
    @classmethod
    def validate_reason_codes(cls, value: Any) -> Any:
        return _normalize_assessment_reason_codes(value)

    @field_validator("rationale")
    @classmethod
    def strip_rationale(cls, value: str) -> str:
        return _strip_nonempty_assessment_text(value)

    @field_validator("confidence")
    @classmethod
    def require_authoritative_confidence(cls, value: float) -> float:
        if not assessment_confidence_meets_minimum(value):
            raise ValueError(
                "confidence must meet the routing assessment minimum "
                f"of {MIN_ROUTING_ASSESSMENT_CONFIDENCE:.2f}"
            )
        return value

    @model_validator(mode="after")
    def validate_band_and_review_override(self) -> "TaskRoutingAssessmentCommand":
        _validate_assessment_band_and_review(self)
        return self


class PersistedTaskRoutingAssessmentFields(BaseModel):
    """Backward-compatible decoder for rows written under the original v1 schema.

    New writes use ``TaskRoutingAssessmentCreate`` and its stricter deterministic
    policy. Existing append-only v1 rows retain the validation rules that were
    active when they were accepted, so reading them cannot retroactively fail.
    """

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        allow_inf_nan=False,
        use_enum_values=True,
    )

    task_id: int = Field(..., ge=1)
    task_version: int = Field(..., ge=1)
    policy_version: Literal["model-aware-routing-v1"] = ROUTING_POLICY_VERSION
    band: TaskDifficultyBand
    axes: TaskDifficultyAxes
    required_skill_levels: dict[str, int] = Field(default_factory=dict)
    required_model: RequiredModelEnvelope
    review_mode: TaskReviewMode
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason_codes: list[str] = Field(default_factory=list)
    rationale: str = Field(..., min_length=1, max_length=MAX_ROUTING_TEXT_LENGTH)
    assessor: str = Field(..., min_length=1, max_length=255)
    assessor_actor_id: int | None = Field(default=None, ge=1)

    @field_validator("required_skill_levels")
    @classmethod
    def validate_stored_required_skills(
        cls,
        value: dict[str, int],
    ) -> dict[str, int]:
        if len(value) > MAX_REQUIRED_SKILLS:
            raise ValueError(
                f"required_skill_levels may contain at most {MAX_REQUIRED_SKILLS} entries"
            )
        normalized: dict[str, int] = {}
        for raw_key, level in value.items():
            key = raw_key.strip().lower()
            if not re.fullmatch(
                r"[a-z0-9](?:[a-z0-9._-]{0,118}[a-z0-9])?",
                key,
            ):
                raise ValueError("Required skill keys must be stable lowercase keys")
            if key in normalized:
                raise ValueError(
                    "Required skill keys must be unique after normalization"
                )
            if not 1 <= level <= 5:
                raise ValueError("Required skill levels must be between 1 and 5")
            normalized[key] = level
        return dict(sorted(normalized.items()))

    @field_validator("reason_codes")
    @classmethod
    def validate_stored_reason_codes(cls, value: list[str]) -> list[str]:
        if len(value) > 32:
            raise ValueError("reason_codes may contain at most 32 entries")
        return _normalize_tags(value, label="reason_codes")

    @field_validator("rationale", "assessor")
    @classmethod
    def strip_stored_assessment_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Assessment text fields must not be blank")
        return normalized

    @field_validator("confidence")
    @classmethod
    def reject_stored_nonfinite_confidence(cls, value: float) -> float:
        if not math.isfinite(value):
            raise ValueError("confidence must be finite")
        return value

    @model_validator(mode="after")
    def validate_original_v1_band_and_review(
        self,
    ) -> "PersistedTaskRoutingAssessmentFields":
        axis_values = self.axes.values()
        if self.band == "routine" and any(value != 1 for value in axis_values):
            raise ValueError("routine requires every governed axis to be 1")
        if self.band == "standard" and any(value == 3 for value in axis_values):
            raise ValueError("standard cannot contain an advanced axis")
        if self.axes.risk == 3 and self.review_mode not in {
            "independent",
            "specialist-independent",
        }:
            raise ValueError("Advanced risk requires an independent review mode")
        return self


class TaskRoutingAssessmentResponse(PersistedTaskRoutingAssessmentFields):
    """Audit-readable assessment projection with fail-closed routeability."""

    id: int
    created_at: datetime
    policy_conformant: bool = False
    is_current: bool

    @model_validator(mode="after")
    def require_conformant_current_assessment(
        self,
    ) -> "TaskRoutingAssessmentResponse":
        if self.is_current and not self.policy_conformant:
            raise ValueError(
                "A nonconformant routing assessment cannot be current"
            )
        return self

    @classmethod
    def from_record(
        cls,
        record: Any,
        *,
        current_task_version: int,
    ) -> "TaskRoutingAssessmentResponse":
        values = {
            field_name: getattr(record, field_name)
            for field_name in cls.model_fields
            if field_name not in {"is_current", "policy_conformant"}
        }
        strict_values = {
            field_name: values[field_name]
            for field_name in TaskRoutingAssessmentCreate.model_fields
        }
        try:
            TaskRoutingAssessmentCreate.model_validate(strict_values)
        except ValidationError:
            policy_conformant = False
        else:
            policy_conformant = True
        values["policy_conformant"] = policy_conformant
        values["is_current"] = (
            policy_conformant
            and record.task_version == current_task_version
        )
        return cls.model_validate(values)


class TaskRoutingAssessmentState(RoutingContractModel):
    """Explicit current, stale, or absent assessment state for one task."""

    task_id: int = Field(..., strict=True, ge=1)
    current_task_version: int = Field(..., strict=True, ge=1)
    state: Literal["none", "current", "stale"]
    assessment: TaskRoutingAssessmentResponse | None = None

    @model_validator(mode="after")
    def validate_lifecycle_state(self) -> "TaskRoutingAssessmentState":
        if self.state == "none":
            if self.assessment is not None:
                raise ValueError("none assessment state cannot contain an assessment")
            return self
        if self.assessment is None:
            raise ValueError(f"{self.state} assessment state requires an assessment")
        if self.assessment.task_id != self.task_id:
            raise ValueError("assessment task_id must match the state task_id")
        if self.state == "current":
            if (
                not self.assessment.is_current
                or self.assessment.task_version != self.current_task_version
            ):
                raise ValueError("current assessment state requires a current assessment")
        elif self.assessment.is_current:
            raise ValueError("stale assessment state cannot contain a current assessment")
        return self


TaskRoutingAssessmentStateResponse = TaskRoutingAssessmentState


class TaskRoutingAssessmentListResponse(RoutingContractModel):
    """Bounded newest-first assessment history for one task."""

    task_id: int = Field(..., strict=True, ge=1)
    current_task_version: int = Field(..., strict=True, ge=1)
    assessments: list[TaskRoutingAssessmentResponse] = Field(
        default_factory=list,
        max_length=MAX_ROUTING_ASSESSMENT_HISTORY,
    )
    total_count: int = Field(..., strict=True, ge=0)
    omitted_count: int = Field(default=0, strict=True, ge=0)

    @model_validator(mode="after")
    def validate_history(self) -> "TaskRoutingAssessmentListResponse":
        if self.total_count != len(self.assessments) + self.omitted_count:
            raise ValueError(
                "total_count must equal returned assessments plus omitted_count"
            )
        if any(item.task_id != self.task_id for item in self.assessments):
            raise ValueError("All assessments must belong to the requested task")
        current_items = [item for item in self.assessments if item.is_current]
        if len(current_items) > 1:
            raise ValueError("Assessment history may contain at most one current item")
        if current_items and (
            current_items[0].task_version != self.current_task_version
        ):
            raise ValueError("Current assessment must match current_task_version")
        if self.assessments != sorted(
            self.assessments,
            key=lambda item: (item.created_at, item.id),
            reverse=True,
        ):
            raise ValueError("Assessment history must be newest first")
        return self


class TaskRoutingAssessmentMutationReceipt(RoutingContractModel):
    """Durable replay-safe receipt for an authoritative assessment write."""

    operation: Literal["routing.assessment.create"] = "routing.assessment.create"
    actor_id: int = Field(..., strict=True, ge=1)
    target_type: Literal["task_routing_assessment"] = "task_routing_assessment"
    target_id: int = Field(..., strict=True, ge=1)
    task_id: int = Field(..., strict=True, ge=1)
    idempotency_key: str = Field(..., min_length=1, max_length=255)
    rationale: str = Field(..., min_length=1, max_length=2_000)
    correlation_id: str = Field(..., min_length=1, max_length=255)
    authoritative_task_version: int = Field(..., strict=True, ge=1)
    assessment: TaskRoutingAssessmentResponse
    audit_event_ids: list[int] = Field(default_factory=list, max_length=16)

    @field_validator("idempotency_key", "rationale", "correlation_id")
    @classmethod
    def validate_receipt_text(cls, value: str) -> str:
        if value != value.strip() or any(
            ord(character) < 32 or ord(character) == 127 for character in value
        ):
            raise ValueError(
                "Receipt metadata must not contain control characters or outer whitespace"
            )
        return value

    @field_validator("audit_event_ids")
    @classmethod
    def validate_audit_event_ids(cls, value: list[int]) -> list[int]:
        if any(isinstance(item, bool) or item < 1 for item in value):
            raise ValueError("audit_event_ids must contain positive integers")
        if len(value) != len(set(value)):
            raise ValueError("audit_event_ids must be unique")
        return value

    @model_validator(mode="after")
    def validate_receipt_target(self) -> "TaskRoutingAssessmentMutationReceipt":
        if self.target_id != self.assessment.id:
            raise ValueError("target_id must identify the returned assessment")
        if self.task_id != self.assessment.task_id:
            raise ValueError("task_id must match the returned assessment")
        if self.authoritative_task_version != self.assessment.task_version:
            raise ValueError(
                "authoritative_task_version must match the returned assessment"
            )
        return self


class AgentRoutingPreviewCreate(RoutingContractModel):
    """Read-only exact-actor preview command bound to current task state."""

    purpose: Literal["execution", "verification"]
    assessment_id: int = Field(..., strict=True, ge=1)
    expected_task_version: int = Field(..., strict=True, ge=1)
    reviewer_profile_id: int | None = Field(default=None, strict=True, ge=1)


class AgentRoutingCandidate(RoutingContractModel):
    """One eligible actor plus exact model-binding candidate."""

    actor_id: int = Field(..., strict=True, ge=1)
    actor_revision: PositiveRevision
    actor_queue_revision: PositiveRevision
    profile_id: int = Field(..., strict=True, ge=1)
    profile_revision: str = Field(..., min_length=1, max_length=120)
    capacity_owner_id: int | None = Field(default=None, strict=True, ge=1)
    capacity_owner_profile_id: int | None = Field(
        default=None,
        strict=True,
        ge=1,
    )
    model_binding_id: int = Field(..., strict=True, ge=1)
    model_binding_revision: PositiveRevision
    model_catalog_id: int = Field(..., strict=True, ge=1)
    model_catalog_key: RoutingKey
    model_catalog_revision: PositiveRevision
    configured_model_alias: str = Field(..., min_length=1, max_length=255)
    eligible: Literal[True] = True
    hard_blocker_codes: list[RoutingBlockerCode] = Field(
        default_factory=list,
        max_length=0,
    )
    matched_skill_levels: dict[str, SkillLevel] = Field(default_factory=dict)
    missing_skill_keys: list[RoutingKey] = Field(default_factory=list, max_length=0)
    blocking_weakness_keys: list[RoutingKey] = Field(
        default_factory=list,
        max_length=0,
    )
    reasoning_tier: ReasoningTier
    context_tier: ModelContextTier
    modality_tags: list[str] = Field(default_factory=list)
    tool_tags: list[str] = Field(default_factory=list)
    data_policy_tags: list[str] = Field(default_factory=list)
    cost_tier: ModelCostTier
    latency_tier: ModelLatencyTier
    available_capacity_days: float = Field(..., ge=0)
    committed_effort_days: float = Field(..., ge=0)
    workload_ratio: float = Field(..., ge=0)
    vacation_conflict: Literal[False] = False
    queued_assignments: int = Field(..., strict=True, ge=0)
    accepted_assignments: int = Field(..., strict=True, ge=0)
    running_runs: int = Field(..., strict=True, ge=0)
    schedule_delay_days: float = Field(..., ge=0)
    schedule_eligible: Literal[True] = True
    adequacy_class: int = Field(..., strict=True, ge=0)
    rank: int = Field(..., strict=True, ge=1)
    confidence: float = Field(
        ...,
        ge=MIN_ROUTING_ASSESSMENT_CONFIDENCE,
        le=1.0,
    )
    rationale: str = Field(..., min_length=1, max_length=2_000)

    @field_validator("matched_skill_levels", mode="before")
    @classmethod
    def validate_matched_skills(cls, value: Any) -> Any:
        return _normalize_required_skill_levels(value)

    @field_validator("modality_tags", "tool_tags", "data_policy_tags")
    @classmethod
    def validate_capability_tags(cls, value: list[str], info: Any) -> list[str]:
        return _normalize_tags(value, label=info.field_name)

    @field_validator(
        "profile_revision",
        "configured_model_alias",
        "rationale",
    )
    @classmethod
    def strip_candidate_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Candidate text fields must not be blank")
        return normalized


class AgentRoutingExclusion(RoutingContractModel):
    """Bounded reason evidence for one ineligible actor/binding pair."""

    actor_id: int = Field(..., strict=True, ge=1)
    actor_revision: PositiveRevision
    actor_queue_revision: PositiveRevision
    profile_id: int | None = Field(default=None, strict=True, ge=1)
    profile_revision: str | None = Field(default=None, min_length=1, max_length=120)
    capacity_owner_id: int | None = Field(default=None, strict=True, ge=1)
    capacity_owner_profile_id: int | None = Field(
        default=None,
        strict=True,
        ge=1,
    )
    model_binding_id: int | None = Field(default=None, strict=True, ge=1)
    model_binding_revision: PositiveRevision | None = None
    model_catalog_id: int | None = Field(default=None, strict=True, ge=1)
    model_catalog_key: RoutingKey | None = None
    model_catalog_revision: PositiveRevision | None = None
    configured_model_alias: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    eligible: Literal[False] = False
    hard_blocker_codes: list[RoutingBlockerCode] = Field(
        ...,
        min_length=1,
        max_length=len(RoutingBlockerCode),
    )
    matched_skill_levels: dict[str, SkillLevel] = Field(default_factory=dict)
    missing_skill_keys: list[RoutingKey] = Field(default_factory=list)
    insufficient_skill_keys: list[RoutingKey] = Field(default_factory=list)
    blocking_weakness_keys: list[RoutingKey] = Field(default_factory=list)
    reasoning_tier: ReasoningTier | None = None
    context_tier: ModelContextTier | None = None
    cost_tier: ModelCostTier | None = None
    latency_tier: ModelLatencyTier | None = None
    missing_modality_tags: list[str] = Field(default_factory=list)
    missing_tool_tags: list[str] = Field(default_factory=list)
    missing_data_policy_tags: list[str] = Field(default_factory=list)
    available_capacity_days: float | None = None
    committed_effort_days: float | None = Field(default=None, ge=0)
    workload_ratio: float | None = Field(default=None, ge=0)
    vacation_conflict: bool | None = None
    queued_assignments: int | None = Field(default=None, strict=True, ge=0)
    accepted_assignments: int | None = Field(default=None, strict=True, ge=0)
    running_runs: int | None = Field(default=None, strict=True, ge=0)
    schedule_delay_days: float | None = Field(default=None, ge=0)
    schedule_eligible: bool | None = None
    rationale: str = Field(..., min_length=1, max_length=2_000)

    @field_validator("hard_blocker_codes", mode="before")
    @classmethod
    def validate_blocker_codes(cls, value: Any) -> Any:
        if not isinstance(value, list):
            raise ValueError("hard_blocker_codes must be a JSON list")
        normalized = _normalize_routing_keys(
            value,
            label="hard_blocker_codes",
            maximum_entries=len(RoutingBlockerCode),
        )
        unknown = normalized and set(normalized).difference(
            blocker.value for blocker in RoutingBlockerCode
        )
        if unknown:
            raise ValueError(
                "Unknown routing blocker codes: " + ", ".join(sorted(unknown))
            )
        return normalized

    @field_validator("matched_skill_levels", mode="before")
    @classmethod
    def validate_matched_skills(cls, value: Any) -> Any:
        return _normalize_required_skill_levels(value)

    @field_validator(
        "missing_skill_keys",
        "insufficient_skill_keys",
        "blocking_weakness_keys",
        mode="before",
    )
    @classmethod
    def validate_skill_keys(cls, value: Any, info: Any) -> Any:
        if not isinstance(value, list):
            raise ValueError(f"{info.field_name} must be a JSON list")
        normalized = _normalize_routing_keys(value, label=info.field_name)
        unknown = set(normalized).difference(ROUTING_SKILL_KEYS)
        if unknown:
            raise ValueError(
                "Unknown routing skill keys: " + ", ".join(sorted(unknown))
            )
        return normalized

    @field_validator(
        "missing_modality_tags",
        "missing_tool_tags",
        "missing_data_policy_tags",
    )
    @classmethod
    def validate_missing_tags(cls, value: list[str], info: Any) -> list[str]:
        return _normalize_tags(value, label=info.field_name)

    @field_validator(
        "profile_revision",
        "configured_model_alias",
        "rationale",
    )
    @classmethod
    def strip_optional_exclusion_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        if not normalized:
            raise ValueError("Exclusion text fields must not be blank")
        return normalized


class AgentRoutingPreviewResponse(RoutingContractModel):
    """Read-only expiring result over a digest-bound routing input snapshot."""

    preview_id: str = Field(..., min_length=1, max_length=255)
    preview_digest: RoutingDigest
    input_digest: RoutingDigest
    task_id: int = Field(..., strict=True, ge=1)
    purpose: Literal["execution", "verification"]
    assessment_id: int = Field(..., strict=True, ge=1)
    assessment_task_version: int = Field(..., strict=True, ge=1)
    current_task_version: int = Field(..., strict=True, ge=1)
    policy_version: Literal["model-aware-routing-v1"] = ROUTING_POLICY_VERSION
    review_mode: TaskReviewMode
    reviewer_profile_id: int | None = Field(default=None, strict=True, ge=1)
    generated_at: datetime
    expires_at: datetime
    recommended_candidate: AgentRoutingCandidate | None = None
    eligible_candidates: list[AgentRoutingCandidate] = Field(
        default_factory=list,
        max_length=MAX_ROUTING_CANDIDATES,
    )
    exclusions: list[AgentRoutingExclusion] = Field(
        default_factory=list,
        max_length=MAX_ROUTING_EXCLUSIONS,
    )
    eligible_candidates_omitted: int = Field(default=0, strict=True, ge=0)
    exclusions_omitted: int = Field(default=0, strict=True, ge=0)
    hard_blocker_codes: list[RoutingBlockerCode] = Field(default_factory=list)

    @field_validator("preview_id")
    @classmethod
    def strip_preview_id(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized or normalized != value:
            raise ValueError("preview_id must not be blank or contain outer whitespace")
        return normalized

    @field_validator("hard_blocker_codes", mode="before")
    @classmethod
    def validate_global_blockers(cls, value: Any) -> Any:
        if not isinstance(value, list):
            raise ValueError("hard_blocker_codes must be a JSON list")
        normalized = _normalize_routing_keys(
            value,
            label="hard_blocker_codes",
            maximum_entries=len(RoutingBlockerCode),
        )
        unknown = set(normalized).difference(
            blocker.value for blocker in RoutingBlockerCode
        )
        if unknown:
            raise ValueError(
                "Unknown routing blocker codes: " + ", ".join(sorted(unknown))
            )
        return normalized

    @model_validator(mode="after")
    def validate_preview_state(self) -> "AgentRoutingPreviewResponse":
        for label, value in (
            ("generated_at", self.generated_at),
            ("expires_at", self.expires_at),
        ):
            if value.tzinfo is None or value.utcoffset() is None:
                raise ValueError(f"{label} must be timezone-aware")
        if (
            self.expires_at - self.generated_at
        ).total_seconds() != ROUTING_PREVIEW_TTL_SECONDS:
            raise ValueError(
                "Routing preview expiry must use the frozen "
                f"{ROUTING_PREVIEW_TTL_SECONDS}-second TTL"
            )
        if self.assessment_task_version != self.current_task_version:
            raise ValueError(
                "Preview assessment version must match current_task_version"
            )
        ranks = [candidate.rank for candidate in self.eligible_candidates]
        if ranks != sorted(ranks) or len(ranks) != len(set(ranks)):
            raise ValueError(
                "Eligible candidates must have unique ascending deterministic ranks"
            )
        no_candidate = RoutingBlockerCode.NO_ELIGIBLE_CANDIDATE.value
        if self.eligible_candidates:
            first = self.eligible_candidates[0]
            if self.recommended_candidate is None:
                raise ValueError(
                    "An eligible preview must contain a recommended_candidate"
                )
            if (
                self.recommended_candidate.actor_id,
                self.recommended_candidate.model_binding_id,
                self.recommended_candidate.rank,
            ) != (first.actor_id, first.model_binding_id, first.rank):
                raise ValueError(
                    "recommended_candidate must be the first eligible candidate"
                )
            if self.hard_blocker_codes:
                raise ValueError(
                    "An eligible preview cannot contain global hard blockers"
                )
        else:
            if self.recommended_candidate is not None:
                raise ValueError(
                    "A no-candidate preview cannot recommend a candidate"
                )
            if no_candidate not in self.hard_blocker_codes:
                raise ValueError(
                    "A no-candidate preview must contain no_eligible_candidate"
                )
        return self


class RoutingCandidateSummary(RoutingContractModel):
    """Compact ordered eligible-candidate evidence retained on assignment."""

    actor_id: int = Field(..., strict=True, ge=1)
    profile_id: int = Field(..., strict=True, ge=1)
    model_binding_id: int = Field(..., strict=True, ge=1)
    model_binding_revision: PositiveRevision
    model_catalog_key: RoutingKey
    rank: int = Field(..., strict=True, ge=1)
    adequacy_class: int = Field(..., strict=True, ge=0)
    cost_tier: ModelCostTier
    latency_tier: ModelLatencyTier


class RoutingExclusionSummary(RoutingContractModel):
    """Compact actionable exclusion evidence retained on assignment."""

    actor_id: int = Field(..., strict=True, ge=1)
    model_binding_id: int | None = Field(default=None, strict=True, ge=1)
    hard_blocker_codes: tuple[RoutingBlockerCode, ...] = Field(
        ...,
        min_length=1,
        max_length=len(RoutingBlockerCode),
    )

    @field_validator("hard_blocker_codes", mode="before")
    @classmethod
    def validate_blocker_codes(cls, value: Any) -> Any:
        if not isinstance(value, (list, tuple)):
            raise ValueError("hard_blocker_codes must be an array")
        normalized = _normalize_routing_keys(
            list(value),
            label="hard_blocker_codes",
            maximum_entries=len(RoutingBlockerCode),
        )
        unknown = set(normalized).difference(
            blocker.value for blocker in RoutingBlockerCode
        )
        if unknown:
            raise ValueError(
                "Unknown routing blocker codes: " + ", ".join(sorted(unknown))
            )
        return tuple(normalized)


class RoutingTrustLineage(RoutingContractModel):
    """Secret-free identities responsible for each routing evidence boundary."""

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        allow_inf_nan=False,
        use_enum_values=True,
        frozen=True,
    )

    assessment_assessor: str = Field(..., min_length=1, max_length=255)
    assessment_assessor_actor_id: int | None = Field(
        default=None,
        strict=True,
        ge=1,
    )
    preview_requested_by_actor_id: int = Field(..., strict=True, ge=1)
    assignment_created_by_actor_id: int = Field(..., strict=True, ge=1)
    execution_actor_id: int = Field(..., strict=True, ge=1)
    observed_model_reported_by_actor_id: int | None = Field(
        default=None,
        strict=True,
        ge=1,
    )

    @field_validator("assessment_assessor")
    @classmethod
    def strip_assessor(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("assessment_assessor must not be blank")
        return normalized


class RoutingDecisionSnapshot(RoutingContractModel):
    """Immutable server-generated evidence for one exact routing selection."""

    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True,
        allow_inf_nan=False,
        use_enum_values=True,
        frozen=True,
    )

    schema_version: Literal["routing-decision-snapshot-v1"] = (
        "routing-decision-snapshot-v1"
    )
    selection_pending: Literal[False] = False
    policy_version: Literal["model-aware-routing-v1"] = ROUTING_POLICY_VERSION
    task_id: int = Field(..., strict=True, ge=1)
    task_version: int = Field(..., strict=True, ge=1)
    assessment_id: int = Field(..., strict=True, ge=1)
    assessment_task_version: int = Field(..., strict=True, ge=1)
    assessment_band: TaskDifficultyBand
    assessment_confidence: float = Field(
        ...,
        ge=MIN_ROUTING_ASSESSMENT_CONFIDENCE,
        le=1.0,
    )
    assessment_reason_codes: tuple[AssessmentReasonCode, ...] = ()
    purpose: Literal["execution", "verification"]
    actor_id: int = Field(..., strict=True, ge=1)
    actor_revision: PositiveRevision
    actor_queue_revision: PositiveRevision
    profile_id: int = Field(..., strict=True, ge=1)
    profile_revision: str = Field(..., min_length=1, max_length=120)
    capacity_owner_id: int | None = Field(default=None, strict=True, ge=1)
    capacity_owner_profile_id: int | None = Field(
        default=None,
        strict=True,
        ge=1,
    )
    model_binding_id: int = Field(..., strict=True, ge=1)
    model_binding_revision: PositiveRevision
    model_catalog_id: int = Field(..., strict=True, ge=1)
    model_catalog_key: RoutingKey
    model_catalog_revision: PositiveRevision
    configured_model_alias: str = Field(..., min_length=1, max_length=255)
    selected_reasoning_tier: ReasoningTier
    selected_context_tier: ModelContextTier
    resolved_model: str | None = Field(default=None, min_length=1, max_length=255)
    review_mode: TaskReviewMode
    reviewer_profile_id: int | None = Field(default=None, strict=True, ge=1)
    routing_preview_id: str = Field(..., min_length=1, max_length=255)
    routing_preview_digest: RoutingDigest
    input_digest: RoutingDigest
    preview_generated_at: datetime
    preview_expires_at: datetime
    selected_rank: int = Field(..., strict=True, ge=1)
    adequacy_class: int = Field(..., strict=True, ge=0)
    selection_reason_codes: tuple[RoutingKey, ...] = ()
    eligible_candidate_summaries: tuple[RoutingCandidateSummary, ...] = Field(
        ...,
        min_length=1,
        max_length=MAX_ROUTING_CANDIDATES,
    )
    exclusion_summaries: tuple[RoutingExclusionSummary, ...] = Field(
        default=(),
        max_length=MAX_ROUTING_EXCLUSIONS,
    )
    eligible_candidates_omitted: int = Field(default=0, strict=True, ge=0)
    exclusions_omitted: int = Field(default=0, strict=True, ge=0)
    rationale: str = Field(..., min_length=1, max_length=2_000)
    confidence: float = Field(
        ...,
        ge=MIN_ROUTING_ASSESSMENT_CONFIDENCE,
        le=1.0,
    )
    trust_lineage: RoutingTrustLineage
    prior_lineage: dict[str, Any] | None = None

    @field_validator(
        "profile_revision",
        "configured_model_alias",
        "resolved_model",
        "routing_preview_id",
        "rationale",
    )
    @classmethod
    def strip_snapshot_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        if not normalized:
            raise ValueError("Routing snapshot text fields must not be blank")
        return normalized

    @field_validator("assessment_reason_codes", mode="before")
    @classmethod
    def validate_snapshot_assessment_reasons(cls, value: Any) -> Any:
        if not isinstance(value, (list, tuple)):
            raise ValueError("assessment_reason_codes must be an array")
        return tuple(_normalize_assessment_reason_codes(list(value)))

    @field_validator("selection_reason_codes", mode="before")
    @classmethod
    def validate_selection_reasons(cls, value: Any) -> Any:
        if not isinstance(value, (list, tuple)):
            raise ValueError("selection_reason_codes must be an array")
        return tuple(
            _normalize_routing_keys(
                list(value),
                label="selection_reason_codes",
                maximum_entries=MAX_ROUTING_TAGS,
            )
        )

    @field_validator("prior_lineage", mode="before")
    @classmethod
    def validate_prior_lineage_packet(
        cls,
        value: Any,
    ) -> dict[str, Any] | None:
        if value is None:
            return None
        if not isinstance(value, dict):
            raise ValueError("prior_lineage must be a JSON object")
        if (
            value.get("schema_version") != "routing-lineage-snapshot-v1"
            or value.get("selection_pending") is not True
        ):
            raise ValueError(
                "prior_lineage must contain a pending routing lineage snapshot"
            )
        validate_routing_packet_size(value, label="Prior routing lineage")
        return value

    @model_validator(mode="after")
    def validate_selected_lineage(self) -> "RoutingDecisionSnapshot":
        if self.assessment_task_version != self.task_version:
            raise ValueError(
                "assessment_task_version must match the selected task_version"
            )
        if self.trust_lineage.execution_actor_id != self.actor_id:
            raise ValueError(
                "trust lineage execution actor must match the selected actor"
            )
        if self.prior_lineage is not None:
            if self.purpose != "execution":
                raise ValueError(
                    "Only execution selections may carry prior routing lineage"
                )
            if self.prior_lineage.get("task_id") != self.task_id:
                raise ValueError(
                    "Prior routing lineage task must match the selected task"
                )
        ranks = [
            candidate.rank
            for candidate in self.eligible_candidate_summaries
        ]
        if ranks != sorted(ranks) or len(ranks) != len(set(ranks)):
            raise ValueError(
                "Eligible candidate summaries must use unique ascending ranks"
            )
        if not any(
            candidate.actor_id == self.actor_id
            and candidate.model_binding_id == self.model_binding_id
            and candidate.rank == self.selected_rank
            for candidate in self.eligible_candidate_summaries
        ):
            raise ValueError(
                "Selected actor, binding, and rank must appear in candidate summaries"
            )
        for label, value in (
            ("preview_generated_at", self.preview_generated_at),
            ("preview_expires_at", self.preview_expires_at),
        ):
            if value.tzinfo is None or value.utcoffset() is None:
                raise ValueError(f"{label} must be timezone-aware")
        if (
            self.preview_expires_at - self.preview_generated_at
        ).total_seconds() != ROUTING_PREVIEW_TTL_SECONDS:
            raise ValueError(
                "Routing snapshot preview expiry must use the frozen "
                f"{ROUTING_PREVIEW_TTL_SECONDS}-second TTL"
            )
        return self
