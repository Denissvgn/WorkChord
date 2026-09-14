# ReconciliationClass

**Location:** `backend/app/autonomy/contracts/topology.py:88`
**Kind:** Enum
**Bases:** `StrEnum`
**Module:** [topology](../modules/topology.md)

## Description

_Auto-generated from `ReconciliationClass` in `backend/app/autonomy/contracts/topology.py`._

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `CREATE` | `'create'` | — |
| `SAFE_UPDATE` | `'safe_update'` | — |
| `NO_CHANGE` | `'no_change'` | — |
| `BLOCKED_CONFLICT` | `'blocked_conflict'` | — |
| `REQUIRES_REPLACEMENT` | `'requires_replacement'` | — |
| `PROPOSE_DISABLE` | `'propose_disable'` | — |
| `UNMANAGED` | `'unmanaged'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ReconciliationClass (backend/app/autonomy/contracts/topology.py)"]
    n1["StrEnum"]
    n2["_action (backend/app/autonomy/contracts/topology.py)"]
    n3["backend/tests/autonomy/test_autonomy_foundation.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/topology.md"
    click n2 "../modules/topology.md"
    click n3 "../modules/test_autonomy_foundation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [topology](../modules/topology.md) | 0 | `BLOCKED_CONFLICT`, `CREATE`, `NO_CHANGE`, `PROPOSE_DISABLE`, `REQUIRES_REPLACEMENT`, `SAFE_UPDATE`, `UNMANAGED` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrEnum` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_action` | type_reference | [topology](../modules/topology.md) | — |
| `test_autonomy_foundation` | import | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | — |
