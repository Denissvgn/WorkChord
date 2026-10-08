# planningNavigationInvalidation Module

**Path:** `frontend/src/features/planningMasters/planningNavigationInvalidation.ts`

## Description

_Auto-generated from `frontend/src/features/planningMasters/planningNavigationInvalidation.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `./usePlanningNavigationSummary` | `planningNavigationSummaryKey` |
| `@tanstack/react-query` | `QueryClient`, `QueryCacheNotifyEvent` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `installPlanningNavigationInvalidation` |
| Constants | `READINESS_INPUT_QUERY_ROOTS` |
| Module calls | `READINESS_INPUT_QUERY_ROOTS = Set` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/features/planningMasters/planningNavigationInvalidation.test.ts"]
    n1["frontend/src/features/planningMasters/planningNavigationInvalidation.ts"]
    n2["frontend/src/features/planningMasters/usePlanningNavigationSummary.ts"]
    n3["frontend/src/features/workspaceQueryPolicy.ts"]
    n0 --> n1
    n0 --> n2
    n1 --> n2
    n3 --> n1
    click n0 "../modules/planningNavigationInvalidation.test.md"
    click n1 "../modules/planningNavigationInvalidation.md"
    click n2 "../modules/usePlanningNavigationSummary.md"
    click n3 "../modules/workspaceQueryPolicy.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [planningNavigationInvalidation.test](../modules/planningNavigationInvalidation.test.md) |
| Inbound | [workspaceQueryPolicy](../modules/workspaceQueryPolicy.md) |
| Outbound | [usePlanningNavigationSummary](../modules/usePlanningNavigationSummary.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `installPlanningNavigationInvalidation` | `(queryClient: QueryClient)` | — | — |
