# AgentModelBinding

**Location:** `frontend/src/types/agent.ts:238`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentModelBinding` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `number` | *required* | — |
| `actor_id` | `number` | *required* | — |
| `model_catalog_id` | `number` | *required* | — |
| `is_default` | `boolean` | *required* | — |
| `enabled` | `boolean` | *required* | — |
| `tool_tags` | `string[]` | *required* | — |
| `data_policy_tags` | `string[]` | *required* | — |
| `revision` | `number` | *required* | — |
| `model_catalog_key` | `string \| null` | *required* | — |
| `selectable` | `boolean` | *required* | — |
| `model_catalog` | `AgentModelCatalogEntry \| null` | *required* | — |
| `live_assignment_count` | `number` | *required* | — |
| `historical_assignment_count` | `number` | *required* | — |
| `run_reference_count` | `number` | *required* | — |
| `created_at` | `string` | *required* | — |
| `updated_at` | `string` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentModelBinding (frontend/src/types/agent.ts)"]
    n1["frontend/src/components/agent/TaskRoutingPanel.test.tsx"]
    n2["frontend/src/components/settings/AgentModelAdministration.test.tsx"]
    n3["frontend/src/components/settings/AgentModelAdministration.tsx"]
    n4["frontend/src/services/agentService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/TaskRoutingPanel.test.md"
    click n2 "../modules/AgentModelAdministration.test.md"
    click n3 "../modules/AgentModelAdministration.md"
    click n4 "../modules/agentService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `actor_id`, `created_at`, `data_policy_tags`, `enabled`, `historical_assignment_count`, `id`, `is_default`, `live_assignment_count`, `model_catalog`, `model_catalog_id`, `model_catalog_key`, `revision` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskRoutingPanel.test` | import | [TaskRoutingPanel.test](../modules/TaskRoutingPanel.test.md) | — |
| `AgentModelAdministration.test` | import | [AgentModelAdministration.test](../modules/AgentModelAdministration.test.md) | — |
| `AgentModelAdministration` | import | [AgentModelAdministration](../modules/AgentModelAdministration.md) | — |
| `agentService` | import | [agentService](../modules/agentService.md) | — |
