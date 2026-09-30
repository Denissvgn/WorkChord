# PersonCapacity Module

**Path:** `frontend/src/components/tasks/PersonCapacity.tsx`

## Description

Displays server-derived daily availability, allocated and productive hours, saved commitments and uncertainty. Person owners can select a calendar and versioned absences. The interface preserves the established design and shows private work only through aggregate capacity.

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
    n2["frontend/src/components/tasks/PersonCapacity.tsx"]
    n3["frontend/src/components/tasks/TaskForm.tsx"]
    n4["frontend/src/pages/MyWorkPage.tsx"]
    n5["frontend/src/services/api.ts"]
    n6["frontend/src/services/calendarService.ts"]
    n7["frontend/src/utils/apiError.ts"]
    n1 --> n0
    n1 --> n7
    n2 --> n0
    n2 --> n1
    n2 --> n5
    n2 --> n6
    n2 --> n7
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n7
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n5
    n4 --> n7
    n6 --> n5
    click n0 "../modules/Button.md"
    click n1 "../modules/QueryState.md"
    click n2 "../modules/PersonCapacity.md"
    click n3 "../modules/TaskForm.md"
    click n4 "../modules/MyWorkPage.md"
    click n5 "../modules/api.md"
    click n6 "../modules/calendarService.md"
    click n7 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
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
