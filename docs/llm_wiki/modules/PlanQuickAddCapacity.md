# PlanQuickAddCapacity Module

**Path:** `frontend/src/components/planning/PlanQuickAddCapacity.tsx`

## Description

_Auto-generated from `frontend/src/components/planning/PlanQuickAddCapacity.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/planningInputService` | `planningInputService` | — | compiler-dependent |
| `../../services/teamService` | `teamService` | — | compiler-dependent |
| `../../types/iteration` | `Iteration` | Declaration | erased |
| `../../types/team` | `TeamMember`, `TeamMemberProfile` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
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
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/feedback/QueryState.tsx"]
    n2["frontend/src/components/planning/PlanQuickAddCapacity.test.tsx"]
    n3["frontend/src/components/planning/PlanQuickAddCapacity.tsx"]
    n4["frontend/src/pages/PlanMasterPage.tsx"]
    n5["frontend/src/services/planningInputService.ts"]
    n6["frontend/src/services/teamService.ts"]
    n7["frontend/src/types/iteration.ts"]
    n8["frontend/src/types/team.ts"]
    n9["frontend/src/utils/apiError.ts"]
    n1 --> n0
    n1 --> n9
    n2 --> n3
    n2 --> n7
    n2 --> n8
    n3 --> n0
    n3 --> n1
    n3 --> n5
    n3 --> n6
    n3 --> n7
    n3 --> n8
    n3 --> n9
    n4 --> n1
    n4 --> n3
    n6 --> n5
    n6 --> n8
    click n0 "../modules/Button.md"
    click n1 "../modules/QueryState.md"
    click n2 "../modules/PlanQuickAddCapacity.test.md"
    click n3 "../modules/PlanQuickAddCapacity.md"
    click n4 "../modules/PlanMasterPage.md"
    click n5 "../modules/planningInputService.md"
    click n6 "../modules/teamService.md"
    click n7 "../modules/types_iteration.md"
    click n8 "../modules/types_team.md"
    click n9 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [PlanQuickAddCapacity.test](../modules/PlanQuickAddCapacity.test.md) |
| Inbound | [PlanMasterPage](../modules/PlanMasterPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [planningInputService](../modules/planningInputService.md) |
| Outbound | [teamService](../modules/teamService.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |
| Outbound | [types_team](../modules/types_team.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `PlanQuickAddCapacity` | `({ iteration, members }: { iteration: Iteration; members: TeamMember[] })` | — | Adds one capacity row from an existing profile without leaving the plan (the default case). |
