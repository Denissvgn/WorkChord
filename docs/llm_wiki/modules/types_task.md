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
| Exports | `BriefCriterion`, `CascadeUpdateInfo`, `CriterionProgress`, `ExternalLink`, `ExternalLinkCreate`, `ExternalLinkProvider`, `ExternalLinkUpdate`, `GitHubExternalLinkCreate`, `GroundedAISuggestionResponse`, `GroundedFact`, `ManualProvenanceExecutor`, `ManualProvenanceWrite`, `ReactivationRequirement`, `ReactivationRequirementInput`, `ReactivationRequirementKind`, `RefusalNextStep`, `RoutingCheck`, `RoutingIssue`, `RoutingReviewer`, `RoutingRung`, `SuggestedSubtask`, `Task`, `TaskAISuggestRequest`, `TaskActionAvailability`, `TaskActions`, `TaskAgentReadiness`, `TaskAgentReadinessCriterion`, `TaskAssignee`, `TaskBatchUpdateItem`, `TaskBatchUpdateRequest`, `TaskBatchUpdateResponse`, `TaskBatchUpdateResponseItem`, `TaskBrief`, `TaskBulkAction`, `TaskBulkOperationRequest`, `TaskBulkOperationResponse`, `TaskBulkOperationResult`, `TaskBulkOutcome`, `TaskClaimedBy`, `TaskCommand`, `TaskCreate`, `TaskDetail`, `TaskDisplayedState`, `TaskFormalizeResponse`, `TaskImportDestination`, `TaskImproveDescriptionResponse`, `TaskMergeRequest`, `TaskMilestone`, `TaskMoveRequest`, `TaskPostponementRecord`, `TaskPostponementResponse`, `TaskProgress`, `TaskProject`, `TaskReference`, `TaskReferencePage`, `TaskReviewRecord`, `TaskRouting`, `TaskRoutingConflictMode`, `TaskRoutingResolution`, `TaskStatus`, `TaskStatusChangeResponse`, `TaskStatusLog`, `TaskStatusStats`, `TaskTerminalState`, `TaskTextContext`, `TaskTimelineItem`, `TaskTimelineResponse`, `TaskUpdate`, `TaskVersionConflictDetail`, `TasksImportRequest`, `TasksImportResponse` |

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
| Inbound | `frontend` (126) |
| Outbound | `frontend` (2) |

> All 127 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

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
| [TaskCreate](../entities/types_task_TaskCreate.md) | Interface | 183 | — | — |
| [TaskUpdate](../entities/types_task_TaskUpdate.md) | Interface | 210 | `Partial<TaskCreate>` | — |
| [TaskMoveRequest](../entities/types_task_TaskMoveRequest.md) | Interface | 218 | — | — |
| [TaskVersionConflictDetail](../entities/TaskVersionConflictDetail.md) | Interface | 225 | — | — |
| [SuggestedSubtask](../entities/types_task_SuggestedSubtask.md) | Interface | 232 | — | — |
| [TaskFormalizeResponse](../entities/TaskFormalizeResponse.md) | Interface | 237 | — | — |
| [TaskImproveDescriptionResponse](../entities/TaskImproveDescriptionResponse.md) | Interface | 246 | — | — |
| [GroundedFact](../entities/types_task_GroundedFact.md) | Interface | 251 | — | — |
| [TaskAISuggestRequest](../entities/types_task_TaskAISuggestRequest.md) | Interface | 256 | — | — |
| [GroundedAISuggestionResponse](../entities/types_task_GroundedAISuggestionResponse.md) | Interface | 281 | — | — |
| [TasksImportRequest](../entities/types_task_TasksImportRequest.md) | Interface | 301 | — | — |
| [TaskTextContext](../entities/types_task_TaskTextContext.md) | Interface | 307 | — | — |
| [TasksImportResponse](../entities/types_task_TasksImportResponse.md) | Interface | 313 | — | — |
| [TaskMergeRequest](../entities/TaskMergeRequest.md) | Interface | 321 | — | — |
| [TaskBulkOperationRequest](../entities/types_task_TaskBulkOperationRequest.md) | Interface | 345 | — | — |
| [TaskBulkOperationResult](../entities/types_task_TaskBulkOperationResult.md) | Interface | 354 | — | — |
| [TaskBulkOperationResponse](../entities/types_task_TaskBulkOperationResponse.md) | Interface | 365 | — | — |
| [CascadeUpdateInfo](../entities/types_task_CascadeUpdateInfo.md) | Interface | 375 | — | — |
| [TaskStatusChangeResponse](../entities/types_task_TaskStatusChangeResponse.md) | Interface | 384 | — | — |
| [TaskStatusLog](../entities/types_task_TaskStatusLog.md) | Interface | 390 | — | — |
| [TaskStatusStats](../entities/types_task_TaskStatusStats.md) | Interface | 402 | — | — |
| [TaskTimelineItem](../entities/types_task_TaskTimelineItem.md) | Interface | 408 | — | — |
| [TaskTimelineResponse](../entities/types_task_TaskTimelineResponse.md) | Interface | 419 | — | — |
| [TaskBatchUpdateItem](../entities/types_task_TaskBatchUpdateItem.md) | Interface | 424 | — | — |
| [TaskBatchUpdateRequest](../entities/types_task_TaskBatchUpdateRequest.md) | Interface | 431 | — | — |
| [TaskBatchUpdateResponseItem](../entities/types_task_TaskBatchUpdateResponseItem.md) | Interface | 437 | — | — |
| [TaskBatchUpdateResponse](../entities/types_task_TaskBatchUpdateResponse.md) | Interface | 443 | — | — |
| [BriefCriterion](../entities/types_task_BriefCriterion.md) | Interface | 449 | — | — |
| [TaskBrief](../entities/types_task_TaskBrief.md) | Interface | 456 | — | — |
| [RoutingRung](../entities/types_task_RoutingRung.md) | Interface | 470 | — | One model catalog entry that may execute a task or review its result. |
| [RoutingReviewer](../entities/types_task_RoutingReviewer.md) | Interface | 478 | `RoutingRung` | — |
| [TaskRouting](../entities/types_task_TaskRouting.md) | Interface | 483 | — | — |
| [RoutingIssue](../entities/types_task_RoutingIssue.md) | Interface | 496 | — | — |
| [RoutingCheck](../entities/types_task_RoutingCheck.md) | Interface | 506 | — | Whether a task's routing fits an assignee and the project's review policy, with a consistent replacement. |
| [CriterionProgress](../entities/types_task_CriterionProgress.md) | Interface | 524 | — | — |
| [TaskProgress](../entities/TaskProgress.md) | Interface | 531 | — | — |
| [TaskReference](../entities/types_task_TaskReference.md) | Interface | 538 | — | — |
| [TaskReferencePage](../entities/types_task_TaskReferencePage.md) | Interface | 545 | — | — |
| [TaskDetail](../entities/TaskDetail.md) | Interface | 546 | — | — |
| [ReactivationRequirementInput](../entities/types_task_ReactivationRequirementInput.md) | Interface | 554 | — | — |
| [ReactivationRequirement](../entities/ReactivationRequirement.md) | Interface | 557 | — | — |
| [TaskPostponementRecord](../entities/types_task_TaskPostponementRecord.md) | Interface | 561 | — | — |
| [TaskPostponementResponse](../entities/types_task_TaskPostponementResponse.md) | Interface | 567 | — | — |
| [TaskReviewRecord](../entities/types_task_TaskReviewRecord.md) | Interface | 569 | — | One recorded review. `owner_override` is an owner's acceptance that set aside publisher independence. |
| [RefusalNextStep](../entities/types_task_RefusalNextStep.md) | Interface | 574 | — | What a person or agent may do about a refusal, from the server's one refusal catalogue. |
| [TaskActionAvailability](../entities/types_task_TaskActionAvailability.md) | Interface | 579 | — | — |
| [ManualProvenanceExecutor](../entities/types_task_ManualProvenanceExecutor.md) | Interface | 581 | — | The executor of work that was delivered outside recorded runs. |
| [ManualProvenanceWrite](../entities/types_task_ManualProvenanceWrite.md) | Interface | 582 | — | — |
| [TaskActions](../entities/TaskActions.md) | Interface | 586 | — | — |
| [TaskCommand](../entities/TaskCommand.md) | Interface | 590 | — | — |
| [TaskStatus](../entities/types_task_TaskStatus.md) | Type alias | 51 | `'planned' \| 'active' \| 'resolved' \| 'postponed' \| 'closed'` | — |
| [TaskTerminalState](../entities/TaskTerminalState.md) | Type alias | 53 | `'canceled' \| 'superseded'` | Withdrawn work: canceled, or superseded when another task delivers its work (a clean replacement included). |
| [TaskDisplayedState](../entities/TaskDisplayedState.md) | Type alias | 55 | `TaskStatus \| TaskTerminalState` | What a task is shown as: its stored status, or its terminal state. |
| [ExternalLinkProvider](../entities/types_task_ExternalLinkProvider.md) | Type alias | 56 | `'github' \| 'gitlab' \| 'figma' \| 'sentry' \| 'custom' \| 'agdash' \| string` | — |
| [TaskImportDestination](../entities/types_task_TaskImportDestination.md) | Type alias | 299 | `'tasks' \| 'triage' \| 'auto'` | — |
| [TaskBulkAction](../entities/types_task_TaskBulkAction.md) | Type alias | 328 | <pre><code>&#124; &#39;set&#95;assignee&#39;&#10;    &#124; &#39;clear&#95;assignee&#39;&#10;    &#124; &#39;auto&#95;assign&#39;&#10;    &#124; &#39;set&#95;project&#39;&#10;    &#124; &#39;clear&#95;project&#39;&#10;    &#124; &#39;set&#95;milestone&#39;&#10;    &#124; &#39;clear&#95;milestone&#39;&#10;    &#124; &#39;set&#95;priority&#39;&#10;    &#124; &#39;add&#95;labels&#39;&#10;    &#124; &#39;remove&#95;labels&#39;&#10;    &#124; &#39;set&#95;flags&#39;&#10;    &#124; &#39;change&#95;status&#39;&#10;    &#124; &#39;delete&#39;</code></pre> | — |
| [TaskBulkOutcome](../entities/types_task_TaskBulkOutcome.md) | Type alias | 343 | `'updated' \| 'deleted' \| 'skipped' \| 'failed' \| 'would_update' \| 'would_delete'` | — |
| [TaskRoutingConflictMode](../entities/TaskRoutingConflictMode.md) | Type alias | 493 | `'refuse' \| 'warn'` | — |
| [TaskRoutingResolution](../entities/TaskRoutingResolution.md) | Type alias | 494 | `'check' \| 'apply_suggestion'` | — |
| [ReactivationRequirementKind](../entities/ReactivationRequirementKind.md) | Type alias | 553 | `'predecessor_accepted' \| 'date' \| 'owner_decision' \| 'linked_resolved'` | — |
