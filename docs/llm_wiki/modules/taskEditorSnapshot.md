# taskEditorSnapshot Module

**Path:** `frontend/src/components/tasks/taskEditorSnapshot.ts`

## Description

_Auto-generated from `frontend/src/components/tasks/taskEditorSnapshot.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/taskService` | `taskService` |
| `../../types/task` | `Task` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `keepNewestTaskSnapshot`, `readTaskEditorSnapshot` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/GuardedTaskModal.tsx"]
    n1["frontend/src/components/tasks/TaskEditorDrawer.tsx"]
    n2["frontend/src/components/tasks/taskEditorSnapshot.ts"]
    n3["frontend/src/services/taskService.ts"]
    n4["frontend/src/types/task.ts"]
    n0 --> n2
    n0 --> n4
    n1 --> n2
    n1 --> n4
    n2 --> n3
    n2 --> n4
    n3 --> n4
    click n0 "../modules/GuardedTaskModal.md"
    click n1 "../modules/TaskEditorDrawer.md"
    click n2 "../modules/taskEditorSnapshot.md"
    click n3 "../modules/taskService.md"
    click n4 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [GuardedTaskModal](../modules/GuardedTaskModal.md) |
| Inbound | [TaskEditorDrawer](../modules/TaskEditorDrawer.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [types_task](../modules/types_task.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `readTaskEditorSnapshot` | *(async)* `(taskId: number, signal: AbortSignal) -> Promise<Task>` | — | — |
| `keepNewestTaskSnapshot` | `(previous: unknown, next: unknown)` | — | — |
