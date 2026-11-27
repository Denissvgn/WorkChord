# TaskReviewHistory Module

**Path:** `frontend/src/components/tasks/TaskReviewHistory.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskReviewHistory.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/taskService` | `taskService` | — | compiler-dependent |
| `../../types/task` | `Task`, `TaskReviewRecord` | Declaration | erased |
| `../../utils/formatDate` | `formatDateTime` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskReviewHistory` |
| Constants | `PAGE_SIZE` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/feedback/QueryState.tsx"]
    n1["frontend/src/components/tasks/TaskReviewHistory.tsx"]
    n2["frontend/src/components/tasks/TaskWorkPanel.tsx"]
    n3["frontend/src/services/taskService.ts"]
    n4["frontend/src/types/task.ts"]
    n5["frontend/src/utils/formatDate.ts"]
    n1 --> n0
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n3 --> n4
    click n0 "../modules/QueryState.md"
    click n1 "../modules/TaskReviewHistory.md"
    click n2 "../modules/TaskWorkPanel.md"
    click n3 "../modules/taskService.md"
    click n4 "../modules/types_task.md"
    click n5 "../modules/formatDate.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskWorkPanel](../modules/TaskWorkPanel.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [formatDate](../modules/formatDate.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskReviewHistory` | `({ task }: { task: Task })` | — | Every recorded review of the task, newest first. An owner override is labelled, never shown as an independent review. |
