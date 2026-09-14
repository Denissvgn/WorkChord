# EvidenceResolutionError

**Location:** `backend/app/autonomy/evidence.py:123`
**Kind:** Class
**Bases:** `ValueError`
**Module:** [evidence](../modules/evidence.md)

## Description

_Auto-generated from `EvidenceResolutionError` in `backend/app/autonomy/evidence.py`._

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["EvidenceResolutionError (backend/app/autonomy/evidence.py)"]
    n1["ValueError"]
    n2["EvidenceResolver._resolve_linked_evidence (backend/app/autonomy/evidence.py)"]
    n3["EvidenceResolver.resolve (backend/app/autonomy/evidence.py)"]
    n4["backend/tests/autonomy/test_autonomy_foundation.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/evidence.md"
    click n2 "../modules/evidence.md"
    click n3 "../modules/evidence.md"
    click n4 "../modules/test_autonomy_foundation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [evidence](../modules/evidence.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `ValueError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `EvidenceResolver._resolve_linked_evidence` | call | [evidence](../modules/evidence.md) | 5 |
| `EvidenceResolver.resolve` | call | [evidence](../modules/evidence.md) | 14 |
| `test_autonomy_foundation` | import | [test_autonomy_foundation](../modules/test_autonomy_foundation.md) | — |
