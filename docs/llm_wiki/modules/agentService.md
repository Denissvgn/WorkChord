# agentService Module

**Path:** `frontend/src/services/agentService.ts`

## Description

_Auto-generated from `frontend/src/services/agentService.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../types/agent` | `AgentActorRosterItem`, `AgentAssignmentListParams`, `AgentAssignmentReadItem`, `AgentCapabilities`, `AgentCommandMetadata`, `AgentModelBinding`, `AgentModelBindingCreate`, `AgentModelBindingDisable`, `AgentModelBindingListParams`, `AgentModelBindingUpdate`, `AgentModelCatalogCreate`, `AgentModelCatalogDisable`, `AgentModelCatalogEntry`, `AgentModelCatalogUpdate`, `AgentModelMutationReceipt`, `AgentPipeline`, `AgentProfileSkillCatalogItem`, `AgentRoutingPreviewCreate`, `AgentRoutingPreviewResponse`, `AgentRun`, `AgentTaskAssignment`, `AgentTeamApplyResponse`, `AgentTeamMaster`, `AgentTeamPlan`, `AgentTeamStatus`, `AgentTeamValidation`, `ModelAwareAgentTaskAssignmentCreate`, `ModelAwareAgentTaskAssignmentUpdate`, `TaskRoutingAssessmentCommand`, `TaskRoutingAssessmentHistory`, `TaskRoutingAssessmentMutationReceipt`, `TaskRoutingAssessmentState`, `TaskTimelineResponse` | Declaration | erased |
| `./api` | `api` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `agentService` |
| Constants | `agentService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/agent/AssignedAgentsSummary.tsx"]
    n1["frontend/src/components/agent/TaskRoutingPanel.tsx"]
    n2["frontend/src/components/settings/AgentAccessPanel.tsx"]
    n3["frontend/src/components/settings/AgentModelAdministration.tsx"]
    n4["frontend/src/features/agentTeamSetup/useAgentTeamReadiness.ts"]
    n5["frontend/src/pages/AgentPipelinePage.tsx"]
    n6["frontend/src/pages/AgentTeamSetupMasterPage.tsx"]
    n7["frontend/src/services/agentService.test.ts"]
    n8["frontend/src/services/agentService.ts"]
    n9["frontend/src/services/api.ts"]
    n10["frontend/src/types/agent.ts"]
    n0 --> n8
    n0 --> n10
    n1 --> n0
    n1 --> n8
    n1 --> n10
    n2 --> n8
    n3 --> n8
    n3 --> n10
    n4 --> n8
    n5 --> n1
    n5 --> n8
    n5 --> n10
    n6 --> n4
    n6 --> n8
    n6 --> n10
    n7 --> n8
    n7 --> n9
    n7 --> n10
    n8 --> n9
    n8 --> n10
    click n0 "../modules/AssignedAgentsSummary.md"
    click n1 "../modules/TaskRoutingPanel.md"
    click n2 "../modules/AgentAccessPanel.md"
    click n3 "../modules/AgentModelAdministration.md"
    click n4 "../modules/useAgentTeamReadiness.md"
    click n5 "../modules/AgentPipelinePage.md"
    click n6 "../modules/AgentTeamSetupMasterPage.md"
    click n7 "../modules/agentService.test.md"
    click n8 "../modules/agentService.md"
    click n9 "../modules/api.md"
    click n10 "../modules/types_agent.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AssignedAgentsSummary](../modules/AssignedAgentsSummary.md) |
| Inbound | [TaskRoutingPanel](../modules/TaskRoutingPanel.md) |
| Inbound | [AgentAccessPanel](../modules/AgentAccessPanel.md) |
| Inbound | [AgentModelAdministration](../modules/AgentModelAdministration.md) |
| Inbound | [useAgentTeamReadiness](../modules/useAgentTeamReadiness.md) |
| Inbound | [AgentPipelinePage](../modules/AgentPipelinePage.md) |
| Inbound | [AgentTeamSetupMasterPage](../modules/AgentTeamSetupMasterPage.md) |
| Inbound | [agentService.test](../modules/agentService.test.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [types_agent](../modules/types_agent.md) |
