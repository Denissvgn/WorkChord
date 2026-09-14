# AttemptLedger

**Location:** `backend/app/autonomy/evidence.py:325`
**Kind:** Class
**Bases:** —
**Module:** [evidence](../modules/evidence.md)

## Description

Allocate attempt numbers and append every lifecycle fact before action.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(*, backend: AttemptLedgerBackend, clock: Callable[[], datetime] = lambda: datetime.now(UTC), maximum_cas_attempts: int = 8) -> None` | — | — |
| `allocate` | `(*, run_id: str, task_id: str, stage_id: str, action_id: str, release_fingerprint: str, charter_digest: str, contract_manifest_digest: str) -> AttemptLedgerRecord` | — | — |
| `append` | `(*, attempt_id: int, event_type: AttemptEventType, evidence_digest: str \| None = None, normalized_reason_code: str \| None = None) -> AttemptLedgerRecord` | — | — |
| `start` | `(*, attempt_id: int) -> AttemptLedgerRecord` | — | — |
| `_validated_snapshot` | `() -> AttemptLedgerSnapshot` | — | — |
| `_validate_transition` | `(records: list[AttemptLedgerRecord], event_type: AttemptEventType) -> None` | `@staticmethod` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AttemptLedger (backend/app/autonomy/evidence.py)"]
    n1["AttemptLedger.__init__ (backend/app/autonomy/evidence.py)"]
    n2["AttemptLedger._validate_transition (backend/app/autonomy/evidence.py)"]
    n3["AttemptLedger._validated_snapshot (backend/app/autonomy/evidence.py)"]
    n4["AttemptLedger.allocate (backend/app/autonomy/evidence.py)"]
    n5["AttemptLedger.append (backend/app/autonomy/evidence.py)"]
    n6["AttemptLedger.start (backend/app/autonomy/evidence.py)"]
    n7["AttemptLedgerBackend.compare_and_append (backend/app/autonomy/evidence.py)"]
    n8["AttemptLedgerBackend.read (backend/app/autonomy/evidence.py)"]
    n9["AttemptLedgerRecord.valid_parent (backend/app/autonomy/evidence.py)"]
    n10["validate_attempt_ledger_snapshot (backend/app/autonomy/evidence.py)"]
    n11["MemoryAttemptBackend.compare_and_append (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n12["MemoryAttemptBackend.read (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    n12 --> n0
    click n0 "../modules/evidence.md"
    click n1 "../modules/evidence.md"
    click n2 "../modules/evidence.md"
    click n3 "../modules/evidence.md"
    click n4 "../modules/evidence.md"
    click n5 "../modules/evidence.md"
    click n6 "../modules/evidence.md"
    click n7 "../modules/evidence.md"
    click n8 "../modules/evidence.md"
    click n9 "../modules/evidence.md"
    click n10 "../modules/evidence.md"
    click n11 "../modules/test_autonomy_foundation.md"
    click n12 "../modules/test_autonomy_foundation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [evidence](../modules/evidence.md) | 6 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AttemptLedger.__init__` | type_reference | [evidence](../modules/evidence.md) | — |
| `AttemptLedger._validate_transition` | type_reference | [evidence](../modules/evidence.md) | — |
| `AttemptLedger._validated_snapshot` | type_reference | [evidence](../modules/evidence.md) | — |
| `AttemptLedger.allocate` | type_reference | [evidence](../modules/evidence.md) | — |
| `AttemptLedger.append` | type_reference | [evidence](../modules/evidence.md) | — |
| `AttemptLedger.start` | type_reference | [evidence](../modules/evidence.md) | — |
| `AttemptLedgerBackend.compare_and_append` | type_reference | [evidence](../modules/evidence.md) | — |
| `AttemptLedgerBackend.read` | type_reference | [evidence](../modules/evidence.md) | — |
| `AttemptLedgerRecord.valid_parent` | type_reference | [evidence](../modules/evidence.md) | — |
| `validate_attempt_ledger_snapshot` | type_reference | [evidence](../modules/evidence.md) | — |
| `MemoryAttemptBackend.compare_and_append` | type_reference | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | — |
| `MemoryAttemptBackend.read` | type_reference | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | — |

> References: showing 12 of 14 logical references; 2 omitted by the 12-row generated summary limit.
