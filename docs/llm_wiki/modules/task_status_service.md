# task_status_service Module

**Path:** `backend/app/services/task_status_service.py`

## Description

Task status transitions, roll-up reconciliation, and status reporting.

## Imports

| Source | Symbols |
|--------|---------|
| `app.models.iteration` | `Iteration` |
| `app.models.task` | `Task`, `TaskDependency`, `TaskStatus` |
| `app.models.task_status_log` | `TaskStatusLog` |
| `app.query_limits` | `CollectionLimitExceededError`, `MAX_BOUNDED_LIST_ITEMS` |
| `app.services.language_service` | `automatic_child_status_reason`, `incomplete_dependency_message`, `resolve_runtime_ui_language`, `task_requires_schedule_message` |
| `app.services.outbound_webhook_service` | `OutboundWebhookService` |
| `app.services.task_service` | `TaskService` |
| `datetime` | `date`, `timedelta` |
| `json` | `json` |
| `sqlalchemy` | `desc`, `func`, `select` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `sqlalchemy.orm` | `selectinload` |
| `typing` | `Any`, `Optional`, `Sequence`, `TYPE_CHECKING` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/models/iteration.py"]
    n1["backend/app/models/task.py"]
    n2["backend/app/models/task_status_log.py"]
    n3["backend/app/query_limits.py"]
    n4["backend/app/services/language_service.py"]
    n5["backend/app/services/outbound_webhook_service.py"]
    n6["backend/app/services/task_service.py"]
    n7["backend/app/services/task_status_service.py"]
    n0 --> n1
    n1 --> n0
    n1 --> n2
    n2 --> n1
    n6 --> n0
    n6 --> n1
    n6 --> n3
    n6 --> n4
    n6 --> n5
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n4
    n7 --> n5
    n7 --> n6
    click n0 "../modules/models_iteration.md"
    click n1 "../modules/models_task.md"
    click n2 "../modules/task_status_log.md"
    click n3 "../modules/query_limits.md"
    click n4 "../modules/language_service.md"
    click n5 "../modules/outbound_webhook_service.md"
    click n6 "../modules/task_service.md"
    click n7 "../modules/task_status_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [models_iteration](../modules/models_iteration.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [task_status_log](../modules/task_status_log.md) |
| Outbound | [query_limits](../modules/query_limits.md) |
| Outbound | [language_service](../modules/language_service.md) |
| Outbound | [outbound_webhook_service](../modules/outbound_webhook_service.md) |
| Outbound | [task_service](../modules/task_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TaskStatusService](../entities/TaskStatusService.md) | 27 | — | Own status transitions, dependent cascades, and parent reconciliation. |
