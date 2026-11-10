# agent Module

**Path:** `frontend/src/types/agent.ts`

## Description

_Auto-generated from `frontend/src/types/agent.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./task` | `Task` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AgentActor`, `AgentActorRole`, `AgentActorRosterItem`, `AgentActorRosterProfile`, `AgentActorRosterProfileSkill`, `AgentAssignmentListParams`, `AgentAssignmentPurpose`, `AgentAssignmentQueueClass`, `AgentAssignmentState`, `AgentCapabilities`, `AgentCommandMetadata`, `AgentModelBinding`, `AgentModelBindingCreate`, `AgentModelBindingDisable`, `AgentModelBindingListParams`, `AgentModelBindingStatus`, `AgentModelBindingUpdate`, `AgentModelCatalogCreate`, `AgentModelCatalogDisable`, `AgentModelCatalogEntry`, `AgentModelCatalogUpdate`, `AgentModelMatchBasis`, `AgentModelMutationReceipt`, `AgentModelTrustState`, `AgentPipeline`, `AgentProfileSkillCatalogItem`, `AgentRoutingCandidate`, `AgentRoutingExclusion`, `AgentRoutingPreviewCreate`, `AgentRoutingPreviewResponse`, `AgentRun`, `AgentRunEvent`, `AgentTaskAssignment`, `AgentTeamActionReceipt`, `AgentTeamApplyResponse`, `AgentTeamLifecycle`, `AgentTeamMaster`, `AgentTeamMemberSpec`, `AgentTeamMemberStatus`, `AgentTeamPlan`, `AgentTeamPlanAction`, `AgentTeamReconciliationClass`, `AgentTeamRole`, `AgentTeamRuntimeHandoff`, `AgentTeamSetupStep`, `AgentTeamSkillPackage`, `AgentTeamStatus`, `AgentTeamStepState`, `AgentTeamValidation`, `AssessmentReasonCode`, `JsonObject`, `JsonPrimitive`, `JsonValue`, `ModelAwareAgentTaskAssignmentCreate`, `ModelAwareAgentTaskAssignmentUpdate`, `ModelAwareRoutingMode`, `ModelAwareRoutingStatus`, `ModelAwareRoutingTopologyReadiness`, `ModelAwareRoutingTopologySource`, `ModelAwareRoutingTopologyStatus`, `ModelContextTier`, `ModelCostTier`, `ModelLatencyTier`, `ModelReasoningTier`, `RequiredModelEnvelope`, `RoutingBlockerCode`, `TaskDifficultyAxes`, `TaskDifficultyBand`, `TaskDifficultyScore`, `TaskReviewMode`, `TaskRoutingAssessment`, `TaskRoutingAssessmentCommand`, `TaskRoutingAssessmentHistory`, `TaskRoutingAssessmentMutationReceipt`, `TaskRoutingAssessmentState`, `TaskSkillLevel`, `TaskTimelineItem`, `TaskTimelineResponse` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

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
| [AgentCommandMetadata](../entities/AgentCommandMetadata.md) | Interface | 94 | — | — |
| [AgentActor](../entities/types_agent_AgentActor.md) | Interface | 100 | — | — |
| [ModelAwareRoutingTopologyReadiness](../entities/ModelAwareRoutingTopologyReadiness.md) | Interface | 127 | — | — |
| [ModelAwareRoutingStatus](../entities/ModelAwareRoutingStatus.md) | Interface | 136 | — | — |
| [AgentCapabilities](../entities/AgentCapabilities.md) | Interface | 144 | — | — |
| [AgentProfileSkillCatalogItem](../entities/AgentProfileSkillCatalogItem.md) | Interface | 160 | — | — |
| [AgentActorRosterProfileSkill](../entities/types_agent_AgentActorRosterProfileSkill.md) | Interface | 167 | — | — |
| [AgentActorRosterProfile](../entities/types_agent_AgentActorRosterProfile.md) | Interface | 178 | — | — |
| [AgentModelCatalogEntry](../entities/types_agent_AgentModelCatalogEntry.md) | Interface | 189 | — | — |
| [AgentModelCatalogCreate](../entities/types_agent_AgentModelCatalogCreate.md) | Interface | 206 | — | — |
| [AgentModelCatalogUpdate](../entities/types_agent_AgentModelCatalogUpdate.md) | Interface | 220 | — | — |
| [AgentModelCatalogDisable](../entities/types_agent_AgentModelCatalogDisable.md) | Interface | 234 | — | — |
| [AgentModelBinding](../entities/types_agent_AgentModelBinding.md) | Interface | 239 | — | — |
| [AgentModelBindingCreate](../entities/types_agent_AgentModelBindingCreate.md) | Interface | 258 | — | — |
| [AgentModelBindingUpdate](../entities/types_agent_AgentModelBindingUpdate.md) | Interface | 268 | — | — |
| [AgentModelBindingDisable](../entities/types_agent_AgentModelBindingDisable.md) | Interface | 277 | — | — |
| [AgentModelMutationReceipt](../entities/types_agent_AgentModelMutationReceipt.md) | Interface | 282 | — | — |
| [AgentActorRosterItem](../entities/types_agent_AgentActorRosterItem.md) | Interface | 299 | `AgentActor` | — |
| [TaskDifficultyAxes](../entities/types_agent_TaskDifficultyAxes.md) | Interface | 309 | — | — |
| [RequiredModelEnvelope](../entities/types_agent_RequiredModelEnvelope.md) | Interface | 317 | — | — |
| [TaskRoutingAssessmentCommand](../entities/types_agent_TaskRoutingAssessmentCommand.md) | Interface | 325 | — | — |
| [TaskRoutingAssessment](../entities/types_agent_TaskRoutingAssessment.md) | Interface | 337 | — | — |
| [TaskRoutingAssessmentState](../entities/types_agent_TaskRoutingAssessmentState.md) | Interface | 357 | — | — |
| [TaskRoutingAssessmentHistory](../entities/TaskRoutingAssessmentHistory.md) | Interface | 364 | — | — |
| [TaskRoutingAssessmentMutationReceipt](../entities/types_agent_TaskRoutingAssessmentMutationReceipt.md) | Interface | 372 | — | — |
| [AgentRoutingPreviewCreate](../entities/types_agent_AgentRoutingPreviewCreate.md) | Interface | 386 | — | — |
| [AgentRoutingCandidate](../entities/types_agent_AgentRoutingCandidate.md) | Interface | 393 | — | — |
| [AgentRoutingExclusion](../entities/types_agent_AgentRoutingExclusion.md) | Interface | 434 | — | — |
| [AgentRoutingPreviewResponse](../entities/types_agent_AgentRoutingPreviewResponse.md) | Interface | 473 | — | — |
| [ModelAwareAgentTaskAssignmentCreate](../entities/types_agent_ModelAwareAgentTaskAssignmentCreate.md) | Interface | 500 | — | — |
| [ModelAwareAgentTaskAssignmentUpdate](../entities/types_agent_ModelAwareAgentTaskAssignmentUpdate.md) | Interface | 518 | — | — |
| [AgentTaskAssignment](../entities/types_agent_AgentTaskAssignment.md) | Interface | 533 | — | — |
| [AgentAssignmentListParams](../entities/AgentAssignmentListParams.md) | Interface | 556 | — | — |
| [AgentModelBindingListParams](../entities/AgentModelBindingListParams.md) | Interface | 564 | — | — |
| [AgentRunEvent](../entities/types_agent_AgentRunEvent.md) | Interface | 569 | — | — |
| [AgentRun](../entities/types_agent_AgentRun.md) | Interface | 582 | — | — |
| [AgentPipeline](../entities/AgentPipeline.md) | Interface | 610 | — | — |
| [TaskTimelineItem](../entities/types_agent_TaskTimelineItem.md) | Interface | 621 | — | — |
| [TaskTimelineResponse](../entities/types_agent_TaskTimelineResponse.md) | Interface | 631 | — | — |
| [AgentTeamSkillPackage](../entities/types_agent_AgentTeamSkillPackage.md) | Interface | 647 | — | — |
| [AgentTeamMemberSpec](../entities/types_agent_AgentTeamMemberSpec.md) | Interface | 653 | — | — |
| [AgentTeamMaster](../entities/types_agent_AgentTeamMaster.md) | Interface | 668 | — | — |
| [AgentTeamValidation](../entities/AgentTeamValidation.md) | Interface | 684 | — | — |
| [AgentTeamPlanAction](../entities/types_agent_AgentTeamPlanAction.md) | Interface | 701 | — | — |
| [AgentTeamPlan](../entities/AgentTeamPlan.md) | Interface | 718 | — | — |
| [AgentTeamActionReceipt](../entities/types_agent_AgentTeamActionReceipt.md) | Interface | 728 | — | — |
| [AgentTeamApplyResponse](../entities/types_agent_AgentTeamApplyResponse.md) | Interface | 742 | — | — |
| [AgentTeamRuntimeHandoff](../entities/types_agent_AgentTeamRuntimeHandoff.md) | Interface | 757 | — | — |
| [AgentTeamMemberStatus](../entities/types_agent_AgentTeamMemberStatus.md) | Interface | 776 | — | — |
| [AgentTeamSetupStep](../entities/types_agent_AgentTeamSetupStep.md) | Interface | 805 | — | — |
| [AgentTeamStatus](../entities/AgentTeamStatus.md) | Interface | 812 | — | — |
| [JsonPrimitive](../entities/JsonPrimitive.md) | Type alias | 3 | `string \| number \| boolean \| null` | — |
| [JsonValue](../entities/JsonValue.md) | Type alias | 4 | `JsonPrimitive \| JsonValue[] \| { [key: string]: JsonValue }` | — |
| [JsonObject](../entities/JsonObject.md) | Type alias | 5 | `{ [key: string]: JsonValue }` | — |
| [AgentActorRole](../entities/AgentActorRole.md) | Type alias | 7 | `'pm' \| 'worker' \| 'verifier'` | — |
| [AgentAssignmentPurpose](../entities/types_agent_AgentAssignmentPurpose.md) | Type alias | 8 | `'execution' \| 'verification'` | — |
| [AgentAssignmentQueueClass](../entities/types_agent_AgentAssignmentQueueClass.md) | Type alias | 9 | `'normal' \| 'rework' \| 'recovery'` | — |
| [AgentAssignmentState](../entities/types_agent_AgentAssignmentState.md) | Type alias | 10 | `'queued' \| 'accepted' \| 'fulfilled' \| 'cancelled'` | — |
| [AgentModelBindingStatus](../entities/AgentModelBindingStatus.md) | Type alias | 11 | `'not_selected' \| 'current' \| 'stale' \| 'unresolved'` | — |
| [AgentModelTrustState](../entities/AgentModelTrustState.md) | Type alias | 12 | `'matched' \| 'mismatch' \| 'unreported' \| 'unverifiable'` | — |
| [AgentModelMatchBasis](../entities/AgentModelMatchBasis.md) | Type alias | 13 | `'configured_alias' \| 'catalog_key'` | — |
| [ModelReasoningTier](../entities/ModelReasoningTier.md) | Type alias | 15 | `1 \| 2 \| 3` | — |
| [ModelContextTier](../entities/ModelContextTier.md) | Type alias | 16 | `'small' \| 'medium' \| 'large'` | — |
| [ModelCostTier](../entities/ModelCostTier.md) | Type alias | 17 | `'low' \| 'medium' \| 'high'` | — |
| [ModelLatencyTier](../entities/ModelLatencyTier.md) | Type alias | 18 | `'fast' \| 'balanced' \| 'slow'` | — |
| [TaskDifficultyScore](../entities/TaskDifficultyScore.md) | Type alias | 19 | `1 \| 2 \| 3` | — |
| [TaskSkillLevel](../entities/TaskSkillLevel.md) | Type alias | 20 | `1 \| 2 \| 3 \| 4 \| 5` | — |
| [TaskDifficultyBand](../entities/TaskDifficultyBand.md) | Type alias | 21 | `'routine' \| 'standard' \| 'advanced'` | — |
| [TaskReviewMode](../entities/TaskReviewMode.md) | Type alias | 22 | `'none' \| 'standard' \| 'independent' \| 'specialist-independent'` | — |
| [AssessmentReasonCode](../entities/types_agent_AssessmentReasonCode.md) | Type alias | 24 | <pre><code>&#124; &#39;novel&#45;architecture&#39;&#10;    &#124; &#39;material&#45;ambiguity&#39;&#10;    &#124; &#39;broad&#45;context&#39;&#10;    &#124; &#39;security&#39;&#10;    &#124; &#39;authorization&#39;&#10;    &#124; &#39;migration&#39;&#10;    &#124; &#39;data&#45;integrity&#39;&#10;    &#124; &#39;concurrency&#39;&#10;    &#124; &#39;production&#39;&#10;    &#124; &#39;irreversible&#45;change&#39;&#10;    &#124; &#39;independent&#45;verification&#39;&#10;    &#124; &#39;specialist&#45;verification&#39;</code></pre> | — |
| [RoutingBlockerCode](../entities/types_agent_RoutingBlockerCode.md) | Type alias | 38 | <pre><code>&#124; &#39;assignment&#95;purpose&#95;queue&#95;class&#95;incompatible&#39;&#10;    &#124; &#39;assessment&#95;missing&#39;&#10;    &#124; &#39;assessment&#95;stale&#39;&#10;    &#124; &#39;assessment&#95;policy&#95;mismatch&#39;&#10;    &#124; &#39;assessment&#95;low&#95;confidence&#39;&#10;    &#124; &#39;task&#95;definition&#95;not&#95;ready&#39;&#10;    &#124; &#39;task&#95;status&#95;incompatible&#39;&#10;    &#124; &#39;task&#95;deferred&#39;&#10;    &#124; &#39;task&#95;composite&#39;&#10;    &#124; &#39;task&#95;dependency&#95;unresolved&#39;&#10;    &#124; &#39;actor&#95;disabled&#39;&#10;    &#124; &#39;actor&#95;role&#95;incompatible&#39;&#10;    &#124; &#39;actor&#95;scope&#95;missing&#39;&#10;    &#124; &#39;actor&#95;policy&#95;incompatible&#39;&#10;    &#124; &#39;actor&#95;topology&#95;incompatible&#39;&#10;    &#124; &#39;actor&#95;profile&#95;missing&#39;&#10;    &#124; &#39;capacity&#95;owner&#95;missing&#39;&#10;    &#124; &#39;capacity&#95;owner&#95;profile&#95;missing&#39;&#10;    &#124; &#39;actor&#95;capacity&#95;profile&#95;mismatch&#39;&#10;    &#124; &#39;profile&#95;kind&#95;human&#39;&#10;    &#124; &#39;profile&#95;kind&#95;unsupported&#39;&#10;    &#124; &#39;profile&#95;automation&#95;disabled&#39;&#10;    &#124; &#39;profile&#95;assignment&#95;mode&#95;missing&#39;&#10;    &#124; &#39;required&#95;skill&#95;missing&#39;&#10;    &#124; &#39;required&#95;skill&#95;level&#95;insufficient&#39;&#10;    &#124; &#39;required&#95;skill&#95;blocking&#95;weakness&#39;&#10;    &#124; &#39;model&#95;binding&#95;missing&#39;&#10;    &#124; &#39;model&#95;binding&#95;disabled&#39;&#10;    &#124; &#39;model&#95;binding&#95;stale&#39;&#10;    &#124; &#39;model&#95;catalog&#95;missing&#39;&#10;    &#124; &#39;model&#95;catalog&#95;disabled&#39;&#10;    &#124; &#39;model&#95;reasoning&#95;tier&#95;insufficient&#39;&#10;    &#124; &#39;model&#95;context&#95;tier&#95;insufficient&#39;&#10;    &#124; &#39;model&#95;modality&#95;missing&#39;&#10;    &#124; &#39;model&#95;tool&#95;missing&#39;&#10;    &#124; &#39;model&#95;data&#95;policy&#95;missing&#39;&#10;    &#124; &#39;capacity&#95;unavailable&#39;&#10;    &#124; &#39;workload&#95;limit&#95;exceeded&#39;&#10;    &#124; &#39;vacation&#95;conflict&#39;&#10;    &#124; &#39;schedule&#95;missing&#39;&#10;    &#124; &#39;schedule&#95;conflict&#39;&#10;    &#124; &#39;queue&#95;limit&#95;exceeded&#39;&#10;    &#124; &#39;current&#95;work&#95;conflict&#39;&#10;    &#124; &#39;reviewer&#95;profile&#95;missing&#39;&#10;    &#124; &#39;reviewer&#95;profile&#95;mismatch&#39;&#10;    &#124; &#39;verification&#95;actor&#95;not&#95;independent&#39;&#10;    &#124; &#39;verification&#95;profile&#95;not&#95;independent&#39;&#10;    &#124; &#39;verification&#95;independence&#95;unverifiable&#39;&#10;    &#124; &#39;verification&#95;specialist&#95;skill&#95;missing&#39;&#10;    &#124; &#39;preview&#95;not&#95;found&#39;&#10;    &#124; &#39;preview&#95;stale&#39;&#10;    &#124; &#39;preview&#95;expired&#39;&#10;    &#124; &#39;preview&#95;digest&#95;mismatch&#39;&#10;    &#124; &#39;no&#95;eligible&#95;candidate&#39;</code></pre> | — |
| [ModelAwareRoutingMode](../entities/ModelAwareRoutingMode.md) | Type alias | 116 | `'off' \| 'shadow' \| 'enforced'` | — |
| [ModelAwareRoutingTopologyStatus](../entities/ModelAwareRoutingTopologyStatus.md) | Type alias | 118 | <pre><code>&#124; &#39;unavailable&#39;&#10;    &#124; &#39;not&#95;ready&#39;&#10;    &#124; &#39;ready&#39;</code></pre> | — |
| [ModelAwareRoutingTopologySource](../entities/ModelAwareRoutingTopologySource.md) | Type alias | 123 | <pre><code>&#124; &#39;unavailable&#39;&#10;    &#124; &#39;agent&#45;team&#45;master&#45;v1&#39;</code></pre> | — |
| [AgentTeamRole](../entities/AgentTeamRole.md) | Type alias | 636 | `'pm' \| 'worker' \| 'verifier'` | — |
| [AgentTeamStepState](../entities/AgentTeamStepState.md) | Type alias | 637 | `'done' \| 'warn' \| 'blocked' \| 'todo'` | — |
| [AgentTeamLifecycle](../entities/AgentTeamLifecycle.md) | Type alias | 638 | <pre><code>&#124; &#39;desired&#39;&#10;    &#124; &#39;configured&#39;&#10;    &#124; &#39;credential&#95;delivered&#39;&#10;    &#124; &#39;onboarding&#39;&#10;    &#124; &#39;connected&#39;&#10;    &#124; &#39;runtime&#95;ready&#39;&#10;    &#124; &#39;disabled&#39;</code></pre> | — |
| [AgentTeamReconciliationClass](../entities/types_agent_AgentTeamReconciliationClass.md) | Type alias | 692 | <pre><code>&#124; &#39;create&#39;&#10;    &#124; &#39;safe&#95;update&#39;&#10;    &#124; &#39;no&#95;change&#39;&#10;    &#124; &#39;blocked&#95;conflict&#39;&#10;    &#124; &#39;requires&#95;replacement&#39;&#10;    &#124; &#39;propose&#95;disable&#39;&#10;    &#124; &#39;unmanaged&#39;</code></pre> | — |
