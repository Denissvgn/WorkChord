# planningTaskIssues Module

**Path:** `frontend/src/features/planningMasters/planningTaskIssues.ts`

## Description

_Auto-generated from `frontend/src/features/planningMasters/planningTaskIssues.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/task` | `Task` | Declaration | erased |
| `./planningReturn` | `PlanningStepId` | Declaration | erased |
| `./planningReturn` | `withPlanMasterReturn` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `PLANNING_ITERATION_PARAM`, `PLANNING_TASK_ISSUES`, `PLANNING_TASK_ISSUE_PARAM`, `PlanningTaskIssue`, `hasPositivePlanningEffort`, `isPlanningLeafTask`, `parsePlanningIterationId`, `parsePlanningTaskIssue`, `planningIssueTasksHref`, `taskMatchesPlanningIssue` |
| Constants | `PLANNING_TASK_ISSUE_PARAM`, `PLANNING_ITERATION_PARAM`, `PLANNING_TASK_ISSUES` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/gantt/GanttChart.tsx"]
    n1["frontend/src/components/tasks/TaskFiltersBar.tsx"]
    n2["frontend/src/features/planningMasters/masters.ts"]
    n3["frontend/src/features/planningMasters/planningReturn.ts"]
    n4["frontend/src/features/planningMasters/planningTaskIssues.test.ts"]
    n5["frontend/src/features/planningMasters/planningTaskIssues.ts"]
    n6["frontend/src/features/planningMasters/usePlanningReadiness.ts"]
    n7["frontend/src/features/savedViews/taskViewState.ts"]
    n8["frontend/src/pages/PlanMasterPage.tsx"]
    n9["frontend/src/pages/TasksPage.tsx"]
    n10["frontend/src/types/task.ts"]
    n11["frontend/src/utils/taskFilters.ts"]
    n0 --> n5
    n1 --> n5
    n2 --> n3
    n2 --> n5
    n4 --> n5
    n4 --> n10
    n5 --> n3
    n5 --> n10
    n6 --> n2
    n6 --> n5
    n6 --> n10
    n7 --> n1
    n7 --> n5
    n8 --> n2
    n8 --> n3
    n8 --> n5
    n8 --> n6
    n9 --> n1
    n9 --> n5
    n9 --> n7
    n11 --> n1
    n11 --> n5
    n11 --> n10
    click n0 "../modules/GanttChart.md"
    click n1 "../modules/TaskFiltersBar.md"
    click n2 "../modules/planningMasters_masters.md"
    click n3 "../modules/planningReturn.md"
    click n4 "../modules/planningTaskIssues.test.md"
    click n5 "../modules/planningTaskIssues.md"
    click n6 "../modules/usePlanningReadiness.md"
    click n7 "../modules/taskViewState.md"
    click n8 "../modules/PlanMasterPage.md"
    click n9 "../modules/TasksPage.md"
    click n10 "../modules/types_task.md"
    click n11 "../modules/taskFilters.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [GanttChart](../modules/GanttChart.md) |
| Inbound | [TaskFiltersBar](../modules/TaskFiltersBar.md) |
| Inbound | [planningMasters_masters](../modules/planningMasters_masters.md) |
| Inbound | [planningTaskIssues.test](../modules/planningTaskIssues.test.md) |
| Inbound | [usePlanningReadiness](../modules/usePlanningReadiness.md) |
| Inbound | [taskViewState](../modules/taskViewState.md) |
| Inbound | [PlanMasterPage](../modules/PlanMasterPage.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Inbound | [taskFilters](../modules/taskFilters.md) |
| Outbound | [planningReturn](../modules/planningReturn.md) |
| Outbound | [types_task](../modules/types_task.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [PlanningTaskIssue](../entities/PlanningTaskIssue.md) | Type alias | 16 | `typeof PLANNING_TASK_ISSUES[number]` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `parsePlanningTaskIssue` | `(value: unknown) -> PlanningTaskIssue \| null` | — | — |
| `parsePlanningIterationId` | `(value: unknown) -> number \| null` | — | — |
| `isPlanningLeafTask` | `(task: Task)` | — | — |
| `hasPositivePlanningEffort` | `(value: number \| null) -> value is number` | — | — |
| `taskMatchesPlanningIssue` | `(task: Task, issue: PlanningTaskIssue)` | — | — |
| `planningIssueTasksHref` | <pre><code>&#40;&#123;&#10;    issue&#44;&#10;    iterationId&#44;&#10;    returnStepId&#44;&#10;&#125;&#58; &#123;&#10;    issue&#58; PlanningTaskIssue&#59;&#10;    iterationId&#58; number&#59;&#10;    returnStepId&#58; PlanningStepId&#59;&#10;&#125;&#41;</code></pre> | — | — |
