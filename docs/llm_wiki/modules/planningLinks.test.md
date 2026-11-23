# planningLinks.test Module

**Path:** `frontend/src/features/scope/planningLinks.test.tsx`

## Description

_Auto-generated from `frontend/src/features/scope/planningLinks.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/analytics/OnTrackSummary` | `OnTrackSummary` | — | compiler-dependent |
| `../../components/planning/PlanReturnBar` | `PlanReturnBar` | — | compiler-dependent |
| `../../components/planning/PlanningWorkflowHelpContent` | `PlanningWorkflowHelpContent` | — | compiler-dependent |
| `../../components/tasks/TaskWorkflowHelpContent` | `TaskWorkflowHelpContent` | — | compiler-dependent |
| `../../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../../pages/PlanSharePage` | `PlanSharePage` | — | compiler-dependent |
| `../../test/renderWithProviders` | `createTestQueryClient`, `renderWithProviders` | — | compiler-dependent |
| `../../types/iteration` | `IterationSummary` | Declaration | erased |
| `./scopeStore` | `useScopeStore` | — | compiler-dependent |
| `./useWorkScope` | `useWorkScope` | — | compiler-dependent |
| `@tanstack/react-query` | `QueryClientProvider` | — | compiler-dependent |
| `@testing-library/react` | `act`, `render`, `screen`, `waitFor` | — | compiler-dependent |
| `react-router-dom` | `createMemoryRouter`, `Outlet`, `Route`, `RouterProvider`, `Routes`, `useLocation` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `iterationServiceMock`, `planShareServiceMock`, `ITERATIONS` |
| Module calls | `iterationServiceMock = hoisted`, `planShareServiceMock = hoisted`, `mock`, `mock`, `mock`, `beforeEach`, `afterEach`, `describe`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/analytics/OnTrackSummary.tsx"]
    n1["frontend/src/components/planning/PlanningWorkflowHelpContent.tsx"]
    n2["frontend/src/components/planning/PlanReturnBar.tsx"]
    n3["frontend/src/components/tasks/TaskWorkflowHelpContent.tsx"]
    n4["frontend/src/features/scope/planningLinks.test.tsx"]
    n5["frontend/src/features/scope/scopeStore.ts"]
    n6["frontend/src/features/scope/useWorkScope.ts"]
    n7["frontend/src/i18n/i18n.ts"]
    n8["frontend/src/pages/PlanSharePage.tsx"]
    n9["frontend/src/test/renderWithProviders.tsx"]
    n10["frontend/src/types/iteration.ts"]
    n0 --> n10
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n4 --> n8
    n4 --> n9
    n4 --> n10
    n6 --> n5
    n9 --> n7
    click n0 "../modules/OnTrackSummary.md"
    click n1 "../modules/PlanningWorkflowHelpContent.md"
    click n2 "../modules/PlanReturnBar.md"
    click n3 "../modules/TaskWorkflowHelpContent.md"
    click n4 "../modules/planningLinks.test.md"
    click n5 "../modules/scopeStore.md"
    click n6 "../modules/useWorkScope.md"
    click n7 "../modules/i18n.md"
    click n8 "../modules/PlanSharePage.md"
    click n9 "../modules/renderWithProviders.md"
    click n10 "../modules/types_iteration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [OnTrackSummary](../modules/OnTrackSummary.md) |
| Outbound | [PlanningWorkflowHelpContent](../modules/PlanningWorkflowHelpContent.md) |
| Outbound | [PlanReturnBar](../modules/PlanReturnBar.md) |
| Outbound | [TaskWorkflowHelpContent](../modules/TaskWorkflowHelpContent.md) |
| Outbound | [scopeStore](../modules/scopeStore.md) |
| Outbound | [useWorkScope](../modules/useWorkScope.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [PlanSharePage](../modules/PlanSharePage.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |
