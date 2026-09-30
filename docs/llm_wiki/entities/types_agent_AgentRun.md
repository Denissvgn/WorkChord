# AgentRun

**Location:** `frontend/src/types/agent.ts:578`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentRun` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `task_id` | `number \| null` | No | — | — |
| `actor_id` | `number` | Yes | — | — |
| `assignment_id` | `number \| null` | No | — | — |
| `claim_generation` | `number \| null` | No | — | — |
| `status` | `'running' \| 'succeeded' \| 'failed' \| 'canceled' \| string` | Yes | — | — |
| `trace_id` | `string \| null` | No | — | — |
| `model_binding_id` | `number \| null` | No | — | — |
| `model_binding_revision` | `number \| null` | No | — | — |
| `configured_model_alias` | `string \| null` | No | — | — |
| `resolved_model_id` | `string \| null` | No | — | — |
| `model_trust_state` | `AgentModelTrustState` | Yes | — | — |
| `model_match_basis` | `AgentModelMatchBasis \| null` | No | — | — |
| `model` | `string \| null` | No | — | — |
| `tool_name` | `string \| null` | No | — | — |
| `metadata` | `JsonObject` | Yes | — | — |
| `artifact_links` | `string[]` | Yes | — | — |
| `commit_url` | `string \| null` | No | — | — |
| `pr_url` | `string \| null` | No | — | — |
| `summary` | `string \| null` | No | — | — |
| `error` | `string \| null` | No | — | — |
| `started_at` | `string` | Yes | — | — |
| `ended_at` | `string \| null` | No | — | — |
| `heartbeat_at` | `string \| null` | No | — | — |
| `events` | `AgentRunEvent[]` | No | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentRun (frontend/src/types/agent.ts)"]
    n1["frontend/src/pages/AgentPipelinePage.test.tsx"]
    n2["frontend/src/services/agentService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/AgentPipelinePage.test.md"
    click n2 "../modules/agentService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `actor_id`, `artifact_links`, `assignment_id`, `claim_generation`, `commit_url`, `configured_model_alias`, `ended_at`, `error`, `events`, `heartbeat_at`, `id`, `metadata` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AgentPipelinePage.test` | import | [AgentPipelinePage.test](../modules/AgentPipelinePage.test.md) | — |
| `agentService` | import | [agentService](../modules/agentService.md) | — |
