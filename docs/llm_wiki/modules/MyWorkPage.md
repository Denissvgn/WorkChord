# MyWorkPage Module

**Path:** `frontend/src/pages/MyWorkPage.tsx`

## Description

Presents authenticated human work, independent review and personal inbox queues across authorized projects. It retains task return context and uses the shared guarded editor. Availability, notification state and delivery failures have explicit controls; unlinked profiles, missing membership and unavailable tasks are surfaced rather than inferred.

## Imports

| Source | Symbols |
|--------|---------|
| `../components/common/Button` | `Button` |
| `../components/feedback/QueryState` | `QueryErrorState` |
| `../components/tasks/GuardedTaskModal` | `CurrentTaskModal` |
| `../components/tasks/PersonCapacity` | `PersonCapacity` |
| `../components/ui` | `PageLayout`, `PageHeader` |
| `../features/identity/identityContext` | `useIdentity` |
| `../services/api` | `api` |
| `../services/discussionService` | `discussionService` |
| `../types/task` | `TaskReference`, `TaskReferencePage` |
| `../utils/apiError` | `getApiErrorMessage` |
| `@tanstack/react-query` | `useInfiniteQuery`, `useMutation` |
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
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/feedback/QueryState.tsx"]
    n2["frontend/src/components/tasks/GuardedTaskModal.tsx"]
    n3["frontend/src/components/tasks/PersonCapacity.tsx"]
    n4["frontend/src/components/ui/index.ts"]
    n5["frontend/src/features/identity/identityContext.ts"]
    n6["frontend/src/pages/MyWorkPage.test.tsx"]
    n7["frontend/src/pages/MyWorkPage.tsx"]
    n8["frontend/src/services/api.ts"]
    n9["frontend/src/services/discussionService.ts"]
    n10["frontend/src/types/task.ts"]
    n11["frontend/src/utils/apiError.ts"]
    n1 --> n0
    n1 --> n11
    n2 --> n1
    n2 --> n10
    n3 --> n0
    n3 --> n1
    n3 --> n8
    n3 --> n11
    n6 --> n5
    n6 --> n7
    n6 --> n10
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n4
    n7 --> n5
    n7 --> n8
    n7 --> n9
    n7 --> n10
    n7 --> n11
    n9 --> n8
    click n0 "../modules/Button.md"
    click n1 "../modules/QueryState.md"
    click n2 "../modules/GuardedTaskModal.md"
    click n3 "../modules/PersonCapacity.md"
    click n4 "../modules/index.md"
    click n5 "../modules/identityContext.md"
    click n6 "../modules/MyWorkPage.test.md"
    click n7 "../modules/MyWorkPage.md"
    click n8 "../modules/api.md"
    click n9 "../modules/discussionService.md"
    click n10 "../modules/types_task.md"
    click n11 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [MyWorkPage.test](../modules/MyWorkPage.test.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [GuardedTaskModal](../modules/GuardedTaskModal.md) |
| Outbound | [PersonCapacity](../modules/PersonCapacity.md) |
| Outbound | [index](../modules/index.md) |
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [discussionService](../modules/discussionService.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [WorkPage](../entities/WorkPage.md) | Class | 17 | — | — |
| [Queue](../entities/Queue.md) | Type alias | 16 | — | — |