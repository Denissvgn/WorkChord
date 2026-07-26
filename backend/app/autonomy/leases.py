"""Short-lived exact-target action leases parented to durable attempt starts."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from collections.abc import Callable
from typing import Literal

from pydantic import Field, model_validator

from app.autonomy.canonical import StrictContractModel, canonical_json_bytes, sha256_hex
from app.autonomy.contracts.charter import AutonomyCharter, ExactResourceBinding
from app.autonomy.evidence import (
    AttemptEventType,
    AttemptLedgerBackend,
    AttemptLedgerRecord,
    ZERO_DIGEST,
    validate_attempt_ledger_snapshot,
)
from app.autonomy.signing import (
    DetachedSignatureEnvelope,
    PublicTrustResolver,
    RemoteSigner,
    verify_detached_signature,
)


SHA256_PATTERN = r"^[0-9a-f]{64}$"
IDENTIFIER_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9._:-]{0,254}$"
OPAQUE_REF_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9._:/@+-]{2,2047}$"


class ActionLeaseRequest(StrictContractModel):
    run_id: str = Field(pattern=IDENTIFIER_PATTERN)
    task_id: str = Field(pattern=IDENTIFIER_PATTERN)
    stage_id: str = Field(pattern=IDENTIFIER_PATTERN)
    action: str = Field(min_length=1, max_length=255)
    environment: Literal["ephemeral", "rehearsal", "production"]
    destructive: bool = False
    resource_logical_key: str = Field(pattern=IDENTIFIER_PATTERN)
    resource_ref: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=2048)
    resource_generation: str = Field(min_length=1, max_length=255)
    topology_revision: int = Field(ge=1)
    attempt_id: int = Field(ge=1)
    attempt_start_digest: str = Field(pattern=SHA256_PATTERN)
    attempt_start_sequence: int = Field(ge=1)
    ledger_head_at_request: str = Field(pattern=SHA256_PATTERN)
    requested_ttl_seconds: int = Field(ge=1, le=3600)
    maximum_calls: int = Field(ge=1, le=100)
    budget_minor_units: int = Field(ge=0)
    nonce: str = Field(pattern=IDENTIFIER_PATTERN)
    lease_mode: Literal["bootstrap-revalidation", "autonomous"]
    autonomy_qualified_report_digest: str | None = Field(
        default=None, pattern=SHA256_PATTERN
    )

    @model_validator(mode="after")
    def qualification_binding(self) -> "ActionLeaseRequest":
        if self.action == "*" or self.action.endswith(".*"):
            raise ValueError("Action lease requires an exact action")
        if self.environment == "production" and self.lease_mode != "autonomous":
            raise ValueError("Bootstrap-revalidation leases cannot target production")
        if self.environment == "production" and self.destructive:
            raise ValueError("Destructive production action leases are forbidden")
        if self.lease_mode == "autonomous" and not self.autonomy_qualified_report_digest:
            raise ValueError("Autonomous leases require an AUT-ADV-001 report digest")
        if (
            self.lease_mode == "bootstrap-revalidation"
            and self.task_id
            not in {"AUT-GOV-001", "AUT-BOOT-001", "AUT-IAM-001", "AUT-EVD-001", "AUT-ORCH-001"}
        ):
            raise ValueError("Bootstrap revalidation lease is limited to the serial tranche")
        return self


class ActionLease(StrictContractModel):
    schema_version: Literal["workchord-action-lease-v1"] = (
        "workchord-action-lease-v1"
    )
    lease_id: str = Field(pattern=SHA256_PATTERN)
    run_id: str = Field(pattern=IDENTIFIER_PATTERN)
    task_id: str = Field(pattern=IDENTIFIER_PATTERN)
    stage_id: str = Field(pattern=IDENTIFIER_PATTERN)
    action: str = Field(min_length=1, max_length=255)
    environment: Literal["ephemeral", "rehearsal", "production"]
    destructive: bool
    release_fingerprint: str = Field(pattern=SHA256_PATTERN)
    charter_digest: str = Field(pattern=SHA256_PATTERN)
    contract_manifest_digest: str = Field(pattern=SHA256_PATTERN)
    resource_logical_key: str = Field(pattern=IDENTIFIER_PATTERN)
    resource_ref: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=2048)
    resource_generation: str = Field(min_length=1, max_length=255)
    topology_revision: int = Field(ge=1)
    attempt_id: int = Field(ge=1)
    attempt_start_digest: str = Field(pattern=SHA256_PATTERN)
    attempt_start_sequence: int = Field(ge=1)
    ledger_head_at_issue: str = Field(pattern=SHA256_PATTERN)
    issued_at: datetime
    expires_at: datetime
    maximum_calls: int = Field(ge=1, le=100)
    budget_minor_units: int = Field(ge=0)
    nonce: str = Field(pattern=IDENTIFIER_PATTERN)
    lease_mode: Literal["bootstrap-revalidation", "autonomous"]
    autonomy_qualified_report_digest: str | None = Field(
        default=None, pattern=SHA256_PATTERN
    )

    @model_validator(mode="after")
    def valid_lease(self) -> "ActionLease":
        if self.issued_at.tzinfo is None or self.expires_at.tzinfo is None:
            raise ValueError("Lease timestamps must be timezone-aware")
        if self.expires_at <= self.issued_at:
            raise ValueError("Lease expiry must follow issue time")
        if self.environment == "production" and self.lease_mode != "autonomous":
            raise ValueError("Bootstrap-revalidation leases cannot target production")
        if self.environment == "production" and self.destructive:
            raise ValueError("Destructive production action leases are forbidden")
        if self.lease_mode == "autonomous" and not self.autonomy_qualified_report_digest:
            raise ValueError("Autonomous leases require an AUT-ADV-001 report digest")
        identity = self.model_dump(mode="json", exclude={"lease_id"})
        expected = sha256_hex(identity)
        if self.lease_id != expected:
            raise ValueError("lease_id does not match the canonical lease")
        return self


class SignedActionLease(StrictContractModel):
    lease: ActionLease
    signature: DetachedSignatureEnvelope


class ActionLeasePolicy:
    """Non-generative issuer that cannot invent authority or attempt ancestry."""

    def __init__(
        self,
        *,
        charter: AutonomyCharter,
        charter_digest: str,
        contract_manifest_digest: str,
        release_fingerprint: str,
        ledger_backend: AttemptLedgerBackend,
        signer: RemoteSigner,
        signing_key_ref: str,
        signing_subject: str = "pg-action-policy",
        clock: Callable[[], datetime] = lambda: datetime.now(UTC),
    ) -> None:
        if sha256_hex(canonical_json_bytes(charter)) != charter_digest:
            raise ValueError("Charter digest does not match the supplied charter")
        self._charter = charter
        self._charter_digest = charter_digest
        self._contract_manifest_digest = contract_manifest_digest
        self._release_fingerprint = release_fingerprint
        self._ledger_backend = ledger_backend
        self._signer = signer
        self._signing_key_ref = signing_key_ref
        self._signing_subject = signing_subject
        self._clock = clock

    def issue(self, request: ActionLeaseRequest) -> SignedActionLease:
        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise ValueError("Trusted clock must be timezone-aware")
        if not (self._charter.valid_from <= now < self._charter.expires_at):
            raise ValueError("Charter is not currently valid")
        resource = self._resolve_resource(request)
        start, head = self._resolve_attempt_start(request)
        if start.run_id != request.run_id or start.task_id != request.task_id:
            raise ValueError("Attempt start belongs to another run or task")
        if start.stage_id != request.stage_id:
            raise ValueError("Attempt start belongs to another stage")
        if start.action_id != request.action:
            raise ValueError("Attempt start belongs to another action")
        if start.release_fingerprint != self._release_fingerprint:
            raise ValueError("Attempt start belongs to another release")
        if start.charter_digest != self._charter_digest:
            raise ValueError("Attempt start belongs to another charter")
        if start.contract_manifest_digest != self._contract_manifest_digest:
            raise ValueError("Attempt start belongs to another contract")
        if request.budget_minor_units > self._charter.budget.maximum_spend_minor_units:
            raise ValueError("Action lease exceeds the charter budget")
        if request.maximum_calls > min(
            self._charter.budget.maximum_api_calls,
            self._charter.budget.maximum_mutations,
        ):
            raise ValueError("Action lease call count exceeds the charter budget")
        if request.environment == "production" and not self._charter.production_mutation_allowed:
            raise ValueError("The charter does not permit production mutation")
        windows = [
            item
            for item in self._charter.execution_windows
            if item.starts_at <= now < item.ends_at
            and request.stage_id in item.permitted_stages
        ]
        if len(windows) != 1:
            raise ValueError("Action stage has no unambiguous active execution window")
        expires_at = min(
            now + timedelta(seconds=request.requested_ttl_seconds),
            self._charter.expires_at,
            windows[0].ends_at,
        )
        lease_values = {
            "schema_version": "workchord-action-lease-v1",
            "run_id": request.run_id,
            "task_id": request.task_id,
            "stage_id": request.stage_id,
            "action": request.action,
            "environment": request.environment,
            "destructive": request.destructive,
            "release_fingerprint": self._release_fingerprint,
            "charter_digest": self._charter_digest,
            "contract_manifest_digest": self._contract_manifest_digest,
            "resource_logical_key": resource.logical_key,
            "resource_ref": resource.resource_ref,
            "resource_generation": resource.generation,
            "topology_revision": request.topology_revision,
            "attempt_id": request.attempt_id,
            "attempt_start_digest": start.digest(),
            "attempt_start_sequence": start.sequence,
            "ledger_head_at_issue": head,
            "issued_at": now,
            "expires_at": expires_at,
            "maximum_calls": request.maximum_calls,
            "budget_minor_units": request.budget_minor_units,
            "nonce": request.nonce,
            "lease_mode": request.lease_mode,
            "autonomy_qualified_report_digest": request.autonomy_qualified_report_digest,
        }
        preliminary = ActionLease.model_construct(
            lease_id="0" * 64,
            **lease_values,
        )
        unsigned = preliminary.model_dump(mode="json", exclude={"lease_id"})
        lease = ActionLease(lease_id=sha256_hex(unsigned), **lease_values)
        signature = self._signer.sign_digest(
            payload_sha256=sha256_hex(canonical_json_bytes(lease)),
            key_ref=self._signing_key_ref,
            subject=self._signing_subject,
        )
        if signature.subject != self._signing_subject:
            raise ValueError("Remote signer returned another subject")
        return SignedActionLease(lease=lease, signature=signature)

    def _resolve_resource(self, request: ActionLeaseRequest) -> ExactResourceBinding:
        matches = [
            item
            for item in self._charter.resources
            if item.logical_key == request.resource_logical_key
        ]
        if len(matches) != 1:
            raise ValueError("Action resource is not uniquely chartered")
        resource = matches[0]
        if resource.resource_ref != request.resource_ref:
            raise ValueError("Action targets the wrong resource")
        if resource.generation != request.resource_generation:
            raise ValueError("Action targets a stale resource generation")
        if request.action not in resource.allowed_operations:
            raise ValueError("Action is not permitted for the resource")
        return resource

    def _resolve_attempt_start(
        self, request: ActionLeaseRequest
    ) -> tuple[AttemptLedgerRecord, str]:
        snapshot = validate_attempt_ledger_snapshot(self._ledger_backend.read())
        if snapshot.head_digest != request.ledger_head_at_request:
            raise ValueError("Attempt ledger head changed; refresh the lease request")
        matches = [
            item
            for item in snapshot.records
            if item.attempt_id == request.attempt_id
            and item.event_type == AttemptEventType.STARTED
        ]
        if len(matches) != 1:
            raise ValueError("Action lease requires exactly one durable attempt start")
        start = matches[0]
        if start.digest() != request.attempt_start_digest:
            raise ValueError("Attempt start digest mismatch")
        if start.sequence != request.attempt_start_sequence:
            raise ValueError("Attempt start sequence mismatch")
        return start, snapshot.head_digest


def verify_action_lease(
    signed: SignedActionLease,
    *,
    trust_resolver: PublicTrustResolver,
    ledger_backend: AttemptLedgerBackend,
    expected_action: str,
    expected_environment: Literal["ephemeral", "rehearsal", "production"],
    expected_destructive: bool,
    expected_resource_ref: str,
    expected_resource_generation: str,
    now: datetime,
) -> ActionLease:
    """Adapter-side verification before any provider mutation."""

    verify_detached_signature(
        canonical_json_bytes(signed.lease), signed.signature, trust_resolver
    )
    lease = signed.lease
    if signed.signature.subject != "pg-action-policy":
        raise ValueError("Only pg-action-policy may sign action leases")
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("Lease verification clock must be timezone-aware")
    if not (lease.issued_at <= now < lease.expires_at):
        raise ValueError("Action lease is not currently valid")
    if lease.action != expected_action:
        raise ValueError("Action lease operation mismatch")
    if lease.environment != expected_environment:
        raise ValueError("Action lease environment mismatch")
    if lease.destructive != expected_destructive:
        raise ValueError("Action lease destructive flag mismatch")
    if lease.resource_ref != expected_resource_ref:
        raise ValueError("Action lease resource mismatch")
    if lease.resource_generation != expected_resource_generation:
        raise ValueError("Action lease resource generation mismatch")
    snapshot = validate_attempt_ledger_snapshot(ledger_backend.read())
    starts = [
        item
        for item in snapshot.records
        if item.sequence == lease.attempt_start_sequence
        and item.attempt_id == lease.attempt_id
        and item.event_type == AttemptEventType.STARTED
    ]
    if len(starts) != 1 or starts[0].digest() != lease.attempt_start_digest:
        raise ValueError("Action lease attempt start cannot be resolved")
    start = starts[0]
    if (
        start.run_id != lease.run_id
        or start.task_id != lease.task_id
        or start.stage_id != lease.stage_id
        or start.action_id != lease.action
        or start.release_fingerprint != lease.release_fingerprint
        or start.charter_digest != lease.charter_digest
        or start.contract_manifest_digest != lease.contract_manifest_digest
    ):
        raise ValueError("Action lease identity differs from its durable attempt start")
    if lease.ledger_head_at_issue not in {
        ZERO_DIGEST,
        *(item.digest() for item in snapshot.records),
    }:
        raise ValueError("Action lease issue head is not in the durable ledger ancestry")
    closed_events = {
        AttemptEventType.FAILED,
        AttemptEventType.STOPPED,
        AttemptEventType.RESET,
        AttemptEventType.EVALUATED,
        AttemptEventType.FINAL,
    }
    if any(
        item.attempt_id == lease.attempt_id and item.event_type in closed_events
        for item in snapshot.records
    ):
        raise ValueError("Action lease attempt is already closed")
    return lease
