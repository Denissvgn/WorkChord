# taskService Module

**Path:** `frontend/src/services/taskService.ts`

## Description

_Auto-generated from `frontend/src/services/taskService.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../types/task` | `Task`, `TaskCreate`, `ExternalLink`, `ExternalLinkCreate`, `ExternalLinkUpdate`, `GitHubExternalLinkCreate`, `GroundedAISuggestionResponse`, `TaskFormalizeResponse`, `TaskAISuggestRequest`, `TaskBulkOperationRequest`, `TaskBulkOperationResponse`, `TaskImportDestination`, `TaskImproveDescriptionResponse`, `TaskMoveRequest`, `TaskUpdate`, `TaskMergeRequest`, `TaskStatus`, `TaskStatusChangeResponse`, `TaskStatusLog`, `TaskTimelineResponse`, `TasksImportRequest`, `TasksImportResponse`, `TaskTextContext`, `TaskBatchUpdateRequest`, `TaskBatchUpdateResponse`, `TaskActions`, `TaskCommand`, `TaskDetail`, `TaskBrief`, `CriterionProgress`, `TaskReferencePage` | Declaration | erased |
| `../types/team` | `AssigneeRecommendation` | Declaration | erased |
| `./api` | `api` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `MetricMatchPage`, `MetricScope`, `WorkMetricName`, `taskService` |
| Constants | `taskService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/services/taskService.ts"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/taskService.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (32) |
| Outbound | `frontend` (3) |

> All 35 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [MetricMatchPage](../entities/MetricMatchPage.md) | Interface | 277 | — | — |
| [WorkMetricName](../entities/WorkMetricName.md) | Type alias | 274 | <pre><code>&#39;total&#39; &#124; &#39;planned&#39; &#124; &#39;active&#39; &#124; &#39;resolved&#39; &#124; &#39;closed&#39; &#124; &#39;implemented&#39; &#124; &#39;accepted&#39; &#124; &#39;blocked&#39;&#10;    &#124; &#39;overdue&#39; &#124; &#39;late&#95;start&#39; &#124; &#39;iteration&#95;overflow&#39; &#124; &#39;acceptance&#95;unknown&#39; &#124; &#39;unknown&#95;estimate&#39;</code></pre> | — |
| [MetricScope](../entities/MetricScope.md) | Type alias | 276 | `{ project_id: number } \| { iteration_id: number } \| { release_id: number }` | — |
