# AgentModelCatalogCreate

**Location:** `frontend/src/types/agent.ts:205`
**Kind:** Class
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
| `context_tier` | `ModelContextTier` | Yes | — | — |
| `modality_tags` | `string[]` | No | — | — |
| `cost_tier` | `ModelCostTier` | Yes | — | — |
| `latency_tier` | `ModelLatencyTier` | Yes | — | — |
| `enabled` | `boolean` | No | — | — |
| `revision` | `1` | No | — | — |
| `last_verified_at` | `string \| null` | No | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentModelCatalogCreate (frontend/src/types/agent.ts)"]
    n1["frontend/src/components/settings/AgentModelAdministration.tsx"]
    n2["frontend/src/services/agentService.test.ts"]
    n3["frontend/src/services/agentService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/AgentModelAdministration.md"
    click n2 "../modules/agentService.test.md"
    click n3 "../modules/agentService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `configured_model_alias`, `context_tier`, `cost_tier`, `enabled`, `key`, `last_verified_at`, `latency_tier`, `modality_tags`, `provider`, `reasoning_tier`, `revision` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AgentModelAdministration` | import | [AgentModelAdministration](../modules/AgentModelAdministration.md) | — |
| `agentService.test` | import | [agentService.test](../modules/agentService.test.md) | — |
| `agentService` | import | [agentService](../modules/agentService.md) | — |
