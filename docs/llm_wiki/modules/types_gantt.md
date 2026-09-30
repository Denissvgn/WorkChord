# gantt Module

**Path:** `frontend/src/types/gantt.ts`

## Description

_Auto-generated from `frontend/src/types/gantt.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `./iteration` | `Iteration` |
| `./task` | `TaskUpdate` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ExplainScheduleDetailLevel`, `ExplainScheduleRequest`, `ExplainScheduleResponse`, `GanttResponse`, `GanttTask`, `ScheduleDecisionExplanation`, `SchedulePreviewResponse`, `ScheduleResult`, `SchedulingDecision`, `WorkloadAnalysis`, `WorkloadIssue` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/gantt/GanttChart.test.tsx"]
    n1["frontend/src/components/gantt/GanttChart.tsx"]
    n2["frontend/src/components/gantt/ScheduleExplanationDetails.tsx"]
    n3["frontend/src/components/gantt/TaskEditModal.tsx"]
    n4["frontend/src/features/planningMasters/usePlanningReadiness.test.tsx"]
    n5["frontend/src/features/planningMasters/usePlanningReadiness.ts"]
    n6["frontend/src/pages/GanttPage.test.tsx"]
    n7["frontend/src/pages/GanttPage.tsx"]
    n8["frontend/src/services/ganttService.ts"]
    n9["frontend/src/types/gantt.ts"]
    n10["frontend/src/types/iteration.ts"]
    n11["frontend/src/types/task.ts"]
    n0 --> n1
    n0 --> n9
    n1 --> n3
    n1 --> n8
    n1 --> n9
    n2 --> n9
    n3 --> n9
    n3 --> n11
    n4 --> n5
    n4 --> n9
    n4 --> n10
    n4 --> n11
    n5 --> n8
    n5 --> n9
    n5 --> n10
    n5 --> n11
    n6 --> n7
    n6 --> n9
    n6 --> n10
    n7 --> n1
    n7 --> n2
    n7 --> n3
    n7 --> n8
    n7 --> n9
    n7 --> n11
    n8 --> n9
    n8 --> n11
    n9 --> n10
    n9 --> n11
    click n0 "../modules/GanttChart.test.md"
    click n1 "../modules/GanttChart.md"
    click n2 "../modules/ScheduleExplanationDetails.md"
    click n3 "../modules/TaskEditModal.md"
    click n4 "../modules/usePlanningReadiness.test.md"
    click n5 "../modules/usePlanningReadiness.md"
    click n6 "../modules/GanttPage.test.md"
    click n7 "../modules/GanttPage.md"
    click n8 "../modules/ganttService.md"
    click n9 "../modules/types_gantt.md"
    click n10 "../modules/types_iteration.md"
    click n11 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [GanttChart.test](../modules/GanttChart.test.md) |
| Inbound | [GanttChart](../modules/GanttChart.md) |
| Inbound | [ScheduleExplanationDetails](../modules/ScheduleExplanationDetails.md) |
| Inbound | [TaskEditModal](../modules/TaskEditModal.md) |
| Inbound | [usePlanningReadiness.test](../modules/usePlanningReadiness.test.md) |
| Inbound | [usePlanningReadiness](../modules/usePlanningReadiness.md) |
| Inbound | [GanttPage.test](../modules/GanttPage.test.md) |
| Inbound | [GanttPage](../modules/GanttPage.md) |
| Inbound | [ganttService](../modules/ganttService.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |
| Outbound | [types_task](../modules/types_task.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [GanttTask](../entities/types_gantt_GanttTask.md) | Class | 6 | — | — |
| [GanttResponse](../entities/types_gantt_GanttResponse.md) | Class | 56 | — | — |
| [ScheduleResult](../entities/types_gantt_ScheduleResult.md) | Class | 66 | — | — |
| [SchedulePreviewResponse](../entities/types_gantt_SchedulePreviewResponse.md) | Class | 76 | — | Server dry-run of sandbox edits through the real scheduler (nothing persisted). |
| [SchedulingDecision](../entities/types_gantt_SchedulingDecision.md) | Class | 84 | — | — |
| [WorkloadIssue](../entities/types_gantt_WorkloadIssue.md) | Class | 92 | — | — |
| [ExplainScheduleRequest](../entities/types_gantt_ExplainScheduleRequest.md) | Class | 100 | — | — |
| [ScheduleDecisionExplanation](../entities/types_gantt_ScheduleDecisionExplanation.md) | Class | 104 | — | — |
| [WorkloadAnalysis](../entities/types_gantt_WorkloadAnalysis.md) | Class | 111 | — | — |
| [ExplainScheduleResponse](../entities/types_gantt_ExplainScheduleResponse.md) | Class | 116 | — | — |
| [ExplainScheduleDetailLevel](../entities/ExplainScheduleDetailLevel.md) | Type alias | 98 | — | — |
