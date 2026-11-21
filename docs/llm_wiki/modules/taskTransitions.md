# taskTransitions Module

**Path:** `frontend/src/features/taskTransitions.ts`

## Description

_Auto-generated from `frontend/src/features/taskTransitions.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../types/task` | `TaskStatus` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TASK_TRANSITIONS`, `canTransition` |
| Constants | `TASK_TRANSITIONS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/KanbanBoard/KanbanBoard.tsx"]
    n1["frontend/src/components/tasks/StatusChangeControl.tsx"]
    n2["frontend/src/components/tasks/TaskRow.tsx"]
    n3["frontend/src/components/tasks/useTaskRowEdits.ts"]
    n4["frontend/src/features/taskTransitions.test.ts"]
    n5["frontend/src/features/taskTransitions.ts"]
    n6["frontend/src/types/task.ts"]
    n0 --> n5
    n0 --> n6
    n1 --> n5
    n1 --> n6
    n2 --> n5
    n2 --> n6
    n3 --> n2
    n3 --> n5
    n3 --> n6
    n4 --> n5
    n5 --> n6
    click n0 "../modules/KanbanBoard.md"
    click n1 "../modules/StatusChangeControl.md"
    click n2 "../modules/TaskRow.md"
    click n3 "../modules/useTaskRowEdits.md"
    click n4 "../modules/taskTransitions.test.md"
    click n5 "../modules/taskTransitions.md"
    click n6 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [KanbanBoard](../modules/KanbanBoard.md) |
| Inbound | [StatusChangeControl](../modules/StatusChangeControl.md) |
| Inbound | [TaskRow](../modules/TaskRow.md) |
| Inbound | [useTaskRowEdits](../modules/useTaskRowEdits.md) |
| Inbound | [taskTransitions.test](../modules/taskTransitions.test.md) |
| Outbound | [types_task](../modules/types_task.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `canTransition` | `(from: TaskStatus, to: TaskStatus)` | — | — |
