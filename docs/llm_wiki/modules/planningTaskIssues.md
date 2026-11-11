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
| Exports | `PLANNING_ITERATION_PARAM`, `PLANNING_TASK_ISSUES`, `PLANNING_TASK_ISSUE_PARAM`, `PlanningTaskIssue`, `hasPositivePlanningEffort`, `isAgentWorkingWithoutCapacity`, `isPlanningGapCandidate`, `isPlanningLeafTask`, `parsePlanningIterationId`, `parsePlanningTaskIssue`, `planningIssueTasksHref`, `taskMatchesPlanningIssue` |
| Constants | `PLANNING_TASK_ISSUE_PARAM`, `PLANNING_ITERATION_PARAM`, `PLANNING_TASK_ISSUES` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/features/planningMasters/planningTaskIssues.ts"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/planningTaskIssues.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (10) |
| Outbound | `frontend` (2) |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

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
| `isPlanningGapCandidate` | `(task: Task)` | — | The server's rule (app/services/planning_issues.py): only planned leaves are scheduling gaps. |
| `isAgentWorkingWithoutCapacity` | `(task: Task)` | — | An agent is working on it, so it is not unassigned, but it still has no capacity row. |
| `hasPositivePlanningEffort` | `(value: number \| null) -> value is number` | — | — |
| `taskMatchesPlanningIssue` | `(task: Task, issue: PlanningTaskIssue)` | — | — |
| `planningIssueTasksHref` | <pre><code>&#40;&#123;&#10;    issue&#44;&#10;    iterationId&#44;&#10;    returnStepId&#44;&#10;&#125;&#58; &#123;&#10;    issue&#58; PlanningTaskIssue&#59;&#10;    iterationId&#58; number&#59;&#10;    returnStepId&#58; PlanningStepId&#59;&#10;&#125;&#41;</code></pre> | — | — |
