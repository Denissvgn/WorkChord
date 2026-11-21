# taskRowValues Module

**Path:** `frontend/src/components/tasks/taskRowValues.ts`

## Description

_Auto-generated from `frontend/src/components/tasks/taskRowValues.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/task` | `Task` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `getEffectiveEffort` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/projects/ProjectTaskTree.tsx"]
    n1["frontend/src/components/tasks/KanbanBoard/KanbanCard.tsx"]
    n2["frontend/src/components/tasks/TaskList.tsx"]
    n3["frontend/src/components/tasks/taskRowValues.ts"]
    n4["frontend/src/pages/MyWorkPage.tsx"]
    n5["frontend/src/types/task.ts"]
    n0 --> n3
    n0 --> n5
    n1 --> n3
    n1 --> n5
    n2 --> n3
    n2 --> n5
    n3 --> n5
    n4 --> n3
    n4 --> n5
    click n0 "../modules/ProjectTaskTree.md"
    click n1 "../modules/KanbanCard.md"
    click n2 "../modules/TaskList.md"
    click n3 "../modules/taskRowValues.md"
    click n4 "../modules/MyWorkPage.md"
    click n5 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ProjectTaskTree](../modules/ProjectTaskTree.md) |
| Inbound | [KanbanCard](../modules/KanbanCard.md) |
| Inbound | [TaskList](../modules/TaskList.md) |
| Inbound | [MyWorkPage](../modules/MyWorkPage.md) |
| Outbound | [types_task](../modules/types_task.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `getEffectiveEffort` | `(task: Task) -> number \| null` | — | The effort a row shows: a parent adds up its children, and one unknown child makes the total unknown. |
