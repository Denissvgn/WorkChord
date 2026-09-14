# release_service Module

**Path:** `backend/app/services/release_service.py`

## Description

Release service for project-scoped shipping records.

## Imports

| Source | Symbols |
|--------|---------|
| `app.models.agent` | `TaskEvent` |
| `app.models.project` | `Project` |
| `app.models.release` | `Release`, `ReleaseStatus` |
| `app.models.task` | `Task` |
| `app.query_limits` | `CollectionLimitExceededError`, `MAX_BOUNDED_LIST_ITEMS` |
| `app.schemas.release` | `ReleaseCreateRequest`, `ReleaseUpdateRequest` |
| `app.services.outbound_webhook_service` | `emit_outbound_webhook_event` |
| `app.services.task_service` | `TaskService` |
| `app.utils.time` | `utc_now` |
| `datetime` | `datetime` |
| `sqlalchemy` | `select` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `sqlalchemy.orm` | `selectinload` |
| `typing` | `Optional`, `Sequence` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/mcp_agent_tools.py"]
    n1["backend/app/models/agent.py"]
    n2["backend/app/models/project.py"]
    n3["backend/app/models/release.py"]
    n4["backend/app/models/task.py"]
    n5["backend/app/query_limits.py"]
    n6["backend/app/routers/projects.py"]
    n7["backend/app/schemas/release.py"]
    n8["backend/app/services/outbound_webhook_service.py"]
    n9["backend/app/services/release_service.py"]
    n10["backend/app/services/task_service.py"]
    n11["backend/app/utils/time.py"]
    n0 --> n1
    n0 --> n7
    n0 --> n9
    n0 --> n10
    n1 --> n2
    n1 --> n4
    n1 --> n11
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n2 --> n11
    n3 --> n2
    n3 --> n4
    n3 --> n11
    n4 --> n1
    n4 --> n2
    n4 --> n11
    n6 --> n5
    n6 --> n7
    n6 --> n9
    n6 --> n10
    n8 --> n11
    n9 --> n1
    n9 --> n2
    n9 --> n3
    n9 --> n4
    n9 --> n5
    n9 --> n7
    n9 --> n8
    n9 --> n10
    n9 --> n11
    n10 --> n1
    n10 --> n2
    n10 --> n4
    n10 --> n5
    n10 --> n8
    click n0 "../modules/mcp_agent_tools.md"
    click n1 "../modules/models_agent.md"
    click n2 "../modules/models_project.md"
    click n3 "../modules/models_release.md"
    click n4 "../modules/models_task.md"
    click n5 "../modules/query_limits.md"
    click n6 "../modules/projects.md"
    click n7 "../modules/schemas_release.md"
    click n8 "../modules/outbound_webhook_service.md"
    click n9 "../modules/release_service.md"
    click n10 "../modules/task_service.md"
    click n11 "../modules/time.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [projects](../modules/projects.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [models_project](../modules/models_project.md) |
| Outbound | [models_release](../modules/models_release.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [query_limits](../modules/query_limits.md) |
| Outbound | [schemas_release](../modules/schemas_release.md) |
| Outbound | [outbound_webhook_service](../modules/outbound_webhook_service.md) |
| Outbound | [task_service](../modules/task_service.md) |
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [ReleaseService](../entities/ReleaseService.md) | 23 | — | Service for release CRUD and task link validation. |
