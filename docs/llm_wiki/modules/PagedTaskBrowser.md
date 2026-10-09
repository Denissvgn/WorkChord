# PagedTaskBrowser Module

**Path:** `frontend/src/components/tasks/PagedTaskBrowser.tsx`

## Description

The complete-graph error offers ID-ordered task browsing with independent search/status controls and explicit load-more. Loaded references are advisory; planning filters and structural decisions require complete context. URL task selection survives continuation and opens the shared guarded editor. Failed reads hide cached private rows and requests honor cancellation.

_Auto-generated from `frontend/src/components/tasks/PagedTaskBrowser.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../components/feedback/LiveWindowStatus` | `LiveWindowStatus` |
| `../../features/useLiveWindow` | `useLiveWindow` |
| `../../services/taskService` | `taskService` |
| `../common/Button` | `Button` |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` |
| `react` | `useState` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `useSearchParams` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `PagedTaskBrowser` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/feedback/LiveWindowStatus.tsx"]
    n2["frontend/src/components/feedback/QueryState.tsx"]
    n3["frontend/src/components/tasks/KanbanBoard/KanbanBoard.tsx"]
    n4["frontend/src/components/tasks/PagedTaskBrowser.test.tsx"]
    n5["frontend/src/components/tasks/PagedTaskBrowser.tsx"]
    n6["frontend/src/components/tasks/TaskList.tsx"]
    n7["frontend/src/features/useLiveWindow.ts"]
    n8["frontend/src/services/taskService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n3 --> n2
    n3 --> n5
    n3 --> n8
    n4 --> n5
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n7
    n5 --> n8
    n6 --> n0
    n6 --> n2
    n6 --> n5
    n6 --> n8
    click n0 "../modules/Button.md"
    click n1 "../modules/LiveWindowStatus.md"
    click n2 "../modules/QueryState.md"
    click n3 "../modules/KanbanBoard.md"
    click n4 "../modules/PagedTaskBrowser.test.md"
    click n5 "../modules/PagedTaskBrowser.md"
    click n6 "../modules/TaskList.md"
    click n7 "../modules/useLiveWindow.md"
    click n8 "../modules/taskService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [KanbanBoard](../modules/KanbanBoard.md) |
| Inbound | [PagedTaskBrowser.test](../modules/PagedTaskBrowser.test.md) |
| Inbound | [TaskList](../modules/TaskList.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [LiveWindowStatus](../modules/LiveWindowStatus.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [useLiveWindow](../modules/useLiveWindow.md) |
| Outbound | [taskService](../modules/taskService.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `PagedTaskBrowser` | `({ iterationId }: { iterationId: number })` | — | — |