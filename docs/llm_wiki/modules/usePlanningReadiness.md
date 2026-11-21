# usePlanningReadiness Module

**Path:** `frontend/src/features/planningMasters/usePlanningReadiness.ts`

## Description

_Auto-generated from `frontend/src/features/planningMasters/usePlanningReadiness.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/ganttService` | `ganttService` | — | compiler-dependent |
| `../../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../../services/taskService` | `taskService` | — | compiler-dependent |
| `../../services/teamService` | `teamService` | — | compiler-dependent |
| `../../services/triageService` | `triageService` | — | compiler-dependent |
| `../../types/gantt` | `GanttResponse` | Declaration | erased |
| `../../types/iteration` | `Iteration` | Declaration | erased |
| `../../types/task` | `Task` | Declaration | erased |
| `../../types/team` | `TeamMember` | Declaration | erased |
| `../scope/useWorkScope` | `useWorkScope` | — | compiler-dependent |
| `./masters` | `PlanReadiness` | Declaration | erased |
| `./planningTaskIssues` | `hasPositivePlanningEffort`, `isAgentWorkingWithoutCapacity`, `isPlanningLeafTask`, `taskMatchesPlanningIssue` | — | compiler-dependent |
| `./usePlanningNavigationSummary` | `planningNavigationSummaryKey` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `react` | `useMemo` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `PlanningQueryFeedback`, `usePlanningReadiness` |
| Constants | `HOURS_PER_DAY`, `ISO_DATE`, `MILLISECONDS_PER_DAY`, `finitePositive` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/features/planningMasters/usePlanningReadiness.ts"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/usePlanningReadiness.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (3) |
| Outbound | `frontend` (13) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

> All 16 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [PlanningReadinessOptions](../entities/PlanningReadinessOptions.md) | Type alias | 22 | <pre><code>&#123;&#10;    includeInbox&#63;&#58; boolean&#59;&#10;&#125;</code></pre> | — |
| [PlanningTeamMember](../entities/PlanningTeamMember.md) | Type alias | 30 | <pre><code>TeamMember &#38; &#123;&#10;    capacity&#95;hours&#58; number&#59;&#10;    planned&#95;hours&#58; number&#59;&#10;&#125;</code></pre> | — |
| [PlanningQueryFeedback](../entities/PlanningQueryFeedback.md) | Type alias | 35 | <pre><code>&#123;&#10;    enabled&#58; boolean&#59;&#10;    hasData&#58; boolean&#59;&#10;    dataUpdatedAt&#58; number&#59;&#10;    isLoading&#58; boolean&#59;&#10;    isFetching&#58; boolean&#59;&#10;    isError&#58; boolean&#59;&#10;    isBlockingError&#58; boolean&#59;&#10;    isRefetchError&#58; boolean&#59;&#10;    error&#58; unknown&#59;&#10;    refetch&#58; &#40;&#41; &#61;&#62; Promise&#60;unknown&#62;&#59;&#10;&#125;</code></pre> | — |
| [QueryFeedbackSource](../entities/QueryFeedbackSource.md) | Type alias | 48 | <pre><code>&#123;&#10;    data&#58; unknown&#59;&#10;    dataUpdatedAt&#58; number&#59;&#10;    error&#58; unknown&#59;&#10;    isLoading&#58; boolean&#59;&#10;    isFetching&#58; boolean&#59;&#10;    isError&#58; boolean&#59;&#10;    refetch&#58; &#40;&#41; &#61;&#62; Promise&#60;unknown&#62;&#59;&#10;&#125;</code></pre> | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `usePlanningReadiness` | <pre><code>&#40;&#123;&#10;    includeInbox &#61; false&#44;&#10;&#125;&#58; PlanningReadinessOptions &#61; &#123;&#125;&#41;</code></pre> | — | — |
