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
| Exports | `BriefCriterion`, `CascadeUpdateInfo`, `CriterionProgress`, `ExternalLink`, `ExternalLinkCreate`, `ExternalLinkProvider`, `ExternalLinkUpdate`, `GitHubExternalLinkCreate`, `GroundedAISuggestionResponse`, `GroundedFact`, `ReactivationRequirement`, `ReactivationRequirementInput`, `ReactivationRequirementKind`, `SuggestedSubtask`, `Task`, `TaskAISuggestRequest`, `TaskActionAvailability`, `TaskActions`, `TaskAgentReadiness`, `TaskAgentReadinessCriterion`, `TaskAssignee`, `TaskBatchUpdateItem`, `TaskBatchUpdateRequest`, `TaskBatchUpdateResponse`, `TaskBatchUpdateResponseItem`, `TaskBrief`, `TaskBulkAction`, `TaskBulkOperationRequest`, `TaskBulkOperationResponse`, `TaskBulkOperationResult`, `TaskBulkOutcome`, `TaskClaimedBy`, `TaskCommand`, `TaskCreate`, `TaskDetail`, `TaskDisplayedState`, `TaskFormalizeResponse`, `TaskImportDestination`, `TaskImproveDescriptionResponse`, `TaskMergeRequest`, `TaskMilestone`, `TaskMoveRequest`, `TaskPostponementRecord`, `TaskPostponementResponse`, `TaskProgress`, `TaskProject`, `TaskReference`, `TaskReferencePage`, `TaskReviewRecord`, `TaskStatus`, `TaskStatusChangeResponse`, `TaskStatusLog`, `TaskStatusStats`, `TaskTerminalState`, `TaskTextContext`, `TaskTimelineItem`, `TaskTimelineResponse`, `TaskUpdate`, `TaskVersionConflictDetail`, `TasksImportRequest`, `TasksImportResponse` |

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
| Inbound | `frontend` (116) |
| Outbound | `frontend` (2) |

> All 117 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskAssignee](../entities/types_task_TaskAssignee.md) | Interface | 4 | — | — |
| [TaskClaimedBy](../entities/types_task_TaskClaimedBy.md) | Interface | 11 | — | — |
| [TaskProject](../entities/types_task_TaskProject.md) | Interface | 17 | — | — |
| [TaskMilestone](../entities/types_task_TaskMilestone.md) | Interface | 24 | — | — |
| [TaskAgentReadinessCriterion](../entities/types_task_TaskAgentReadinessCriterion.md) | Interface | 32 | — | — |
| [TaskAgentReadiness](../entities/types_task_TaskAgentReadiness.md) | Interface | 39 | — | — |
| [ExternalLink](../entities/types_task_ExternalLink.md) | Interface | 58 | — | — |
| [ExternalLinkCreate](../entities/types_task_ExternalLinkCreate.md) | Interface | 73 | — | — |
| [GitHubExternalLinkCreate](../entities/types_task_GitHubExternalLinkCreate.md) | Interface | 82 | — | — |
| [ExternalLinkUpdate](../entities/types_task_ExternalLinkUpdate.md) | Interface | 86 | — | — |
| [Task](../entities/types_task_Task.md) | Interface | 95 | — | — |
| [TaskCreate](../entities/types_task_TaskCreate.md) | Interface | 181 | — | — |
| [TaskUpdate](../entities/types_task_TaskUpdate.md) | Interface | 208 | `Partial<TaskCreate>` | — |
| [TaskMoveRequest](../entities/types_task_TaskMoveRequest.md) | Interface | 214 | — | — |
| [TaskVersionConflictDetail](../entities/TaskVersionConflictDetail.md) | Interface | 221 | — | — |
| [SuggestedSubtask](../entities/types_task_SuggestedSubtask.md) | Interface | 228 | — | — |
| [TaskFormalizeResponse](../entities/TaskFormalizeResponse.md) | Interface | 233 | — | — |
| [TaskImproveDescriptionResponse](../entities/TaskImproveDescriptionResponse.md) | Interface | 242 | — | — |
| [GroundedFact](../entities/types_task_GroundedFact.md) | Interface | 247 | — | — |
| [TaskAISuggestRequest](../entities/types_task_TaskAISuggestRequest.md) | Interface | 252 | — | — |
| [GroundedAISuggestionResponse](../entities/types_task_GroundedAISuggestionResponse.md) | Interface | 277 | — | — |
| [TasksImportRequest](../entities/types_task_TasksImportRequest.md) | Interface | 297 | — | — |
| [TaskTextContext](../entities/types_task_TaskTextContext.md) | Interface | 303 | — | — |
| [TasksImportResponse](../entities/types_task_TasksImportResponse.md) | Interface | 309 | — | — |
| [TaskMergeRequest](../entities/TaskMergeRequest.md) | Interface | 317 | — | — |
| [TaskBulkOperationRequest](../entities/types_task_TaskBulkOperationRequest.md) | Interface | 341 | — | — |
| [TaskBulkOperationResult](../entities/types_task_TaskBulkOperationResult.md) | Interface | 350 | — | — |
| [TaskBulkOperationResponse](../entities/types_task_TaskBulkOperationResponse.md) | Interface | 360 | — | — |
| [CascadeUpdateInfo](../entities/types_task_CascadeUpdateInfo.md) | Interface | 370 | — | — |
| [TaskStatusChangeResponse](../entities/types_task_TaskStatusChangeResponse.md) | Interface | 379 | — | — |
| [TaskStatusLog](../entities/types_task_TaskStatusLog.md) | Interface | 385 | — | — |
| [TaskStatusStats](../entities/types_task_TaskStatusStats.md) | Interface | 397 | — | — |
| [TaskTimelineItem](../entities/types_task_TaskTimelineItem.md) | Interface | 403 | — | — |
| [TaskTimelineResponse](../entities/types_task_TaskTimelineResponse.md) | Interface | 414 | — | — |
| [TaskBatchUpdateItem](../entities/types_task_TaskBatchUpdateItem.md) | Interface | 419 | — | — |
| [TaskBatchUpdateRequest](../entities/types_task_TaskBatchUpdateRequest.md) | Interface | 426 | — | — |
| [TaskBatchUpdateResponseItem](../entities/types_task_TaskBatchUpdateResponseItem.md) | Interface | 432 | — | — |
| [TaskBatchUpdateResponse](../entities/types_task_TaskBatchUpdateResponse.md) | Interface | 438 | — | — |
| [BriefCriterion](../entities/types_task_BriefCriterion.md) | Interface | 444 | — | — |
| [TaskBrief](../entities/types_task_TaskBrief.md) | Interface | 451 | — | — |
| [CriterionProgress](../entities/types_task_CriterionProgress.md) | Interface | 462 | — | — |
| [TaskProgress](../entities/TaskProgress.md) | Interface | 469 | — | — |
| [TaskReference](../entities/types_task_TaskReference.md) | Interface | 476 | — | — |
| [TaskReferencePage](../entities/types_task_TaskReferencePage.md) | Interface | 483 | — | — |
| [TaskDetail](../entities/TaskDetail.md) | Interface | 484 | — | — |
| [ReactivationRequirementInput](../entities/types_task_ReactivationRequirementInput.md) | Interface | 492 | — | — |
| [ReactivationRequirement](../entities/ReactivationRequirement.md) | Interface | 495 | — | — |
| [TaskPostponementRecord](../entities/types_task_TaskPostponementRecord.md) | Interface | 499 | — | — |
| [TaskPostponementResponse](../entities/types_task_TaskPostponementResponse.md) | Interface | 505 | — | — |
| [TaskReviewRecord](../entities/types_task_TaskReviewRecord.md) | Interface | 507 | — | One recorded review. `owner_override` is an owner's acceptance that set aside publisher independence. |
| [TaskActionAvailability](../entities/types_task_TaskActionAvailability.md) | Interface | 511 | — | — |
| [TaskActions](../entities/TaskActions.md) | Interface | 512 | — | — |
| [TaskCommand](../entities/TaskCommand.md) | Interface | 516 | — | — |
| [TaskStatus](../entities/types_task_TaskStatus.md) | Type alias | 51 | `'planned' \| 'active' \| 'resolved' \| 'postponed' \| 'closed'` | — |
| [TaskTerminalState](../entities/TaskTerminalState.md) | Type alias | 53 | `'canceled' \| 'superseded'` | Withdrawn work: canceled, or superseded when another task delivers its work (a clean replacement included). |
| [TaskDisplayedState](../entities/TaskDisplayedState.md) | Type alias | 55 | `TaskStatus \| TaskTerminalState` | What a task is shown as: its stored status, or its terminal state. |
| [ExternalLinkProvider](../entities/types_task_ExternalLinkProvider.md) | Type alias | 56 | `'github' \| 'gitlab' \| 'figma' \| 'sentry' \| 'custom' \| 'agdash' \| string` | — |
| [TaskImportDestination](../entities/types_task_TaskImportDestination.md) | Type alias | 295 | `'tasks' \| 'triage' \| 'auto'` | — |
| [TaskBulkAction](../entities/types_task_TaskBulkAction.md) | Type alias | 324 | <pre><code>&#124; &#39;set&#95;assignee&#39;&#10;    &#124; &#39;clear&#95;assignee&#39;&#10;    &#124; &#39;auto&#95;assign&#39;&#10;    &#124; &#39;set&#95;project&#39;&#10;    &#124; &#39;clear&#95;project&#39;&#10;    &#124; &#39;set&#95;milestone&#39;&#10;    &#124; &#39;clear&#95;milestone&#39;&#10;    &#124; &#39;set&#95;priority&#39;&#10;    &#124; &#39;add&#95;labels&#39;&#10;    &#124; &#39;remove&#95;labels&#39;&#10;    &#124; &#39;set&#95;flags&#39;&#10;    &#124; &#39;change&#95;status&#39;&#10;    &#124; &#39;delete&#39;</code></pre> | — |
| [TaskBulkOutcome](../entities/types_task_TaskBulkOutcome.md) | Type alias | 339 | `'updated' \| 'deleted' \| 'skipped' \| 'failed' \| 'would_update' \| 'would_delete'` | — |
| [ReactivationRequirementKind](../entities/ReactivationRequirementKind.md) | Type alias | 491 | `'predecessor_accepted' \| 'date' \| 'owner_decision' \| 'linked_resolved'` | — |
