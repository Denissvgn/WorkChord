# agentService Module

**Path:** `frontend/src/services/agentService.ts`

## Description

_Auto-generated from `frontend/src/services/agentService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/agent` | `AgentActorRosterItem`, `AgentAssignmentListParams`, `AgentCapabilities`, `AgentCommandMetadata`, `AgentModelBinding`, `AgentModelBindingCreate`, `AgentModelBindingDisable`, `AgentModelBindingListParams`, `AgentModelBindingUpdate`, `AgentModelCatalogCreate`, `AgentModelCatalogDisable`, `AgentModelCatalogEntry`, `AgentModelCatalogUpdate`, `AgentModelMutationReceipt`, `AgentPipeline`, `AgentProfileSkillCatalogItem`, `AgentRoutingPreviewCreate`, `AgentRoutingPreviewResponse`, `AgentRun`, `AgentTaskAssignment`, `AgentTeamApplyResponse`, `AgentTeamMaster`, `AgentTeamPlan`, `AgentTeamStatus`, `AgentTeamValidation`, `ModelAwareAgentTaskAssignmentCreate`, `ModelAwareAgentTaskAssignmentUpdate`, `TaskRoutingAssessmentCommand`, `TaskRoutingAssessmentHistory`, `TaskRoutingAssessmentMutationReceipt`, `TaskRoutingAssessmentState`, `TaskTimelineResponse` |
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `agentService` |
| Constants | `agentService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/agent/TaskRoutingPanel.tsx"]
    n1["frontend/src/components/settings/AgentAccessPanel.tsx"]
    n2["frontend/src/components/settings/AgentModelAdministration.tsx"]
    n3["frontend/src/features/agentTeamSetup/useAgentTeamReadiness.ts"]
    n4["frontend/src/pages/AgentPipelinePage.tsx"]
    n5["frontend/src/pages/AgentTeamSetupMasterPage.tsx"]
    n6["frontend/src/services/agentService.test.ts"]
    n7["frontend/src/services/agentService.ts"]
    n8["frontend/src/services/api.ts"]
    n9["frontend/src/types/agent.ts"]
    n0 --> n7
    n0 --> n9
    n1 --> n7
    n2 --> n7
    n2 --> n9
    n3 --> n7
    n4 --> n0
    n4 --> n7
    n4 --> n9
    n5 --> n3
    n5 --> n7
    n5 --> n9
    n6 --> n7
    n6 --> n8
    n6 --> n9
    n7 --> n8
    n7 --> n9
    click n0 "../modules/TaskRoutingPanel.md"
    click n1 "../modules/AgentAccessPanel.md"
    click n2 "../modules/AgentModelAdministration.md"
    click n3 "../modules/useAgentTeamReadiness.md"
    click n4 "../modules/AgentPipelinePage.md"
    click n5 "../modules/AgentTeamSetupMasterPage.md"
    click n6 "../modules/agentService.test.md"
    click n7 "../modules/agentService.md"
    click n8 "../modules/api.md"
    click n9 "../modules/types_agent.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskRoutingPanel](../modules/TaskRoutingPanel.md) |
| Inbound | [AgentAccessPanel](../modules/AgentAccessPanel.md) |
| Inbound | [AgentModelAdministration](../modules/AgentModelAdministration.md) |
| Inbound | [useAgentTeamReadiness](../modules/useAgentTeamReadiness.md) |
| Inbound | [AgentPipelinePage](../modules/AgentPipelinePage.md) |
| Inbound | [AgentTeamSetupMasterPage](../modules/AgentTeamSetupMasterPage.md) |
| Inbound | [agentService.test](../modules/agentService.test.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [types_agent](../modules/types_agent.md) |
