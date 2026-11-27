"""Contracts for the calibration terms under which performance history may inform routing.

A calibration contract names the qualification keys it covers, the sample
bounds and decay any calibration must respect, the bias review that preceded
it and the accountable approver. Storing or approving a contract changes no
routing decision: routing reads only whether an approved contract exists.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from app.schemas.agent_routing import MAX_ROUTING_TAGS, PositiveRevision, RoutingDigest, RoutingKey


CALIBRATION_CONTRACT_SCHEMA_VERSION = "routing-calibration-contract-v1"
CalibrationContractState = Literal["submitted", "approved"]
CalibrationContractAction = Literal["submit", "approve"]
CalibrationDecayMethod = Literal["exponential", "linear", "window"]
MAX_CALIBRATION_SAMPLES = 1_000_000
MAX_CALIBRATION_DAYS = 3_650
MAX_CALIBRATION_LABEL = 255
MAX_CALIBRATION_TEXT = 4_000


class _CalibrationModel(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)


def _clean_text(value: str | None, *, label: str) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{label} must not be blank")
    if any(ord(character) < 32 and character not in "\n\t" for character in normalized):
        raise ValueError(f"{label} must not contain control characters")
    return normalized


class CalibrationSampleBounds(_CalibrationModel):
    """How many observations, and how old, a calibration may use per model and key."""

    minimum_samples: int = Field(..., strict=True, ge=1, le=MAX_CALIBRATION_SAMPLES)
    maximum_samples: int = Field(..., strict=True, ge=1, le=MAX_CALIBRATION_SAMPLES)
    maximum_age_days: int = Field(..., strict=True, ge=1, le=MAX_CALIBRATION_DAYS)

    @model_validator(mode="after")
    def require_ordered_bounds(self) -> "CalibrationSampleBounds":
        if self.maximum_samples < self.minimum_samples:
            raise ValueError("maximum_samples must not be lower than minimum_samples")
        return self


class CalibrationDecay(_CalibrationModel):
    """How an older observation's weight falls.

    ``days`` is the half-life for ``exponential``, the age at which weight
    reaches zero for ``linear``, and the length of the window for ``window``.
    """

    method: CalibrationDecayMethod
    days: int = Field(..., strict=True, ge=1, le=MAX_CALIBRATION_DAYS)


class CalibrationBiasReview(_CalibrationModel):
    """The record of the bias review the terms were checked against."""

    reviewer: str = Field(..., min_length=1, max_length=MAX_CALIBRATION_LABEL)
    reviewed_at: datetime
    findings: str = Field(..., min_length=1, max_length=MAX_CALIBRATION_TEXT)
    mitigations: str | None = Field(default=None, max_length=MAX_CALIBRATION_TEXT)

    @field_validator("reviewer", "findings")
    @classmethod
    def strip_required(cls, value: str, info: Any) -> str:
        return _clean_text(value, label=info.field_name)  # type: ignore[return-value]

    @field_validator("mitigations")
    @classmethod
    def strip_optional(cls, value: str | None) -> str | None:
        if value is not None and not value.strip():
            return None
        return _clean_text(value, label="mitigations")

    @field_validator("reviewed_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("reviewed_at must be timezone-aware")
        return value


class RoutingCalibrationContractTerms(_CalibrationModel):
    """The complete terms of one contract revision; every field is required."""

    qualification_keys: list[RoutingKey] = Field(..., min_length=1, max_length=MAX_ROUTING_TAGS)
    sample_bounds: CalibrationSampleBounds
    decay: CalibrationDecay
    bias_review: CalibrationBiasReview
    approver: str = Field(
        ...,
        min_length=1,
        max_length=MAX_CALIBRATION_LABEL,
        description="The accountable person or role whose approval the terms require.",
    )

    @field_validator("qualification_keys", mode="before")
    @classmethod
    def normalize_keys(cls, value: object) -> object:
        if not isinstance(value, list):
            return value
        return [item.strip().lower() if isinstance(item, str) else item for item in value]

    @field_validator("qualification_keys")
    @classmethod
    def unique_keys(cls, value: list[str]) -> list[str]:
        if len(set(value)) != len(value):
            raise ValueError("qualification_keys must not repeat a key")
        return sorted(value)

    @field_validator("approver")
    @classmethod
    def strip_approver(cls, value: str) -> str:
        return _clean_text(value, label="approver")  # type: ignore[return-value]

    @model_validator(mode="after")
    def decay_within_sample_age(self) -> "RoutingCalibrationContractTerms":
        if self.decay.days > self.sample_bounds.maximum_age_days:
            raise ValueError("decay.days must not exceed sample_bounds.maximum_age_days")
        return self

    def stored(self) -> dict[str, Any]:
        """The canonical JSON form kept on the contract and its revisions."""

        return self.model_dump(mode="json")

    def digest(self) -> str:
        """SHA-256 over the canonical terms; an approval names the digest it read."""

        encoded = json.dumps(self.stored(), sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


class RoutingCalibrationContractSubmit(RoutingCalibrationContractTerms):
    """Submit a new contract under a key that names no contract yet."""

    key: RoutingKey

    @field_validator("key", mode="before")
    @classmethod
    def normalize_key(cls, value: object) -> object:
        return value.strip().lower() if isinstance(value, str) else value


class RoutingCalibrationContractRevise(RoutingCalibrationContractTerms):
    """Submit complete new terms for an existing contract; any approval lapses."""

    expected_revision: PositiveRevision


class RoutingCalibrationContractApprove(_CalibrationModel):
    """Approve the current submitted terms, named by revision and digest."""

    expected_revision: PositiveRevision
    expected_terms_digest: RoutingDigest


class CalibrationContractActor(_CalibrationModel):
    """Who issued a command: the operator's admin key, or an agent actor."""

    actor_type: str
    actor_id: int | None = None


class RoutingCalibrationContractResponse(_CalibrationModel):
    """The current revision of one contract."""

    id: int
    key: str
    schema_version: Literal["routing-calibration-contract-v1"]
    state: CalibrationContractState
    revision: PositiveRevision
    terms: RoutingCalibrationContractTerms
    terms_digest: RoutingDigest
    submitted_by: CalibrationContractActor
    submitted_at: datetime
    approved_by: CalibrationContractActor | None = None
    approved_at: datetime | None = None
    approval_reason: str | None = None
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_record(cls, row: Any) -> "RoutingCalibrationContractResponse":
        return cls(
            id=row.id,
            key=row.key,
            schema_version=row.schema_version,
            state=row.state,
            revision=row.revision,
            terms=row.terms,
            terms_digest=row.terms_digest,
            submitted_by=CalibrationContractActor(
                actor_type=row.submitted_by_actor_type, actor_id=row.submitted_by_actor_id
            ),
            submitted_at=row.submitted_at,
            approved_by=(
                CalibrationContractActor(actor_type=row.approved_by_actor_type, actor_id=row.approved_by_actor_id)
                if row.approved_by_actor_type is not None
                else None
            ),
            approved_at=row.approved_at,
            approval_reason=row.approval_reason,
            created_at=row.created_at,
            updated_at=row.updated_at,
        )


class RoutingCalibrationContractRevisionResponse(_CalibrationModel):
    """One append-only command on a contract, with its terms and reason."""

    revision: PositiveRevision
    action: CalibrationContractAction
    state: CalibrationContractState
    terms: RoutingCalibrationContractTerms
    terms_digest: RoutingDigest
    reason: str
    actor_type: str
    actor_id: int | None = None
    correlation_id: str | None = None
    created_at: datetime


class RoutingCalibrationContractDetail(RoutingCalibrationContractResponse):
    """One contract with every revision it has had."""

    revisions: list[RoutingCalibrationContractRevisionResponse] = Field(default_factory=list)


class RoutingCalibrationContractListResponse(_CalibrationModel):
    """The deployment's contracts, and whether routing may treat any as approved."""

    schema_version: Literal["routing-calibration-contract-v1"] = CALIBRATION_CONTRACT_SCHEMA_VERSION
    approved_contract_exists: bool
    performance_history_use: Literal["advisory"] = Field(
        default="advisory",
        description="Routing does not consume performance history, whether or not a contract is approved.",
    )
    contracts: list[RoutingCalibrationContractResponse]
