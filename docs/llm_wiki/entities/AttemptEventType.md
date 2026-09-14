# AttemptEventType

**Location:** `backend/app/autonomy/evidence.py:236`
**Kind:** Enum
**Bases:** `StrEnum`
**Module:** [evidence](../modules/evidence.md)

## Description

_Auto-generated from `AttemptEventType` in `backend/app/autonomy/evidence.py`._

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `ALLOCATED` | `'allocated'` | — |
| `STARTED` | `'started'` | — |
| `CHECKPOINT` | `'checkpoint'` | — |
| `FAILED` | `'failed'` | — |
| `STOPPED` | `'stopped'` | — |
| `RESET` | `'reset'` | — |
| `EVALUATED` | `'evaluated'` | — |
| `FINAL` | `'final'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AttemptEventType (backend/app/autonomy/evidence.py)"]
    n1["StrEnum"]
    n2["AttemptLedger._validate_transition (backend/app/autonomy/evidence.py)"]
    n3["AttemptLedger.append (backend/app/autonomy/evidence.py)"]
    n4["backend/app/autonomy/leases.py"]
    n5["backend/tests/autonomy/test_autonomy_foundation.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/evidence.md"
    click n2 "../modules/evidence.md"
    click n3 "../modules/evidence.md"
    click n4 "../modules/leases.md"
    click n5 "../modules/test_autonomy_foundation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [evidence](../modules/evidence.md) | 0 | `ALLOCATED`, `CHECKPOINT`, `EVALUATED`, `FAILED`, `FINAL`, `RESET`, `STARTED`, `STOPPED` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrEnum` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AttemptLedger._validate_transition` | type_reference | [evidence](../modules/evidence.md) | — |
| `AttemptLedger.append` | type_reference | [evidence](../modules/evidence.md) | — |
| `leases` | import | [leases](../modules/leases.md) | — |
| `test_autonomy_foundation` | import | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | — |
