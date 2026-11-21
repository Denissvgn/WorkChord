# PersonCapacity Module

**Path:** `frontend/src/components/tasks/PersonCapacity.tsx`

## Description

Displays server-derived daily availability, allocated and productive hours, saved commitments and uncertainty. Person owners can select a calendar and versioned absences. The interface preserves the established design and shows private work only through aggregate capacity.

Person calendar changes retain the opening availability revision across live refreshes. Changed server state requires an explicit current comparison before reapplication; pending absence and calendar writes retain input intent.

The personal availability editor retains an explicit annual calendar selection and its observed profile revision through a failed save. The owner can retry that draft or compare it with a newer saved policy. A successful save refreshes the person's capacity projection.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Select` | `Select` | — | compiler-dependent |
| `../../services/api` | `api` | — | compiler-dependent |
| `../../services/calendarService` | `calendarService` | — | compiler-dependent |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `../iteration/AnnualCalendarFields` | `AnnualCalendarFields` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `react` | `useId`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `PersonCapacity` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/Select.tsx"]
    n2["frontend/src/components/feedback/QueryState.tsx"]
    n3["frontend/src/components/iteration/AnnualCalendarFields.tsx"]
    n4["frontend/src/components/tasks/PersonCapacity.test.tsx"]
    n5["frontend/src/components/tasks/PersonCapacity.tsx"]
    n6["frontend/src/components/tasks/TaskForm.tsx"]
    n7["frontend/src/components/team/TeamProfileManager.tsx"]
    n8["frontend/src/pages/MyWorkPage.tsx"]
    n9["frontend/src/services/api.ts"]
    n10["frontend/src/services/calendarService.ts"]
    n11["frontend/src/utils/apiError.ts"]
    n2 --> n0
    n2 --> n11
    n3 --> n1
    n4 --> n5
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n9
    n5 --> n10
    n5 --> n11
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n5
    n6 --> n11
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n5
    n7 --> n11
    n8 --> n0
    n8 --> n2
    n8 --> n5
    n8 --> n9
    n8 --> n11
    n10 --> n9
    click n0 "../modules/Button.md"
    click n1 "../modules/Select.md"
    click n2 "../modules/QueryState.md"
    click n3 "../modules/AnnualCalendarFields.md"
    click n4 "../modules/PersonCapacity.test.md"
    click n5 "../modules/PersonCapacity.md"
    click n6 "../modules/TaskForm.md"
    click n7 "../modules/TeamProfileManager.md"
    click n8 "../modules/MyWorkPage.md"
    click n9 "../modules/api.md"
    click n10 "../modules/calendarService.md"
    click n11 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [PersonCapacity.test](../modules/PersonCapacity.test.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [TeamProfileManager](../modules/TeamProfileManager.md) |
| Inbound | [MyWorkPage](../modules/MyWorkPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Select](../modules/Select.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [AnnualCalendarFields](../modules/AnnualCalendarFields.md) |
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
| [Absence](../entities/Absence.md) | Interface | 12 | — | — |
| [Availability](../entities/Availability.md) | Interface | 13 | — | — |
| [Capacity](../entities/Capacity.md) | Interface | 14 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `PersonCapacity` | `({ profileId, startDate, endDate, manage = false, label }: { profileId: number; startDate?: string; endDate?: string; manage?: boolean; label?: string })` | — | — |
