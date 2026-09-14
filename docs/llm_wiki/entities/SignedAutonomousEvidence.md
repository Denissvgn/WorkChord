# SignedAutonomousEvidence

**Location:** `backend/app/autonomy/evidence.py:102`
**Kind:** Pydantic model
**Bases:** `StrictContractModel`
**Module:** [evidence](../modules/evidence.md)

## Description

_Auto-generated from `SignedAutonomousEvidence` in `backend/app/autonomy/evidence.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `evidence` | `AutonomousEvidence` | `evidence` | Yes | No | — | — | — | — |
| `signature` | `DetachedSignatureEnvelope` | `signature` | Yes | No | — | — | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `digest` | `() -> str` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SignedAutonomousEvidence (backend/app/autonomy/evidence.py)"]
    n1["StrictContractModel (backend/app/autonomy/canonical.py)"]
    n2["EvidenceResolver._resolve_linked_evidence (backend/app/autonomy/evidence.py)"]
    n3["EvidenceResolver.resolve (backend/app/autonomy/evidence.py)"]
    n4["store_signed_evidence (backend/app/autonomy/evidence.py)"]
    n5["backend/app/autonomy/handoff.py"]
    n6["backend/app/autonomy/preflight.py"]
    n7["backend/app/autonomy/status.py"]
    n8["_handoff_fact (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n9["_signed_evidence (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n10["test_evidence_resolver_and_attempt_ledger_fail_closed_on_tamper_or_omission (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    click n0 "../modules/evidence.md"
    click n1 "../modules/autonomy_canonical.md"
    click n2 "../modules/evidence.md"
    click n3 "../modules/evidence.md"
    click n4 "../modules/evidence.md"
    click n5 "../modules/handoff.md"
    click n6 "../modules/preflight.md"
    click n7 "../modules/status.md"
    click n8 "../modules/test_autonomy_foundation.md"
    click n9 "../modules/test_autonomy_foundation.md"
    click n10 "../modules/test_autonomy_foundation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [evidence](../modules/evidence.md) | 1 | `evidence`, `signature` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrictContractModel` | [autonomy_canonical](../modules/autonomy_canonical.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `EvidenceResolver._resolve_linked_evidence` | type_reference | [evidence](../modules/evidence.md) | — |
| `EvidenceResolver.resolve` | type_reference | [evidence](../modules/evidence.md) | — |
| `store_signed_evidence` | type_reference | [evidence](../modules/evidence.md) | — |
| `handoff` | import | [handoff](../modules/handoff.md) | — |
| `preflight` | import | [preflight](../modules/preflight.md) | — |
| `status` | import | [status](../modules/status.md) | — |
| `_handoff_fact` | call | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | 1 |
| `_signed_evidence` | call | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | 1 |
| `_signed_evidence` | type_reference | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | — |
| `test_evidence_resolver_and_attempt_ledger_fail_closed_on_tamper_or_omission` | call | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | 1 |
