# BacklogPanel Module

**Path:** `frontend/src/components/tasks/BacklogPanel.tsx`

## Description

Provides project-scoped capture and bounded backlog navigation without inventing an iteration. A project must be chosen for creation, and the shared guarded editor retains task drafts.

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/projectService` | `projectService` |
| `../../services/taskService` | `taskService` |
| `../common/Button` | `Button` |
| `../feedback/QueryState` | `QueryErrorState` |
| `./GuardedTaskModal` | `GuardedTaskModal` |
| `@tanstack/react-query` | `useInfiniteQuery`, `useQuery` |
| `react` | `useId`, `useState` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `Link`, `useSearchParams` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `BacklogPanel` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/feedback/QueryState.tsx"]
    n2["frontend/src/components/tasks/BacklogPanel.tsx"]
    n3["frontend/src/components/tasks/GuardedTaskModal.tsx"]
    n4["frontend/src/pages/TasksPage.tsx"]
    n5["frontend/src/services/projectService.ts"]
    n6["frontend/src/services/taskService.ts"]
    n1 --> n0
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n5
    n2 --> n6
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    n4 --> n6
    click n0 "../modules/Button.md"
    click n1 "../modules/QueryState.md"
    click n2 "../modules/BacklogPanel.md"
    click n3 "../modules/GuardedTaskModal.md"
    click n4 "../modules/TasksPage.md"
    click n5 "../modules/projectService.md"
    click n6 "../modules/taskService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [GuardedTaskModal](../modules/GuardedTaskModal.md) |
| Outbound | [projectService](../modules/projectService.md) |
| Outbound | [taskService](../modules/taskService.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `BacklogPanel` | `()` | — | — |
