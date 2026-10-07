# PagedTaskBrowser Module

**Path:** `frontend/src/components/tasks/PagedTaskBrowser.tsx`

## Description

The complete-graph error offers ID-ordered task browsing with independent search/status controls and explicit load-more. Loaded references are advisory; planning filters and structural decisions require complete context. URL task selection survives continuation and opens the shared guarded editor. Failed reads hide cached private rows and requests honor cancellation.

_Auto-generated from `frontend/src/components/tasks/PagedTaskBrowser.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/taskService` | `taskService` |
| `../common/Button` | `Button` |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` |
| `@tanstack/react-query` | `useInfiniteQuery` |
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
    n1["frontend/src/components/feedback/QueryState.tsx"]
    n2["frontend/src/components/tasks/KanbanBoard/KanbanBoard.tsx"]
    n3["frontend/src/components/tasks/PagedTaskBrowser.test.tsx"]
    n4["frontend/src/components/tasks/PagedTaskBrowser.tsx"]
    n5["frontend/src/components/tasks/TaskList.tsx"]
    n6["frontend/src/services/taskService.ts"]
    n1 --> n0
    n2 --> n0
    n2 --> n1
    n2 --> n4
    n2 --> n6
    n3 --> n4
    n4 --> n0
    n4 --> n1
    n4 --> n6
    n5 --> n0
    n5 --> n1
    n5 --> n4
    n5 --> n6
    click n0 "../modules/Button.md"
    click n1 "../modules/QueryState.md"
    click n2 "../modules/KanbanBoard.md"
    click n3 "../modules/PagedTaskBrowser.test.md"
    click n4 "../modules/PagedTaskBrowser.md"
    click n5 "../modules/TaskList.md"
    click n6 "../modules/taskService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [KanbanBoard](../modules/KanbanBoard.md) |
| Inbound | [PagedTaskBrowser.test](../modules/PagedTaskBrowser.test.md) |
| Inbound | [TaskList](../modules/TaskList.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [taskService](../modules/taskService.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `PagedTaskBrowser` | `({ iterationId }: { iterationId: number })` | — | — |
