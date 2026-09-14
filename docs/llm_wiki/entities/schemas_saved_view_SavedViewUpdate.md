# SavedViewUpdate

**Location:** `backend/app/schemas/saved_view.py:45`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_saved_view](../modules/schemas_saved_view.md)

## Description

Schema for updating a saved view.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `require_creator_when_setting_personal_scope` | model | — | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `name` | `Optional[str]` | `name` | No | Yes | `None` | min_length=1; max_length=255 | — | — |
| `description` | `Optional[str]` | `description` | No | Yes | `None` | — | — | — |
| `view_type` | `Optional[SavedViewType]` | `view_type` | No | Yes | `None` | — | — | — |
| `scope` | `Optional[SavedViewScope]` | `scope` | No | Yes | `None` | — | — | — |
| `filters_json` | `Optional[dict[str, Any]]` | `filters_json` | No | Yes | `None` | — | — | — |
| `sort_json` | `Optional[dict[str, Any]]` | `sort_json` | No | Yes | `None` | — | — | — |
| `columns_json` | `Optional[dict[str, Any]]` | `columns_json` | No | Yes | `None` | — | — | — |
| `created_by_session_id` | `Optional[int]` | `created_by_session_id` | No | Yes | `None` | — | — | — |
| `schema_version` | `Optional[int]` | `schema_version` | No | Yes | `None` | ge=1 | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `require_creator_when_setting_personal_scope` | `() -> 'SavedViewUpdate'` | `@model_validator(mode='after')` | Changing a view to personal scope must include a creator session. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SavedViewUpdate (backend/app/schemas/saved_view.py)"]
    n1["BaseModel"]
    n2["backend/app/schemas/__init__.py"]
    n3["SavedViewUpdate.require_creator_when_setting_personal_scope (backend/app/schemas/saved_view.py)"]
    n4["SavedViewService.update (backend/app/services/saved_view_service.py)"]
    n5["SavedViewService.update_for_session (backend/app/services/saved_view_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/schemas_saved_view.md"
    click n2 "../modules/schemas___init__.md"
    click n3 "../modules/schemas_saved_view.md"
    click n4 "../modules/saved_view_service.md"
    click n5 "../modules/saved_view_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_saved_view](../modules/schemas_saved_view.md) | 1 | `columns_json`, `created_by_session_id`, `description`, `filters_json`, `name`, `schema_version`, `scope`, `sort_json`, `view_type` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `SavedViewUpdate.require_creator_when_setting_personal_scope` | type_reference | [schemas_saved_view](../modules/schemas_saved_view.md) | — |
| `SavedViewService.update` | type_reference | [saved_view_service](../modules/saved_view_service.md) | — |
| `SavedViewService.update_for_session` | call | [saved_view_service](../modules/saved_view_service.md) | 1 |
| `SavedViewService.update_for_session` | type_reference | [saved_view_service](../modules/saved_view_service.md) | — |
