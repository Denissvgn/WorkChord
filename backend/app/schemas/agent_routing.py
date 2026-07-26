"""Provider-neutral model-routing persistence contracts.

These schemas deliberately contain no credentials, provider endpoints, prompts,
or runtime logs.  They define the bounded data shapes used by the Wave 1
persistence layer; routing policy and candidate selection remain separate.
"""

from __future__ import annotations

import math
import re
from datetime import datetime
from typing import Annotated, Any, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)


ROUTING_POLICY_VERSION = "model-aware-routing-v1"
MAX_ROUTING_TAGS = 32
MAX_REQUIRED_SKILLS = 50
MAX_REASON_CODES = 32
MAX_ROUTING_TEXT_LENGTH = 8_000

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
ModelContextTier = Literal["small", "medium", "large"]
ModelCostTier = Literal["low", "medium", "high"]
ModelLatencyTier = Literal["fast", "balanced", "slow"]
TaskDifficultyBand = Literal["routine", "standard", "advanced"]
TaskReviewMode = Literal[
    "none",
    "standard",
    "independent",
    "specialist-independent",
]


def _normalize_tags(values: list[str], *, label: str) -> list[str]:
    if len(values) > MAX_ROUTING_TAGS:
        raise ValueError(f"{label} may contain at most {MAX_ROUTING_TAGS} entries")
    normalized: list[str] = []
    for value in values:
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
    )


class AgentModelCatalogFields(RoutingContractModel):
    """Secret-free provider-neutral model catalog fields."""

    key: RoutingKey
    provider: str = Field(..., min_length=1, max_length=120)
    configured_model_alias: str = Field(..., min_length=1, max_length=255)
    reasoning_tier: int = Field(..., ge=1, le=3)
    context_tier: ModelContextTier
    modality_tags: list[str] = Field(default_factory=lambda: ["text"])
    cost_tier: ModelCostTier
    latency_tier: ModelLatencyTier
    enabled: bool = True
    revision: int = Field(default=1, ge=1)
    last_verified_at: datetime | None = None

    @field_validator("key", mode="before")
    @classmethod
    def normalize_catalog_key(cls, value: Any) -> Any:
        return value.strip().lower() if isinstance(value, str) else value

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
    revision: int = Field(default=1, ge=1)

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


class AgentModelBindingResponse(AgentModelBindingFields):
    """Persisted binding projection."""

    id: int
    model_catalog_key: str | None = None
    selectable: bool = False
    created_at: datetime
    updated_at: datetime


class TaskDifficultyAxes(RoutingContractModel):
    """Five governed task-difficulty axes on a closed 1..3 scale."""

    reasoning: int = Field(..., ge=1, le=3)
    ambiguity: int = Field(..., ge=1, le=3)
    context_breadth: int = Field(..., ge=1, le=3)
    risk: int = Field(..., ge=1, le=3)
    verification_burden: int = Field(..., ge=1, le=3)

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

    minimum_reasoning_tier: int = Field(..., ge=1, le=3)
    minimum_context_tier: ModelContextTier
    modality_tags: list[str] = Field(default_factory=lambda: ["text"])
    tool_tags: list[str] = Field(default_factory=list)
    data_policy_tags: list[str] = Field(default_factory=list)

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
    def validate_required_skills(cls, value: dict[str, int]) -> dict[str, int]:
        if len(value) > MAX_REQUIRED_SKILLS:
            raise ValueError(
                f"required_skill_levels may contain at most {MAX_REQUIRED_SKILLS} entries"
            )
        normalized: dict[str, int] = {}
        for raw_key, level in value.items():
            key = raw_key.strip().lower()
            if not re.fullmatch(r"[a-z0-9](?:[a-z0-9._-]{0,118}[a-z0-9])?", key):
                raise ValueError("Required skill keys must be stable lowercase keys")
            if key in normalized:
                raise ValueError("Required skill keys must be unique after normalization")
            if not 1 <= level <= 5:
                raise ValueError("Required skill levels must be between 1 and 5")
            normalized[key] = level
        return dict(sorted(normalized.items()))

    @field_validator("reason_codes")
    @classmethod
    def validate_reason_codes(cls, value: list[str]) -> list[str]:
        if len(value) > MAX_REASON_CODES:
            raise ValueError(f"reason_codes may contain at most {MAX_REASON_CODES} entries")
        return _normalize_tags(value, label="reason_codes")

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
        axes = self.axes.values()
        if self.band == "routine" and any(value != 1 for value in axes):
            raise ValueError("routine requires every governed axis to be 1")
        if self.band == "standard" and any(value == 3 for value in axes):
            raise ValueError("standard cannot contain an advanced axis")
        if self.axes.risk == 3 and self.review_mode not in {
            "independent",
            "specialist-independent",
        }:
            raise ValueError("Advanced risk requires an independent review mode")
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


class TaskRoutingAssessmentResponse(TaskRoutingAssessmentFields):
    """Persisted assessment projection with deterministic staleness."""

    id: int
    created_at: datetime
    is_current: bool

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
            if field_name not in {"is_current"}
        }
        values["is_current"] = record.task_version == current_task_version
        return cls.model_validate(values)
