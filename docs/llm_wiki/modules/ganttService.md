# ganttService Module

**Path:** `frontend/src/services/ganttService.ts`

## Description

_Auto-generated from `frontend/src/services/ganttService.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../types/gantt` | `ExplainScheduleDetailLevel`, `ExplainScheduleRequest`, `ExplainScheduleResponse`, `GanttResponse`, `SchedulePreviewResponse`, `ScheduleResult` | Declaration | erased |
| `../types/task` | `TaskBatchUpdateItem` | Declaration | erased |
| `./api` | `api` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ganttService` |
| Constants | `ganttService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/planning/PlanScheduleSection.tsx"]
    n1["frontend/src/features/firstRun/sampleProject.ts"]
    n2["frontend/src/features/planningMasters/usePlanningReadiness.ts"]
    n3["frontend/src/pages/GanttPage.tsx"]
    n4["frontend/src/services/api.ts"]
    n5["frontend/src/services/ganttService.ts"]
    n6["frontend/src/types/gantt.ts"]
    n7["frontend/src/types/task.ts"]
    n0 --> n5
    n0 --> n6
    n0 --> n7
    n1 --> n5
    n2 --> n5
    n2 --> n6
    n2 --> n7
    n3 --> n5
    n3 --> n6
    n3 --> n7
    n5 --> n4
    n5 --> n6
    n5 --> n7
    n6 --> n7
    click n0 "../modules/PlanScheduleSection.md"
    click n1 "../modules/sampleProject.md"
    click n2 "../modules/usePlanningReadiness.md"
    click n3 "../modules/GanttPage.md"
    click n4 "../modules/api.md"
    click n5 "../modules/ganttService.md"
    click n6 "../modules/types_gantt.md"
    click n7 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [PlanScheduleSection](../modules/PlanScheduleSection.md) |
| Inbound | [sampleProject](../modules/sampleProject.md) |
| Inbound | [usePlanningReadiness](../modules/usePlanningReadiness.md) |
| Inbound | [GanttPage](../modules/GanttPage.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [types_gantt](../modules/types_gantt.md) |
| Outbound | [types_task](../modules/types_task.md) |
