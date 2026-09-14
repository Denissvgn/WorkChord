# AgentTeamApplyResponse

**Location:** `frontend/src/types/agent.ts:738`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentTeamApplyResponse` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `schema_version` | `'agent-team-apply-receipt-v1'` | *required* | — |
| `apply_id` | `string` | *required* | — |
| `topology_key` | `string` | *required* | — |
| `manifest_digest` | `string` | *required* | — |
| `plan_digest` | `string` | *required* | — |
| `expected_topology_revision` | `number` | *required* | — |
| `resulting_topology_revision` | `number` | *required* | — |
| `status` | `'completed' \| 'partial' \| 'blocked'` | *required* | — |
| `replayed` | `boolean` | *required* | — |
| `receipts` | `AgentTeamActionReceipt[]` | *required* | — |
| `pending_action_ids` | `string[]` | *required* | — |
| `blocker_codes` | `string[]` | *required* | — |

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
