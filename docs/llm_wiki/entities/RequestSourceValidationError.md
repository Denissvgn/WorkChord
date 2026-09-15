# RequestSourceValidationError

**Location:** `backend/app/services/request_source_service.py:25`
**Kind:** Class
**Bases:** `ValueError`
**Module:** [request_source_service](../modules/request_source_service.md)

## Description

Raised when request-source input is invalid.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RequestSourceValidationError (backend/app/services/request_source_service.py)"]
    n1["ValueError"]
    n2["backend/app/routers/request_sources.py"]
    n3["RequestSourceService._normalize_target_type (backend/app/services/request_source_service.py)"]
    n4["RequestSourceService._target_model_and_field (backend/app/services/request_source_service.py)"]
    n5["RequestSourceService.create_link (backend/app/services/request_source_service.py)"]
    n6["RequestSourceService.search_sources (backend/app/services/request_source_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/request_source_service.md"
    click n2 "../modules/request_sources.md"
    click n3 "../modules/request_source_service.md"
    click n4 "../modules/request_source_service.md"
    click n5 "../modules/request_source_service.md"
    click n6 "../modules/request_source_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [request_source_service](../modules/request_source_service.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `ValueError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `request_sources` | import | [request_sources](../modules/request_sources.md) | — |
| `RequestSourceService._normalize_target_type` | call | [request_source_service](../modules/request_source_service.md) | 1 |
| `RequestSourceService._target_model_and_field` | call | [request_source_service](../modules/request_source_service.md) | 1 |
| `RequestSourceService.create_link` | call | [request_source_service](../modules/request_source_service.md) | 1 |
| `RequestSourceService.search_sources` | call | [request_source_service](../modules/request_source_service.md) | 1 |
