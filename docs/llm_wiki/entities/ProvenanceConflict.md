# ProvenanceConflict

**Location:** `backend/app/services/manual_provenance_service.py:45`
**Kind:** Class
**Bases:** `PlanningConflict`
**Module:** [manual_provenance_service](../modules/manual_provenance_service.md)

## Description

A refusal that also names the offending fact, such as a commit and its attribution gap.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(code, message, **context)` | — | — |
| `detail` | `()` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ProvenanceConflict (backend/app/services/manual_provenance_service.py)"]
    n1["PlanningConflict (backend/app/commands.py)"]
    n2["ManualProvenanceService._verify_candidate (backend/app/services/manual_provenance_service.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/manual_provenance_service.md"
    click n1 "../modules/commands.md"
    click n2 "../modules/manual_provenance_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [manual_provenance_service](../modules/manual_provenance_service.md) | 2 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `PlanningConflict` | [commands](../modules/commands.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `ManualProvenanceService._verify_candidate` | call | [manual_provenance_service](../modules/manual_provenance_service.md) | 6 |
