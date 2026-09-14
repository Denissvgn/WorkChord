# RequestSourceConflictError

**Location:** `backend/app/services/request_source_service.py:35`
**Kind:** Class
**Bases:** `ValueError`
**Module:** [request_source_service](../modules/request_source_service.md)

## Description

Raised when a source is already linked to the target.

## Attributes

*No annotated attributes found.*

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RequestSourceConflictError (backend/app/services/request_source_service.py)"]
    n1["ValueError"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["backend/app/routers/request_sources.py"]
    n4["RequestSourceService.create_link (backend/app/services/request_source_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/request_source_service.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/request_sources.md"
    click n4 "../modules/request_source_service.md"
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
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `request_sources` | import | [request_sources](../modules/request_sources.md) | — |
| `RequestSourceService.create_link` | call | [request_source_service](../modules/request_source_service.md) | 1 |
