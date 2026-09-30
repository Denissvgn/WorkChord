# ScheduleResult

**Location:** `frontend/src/types/gantt.ts:66`
**Kind:** Class
**Bases:** —
**Module:** [types_gantt](../modules/types_gantt.md)

## Description

_Auto-generated from `ScheduleResult` in `frontend/src/types/gantt.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `planning_revision` | `number` | No | — | — |
| `capacity_issues` | `{ profile_id: number \| null; code: string; message: string; dates?: string[] }[]` | No | — | — |
| `success` | `boolean` | Yes | — | — |
| `decisions` | `SchedulingDecision[]` | Yes | — | — |
| `workload_balanced` | `boolean` | Yes | — | — |
| `workload_issues` | `WorkloadIssue[]` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ScheduleResult (frontend/src/types/gantt.ts)"]
    n1["frontend/src/components/gantt/GanttChart.test.tsx"]
    n2["frontend/src/services/ganttService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_gantt.md"
    click n1 "../modules/GanttChart.test.md"
    click n2 "../modules/ganttService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_gantt](../modules/types_gantt.md) | 0 | `capacity_issues`, `decisions`, `planning_revision`, `success`, `workload_balanced`, `workload_issues` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `GanttChart.test` | import | [GanttChart.test](../modules/GanttChart.test.md) | — |
| `ganttService` | import | [ganttService](../modules/ganttService.md) | — |
