# ExternalLinkConflictError

**Location:** `backend/app/services/external_link_service.py:31`
**Kind:** Class
**Bases:** `Exception`
**Module:** [external_link_service](../modules/external_link_service.md)

## Description

Raised when a provider-specific link already exists for an entity.

## Attributes

*No annotated attributes found.*

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ExternalLinkConflictError (backend/app/services/external_link_service.py)"]
    n1["Exception"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["backend/app/routers/tasks.py"]
    n4["ExternalLinkService.create_release_github_link (backend/app/services/external_link_service.py)"]
    n5["ExternalLinkService.create_task_github_link (backend/app/services/external_link_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/external_link_service.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/tasks.md"
    click n4 "../modules/external_link_service.md"
    click n5 "../modules/external_link_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [external_link_service](../modules/external_link_service.md) | 0 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Exception` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `tasks` | import | [tasks](../modules/tasks.md) | — |
| `ExternalLinkService.create_release_github_link` | call | [external_link_service](../modules/external_link_service.md) | 1 |
| `ExternalLinkService.create_task_github_link` | call | [external_link_service](../modules/external_link_service.md) | 1 |
