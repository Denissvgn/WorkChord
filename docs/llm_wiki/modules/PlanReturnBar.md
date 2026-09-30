# PlanReturnBar Module

**Path:** `frontend/src/components/planning/PlanReturnBar.tsx`

## Description

_Auto-generated from `frontend/src/components/planning/PlanReturnBar.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../features/planningMasters/planningReturn` | `isPlanningStepId`, `planMasterStepHref`, `PLANNING_RETURN_STEP_PARAM` |
| `lucide-react` | `ArrowLeft`, `Waypoints` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `Link`, `useSearchParams` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `PlanReturnBar` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/planning/PlanningWorkbenchFrame.tsx"]
    n1["frontend/src/components/planning/PlanReturnBar.test.tsx"]
    n2["frontend/src/components/planning/PlanReturnBar.tsx"]
    n3["frontend/src/features/planningMasters/planningReturn.ts"]
    n4["frontend/src/pages/IterationsPage.tsx"]
    n5["frontend/src/pages/TasksPage.tsx"]
    n6["frontend/src/pages/TeamPage.tsx"]
    n0 --> n2
    n1 --> n2
    n2 --> n3
    n4 --> n2
    n5 --> n2
    n6 --> n2
    click n0 "../modules/PlanningWorkbenchFrame.md"
    click n1 "../modules/PlanReturnBar.test.md"
    click n2 "../modules/PlanReturnBar.md"
    click n3 "../modules/planningReturn.md"
    click n4 "../modules/IterationsPage.md"
    click n5 "../modules/TasksPage.md"
    click n6 "../modules/TeamPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [PlanningWorkbenchFrame](../modules/PlanningWorkbenchFrame.md) |
| Inbound | [PlanReturnBar.test](../modules/PlanReturnBar.test.md) |
| Inbound | [IterationsPage](../modules/IterationsPage.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Inbound | [TeamPage](../modules/TeamPage.md) |
| Outbound | [planningReturn](../modules/planningReturn.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `PlanReturnBar` | `()` | — | — |
