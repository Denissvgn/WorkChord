"""Provider mutation/source-collection boundaries and correlation rules."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Literal, Protocol, runtime_checkable

from pydantic import Field, field_validator, model_validator

from app.autonomy.canonical import (
    StrictContractModel,
    canonical_json_bytes,
    ensure_secret_free,
    sha256_hex,
)
from app.autonomy.leases import SignedActionLease


SHA256_PATTERN = r"^[0-9a-f]{64}$"
IDENTIFIER_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9._:-]{0,254}$"
OPAQUE_REF_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9._:/@+-]{2,2047}$"


class ProviderActionRequest(StrictContractModel):
    """Exact mutation request; adapter selection remains charter-owned."""

    domain: Literal[
        "platform",
        "database",
        "application",
        "security",
        "sanitization",
        "retention",
    ]
    operation: str = Field(min_length=1, max_length=255)
    resource_ref: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=2048)
    resource_generation: str = Field(min_length=1, max_length=255)
    environment: Literal["ephemeral", "rehearsal", "production"]
    destructive: bool = False
    exact_object_digest: str | None = Field(default=None, pattern=SHA256_PATTERN)
    lease: SignedActionLease

    @model_validator(mode="after")
    def bounded_action(self) -> "ProviderActionRequest":
        if self.operation == "*" or self.operation.endswith(".*"):
            raise ValueError("Provider operation must be exact")
        if "publication" in self.operation or "announcement" in self.operation:
            raise ValueError("Release-publication operations are not implemented")
        if self.lease.lease.action != self.operation:
            raise ValueError("Provider action differs from its signed lease")
        if self.lease.lease.environment != self.environment:
            raise ValueError("Provider environment differs from its signed lease")
        if self.lease.lease.destructive != self.destructive:
            raise ValueError("Provider destructive flag differs from its signed lease")
        if self.lease.lease.resource_ref != self.resource_ref:
            raise ValueError("Provider target differs from its signed lease")
        if self.lease.lease.resource_generation != self.resource_generation:
            raise ValueError("Provider generation differs from its signed lease")
        if self.destructive:
            if self.environment == "production":
                raise ValueError("Production deletion/overwrite is forbidden")
            if self.domain == "retention" and self.exact_object_digest is None:
                raise ValueError("Retention deletion requires one exact object digest")
        ensure_secret_free(
            self.model_dump(mode="json", exclude={"lease"})
        )
        return self


class ProviderMutationReceipt(StrictContractModel):
    """Adapter response only; it cannot establish acceptance by itself."""

    schema_version: Literal["workchord-provider-mutation-receipt-v1"] = (
        "workchord-provider-mutation-receipt-v1"
    )
    lease_digest: str = Field(pattern=SHA256_PATTERN)
    domain: str = Field(pattern=IDENTIFIER_PATTERN)
    operation: str = Field(min_length=1, max_length=255)
    resource_ref: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=2048)
    resource_generation_before: str = Field(min_length=1, max_length=255)
    resource_generation_after: str = Field(min_length=1, max_length=255)
    provider_request_id: str = Field(min_length=1, max_length=512)
    response_received_at: datetime
    raw_response_uri: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=2048)
    raw_response_sha256: str = Field(pattern=SHA256_PATTERN)
    tls_peer_identity_digest: str = Field(pattern=SHA256_PATTERN)

    @field_validator("response_received_at")
    @classmethod
    def aware_response_time(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Provider response timestamps must be timezone-aware")
        return value


class ProviderAuditObservation(StrictContractModel):
    """Separately credentialed read-only provider/audit observation."""

    schema_version: Literal["workchord-provider-audit-observation-v1"] = (
        "workchord-provider-audit-observation-v1"
    )
    collector_identity: Literal["pg-source-collector"] = "pg-source-collector"
    provider_request_id: str = Field(min_length=1, max_length=512)
    provider_event_id: str = Field(min_length=1, max_length=512)
    operation: str = Field(min_length=1, max_length=255)
    resource_ref: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=2048)
    resource_generation_before: str = Field(min_length=1, max_length=255)
    resource_generation_after: str = Field(min_length=1, max_length=255)
    observed_at: datetime
    source_query_digest: str = Field(pattern=SHA256_PATTERN)
    raw_audit_uri: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=2048)
    raw_audit_sha256: str = Field(pattern=SHA256_PATTERN)
    source_generation: str = Field(min_length=1, max_length=255)

    @field_validator("observed_at")
    @classmethod
    def aware_observation_time(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Provider audit timestamps must be timezone-aware")
        return value


class CorrelatedProviderAction(StrictContractModel):
    schema_version: Literal["workchord-correlated-provider-action-v1"] = (
        "workchord-correlated-provider-action-v1"
    )
    lease_digest: str = Field(pattern=SHA256_PATTERN)
    operation: str = Field(min_length=1, max_length=255)
    resource_ref: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=2048)
    resource_generation_before: str = Field(min_length=1, max_length=255)
    resource_generation_after: str = Field(min_length=1, max_length=255)
    provider_request_id: str = Field(min_length=1, max_length=512)
    provider_event_id: str = Field(min_length=1, max_length=512)
    mutation_receipt_digest: str = Field(pattern=SHA256_PATTERN)
    audit_observation_digest: str = Field(pattern=SHA256_PATTERN)


@runtime_checkable
class ProviderMutationAdapter(Protocol):
    def execute(self, request: ProviderActionRequest) -> ProviderMutationReceipt: ...


@runtime_checkable
class ProviderSourceCollector(Protocol):
    def collect_action(
        self, *, provider_request_id: str, resource_ref: str
    ) -> ProviderAuditObservation: ...


def correlate_provider_action(
    *,
    request: ProviderActionRequest,
    mutation: ProviderMutationReceipt,
    audit: ProviderAuditObservation,
    maximum_clock_delta: timedelta = timedelta(minutes=5),
) -> CorrelatedProviderAction:
    """Require independent request/audit/resource/generation agreement."""

    lease = request.lease.lease
    if mutation.lease_digest != lease.lease_id:
        raise ValueError("Mutation receipt belongs to another action lease")
    if mutation.domain != request.domain or mutation.operation != request.operation:
        raise ValueError("Mutation receipt domain/operation mismatch")
    if audit.operation != request.operation:
        raise ValueError("Provider audit operation mismatch")
    if mutation.provider_request_id != audit.provider_request_id:
        raise ValueError("Provider request/audit correlation failed")
    if mutation.resource_ref != request.resource_ref or audit.resource_ref != request.resource_ref:
        raise ValueError("Provider request/audit target mismatch")
    if mutation.resource_generation_before != request.resource_generation:
        raise ValueError("Mutation began from an unexpected generation")
    if audit.resource_generation_before != mutation.resource_generation_before:
        raise ValueError("Provider audit reports another input generation")
    if audit.resource_generation_after != mutation.resource_generation_after:
        raise ValueError("Provider audit reports another output generation")
    delta = abs(audit.observed_at - mutation.response_received_at)
    if delta > maximum_clock_delta:
        raise ValueError("Provider request/audit clocks cannot be correlated")
    return CorrelatedProviderAction(
        lease_digest=lease.lease_id,
        operation=request.operation,
        resource_ref=request.resource_ref,
        resource_generation_before=mutation.resource_generation_before,
        resource_generation_after=mutation.resource_generation_after,
        provider_request_id=mutation.provider_request_id,
        provider_event_id=audit.provider_event_id,
        mutation_receipt_digest=sha256_hex(canonical_json_bytes(mutation)),
        audit_observation_digest=sha256_hex(canonical_json_bytes(audit)),
    )


class CollectorBinding(StrictContractModel):
    fact_kind: str = Field(pattern=IDENTIFIER_PATTERN)
    source_system: str = Field(pattern=IDENTIFIER_PATTERN)
    collector_identity: Literal["pg-source-collector"] = "pg-source-collector"
    maximum_age_seconds: int = Field(ge=1, le=2_592_000)
    completeness_rule: str = Field(min_length=1, max_length=1024)
    source_query_schema: str = Field(pattern=IDENTIFIER_PATTERN)


class SourceCollectorRegistry(StrictContractModel):
    schema_version: Literal["workchord-source-collector-registry-v1"] = (
        "workchord-source-collector-registry-v1"
    )
    registry_revision: int = Field(ge=1)
    bindings: tuple[CollectorBinding, ...] = Field(min_length=1, max_length=2048)

    @model_validator(mode="after")
    def unique_facts(self) -> "SourceCollectorRegistry":
        facts = [item.fact_kind for item in self.bindings]
        if len(set(facts)) != len(facts):
            raise ValueError("Every source fact must have exactly one collector binding")
        return self

    def require(self, required_fact_kinds: set[str]) -> None:
        present = {item.fact_kind for item in self.bindings}
        missing = sorted(required_fact_kinds - present)
        if missing:
            raise ValueError(f"Collector registry is incomplete: {missing}")


class MetricSample(StrictContractModel):
    sampled_at: datetime
    value: float
    counter_generation: str = Field(min_length=1, max_length=255)

    @field_validator("sampled_at")
    @classmethod
    def aware_sample(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Metric samples must be timezone-aware")
        return value


class CompleteMetricWindow(StrictContractModel):
    metric_key: str = Field(pattern=IDENTIFIER_PATTERN)
    starts_at: datetime
    ends_at: datetime
    expected_interval_seconds: int = Field(ge=1, le=3600)
    maximum_gap_seconds: int = Field(ge=1, le=7200)
    samples: tuple[MetricSample, ...] = Field(min_length=2, max_length=2_000_000)

    @model_validator(mode="after")
    def complete_window(self) -> "CompleteMetricWindow":
        if (
            self.starts_at.tzinfo is None
            or self.starts_at.utcoffset() is None
            or self.ends_at.tzinfo is None
            or self.ends_at.utcoffset() is None
        ):
            raise ValueError("Metric window times must be timezone-aware")
        if self.ends_at <= self.starts_at:
            raise ValueError("Metric window is empty")
        ordered = tuple(sorted(self.samples, key=lambda item: item.sampled_at))
        if ordered != self.samples:
            raise ValueError("Metric samples must be time ordered")
        if ordered[0].sampled_at > self.starts_at or ordered[-1].sampled_at < self.ends_at:
            raise ValueError("Metric samples do not cover the requested bounds")
        generations = {item.counter_generation for item in ordered}
        if len(generations) != 1:
            raise ValueError("Metric counter reset/generation changed inside the window")
        for previous, current in zip(ordered, ordered[1:], strict=False):
            if (current.sampled_at - previous.sampled_at).total_seconds() > self.maximum_gap_seconds:
                raise ValueError("Metric window contains an unobserved gap")
        return self


class ReplicaMembershipObservation(StrictContractModel):
    expected_members: tuple[str, ...] = Field(min_length=1, max_length=1024)
    observed_members: tuple[str, ...] = Field(min_length=1, max_length=1024)
    scheduler_membership_digest: str = Field(pattern=SHA256_PATTERN)
    connection_ownership_digest: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def complete_membership(self) -> "ReplicaMembershipObservation":
        if len(set(self.expected_members)) != len(self.expected_members):
            raise ValueError("Expected replica membership contains duplicates")
        if len(set(self.observed_members)) != len(self.observed_members):
            raise ValueError("Observed replica membership contains duplicates")
        if set(self.expected_members) != set(self.observed_members):
            missing = sorted(set(self.expected_members) - set(self.observed_members))
            extra = sorted(set(self.observed_members) - set(self.expected_members))
            raise ValueError(f"Replica membership mismatch; missing={missing}, extra={extra}")
        return self
