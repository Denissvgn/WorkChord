# task_context_revision_service Module

**Path:** `backend/app/services/task_context_revision_service.py`

## Description

Atomic task-version fencing for relationship-backed execution context.

## Imports

| Source | Symbols |
|--------|---------|
| `app.models.agent` | `TaskEvent` |
| `app.models.task` | `Task` |
| `json` | `json` |
| `sqlalchemy` | `select`, `text`, `update` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `sqlalchemy.orm` | `attributes` |
| `typing` | `Any` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/mcp_agent_tools.py"]
    n1["backend/app/models/agent.py"]
    n2["backend/app/models/task.py"]
    n3["backend/app/services/external_link_service.py"]
    n4["backend/app/services/github_status_service.py"]
    n5["backend/app/services/github_webhook_service.py"]
    n6["backend/app/services/request_source_service.py"]
    n7["backend/app/services/task_context_revision_service.py"]
    n0 --> n1
    n0 --> n3
    n0 --> n6
    n0 --> n7
    n1 --> n2
    n2 --> n1
    n3 --> n2
    n3 --> n7
    n4 --> n3
    n4 --> n7
    n5 --> n1
    n5 --> n4
    n5 --> n7
    n6 --> n2
    n6 --> n7
    n7 --> n1
    n7 --> n2
    click n0 "../modules/mcp_agent_tools.md"
    click n1 "../modules/models_agent.md"
    click n2 "../modules/models_task.md"
    click n3 "../modules/external_link_service.md"
    click n4 "../modules/github_status_service.md"
    click n5 "../modules/github_webhook_service.md"
    click n6 "../modules/request_source_service.md"
    click n7 "../modules/task_context_revision_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [external_link_service](../modules/external_link_service.md) |
| Inbound | [github_status_service](../modules/github_status_service.md) |
| Inbound | [github_webhook_service](../modules/github_webhook_service.md) |
| Inbound | [request_source_service](../modules/request_source_service.md) |
| Outbound | [models_agent](../modules/models_agent.md) |
| Outbound | [models_task](../modules/models_task.md) |

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
| `lock_task_context` | *(async)* `(db: AsyncSession, task_id: int) -> bool` | — | Serialize one task-context mutation without changing its version. |
| `reserve_task_context_revision` | *(async)* `(db: AsyncSession, task_id: int, *, context_kind: str, action: str, details: dict[str, Any] \| None = None) -> int \| None` | — | Lock a task, increment its version, and append a server-owned audit event. |
