# agent Module

**Path:** `frontend/src/types/agent.ts`

## Description

_Auto-generated from `frontend/src/types/agent.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `./task` | `Task` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AgentActor`, `AgentActorRole`, `AgentActorRosterItem`, `AgentActorRosterProfile`, `AgentActorRosterProfileSkill`, `AgentAssignmentListParams`, `AgentAssignmentPurpose`, `AgentAssignmentQueueClass`, `AgentAssignmentState`, `AgentCapabilities`, `AgentCommandMetadata`, `AgentModelBinding`, `AgentModelBindingCreate`, `AgentModelBindingDisable`, `AgentModelBindingListParams`, `AgentModelBindingStatus`, `AgentModelBindingUpdate`, `AgentModelCatalogCreate`, `AgentModelCatalogDisable`, `AgentModelCatalogEntry`, `AgentModelCatalogUpdate`, `AgentModelMatchBasis`, `AgentModelMutationReceipt`, `AgentModelTrustState`, `AgentPipeline`, `AgentProfileSkillCatalogItem`, `AgentRoutingCandidate`, `AgentRoutingExclusion`, `AgentRoutingPreviewCreate`, `AgentRoutingPreviewResponse`, `AgentRun`, `AgentRunEvent`, `AgentTaskAssignment`, `AgentTeamActionReceipt`, `AgentTeamApplyResponse`, `AgentTeamLifecycle`, `AgentTeamMaster`, `AgentTeamMemberSpec`, `AgentTeamMemberStatus`, `AgentTeamPlan`, `AgentTeamPlanAction`, `AgentTeamReconciliationClass`, `AgentTeamRole`, `AgentTeamRuntimeHandoff`, `AgentTeamSetupStep`, `AgentTeamSkillPackage`, `AgentTeamStatus`, `AgentTeamStepState`, `AgentTeamValidation`, `AssessmentReasonCode`, `JsonObject`, `JsonPrimitive`, `JsonValue`, `ModelAwareAgentTaskAssignmentCreate`, `ModelAwareAgentTaskAssignmentUpdate`, `ModelAwareRoutingMode`, `ModelAwareRoutingStatus`, `ModelAwareRoutingTopologyReadiness`, `ModelAwareRoutingTopologySource`, `ModelAwareRoutingTopologyStatus`, `ModelContextTier`, `ModelCostTier`, `ModelLatencyTier`, `ModelReasoningTier`, `RequiredModelEnvelope`, `RoutingBlockerCode`, `TaskDifficultyAxes`, `TaskDifficultyBand`, `TaskDifficultyScore`, `TaskReviewMode`, `TaskRoutingAssessment`, `TaskRoutingAssessmentCommand`, `TaskRoutingAssessmentHistory`, `TaskRoutingAssessmentMutationReceipt`, `TaskRoutingAssessmentState`, `TaskSkillLevel`, `TaskTimelineItem`, `TaskTimelineResponse` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/types/agent.ts"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/types_agent.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (20) |
| Outbound | `frontend` (1) |

> All 21 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [AgentCommandMetadata](../entities/AgentCommandMetadata.md) | Class | 94 | — | — |
| [AgentActor](../entities/types_agent_AgentActor.md) | Class | 100 | — | — |
| [ModelAwareRoutingTopologyReadiness](../entities/ModelAwareRoutingTopologyReadiness.md) | Class | 127 | — | — |
| [ModelAwareRoutingStatus](../entities/ModelAwareRoutingStatus.md) | Class | 136 | — | — |
| [AgentCapabilities](../entities/AgentCapabilities.md) | Class | 144 | — | — |
| [AgentProfileSkillCatalogItem](../entities/AgentProfileSkillCatalogItem.md) | Class | 159 | — | — |
| [AgentActorRosterProfileSkill](../entities/types_agent_AgentActorRosterProfileSkill.md) | Class | 166 | — | — |
| [AgentActorRosterProfile](../entities/types_agent_AgentActorRosterProfile.md) | Class | 177 | — | — |
| [AgentModelCatalogEntry](../entities/types_agent_AgentModelCatalogEntry.md) | Class | 188 | — | — |
| [AgentModelCatalogCreate](../entities/types_agent_AgentModelCatalogCreate.md) | Class | 205 | — | — |
| [AgentModelCatalogUpdate](../entities/types_agent_AgentModelCatalogUpdate.md) | Class | 219 | — | — |
| [AgentModelCatalogDisable](../entities/types_agent_AgentModelCatalogDisable.md) | Class | 233 | — | — |
| [AgentModelBinding](../entities/types_agent_AgentModelBinding.md) | Class | 238 | — | — |
| [AgentModelBindingCreate](../entities/types_agent_AgentModelBindingCreate.md) | Class | 257 | — | — |
| [AgentModelBindingUpdate](../entities/types_agent_AgentModelBindingUpdate.md) | Class | 267 | — | — |
| [AgentModelBindingDisable](../entities/types_agent_AgentModelBindingDisable.md) | Class | 276 | — | — |
| [AgentModelMutationReceipt](../entities/types_agent_AgentModelMutationReceipt.md) | Class | 281 | — | — |
| [AgentActorRosterItem](../entities/types_agent_AgentActorRosterItem.md) | Class | 298 | `AgentActor` | — |
| [TaskDifficultyAxes](../entities/types_agent_TaskDifficultyAxes.md) | Class | 308 | — | — |
| [RequiredModelEnvelope](../entities/types_agent_RequiredModelEnvelope.md) | Class | 316 | — | — |
| [TaskRoutingAssessmentCommand](../entities/types_agent_TaskRoutingAssessmentCommand.md) | Class | 324 | — | — |
| [TaskRoutingAssessment](../entities/types_agent_TaskRoutingAssessment.md) | Class | 336 | — | — |
| [TaskRoutingAssessmentState](../entities/types_agent_TaskRoutingAssessmentState.md) | Class | 356 | — | — |
| [TaskRoutingAssessmentHistory](../entities/TaskRoutingAssessmentHistory.md) | Class | 363 | — | — |
| [TaskRoutingAssessmentMutationReceipt](../entities/types_agent_TaskRoutingAssessmentMutationReceipt.md) | Class | 371 | — | — |
| [AgentRoutingPreviewCreate](../entities/types_agent_AgentRoutingPreviewCreate.md) | Class | 385 | — | — |
| [AgentRoutingCandidate](../entities/types_agent_AgentRoutingCandidate.md) | Class | 392 | — | — |
| [AgentRoutingExclusion](../entities/types_agent_AgentRoutingExclusion.md) | Class | 433 | — | — |
| [AgentRoutingPreviewResponse](../entities/types_agent_AgentRoutingPreviewResponse.md) | Class | 472 | — | — |
| [ModelAwareAgentTaskAssignmentCreate](../entities/types_agent_ModelAwareAgentTaskAssignmentCreate.md) | Class | 496 | — | — |
| [ModelAwareAgentTaskAssignmentUpdate](../entities/types_agent_ModelAwareAgentTaskAssignmentUpdate.md) | Class | 514 | — | — |
| [AgentTaskAssignment](../entities/types_agent_AgentTaskAssignment.md) | Class | 529 | — | — |
| [AgentAssignmentListParams](../entities/AgentAssignmentListParams.md) | Class | 552 | — | — |
| [AgentModelBindingListParams](../entities/AgentModelBindingListParams.md) | Class | 560 | — | — |
| [AgentRunEvent](../entities/types_agent_AgentRunEvent.md) | Class | 565 | — | — |
| [AgentRun](../entities/types_agent_AgentRun.md) | Class | 578 | — | — |
| [AgentPipeline](../entities/AgentPipeline.md) | Class | 606 | — | — |
| [TaskTimelineItem](../entities/types_agent_TaskTimelineItem.md) | Class | 617 | — | — |
| [TaskTimelineResponse](../entities/types_agent_TaskTimelineResponse.md) | Class | 627 | — | — |
| [AgentTeamSkillPackage](../entities/types_agent_AgentTeamSkillPackage.md) | Class | 643 | — | — |
| [AgentTeamMemberSpec](../entities/types_agent_AgentTeamMemberSpec.md) | Class | 649 | — | — |
| [AgentTeamMaster](../entities/types_agent_AgentTeamMaster.md) | Class | 664 | — | — |
| [AgentTeamValidation](../entities/AgentTeamValidation.md) | Class | 680 | — | — |
| [AgentTeamPlanAction](../entities/types_agent_AgentTeamPlanAction.md) | Class | 697 | — | — |
| [AgentTeamPlan](../entities/AgentTeamPlan.md) | Class | 714 | — | — |
| [AgentTeamActionReceipt](../entities/types_agent_AgentTeamActionReceipt.md) | Class | 724 | — | — |
| [AgentTeamApplyResponse](../entities/types_agent_AgentTeamApplyResponse.md) | Class | 738 | — | — |
| [AgentTeamRuntimeHandoff](../entities/types_agent_AgentTeamRuntimeHandoff.md) | Class | 753 | — | — |
| [AgentTeamMemberStatus](../entities/types_agent_AgentTeamMemberStatus.md) | Class | 771 | — | — |
| [AgentTeamSetupStep](../entities/types_agent_AgentTeamSetupStep.md) | Class | 798 | — | — |
| [AgentTeamStatus](../entities/AgentTeamStatus.md) | Class | 805 | — | — |
| [JsonPrimitive](../entities/JsonPrimitive.md) | Type alias | 3 | — | — |
| [JsonValue](../entities/JsonValue.md) | Type alias | 4 | — | — |
| [JsonObject](../entities/JsonObject.md) | Type alias | 5 | — | — |
| [AgentActorRole](../entities/AgentActorRole.md) | Type alias | 7 | — | — |
| [AgentAssignmentPurpose](../entities/types_agent_AgentAssignmentPurpose.md) | Type alias | 8 | — | — |
| [AgentAssignmentQueueClass](../entities/types_agent_AgentAssignmentQueueClass.md) | Type alias | 9 | — | — |
| [AgentAssignmentState](../entities/types_agent_AgentAssignmentState.md) | Type alias | 10 | — | — |
| [AgentModelBindingStatus](../entities/AgentModelBindingStatus.md) | Type alias | 11 | — | — |
| [AgentModelTrustState](../entities/AgentModelTrustState.md) | Type alias | 12 | — | — |
| [AgentModelMatchBasis](../entities/AgentModelMatchBasis.md) | Type alias | 13 | — | — |
| [ModelReasoningTier](../entities/ModelReasoningTier.md) | Type alias | 15 | — | — |
| [ModelContextTier](../entities/ModelContextTier.md) | Type alias | 16 | — | — |
| [ModelCostTier](../entities/ModelCostTier.md) | Type alias | 17 | — | — |
| [ModelLatencyTier](../entities/ModelLatencyTier.md) | Type alias | 18 | — | — |
| [TaskDifficultyScore](../entities/TaskDifficultyScore.md) | Type alias | 19 | — | — |
| [TaskSkillLevel](../entities/TaskSkillLevel.md) | Type alias | 20 | — | — |
| [TaskDifficultyBand](../entities/TaskDifficultyBand.md) | Type alias | 21 | — | — |
| [TaskReviewMode](../entities/TaskReviewMode.md) | Type alias | 22 | — | — |
| [AssessmentReasonCode](../entities/types_agent_AssessmentReasonCode.md) | Type alias | 24 | — | — |
| [RoutingBlockerCode](../entities/types_agent_RoutingBlockerCode.md) | Type alias | 38 | — | — |
| [ModelAwareRoutingMode](../entities/ModelAwareRoutingMode.md) | Type alias | 116 | — | — |
| [ModelAwareRoutingTopologyStatus](../entities/ModelAwareRoutingTopologyStatus.md) | Type alias | 118 | — | — |
| [ModelAwareRoutingTopologySource](../entities/ModelAwareRoutingTopologySource.md) | Type alias | 123 | — | — |
| [AgentTeamRole](../entities/AgentTeamRole.md) | Type alias | 632 | — | — |
| [AgentTeamStepState](../entities/AgentTeamStepState.md) | Type alias | 633 | — | — |
| [AgentTeamLifecycle](../entities/AgentTeamLifecycle.md) | Type alias | 634 | — | — |
| [AgentTeamReconciliationClass](../entities/types_agent_AgentTeamReconciliationClass.md) | Type alias | 688 | — | — |
