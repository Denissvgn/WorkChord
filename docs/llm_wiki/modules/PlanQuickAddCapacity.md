# PlanQuickAddCapacity Module

**Path:** `frontend/src/components/capacity/PlanQuickAddCapacity.tsx`

## Description

The capacity picker loads profiles when it opens and excludes profiles already assigned to the selected iteration. A planner can select several people or agents before confirming. It refreshes the relevant iteration and planning data after the membership update.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/teamService` | `teamService` | — | compiler-dependent |
| `../../types/iteration` | `Iteration` | Declaration | erased |
| `../../types/team` | `TeamMember` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/Modal` | `Modal` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `./capacityMutations` | `addCapacityRows`, `refreshCapacity` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `lucide-react` | `Bot`, `User` | — | compiler-dependent |
| `react` | `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `PlanQuickAddCapacity` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/capacity/capacityMutations.ts"]
    n1["frontend/src/components/capacity/CapacitySection.tsx"]
    n2["frontend/src/components/capacity/PlanQuickAddCapacity.test.tsx"]
    n3["frontend/src/components/capacity/PlanQuickAddCapacity.tsx"]
    n4["frontend/src/components/common/Button.tsx"]
    n5["frontend/src/components/common/Modal.tsx"]
    n6["frontend/src/components/feedback/QueryState.tsx"]
    n7["frontend/src/services/teamService.ts"]
    n8["frontend/src/types/iteration.ts"]
    n9["frontend/src/types/team.ts"]
    n10["frontend/src/utils/apiError.ts"]
    n0 --> n7
    n0 --> n9
    n1 --> n0
    n1 --> n3
    n1 --> n4
    n1 --> n7
    n1 --> n8
    n1 --> n9
    n1 --> n10
    n2 --> n3
    n2 --> n8
    n2 --> n9
    n3 --> n0
    n3 --> n4
    n3 --> n5
    n3 --> n6
    n3 --> n7
    n3 --> n8
    n3 --> n9
    n3 --> n10
    n6 --> n4
    n6 --> n10
    n7 --> n9
    click n0 "../modules/capacityMutations.md"
    click n1 "../modules/CapacitySection.md"
    click n2 "../modules/PlanQuickAddCapacity.test.md"
    click n3 "../modules/PlanQuickAddCapacity.md"
    click n4 "../modules/Button.md"
    click n5 "../modules/Modal.md"
    click n6 "../modules/QueryState.md"
    click n7 "../modules/teamService.md"
    click n8 "../modules/types_iteration.md"
    click n9 "../modules/types_team.md"
    click n10 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [CapacitySection](../modules/CapacitySection.md) |
| Inbound | [PlanQuickAddCapacity.test](../modules/PlanQuickAddCapacity.test.md) |
| Outbound | [capacityMutations](../modules/capacityMutations.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Modal](../modules/Modal.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [teamService](../modules/teamService.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |
| Outbound | [types_team](../modules/types_team.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `PlanQuickAddCapacity` | `({ iteration, members, primary = true }: { iteration: Iteration; members: TeamMember[]; primary?: boolean })` | — | Adds one capacity row from an existing profile without leaving the plan (the default case). |
