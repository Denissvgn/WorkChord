# SavedViewDuplicateRequest

**Location:** `backend/app/schemas/saved_view.py:95`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_saved_view](../modules/schemas_saved_view.md)

## Description

Public API payload for duplicating an existing saved view.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `name` | `Optional[str]` | `name` | No | Yes | `None` | max_length=255; min_length=1 | — | — |
| `description` | `Optional[str]` | `description` | No | Yes | `None` | — | — | — |
| `scope` | `SavedViewScope` | `scope` | No | No | `SavedViewScope.PERSONAL` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SavedViewDuplicateRequest (backend/app/schemas/saved_view.py)"]
    n1["BaseModel"]
    n2["duplicate_saved_view (backend/app/routers/saved_views.py)"]
    n3["backend/app/schemas/__init__.py"]
    n4["SavedViewService.duplicate_for_session (backend/app/services/saved_view_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_saved_view.md"
    click n2 "../modules/saved_views.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/saved_view_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_saved_view](../modules/schemas_saved_view.md) | 0 | `description`, `name`, `scope` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `duplicate_saved_view` | type_reference | [saved_views](../modules/saved_views.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `SavedViewService.duplicate_for_session` | type_reference | [saved_view_service](../modules/saved_view_service.md) | — |
