# TriageDraftNotFoundError

**Location:** `backend/app/services/triage_service.py:50`
**Kind:** Class
**Bases:** `Exception`
**Module:** [triage_service](../modules/triage_service.md)

## Description

Raised when referenced draft context does not exist.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TriageDraftNotFoundError (backend/app/services/triage_service.py)"]
    n1["Exception"]
    n2["backend/app/routers/triage.py"]
    n3["TriageService._get_task_draft_classification (backend/app/services/triage_service.py)"]
    n4["TriageService._get_task_draft_template (backend/app/services/triage_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/triage_service.md"
    click n2 "../modules/routers_triage.md"
    click n3 "../modules/triage_service.md"
    click n4 "../modules/triage_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [triage_service](../modules/triage_service.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Exception` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `triage` | import | [routers_triage](../modules/routers_triage.md) | — |
| `TriageService._get_task_draft_classification` | call | [triage_service](../modules/triage_service.md) | 1 |
| `TriageService._get_task_draft_template` | call | [triage_service](../modules/triage_service.md) | 1 |
