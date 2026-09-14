# ganttService Module

**Path:** `frontend/src/services/ganttService.ts`

## Description

_Auto-generated from `frontend/src/services/ganttService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/gantt` | `ExplainScheduleDetailLevel`, `ExplainScheduleRequest`, `ExplainScheduleResponse`, `GanttResponse`, `SchedulePreviewResponse`, `ScheduleResult` |
| `../types/task` | `TaskBatchUpdateItem` |
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ganttService` |
| Constants | `ganttService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/gantt/GanttChart.tsx"]
    n1["frontend/src/features/planningMasters/usePlanningReadiness.ts"]
    n2["frontend/src/pages/GanttPage.tsx"]
    n3["frontend/src/services/api.ts"]
    n4["frontend/src/services/ganttService.ts"]
    n5["frontend/src/types/gantt.ts"]
    n6["frontend/src/types/task.ts"]
    n0 --> n4
    n0 --> n5
    n1 --> n4
    n1 --> n5
    n1 --> n6
    n2 --> n0
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n4 --> n3
    n4 --> n5
    n4 --> n6
    n5 --> n6
    click n0 "../modules/GanttChart.md"
    click n1 "../modules/usePlanningReadiness.md"
    click n2 "../modules/GanttPage.md"
    click n3 "../modules/api.md"
    click n4 "../modules/ganttService.md"
    click n5 "../modules/types_gantt.md"
    click n6 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [GanttChart](../modules/GanttChart.md) |
| Inbound | [usePlanningReadiness](../modules/usePlanningReadiness.md) |
| Inbound | [GanttPage](../modules/GanttPage.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [types_gantt](../modules/types_gantt.md) |
| Outbound | [types_task](../modules/types_task.md) |
