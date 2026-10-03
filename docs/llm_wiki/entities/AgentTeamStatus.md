# AgentTeamStatus

**Location:** `frontend/src/types/agent.ts:812`
**Kind:** Class
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentTeamStatus` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `schema_version` | `'agent-team-status-v1'` | Yes | — | — |
| `topology_key` | `string \| null` | Yes | — | — |
| `topology_revision` | `number \| null` | Yes | — | — |
| `manifest_digest` | `string \| null` | Yes | — | — |
| `topology_state` | `'absent' \| 'configured' \| 'onboarding' \| 'runtime_ready' \| 'blocked' \| 'disabled'` | Yes | — | — |
| `runtime_ready` | `boolean` | Yes | — | — |
| `availability` | `'availability_unknown'` | Yes | — | — |
| `blocker_codes` | `string[]` | Yes | — | — |
| `steps` | `AgentTeamSetupStep[]` | Yes | — | — |
| `members` | `AgentTeamMemberStatus[]` | Yes | — | — |
| `pending_action_ids` | `string[]` | Yes | — | — |
| `can_mutate` | `boolean` | Yes | — | — |
| `next_action` | `string \| null` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTeamStatus (frontend/src/types/agent.ts)"]
    n1["frontend/src/features/agentTeamSetup/statusScopes.test.ts"]
    n2["deriveAgentTeamStatusScopes (frontend/src/features/agentTeamSetup/statusScopes.ts)"]
    n3["frontend/src/pages/AgentTeamSetupMasterPage.test.tsx"]
    n4["frontend/src/services/agentService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/statusScopes.test.md"
    click n2 "../modules/statusScopes.md"
    click n3 "../modules/AgentTeamSetupMasterPage.test.md"
    click n4 "../modules/agentService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `availability`, `blocker_codes`, `can_mutate`, `manifest_digest`, `members`, `next_action`, `pending_action_ids`, `runtime_ready`, `schema_version`, `steps`, `topology_key`, `topology_revision` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `statusScopes.test` | import | [statusScopes.test](../modules/statusScopes.test.md) | — |
| `deriveAgentTeamStatusScopes` | type_reference | [statusScopes](../modules/statusScopes.md) | — |
| `AgentTeamSetupMasterPage.test` | import | [AgentTeamSetupMasterPage.test](../modules/AgentTeamSetupMasterPage.test.md) | — |
| `agentService` | import | [agentService](../modules/agentService.md) | — |
