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
    MAX_ROUTING_PACKET_BYTES,
    AssessmentReasonCode,
    ContextTier,
    CostTier,
    DifficultyBand,
    LatencyTier,
    ROUTING_POLICY_VERSION,
    ROUTING_SKILL_KEYS,
    ReasoningTier,
    ReviewMode,
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
            if isinstance(level, bool) or not isinstance(level, int) or not 1 <= level <= 5:
                raise ValueError("Required skill levels must be between 1 and 5")
            normalized[key] = level
        return dict(sorted(normalized.items()))

    @field_validator("reason_codes", mode="before")
    @classmethod
    def validate_reason_codes(cls, value: Any) -> Any:
        if not isinstance(value, list):
            raise ValueError("reason_codes must be a JSON list")
        if len(value) > MAX_REASON_CODES:
            raise ValueError(f"reason_codes may contain at most {MAX_REASON_CODES} entries")
        normalized = _normalize_tags(value, label="reason_codes")
        unknown = set(normalized).difference(ASSESSMENT_REASON_CODES)
        if unknown:
            raise ValueError(
                "Unknown assessment reason codes: " + ", ".join(sorted(unknown))
            )
        return normalized

    @field_validator("rationale", "assessor")
    @classmethod
    def strip_assessment_text(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Assessment text fields must not be blank")
        return normalized

    @field_validator("confidence")
    @classmethod
    def reject_nonfinite_confidence(cls, value: float) -> float:
        if not math.isfinite(value):
            raise ValueError("confidence must be finite")
        return value

    @model_validator(mode="after")
    def validate_band_and_review_override(self) -> "TaskRoutingAssessmentFields":
        derived_band = derive_difficulty_band(self.axes, self.reason_codes)
        if self.band == "routine" and derived_band != "routine":
            raise ValueError(
                "routine requires every governed axis to be 1 and no "
                "escalating reason code"
            )
        if self.band == "standard" and derived_band == "advanced":
            raise ValueError(
                "standard cannot contain an advanced axis or escalating reason code"
            )
        if self.band != derived_band:
            raise ValueError(
                f"band must match deterministic policy derivation: {derived_band}"
            )
        required_review = minimum_review_mode(self.axes, self.reason_codes)
        if self.axes.risk == 3 and not review_mode_meets(
            self.review_mode,
            "independent",
        ):
            raise ValueError("Advanced risk requires an independent review mode")
        if not review_mode_meets(self.review_mode, required_review):
            raise ValueError(
                f"review_mode must meet the policy minimum: {required_review}"
            )
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
