"""Bounded schemas for autonomous work-package and verifier lifecycles."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


SHA256_PATTERN = r"^[0-9a-f]{64}$"
IDENTIFIER_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9._:-]{0,254}$"


class AutonomySchema(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class VerificationRequirementCreate(AutonomySchema):
    slot_key: str = Field(pattern=IDENTIFIER_PATTERN)
    verifier_logical_key: str = Field(pattern=IDENTIFIER_PATTERN)
    criterion_schema: str = Field(pattern=IDENTIFIER_PATTERN)
    evaluator_version: str = Field(min_length=1, max_length=255)
    executor_independence_group: str = Field(pattern=IDENTIFIER_PATTERN)
    verifier_independence_group: str = Field(pattern=IDENTIFIER_PATTERN)

    @model_validator(mode="after")
    def independent(self) -> "VerificationRequirementCreate":
        if self.executor_independence_group == self.verifier_independence_group:
            raise ValueError("Executor and verifier independence groups must differ")
        return self


class AgentWorkPackageCreate(AutonomySchema):
    package_key: str = Field(pattern=IDENTIFIER_PATTERN)
    package_version: int = Field(ge=1)
    execution_task_id: int | None = Field(default=None, ge=1)
    predecessor_package_id: int | None = Field(default=None, ge=1)
    artifact_set_digest: str = Field(pattern=SHA256_PATTERN)
    contract_manifest_digest: str = Field(pattern=SHA256_PATTERN)
    source_contract_digest: str = Field(pattern=SHA256_PATTERN)
    external_journal_revision: int = Field(ge=1)
    external_journal_head_digest: str = Field(pattern=SHA256_PATTERN)
    requirements: tuple[VerificationRequirementCreate, ...] = Field(
        min_length=1, max_length=64
    )

    @model_validator(mode="after")
    def unique_slots(self) -> "AgentWorkPackageCreate":
        slots = [item.slot_key for item in self.requirements]
        if len(set(slots)) != len(slots):
            raise ValueError("Verification requirement slots must be unique")
        if self.external_journal_head_digest == "0" * 64:
            raise ValueError("WorkChord projection requires a committed external journal head")
        object.__setattr__(
            self,
            "requirements",
            tuple(sorted(self.requirements, key=lambda item: item.slot_key)),
        )
        return self


class ResolvedVerifierLease(AutonomySchema):
    """Result of resolving an external signed action lease before service entry."""

    lease_digest: str = Field(pattern=SHA256_PATTERN)
    task_id: str = Field(pattern=IDENTIFIER_PATTERN)
    stage_id: str = Field(pattern=IDENTIFIER_PATTERN)
    action: Literal["verification-claim", "verification-begin", "verification-renew", "verification-submit"]
    actor_logical_key: str = Field(pattern=IDENTIFIER_PATTERN)
    actor_id: int = Field(ge=1)
    topology_revision: int = Field(ge=1)
    attempt_start_digest: str = Field(pattern=SHA256_PATTERN)
    issued_at: datetime
    expires_at: datetime

    @model_validator(mode="after")
    def valid_window(self) -> "ResolvedVerifierLease":
        if self.issued_at.tzinfo is None or self.expires_at.tzinfo is None:
            raise ValueError("Resolved verifier lease timestamps must be timezone-aware")
        if self.expires_at <= self.issued_at:
            raise ValueError("Resolved verifier lease expiry is invalid")
        return self


class VerificationClaimRequest(AutonomySchema):
    requirement_id: int = Field(ge=1)
    expected_package_version: int = Field(ge=1)
    expected_artifact_set_digest: str = Field(pattern=SHA256_PATTERN)
    external_journal_revision: int = Field(ge=1)
    external_journal_head_digest: str = Field(pattern=SHA256_PATTERN)


class VerificationBeginRequest(AutonomySchema):
    requirement_id: int = Field(ge=1)
    expected_lease_generation: int = Field(ge=1)
    expected_lease_digest: str = Field(pattern=SHA256_PATTERN)
    runtime_attestation_digest: str = Field(pattern=SHA256_PATTERN)
    external_journal_revision: int = Field(ge=1)
    external_journal_head_digest: str = Field(pattern=SHA256_PATTERN)


class VerificationRenewRequest(AutonomySchema):
    requirement_id: int = Field(ge=1)
    expected_lease_generation: int = Field(ge=1)
    expected_lease_digest: str = Field(pattern=SHA256_PATTERN)
    external_journal_revision: int = Field(ge=1)
    external_journal_head_digest: str = Field(pattern=SHA256_PATTERN)


class VerificationCriterionResult(AutonomySchema):
    criterion_id: str = Field(pattern=IDENTIFIER_PATTERN)
    evidence_object_digest: str = Field(pattern=SHA256_PATTERN)
    evaluator_predicate_digest: str = Field(pattern=SHA256_PATTERN)
    outcome: Literal["passed", "failed"]


class VerificationSubmitRequest(AutonomySchema):
    requirement_id: int = Field(ge=1)
    expected_lease_generation: int = Field(ge=1)
    expected_lease_digest: str = Field(pattern=SHA256_PATTERN)
    artifact_set_digest: str = Field(pattern=SHA256_PATTERN)
    criterion_results: tuple[VerificationCriterionResult, ...] = Field(
        min_length=1, max_length=512
    )
    evaluator_attestation_digest: str = Field(pattern=SHA256_PATTERN)
    external_journal_revision: int = Field(ge=1)
    external_journal_head_digest: str = Field(pattern=SHA256_PATTERN)

    @field_validator("criterion_results")
    @classmethod
    def unique_criteria(
        cls, value: tuple[VerificationCriterionResult, ...]
    ) -> tuple[VerificationCriterionResult, ...]:
        ids = [item.criterion_id for item in value]
        if len(set(ids)) != len(ids):
            raise ValueError("Criterion IDs must be unique")
        return tuple(sorted(value, key=lambda item: item.criterion_id))


class VerificationRequirementResponse(AutonomySchema):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: int
    package_id: int
    slot_key: str
    verifier_logical_key: str
    state: str
    assigned_verifier_actor_id: int | None
    criterion_schema: str
    artifact_set_digest: str
    evaluator_version: str
    executor_independence_group: str
    verifier_independence_group: str
    lease_generation: int
    lease_digest: str | None
    attempt_start_digest: str | None
    lease_expires_at: datetime | None
    heartbeat_at: datetime | None
    evidence_digest: str | None
    verdict_digest: str | None
    created_at: datetime
    updated_at: datetime


class AgentWorkPackageResponse(AutonomySchema):
    model_config = ConfigDict(from_attributes=True, extra="forbid")

    id: int
    package_key: str
    package_version: int
    execution_task_id: int | None
    predecessor_package_id: int | None
    state: str
    artifact_set_digest: str
    contract_manifest_digest: str
    source_contract_digest: str
    external_journal_revision: int
    external_journal_head_digest: str
    created_at: datetime
    updated_at: datetime
    requirements: list[VerificationRequirementResponse] = Field(max_length=64)


class VerificationTransitionResponse(AutonomySchema):
    requirement: VerificationRequirementResponse
    package_state: Literal["planned", "evaluating", "passed", "rework_required"]
    verdict: Literal["passed", "rejected"] | None = None
