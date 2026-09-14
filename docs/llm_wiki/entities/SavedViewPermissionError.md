# SavedViewPermissionError

**Location:** `backend/app/services/saved_view_service.py:24`
**Kind:** Class
**Bases:** `PermissionError`
**Module:** [saved_view_service](../modules/saved_view_service.md)

## Description

Raised when a session cannot mutate a saved view.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SavedViewPermissionError (backend/app/services/saved_view_service.py)"]
    n1["PermissionError"]
    n2["backend/app/routers/saved_views.py"]
    n3["SavedViewService._reject_system_scope (backend/app/services/saved_view_service.py)"]
    n4["SavedViewService.delete_for_session (backend/app/services/saved_view_service.py)"]
    n5["SavedViewService.update_for_session (backend/app/services/saved_view_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/saved_view_service.md"
    click n2 "../modules/saved_views.md"
    click n3 "../modules/saved_view_service.md"
    click n4 "../modules/saved_view_service.md"
    click n5 "../modules/saved_view_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [saved_view_service](../modules/saved_view_service.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `PermissionError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `saved_views` | import | [saved_views](../modules/saved_views.md) | — |
| `SavedViewService._reject_system_scope` | call | [saved_view_service](../modules/saved_view_service.md) | 1 |
| `SavedViewService.delete_for_session` | call | [saved_view_service](../modules/saved_view_service.md) | 1 |
| `SavedViewService.update_for_session` | call | [saved_view_service](../modules/saved_view_service.md) | 1 |
