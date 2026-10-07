# task Module

**Path:** `frontend/src/types/task.ts`

## Description

_Auto-generated from `frontend/src/types/task.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `./team` | `AssigneeRecommendation` |
| `./triage` | `TriageItem` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `BriefCriterion`, `CascadeUpdateInfo`, `CriterionProgress`, `ExternalLink`, `ExternalLinkCreate`, `ExternalLinkProvider`, `ExternalLinkUpdate`, `GitHubExternalLinkCreate`, `GroundedAISuggestionResponse`, `GroundedFact`, `SuggestedSubtask`, `Task`, `TaskAISuggestRequest`, `TaskActionAvailability`, `TaskActions`, `TaskAgentReadiness`, `TaskAgentReadinessCriterion`, `TaskAssignee`, `TaskBatchUpdateItem`, `TaskBatchUpdateRequest`, `TaskBatchUpdateResponse`, `TaskBatchUpdateResponseItem`, `TaskBrief`, `TaskBulkAction`, `TaskBulkOperationRequest`, `TaskBulkOperationResponse`, `TaskBulkOperationResult`, `TaskBulkOutcome`, `TaskClaimedBy`, `TaskCommand`, `TaskCreate`, `TaskDetail`, `TaskFormalizeResponse`, `TaskImportDestination`, `TaskImproveDescriptionResponse`, `TaskMergeRequest`, `TaskMilestone`, `TaskMoveRequest`, `TaskProgress`, `TaskProject`, `TaskReference`, `TaskReferencePage`, `TaskStatus`, `TaskStatusChangeResponse`, `TaskStatusLog`, `TaskStatusStats`, `TaskTextContext`, `TaskTimelineItem`, `TaskTimelineResponse`, `TaskUpdate`, `TaskVersionConflictDetail`, `TasksImportRequest`, `TasksImportResponse` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
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
| Inbound | `frontend` (61) |
| Outbound | `frontend` (2) |

> All 62 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskAssignee](../entities/types_task_TaskAssignee.md) | Class | 4 | — | — |
| [TaskClaimedBy](../entities/types_task_TaskClaimedBy.md) | Class | 9 | — | — |
| [TaskProject](../entities/types_task_TaskProject.md) | Class | 15 | — | — |
| [TaskMilestone](../entities/types_task_TaskMilestone.md) | Class | 22 | — | — |
| [TaskAgentReadinessCriterion](../entities/types_task_TaskAgentReadinessCriterion.md) | Class | 30 | — | — |
| [TaskAgentReadiness](../entities/types_task_TaskAgentReadiness.md) | Class | 37 | — | — |
| [ExternalLink](../entities/types_task_ExternalLink.md) | Class | 48 | — | — |
| [ExternalLinkCreate](../entities/types_task_ExternalLinkCreate.md) | Class | 63 | — | — |
| [GitHubExternalLinkCreate](../entities/types_task_GitHubExternalLinkCreate.md) | Class | 72 | — | — |
| [ExternalLinkUpdate](../entities/types_task_ExternalLinkUpdate.md) | Class | 76 | — | — |
| [Task](../entities/types_task_Task.md) | Class | 85 | — | — |
| [TaskCreate](../entities/types_task_TaskCreate.md) | Class | 163 | — | — |
| [TaskUpdate](../entities/types_task_TaskUpdate.md) | Class | 189 | `Partial` | — |
| [TaskMoveRequest](../entities/types_task_TaskMoveRequest.md) | Class | 195 | — | — |
| [TaskVersionConflictDetail](../entities/TaskVersionConflictDetail.md) | Class | 202 | — | — |
| [SuggestedSubtask](../entities/types_task_SuggestedSubtask.md) | Class | 209 | — | — |
| [TaskFormalizeResponse](../entities/TaskFormalizeResponse.md) | Class | 214 | — | — |
| [TaskImproveDescriptionResponse](../entities/TaskImproveDescriptionResponse.md) | Class | 223 | — | — |
| [GroundedFact](../entities/types_task_GroundedFact.md) | Class | 228 | — | — |
| [TaskAISuggestRequest](../entities/types_task_TaskAISuggestRequest.md) | Class | 233 | — | — |
| [GroundedAISuggestionResponse](../entities/types_task_GroundedAISuggestionResponse.md) | Class | 258 | — | — |
| [TasksImportRequest](../entities/types_task_TasksImportRequest.md) | Class | 278 | — | — |
| [TaskTextContext](../entities/types_task_TaskTextContext.md) | Class | 284 | — | — |
| [TasksImportResponse](../entities/types_task_TasksImportResponse.md) | Class | 290 | — | — |
| [TaskMergeRequest](../entities/TaskMergeRequest.md) | Class | 298 | — | — |
| [TaskBulkOperationRequest](../entities/types_task_TaskBulkOperationRequest.md) | Class | 322 | — | — |
| [TaskBulkOperationResult](../entities/types_task_TaskBulkOperationResult.md) | Class | 331 | — | — |
| [TaskBulkOperationResponse](../entities/types_task_TaskBulkOperationResponse.md) | Class | 341 | — | — |
| [CascadeUpdateInfo](../entities/types_task_CascadeUpdateInfo.md) | Class | 351 | — | — |
| [TaskStatusChangeResponse](../entities/types_task_TaskStatusChangeResponse.md) | Class | 360 | — | — |
| [TaskStatusLog](../entities/types_task_TaskStatusLog.md) | Class | 366 | — | — |
| [TaskStatusStats](../entities/types_task_TaskStatusStats.md) | Class | 378 | — | — |
| [TaskTimelineItem](../entities/types_task_TaskTimelineItem.md) | Class | 384 | — | — |
| [TaskTimelineResponse](../entities/types_task_TaskTimelineResponse.md) | Class | 394 | — | — |
| [TaskBatchUpdateItem](../entities/types_task_TaskBatchUpdateItem.md) | Class | 399 | — | — |
| [TaskBatchUpdateRequest](../entities/types_task_TaskBatchUpdateRequest.md) | Class | 406 | — | — |
| [TaskBatchUpdateResponseItem](../entities/types_task_TaskBatchUpdateResponseItem.md) | Class | 412 | — | — |
| [TaskBatchUpdateResponse](../entities/types_task_TaskBatchUpdateResponse.md) | Class | 418 | — | — |
| [BriefCriterion](../entities/types_task_BriefCriterion.md) | Class | 424 | — | — |
| [TaskBrief](../entities/types_task_TaskBrief.md) | Class | 431 | — | — |
| [CriterionProgress](../entities/types_task_CriterionProgress.md) | Class | 442 | — | — |
| [TaskProgress](../entities/TaskProgress.md) | Class | 449 | — | — |
| [TaskReference](../entities/types_task_TaskReference.md) | Class | 456 | — | — |
| [TaskReferencePage](../entities/types_task_TaskReferencePage.md) | Class | 462 | — | — |
| [TaskDetail](../entities/TaskDetail.md) | Class | 463 | — | — |
| [TaskActionAvailability](../entities/types_task_TaskActionAvailability.md) | Class | 467 | — | — |
| [TaskActions](../entities/TaskActions.md) | Class | 468 | — | — |
| [TaskCommand](../entities/TaskCommand.md) | Class | 472 | — | — |
| [TaskStatus](../entities/types_task_TaskStatus.md) | Type alias | 45 | — | — |
| [ExternalLinkProvider](../entities/types_task_ExternalLinkProvider.md) | Type alias | 46 | — | — |
| [TaskImportDestination](../entities/types_task_TaskImportDestination.md) | Type alias | 276 | — | — |
| [TaskBulkAction](../entities/types_task_TaskBulkAction.md) | Type alias | 305 | — | — |
| [TaskBulkOutcome](../entities/types_task_TaskBulkOutcome.md) | Type alias | 320 | — | — |
