# AgentTaskAssignment

**Location:** `frontend/src/types/agent.ts:529`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentTaskAssignment` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `number` | *required* | — |
| `task_id` | `number` | *required* | — |
| `actor_id` | `number` | *required* | — |
| `team_member_id` | `number \| null` | *required* | — |
| `purpose` | `AgentAssignmentPurpose \| string` | *required* | — |
| `queue_class` | `AgentAssignmentQueueClass \| string` | *required* | — |
| `state` | `AgentAssignmentState \| string` | *required* | — |
| `queue_rank` | `number` | *required* | — |
| `not_before` | `string \| null` | *required* | — |
| `assigned_by_actor_id` | `number \| null` | *required* | — |
| `reviewer_profile_id` | `number \| null` | *required* | — |
| `task_version` | `number` | *required* | — |
| `model_binding_id` | `number \| null` | *required* | — |
| `model_binding_revision` | `number \| null` | *required* | — |
| `model_binding_status` | `AgentModelBindingStatus` | *required* | — |
| `model_binding_stale_reasons` | `string[]` | *required* | — |
| `routing_snapshot` | `JsonObject` | *required* | — |
| `reason` | `string \| null` | *required* | — |
| `created_at` | `string` | *required* | — |
| `updated_at` | `string` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTaskAssignment (frontend/src/types/agent.ts)"]
    n1["frontend/src/components/agent/TaskRoutingPanel.test.tsx"]
    n2["frontend/src/components/agent/TaskRoutingPanel.tsx"]
    n3["frontend/src/services/agentService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/TaskRoutingPanel.test.md"
    click n2 "../modules/TaskRoutingPanel.md"
    click n3 "../modules/agentService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `actor_id`, `assigned_by_actor_id`, `created_at`, `id`, `model_binding_id`, `model_binding_revision`, `model_binding_stale_reasons`, `model_binding_status`, `not_before`, `purpose`, `queue_class`, `queue_rank` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskRoutingPanel.test` | import | [TaskRoutingPanel.test](../modules/TaskRoutingPanel.test.md) | — |
| `TaskRoutingPanel` | import | [TaskRoutingPanel](../modules/TaskRoutingPanel.md) | — |
| `agentService` | import | [agentService](../modules/agentService.md) | — |
