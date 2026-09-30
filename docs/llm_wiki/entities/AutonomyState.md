# AutonomyState

**Location:** `backend/app/autonomy/contracts/charter.py:37`
**Kind:** Enum
**Bases:** `StrEnum`
**Module:** [charter](../modules/charter.md)

## Description

_Auto-generated from `AutonomyState` in `backend/app/autonomy/contracts/charter.py`._

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `NOT_READY` | `'AUTONOMY-NOT-READY'` | — |
| `BLOCKED_EXTERNAL` | `'BLOCKED_EXTERNAL'` | — |
| `QUALIFIED` | `'AUTONOMY-QUALIFIED'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AutonomyState (backend/app/autonomy/contracts/charter.py)"]
    n1["StrEnum"]
    n2["backend/app/autonomy/preflight.py"]
    n3["backend/tests/autonomy/test_autonomy_foundation.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/charter.md"
    click n2 "../modules/preflight.md"
    click n3 "../modules/test_autonomy_foundation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [charter](../modules/charter.md) | 0 | `BLOCKED_EXTERNAL`, `NOT_READY`, `QUALIFIED` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrEnum` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `preflight` | import | [preflight](../modules/preflight.md) | — |
| `test_autonomy_foundation` | import | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | — |
