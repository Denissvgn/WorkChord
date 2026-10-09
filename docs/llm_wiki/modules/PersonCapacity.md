# PersonCapacity Module

**Path:** `frontend/src/components/tasks/PersonCapacity.tsx`

## Description

Displays server-derived daily availability, allocated and productive hours, saved commitments and uncertainty. Person owners can select a calendar and versioned absences. The interface preserves the established design and shows private work only through aggregate capacity.

Person calendar changes retain the opening availability revision across live refreshes. Changed server state requires an explicit current comparison before reapplication; pending absence and calendar writes retain input intent.

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/api` | `api` |
| `../../services/calendarService` | `calendarService` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../common/Button` | `Button` |
| `../feedback/QueryState` | `QueryErrorState` |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` |
| `react` | `useId`, `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `PersonCapacity` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/feedback/QueryState.tsx"]
    n2["frontend/src/components/tasks/PersonCapacity.test.tsx"]
    n3["frontend/src/components/tasks/PersonCapacity.tsx"]
    n4["frontend/src/components/tasks/TaskForm.tsx"]
    n5["frontend/src/pages/MyWorkPage.tsx"]
    n6["frontend/src/services/api.ts"]
    n7["frontend/src/services/calendarService.ts"]
    n8["frontend/src/utils/apiError.ts"]
    n1 --> n0
    n1 --> n8
    n2 --> n3
    n3 --> n0
    n3 --> n1
    n3 --> n6
    n3 --> n7
    n3 --> n8
    n4 --> n0
    n4 --> n1
    n4 --> n3
    n4 --> n8
    n5 --> n0
    n5 --> n1
    n5 --> n3
    n5 --> n6
    n5 --> n8
    n7 --> n6
    click n0 "../modules/Button.md"
    click n1 "../modules/QueryState.md"
    click n2 "../modules/PersonCapacity.test.md"
    click n3 "../modules/PersonCapacity.md"
    click n4 "../modules/TaskForm.md"
    click n5 "../modules/MyWorkPage.md"
    click n6 "../modules/api.md"
    click n7 "../modules/calendarService.md"
    click n8 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [PersonCapacity.test](../modules/PersonCapacity.test.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [MyWorkPage](../modules/MyWorkPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [calendarService](../modules/calendarService.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [Absence](../entities/Absence.md) | Class | 10 | — | — |
| [Availability](../entities/Availability.md) | Class | 11 | — | — |
| [Capacity](../entities/Capacity.md) | Class | 12 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `PersonCapacity` | `({ profileId, startDate, endDate, manage = false }: { profileId: number; startDate?: string; endDate?: string; manage?: boolean })` | — | — |