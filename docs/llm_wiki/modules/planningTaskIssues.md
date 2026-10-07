# planningTaskIssues Module

**Path:** `frontend/src/features/planningMasters/planningTaskIssues.ts`

## Description

_Auto-generated from `frontend/src/features/planningMasters/planningTaskIssues.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../types/task` | `Task` |
| `./planningReturn` | `withPlanMasterReturn`, `PlanningStepId` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `PLANNING_ITERATION_PARAM`, `PLANNING_TASK_ISSUES`, `PLANNING_TASK_ISSUE_PARAM`, `PlanningTaskIssue`, `hasPositivePlanningEffort`, `isPlanningLeafTask`, `parsePlanningIterationId`, `parsePlanningTaskIssue`, `planningIssueTasksHref`, `taskMatchesPlanningIssue` |
| Constants | `PLANNING_TASK_ISSUE_PARAM`, `PLANNING_ITERATION_PARAM`, `PLANNING_TASK_ISSUES` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/TaskFiltersBar.tsx"]
    n1["frontend/src/features/planningMasters/masters.ts"]
    n2["frontend/src/features/planningMasters/planningReturn.ts"]
    n3["frontend/src/features/planningMasters/planningTaskIssues.test.ts"]
    n4["frontend/src/features/planningMasters/planningTaskIssues.ts"]
    n5["frontend/src/features/planningMasters/usePlanningReadiness.ts"]
    n6["frontend/src/features/savedViews/taskViewState.ts"]
    n7["frontend/src/pages/PlanMasterPage.tsx"]
    n8["frontend/src/pages/TasksPage.tsx"]
    n9["frontend/src/types/task.ts"]
    n10["frontend/src/utils/taskFilters.ts"]
    n0 --> n4
    n1 --> n2
    n1 --> n4
    n3 --> n4
    n3 --> n9
    n4 --> n2
    n4 --> n9
    n5 --> n1
    n5 --> n4
    n5 --> n9
    n6 --> n0
    n6 --> n4
    n7 --> n1
    n7 --> n2
    n7 --> n4
    n7 --> n5
    n8 --> n0
    n8 --> n4
    n8 --> n6
    n10 --> n0
    n10 --> n4
    n10 --> n9
    click n0 "../modules/TaskFiltersBar.md"
    click n1 "../modules/planningMasters_masters.md"
    click n2 "../modules/planningReturn.md"
    click n3 "../modules/planningTaskIssues.test.md"
    click n4 "../modules/planningTaskIssues.md"
    click n5 "../modules/usePlanningReadiness.md"
    click n6 "../modules/taskViewState.md"
    click n7 "../modules/PlanMasterPage.md"
    click n8 "../modules/TasksPage.md"
    click n9 "../modules/types_task.md"
    click n10 "../modules/taskFilters.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
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
| [PlanningTaskIssue](../entities/PlanningTaskIssue.md) | Type alias | 16 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `parsePlanningTaskIssue` | `(value: unknown) -> PlanningTaskIssue \| null` | — | — |
| `parsePlanningIterationId` | `(value: unknown) -> number \| null` | — | — |
| `isPlanningLeafTask` | `(task: Task)` | — | — |
| `hasPositivePlanningEffort` | `(value: number \| null) -> value is number` | — | — |
| `taskMatchesPlanningIssue` | `(task: Task, issue: PlanningTaskIssue)` | — | — |
| `planningIssueTasksHref` | `({     issue,     iterationId,     returnStepId, }: {     issue: PlanningTaskIssue;     iterationId: number;     returnStepId: PlanningStepId; })` | — | — |
