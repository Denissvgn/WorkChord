# BacklogPanel Module

**Path:** `frontend/src/components/tasks/BacklogPanel.tsx`

## Description

Provides project-scoped capture and bounded backlog navigation without inventing an iteration. A project must be chosen for creation, and the shared guarded editor retains task drafts.

## Imports

| Source | Symbols |
|--------|---------|
| `../../components/feedback/LiveWindowStatus` | `LiveWindowStatus` |
| `../../features/useLiveWindow` | `useLiveWindow` |
| `../../services/projectService` | `projectService` |
| `../../services/taskService` | `taskService` |
| `../common/Button` | `Button` |
| `../feedback/QueryState` | `QueryErrorState` |
| `./GuardedTaskModal` | `GuardedTaskModal` |
| `@tanstack/react-query` | `useQuery` |
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
    n1["frontend/src/components/feedback/LiveWindowStatus.tsx"]
    n2["frontend/src/components/feedback/QueryState.tsx"]
    n3["frontend/src/components/tasks/BacklogPanel.tsx"]
    n4["frontend/src/components/tasks/GuardedTaskModal.tsx"]
    n5["frontend/src/features/useLiveWindow.ts"]
    n6["frontend/src/pages/TasksPage.tsx"]
    n7["frontend/src/services/projectService.ts"]
    n8["frontend/src/services/taskService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n3 --> n7
    n3 --> n8
    n4 --> n2
    n6 --> n0
    n6 --> n2
    n6 --> n3
    n6 --> n4
    n6 --> n8
    click n0 "../modules/Button.md"
    click n1 "../modules/LiveWindowStatus.md"
    click n2 "../modules/QueryState.md"
    click n3 "../modules/BacklogPanel.md"
    click n4 "../modules/GuardedTaskModal.md"
    click n5 "../modules/useLiveWindow.md"
    click n6 "../modules/TasksPage.md"
    click n7 "../modules/projectService.md"
    click n8 "../modules/taskService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [LiveWindowStatus](../modules/LiveWindowStatus.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [GuardedTaskModal](../modules/GuardedTaskModal.md) |
| Outbound | [useLiveWindow](../modules/useLiveWindow.md) |
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