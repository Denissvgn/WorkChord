# task_status_service Module

**Path:** `backend/app/services/task_status_service.py`

## Description

Task status transitions, roll-up reconciliation, and status reporting.

Retains planned/active/resolved/closed transitions while separating actual UTC start/resolve/accept events from forecast dates and committed baselines. Acceptance requires review authority and is bound to the current task revision; automatic parent roll-up cannot fabricate independent leaf acceptance.

Direct lifecycle changes retain planned, active, resolved and closed values; summaries derive status from children. Human manual starts preserve forecast dates while recording actual UTC events. Independent acceptance is checked before closure. A review-authorized rejection returns work to active without attributing execution to the reviewer and requires fresh progress for subsequent acceptance.

## Imports

| Source | Symbols |
|--------|---------|
| `app.authority` | `AuthorityError` |
| `app.commands` | `atomic_command`, `command_transaction`, `commit_or_flush`, `lock_iterations` |
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
    n0["backend/app/authority.py"]
    n1["backend/app/commands.py"]
    n2["backend/app/models/iteration.py"]
    n3["backend/app/models/task.py"]
    n4["backend/app/models/task_status_log.py"]
    n5["backend/app/query_limits.py"]
    n6["backend/app/services/hierarchy_repair_service.py"]
    n7["backend/app/services/language_service.py"]
    n8["backend/app/services/outbound_webhook_service.py"]
    n9["backend/app/services/task_service.py"]
    n10["backend/app/services/task_status_service.py"]
    n0 --> n3
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n9
    n2 --> n3
    n3 --> n2
    n3 --> n4
    n4 --> n3
    n6 --> n0
    n6 --> n1
    n6 --> n3
    n6 --> n9
    n6 --> n10
    n8 --> n1
    n9 --> n0
    n9 --> n1
    n9 --> n2
    n9 --> n3
    n9 --> n5
    n9 --> n7
    n9 --> n8
    n10 --> n0
    n10 --> n1
    n10 --> n2
    n10 --> n3
    n10 --> n4
    n10 --> n5
    n10 --> n7
    n10 --> n8
    n10 --> n9
    click n0 "../modules/authority.md"
    click n1 "../modules/commands.md"
    click n2 "../modules/models_iteration.md"
    click n3 "../modules/models_task.md"
    click n4 "../modules/task_status_log.md"
    click n5 "../modules/query_limits.md"
    click n6 "../modules/hierarchy_repair_service.md"
    click n7 "../modules/language_service.md"
    click n8 "../modules/outbound_webhook_service.md"
    click n9 "../modules/task_service.md"
    click n10 "../modules/task_status_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [hierarchy_repair_service](../modules/hierarchy_repair_service.md) |
| Outbound | [authority](../modules/authority.md) |
| Outbound | [commands](../modules/commands.md) |
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
| [TaskStatusService](../entities/TaskStatusService.md) | 30 | — | Own status transitions, dependent cascades, and parent reconciliation. |