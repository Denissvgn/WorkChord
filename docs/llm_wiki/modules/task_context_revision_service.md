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
    n0["backend"]
    n1["backend/app/services/task_context_revision_service.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/task_context_revision_service.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (7) |
| Outbound | `backend` (5) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [TaskContextVersionConflictError](../entities/TaskContextVersionConflictError.md) | 14 | `RuntimeError` | Raised when another transaction reserves the task context version first. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `lock_task_context` | *(async)* `(db: AsyncSession, task_id: int) -> bool` | — | Lock the iteration before task context, including SQLite's writer reservation. |
| `reserve_task_context_revision` | *(async)* `(db: AsyncSession, task_id: int, *, context_kind: str, action: str, details: dict[str, Any] \| None = None, preserve_acceptance: bool = False) -> int \| None` | — | Reserve the shared task version and append context evidence under its command owner. |
| `_acceptance_current` | `(task: Task) -> bool` | — | — |
