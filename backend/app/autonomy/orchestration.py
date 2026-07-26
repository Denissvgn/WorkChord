"""External-journal-first DAG and fenced verification state machines."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from collections.abc import Callable
from typing import Literal, Protocol, runtime_checkable

from pydantic import Field, field_validator, model_validator

from app.autonomy.canonical import StrictContractModel, canonical_json_bytes, sha256_hex
from app.autonomy.evidence import ZERO_DIGEST


SHA256_PATTERN = r"^[0-9a-f]{64}$"
IDENTIFIER_PATTERN = r"^[a-zA-Z0-9][a-zA-Z0-9._:-]{0,254}$"


class DagNodeState(StrEnum):
    PLANNED = "planned"
    READY = "ready"
    LEASED = "leased"
    RUNNING = "running"
    EVIDENCE_PENDING = "evidence_pending"
    EVALUATING = "evaluating"
    PASSED = "passed"
    FAILED = "failed"
    BLOCKED_EXTERNAL = "blocked_external"
    RESET_REQUIRED = "reset_required"


TERMINAL_DAG_STATES = {
    DagNodeState.PASSED,
    DagNodeState.FAILED,
    DagNodeState.BLOCKED_EXTERNAL,
    DagNodeState.RESET_REQUIRED,
}


class DagNodeSpec(StrictContractModel):
    node_id: str = Field(pattern=IDENTIFIER_PATTERN)
    node_version: int = Field(ge=1)
    dependencies: tuple[str, ...] = Field(default=(), max_length=256)
    reset_targets: tuple[str, ...] = Field(default=(), max_length=256)
    timeout_seconds: int = Field(ge=1, le=2_592_000)
    maximum_attempts: int = Field(ge=1, le=100)
    retry_classes: tuple[str, ...] = Field(default=(), max_length=128)
    maximum_cost_minor_units: int = Field(ge=0)
    evaluator_version: str = Field(min_length=1, max_length=255)
    source_contract_digest: str = Field(pattern=SHA256_PATTERN)

    @field_validator("dependencies", "reset_targets", "retry_classes")
    @classmethod
    def unique_values(cls, value: tuple[str, ...]) -> tuple[str, ...]:
        if len(set(value)) != len(value):
            raise ValueError("DAG dependency/reset/retry values must be unique")
        return tuple(sorted(value))

    @model_validator(mode="after")
    def no_self_edges(self) -> "DagNodeSpec":
        if self.node_id in self.dependencies or self.node_id in self.reset_targets:
            raise ValueError("DAG node cannot depend on or reset itself")
        return self


class AutonomousDagContract(StrictContractModel):
    schema_version: Literal["workchord-autonomous-dag-v1"] = (
        "workchord-autonomous-dag-v1"
    )
    run_id: str = Field(pattern=IDENTIFIER_PATTERN)
    release_fingerprint: str = Field(pattern=SHA256_PATTERN)
    charter_digest: str = Field(pattern=SHA256_PATTERN)
    contract_manifest_digest: str = Field(pattern=SHA256_PATTERN)
    nodes: tuple[DagNodeSpec, ...] = Field(min_length=1, max_length=10_000)

    @model_validator(mode="after")
    def acyclic_complete_graph(self) -> "AutonomousDagContract":
        by_id = {item.node_id: item for item in self.nodes}
        if len(by_id) != len(self.nodes):
            raise ValueError("DAG node IDs must be unique")
        for item in self.nodes:
            unknown = (set(item.dependencies) | set(item.reset_targets)) - set(by_id)
            if unknown:
                raise ValueError(f"DAG node {item.node_id} references unknown nodes: {sorted(unknown)}")
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(node_id: str) -> None:
            if node_id in visiting:
                raise ValueError("DAG dependencies contain a cycle")
            if node_id in visited:
                return
            visiting.add(node_id)
            for dependency in by_id[node_id].dependencies:
                visit(dependency)
            visiting.remove(node_id)
            visited.add(node_id)

        for node_id in by_id:
            visit(node_id)
        return self

    def digest(self) -> str:
        return sha256_hex(canonical_json_bytes(self))


class DagJournalEntry(StrictContractModel):
    schema_version: Literal["workchord-dag-journal-entry-v1"] = (
        "workchord-dag-journal-entry-v1"
    )
    sequence: int = Field(ge=1)
    run_id: str = Field(pattern=IDENTIFIER_PATTERN)
    dag_digest: str = Field(pattern=SHA256_PATTERN)
    node_id: str = Field(pattern=IDENTIFIER_PATTERN)
    node_version: int = Field(ge=1)
    from_state: DagNodeState | None
    to_state: DagNodeState
    transition: str = Field(pattern=IDENTIFIER_PATTERN)
    controller_subject: str = Field(min_length=1, max_length=512)
    cas_revision: int = Field(ge=1)
    lease_digest: str | None = Field(default=None, pattern=SHA256_PATTERN)
    attempt_start_digest: str | None = Field(default=None, pattern=SHA256_PATTERN)
    evidence_digest: str | None = Field(default=None, pattern=SHA256_PATTERN)
    checkpoint_digest: str | None = Field(default=None, pattern=SHA256_PATTERN)
    reason_code: str | None = Field(default=None, pattern=IDENTIFIER_PATTERN)
    recorded_at: datetime
    previous_hash: str = Field(pattern=SHA256_PATTERN)

    @field_validator("recorded_at")
    @classmethod
    def aware_time(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("DAG journal timestamps must be timezone-aware")
        return value

    def digest(self) -> str:
        return sha256_hex(canonical_json_bytes(self))


class DagJournalSnapshot(StrictContractModel):
    revision: int = Field(ge=0)
    head_digest: str = Field(pattern=SHA256_PATTERN)
    entries: tuple[DagJournalEntry, ...] = Field(default=(), max_length=2_000_000)


@runtime_checkable
class ExternalDagJournal(Protocol):
    """CAS state service deployed outside the WorkChord database/runtime."""

    def read(self, *, run_id: str) -> DagJournalSnapshot: ...

    def compare_and_append(
        self,
        *,
        run_id: str,
        expected_revision: int,
        expected_head_digest: str,
        entry: DagJournalEntry,
    ) -> bool: ...


class DagStateConflict(RuntimeError):
    pass


_ALLOWED_TRANSITIONS: dict[DagNodeState | None, set[DagNodeState]] = {
    None: {DagNodeState.PLANNED},
    DagNodeState.PLANNED: {
        DagNodeState.READY,
        DagNodeState.BLOCKED_EXTERNAL,
        DagNodeState.RESET_REQUIRED,
    },
    DagNodeState.READY: {
        DagNodeState.LEASED,
        DagNodeState.BLOCKED_EXTERNAL,
        DagNodeState.RESET_REQUIRED,
    },
    DagNodeState.LEASED: {
        DagNodeState.RUNNING,
        DagNodeState.READY,
        DagNodeState.BLOCKED_EXTERNAL,
        DagNodeState.RESET_REQUIRED,
    },
    DagNodeState.RUNNING: {
        DagNodeState.EVIDENCE_PENDING,
        DagNodeState.READY,
        DagNodeState.FAILED,
        DagNodeState.BLOCKED_EXTERNAL,
        DagNodeState.RESET_REQUIRED,
    },
    DagNodeState.EVIDENCE_PENDING: {
        DagNodeState.EVALUATING,
        DagNodeState.FAILED,
        DagNodeState.BLOCKED_EXTERNAL,
        DagNodeState.RESET_REQUIRED,
    },
    DagNodeState.EVALUATING: {
        DagNodeState.PASSED,
        DagNodeState.FAILED,
        DagNodeState.BLOCKED_EXTERNAL,
        DagNodeState.RESET_REQUIRED,
    },
    DagNodeState.PASSED: {DagNodeState.RESET_REQUIRED},
    DagNodeState.FAILED: {DagNodeState.RESET_REQUIRED},
    DagNodeState.BLOCKED_EXTERNAL: {DagNodeState.RESET_REQUIRED},
    DagNodeState.RESET_REQUIRED: set(),
}


class DagController:
    """Commit authoritative state externally before any WorkChord projection."""

    def __init__(
        self,
        *,
        contract: AutonomousDagContract,
        journal: ExternalDagJournal,
        controller_subject: str,
        clock: Callable[[], datetime] = lambda: datetime.now(UTC),
        maximum_cas_attempts: int = 8,
    ) -> None:
        if maximum_cas_attempts < 1 or maximum_cas_attempts > 100:
            raise ValueError("maximum_cas_attempts must be between 1 and 100")
        self.contract = contract
        self._journal = journal
        self._controller_subject = controller_subject
        self._clock = clock
        self._maximum_cas_attempts = maximum_cas_attempts
        self._nodes = {item.node_id: item for item in contract.nodes}

    def initialize(self) -> None:
        """Append one planned genesis per node in canonical topological order."""

        for node_id in self._topological_order():
            if node_id in self.current_states():
                continue
            self.transition(node_id=node_id, to_state=DagNodeState.PLANNED, transition="initialize")

    def current_states(self) -> dict[str, DagNodeState]:
        snapshot = self._validated_snapshot()
        states: dict[str, DagNodeState] = {}
        for entry in snapshot.entries:
            states[entry.node_id] = entry.to_state
        return states

    def transition(
        self,
        *,
        node_id: str,
        to_state: DagNodeState,
        transition: str,
        lease_digest: str | None = None,
        attempt_start_digest: str | None = None,
        evidence_digest: str | None = None,
        checkpoint_digest: str | None = None,
        reason_code: str | None = None,
    ) -> DagJournalEntry:
        if node_id not in self._nodes:
            raise ValueError("Unknown DAG node")
        for _ in range(self._maximum_cas_attempts):
            snapshot = self._validated_snapshot()
            state_map: dict[str, DagNodeState] = {}
            for item in snapshot.entries:
                state_map[item.node_id] = item.to_state
            from_state = state_map.get(node_id)
            if to_state not in _ALLOWED_TRANSITIONS[from_state]:
                raise ValueError(f"Invalid DAG transition {from_state!s} -> {to_state}")
            node = self._nodes[node_id]
            if to_state == DagNodeState.READY:
                missing = [
                    dependency
                    for dependency in node.dependencies
                    if state_map.get(dependency) != DagNodeState.PASSED
                ]
                if missing:
                    raise ValueError(f"DAG dependencies have not passed: {missing}")
            if to_state == DagNodeState.LEASED and not (
                lease_digest and attempt_start_digest
            ):
                raise ValueError("Leased state requires lease and attempt-start digests")
            if to_state == DagNodeState.EVIDENCE_PENDING and not evidence_digest:
                raise ValueError("Evidence-pending state requires an evidence digest")
            if to_state in {DagNodeState.FAILED, DagNodeState.BLOCKED_EXTERNAL, DagNodeState.RESET_REQUIRED} and not reason_code:
                raise ValueError("Failure/block/reset transitions require a reason code")
            entry = DagJournalEntry(
                sequence=len(snapshot.entries) + 1,
                run_id=self.contract.run_id,
                dag_digest=self.contract.digest(),
                node_id=node_id,
                node_version=node.node_version,
                from_state=from_state,
                to_state=to_state,
                transition=transition,
                controller_subject=self._controller_subject,
                cas_revision=snapshot.revision + 1,
                lease_digest=lease_digest,
                attempt_start_digest=attempt_start_digest,
                evidence_digest=evidence_digest,
                checkpoint_digest=checkpoint_digest,
                reason_code=reason_code,
                recorded_at=self._clock(),
                previous_hash=snapshot.head_digest,
            )
            if self._journal.compare_and_append(
                run_id=self.contract.run_id,
                expected_revision=snapshot.revision,
                expected_head_digest=snapshot.head_digest,
                entry=entry,
            ):
                return entry
        raise DagStateConflict("DAG transition exhausted CAS retries")

    def reset_dependents(self, *, failed_node_id: str, reason_code: str) -> tuple[DagJournalEntry, ...]:
        """Append resets in stable dependency order without rewriting history."""

        if failed_node_id not in self._nodes:
            raise ValueError("Unknown failed DAG node")
        states = self.current_states()
        affected: set[str] = set(self._nodes[failed_node_id].reset_targets)
        changed = True
        while changed:
            changed = False
            for candidate in self.contract.nodes:
                if candidate.node_id in affected:
                    continue
                if set(candidate.dependencies) & ({failed_node_id} | affected):
                    affected.add(candidate.node_id)
                    changed = True
        entries: list[DagJournalEntry] = []
        for node_id in self._topological_order():
            state = states.get(node_id)
            if node_id not in affected or state in (None, DagNodeState.RESET_REQUIRED):
                continue
            entries.append(
                self.transition(
                    node_id=node_id,
                    to_state=DagNodeState.RESET_REQUIRED,
                    transition="dependency-reset",
                    reason_code=reason_code,
                )
            )
        return tuple(entries)

    def _validated_snapshot(self) -> DagJournalSnapshot:
        snapshot = self._journal.read(run_id=self.contract.run_id)
        parent = ZERO_DIGEST
        states: dict[str, DagNodeState] = {}
        previous_recorded_at: datetime | None = None
        for sequence, entry in enumerate(snapshot.entries, start=1):
            if entry.sequence != sequence or entry.cas_revision != sequence:
                raise ValueError("DAG journal contains a sequence/revision gap")
            if entry.previous_hash != parent:
                raise ValueError("DAG journal hash chain is invalid")
            if entry.run_id != self.contract.run_id or entry.dag_digest != self.contract.digest():
                raise ValueError("DAG journal entry belongs to another contract")
            if entry.controller_subject != self._controller_subject:
                raise ValueError("DAG journal entry belongs to another controller subject")
            if previous_recorded_at is not None and entry.recorded_at < previous_recorded_at:
                raise ValueError("DAG journal timestamps moved backwards")
            node = self._nodes.get(entry.node_id)
            if node is None or entry.node_version != node.node_version:
                raise ValueError("DAG journal node identity/version is not chartered")
            expected_from = states.get(entry.node_id)
            if entry.from_state != expected_from:
                raise ValueError("DAG journal from_state does not match history")
            if entry.to_state not in _ALLOWED_TRANSITIONS[expected_from]:
                raise ValueError("DAG journal contains an invalid transition")
            if entry.to_state == DagNodeState.READY:
                missing = [
                    dependency
                    for dependency in node.dependencies
                    if states.get(dependency) != DagNodeState.PASSED
                ]
                if missing:
                    raise ValueError("DAG journal readied a node before dependencies passed")
            if entry.to_state == DagNodeState.LEASED and not (
                entry.lease_digest and entry.attempt_start_digest
            ):
                raise ValueError("DAG journal leased state lacks lease ancestry")
            if entry.to_state == DagNodeState.EVIDENCE_PENDING and not entry.evidence_digest:
                raise ValueError("DAG journal evidence-pending state lacks evidence")
            if entry.to_state in {
                DagNodeState.FAILED,
                DagNodeState.BLOCKED_EXTERNAL,
                DagNodeState.RESET_REQUIRED,
            } and not entry.reason_code:
                raise ValueError("DAG journal failure/block/reset lacks a reason code")
            states[entry.node_id] = entry.to_state
            parent = entry.digest()
            previous_recorded_at = entry.recorded_at
        if snapshot.revision != len(snapshot.entries):
            raise ValueError("DAG journal revision does not match history")
        if snapshot.head_digest != parent:
            raise ValueError("DAG journal head does not match history")
        return snapshot

    def _topological_order(self) -> tuple[str, ...]:
        remaining = {item.node_id: set(item.dependencies) for item in self.contract.nodes}
        order: list[str] = []
        while remaining:
            ready = sorted(node_id for node_id, dependencies in remaining.items() if not dependencies)
            if not ready:
                raise ValueError("DAG dependencies contain a cycle")
            for node_id in ready:
                order.append(node_id)
                remaining.pop(node_id)
            for dependencies in remaining.values():
                dependencies.difference_update(ready)
        return tuple(order)


class VerificationRequirementState(StrEnum):
    PLANNED = "planned"
    READY = "ready"
    CLAIMED = "claimed"
    RUNNING = "running"
    PASSED = "passed"
    REJECTED = "rejected"
    EXPIRED = "expired"


class VerificationRequirementContract(StrictContractModel):
    slot_id: str = Field(pattern=IDENTIFIER_PATTERN)
    verifier_logical_key: str = Field(pattern=IDENTIFIER_PATTERN)
    criterion_schema: str = Field(pattern=IDENTIFIER_PATTERN)
    artifact_set_digest: str = Field(pattern=SHA256_PATTERN)
    evaluator_version: str = Field(min_length=1, max_length=255)
    executor_independence_group: str = Field(pattern=IDENTIFIER_PATTERN)
    required_verifier_independence_group: str = Field(pattern=IDENTIFIER_PATTERN)
    maximum_lease_seconds: int = Field(ge=1, le=3600)

    @model_validator(mode="after")
    def independent(self) -> "VerificationRequirementContract":
        if self.executor_independence_group == self.required_verifier_independence_group:
            raise ValueError("Executor and verifier independence groups must differ")
        return self


class WorkPackageContract(StrictContractModel):
    schema_version: Literal["agent-work-package-v1"] = "agent-work-package-v1"
    package_id: str = Field(pattern=IDENTIFIER_PATTERN)
    package_version: int = Field(ge=1)
    execution_task_id: str | None = Field(default=None, pattern=IDENTIFIER_PATTERN)
    artifact_set_digest: str = Field(pattern=SHA256_PATTERN)
    requirements: tuple[VerificationRequirementContract, ...] = Field(
        min_length=1, max_length=64
    )
    predecessor_package_digest: str | None = Field(default=None, pattern=SHA256_PATTERN)

    @model_validator(mode="after")
    def unique_slots(self) -> "WorkPackageContract":
        slots = [item.slot_id for item in self.requirements]
        if len(set(slots)) != len(slots):
            raise ValueError("Verification requirement slots must be unique")
        if any(item.artifact_set_digest != self.artifact_set_digest for item in self.requirements):
            raise ValueError("Every verifier slot must freeze the same artifact set")
        return self


def aggregate_work_package(
    contract: WorkPackageContract,
    states: dict[str, VerificationRequirementState],
) -> Literal["evaluating", "passed", "rework_required"]:
    """Derive package state without rewriting the execution task."""

    expected = {item.slot_id for item in contract.requirements}
    if set(states) - expected:
        raise ValueError("Package state contains an unknown verification slot")
    if any(
        states.get(slot) in {VerificationRequirementState.REJECTED, VerificationRequirementState.EXPIRED}
        for slot in expected
    ):
        return "rework_required"
    if expected and all(states.get(slot) == VerificationRequirementState.PASSED for slot in expected):
        return "passed"
    return "evaluating"
