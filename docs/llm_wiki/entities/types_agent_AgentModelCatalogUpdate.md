# AgentModelCatalogUpdate

**Location:** `frontend/src/types/agent.ts:220`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentModelCatalogUpdate` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `expected_revision` | `number` | Yes | — | — |
| `provider` | `string` | No | — | — |
| `configured_model_alias` | `string` | No | — | — |
| `reasoning_tier` | `ModelReasoningTier` | No | — | — |
| `context_tier` | `ModelContextTier` | No | — | — |
| `modality_tags` | `string[]` | No | — | — |
| `cost_tier` | `ModelCostTier` | No | — | — |
| `latency_tier` | `ModelLatencyTier` | No | — | — |
| `enabled` | `true` | No | — | — |
| `last_verified_at` | `string \| null` | No | — | — |
| `reconcile_live_assignments` | `boolean` | No | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentModelCatalogUpdate (frontend/src/types/agent.ts)"]
    n1["frontend/src/services/agentService.ts"]
    n1 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/agentService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `configured_model_alias`, `context_tier`, `cost_tier`, `enabled`, `expected_revision`, `last_verified_at`, `latency_tier`, `modality_tags`, `provider`, `reasoning_tier`, `reconcile_live_assignments` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `agentService` | import | [agentService](../modules/agentService.md) | — |
