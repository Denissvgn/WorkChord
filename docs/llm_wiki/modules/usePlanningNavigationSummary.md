# usePlanningNavigationSummary Module

**Path:** `frontend/src/features/planningMasters/usePlanningNavigationSummary.ts`

## Description

_Auto-generated from `frontend/src/features/planningMasters/usePlanningNavigationSummary.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../../store/iterationStore` | `useIterationStore` | — | compiler-dependent |
| `../../types/iteration` | `Iteration` | Declaration | erased |
| `./masters` | `PlanReadiness` | Declaration | erased |
| `./masters` | `deriveStatus`, `readiness` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `react` | `useMemo` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `planningNavigationSummaryKey`, `usePlanningNavigationSummary` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/iteration/IterationCapacityLine.tsx"]
    n1["frontend/src/components/layout/AppTopNav.tsx"]
    n2["frontend/src/components/layout/SidebarIterationCard.tsx"]
    n3["frontend/src/features/identity/IdentityProvider.test.tsx"]
    n4["frontend/src/features/planningMasters/masters.ts"]
    n5["frontend/src/features/planningMasters/planningNavigationInvalidation.test.ts"]
    n6["frontend/src/features/planningMasters/planningNavigationInvalidation.ts"]
    n7["frontend/src/features/planningMasters/usePlanningNavigationSummary.ts"]
    n8["frontend/src/features/planningMasters/usePlanningReadiness.ts"]
    n9["frontend/src/services/iterationService.ts"]
    n10["frontend/src/store/iterationStore.ts"]
    n11["frontend/src/types/iteration.ts"]
    n0 --> n7
    n0 --> n9
    n1 --> n7
    n2 --> n7
    n3 --> n7
    n5 --> n6
    n5 --> n7
    n6 --> n7
    n7 --> n4
    n7 --> n9
    n7 --> n10
    n7 --> n11
    n8 --> n4
    n8 --> n7
    n8 --> n9
    n8 --> n10
    n8 --> n11
    n9 --> n11
    click n0 "../modules/IterationCapacityLine.md"
    click n1 "../modules/AppTopNav.md"
    click n2 "../modules/SidebarIterationCard.md"
    click n3 "../modules/IdentityProvider.test.md"
    click n4 "../modules/planningMasters_masters.md"
    click n5 "../modules/planningNavigationInvalidation.test.md"
    click n6 "../modules/planningNavigationInvalidation.md"
    click n7 "../modules/usePlanningNavigationSummary.md"
    click n8 "../modules/usePlanningReadiness.md"
    click n9 "../modules/iterationService.md"
    click n10 "../modules/iterationStore.md"
    click n11 "../modules/types_iteration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [IterationCapacityLine](../modules/IterationCapacityLine.md) |
| Inbound | [AppTopNav](../modules/AppTopNav.md) |
| Inbound | [SidebarIterationCard](../modules/SidebarIterationCard.md) |
| Inbound | [IdentityProvider.test](../modules/IdentityProvider.test.md) |
| Inbound | [planningNavigationInvalidation.test](../modules/planningNavigationInvalidation.test.md) |
| Inbound | [planningNavigationInvalidation](../modules/planningNavigationInvalidation.md) |
| Inbound | [usePlanningReadiness](../modules/usePlanningReadiness.md) |
| Outbound | [planningMasters_masters](../modules/planningMasters_masters.md) |
| Outbound | [iterationService](../modules/iterationService.md) |
| Outbound | [iterationStore](../modules/iterationStore.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `planningNavigationSummaryKey` | `(iterationId?: number)` | — | — |
| `usePlanningNavigationSummary` | `()` | — | — |
