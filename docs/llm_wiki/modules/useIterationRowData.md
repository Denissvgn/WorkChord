# useIterationRowData Module

**Path:** `frontend/src/components/tasks/useIterationRowData.ts`

## Description

_Auto-generated from `frontend/src/components/tasks/useIterationRowData.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/taskService` | `taskService` | — | compiler-dependent |
| `../../services/teamService` | `teamService` | — | compiler-dependent |
| `../../types/task` | `Task` | Declaration | erased |
| `./TaskRow` | `TaskRowAssigneeOption` | Declaration | erased |
| `./useTaskRowEdits` | `assigneeOptionsFrom` | — | compiler-dependent |
| `@tanstack/react-query` | `useQueries` | — | compiler-dependent |
| `react` | `useMemo` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `useIterationRowData` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/projects/ProjectTaskTree.tsx"]
    n1["frontend/src/components/tasks/TaskRow.tsx"]
    n2["frontend/src/components/tasks/useIterationRowData.ts"]
    n3["frontend/src/components/tasks/useTaskRowEdits.ts"]
    n4["frontend/src/pages/MyWorkPage.tsx"]
    n5["frontend/src/services/taskService.ts"]
    n6["frontend/src/services/teamService.ts"]
    n7["frontend/src/types/task.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n7
    n1 --> n7
    n2 --> n1
    n2 --> n3
    n2 --> n5
    n2 --> n6
    n2 --> n7
    n3 --> n1
    n3 --> n5
    n3 --> n6
    n3 --> n7
    n4 --> n1
    n4 --> n2
    n4 --> n3
    n4 --> n7
    n5 --> n7
    click n0 "../modules/ProjectTaskTree.md"
    click n1 "../modules/TaskRow.md"
    click n2 "../modules/useIterationRowData.md"
    click n3 "../modules/useTaskRowEdits.md"
    click n4 "../modules/MyWorkPage.md"
    click n5 "../modules/taskService.md"
    click n6 "../modules/teamService.md"
    click n7 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ProjectTaskTree](../modules/ProjectTaskTree.md) |
| Inbound | [MyWorkPage](../modules/MyWorkPage.md) |
| Outbound | [TaskRow](../modules/TaskRow.md) |
| Outbound | [useTaskRowEdits](../modules/useTaskRowEdits.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [teamService](../modules/teamService.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useIterationRowData` | `(iterationIds: (number \| null \| undefined)[], { loadTasks = true }: { loadTasks?: boolean } = {})` | — | What rows of several iterations need that a task reference does not carry, loaded the way the |
