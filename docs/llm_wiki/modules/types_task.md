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
| Exports | `CascadeUpdateInfo`, `ExternalLink`, `ExternalLinkCreate`, `ExternalLinkProvider`, `ExternalLinkUpdate`, `GitHubExternalLinkCreate`, `GroundedAISuggestionResponse`, `GroundedFact`, `SuggestedSubtask`, `Task`, `TaskAISuggestRequest`, `TaskAgentReadiness`, `TaskAgentReadinessCriterion`, `TaskAssignee`, `TaskBatchUpdateItem`, `TaskBatchUpdateRequest`, `TaskBatchUpdateResponse`, `TaskBatchUpdateResponseItem`, `TaskBulkAction`, `TaskBulkOperationRequest`, `TaskBulkOperationResponse`, `TaskBulkOperationResult`, `TaskBulkOutcome`, `TaskClaimedBy`, `TaskCreate`, `TaskFormalizeResponse`, `TaskImportDestination`, `TaskImproveDescriptionResponse`, `TaskMergeRequest`, `TaskMilestone`, `TaskMoveRequest`, `TaskProject`, `TaskStatus`, `TaskStatusChangeResponse`, `TaskStatusLog`, `TaskStatusStats`, `TaskTimelineItem`, `TaskTimelineResponse`, `TaskUpdate`, `TaskVersionConflictDetail`, `TasksImportRequest`, `TasksImportResponse` |

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
| Inbound | `frontend` (54) |
| Outbound | `frontend` (2) |

> All 55 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskAssignee](../entities/types_task_TaskAssignee.md) | Class | 4 | — | — |
| [TaskClaimedBy](../entities/types_task_TaskClaimedBy.md) | Class | 9 | — | — |
| [TaskProject](../entities/types_task_TaskProject.md) | Class | 15 | — | — |
| [TaskMilestone](../entities/types_task_TaskMilestone.md) | Class | 22 | — | — |
| [TaskAgentReadinessCriterion](../entities/types_task_TaskAgentReadinessCriterion.md) | Class | 30 | — | — |
| [TaskAgentReadiness](../entities/types_task_TaskAgentReadiness.md) | Class | 37 | — | — |
| [ExternalLink](../entities/types_task_ExternalLink.md) | Class | 47 | — | — |
| [ExternalLinkCreate](../entities/types_task_ExternalLinkCreate.md) | Class | 62 | — | — |
| [GitHubExternalLinkCreate](../entities/types_task_GitHubExternalLinkCreate.md) | Class | 71 | — | — |
| [ExternalLinkUpdate](../entities/types_task_ExternalLinkUpdate.md) | Class | 75 | — | — |
| [Task](../entities/types_task_Task.md) | Class | 84 | — | — |
| [TaskCreate](../entities/types_task_TaskCreate.md) | Class | 145 | — | — |
| [TaskUpdate](../entities/types_task_TaskUpdate.md) | Class | 168 | `Partial` | — |
| [TaskMoveRequest](../entities/types_task_TaskMoveRequest.md) | Class | 174 | — | — |
| [TaskVersionConflictDetail](../entities/TaskVersionConflictDetail.md) | Class | 181 | — | — |
| [SuggestedSubtask](../entities/types_task_SuggestedSubtask.md) | Class | 188 | — | — |
| [TaskFormalizeResponse](../entities/TaskFormalizeResponse.md) | Class | 193 | — | — |
| [TaskImproveDescriptionResponse](../entities/TaskImproveDescriptionResponse.md) | Class | 202 | — | — |
| [GroundedFact](../entities/types_task_GroundedFact.md) | Class | 207 | — | — |
| [TaskAISuggestRequest](../entities/types_task_TaskAISuggestRequest.md) | Class | 212 | — | — |
| [GroundedAISuggestionResponse](../entities/types_task_GroundedAISuggestionResponse.md) | Class | 236 | — | — |
| [TasksImportRequest](../entities/types_task_TasksImportRequest.md) | Class | 256 | — | — |
| [TasksImportResponse](../entities/types_task_TasksImportResponse.md) | Class | 261 | — | — |
| [TaskMergeRequest](../entities/TaskMergeRequest.md) | Class | 269 | — | — |
| [TaskBulkOperationRequest](../entities/types_task_TaskBulkOperationRequest.md) | Class | 293 | — | — |
| [TaskBulkOperationResult](../entities/types_task_TaskBulkOperationResult.md) | Class | 302 | — | — |
| [TaskBulkOperationResponse](../entities/types_task_TaskBulkOperationResponse.md) | Class | 312 | — | — |
| [CascadeUpdateInfo](../entities/types_task_CascadeUpdateInfo.md) | Class | 322 | — | — |
| [TaskStatusChangeResponse](../entities/types_task_TaskStatusChangeResponse.md) | Class | 331 | — | — |
| [TaskStatusLog](../entities/types_task_TaskStatusLog.md) | Class | 337 | — | — |
| [TaskStatusStats](../entities/types_task_TaskStatusStats.md) | Class | 349 | — | — |
| [TaskTimelineItem](../entities/types_task_TaskTimelineItem.md) | Class | 355 | — | — |
| [TaskTimelineResponse](../entities/types_task_TaskTimelineResponse.md) | Class | 365 | — | — |
| [TaskBatchUpdateItem](../entities/types_task_TaskBatchUpdateItem.md) | Class | 370 | — | — |
| [TaskBatchUpdateRequest](../entities/types_task_TaskBatchUpdateRequest.md) | Class | 377 | — | — |
| [TaskBatchUpdateResponseItem](../entities/types_task_TaskBatchUpdateResponseItem.md) | Class | 382 | — | — |
| [TaskBatchUpdateResponse](../entities/types_task_TaskBatchUpdateResponse.md) | Class | 388 | — | — |
| [TaskStatus](../entities/types_task_TaskStatus.md) | Type alias | 44 | — | — |
| [ExternalLinkProvider](../entities/types_task_ExternalLinkProvider.md) | Type alias | 45 | — | — |
| [TaskImportDestination](../entities/types_task_TaskImportDestination.md) | Type alias | 254 | — | — |
| [TaskBulkAction](../entities/types_task_TaskBulkAction.md) | Type alias | 276 | — | — |
| [TaskBulkOutcome](../entities/types_task_TaskBulkOutcome.md) | Type alias | 291 | — | — |
