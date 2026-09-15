# task_context_revision_service Module

**Path:** `backend/app/services/task_context_revision_service.py`

## Description

Atomic task-version fencing for relationship-backed execution context.

Relationship-backed execution context uses the same iteration-before-task lock order, snapshot transaction and task version reservation as ordinary task commands. Context changes append evidence without owning an independent commit inside a transport command.

## Imports

| Source | Symbols |
|--------|---------|
| `app.commands` | `command_transaction` |
| `app.models.agent` | `TaskEvent` |
| `app.models.task` | `Task` |
| `app.services.snapshot_service` | `SnapshotService` |
| `app.services.task_service` | `TaskService`, `TaskService`, `TaskVersionConflictError` |
| `json` | `json` |
| `sqlalchemy` | `select` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `typing` | `Any` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/commands.py"]
    n1["backend/app/mcp_agent_tools.py"]
    n2["backend/app/models/agent.py"]
    n3["backend/app/models/task.py"]
    n4["backend/app/services/external_link_service.py"]
    n5["backend/app/services/github_status_service.py"]
    n6["backend/app/services/github_webhook_service.py"]
    n7["backend/app/services/request_source_service.py"]
    n8["backend/app/services/snapshot_service.py"]
    n9["backend/app/services/task_context_revision_service.py"]
    n10["backend/app/services/task_service.py"]
    n0 --> n3
    n0 --> n8
    n0 --> n10
    n1 --> n0
    n1 --> n2
    n1 --> n4
    n1 --> n7
    n1 --> n9
    n1 --> n10
    n2 --> n3
    n3 --> n2
    n4 --> n0
    n4 --> n3
    n4 --> n9
    n5 --> n0
    n5 --> n4
    n5 --> n9
    n6 --> n0
    n6 --> n2
    n6 --> n5
    n6 --> n9
    n6 --> n10
    n7 --> n0
    n7 --> n3
    n7 --> n9
    n8 --> n0
    n9 --> n0
    n9 --> n2
    n9 --> n3
    n9 --> n8
    n9 --> n10
    n10 --> n0
    n10 --> n2
    n10 --> n3
    n10 --> n4
    n10 --> n8
    click n0 "../modules/commands.md"
    click n1 "../modules/mcp_agent_tools.md"
    click n2 "../modules/models_agent.md"
    click n3 "../modules/models_task.md"
    click n4 "../modules/external_link_service.md"
    click n5 "../modules/github_status_service.md"
    click n6 "../modules/github_webhook_service.md"
    click n7 "../modules/request_source_service.md"
    click n8 "../modules/snapshot_service.md"
    click n9 "../modules/task_context_revision_service.md"
    click n10 "../modules/task_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [external_link_service](../modules/external_link_service.md) |
| Inbound | [github_status_service](../modules/github_status_service.md) |
| Inbound | [github_webhook_service](../modules/github_webhook_service.md) |
| Inbound | [request_source_service](../modules/request_source_service.md) |
| Outbound | [commands](../modules/commands.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [models_task](../modules/models_task.md) |
| Outbound | [snapshot_service](../modules/snapshot_service.md) |
| Outbound | [task_service](../modules/task_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TaskContextVersionConflictError](../entities/TaskContextVersionConflictError.md) | 14 | `RuntimeError` | Raised when another transaction reserves the task context version first. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `lock_task_context` | *(async)* `(db: AsyncSession, task_id: int) -> bool` | — | Lock the iteration before task context, including SQLite's writer reservation. |
| `reserve_task_context_revision` | *(async)* `(db: AsyncSession, task_id: int, *, context_kind: str, action: str, details: dict[str, Any] \| None = None) -> int \| None` | — | Reserve the shared task version and append context evidence under its command owner. |
