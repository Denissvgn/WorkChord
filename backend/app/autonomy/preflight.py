"""Deterministic autonomous-start gate evaluation."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import Field, model_validator

from app.autonomy.canonical import StrictContractModel, canonical_json_bytes, sha256_hex
from app.autonomy.contracts.charter import (
    AutonomyState,
    CharterVerificationReceipt,
    ProgramDecision,
)
from app.autonomy.contracts.postgresql.loader import PostgreSQLContractBundle
from app.autonomy.evidence import SignedAutonomousEvidence
from app.autonomy.signing import DetachedSignatureEnvelope, RemoteSigner


SHA256_PATTERN = r"^[0-9a-f]{64}$"
IDENTIFIER_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9._:-]{0,254}$"

CORE_FEATURES = {
    "agent-capabilities-v1",
    "actor-roster-v1",
    "actor-task-assignments",
    "my-work-v1",
    "snapshot-pagination-v1",
    "work-etag-v1",
    "complete-task-context",
    "atomic-begin-submit",
    "atomic-renew-v1",
    "fenced-claims",
    "typed-rework-recovery",
    "agent-discovery-triage-v1",
    "pm-control-v1",
    "verification-v1",
    "skill-bundles-v1",
    "model-aware-routing-v1",
    "agent-team-master-v1",
    "fenced-verifier-runs-v1",
    "durable-observation-jobs-v1",
    "autonomous-postgresql-closeout-v1",
}

_PREDICATES: tuple[tuple[str, str, Literal["blocked_external", "autonomy_not_ready", "no_ship"]], ...] = (
    ("standing-delegation", "standing-delegation-proof", "blocked_external"),
    ("bootstrap-mutation-authority", "bootstrap-slot-reconciliation", "autonomy_not_ready"),
    ("autonomy-implementation", "autonomy-qualified-report", "autonomy_not_ready"),
    ("contract-authority", "immutable-contract-archive-proof", "autonomy_not_ready"),
    ("actor-topology", "actor-topology-proof", "blocked_external"),
    ("routing-runtime", "routing-runtime-proof", "autonomy_not_ready"),
    ("independence", "independence-proof", "no_ship"),
    ("source-provenance", "source-provenance-proof", "autonomy_not_ready"),
    ("remote-signing", "remote-signing-proof", "no_ship"),
    ("rehearsal-privacy", "rehearsal-privacy-proof", "autonomy_not_ready"),
    ("git-ci-oci", "git-ci-oci-proof", "blocked_external"),
    ("infrastructure", "infrastructure-proof", "blocked_external"),
    ("time-windows", "time-window-proof", "blocked_external"),
    ("production-disabled", "production-disabled-proof", "no_ship"),
)


class VerifiedPreflightArtifact(StrictContractModel):
    predicate_id: str = Field(pattern=IDENTIFIER_PATTERN)
    evidence_kind: str = Field(pattern=IDENTIFIER_PATTERN)
    object_digest: str = Field(pattern=SHA256_PATTERN)
    signed_evidence: SignedAutonomousEvidence

    @model_validator(mode="after")
    def exact_source_evidence(self) -> "VerifiedPreflightArtifact":
        evidence = self.signed_evidence.evidence
        if self.object_digest != sha256_hex(
            canonical_json_bytes(self.signed_evidence)
        ):
            raise ValueError("Preflight object digest does not match its envelope")
        if evidence.action_id != self.evidence_kind:
            raise ValueError("Preflight artifact kind does not match its source evidence")
        if evidence.source_outcome != "succeeded":
            raise ValueError("Only succeeded source evidence may pass preflight")
        return self


class PreflightPredicateResult(StrictContractModel):
    predicate_id: str = Field(pattern=IDENTIFIER_PATTERN)
    state: Literal["passed", "blocked_external", "autonomy_not_ready", "no_ship"]
    required_evidence_kind: str = Field(pattern=IDENTIFIER_PATTERN)
    evidence_object_digest: str | None = Field(default=None, pattern=SHA256_PATTERN)
    blocker_code: str | None = Field(default=None, pattern=IDENTIFIER_PATTERN)


class AgentPreflightReport(StrictContractModel):
    schema_version: Literal["workchord-postgresql-agent-preflight-v1"] = (
        "workchord-postgresql-agent-preflight-v1"
    )
    evaluated_at: datetime
    release_fingerprint: str = Field(pattern=SHA256_PATTERN)
    contract_manifest_digest: str = Field(pattern=SHA256_PATTERN)
    autonomy_state: AutonomyState
    program_decision: ProgramDecision
    predicates: tuple[PreflightPredicateResult, ...]
    advertised_features: tuple[str, ...]
    report_digest: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def canonical_report(self) -> "AgentPreflightReport":
        ids = [item.predicate_id for item in self.predicates]
        expected = [item[0] for item in _PREDICATES]
        if ids != expected:
            raise ValueError("Preflight predicate order/completeness mismatch")
        unsigned = self.model_dump(mode="json", exclude={"report_digest"})
        if self.report_digest != sha256_hex(unsigned):
            raise ValueError("Preflight report digest mismatch")
        return self


class SignedAgentPreflightReport(StrictContractModel):
    report: AgentPreflightReport
    signature: DetachedSignatureEnvelope


def evaluate_agent_preflight(
    *,
    release_fingerprint: str,
    bundle: PostgreSQLContractBundle,
    charter_receipt: CharterVerificationReceipt | None,
    artifacts: tuple[VerifiedPreflightArtifact, ...] = (),
    advertised_features: set[str] | frozenset[str] = frozenset(),
    evaluated_at: datetime | None = None,
) -> AgentPreflightReport:
    """Evaluate every start row; missing facts are explicit blockers, never skips."""

    now = evaluated_at or datetime.now(UTC)
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("Preflight clock must be timezone-aware")
    by_predicate: dict[str, VerifiedPreflightArtifact] = {}
    for item in artifacts:
        if item.predicate_id in by_predicate:
            raise ValueError("Preflight predicate has duplicate evidence")
        by_predicate[item.predicate_id] = item
    unknown = set(by_predicate) - {item[0] for item in _PREDICATES}
    if unknown:
        raise ValueError(f"Unknown preflight predicates: {sorted(unknown)}")

    rows: list[PreflightPredicateResult] = []
    for predicate_id, evidence_kind, failure_state in _PREDICATES:
        artifact = by_predicate.get(predicate_id)
        passed = artifact is not None and artifact.evidence_kind == evidence_kind
        if passed and artifact is not None:
            evidence = artifact.signed_evidence.evidence
            passed = (
                evidence.release_fingerprint == release_fingerprint
                and evidence.contract_manifest_digest == bundle.manifest_digest
                and (
                    charter_receipt is None
                    or charter_receipt.charter_digest is None
                    or evidence.charter_digest == charter_receipt.charter_digest
                )
            )
        if predicate_id == "standing-delegation":
            passed = (
                passed
                and charter_receipt is not None
                and charter_receipt.charter_digest is not None
                and charter_receipt.autonomy_state != AutonomyState.BLOCKED_EXTERNAL
            )
        elif predicate_id == "contract-authority":
            passed = passed and bundle.archive_verified
        elif predicate_id == "routing-runtime":
            passed = passed and CORE_FEATURES.issubset(advertised_features)
        rows.append(
            PreflightPredicateResult(
                predicate_id=predicate_id,
                state="passed" if passed else failure_state,
                required_evidence_kind=evidence_kind,
                evidence_object_digest=artifact.object_digest if passed and artifact else None,
                blocker_code=None if passed else f"{predicate_id}-unmet",
            )
        )

    states = {item.state for item in rows}
    if "blocked_external" in states:
        autonomy_state = AutonomyState.BLOCKED_EXTERNAL
    elif "no_ship" in states:
        autonomy_state = AutonomyState.NOT_READY
    elif "autonomy_not_ready" in states:
        autonomy_state = AutonomyState.NOT_READY
    else:
        autonomy_state = AutonomyState.QUALIFIED
    values = {
        "schema_version": "workchord-postgresql-agent-preflight-v1",
        "evaluated_at": now,
        "release_fingerprint": release_fingerprint,
        "contract_manifest_digest": bundle.manifest_digest,
        "autonomy_state": autonomy_state,
        "program_decision": ProgramDecision.NO_SHIP,
        "predicates": tuple(rows),
        "advertised_features": tuple(sorted(advertised_features)),
    }
    preliminary = AgentPreflightReport.model_construct(
        **values,
        report_digest="0" * 64,
    )
    unsigned = preliminary.model_dump(mode="json", exclude={"report_digest"})
    return AgentPreflightReport(**values, report_digest=sha256_hex(unsigned))


def sign_agent_preflight(
    report: AgentPreflightReport,
    *,
    signer: RemoteSigner,
    key_ref: str,
    subject: str = "pg-program-controller",
) -> SignedAgentPreflightReport:
    signature = signer.sign_digest(
        payload_sha256=sha256_hex(canonical_json_bytes(report)),
        key_ref=key_ref,
        subject=subject,
    )
    if signature.subject != subject:
        raise ValueError("Remote signer returned another preflight subject")
    return SignedAgentPreflightReport(report=report, signature=signature)
