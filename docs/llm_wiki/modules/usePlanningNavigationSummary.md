# usePlanningNavigationSummary Module

**Path:** `frontend/src/features/planningMasters/usePlanningNavigationSummary.ts`

## Description

_Auto-generated from `frontend/src/features/planningMasters/usePlanningNavigationSummary.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/iterationService` | `iterationService` |
| `../../store/iterationStore` | `useIterationStore` |
| `../../types/iteration` | `Iteration` |
| `./masters` | `deriveStatus`, `readiness`, `PlanReadiness` |
| `@tanstack/react-query` | `useQuery` |
| `react` | `useMemo` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `planningNavigationSummaryKey`, `usePlanningNavigationSummary` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/layout/AppTopNav.tsx"]
    n1["frontend/src/components/layout/SidebarIterationCard.tsx"]
    n2["frontend/src/features/identity/IdentityProvider.test.tsx"]
    n3["frontend/src/features/planningMasters/masters.ts"]
    n4["frontend/src/features/planningMasters/planningNavigationInvalidation.test.ts"]
    n5["frontend/src/features/planningMasters/planningNavigationInvalidation.ts"]
    n6["frontend/src/features/planningMasters/usePlanningNavigationSummary.ts"]
    n7["frontend/src/services/iterationService.ts"]
    n8["frontend/src/store/iterationStore.ts"]
    n9["frontend/src/types/iteration.ts"]
    n0 --> n6
    n1 --> n6
    n2 --> n6
    n4 --> n5
    n4 --> n6
    n5 --> n6
    n6 --> n3
    n6 --> n7
    n6 --> n8
    n6 --> n9
    n7 --> n9
    click n0 "../modules/AppTopNav.md"
    click n1 "../modules/SidebarIterationCard.md"
    click n2 "../modules/IdentityProvider.test.md"
    click n3 "../modules/planningMasters_masters.md"
    click n4 "../modules/planningNavigationInvalidation.test.md"
    click n5 "../modules/planningNavigationInvalidation.md"
    click n6 "../modules/usePlanningNavigationSummary.md"
    click n7 "../modules/iterationService.md"
    click n8 "../modules/iterationStore.md"
    click n9 "../modules/types_iteration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AppTopNav](../modules/AppTopNav.md) |
| Inbound | [SidebarIterationCard](../modules/SidebarIterationCard.md) |
| Inbound | [IdentityProvider.test](../modules/IdentityProvider.test.md) |
| Inbound | [planningNavigationInvalidation.test](../modules/planningNavigationInvalidation.test.md) |
| Inbound | [planningNavigationInvalidation](../modules/planningNavigationInvalidation.md) |
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
| `planningNavigationSummaryKey` | `(iterationId: number)` | — | — |
| `usePlanningNavigationSummary` | `()` | — | — |
