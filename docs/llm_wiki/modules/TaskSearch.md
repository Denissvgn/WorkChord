# TaskSearch Module

**Path:** `frontend/src/components/tasks/TaskSearch.tsx`

## Description

Searches authorized title/ID projections with bounded pagination and project/iteration context. The query stays in the URL and opening a result retains the surrounding view parameters.

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/taskService` | `taskService` |
| `../common/Button` | `Button` |
| `../feedback/QueryState` | `QueryErrorState` |
| `@tanstack/react-query` | `useInfiniteQuery` |
| `react` | `useEffect`, `useId`, `useState` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `Link`, `useSearchParams` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskSearch` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/feedback/QueryState.tsx"]
    n2["frontend/src/components/tasks/TaskSearch.tsx"]
    n3["frontend/src/pages/TasksPage.tsx"]
    n4["frontend/src/services/taskService.ts"]
    n1 --> n0
    n2 --> n0
    n2 --> n1
    n2 --> n4
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n4
    click n0 "../modules/Button.md"
    click n1 "../modules/QueryState.md"
    click n2 "../modules/TaskSearch.md"
    click n3 "../modules/TasksPage.md"
    click n4 "../modules/taskService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TasksPage](../modules/TasksPage.md) |
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
| `TaskSearch` | `()` | — | — |
