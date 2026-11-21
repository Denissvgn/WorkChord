# PlanReturnBar Module

**Path:** `frontend/src/components/planning/PlanReturnBar.tsx`

## Description

_Auto-generated from `frontend/src/components/planning/PlanReturnBar.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/planningMasters/planningReturn` | `isPlanningStepId`, `planStepHref`, `PLANNING_RETURN_STEP_PARAM` | — | compiler-dependent |
| `../../features/scope/useScopeLink` | `useScopeLink` | — | compiler-dependent |
| `../common/ButtonLink` | `ButtonLink` | — | compiler-dependent |
| `lucide-react` | `ArrowLeft`, `Waypoints` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `useSearchParams` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `PlanReturnBar` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/ButtonLink.tsx"]
    n1["frontend/src/components/planning/PlanningWorkbenchFrame.tsx"]
    n2["frontend/src/components/planning/PlanReturnBar.test.tsx"]
    n3["frontend/src/components/planning/PlanReturnBar.tsx"]
    n4["frontend/src/features/firstRun/GetStartedFlow.test.tsx"]
    n5["frontend/src/features/planningMasters/planningReturn.ts"]
    n6["frontend/src/features/scope/planningLinks.test.tsx"]
    n7["frontend/src/features/scope/useScopeLink.ts"]
    n8["frontend/src/pages/TasksPage.tsx"]
    n9["frontend/src/pages/TeamPage.tsx"]
    n1 --> n3
    n2 --> n3
    n3 --> n0
    n3 --> n5
    n3 --> n7
    n4 --> n3
    n4 --> n8
    n6 --> n3
    n8 --> n0
    n8 --> n3
    n8 --> n5
    n8 --> n7
    n9 --> n3
    click n0 "../modules/ButtonLink.md"
    click n1 "../modules/PlanningWorkbenchFrame.md"
    click n2 "../modules/PlanReturnBar.test.md"
    click n3 "../modules/PlanReturnBar.md"
    click n4 "../modules/GetStartedFlow.test.md"
    click n5 "../modules/planningReturn.md"
    click n6 "../modules/planningLinks.test.md"
    click n7 "../modules/useScopeLink.md"
    click n8 "../modules/TasksPage.md"
    click n9 "../modules/TeamPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [PlanningWorkbenchFrame](../modules/PlanningWorkbenchFrame.md) |
| Inbound | [PlanReturnBar.test](../modules/PlanReturnBar.test.md) |
| Inbound | [GetStartedFlow.test](../modules/GetStartedFlow.test.md) |
| Inbound | [planningLinks.test](../modules/planningLinks.test.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Inbound | [TeamPage](../modules/TeamPage.md) |
| Outbound | [ButtonLink](../modules/ButtonLink.md) |
| Outbound | [planningReturn](../modules/planningReturn.md) |
| Outbound | [useScopeLink](../modules/useScopeLink.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `PlanReturnBar` | `()` | — | — |
