# manifest Module

**Path:** `frontend/src/features/agentTeamSetup/manifest.ts`

## Description

_Auto-generated from `frontend/src/features/agentTeamSetup/manifest.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/agent` | `AgentTeamMaster` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `assertAgentTeamMasterSecretFree`, `parseAgentTeamMasterEditor` |
| Constants | `SECRET_FIELDS`, `SECRET_VALUE_PATTERNS` |
| Module calls | `SECRET_FIELDS = Set` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/team/AgentManifestWorkflow.tsx"]
    n1["frontend/src/components/team/ConnectAgentSteps.tsx"]
    n2["frontend/src/features/agentTeamSetup/connectAgent.ts"]
    n3["frontend/src/features/agentTeamSetup/manifest.ts"]
    n4["frontend/src/features/agentTeamSetup/masters.test.ts"]
    n5["frontend/src/types/agent.ts"]
    n0 --> n3
    n0 --> n5
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n5
    n2 --> n3
    n2 --> n5
    n3 --> n5
    n4 --> n3
    n4 --> n5
    click n0 "../modules/AgentManifestWorkflow.md"
    click n1 "../modules/ConnectAgentSteps.md"
    click n2 "../modules/connectAgent.md"
    click n3 "../modules/agentTeamSetup_manifest.md"
    click n4 "../modules/agentTeamSetup_masters.test.md"
    click n5 "../modules/types_agent.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AgentManifestWorkflow](../modules/AgentManifestWorkflow.md) |
| Inbound | [ConnectAgentSteps](../modules/ConnectAgentSteps.md) |
| Inbound | [connectAgent](../modules/connectAgent.md) |
| Inbound | [agentTeamSetup_masters.test](../modules/agentTeamSetup_masters.test.md) |
| Outbound | [types_agent](../modules/types_agent.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `assertAgentTeamMasterSecretFree` | `(value: unknown, path = '$') -> void` | — | — |
| `parseAgentTeamMasterEditor` | `(text: string) -> AgentTeamMaster` | — | — |
