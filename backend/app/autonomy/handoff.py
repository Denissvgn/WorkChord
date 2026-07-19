"""Deterministic, unpublished manual-handoff and closeout decision tooling."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Literal

from pydantic import Field, field_validator, model_validator

from app.autonomy.canonical import (
    StrictContractModel,
    canonical_json_bytes,
    ensure_secret_free,
    sha256_hex,
)
from app.autonomy.contracts.charter import ProgramDecision
from app.autonomy.evidence import (
    RedactionClass,
    SignedAutonomousEvidence,
    WormObjectStore,
)
from app.autonomy.signing import (
    DetachedSignatureEnvelope,
    PublicTrustResolver,
    RemoteSigner,
    verify_detached_signature,
)
from app.autonomy.status import StatusAmendmentLedger


SHA256_PATTERN = r"^[0-9a-f]{64}$"
IDENTIFIER_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9._:-]{0,254}$"


class AvailabilityState(StrEnum):
    PENDING = "pending"
    MET = "met"
    MISSED = "missed"


class RetentionState(StrEnum):
    RETAINED_NOT_DUE = "retained-not-due"
    DISPOSED = "disposed"
    OVERDUE = "overdue"


class ResolvedHandoffFact(StrictContractModel):
    """A resolver-produced source fact; prose/booleans cannot substitute."""

    fact_kind: str = Field(pattern=IDENTIFIER_PATTERN)
    object_digest: str = Field(pattern=SHA256_PATTERN)
    object_uri: str = Field(min_length=1, max_length=2048)
    evidence: SignedAutonomousEvidence

    @model_validator(mode="after")
    def exact_fact(self) -> "ResolvedHandoffFact":
        observed = self.evidence.evidence
        if self.object_digest != sha256_hex(canonical_json_bytes(self.evidence)):
            raise ValueError("Handoff fact digest does not match its envelope")
        if observed.action_id != self.fact_kind:
            raise ValueError("Handoff fact kind does not match signed source evidence")
        if observed.source_outcome != "succeeded":
            raise ValueError("Unsuccessful source evidence cannot enter a handoff")
        return self


class HandoffEvidenceReference(StrictContractModel):
    fact_kind: str = Field(pattern=IDENTIFIER_PATTERN)
    immutable_uri: str = Field(min_length=1, max_length=2048)
    object_digest: str = Field(pattern=SHA256_PATTERN)
    issuer_workload_identity: str = Field(min_length=1, max_length=512)
    issuer_role: str = Field(pattern=IDENTIFIER_PATTERN)
    source_system: str = Field(pattern=IDENTIFIER_PATTERN)
    source_generation: str = Field(min_length=1, max_length=255)


class CapacityClaimBoundary(StrictContractModel):
    opaque_browser_identities: Literal[1250] = 1250
    active_browser_sessions: Literal[250] = 250
    concurrent_mcp_agent_clients: Literal[200] = 200
    authenticated_people_claim_allowed: Literal[False] = False


class ManualPublicationHandoff(StrictContractModel):
    """Exact immutable bytes made available to a separate manual process."""

    schema_version: Literal["manual-publication-handoff-v1"] = (
        "manual-publication-handoff-v1"
    )
    publication_state: Literal["NOT-PUBLISHED"] = "NOT-PUBLISHED"
    publication_requirement: Literal["MANUAL-PUBLICATION-REQUIRED"] = (
        "MANUAL-PUBLICATION-REQUIRED"
    )
    release_fingerprint: str = Field(pattern=SHA256_PATTERN)
    charter_digest: str = Field(pattern=SHA256_PATTERN)
    contract_manifest_digest: str = Field(pattern=SHA256_PATTERN)
    production_record_digest: str = Field(pattern=SHA256_PATTERN)
    built_at: datetime
    valid_until: datetime
    availability_state: AvailabilityState
    retention_state: RetentionState
    availability_observation_ends_at: datetime
    retention_due_at: datetime
    capacity_boundary: CapacityClaimBoundary
    availability_claim_allowed: bool
    candidate_notes: str = Field(min_length=1, max_length=100_000)
    candidate_notes_sha256: str = Field(pattern=SHA256_PATTERN)
    evidence: tuple[HandoffEvidenceReference, ...] = Field(
        min_length=1, max_length=512
    )
    handoff_digest: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def immutable_boundary(self) -> "ManualPublicationHandoff":
        for timestamp in (
            self.built_at,
            self.valid_until,
            self.availability_observation_ends_at,
            self.retention_due_at,
        ):
            if timestamp.tzinfo is None or timestamp.utcoffset() is None:
                raise ValueError("Handoff timestamps must be timezone-aware")
        if self.valid_until <= self.built_at:
            raise ValueError("Handoff valid_until must follow build time")
        if self.candidate_notes_sha256 != sha256_hex(self.candidate_notes):
            raise ValueError("Candidate-note digest mismatch")
        if self.availability_claim_allowed != (
            self.availability_state == AvailabilityState.MET
        ):
            raise ValueError("Availability claims require a complete passing observation")
        fact_kinds = [item.fact_kind for item in self.evidence]
        if len(set(fact_kinds)) != len(fact_kinds):
            raise ValueError("Handoff evidence facts must be unique")
        unsigned = self.model_dump(mode="json", exclude={"handoff_digest"})
        if self.handoff_digest != sha256_hex(unsigned):
            raise ValueError("Handoff digest mismatch")
        ensure_secret_free(unsigned)
        return self


class HandoffVerification(StrictContractModel):
    schema_version: Literal["manual-publication-handoff-verification-v1"] = (
        "manual-publication-handoff-verification-v1"
    )
    handoff_digest: str = Field(pattern=SHA256_PATTERN)
    verifier_identity: Literal["pg-release-verifier"] = "pg-release-verifier"
    verified_at: datetime
    evidence_graph_digest: str = Field(pattern=SHA256_PATTERN)
    candidate_notes_sha256: str = Field(pattern=SHA256_PATTERN)
    conclusion: Literal["verified"] = "verified"

    @field_validator("verified_at")
    @classmethod
    def aware_verification_time(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("Handoff verification time must be timezone-aware")
        return value


class SignedHandoffVerification(StrictContractModel):
    verification: HandoffVerification
    signature: DetachedSignatureEnvelope


class CloseoutDecision(StrictContractModel):
    schema_version: Literal["workchord-postgresql-closeout-decision-v1"] = (
        "workchord-postgresql-closeout-decision-v1"
    )
    evaluator_identity: Literal["pg-closeout-evaluator"] = "pg-closeout-evaluator"
    evaluated_at: datetime
    valid_until: datetime
    decision: ProgramDecision
    handoff_digest: str = Field(pattern=SHA256_PATTERN)
    status_ledger_digest: str = Field(pattern=SHA256_PATTERN)
    availability_state: AvailabilityState
    retention_state: RetentionState
    blocker_codes: tuple[str, ...] = Field(max_length=512)
    manual_external_items: tuple[Literal["DBM-DOC-002", "G15"], ...] = (
        "DBM-DOC-002",
        "G15",
    )
    external_post_publication_items: tuple[Literal["DBM-CLOSE-001"], ...] = (
        "DBM-CLOSE-001",
    )
    decision_digest: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def deterministic_decision(self) -> "CloseoutDecision":
        if self.evaluated_at.tzinfo is None or self.valid_until.tzinfo is None:
            raise ValueError("Closeout timestamps must be timezone-aware")
        if self.valid_until <= self.evaluated_at:
            raise ValueError("Closeout decision is already expired")
        if self.decision == ProgramDecision.READY_FOR_MANUAL_PUBLICATION and self.blocker_codes:
            raise ValueError("A readiness decision cannot contain blockers")
        if self.decision == ProgramDecision.NO_SHIP and not self.blocker_codes:
            raise ValueError("NO-SHIP requires at least one blocker")
        unsigned = self.model_dump(mode="json", exclude={"decision_digest"})
        if self.decision_digest != sha256_hex(unsigned):
            raise ValueError("Closeout decision digest mismatch")
        return self


class SignedCloseoutDecision(StrictContractModel):
    decision: CloseoutDecision
    signature: DetachedSignatureEnvelope


_HANDOFF_REQUIRED_FACTS = {
    "production-cutover-record",
    "release-freeze-proof",
    "postcutover-runtime-proof",
    "handoff-input-integrity-proof",
}


def build_manual_publication_handoff(
    *,
    release_fingerprint: str,
    charter_digest: str,
    contract_manifest_digest: str,
    facts: tuple[ResolvedHandoffFact, ...],
    built_at: datetime,
    valid_until: datetime,
    availability_state: AvailabilityState,
    retention_state: RetentionState,
    availability_observation_ends_at: datetime,
    retention_due_at: datetime,
) -> ManualPublicationHandoff:
    """Render exact candidate notes; it cannot publish or imply publication."""

    by_kind = {item.fact_kind: item for item in facts}
    if len(by_kind) != len(facts):
        raise ValueError("Handoff facts must be unique")
    missing = sorted(_HANDOFF_REQUIRED_FACTS - set(by_kind))
    if missing:
        raise ValueError(f"Handoff is missing required source facts: {missing}")
    production = by_kind["production-cutover-record"].evidence.evidence
    if production.issuer_workload_identity != "pg-production-recorder":
        raise ValueError("Production record must be issued by pg-production-recorder")
    if production.release_fingerprint != release_fingerprint:
        raise ValueError("Production record belongs to another release")
    if production.charter_digest != charter_digest:
        raise ValueError("Production record belongs to another charter")
    if production.contract_manifest_digest != contract_manifest_digest:
        raise ValueError("Production record belongs to another contract")
    for fact in facts:
        evidence = fact.evidence.evidence
        if (
            evidence.release_fingerprint != release_fingerprint
            or evidence.charter_digest != charter_digest
            or evidence.contract_manifest_digest != contract_manifest_digest
        ):
            raise ValueError("Handoff facts do not share one release/charter/contract")
    if availability_state == AvailabilityState.MET:
        availability = by_kind.get("30-day-availability-proof")
        if availability is None or availability.evidence.evidence.issuer_workload_identity != "pg-availability-verifier":
            raise ValueError("A 99.9% claim requires the availability verifier proof")
    if availability_state == AvailabilityState.MISSED and "availability-missed-proof" not in by_kind:
        raise ValueError("Missed availability requires source evidence")
    if retention_state == RetentionState.DISPOSED and "sqlite-disposal-proof" not in by_kind:
        raise ValueError("Disposed retention state requires exact-digest absence proof")
    if retention_state == RetentionState.OVERDUE and "retention-overdue-proof" not in by_kind:
        raise ValueError("Overdue retention state requires trusted-time evidence")
    references = tuple(
        HandoffEvidenceReference(
            fact_kind=item.fact_kind,
            immutable_uri=item.object_uri,
            object_digest=item.object_digest,
            issuer_workload_identity=item.evidence.evidence.issuer_workload_identity,
            issuer_role=item.evidence.evidence.issuer_role,
            source_system=item.evidence.evidence.source_system,
            source_generation=item.evidence.evidence.source_resource_generation,
        )
        for item in sorted(facts, key=lambda item: item.fact_kind)
    )
    notes = _render_candidate_notes(
        release_fingerprint=release_fingerprint,
        availability_state=availability_state,
        retention_state=retention_state,
    )
    values = {
        "schema_version": "manual-publication-handoff-v1",
        "publication_state": "NOT-PUBLISHED",
        "publication_requirement": "MANUAL-PUBLICATION-REQUIRED",
        "release_fingerprint": release_fingerprint,
        "charter_digest": charter_digest,
        "contract_manifest_digest": contract_manifest_digest,
        "production_record_digest": by_kind["production-cutover-record"].object_digest,
        "built_at": built_at,
        "valid_until": valid_until,
        "availability_state": availability_state,
        "retention_state": retention_state,
        "availability_observation_ends_at": availability_observation_ends_at,
        "retention_due_at": retention_due_at,
        "capacity_boundary": CapacityClaimBoundary(),
        "availability_claim_allowed": availability_state == AvailabilityState.MET,
        "candidate_notes": notes,
        "candidate_notes_sha256": sha256_hex(notes),
        "evidence": references,
    }
    preliminary = ManualPublicationHandoff.model_construct(
        **values, handoff_digest="0" * 64
    )
    unsigned = preliminary.model_dump(mode="json", exclude={"handoff_digest"})
    return ManualPublicationHandoff(**values, handoff_digest=sha256_hex(unsigned))


def store_manual_publication_handoff(
    store: WormObjectStore,
    handoff: ManualPublicationHandoff,
) -> str:
    payload = canonical_json_bytes(handoff)
    digest = sha256_hex(payload)
    store.put_if_absent(
        object_key=digest,
        payload=payload,
        redaction_class=RedactionClass.INTERNAL,
    )
    if store.get(object_key=digest) != payload:
        raise ValueError("Immutable handoff storage returned different bytes")
    return digest


def sign_handoff_verification(
    handoff: ManualPublicationHandoff,
    *,
    signer: RemoteSigner,
    key_ref: str,
    verified_at: datetime,
) -> SignedHandoffVerification:
    graph_digest = sha256_hex(
        [item.object_digest for item in handoff.evidence]
    )
    verification = HandoffVerification(
        handoff_digest=handoff.handoff_digest,
        verified_at=verified_at,
        evidence_graph_digest=graph_digest,
        candidate_notes_sha256=handoff.candidate_notes_sha256,
    )
    signature = signer.sign_digest(
        payload_sha256=sha256_hex(canonical_json_bytes(verification)),
        key_ref=key_ref,
        subject="pg-release-verifier",
    )
    if signature.subject != "pg-release-verifier":
        raise ValueError("Remote signer returned another handoff-verifier subject")
    return SignedHandoffVerification(
        verification=verification,
        signature=signature,
    )


def evaluate_closeout(
    *,
    handoff: ManualPublicationHandoff,
    handoff_verification: SignedHandoffVerification,
    status_ledger: StatusAmendmentLedger,
    trust_resolver: PublicTrustResolver,
    evaluated_at: datetime,
) -> CloseoutDecision:
    """Derive current readiness/NO-SHIP without closing manual external items."""

    blockers: list[str] = []
    if evaluated_at.tzinfo is None or evaluated_at.utcoffset() is None:
        raise ValueError("Closeout evaluation time must be timezone-aware")
    if evaluated_at < handoff.built_at:
        blockers.append("closeout-predates-handoff")
    if evaluated_at >= handoff.valid_until:
        blockers.append("handoff-expired")
    verification = handoff_verification.verification
    try:
        verify_detached_signature(
            canonical_json_bytes(verification),
            handoff_verification.signature,
            trust_resolver,
        )
    except Exception:
        blockers.append("handoff-verification-invalid")
    if handoff_verification.signature.subject != "pg-release-verifier":
        blockers.append("handoff-verifier-identity-invalid")
    if verification.handoff_digest != handoff.handoff_digest:
        blockers.append("handoff-digest-mismatch")
    if verification.candidate_notes_sha256 != handoff.candidate_notes_sha256:
        blockers.append("candidate-notes-digest-mismatch")
    if verification.evidence_graph_digest != sha256_hex(
        [item.object_digest for item in handoff.evidence]
    ):
        blockers.append("handoff-evidence-graph-mismatch")
    if not (
        handoff.built_at <= verification.verified_at <= evaluated_at
        and verification.verified_at < handoff.valid_until
    ):
        blockers.append("handoff-verification-time-invalid")
    if (
        status_ledger.release_fingerprint != handoff.release_fingerprint
        or status_ledger.charter_digest != handoff.charter_digest
        or status_ledger.contract_manifest_digest != handoff.contract_manifest_digest
    ):
        blockers.append("status-ledger-binding-mismatch")
    if status_ledger.generated_at > evaluated_at:
        blockers.append("status-ledger-from-future")
    if handoff.availability_state == AvailabilityState.MISSED:
        blockers.append("availability-missed")
    if handoff.retention_state == RetentionState.OVERDUE:
        blockers.append("retention-overdue")

    permitted_missing = {
        "manual-publication-record",
        "availability-resolution",
        "retention-resolution",
    }
    for task in status_ledger.tasks:
        for kind in task.missing_evidence_kinds:
            if kind not in permitted_missing:
                blockers.append(f"task-{task.task_id}-{kind}-missing")
    for gate in status_ledger.gates:
        for kind in gate.missing_evidence_kinds:
            if gate.gate_id == "G15" and kind == "manual-publication-record":
                continue
            if gate.gate_id == "G14" and kind in {
                "availability-continuity",
                "retention-current",
            }:
                continue
            blockers.append(f"gate-{gate.gate_id}-{kind}-missing")
    blockers = sorted(set(blockers))
    decision = (
        ProgramDecision.NO_SHIP
        if blockers
        else ProgramDecision.READY_FOR_MANUAL_PUBLICATION
    )
    values = {
        "schema_version": "workchord-postgresql-closeout-decision-v1",
        "evaluator_identity": "pg-closeout-evaluator",
        "evaluated_at": evaluated_at,
        "valid_until": handoff.valid_until,
        "decision": decision,
        "handoff_digest": handoff.handoff_digest,
        "status_ledger_digest": status_ledger.ledger_digest,
        "availability_state": handoff.availability_state,
        "retention_state": handoff.retention_state,
        "blocker_codes": tuple(blockers),
        "manual_external_items": ("DBM-DOC-002", "G15"),
        "external_post_publication_items": ("DBM-CLOSE-001",),
    }
    preliminary = CloseoutDecision.model_construct(
        **values, decision_digest="0" * 64
    )
    unsigned = preliminary.model_dump(mode="json", exclude={"decision_digest"})
    return CloseoutDecision(**values, decision_digest=sha256_hex(unsigned))


def sign_closeout_decision(
    decision: CloseoutDecision,
    *,
    signer: RemoteSigner,
    key_ref: str,
) -> SignedCloseoutDecision:
    signature = signer.sign_digest(
        payload_sha256=sha256_hex(canonical_json_bytes(decision)),
        key_ref=key_ref,
        subject="pg-closure-verifier",
    )
    if signature.subject != "pg-closure-verifier":
        raise ValueError("Remote signer returned another closure-verifier subject")
    return SignedCloseoutDecision(decision=decision, signature=signature)


def _render_candidate_notes(
    *,
    release_fingerprint: str,
    availability_state: AvailabilityState,
    retention_state: RetentionState,
) -> str:
    availability_line = {
        AvailabilityState.PENDING: (
            "The 30-day availability observation is pending; no 99.9% availability "
            "claim is supported."
        ),
        AvailabilityState.MET: (
            "The complete 30-day availability observation supports the frozen 99.9% claim."
        ),
        AvailabilityState.MISSED: (
            "The availability objective was missed; no 99.9% availability claim is supported."
        ),
    }[availability_state]
    retention_line = {
        RetentionState.RETAINED_NOT_DUE: "The frozen SQLite snapshot is retained and not yet due for disposal.",
        RetentionState.DISPOSED: "Exact-digest SQLite snapshot disposal and absence were verified.",
        RetentionState.OVERDUE: "SQLite snapshot disposal is overdue; publication readiness is blocked.",
    }[retention_state]
    return "\n".join(
        (
            "NOT PUBLISHED - MANUAL PUBLICATION REQUIRED",
            f"Release fingerprint: {release_fingerprint}",
            (
                "Qualified capacity wording is limited to 1,250 opaque browser identities, "
                "250 active browser sessions, and 200 concurrent MCP/agent clients."
            ),
            "This does not claim 1,250 authenticated people.",
            availability_line,
            retention_line,
        )
    )
