# SavedViewValidationError

**Location:** `backend/app/services/saved_view_service.py:30`
**Kind:** Class
**Bases:** `ValueError`
**Module:** [saved_view_service](../modules/saved_view_service.md)

## Description

Raised when a saved view payload is invalid.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SavedViewValidationError (backend/app/services/saved_view_service.py)"]
    n1["ValueError"]
    n2["backend/app/routers/saved_views.py"]
    n3["SavedViewService._normalized_system_definition (backend/app/services/saved_view_service.py)"]
    n4["SavedViewService._require_object (backend/app/services/saved_view_service.py)"]
    n5["SavedViewService._require_personal_creator (backend/app/services/saved_view_service.py)"]
    n6["SavedViewService.create (backend/app/services/saved_view_service.py)"]
    n7["SavedViewService.duplicate_for_session (backend/app/services/saved_view_service.py)"]
    n8["SavedViewService.update (backend/app/services/saved_view_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    click n0 "../modules/saved_view_service.md"
    click n2 "../modules/saved_views.md"
    click n3 "../modules/saved_view_service.md"
    click n4 "../modules/saved_view_service.md"
    click n5 "../modules/saved_view_service.md"
    click n6 "../modules/saved_view_service.md"
    click n7 "../modules/saved_view_service.md"
    click n8 "../modules/saved_view_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [saved_view_service](../modules/saved_view_service.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `ValueError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `saved_views` | import | [saved_views](../modules/saved_views.md) | — |
| `SavedViewService._normalized_system_definition` | call | [saved_view_service](../modules/saved_view_service.md) | 2 |
| `SavedViewService._require_object` | call | [saved_view_service](../modules/saved_view_service.md) | 1 |
| `SavedViewService._require_personal_creator` | call | [saved_view_service](../modules/saved_view_service.md) | 1 |
| `SavedViewService.create` | call | [saved_view_service](../modules/saved_view_service.md) | 2 |
| `SavedViewService.duplicate_for_session` | call | [saved_view_service](../modules/saved_view_service.md) | 1 |
| `SavedViewService.update` | call | [saved_view_service](../modules/saved_view_service.md) | 2 |
