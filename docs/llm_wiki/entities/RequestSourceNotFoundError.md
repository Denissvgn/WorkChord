# RequestSourceNotFoundError

**Location:** `backend/app/services/request_source_service.py:27`
**Kind:** Class
**Bases:** `LookupError`
**Module:** [request_source_service](../modules/request_source_service.md)

## Description

Raised when a request source or link cannot be found.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RequestSourceNotFoundError (backend/app/services/request_source_service.py)"]
    n1["LookupError"]
    n2["backend/app/routers/request_sources.py"]
    n3["RequestSourceService._get_source_or_raise (backend/app/services/request_source_service.py)"]
    n4["RequestSourceService.create_link (backend/app/services/request_source_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/request_source_service.md"
    click n2 "../modules/request_sources.md"
    click n3 "../modules/request_source_service.md"
    click n4 "../modules/request_source_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [request_source_service](../modules/request_source_service.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `LookupError` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `request_sources` | import | [request_sources](../modules/request_sources.md) | — |
| `RequestSourceService._get_source_or_raise` | call | [request_source_service](../modules/request_source_service.md) | 1 |
| `RequestSourceService.create_link` | call | [request_source_service](../modules/request_source_service.md) | 1 |
