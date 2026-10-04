# ModelAwareAgentTaskAssignmentCreate

**Location:** `frontend/src/types/agent.ts:500`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `ModelAwareAgentTaskAssignmentCreate` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `task_id` | `number` | Yes | — | — |
| `actor_id` | `number` | Yes | — | — |
| `expected_task_version` | `number` | Yes | — | — |
| `purpose` | `AgentAssignmentPurpose` | Yes | — | — |
| `assessment_id` | `number` | Yes | — | — |
| `model_binding_id` | `number` | Yes | — | — |
| `model_binding_revision` | `number` | Yes | — | — |
| `routing_preview_id` | `string` | Yes | — | — |
| `routing_preview_digest` | `string` | Yes | — | — |
| `team_member_id` | `number \| null` | No | — | — |
| `reviewer_profile_id` | `number \| null` | No | — | — |
| `queue_class` | `AgentAssignmentQueueClass` | No | — | — |
| `queue_rank` | `number` | No | — | — |
| `not_before` | `string \| null` | No | — | — |
| `reason` | `string \| null` | No | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ModelAwareAgentTaskAssignmentCreate (frontend/src/types/agent.ts)"]
    n1["frontend/src/services/agentService.test.ts"]
    n2["frontend/src/services/agentService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/agentService.test.md"
    click n2 "../modules/agentService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `actor_id`, `assessment_id`, `expected_task_version`, `model_binding_id`, `model_binding_revision`, `not_before`, `purpose`, `queue_class`, `queue_rank`, `reason`, `reviewer_profile_id`, `routing_preview_digest` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `agentService.test` | import | [agentService.test](../modules/agentService.test.md) | — |
| `agentService` | import | [agentService](../modules/agentService.md) | — |
