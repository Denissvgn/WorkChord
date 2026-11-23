# AgentTeamStatus

**Location:** `frontend/src/types/agent.ts:835`
**Kind:** Interface
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

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTeamStatus (frontend/src/types/agent.ts)"]
    n1["frontend/src/components/team/AgentManifestWorkflow.test.tsx"]
    n2["frontend/src/components/team/ConnectAgentSteps.test.tsx"]
    n3["frontend/src/components/team/TeamProfileManager.test.tsx"]
    n4["buildConnectedMember (frontend/src/features/agentTeamSetup/connectAgent.ts)"]
    n5["hasPM (frontend/src/features/agentTeamSetup/connectAgent.ts)"]
    n6["replacesPendingPM (frontend/src/features/agentTeamSetup/connectAgent.ts)"]
    n7["waitingMembers (frontend/src/features/agentTeamSetup/connectAgent.ts)"]
    n8["frontend/src/features/agentTeamSetup/statusScopes.test.ts"]
    n9["deriveAgentTeamStatusScopes (frontend/src/features/agentTeamSetup/statusScopes.ts)"]
    n10["frontend/src/services/agentService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/AgentManifestWorkflow.test.md"
    click n2 "../modules/ConnectAgentSteps.test.md"
    click n3 "../modules/TeamProfileManager.test.md"
    click n4 "../modules/connectAgent.md"
    click n5 "../modules/connectAgent.md"
    click n6 "../modules/connectAgent.md"
    click n7 "../modules/connectAgent.md"
    click n8 "../modules/statusScopes.test.md"
    click n9 "../modules/statusScopes.md"
    click n10 "../modules/agentService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `availability`, `blocker_codes`, `can_mutate`, `manifest_digest`, `members`, `next_action`, `pending_action_ids`, `runtime_ready`, `schema_version`, `steps`, `topology_key`, `topology_revision` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AgentManifestWorkflow.test` | import | [AgentManifestWorkflow.test](../modules/AgentManifestWorkflow.test.md) | — |
| `ConnectAgentSteps.test` | import | [ConnectAgentSteps.test](../modules/ConnectAgentSteps.test.md) | — |
| `TeamProfileManager.test` | import | [TeamProfileManager.test](../modules/TeamProfileManager.test.md) | — |
| `buildConnectedMember` | type_reference | [connectAgent](../modules/connectAgent.md) | — |
| `hasPM` | type_reference | [connectAgent](../modules/connectAgent.md) | — |
| `replacesPendingPM` | type_reference | [connectAgent](../modules/connectAgent.md) | — |
| `waitingMembers` | type_reference | [connectAgent](../modules/connectAgent.md) | — |
| `statusScopes.test` | import | [statusScopes.test](../modules/statusScopes.test.md) | — |
| `deriveAgentTeamStatusScopes` | type_reference | [statusScopes](../modules/statusScopes.md) | — |
| `agentService` | import | [agentService](../modules/agentService.md) | — |
