# task Module

**Path:** `frontend/src/types/task.ts`

## Description

_Auto-generated from `frontend/src/types/task.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./team` | `AssigneeRecommendation` | Declaration | erased |
| `./triage` | `TriageItem` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `BriefCriterion`, `CascadeUpdateInfo`, `CriterionProgress`, `ExternalLink`, `ExternalLinkCreate`, `ExternalLinkProvider`, `ExternalLinkUpdate`, `GitHubExternalLinkCreate`, `GroundedAISuggestionResponse`, `GroundedFact`, `SuggestedSubtask`, `Task`, `TaskAISuggestRequest`, `TaskActionAvailability`, `TaskActions`, `TaskAgentReadiness`, `TaskAgentReadinessCriterion`, `TaskAssignee`, `TaskBatchUpdateItem`, `TaskBatchUpdateRequest`, `TaskBatchUpdateResponse`, `TaskBatchUpdateResponseItem`, `TaskBrief`, `TaskBulkAction`, `TaskBulkOperationRequest`, `TaskBulkOperationResponse`, `TaskBulkOperationResult`, `TaskBulkOutcome`, `TaskClaimedBy`, `TaskCommand`, `TaskCreate`, `TaskDetail`, `TaskFormalizeResponse`, `TaskImportDestination`, `TaskImproveDescriptionResponse`, `TaskMergeRequest`, `TaskMilestone`, `TaskMoveRequest`, `TaskProgress`, `TaskProject`, `TaskReference`, `TaskReferencePage`, `TaskStatus`, `TaskStatusChangeResponse`, `TaskStatusLog`, `TaskStatusStats`, `TaskTextContext`, `TaskTimelineItem`, `TaskTimelineResponse`, `TaskUpdate`, `TaskVersionConflictDetail`, `TasksImportRequest`, `TasksImportResponse` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/types/task.ts"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/types_task.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (69) |
| Outbound | `frontend` (2) |

> All 70 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskAssignee](../entities/types_task_TaskAssignee.md) | Interface | 4 | — | — |
| [TaskClaimedBy](../entities/types_task_TaskClaimedBy.md) | Interface | 9 | — | — |
| [TaskProject](../entities/types_task_TaskProject.md) | Interface | 15 | — | — |
| [TaskMilestone](../entities/types_task_TaskMilestone.md) | Interface | 22 | — | — |
| [TaskAgentReadinessCriterion](../entities/types_task_TaskAgentReadinessCriterion.md) | Interface | 30 | — | — |
| [TaskAgentReadiness](../entities/types_task_TaskAgentReadiness.md) | Interface | 37 | — | — |
| [ExternalLink](../entities/types_task_ExternalLink.md) | Interface | 52 | — | — |
| [ExternalLinkCreate](../entities/types_task_ExternalLinkCreate.md) | Interface | 67 | — | — |
| [GitHubExternalLinkCreate](../entities/types_task_GitHubExternalLinkCreate.md) | Interface | 76 | — | — |
| [ExternalLinkUpdate](../entities/types_task_ExternalLinkUpdate.md) | Interface | 80 | — | — |
| [Task](../entities/types_task_Task.md) | Interface | 89 | — | — |
| [TaskCreate](../entities/types_task_TaskCreate.md) | Interface | 169 | — | — |
| [TaskUpdate](../entities/types_task_TaskUpdate.md) | Interface | 195 | `Partial<TaskCreate>` | — |
| [TaskMoveRequest](../entities/types_task_TaskMoveRequest.md) | Interface | 201 | — | — |
| [TaskVersionConflictDetail](../entities/TaskVersionConflictDetail.md) | Interface | 208 | — | — |
| [SuggestedSubtask](../entities/types_task_SuggestedSubtask.md) | Interface | 215 | — | — |
| [TaskFormalizeResponse](../entities/TaskFormalizeResponse.md) | Interface | 220 | — | — |
| [TaskImproveDescriptionResponse](../entities/TaskImproveDescriptionResponse.md) | Interface | 229 | — | — |
| [GroundedFact](../entities/types_task_GroundedFact.md) | Interface | 234 | — | — |
| [TaskAISuggestRequest](../entities/types_task_TaskAISuggestRequest.md) | Interface | 239 | — | — |
| [GroundedAISuggestionResponse](../entities/types_task_GroundedAISuggestionResponse.md) | Interface | 264 | — | — |
| [TasksImportRequest](../entities/types_task_TasksImportRequest.md) | Interface | 284 | — | — |
| [TaskTextContext](../entities/types_task_TaskTextContext.md) | Interface | 290 | — | — |
| [TasksImportResponse](../entities/types_task_TasksImportResponse.md) | Interface | 296 | — | — |
| [TaskMergeRequest](../entities/TaskMergeRequest.md) | Interface | 304 | — | — |
| [TaskBulkOperationRequest](../entities/types_task_TaskBulkOperationRequest.md) | Interface | 328 | — | — |
| [TaskBulkOperationResult](../entities/types_task_TaskBulkOperationResult.md) | Interface | 337 | — | — |
| [TaskBulkOperationResponse](../entities/types_task_TaskBulkOperationResponse.md) | Interface | 347 | — | — |
| [CascadeUpdateInfo](../entities/types_task_CascadeUpdateInfo.md) | Interface | 357 | — | — |
| [TaskStatusChangeResponse](../entities/types_task_TaskStatusChangeResponse.md) | Interface | 366 | — | — |
| [TaskStatusLog](../entities/types_task_TaskStatusLog.md) | Interface | 372 | — | — |
| [TaskStatusStats](../entities/types_task_TaskStatusStats.md) | Interface | 384 | — | — |
| [TaskTimelineItem](../entities/types_task_TaskTimelineItem.md) | Interface | 390 | — | — |
| [TaskTimelineResponse](../entities/types_task_TaskTimelineResponse.md) | Interface | 401 | — | — |
| [TaskBatchUpdateItem](../entities/types_task_TaskBatchUpdateItem.md) | Interface | 406 | — | — |
| [TaskBatchUpdateRequest](../entities/types_task_TaskBatchUpdateRequest.md) | Interface | 413 | — | — |
| [TaskBatchUpdateResponseItem](../entities/types_task_TaskBatchUpdateResponseItem.md) | Interface | 419 | — | — |
| [TaskBatchUpdateResponse](../entities/types_task_TaskBatchUpdateResponse.md) | Interface | 425 | — | — |
| [BriefCriterion](../entities/types_task_BriefCriterion.md) | Interface | 431 | — | — |
| [TaskBrief](../entities/types_task_TaskBrief.md) | Interface | 438 | — | — |
| [CriterionProgress](../entities/types_task_CriterionProgress.md) | Interface | 449 | — | — |
| [TaskProgress](../entities/TaskProgress.md) | Interface | 456 | — | — |
| [TaskReference](../entities/types_task_TaskReference.md) | Interface | 463 | — | — |
| [TaskReferencePage](../entities/types_task_TaskReferencePage.md) | Interface | 470 | — | — |
| [TaskDetail](../entities/TaskDetail.md) | Interface | 471 | — | — |
| [TaskActionAvailability](../entities/types_task_TaskActionAvailability.md) | Interface | 476 | — | — |
| [TaskActions](../entities/TaskActions.md) | Interface | 477 | — | — |
| [TaskCommand](../entities/TaskCommand.md) | Interface | 481 | — | — |
| [TaskStatus](../entities/types_task_TaskStatus.md) | Type alias | 49 | `'planned' \| 'active' \| 'resolved' \| 'closed'` | — |
| [ExternalLinkProvider](../entities/types_task_ExternalLinkProvider.md) | Type alias | 50 | `'github' \| 'gitlab' \| 'figma' \| 'sentry' \| 'custom' \| string` | — |
| [TaskImportDestination](../entities/types_task_TaskImportDestination.md) | Type alias | 282 | `'tasks' \| 'triage' \| 'auto'` | — |
| [TaskBulkAction](../entities/types_task_TaskBulkAction.md) | Type alias | 311 | <pre><code>&#124; &#39;set&#95;assignee&#39;&#10;    &#124; &#39;clear&#95;assignee&#39;&#10;    &#124; &#39;auto&#95;assign&#39;&#10;    &#124; &#39;set&#95;project&#39;&#10;    &#124; &#39;clear&#95;project&#39;&#10;    &#124; &#39;set&#95;milestone&#39;&#10;    &#124; &#39;clear&#95;milestone&#39;&#10;    &#124; &#39;set&#95;priority&#39;&#10;    &#124; &#39;add&#95;labels&#39;&#10;    &#124; &#39;remove&#95;labels&#39;&#10;    &#124; &#39;set&#95;flags&#39;&#10;    &#124; &#39;change&#95;status&#39;&#10;    &#124; &#39;delete&#39;</code></pre> | — |
| [TaskBulkOutcome](../entities/types_task_TaskBulkOutcome.md) | Type alias | 326 | `'updated' \| 'deleted' \| 'skipped' \| 'failed' \| 'would_update' \| 'would_delete'` | — |
