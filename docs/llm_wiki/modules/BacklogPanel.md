# BacklogPanel Module

**Path:** `frontend/src/components/tasks/BacklogPanel.tsx`

## Description

Provides project-scoped capture and bounded backlog navigation without inventing an iteration. A project must be chosen for creation, and the shared guarded editor retains task drafts.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Select` | `Select` | — | compiler-dependent |
| `../../components/feedback/LiveWindowStatus` | `LiveWindowStatus` | — | compiler-dependent |
| `../../features/scope/useScopeLink` | `useLinkScope`, `useScopeLink` | — | compiler-dependent |
| `../../features/scope/useWorkScope` | `useSetWorkScope` | — | compiler-dependent |
| `../../features/useLiveWindow` | `useLiveWindow` | — | compiler-dependent |
| `../../services/projectService` | `projectService` | — | compiler-dependent |
| `../../services/taskService` | `taskService` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `./GuardedTaskDrawer` | `GuardedTaskDrawer` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `react` | `useId`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link`, `useSearchParams` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `BacklogPanel` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/Select.tsx"]
    n2["frontend/src/components/feedback/LiveWindowStatus.tsx"]
    n3["frontend/src/components/feedback/QueryState.tsx"]
    n4["frontend/src/components/tasks/BacklogPanel.tsx"]
    n5["frontend/src/components/tasks/GuardedTaskDrawer.tsx"]
    n6["frontend/src/features/scope/useScopeLink.ts"]
    n7["frontend/src/features/scope/useWorkScope.ts"]
    n8["frontend/src/features/useLiveWindow.ts"]
    n9["frontend/src/pages/TasksPage.tsx"]
    n10["frontend/src/services/projectService.ts"]
    n11["frontend/src/services/taskService.ts"]
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n4 --> n8
    n4 --> n10
    n4 --> n11
    n5 --> n3
    n9 --> n0
    n9 --> n3
    n9 --> n4
    n9 --> n5
    n9 --> n6
    n9 --> n7
    n9 --> n11
    click n0 "../modules/Button.md"
    click n1 "../modules/Select.md"
    click n2 "../modules/LiveWindowStatus.md"
    click n3 "../modules/QueryState.md"
    click n4 "../modules/BacklogPanel.md"
    click n5 "../modules/GuardedTaskDrawer.md"
    click n6 "../modules/useScopeLink.md"
    click n7 "../modules/useWorkScope.md"
    click n8 "../modules/useLiveWindow.md"
    click n9 "../modules/TasksPage.md"
    click n10 "../modules/projectService.md"
    click n11 "../modules/taskService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Select](../modules/Select.md) |
| Outbound | [LiveWindowStatus](../modules/LiveWindowStatus.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [GuardedTaskDrawer](../modules/GuardedTaskDrawer.md) |
| Outbound | [useScopeLink](../modules/useScopeLink.md) |
| Outbound | [useWorkScope](../modules/useWorkScope.md) |
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
