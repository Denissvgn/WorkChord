# RedactionClass

**Location:** `backend/app/autonomy/evidence.py:31`
**Kind:** Enum
**Bases:** `StrEnum`
**Module:** [evidence](../modules/evidence.md)

## Description

_Auto-generated from `RedactionClass` in `backend/app/autonomy/evidence.py`._

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `RESTRICTED_TOPOLOGY` | `'restricted-topology'` | — |
| `INTERNAL` | `'internal'` | — |
| `PUBLIC` | `'public'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RedactionClass (backend/app/autonomy/evidence.py)"]
    n1["StrEnum"]
    n2["WormObjectStore.put_if_absent (backend/app/autonomy/evidence.py)"]
    n3["backend/app/autonomy/handoff.py"]
    n4["MemoryWormStore.put_if_absent (backend/tests/autonomy/test_autonomy_foundation.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/evidence.md"
    click n2 "../modules/evidence.md"
    click n3 "../modules/handoff.md"
    click n4 "../modules/test_autonomy_foundation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [evidence](../modules/evidence.md) | 0 | `INTERNAL`, `PUBLIC`, `RESTRICTED_TOPOLOGY` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrEnum` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `WormObjectStore.put_if_absent` | type_reference | [evidence](../modules/evidence.md) | — |
| `handoff` | import | [handoff](../modules/handoff.md) | — |
| `MemoryWormStore.put_if_absent` | type_reference | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | — |
