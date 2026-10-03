# TaskRoutingAssessmentMutationReceipt

**Location:** `frontend/src/types/agent.ts:372`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `TaskRoutingAssessmentMutationReceipt` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `operation` | `'routing.assessment.create'` | Yes | — | — |
| `actor_id` | `number` | Yes | — | — |
| `target_type` | `'task_routing_assessment'` | Yes | — | — |
| `target_id` | `number` | Yes | — | — |
| `task_id` | `number` | Yes | — | — |
| `idempotency_key` | `string` | Yes | — | — |
| `rationale` | `string` | Yes | — | — |
| `correlation_id` | `string` | Yes | — | — |
| `authoritative_task_version` | `number` | Yes | — | — |
| `assessment` | `TaskRoutingAssessment` | Yes | — | — |
| `audit_event_ids` | `number[]` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskRoutingAssessmentMutationReceipt (frontend/src/types/agent.ts)"]
    n1["frontend/src/services/agentService.ts"]
    n1 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/agentService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `actor_id`, `assessment`, `audit_event_ids`, `authoritative_task_version`, `correlation_id`, `idempotency_key`, `operation`, `rationale`, `target_id`, `target_type`, `task_id` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `agentService` | import | [agentService](../modules/agentService.md) | — |
