# external_link_service Module

**Path:** `backend/app/services/external_link_service.py`

## Description

External link service.

## Imports

| Source | Symbols |
|--------|---------|
| `app.commands` | `commit_or_flush` |
| `app.models.external_link` | `ExternalLink`, `ExternalLinkEntityType` |
| `app.models.task` | `Task` |
| `app.schemas.external_link` | `ExternalLinkCreate`, `ExternalLinkEntityType`, `ExternalLinkProvider`, `ExternalLinkResponse`, `ExternalLinkUpdate`, `TaskExternalLinkCreate` |
| `app.services.outbound_webhook_service` | `emit_outbound_webhook_event` |
| `app.services.task_context_revision_service` | `reserve_task_context_revision` |
| `dataclasses` | `dataclass` |
| `sqlalchemy` | `delete`, `select` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `typing` | `Any`, `Optional`, `Sequence` |
| `urllib.parse` | `urlparse` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/commands.py"]
    n1["backend/app/mcp_agent_tools.py"]
    n2["backend/app/models/external_link.py"]
    n3["backend/app/models/task.py"]
    n4["backend/app/routers/tasks.py"]
    n5["backend/app/schemas/external_link.py"]
    n6["backend/app/services/external_link_service.py"]
    n7["backend/app/services/github_status_service.py"]
    n8["backend/app/services/outbound_webhook_service.py"]
    n9["backend/app/services/task_context_revision_service.py"]
    n10["backend/app/services/task_service.py"]
    n0 --> n3
    n0 --> n10
    n1 --> n0
    n1 --> n6
    n1 --> n9
    n1 --> n10
    n3 --> n2
    n4 --> n0
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n4 --> n10
    n6 --> n0
    n6 --> n2
    n6 --> n3
    n6 --> n5
    n6 --> n8
    n6 --> n9
    n7 --> n0
    n7 --> n2
    n7 --> n6
    n7 --> n9
    n8 --> n0
    n9 --> n0
    n9 --> n3
    n9 --> n10
    n10 --> n0
    n10 --> n3
    n10 --> n6
    n10 --> n8
    click n0 "../modules/commands.md"
    click n1 "../modules/mcp_agent_tools.md"
    click n2 "../modules/models_external_link.md"
    click n3 "../modules/models_task.md"
    click n4 "../modules/tasks.md"
    click n5 "../modules/schemas_external_link.md"
    click n6 "../modules/external_link_service.md"
    click n7 "../modules/github_status_service.md"
    click n8 "../modules/outbound_webhook_service.md"
    click n9 "../modules/task_context_revision_service.md"
    click n10 "../modules/task_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [tasks](../modules/tasks.md) |
| Inbound | [github_status_service](../modules/github_status_service.md) |
| Inbound | [task_service](../modules/task_service.md) |
| Outbound | [commands](../modules/commands.md) |
| Outbound | [models_external_link](../modules/models_external_link.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [schemas_external_link](../modules/schemas_external_link.md) |
| Outbound | [outbound_webhook_service](../modules/outbound_webhook_service.md) |
| Outbound | [task_context_revision_service](../modules/task_context_revision_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [ExternalLinkValidationError](../entities/ExternalLinkValidationError.md) | 25 | `ValueError` | Raised when a provider-specific link cannot be parsed. |
| [ExternalLinkConflictError](../entities/ExternalLinkConflictError.md) | 29 | `Exception` | Raised when a provider-specific link already exists for an entity. |
| [ParsedGitHubLink](../entities/ParsedGitHubLink.md) | 34 | — | Normalized GitHub link details ready for persistence. |
| [ExternalLinkService](../entities/ExternalLinkService.md) | 63 | — | Service for generic external links and task-scoped link operations. |
