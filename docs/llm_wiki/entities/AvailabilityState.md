# AvailabilityState

**Location:** `backend/app/autonomy/handoff.py:36`
**Kind:** Enum
**Bases:** `StrEnum`
**Module:** [handoff](../modules/handoff.md)

## Description

_Auto-generated from `AvailabilityState` in `backend/app/autonomy/handoff.py`._

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `PENDING` | `'pending'` | — |
| `MET` | `'met'` | — |
| `MISSED` | `'missed'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AvailabilityState (backend/app/autonomy/handoff.py)"]
    n1["StrEnum"]
    n2["_render_candidate_notes (backend/app/autonomy/handoff.py)"]
    n3["build_manual_publication_handoff (backend/app/autonomy/handoff.py)"]
    n4["backend/tests/autonomy/test_autonomy_foundation.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/handoff.md"
    click n2 "../modules/handoff.md"
    click n3 "../modules/handoff.md"
    click n4 "../modules/test_autonomy_foundation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [handoff](../modules/handoff.md) | 0 | `MET`, `MISSED`, `PENDING` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrEnum` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `_render_candidate_notes` | type_reference | [handoff](../modules/handoff.md) | — |
| `build_manual_publication_handoff` | type_reference | [handoff](../modules/handoff.md) | — |
| `test_autonomy_foundation` | import | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | — |
