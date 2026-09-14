# RequestSourceTargetNotFoundError

**Location:** `backend/app/services/request_source_service.py:31`
**Kind:** Class
**Bases:** `LookupError`
**Module:** [request_source_service](../modules/request_source_service.md)

## Description

Raised when a requested link target cannot be found.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RequestSourceTargetNotFoundError (backend/app/services/request_source_service.py)"]
    n1["LookupError"]
    n2["backend/app/routers/request_sources.py"]
    n3["RequestSourceService._require_target_exists (backend/app/services/request_source_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/request_source_service.md"
    click n2 "../modules/request_sources.md"
    click n3 "../modules/request_source_service.md"
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
| `RequestSourceService._require_target_exists` | call | [request_source_service](../modules/request_source_service.md) | 1 |
