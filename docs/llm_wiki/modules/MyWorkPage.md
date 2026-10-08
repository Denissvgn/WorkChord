# MyWorkPage Module

**Path:** `frontend/src/pages/MyWorkPage.tsx`

## Description

Presents authenticated human work, independent review and personal inbox queues across authorized projects. It retains task return context and uses the shared guarded editor. Availability, notification state and delivery failures have explicit controls; unlinked profiles, missing membership and unavailable tasks are surfaced rather than inferred.

## Imports

| Source | Symbols |
|--------|---------|
| `../components/common/Button` | `Button` |
| `../components/feedback/QueryState` | `QueryErrorState` |
| `../components/tasks/GuardedTaskModal` | `GuardedTaskModal` |
| `../components/tasks/PersonCapacity` | `PersonCapacity` |
| `../components/ui` | `PageLayout`, `PageHeader` |
| `../features/identity/identityContext` | `useIdentity` |
| `../services/api` | `api` |
| `../services/discussionService` | `discussionService` |
| `../services/taskService` | `taskService` |
| `../types/task` | `TaskReference`, `TaskReferencePage` |
| `../utils/apiError` | `getApiErrorMessage` |
| `@tanstack/react-query` | `useInfiniteQuery`, `useMutation`, `useQuery` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `useSearchParams` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |
| Constants | `QUEUES` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/pages/MyWorkPage.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/MyWorkPage.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (1) |
| Outbound | `frontend` (11) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [WorkPage](../entities/WorkPage.md) | Class | 18 | — | — |
| [Queue](../entities/Queue.md) | Type alias | 17 | — | — |
