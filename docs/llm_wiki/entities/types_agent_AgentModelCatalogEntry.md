# AgentModelCatalogEntry

**Location:** `frontend/src/types/agent.ts:189`
**Kind:** Interface
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentModelCatalogEntry` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `key` | `string` | Yes | — | — |
| `provider` | `string` | Yes | — | — |
| `configured_model_alias` | `string` | Yes | — | — |
| `reasoning_tier` | `ModelReasoningTier` | Yes | — | — |
| `context_tier` | `ModelContextTier` | Yes | — | — |
| `modality_tags` | `string[]` | Yes | — | — |
| `cost_tier` | `ModelCostTier` | Yes | — | — |
| `local_first` | `boolean` | Yes | — | — |
| `latency_tier` | `ModelLatencyTier` | Yes | — | — |
| `enabled` | `boolean` | Yes | — | — |
| `revision` | `number` | Yes | — | — |
| `last_verified_at` | `string \| null` | Yes | — | — |
| `created_at` | `string` | Yes | — | — |
| `updated_at` | `string` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentModelCatalogEntry (frontend/src/types/agent.ts)"]
    n1["frontend/src/components/agent/TaskRoutingPanel.test.tsx"]
    n2["frontend/src/components/team/AgentModelAdministration.test.tsx"]
    n3["frontend/src/components/team/AgentModelAdministration.tsx"]
    n4["frontend/src/components/team/ConnectAgentSteps.test.tsx"]
    n5["ModelBindings (frontend/src/components/team/ModelBindings.tsx)"]
    n6["ModelCatalog (frontend/src/components/team/ModelCatalog.tsx)"]
    n7["frontend/src/pages/TeamPage.transport.test.tsx"]
    n8["frontend/src/services/agentService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/TaskRoutingPanel.test.md"
    click n2 "../modules/AgentModelAdministration.test.md"
    click n3 "../modules/AgentModelAdministration.md"
    click n4 "../modules/ConnectAgentSteps.test.md"
    click n5 "../modules/ModelBindings.md"
    click n6 "../modules/ModelCatalog.md"
    click n7 "../modules/TeamPage.transport.test.md"
    click n8 "../modules/agentService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `configured_model_alias`, `context_tier`, `cost_tier`, `created_at`, `enabled`, `id`, `key`, `last_verified_at`, `latency_tier`, `local_first`, `modality_tags`, `provider` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskRoutingPanel.test` | import | [TaskRoutingPanel.test](../modules/TaskRoutingPanel.test.md) | — |
| `AgentModelAdministration.test` | import | [AgentModelAdministration.test](../modules/AgentModelAdministration.test.md) | — |
| `AgentModelAdministration` | import | [AgentModelAdministration](../modules/AgentModelAdministration.md) | — |
| `ConnectAgentSteps.test` | import | [ConnectAgentSteps.test](../modules/ConnectAgentSteps.test.md) | — |
| `ModelBindings` | type_reference | [ModelBindings](../modules/ModelBindings.md) | — |
| `ModelCatalog` | type_reference | [ModelCatalog](../modules/ModelCatalog.md) | — |
| `TeamPage.transport.test` | import | [TeamPage.transport.test](../modules/TeamPage.transport.test.md) | — |
| `agentService` | import | [agentService](../modules/agentService.md) | — |
