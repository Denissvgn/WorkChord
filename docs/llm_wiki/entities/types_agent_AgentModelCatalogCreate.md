# AgentModelCatalogCreate

**Location:** `frontend/src/types/agent.ts:211`
**Kind:** Interface
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentModelCatalogCreate` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `key` | `string` | Yes | — | — |
| `provider` | `string` | Yes | — | — |
| `configured_model_alias` | `string` | Yes | — | — |
| `reasoning_tier` | `ModelReasoningTier` | Yes | — | — |
| `effort` | `ModelEffort` | No | — | — |
| `context_tier` | `ModelContextTier` | Yes | — | — |
| `modality_tags` | `string[]` | No | — | — |
| `cost_tier` | `ModelCostTier` | Yes | — | — |
| `local_first` | `boolean` | No | — | — |
| `latency_tier` | `ModelLatencyTier` | Yes | — | — |
| `enabled` | `boolean` | No | — | — |
| `revision` | `1` | No | — | — |
| `last_verified_at` | `string \| null` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentModelCatalogCreate (frontend/src/types/agent.ts)"]
    n1["frontend/src/components/team/AgentModelAdministration.tsx"]
    n2["frontend/src/components/team/ConnectAgentSteps.tsx"]
    n3["frontend/src/services/agentService.test.ts"]
    n4["frontend/src/services/agentService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/AgentModelAdministration.md"
    click n2 "../modules/ConnectAgentSteps.md"
    click n3 "../modules/agentService.test.md"
    click n4 "../modules/agentService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `configured_model_alias`, `context_tier`, `cost_tier`, `effort`, `enabled`, `key`, `last_verified_at`, `latency_tier`, `local_first`, `modality_tags`, `provider`, `reasoning_tier` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AgentModelAdministration` | import | [AgentModelAdministration](../modules/AgentModelAdministration.md) | — |
| `ConnectAgentSteps` | import | [ConnectAgentSteps](../modules/ConnectAgentSteps.md) | — |
| `agentService.test` | import | [agentService.test](../modules/agentService.test.md) | — |
| `agentService` | import | [agentService](../modules/agentService.md) | — |
