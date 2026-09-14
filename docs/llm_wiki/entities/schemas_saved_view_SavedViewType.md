# SavedViewType

**Location:** `backend/app/schemas/saved_view.py:9`
**Kind:** Enum
**Bases:** `str`, `Enum`
**Module:** [schemas_saved_view](../modules/schemas_saved_view.md)

## Description

Surface that a saved view applies to.

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `TASKS` | `'tasks'` | — |
| `PROJECTS` | `'projects'` | — |
| `TRIAGE` | `'triage'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SavedViewType (backend/app/schemas/saved_view.py)"]
    n1["Enum"]
    n2["str"]
    n3["list_saved_views (backend/app/mcp_agent_tools.py)"]
    n4["list_saved_views (backend/app/routers/saved_views.py)"]
    n5["backend/app/schemas/__init__.py"]
    n6["SavedViewService.duplicate_for_session (backend/app/services/saved_view_service.py)"]
    n7["SavedViewService.list_visible (backend/app/services/saved_view_service.py)"]
    n8["SavedViewService.normalize_filters (backend/app/services/saved_view_service.py)"]
    n9["SavedViewService.normalize_sort (backend/app/services/saved_view_service.py)"]
    n10["backend/tests/test_saved_view_service.py"]
    n0 --> n1
    n0 --> n2
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    click n0 "../modules/schemas_saved_view.md"
    click n3 "../modules/mcp_agent_tools.md"
    click n4 "../modules/saved_views.md"
    click n5 "../modules/schemas___init__.md"
    click n6 "../modules/saved_view_service.md"
    click n7 "../modules/saved_view_service.md"
    click n8 "../modules/saved_view_service.md"
    click n9 "../modules/saved_view_service.md"
    click n10 "../modules/test_saved_view_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_saved_view](../modules/schemas_saved_view.md) | 0 | `PROJECTS`, `TASKS`, `TRIAGE` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Enum` | — |
| Base | `str` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `list_saved_views` | call | [mcp_agent_tools](../modules/mcp_agent_tools.md) | 1 |
| `list_saved_views` | type_reference | [saved_views](../modules/saved_views.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `SavedViewService.duplicate_for_session` | call | [saved_view_service](../modules/saved_view_service.md) | 1 |
| `SavedViewService.list_visible` | type_reference | [saved_view_service](../modules/saved_view_service.md) | — |
| `SavedViewService.normalize_filters` | type_reference | [saved_view_service](../modules/saved_view_service.md) | — |
| `SavedViewService.normalize_sort` | type_reference | [saved_view_service](../modules/saved_view_service.md) | — |
| `test_saved_view_service` | import | [test_saved_view_service](../modules/test_saved_view_service.md) | — |
