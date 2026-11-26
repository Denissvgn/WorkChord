# AgentActorRosterItem

**Location:** `frontend/src/types/agent.ts:303`
**Kind:** Interface
**Bases:** `AgentActor`
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentActorRosterItem` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `actor_revision` | `number` | Yes | — | — |
| `profile_revision` | `string \| null` | Yes | — | — |
| `profile` | `AgentActorRosterProfile \| null` | Yes | — | — |
| `eligible_model_bindings` | `AgentModelBinding[]` | Yes | — | — |
| `queued_assignments` | `number` | Yes | — | — |
| `accepted_assignments` | `number` | Yes | — | — |
| `running_runs` | `number` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentActorRosterItem (frontend/src/types/agent.ts)"]
    n1["AgentActor (frontend/src/types/agent.ts)"]
    n2["frontend/src/components/agent/RoutingCandidateComparison.tsx"]
    n3["frontend/src/components/agent/TaskRoutingPanel.test.tsx"]
    n4["frontend/src/components/team/AgentModelAdministration.test.tsx"]
    n5["frontend/src/components/team/directoryModel.test.ts"]
    n6["actorName (frontend/src/components/team/directoryModel.ts)"]
    n7["agentStatus (frontend/src/components/team/directoryModel.ts)"]
    n8["buildDirectory (frontend/src/components/team/directoryModel.ts)"]
    n9["frontend/src/components/team/TeamProfileManager.test.tsx"]
    n10["frontend/src/components/team/TeamProfileManager.tsx"]
    n11["frontend/src/pages/TeamPage.test.tsx"]
    n12["frontend/src/services/agentService.ts"]
    n13["frontend/src/test/fixtures/modelAwareRouting.ts"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    n12 --> n0
    n13 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/types_agent.md"
    click n2 "../modules/RoutingCandidateComparison.md"
    click n3 "../modules/TaskRoutingPanel.test.md"
    click n4 "../modules/AgentModelAdministration.test.md"
    click n5 "../modules/directoryModel.test.md"
    click n6 "../modules/directoryModel.md"
    click n7 "../modules/directoryModel.md"
    click n8 "../modules/directoryModel.md"
    click n9 "../modules/TeamProfileManager.test.md"
    click n10 "../modules/TeamProfileManager.md"
    click n11 "../modules/TeamPage.test.md"
    click n12 "../modules/agentService.md"
    click n13 "../modules/modelAwareRouting.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `accepted_assignments`, `actor_revision`, `eligible_model_bindings`, `profile`, `profile_revision`, `queued_assignments`, `running_runs` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `AgentActor` | [types_agent](../modules/types_agent.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `RoutingCandidateComparison` | import | [RoutingCandidateComparison](../modules/RoutingCandidateComparison.md) | — |
| `TaskRoutingPanel.test` | import | [TaskRoutingPanel.test](../modules/TaskRoutingPanel.test.md) | — |
| `AgentModelAdministration.test` | import | [AgentModelAdministration.test](../modules/AgentModelAdministration.test.md) | — |
| `directoryModel.test` | import | [directoryModel.test](../modules/directoryModel.test.md) | — |
| `actorName` | type_reference | [directoryModel](../modules/directoryModel.md) | — |
| `agentStatus` | type_reference | [directoryModel](../modules/directoryModel.md) | — |
| `buildDirectory` | type_reference | [directoryModel](../modules/directoryModel.md) | — |
| `TeamProfileManager.test` | import | [TeamProfileManager.test](../modules/TeamProfileManager.test.md) | — |
| `TeamProfileManager` | import | [TeamProfileManager](../modules/TeamProfileManager.md) | — |
| `TeamPage.test` | import | [TeamPage.test](../modules/TeamPage.test.md) | — |
| `agentService` | import | [agentService](../modules/agentService.md) | — |
| `modelAwareRouting` | import | [modelAwareRouting](../modules/modelAwareRouting.md) | — |
