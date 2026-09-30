# AgentTeamApplyResponse

**Location:** `frontend/src/types/agent.ts:738`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentTeamApplyResponse` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `schema_version` | `'agent-team-apply-receipt-v1'` | Yes | — | — |
| `apply_id` | `string` | Yes | — | — |
| `topology_key` | `string` | Yes | — | — |
| `manifest_digest` | `string` | Yes | — | — |
| `plan_digest` | `string` | Yes | — | — |
| `expected_topology_revision` | `number` | Yes | — | — |
| `resulting_topology_revision` | `number` | Yes | — | — |
| `status` | `'completed' \| 'partial' \| 'blocked'` | Yes | — | — |
| `replayed` | `boolean` | Yes | — | — |
| `receipts` | `AgentTeamActionReceipt[]` | Yes | — | — |
| `pending_action_ids` | `string[]` | Yes | — | — |
| `blocker_codes` | `string[]` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTeamApplyResponse (frontend/src/types/agent.ts)"]
    n1["frontend/src/pages/AgentTeamSetupMasterPage.tsx"]
    n2["frontend/src/services/agentService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/AgentTeamSetupMasterPage.md"
    click n2 "../modules/agentService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `apply_id`, `blocker_codes`, `expected_topology_revision`, `manifest_digest`, `pending_action_ids`, `plan_digest`, `receipts`, `replayed`, `resulting_topology_revision`, `schema_version`, `status`, `topology_key` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AgentTeamSetupMasterPage` | import | [AgentTeamSetupMasterPage](../modules/AgentTeamSetupMasterPage.md) | — |
| `agentService` | import | [agentService](../modules/agentService.md) | — |
