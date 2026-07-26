"""Source-attested evidence envelopes and append-only attempt coordination."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from enum import StrEnum
from collections.abc import Callable
from typing import Any, Literal, Protocol, runtime_checkable

from pydantic import Field, field_validator, model_validator

from app.autonomy.canonical import (
    StrictContractModel,
    canonical_json_bytes,
    ensure_secret_free,
    sha256_hex,
)
from app.autonomy.signing import (
    DetachedSignatureEnvelope,
    PublicTrustResolver,
    verify_detached_signature,
)


SHA256_PATTERN = r"^[0-9a-f]{64}$"
IDENTIFIER_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9._:-]{0,254}$"
OPAQUE_REF_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9._:/@+-]{2,2047}$"
ZERO_DIGEST = "0" * 64


class RedactionClass(StrEnum):
    RESTRICTED_TOPOLOGY = "restricted-topology"
    INTERNAL = "internal"
    PUBLIC = "public"


class AutonomousEvidence(StrictContractModel):
    """Unsigned canonical source observation submitted to a remote signer."""

    schema_version: Literal["workchord-autonomous-evidence-v1"] = (
        "workchord-autonomous-evidence-v1"
    )
    run_id: str = Field(pattern=IDENTIFIER_PATTERN)
    task_id: str = Field(pattern=IDENTIFIER_PATTERN)
    stage_id: str = Field(pattern=IDENTIFIER_PATTERN)
    action_id: str = Field(pattern=IDENTIFIER_PATTERN)
    release_fingerprint: str = Field(pattern=SHA256_PATTERN)
    charter_digest: str = Field(pattern=SHA256_PATTERN)
    contract_manifest_digest: str = Field(pattern=SHA256_PATTERN)
    issuer_workload_identity: str = Field(min_length=1, max_length=512)
    issuer_role: str = Field(pattern=IDENTIFIER_PATTERN)
    source_system: str = Field(pattern=IDENTIFIER_PATTERN)
    source_resource_ref: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=2048)
    source_resource_generation: str = Field(min_length=1, max_length=255)
    source_receipt_ref: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=2048)
    request_digest: str = Field(pattern=SHA256_PATTERN)
    idempotency_digest: str = Field(pattern=SHA256_PATTERN)
    observed_started_at: datetime
    observed_ended_at: datetime
    clock_source_ref: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=2048)
    query_digest: str = Field(pattern=SHA256_PATTERN)
    exit_code: int | None = Field(default=None, ge=0, le=255)
    source_outcome: Literal["succeeded", "failed", "stopped", "unavailable"]
    raw_artifact_uri: str = Field(pattern=OPAQUE_REF_PATTERN, max_length=2048)
    raw_artifact_sha256: str = Field(pattern=SHA256_PATTERN)
    parent_hashes: tuple[str, ...] = Field(default=(), max_length=256)
    ledger_sequence: int = Field(ge=1)
    previous_hash: str = Field(pattern=SHA256_PATTERN)
    redaction_class: RedactionClass

    @field_validator("observed_started_at", "observed_ended_at")
    @classmethod
    def aware_times(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Evidence timestamps must be timezone-aware")
        return value

    @field_validator("parent_hashes")
    @classmethod
    def unique_parents(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(set(value)) != len(value):
            raise ValueError("Evidence parent hashes must be unique")
        if any(len(item) != 64 or any(char not in "0123456789abcdef" for char in item) for item in value):
            raise ValueError("Evidence parents must be lowercase SHA-256 digests")
        return tuple(sorted(value))

    @model_validator(mode="after")
    def source_envelope(self) -> "AutonomousEvidence":
        if self.observed_ended_at < self.observed_started_at:
            raise ValueError("Evidence end time precedes its start time")
        if self.ledger_sequence == 1 and self.previous_hash != ZERO_DIGEST:
            raise ValueError("The first evidence record must use the zero parent")
        if self.ledger_sequence > 1 and self.previous_hash == ZERO_DIGEST:
            raise ValueError("Non-genesis evidence requires a previous hash")
        ensure_secret_free(self.model_dump(mode="json"))
        return self

    def digest(self) -> str:
        return sha256_hex(canonical_json_bytes(self))


class SignedAutonomousEvidence(StrictContractModel):
    evidence: AutonomousEvidence
    signature: DetachedSignatureEnvelope

    def digest(self) -> str:
        return sha256_hex(canonical_json_bytes(self))


@runtime_checkable
class WormObjectStore(Protocol):
    """Charter-selected immutable store; implementations must enforce WORM."""

    def put_if_absent(
        self, *, object_key: str, payload: bytes, redaction_class: RedactionClass
    ) -> None: ...

    def get(self, *, object_key: str) -> bytes: ...

    def ordered_keys(self, *, prefix: str) -> tuple[str, ...]: ...


class EvidenceResolutionError(ValueError):
    pass


class EvidenceResolver:
    """Resolve immutable evidence and verify trust/provenance bindings."""

    def __init__(
        self,
        *,
        store: WormObjectStore,
        trust_resolver: PublicTrustResolver,
        clock: Callable[[], datetime] = lambda: datetime.now(UTC),
    ) -> None:
        self._store = store
        self._trust_resolver = trust_resolver
        self._clock = clock

    def resolve(
        self,
        object_digest: str,
        *,
        expected_release_fingerprint: str,
        expected_charter_digest: str,
        expected_contract_manifest_digest: str,
        expected_issuer_roles: set[str],
        expected_source_system: str,
        maximum_age: timedelta,
    ) -> SignedAutonomousEvidence:
        _validate_digest(object_digest, "object_digest")
        try:
            payload = self._store.get(object_key=object_digest)
        except Exception as exc:
            raise EvidenceResolutionError("Evidence object is unavailable") from exc
        if sha256_hex(payload) != object_digest:
            raise EvidenceResolutionError("Evidence object digest mismatch")
        try:
            signed = SignedAutonomousEvidence.model_validate_json(payload)
        except Exception as exc:
            raise EvidenceResolutionError("Evidence object schema is invalid") from exc
        evidence_bytes = canonical_json_bytes(signed.evidence)
        try:
            verify_detached_signature(
                evidence_bytes, signed.signature, self._trust_resolver
            )
        except Exception as exc:
            raise EvidenceResolutionError("Evidence signature is invalid") from exc
        evidence = signed.evidence
        if signed.signature.subject != evidence.issuer_workload_identity:
            raise EvidenceResolutionError("Evidence signer does not match workload identity")
        if evidence.release_fingerprint != expected_release_fingerprint:
            raise EvidenceResolutionError("Evidence belongs to another release")
        if evidence.charter_digest != expected_charter_digest:
            raise EvidenceResolutionError("Evidence belongs to another charter")
        if evidence.contract_manifest_digest != expected_contract_manifest_digest:
            raise EvidenceResolutionError("Evidence uses another contract")
        if evidence.issuer_role not in expected_issuer_roles:
            raise EvidenceResolutionError("Evidence issuer role is not eligible")
        if evidence.source_system != expected_source_system:
            raise EvidenceResolutionError("Evidence uses the wrong source system")
        now = self._clock()
        if now.tzinfo is None or now.utcoffset() is None:
            raise EvidenceResolutionError("Trusted clock returned a naive timestamp")
        age = now - evidence.observed_ended_at.astimezone(UTC)
        if age < timedelta(0) or age > maximum_age:
            raise EvidenceResolutionError("Evidence is stale or future-dated")
        if evidence.previous_hash != ZERO_DIGEST:
            previous = self._resolve_linked_evidence(
                evidence.previous_hash,
                child=evidence,
            )
            if previous.evidence.ledger_sequence != evidence.ledger_sequence - 1:
                raise EvidenceResolutionError("Evidence previous record is not contiguous")
        for parent_digest in evidence.parent_hashes:
            parent = self._resolve_linked_evidence(parent_digest, child=evidence)
            if parent.evidence.ledger_sequence >= evidence.ledger_sequence:
                raise EvidenceResolutionError("Evidence parent does not precede its child")
        return signed

    def _resolve_linked_evidence(
        self,
        object_digest: str,
        *,
        child: AutonomousEvidence,
    ) -> SignedAutonomousEvidence:
        try:
            payload = self._store.get(object_key=object_digest)
        except Exception as exc:
            raise EvidenceResolutionError("Evidence parent is unavailable") from exc
        if sha256_hex(payload) != object_digest:
            raise EvidenceResolutionError("Evidence parent digest mismatch")
        try:
            signed = SignedAutonomousEvidence.model_validate_json(payload)
            verify_detached_signature(
                canonical_json_bytes(signed.evidence),
                signed.signature,
                self._trust_resolver,
            )
        except Exception as exc:
            raise EvidenceResolutionError("Evidence parent signature/schema is invalid") from exc
        parent = signed.evidence
        if signed.signature.subject != parent.issuer_workload_identity:
            raise EvidenceResolutionError("Evidence parent signer identity mismatch")
        if (
            parent.run_id != child.run_id
            or parent.release_fingerprint != child.release_fingerprint
            or parent.charter_digest != child.charter_digest
            or parent.contract_manifest_digest != child.contract_manifest_digest
        ):
            raise EvidenceResolutionError("Evidence parent belongs to another run/contract")
        return signed


class AttemptEventType(StrEnum):
    ALLOCATED = "allocated"
    STARTED = "started"
    CHECKPOINT = "checkpoint"
    FAILED = "failed"
    STOPPED = "stopped"
    RESET = "reset"
    EVALUATED = "evaluated"
    FINAL = "final"


class AttemptLedgerRecord(StrictContractModel):
    schema_version: Literal["workchord-attempt-ledger-record-v1"] = (
        "workchord-attempt-ledger-record-v1"
    )
    attempt_id: int = Field(ge=1)
    sequence: int = Field(ge=1)
    event_type: AttemptEventType
    run_id: str = Field(pattern=IDENTIFIER_PATTERN)
    task_id: str = Field(pattern=IDENTIFIER_PATTERN)
    stage_id: str = Field(pattern=IDENTIFIER_PATTERN)
    action_id: str = Field(pattern=IDENTIFIER_PATTERN)
    release_fingerprint: str = Field(pattern=SHA256_PATTERN)
    charter_digest: str = Field(pattern=SHA256_PATTERN)
    contract_manifest_digest: str = Field(pattern=SHA256_PATTERN)
    recorded_at: datetime
    previous_hash: str = Field(pattern=SHA256_PATTERN)
    evidence_digest: str | None = Field(default=None, pattern=SHA256_PATTERN)
    normalized_reason_code: str | None = Field(
        default=None, pattern=IDENTIFIER_PATTERN
    )

    @field_validator("recorded_at")
    @classmethod
    def aware_recorded_at(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Ledger timestamps must be timezone-aware")
        return value

    @model_validator(mode="after")
    def valid_parent(self) -> "AttemptLedgerRecord":
        if self.sequence == 1 and self.previous_hash != ZERO_DIGEST:
            raise ValueError("Ledger genesis must use the zero parent")
        if self.sequence > 1 and self.previous_hash == ZERO_DIGEST:
            raise ValueError("Non-genesis ledger records require a parent")
        if self.event_type == AttemptEventType.ALLOCATED and self.evidence_digest:
            raise ValueError("Allocation cannot claim evidence before work starts")
        if self.event_type in {
            AttemptEventType.CHECKPOINT,
            AttemptEventType.EVALUATED,
        } and not self.evidence_digest:
            raise ValueError("Checkpoint/evaluation records require evidence")
        if self.event_type in {
            AttemptEventType.FAILED,
            AttemptEventType.STOPPED,
            AttemptEventType.RESET,
        } and not self.normalized_reason_code:
            raise ValueError("Failure/stop/reset records require a normalized reason")
        return self

    def digest(self) -> str:
        return sha256_hex(canonical_json_bytes(self))


class AttemptLedgerSnapshot(StrictContractModel):
    revision: int = Field(ge=0)
    head_digest: str = Field(pattern=SHA256_PATTERN)
    records: tuple[AttemptLedgerRecord, ...] = Field(default=(), max_length=1_000_000)


@runtime_checkable
class AttemptLedgerBackend(Protocol):
    """External CAS ledger physically independent of WorkChord PostgreSQL."""

    def read(self) -> AttemptLedgerSnapshot: ...

    def compare_and_append(
        self,
        *,
        expected_revision: int,
        expected_head_digest: str,
        record: AttemptLedgerRecord,
    ) -> bool: ...


class AttemptLedgerConflict(RuntimeError):
    pass


class AttemptLedger:
    """Allocate attempt numbers and append every lifecycle fact before action."""

    _TERMINAL = {AttemptEventType.FINAL}

    def __init__(
        self,
        *,
        backend: AttemptLedgerBackend,
        clock: Callable[[], datetime] = lambda: datetime.now(UTC),
        maximum_cas_attempts: int = 8,
    ) -> None:
        if maximum_cas_attempts < 1 or maximum_cas_attempts > 100:
            raise ValueError("maximum_cas_attempts must be between 1 and 100")
        self._backend = backend
        self._clock = clock
        self._maximum_cas_attempts = maximum_cas_attempts

    def allocate(
        self,
        *,
        run_id: str,
        task_id: str,
        stage_id: str,
        action_id: str,
        release_fingerprint: str,
        charter_digest: str,
        contract_manifest_digest: str,
    ) -> AttemptLedgerRecord:
        for _ in range(self._maximum_cas_attempts):
            snapshot = self._validated_snapshot()
            attempt_id = (
                max((record.attempt_id for record in snapshot.records), default=0) + 1
            )
            record = AttemptLedgerRecord(
                attempt_id=attempt_id,
                sequence=len(snapshot.records) + 1,
                event_type=AttemptEventType.ALLOCATED,
                run_id=run_id,
                task_id=task_id,
                stage_id=stage_id,
                action_id=action_id,
                release_fingerprint=release_fingerprint,
                charter_digest=charter_digest,
                contract_manifest_digest=contract_manifest_digest,
                recorded_at=self._clock(),
                previous_hash=snapshot.head_digest,
            )
            if self._backend.compare_and_append(
                expected_revision=snapshot.revision,
                expected_head_digest=snapshot.head_digest,
                record=record,
            ):
                return record
        raise AttemptLedgerConflict("Attempt allocation exhausted CAS retries")

    def append(
        self,
        *,
        attempt_id: int,
        event_type: AttemptEventType,
        evidence_digest: str | None = None,
        normalized_reason_code: str | None = None,
    ) -> AttemptLedgerRecord:
        if event_type == AttemptEventType.ALLOCATED:
            raise ValueError("Use allocate() so callers cannot select attempt IDs")
        for _ in range(self._maximum_cas_attempts):
            snapshot = self._validated_snapshot()
            attempt_records = [
                record for record in snapshot.records if record.attempt_id == attempt_id
            ]
            if not attempt_records:
                raise ValueError("Attempt was not durably allocated")
            self._validate_transition(attempt_records, event_type)
            origin = attempt_records[0]
            record = AttemptLedgerRecord(
                attempt_id=attempt_id,
                sequence=len(snapshot.records) + 1,
                event_type=event_type,
                run_id=origin.run_id,
                task_id=origin.task_id,
                stage_id=origin.stage_id,
                action_id=origin.action_id,
                release_fingerprint=origin.release_fingerprint,
                charter_digest=origin.charter_digest,
                contract_manifest_digest=origin.contract_manifest_digest,
                recorded_at=self._clock(),
                previous_hash=snapshot.head_digest,
                evidence_digest=evidence_digest,
                normalized_reason_code=normalized_reason_code,
            )
            if self._backend.compare_and_append(
                expected_revision=snapshot.revision,
                expected_head_digest=snapshot.head_digest,
                record=record,
            ):
                return record
        raise AttemptLedgerConflict("Attempt append exhausted CAS retries")

    def start(self, *, attempt_id: int) -> AttemptLedgerRecord:
        return self.append(attempt_id=attempt_id, event_type=AttemptEventType.STARTED)

    def _validated_snapshot(self) -> AttemptLedgerSnapshot:
        snapshot = self._backend.read()
        return validate_attempt_ledger_snapshot(snapshot)

    @staticmethod
    def _validate_transition(
        records: list[AttemptLedgerRecord], event_type: AttemptEventType
    ) -> None:
        events = [record.event_type for record in records]
        if AttemptEventType.FINAL in events:
            raise ValueError("Finalized attempts are immutable")
        last = events[-1]
        allowed: dict[AttemptEventType, set[AttemptEventType]] = {
            AttemptEventType.ALLOCATED: {
                AttemptEventType.STARTED,
                AttemptEventType.STOPPED,
            },
            AttemptEventType.STARTED: {
                AttemptEventType.CHECKPOINT,
                AttemptEventType.FAILED,
                AttemptEventType.STOPPED,
            },
            AttemptEventType.CHECKPOINT: {
                AttemptEventType.CHECKPOINT,
                AttemptEventType.FAILED,
                AttemptEventType.STOPPED,
                AttemptEventType.EVALUATED,
            },
            AttemptEventType.FAILED: {AttemptEventType.EVALUATED},
            AttemptEventType.STOPPED: {AttemptEventType.EVALUATED},
            AttemptEventType.EVALUATED: {
                AttemptEventType.RESET,
                AttemptEventType.FINAL,
            },
            AttemptEventType.RESET: {AttemptEventType.FINAL},
            AttemptEventType.FINAL: set(),
        }
        if event_type not in allowed[last]:
            raise ValueError(
                f"Invalid attempt transition {last.value} -> {event_type.value}"
            )


def validate_attempt_ledger_snapshot(
    snapshot: AttemptLedgerSnapshot,
) -> AttemptLedgerSnapshot:
    """Replay and validate a complete externally supplied attempt-ledger snapshot."""

    expected_parent = ZERO_DIGEST
    histories: dict[int, list[AttemptLedgerRecord]] = {}
    previous_recorded_at: datetime | None = None
    for expected_sequence, record in enumerate(snapshot.records, start=1):
        if record.sequence != expected_sequence:
            raise ValueError("Attempt ledger contains a sequence gap")
        if record.previous_hash != expected_parent:
            raise ValueError("Attempt ledger parent chain is invalid")
        if previous_recorded_at is not None and record.recorded_at < previous_recorded_at:
            raise ValueError("Attempt ledger timestamps moved backwards")
        if record.event_type == AttemptEventType.ALLOCATED:
            if record.attempt_id in histories:
                raise ValueError("Attempt ID was allocated more than once")
            if record.attempt_id != len(histories) + 1:
                raise ValueError("Attempt allocations are not monotonic and contiguous")
            histories[record.attempt_id] = [record]
        else:
            history = histories.get(record.attempt_id)
            if history is None:
                raise ValueError("Attempt event precedes allocation")
            origin = history[0]
            if any(
                getattr(record, field_name) != getattr(origin, field_name)
                for field_name in (
                    "run_id",
                    "task_id",
                    "stage_id",
                    "action_id",
                    "release_fingerprint",
                    "charter_digest",
                    "contract_manifest_digest",
                )
            ):
                raise ValueError("Attempt event identity differs from its allocation")
            AttemptLedger._validate_transition(history, record.event_type)
            history.append(record)
        expected_parent = record.digest()
        previous_recorded_at = record.recorded_at
    if snapshot.revision != len(snapshot.records):
        raise ValueError("Attempt ledger revision does not match record count")
    if snapshot.head_digest != expected_parent:
        raise ValueError("Attempt ledger head does not match its records")
    return snapshot


def store_signed_evidence(
    store: WormObjectStore,
    signed: SignedAutonomousEvidence,
) -> str:
    """Put one exact signed envelope under its content digest."""

    payload = canonical_json_bytes(signed)
    object_digest = sha256_hex(payload)
    store.put_if_absent(
        object_key=object_digest,
        payload=payload,
        redaction_class=signed.evidence.redaction_class,
    )
    persisted = store.get(object_key=object_digest)
    if persisted != payload:
        raise ValueError("WORM store returned different bytes for an existing digest")
    return object_digest


def _validate_digest(value: str, field_name: str) -> None:
    if len(value) != 64 or any(char not in "0123456789abcdef" for char in value):
        raise ValueError(f"{field_name} must be a lowercase SHA-256 digest")
