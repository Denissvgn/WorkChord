# manifest Module

**Path:** `frontend/src/features/agentTeamSetup/manifest.ts`

## Description

_Auto-generated from `frontend/src/features/agentTeamSetup/manifest.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../types/agent` | `AgentTeamMaster` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `assertAgentTeamMasterSecretFree`, `parseAgentTeamMasterEditor` |
| Constants | `SECRET_FIELDS`, `SECRET_VALUE_PATTERNS` |
| Module calls | `SECRET_FIELDS = Set` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/features/agentTeamSetup/manifest.ts"]
    n1["frontend/src/features/agentTeamSetup/masters.test.ts"]
    n2["frontend/src/pages/AgentTeamSetupMasterPage.tsx"]
    n3["frontend/src/types/agent.ts"]
    n0 --> n3
    n1 --> n0
    n1 --> n3
    n2 --> n0
    n2 --> n3
    click n0 "../modules/agentTeamSetup_manifest.md"
    click n1 "../modules/agentTeamSetup_masters.test.md"
    click n2 "../modules/AgentTeamSetupMasterPage.md"
    click n3 "../modules/types_agent.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [agentTeamSetup_masters.test](../modules/agentTeamSetup_masters.test.md) |
| Inbound | [AgentTeamSetupMasterPage](../modules/AgentTeamSetupMasterPage.md) |
| Outbound | [types_agent](../modules/types_agent.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `assertAgentTeamMasterSecretFree` | `(value: unknown, path = '$') -> void` | — | — |
| `parseAgentTeamMasterEditor` | `(text: string) -> AgentTeamMaster` | — | — |
