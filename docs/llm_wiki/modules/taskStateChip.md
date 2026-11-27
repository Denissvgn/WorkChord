# taskStateChip Module

**Path:** `frontend/src/components/tasks/taskStateChip.ts`

## Description

_Auto-generated from `frontend/src/components/tasks/taskStateChip.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/task` | `Task`, `TaskStatus` | Declaration | erased |
| `../../utils/taskState` | `isStoppedState`, `stateOf` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskStateChip`, `isDone`, `taskStateChip` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/projects/ProjectTaskTree.tsx"]
    n1["frontend/src/components/tasks/KanbanBoard/KanbanCard.tsx"]
    n2["frontend/src/components/tasks/StoppedWork.test.tsx"]
    n3["frontend/src/components/tasks/TaskList.tsx"]
    n4["frontend/src/components/tasks/TaskRow.tsx"]
    n5["frontend/src/components/tasks/taskRowParts.tsx"]
    n6["frontend/src/components/tasks/taskStateChip.ts"]
    n7["frontend/src/pages/MyWorkPage.tsx"]
    n8["frontend/src/types/task.ts"]
    n9["frontend/src/utils/taskState.ts"]
    n0 --> n4
    n0 --> n6
    n0 --> n8
    n0 --> n9
    n1 --> n5
    n1 --> n6
    n1 --> n8
    n2 --> n4
    n2 --> n6
    n2 --> n8
    n3 --> n4
    n3 --> n6
    n3 --> n8
    n3 --> n9
    n4 --> n5
    n4 --> n6
    n4 --> n8
    n4 --> n9
    n5 --> n6
    n6 --> n8
    n6 --> n9
    n7 --> n4
    n7 --> n6
    n7 --> n8
    n7 --> n9
    n9 --> n8
    click n0 "../modules/ProjectTaskTree.md"
    click n1 "../modules/KanbanCard.md"
    click n2 "../modules/StoppedWork.test.md"
    click n3 "../modules/TaskList.md"
    click n4 "../modules/TaskRow.md"
    click n5 "../modules/taskRowParts.md"
    click n6 "../modules/taskStateChip.md"
    click n7 "../modules/MyWorkPage.md"
    click n8 "../modules/types_task.md"
    click n9 "../modules/taskState.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ProjectTaskTree](../modules/ProjectTaskTree.md) |
| Inbound | [KanbanCard](../modules/KanbanCard.md) |
| Inbound | [StoppedWork.test](../modules/StoppedWork.test.md) |
| Inbound | [TaskList](../modules/TaskList.md) |
| Inbound | [TaskRow](../modules/TaskRow.md) |
| Inbound | [taskRowParts](../modules/taskRowParts.md) |
| Inbound | [MyWorkPage](../modules/MyWorkPage.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [taskState](../modules/taskState.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskStateChip](../entities/TaskStateChip.md) | Type alias | 5 | <pre><code>&#124; &#123; kind&#58; &#39;blocked&#39; &#125;&#10;    &#124; &#123; kind&#58; &#39;needsDefinition&#39; &#125;&#10;    &#124; &#123; kind&#58; &#39;waits&#39;&#59; count&#58; number &#125;&#10;    &#124; &#123; kind&#58; &#39;ready&#39; &#125;&#10;    &#124; &#123; kind&#58; &#39;inReview&#39; &#125;</code></pre> | The one state a row names, chosen by priority: Blocked, Needs definition, Waits for n, Ready to start, In review. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `isDone` | `(status: TaskStatus \| undefined)` | — | — |
| `taskStateChip` | `(task: Task, taskMap?: Map<number, Task>) -> TaskStateChip \| null` | — | Chooses the single state chip for a task; `taskMap` lets Waits count only the dependencies still open. |
