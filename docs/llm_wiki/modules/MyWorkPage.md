# MyWorkPage Module

**Path:** `frontend/src/pages/MyWorkPage.tsx`

## Description

Presents authenticated human work, independent review and personal inbox queues across authorized projects. It retains task return context and uses the shared guarded editor. Availability, notification state and delivery failures have explicit controls; unlinked profiles, missing membership and unavailable tasks are surfaced rather than inferred.

Only the selected work/review/inbox consumers remain enabled. Paged queues use retained windows and independent head discovery; latest-window navigation preserves task selection. Closing an editor refreshes only the relevant enabled queue.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/common/Button` | `Button` | — | compiler-dependent |
| `../components/feedback/LiveWindowStatus` | `LiveWindowStatus` | — | compiler-dependent |
| `../components/feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `../components/tasks/GuardedTaskModal` | `CurrentTaskModal` | — | compiler-dependent |
| `../components/tasks/PersonCapacity` | `PersonCapacity` | — | compiler-dependent |
| `../components/ui` | `PageLayout`, `PageHeader` | — | compiler-dependent |
| `../features/identity/LocalProfilePicker` | `LocalProfilePicker` | — | compiler-dependent |
| `../features/identity/identityContext` | `useIdentity` | — | compiler-dependent |
| `../features/useLiveWindow` | `useLiveWindow` | — | compiler-dependent |
| `../services/api` | `api` | — | compiler-dependent |
| `../services/discussionService` | `discussionService` | — | compiler-dependent |
| `../types/task` | `TaskReference`, `TaskReferencePage` | Declaration | erased |
| `../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `useSearchParams` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |
| Constants | `QUEUES`, `WORK_QUEUES` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

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
| Outbound | `frontend` (13) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

> All 14 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [WorkPage](../entities/WorkPage.md) | Interface | 21 | — | — |
| [Queue](../entities/Queue.md) | Type alias | 20 | `typeof QUEUES[number]` | — |