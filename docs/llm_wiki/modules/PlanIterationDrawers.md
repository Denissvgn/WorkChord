# PlanIterationDrawers Module

**Path:** `frontend/src/components/planning/PlanIterationDrawers.tsx`

## Description

_Auto-generated from `frontend/src/components/planning/PlanIterationDrawers.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/planningMasters/useIterationPanels` | `useIterationPanels` | — | compiler-dependent |
| `../../features/scope/useScopeLink` | `useScopeLink`, `useLinkScope` | — | compiler-dependent |
| `../../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../../types/iteration` | `Iteration` | Declaration | erased |
| `../iteration/AllIterationsDrawer` | `AllIterationsDrawer` | — | compiler-dependent |
| `../iteration/IterationEditorDrawer` | `IterationEditorDrawer` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `react` | `useCallback`, `useEffect`, `useRef`, `useState` | — | compiler-dependent |
| `react-router-dom` | `useLocation`, `useNavigate` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `PlanIterationDrawers` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/iteration/AllIterationsDrawer.tsx"]
    n1["frontend/src/components/iteration/IterationEditorDrawer.tsx"]
    n2["frontend/src/components/planning/PlanIterationDrawers.tsx"]
    n3["frontend/src/features/planningMasters/useIterationPanels.ts"]
    n4["frontend/src/features/scope/useScopeLink.ts"]
    n5["frontend/src/pages/PlanPage.tsx"]
    n6["frontend/src/services/iterationService.ts"]
    n7["frontend/src/types/iteration.ts"]
    n0 --> n7
    n1 --> n7
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n2 --> n6
    n2 --> n7
    n5 --> n2
    n5 --> n4
    n5 --> n7
    n6 --> n7
    click n0 "../modules/AllIterationsDrawer.md"
    click n1 "../modules/IterationEditorDrawer.md"
    click n2 "../modules/PlanIterationDrawers.md"
    click n3 "../modules/useIterationPanels.md"
    click n4 "../modules/useScopeLink.md"
    click n5 "../modules/PlanPage.md"
    click n6 "../modules/iterationService.md"
    click n7 "../modules/types_iteration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [PlanPage](../modules/PlanPage.md) |
| Outbound | [AllIterationsDrawer](../modules/AllIterationsDrawer.md) |
| Outbound | [IterationEditorDrawer](../modules/IterationEditorDrawer.md) |
| Outbound | [useIterationPanels](../modules/useIterationPanels.md) |
| Outbound | [useScopeLink](../modules/useScopeLink.md) |
| Outbound | [iterationService](../modules/iterationService.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `PlanIterationDrawers` | `()` | — | The drawers that manage iterations from Plan: every iteration of the scope's project, and the |
