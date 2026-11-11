# TaskReviewer Module

**Path:** `frontend/src/components/tasks/TaskReviewer.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskReviewer.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/taskService` | `taskService` | — | compiler-dependent |
| `../../types/task` | `Task` | Declaration | erased |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskReviewer` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/feedback/QueryState.tsx"]
    n1["frontend/src/components/tasks/TaskReviewer.tsx"]
    n2["frontend/src/components/tasks/TaskWorkPanel.tsx"]
    n3["frontend/src/services/taskService.ts"]
    n4["frontend/src/types/task.ts"]
    n1 --> n0
    n1 --> n3
    n1 --> n4
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n3 --> n4
    click n0 "../modules/QueryState.md"
    click n1 "../modules/TaskReviewer.md"
    click n2 "../modules/TaskWorkPanel.md"
    click n3 "../modules/taskService.md"
    click n4 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskWorkPanel](../modules/TaskWorkPanel.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskReviewer` | `({ task }: { task: Task })` | — | Who reviews submitted work: the agent with the live review assignment, or any authorized person. |
