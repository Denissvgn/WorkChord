# AgentTeamMemberSpec

**Location:** `frontend/src/types/agent.ts:682`
**Kind:** Interface
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `AgentTeamMemberSpec` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `actor_key` | `string` | Yes | — | — |
| `actor_name` | `string` | Yes | — | — |
| `display_name` | `string` | Yes | — | — |
| `role` | `AgentTeamRole` | Yes | — | — |
| `scope_preset` | `'pm-v1' \| 'worker-v1' \| 'verifier-v1'` | Yes | — | — |
| `profile_key` | `string` | Yes | — | — |
| `skill_package` | `AgentTeamSkillPackage` | Yes | — | — |
| `assignment_modes` | `string[]` | Yes | — | — |
| `model_binding_keys` | `string[]` | Yes | — | — |
| `default_model_binding_key` | `string` | Yes | — | — |
| `runtime_ref` | `string` | Yes | — | — |
| `credential_ref` | `string` | Yes | — | — |
| `declared_tool_tags` | `Record<string, string[]>` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AgentTeamMemberSpec (frontend/src/types/agent.ts)"]
    n1["frontend/src/components/team/ConnectAgentSteps.test.tsx"]
    n2["frontend/src/components/team/ConnectAgentSteps.tsx"]
    n3["ConnectionSteps (frontend/src/components/team/ConnectionSteps.tsx)"]
    n4["frontend/src/components/team/TeamProfileManager.test.tsx"]
    n5["buildConnectedMember (frontend/src/features/agentTeamSetup/connectAgent.ts)"]
    n6["credentialFilename (frontend/src/features/agentTeamSetup/connectAgent.ts)"]
    n7["runtimeOfMember (frontend/src/features/agentTeamSetup/connectAgent.ts)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/types_agent.md"
    click n1 "../modules/ConnectAgentSteps.test.md"
    click n2 "../modules/ConnectAgentSteps.md"
    click n3 "../modules/ConnectionSteps.md"
    click n4 "../modules/TeamProfileManager.test.md"
    click n5 "../modules/connectAgent.md"
    click n6 "../modules/connectAgent.md"
    click n7 "../modules/connectAgent.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `actor_key`, `actor_name`, `assignment_modes`, `credential_ref`, `declared_tool_tags`, `default_model_binding_key`, `display_name`, `model_binding_keys`, `profile_key`, `role`, `runtime_ref`, `scope_preset` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `ConnectAgentSteps.test` | import | [ConnectAgentSteps.test](../modules/ConnectAgentSteps.test.md) | — |
| `ConnectAgentSteps` | import | [ConnectAgentSteps](../modules/ConnectAgentSteps.md) | — |
| `ConnectionSteps` | type_reference | [ConnectionSteps](../modules/ConnectionSteps.md) | — |
| `TeamProfileManager.test` | import | [TeamProfileManager.test](../modules/TeamProfileManager.test.md) | — |
| `buildConnectedMember` | type_reference | [connectAgent](../modules/connectAgent.md) | — |
| `credentialFilename` | type_reference | [connectAgent](../modules/connectAgent.md) | — |
| `runtimeOfMember` | type_reference | [connectAgent](../modules/connectAgent.md) | — |
