"""Deterministic DBM task/gate status amendment evaluation."""

from __future__ import annotations

from datetime import UTC, datetime
import re
from typing import Literal

from pydantic import Field, model_validator

from app.autonomy.canonical import StrictContractModel, canonical_json_bytes, sha256_hex
from app.autonomy.contracts.postgresql.loader import PostgreSQLContractBundle
from app.autonomy.evidence import SignedAutonomousEvidence


SHA256_PATTERN = r"^[0-9a-f]{64}$"
IDENTIFIER_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9._:-]{0,254}$"


class StatusRule(StrictContractModel):
    id: str = Field(pattern=IDENTIFIER_PATTERN)
    implementation: Literal["implemented_local"] | None = None
    required_evidence: tuple[str, ...] = Field(min_length=1, max_length=128)
    next_tasks: tuple[str, ...] = Field(min_length=1, max_length=32)
    terminal_boundary: Literal["manual_external", "external_post_publication"] | None = None


class StatusRulesContract(StrictContractModel):
    schema_version: Literal["workchord-postgresql-status-rules-v1"]
    waiver_policy: Literal["forbidden"]
    tasks: tuple[StatusRule, ...] = Field(min_length=1, max_length=256)
    gates: tuple[StatusRule, ...] = Field(min_length=15, max_length=15)

    @model_validator(mode="after")
    def exact_registry(self) -> "StatusRulesContract":
        task_ids = [item.id for item in self.tasks]
        gate_ids = [item.id for item in self.gates]
        if len(set(task_ids)) != len(task_ids):
            raise ValueError("Status task rules contain duplicates")
        if set(gate_ids) != {f"G{index}" for index in range(1, 16)}:
            raise ValueError("Status gate rules must contain G1-G15 exactly once")
        return self


class ResolvedStatusEvidence(StrictContractModel):
    """A resolver-produced reference to one signed immutable source envelope."""

    evidence_kind: str = Field(pattern=IDENTIFIER_PATTERN)
    object_digest: str = Field(pattern=SHA256_PATTERN)
    object_uri: str = Field(min_length=1, max_length=2048)
    signed_evidence: SignedAutonomousEvidence
    expires_at: datetime | None = None
    reset_trigger: str = Field(min_length=1, max_length=512)

    @model_validator(mode="after")
    def source_bound(self) -> "ResolvedStatusEvidence":
        if self.object_digest != sha256_hex(
            canonical_json_bytes(self.signed_evidence)
        ):
            raise ValueError("Status evidence digest does not match its envelope")
        if self.signed_evidence.evidence.action_id != self.evidence_kind:
            raise ValueError("Status evidence kind does not match its signed action")
        if self.signed_evidence.evidence.source_outcome != "succeeded":
            raise ValueError("Failed/stopped/unavailable evidence cannot satisfy status")
        if self.expires_at is not None and (
            self.expires_at.tzinfo is None or self.expires_at.utcoffset() is None
        ):
            raise ValueError("Status evidence expiry must be timezone-aware")
        return self


class StatusEvidenceReference(StrictContractModel):
    evidence_kind: str = Field(pattern=IDENTIFIER_PATTERN)
    immutable_evidence_uri: str = Field(min_length=1, max_length=2048)
    immutable_evidence_checksum: str = Field(pattern=SHA256_PATTERN)
    workload_identity: str = Field(min_length=1, max_length=512)
    source_system: str = Field(pattern=IDENTIFIER_PATTERN)
    expires_at: datetime | None
    reset_trigger: str = Field(min_length=1, max_length=512)


class TaskStatusAmendment(StrictContractModel):
    task_id: str = Field(pattern=IDENTIFIER_PATTERN)
    implementation_state: Literal["implemented_local"]
    acceptance_state: Literal["acceptance_evidenced", "acceptance_pending"]
    release_gate_state: Literal["not_a_gate"] = "not_a_gate"
    required_evidence_kinds: tuple[str, ...]
    satisfied_evidence: tuple[StatusEvidenceReference, ...]
    missing_evidence_kinds: tuple[str, ...]
    next_tasks: tuple[str, ...]
    terminal_boundary: Literal["manual_external", "external_post_publication"] | None


class GateStatusAmendment(StrictContractModel):
    gate_id: str = Field(pattern=IDENTIFIER_PATTERN)
    gate_state: Literal["gate_passed", "gate_pending"]
    required_evidence_kinds: tuple[str, ...]
    satisfied_evidence: tuple[StatusEvidenceReference, ...]
    missing_evidence_kinds: tuple[str, ...]
    next_tasks: tuple[str, ...]
    terminal_boundary: Literal["manual_external", "external_post_publication"] | None


class StatusAmendmentLedger(StrictContractModel):
    schema_version: Literal["workchord-postgresql-status-amendment-v1"] = (
        "workchord-postgresql-status-amendment-v1"
    )
    generated_at: datetime
    evaluator_identity: Literal["pg-status-evaluator"] = "pg-status-evaluator"
    contract_manifest_digest: str = Field(pattern=SHA256_PATTERN)
    release_fingerprint: str = Field(pattern=SHA256_PATTERN)
    charter_digest: str = Field(pattern=SHA256_PATTERN)
    source_status_snapshot_digest: str = Field(pattern=SHA256_PATTERN)
    waiver_policy: Literal["forbidden"] = "forbidden"
    tasks: tuple[TaskStatusAmendment, ...]
    gates: tuple[GateStatusAmendment, ...]
    overall_state: Literal["acceptance_pending", "acceptance_evidenced"]
    ledger_digest: str = Field(pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def canonical_digest_and_completeness(self) -> "StatusAmendmentLedger":
        task_ids = [item.task_id for item in self.tasks]
        gate_ids = [item.gate_id for item in self.gates]
        if len(set(task_ids)) != len(task_ids):
            raise ValueError("Status amendment contains duplicate tasks")
        if set(gate_ids) != {f"G{index}" for index in range(1, 16)}:
            raise ValueError("Status amendment must contain G1-G15 exactly once")
        unsigned = self.model_dump(mode="json", exclude={"ledger_digest"})
        if self.ledger_digest != sha256_hex(unsigned):
            raise ValueError("Status amendment digest mismatch")
        return self


def evaluate_status_amendment(
    *,
    bundle: PostgreSQLContractBundle,
    release_fingerprint: str,
    charter_digest: str,
    source_status_snapshot_digest: str,
    resolved_evidence: tuple[ResolvedStatusEvidence, ...] = (),
    generated_at: datetime | None = None,
) -> StatusAmendmentLedger:
    """Derive conservative task/gate truth; evidence absence can never pass."""

    if re.fullmatch(SHA256_PATTERN, source_status_snapshot_digest) is None:
        raise ValueError("source_status_snapshot_digest must be SHA-256")
    rules = StatusRulesContract.model_validate(
        bundle.member_json("status-rules-v1.json")
    )
    if {item.id for item in rules.tasks} != set(bundle.manifest.trace.dbm_tasks):
        raise ValueError("Status rules do not cover the exact manifest DBM task set")
    now = generated_at or datetime.now(UTC)
    if now.tzinfo is None or now.utcoffset() is None:
        raise ValueError("Status evaluation time must be timezone-aware")
    by_kind: dict[str, ResolvedStatusEvidence] = {}
    for item in resolved_evidence:
        if item.evidence_kind in by_kind:
            raise ValueError("Status evidence kind appears more than once")
        if item.expires_at is not None and item.expires_at <= now:
            continue
        evidence = item.signed_evidence.evidence
        if (
            evidence.release_fingerprint != release_fingerprint
            or evidence.charter_digest != charter_digest
            or evidence.contract_manifest_digest != bundle.manifest_digest
        ):
            raise ValueError("Status evidence belongs to another release/charter/contract")
        by_kind[item.evidence_kind] = item

    task_rows = tuple(_task_row(rule, by_kind) for rule in rules.tasks)
    gate_rows = tuple(_gate_row(rule, by_kind) for rule in rules.gates)
    all_evidenced = all(
        item.acceptance_state == "acceptance_evidenced" for item in task_rows
    ) and all(item.gate_state == "gate_passed" for item in gate_rows)
    values = {
        "schema_version": "workchord-postgresql-status-amendment-v1",
        "generated_at": now,
        "evaluator_identity": "pg-status-evaluator",
        "contract_manifest_digest": bundle.manifest_digest,
        "release_fingerprint": release_fingerprint,
        "charter_digest": charter_digest,
        "source_status_snapshot_digest": source_status_snapshot_digest,
        "waiver_policy": "forbidden",
        "tasks": task_rows,
        "gates": gate_rows,
        "overall_state": "acceptance_evidenced" if all_evidenced else "acceptance_pending",
    }
    preliminary = StatusAmendmentLedger.model_construct(
        **values,
        ledger_digest="0" * 64,
    )
    unsigned = preliminary.model_dump(mode="json", exclude={"ledger_digest"})
    return StatusAmendmentLedger(**values, ledger_digest=sha256_hex(unsigned))


def _reference(item: ResolvedStatusEvidence) -> StatusEvidenceReference:
    evidence = item.signed_evidence.evidence
    return StatusEvidenceReference(
        evidence_kind=item.evidence_kind,
        immutable_evidence_uri=item.object_uri,
        immutable_evidence_checksum=item.object_digest,
        workload_identity=evidence.issuer_workload_identity,
        source_system=evidence.source_system,
        expires_at=item.expires_at,
        reset_trigger=item.reset_trigger,
    )


def _task_row(
    rule: StatusRule,
    by_kind: dict[str, ResolvedStatusEvidence],
) -> TaskStatusAmendment:
    satisfied = tuple(
        _reference(by_kind[kind]) for kind in rule.required_evidence if kind in by_kind
    )
    missing = tuple(kind for kind in rule.required_evidence if kind not in by_kind)
    return TaskStatusAmendment(
        task_id=rule.id,
        implementation_state="implemented_local",
        acceptance_state="acceptance_pending" if missing else "acceptance_evidenced",
        required_evidence_kinds=rule.required_evidence,
        satisfied_evidence=satisfied,
        missing_evidence_kinds=missing,
        next_tasks=rule.next_tasks,
        terminal_boundary=rule.terminal_boundary,
    )


def _gate_row(
    rule: StatusRule,
    by_kind: dict[str, ResolvedStatusEvidence],
) -> GateStatusAmendment:
    satisfied = tuple(
        _reference(by_kind[kind]) for kind in rule.required_evidence if kind in by_kind
    )
    missing = tuple(kind for kind in rule.required_evidence if kind not in by_kind)
    return GateStatusAmendment(
        gate_id=rule.id,
        gate_state="gate_pending" if missing else "gate_passed",
        required_evidence_kinds=rule.required_evidence,
        satisfied_evidence=satisfied,
        missing_evidence_kinds=missing,
        next_tasks=rule.next_tasks,
        terminal_boundary=rule.terminal_boundary,
    )
