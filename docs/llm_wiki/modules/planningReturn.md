# planningReturn Module

**Path:** `frontend/src/features/planningMasters/planningReturn.ts`

## Description

_Auto-generated from `frontend/src/features/planningMasters/planningReturn.ts`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `PLANNING_RETURN_STEP_PARAM`, `PLANNING_STEP_IDS`, `PLAN_RETURNED_PARAM`, `PlanningStepId`, `isPlanningStepId`, `planMasterStepHref`, `withPlanMasterReturn` |
| Constants | `PLANNING_RETURN_STEP_PARAM`, `PLANNING_STEP_IDS`, `PLAN_RETURNED_PARAM` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/analytics/OnTrackSummary.tsx"]
    n1["frontend/src/components/planning/PlanReturnBar.tsx"]
    n2["frontend/src/features/planningMasters/masters.ts"]
    n3["frontend/src/features/planningMasters/planningReturn.ts"]
    n4["frontend/src/features/planningMasters/planningTaskIssues.ts"]
    n5["frontend/src/pages/PlanMasterPage.tsx"]
    n0 --> n3
    n1 --> n3
    n2 --> n3
    n2 --> n4
    n4 --> n3
    n5 --> n2
    n5 --> n3
    n5 --> n4
    click n0 "../modules/OnTrackSummary.md"
    click n1 "../modules/PlanReturnBar.md"
    click n2 "../modules/planningMasters_masters.md"
    click n3 "../modules/planningReturn.md"
    click n4 "../modules/planningTaskIssues.md"
    click n5 "../modules/PlanMasterPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [OnTrackSummary](../modules/OnTrackSummary.md) |
| Inbound | [PlanReturnBar](../modules/PlanReturnBar.md) |
| Inbound | [planningMasters_masters](../modules/planningMasters_masters.md) |
| Inbound | [planningTaskIssues](../modules/planningTaskIssues.md) |
| Inbound | [PlanMasterPage](../modules/PlanMasterPage.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [PlanningStepId](../entities/PlanningStepId.md) | Type alias | 12 | `typeof PLANNING_STEP_IDS[number]` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `isPlanningStepId` | `(value: string \| null) -> value is PlanningStepId` | — | — |
| `planMasterStepHref` | `(stepId: PlanningStepId, { returned = false }: { returned?: boolean } = {})` | — | Link back to a plan step; `returned` makes the step re-check and advance when done. |
| `withPlanMasterReturn` | `(route: string, returnStepId: PlanningStepId, options: Record<string, string> = {})` | — | — |
