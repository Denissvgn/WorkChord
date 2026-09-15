# visibleWork Module

**Path:** `frontend/src/utils/visibleWork.ts`

## Description

_Auto-generated from `frontend/src/utils/visibleWork.ts`._

List and Board use one filtered tree and actionable-leaf projection. Parent context remains discoverable without increasing leaf counts or bringing unmatched siblings into a Board card.

## Imports

| Source | Symbols |
|--------|---------|
| `../components/tasks/TaskFiltersBar` | `TaskFilters` |
| `../types/label` | `LabelGroup` |
| `../types/task` | `Task` |
| `./taskFilters` | `filterTaskWithChildren` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `VisibleLeaf`, `selectVisibleWork` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/KanbanBoard/KanbanBoard.tsx"]
    n1["frontend/src/components/tasks/TaskFiltersBar.tsx"]
    n2["frontend/src/components/tasks/TaskList.tsx"]
    n3["frontend/src/types/label.ts"]
    n4["frontend/src/types/task.ts"]
    n5["frontend/src/utils/taskFilters.ts"]
    n6["frontend/src/utils/visibleWork.test.ts"]
    n7["frontend/src/utils/visibleWork.ts"]
    n0 --> n1
    n0 --> n4
    n0 --> n7
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n2 --> n7
    n5 --> n1
    n5 --> n3
    n5 --> n4
    n6 --> n4
    n6 --> n7
    n7 --> n1
    n7 --> n3
    n7 --> n4
    n7 --> n5
    click n0 "../modules/KanbanBoard.md"
    click n1 "../modules/TaskFiltersBar.md"
    click n2 "../modules/TaskList.md"
    click n3 "../modules/types_label.md"
    click n4 "../modules/types_task.md"
    click n5 "../modules/taskFilters.md"
    click n6 "../modules/visibleWork.test.md"
    click n7 "../modules/visibleWork.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [KanbanBoard](../modules/KanbanBoard.md) |
| Inbound | [TaskList](../modules/TaskList.md) |
| Inbound | [visibleWork.test](../modules/visibleWork.test.md) |
| Outbound | [TaskFiltersBar](../modules/TaskFiltersBar.md) |
| Outbound | [types_label](../modules/types_label.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [taskFilters](../modules/taskFilters.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [VisibleLeaf](../entities/VisibleLeaf.md) | Type alias | 6 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `selectVisibleWork` | `(tasks: Task[], filters: TaskFilters, groups: LabelGroup[] = [])` | — | — |
