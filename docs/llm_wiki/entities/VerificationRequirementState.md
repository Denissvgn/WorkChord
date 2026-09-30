# VerificationRequirementState

**Location:** `backend/app/autonomy/orchestration.py:413`
**Kind:** Enum
**Bases:** `StrEnum`
**Module:** [orchestration](../modules/orchestration.md)

## Description

_Auto-generated from `VerificationRequirementState` in `backend/app/autonomy/orchestration.py`._

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `PLANNED` | `'planned'` | — |
| `READY` | `'ready'` | — |
| `CLAIMED` | `'claimed'` | — |
| `RUNNING` | `'running'` | — |
| `PASSED` | `'passed'` | — |
| `REJECTED` | `'rejected'` | — |
| `EXPIRED` | `'expired'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["VerificationRequirementState (backend/app/autonomy/orchestration.py)"]
    n1["StrEnum"]
    n2["aggregate_work_package (backend/app/autonomy/orchestration.py)"]
    n3["backend/tests/autonomy/test_autonomy_foundation.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/orchestration.md"
    click n2 "../modules/orchestration.md"
    click n3 "../modules/test_autonomy_foundation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [orchestration](../modules/orchestration.md) | 0 | `CLAIMED`, `EXPIRED`, `PASSED`, `PLANNED`, `READY`, `REJECTED`, `RUNNING` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrEnum` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `aggregate_work_package` | type_reference | [orchestration](../modules/orchestration.md) | — |
| `test_autonomy_foundation` | import | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | — |
