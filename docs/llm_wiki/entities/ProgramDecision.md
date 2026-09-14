# ProgramDecision

**Location:** `backend/app/autonomy/contracts/charter.py:32`
**Kind:** Enum
**Bases:** `StrEnum`
**Module:** [charter](../modules/charter.md)

## Description

_Auto-generated from `ProgramDecision` in `backend/app/autonomy/contracts/charter.py`._

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `NO_SHIP` | `'NO-SHIP'` | — |
| `READY_FOR_MANUAL_PUBLICATION` | `'READY-FOR-MANUAL-PUBLICATION'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ProgramDecision (backend/app/autonomy/contracts/charter.py)"]
    n1["StrEnum"]
    n2["backend/app/autonomy/handoff.py"]
    n3["backend/app/autonomy/preflight.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/charter.md"
    click n2 "../modules/handoff.md"
    click n3 "../modules/preflight.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [charter](../modules/charter.md) | 0 | `NO_SHIP`, `READY_FOR_MANUAL_PUBLICATION` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `StrEnum` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `handoff` | import | [handoff](../modules/handoff.md) | — |
| `preflight` | import | [preflight](../modules/preflight.md) | — |
