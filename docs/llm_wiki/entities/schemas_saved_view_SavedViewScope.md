# SavedViewScope

**Location:** `backend/app/schemas/saved_view.py:16`
**Kind:** Enum
**Bases:** `str`, `Enum`
**Module:** [schemas_saved_view](../modules/schemas_saved_view.md)

## Description

Visibility scope for a saved view.

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `PERSONAL` | `'personal'` | — |
| `SHARED` | `'shared'` | — |
| `SYSTEM` | `'system'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SavedViewScope (backend/app/schemas/saved_view.py)"]
    n1["Enum"]
    n2["str"]
    n3["backend/app/schemas/__init__.py"]
    n4["SavedViewService._reject_system_scope (backend/app/services/saved_view_service.py)"]
    n5["SavedViewService._require_personal_creator (backend/app/services/saved_view_service.py)"]
    n0 --> n1
    n0 --> n2
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/schemas_saved_view.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/saved_view_service.md"
    click n5 "../modules/saved_view_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_saved_view](../modules/schemas_saved_view.md) | 0 | `PERSONAL`, `SHARED`, `SYSTEM` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Enum` | — |
| Base | `str` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `SavedViewService._reject_system_scope` | type_reference | [saved_view_service](../modules/saved_view_service.md) | — |
| `SavedViewService._require_personal_creator` | type_reference | [saved_view_service](../modules/saved_view_service.md) | — |
