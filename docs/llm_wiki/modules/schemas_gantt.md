# gantt Module

**Path:** `backend/app/schemas/gantt.py`

## Description

Gantt chart schemas.

## Imports

| Source | Symbols |
|--------|---------|
| `app.schemas.iteration` | `IterationResponse` |
| `app.schemas.task` | `TaskBatchUpdateItem` |
| `app.schemas.work_metrics` | `TaskMetricSignals` |
| `datetime` | `date` |
| `pydantic` | `BaseModel` |
| `typing` | `Literal`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/routers/gantt.py"]
    n1["backend/app/schemas/__init__.py"]
    n2["backend/app/schemas/gantt.py"]
    n3["backend/app/schemas/iteration.py"]
    n4["backend/app/schemas/task.py"]
    n5["backend/app/schemas/work_metrics.py"]
    n6["backend/app/services/llm_service.py"]
    n7["backend/app/services/scheduler_service.py"]
    n0 --> n2
    n0 --> n3
    n0 --> n7
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n3 --> n5
    n4 --> n5
    n6 --> n2
    n7 --> n2
    click n0 "../modules/routers_gantt.md"
    click n1 "../modules/schemas___init__.md"
    click n2 "../modules/schemas_gantt.md"
    click n3 "../modules/schemas_iteration.md"
    click n4 "../modules/schemas_task.md"
    click n5 "../modules/schemas_work_metrics.md"
    click n6 "../modules/llm_service.md"
    click n7 "../modules/scheduler_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [routers_gantt](../modules/routers_gantt.md) |
| Inbound | [schemas___init__](../modules/schemas___init__.md) |
| Inbound | [llm_service](../modules/llm_service.md) |
| Inbound | [scheduler_service](../modules/scheduler_service.md) |
| Outbound | [schemas_iteration](../modules/schemas_iteration.md) |
| Outbound | [schemas_task](../modules/schemas_task.md) |
| Outbound | [schemas_work_metrics](../modules/schemas_work_metrics.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [GanttAssignee](../entities/GanttAssignee.md) | Pydantic model | 13 | `BaseModel` | Assignee info for Gantt task. |
| [GanttMilestone](../entities/GanttMilestone.md) | Pydantic model | 19 | `BaseModel` | Milestone info for Gantt task editing. |
| [GanttTask](../entities/schemas_gantt_GanttTask.md) | Class | 28 | `TaskMetricSignals` | Task representation for Gantt chart. |
| [SchedulingDecision](../entities/schemas_gantt_SchedulingDecision.md) | Pydantic model | 60 | `BaseModel` | Explanation for a scheduling decision. |
| [UnscheduledReason](../entities/schemas_gantt_UnscheduledReason.md) | Type alias | 69 | `Literal['no_assignee', 'assignee_not_in_iteration', 'no_estimate', 'no_capacity', 'prerequisites_pending', 'predecessor_unscheduled', 'deferred', 'blocked', 'not_placed']` | — |
| [UnscheduledTask](../entities/schemas_gantt_UnscheduledTask.md) | Pydantic model | 82 | `BaseModel` | A planned task the scheduler left without dates, and what would change that. |
| [WorkloadIssue](../entities/schemas_gantt_WorkloadIssue.md) | Pydantic model | 90 | `BaseModel` | Workload issue for a team member. |
| [ScheduleResult](../entities/schemas_gantt_ScheduleResult.md) | Pydantic model | 97 | `BaseModel` | Result of scheduling operation. |
| [GanttResponse](../entities/schemas_gantt_GanttResponse.md) | Pydantic model | 109 | `BaseModel` | Full Gantt chart response. |
| [ScheduleApplyRequest](../entities/ScheduleApplyRequest.md) | Pydantic model | 120 | `BaseModel` | — |
| [SchedulePreviewRequest](../entities/SchedulePreviewRequest.md) | Pydantic model | 126 | `BaseModel` | Sandbox edits to dry-run through the real scheduler. |
| [SchedulePreviewResponse](../entities/schemas_gantt_SchedulePreviewResponse.md) | Pydantic model | 137 | `BaseModel` | Projected Gantt state after applying changes and rescheduling. |
