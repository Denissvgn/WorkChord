# AgentModelBindingCreate

**Location:** `frontend/src/types/agent.ts:258`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentModelBindingCreate` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `actor_id` | `number` | Yes | — | — |
| `model_catalog_id` | `number` | Yes | — | — |
| `is_default` | `boolean` | No | — | — |
| `enabled` | `boolean` | No | — | — |
| `tool_tags` | `string[]` | No | — | — |
| `data_policy_tags` | `string[]` | No | — | — |
| `revision` | `1` | No | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentModelBindingCreate (frontend/src/types/agent.ts)"]
    n1["frontend/src/components/settings/AgentModelAdministration.tsx"]
    n2["frontend/src/services/agentService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/AgentModelAdministration.md"
    click n2 "../modules/agentService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `actor_id`, `data_policy_tags`, `enabled`, `is_default`, `model_catalog_id`, `revision`, `tool_tags` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AgentModelAdministration` | import | [AgentModelAdministration](../modules/AgentModelAdministration.md) | — |
| `agentService` | import | [agentService](../modules/agentService.md) | — |
