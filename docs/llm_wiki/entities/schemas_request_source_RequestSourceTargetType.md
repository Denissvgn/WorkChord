# RequestSourceTargetType

**Location:** `backend/app/schemas/request_source.py:31`
**Kind:** Enum
**Bases:** `str`, `Enum`
**Module:** [schemas_request_source](../modules/schemas_request_source.md)

## Description

Supported request-source link target types.

## Attributes

| Name | Declared value | Description |
|------|-------|-------------|
| `TASK` | `'task'` | — |
| `PROJECT` | `'project'` | — |
| `TRIAGE_ITEM` | `'triage_item'` | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RequestSourceTargetType (backend/app/schemas/request_source.py)"]
    n1["Enum"]
    n2["str"]
    n3["backend/app/schemas/__init__.py"]
    n4["RequestSourceService._normalize_target_type (backend/app/services/request_source_service.py)"]
    n5["RequestSourceService._require_target_exists (backend/app/services/request_source_service.py)"]
    n6["RequestSourceService._target_model_and_field (backend/app/services/request_source_service.py)"]
    n7["RequestSourceService.list_links_for_target (backend/app/services/request_source_service.py)"]
    n0 --> n1
    n0 --> n2
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/schemas_request_source.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/request_source_service.md"
    click n5 "../modules/request_source_service.md"
    click n6 "../modules/request_source_service.md"
    click n7 "../modules/request_source_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_request_source](../modules/schemas_request_source.md) | 0 | `PROJECT`, `TASK`, `TRIAGE_ITEM` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Enum` | — |
| Base | `str` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `RequestSourceService._normalize_target_type` | call | [request_source_service](../modules/request_source_service.md) | 1 |
| `RequestSourceService._normalize_target_type` | type_reference | [request_source_service](../modules/request_source_service.md) | — |
| `RequestSourceService._require_target_exists` | type_reference | [request_source_service](../modules/request_source_service.md) | — |
| `RequestSourceService._target_model_and_field` | type_reference | [request_source_service](../modules/request_source_service.md) | — |
| `RequestSourceService.list_links_for_target` | type_reference | [request_source_service](../modules/request_source_service.md) | — |
