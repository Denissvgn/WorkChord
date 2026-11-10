# masters.test Module

**Path:** `frontend/src/features/agentTeamSetup/masters.test.ts`

## Description

_Auto-generated from `frontend/src/features/agentTeamSetup/masters.test.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/agent` | `AgentTeamMaster`, `AgentTeamSetupStep` | Declaration | erased |
| `./manifest` | `parseAgentTeamMasterEditor` | — | compiler-dependent |
| `./masters` | `AGENT_TEAM_STEP_IDS`, `stateTone`, `stepProgress`, `stepsById` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `serverSteps` |
| Module calls | `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/features/agentTeamSetup/manifest.ts"]
    n1["frontend/src/features/agentTeamSetup/masters.test.ts"]
    n2["frontend/src/features/agentTeamSetup/masters.ts"]
    n3["frontend/src/types/agent.ts"]
    n0 --> n3
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n2 --> n3
    click n0 "../modules/agentTeamSetup_manifest.md"
    click n1 "../modules/agentTeamSetup_masters.test.md"
    click n2 "../modules/agentTeamSetup_masters.md"
    click n3 "../modules/types_agent.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [agentTeamSetup_manifest](../modules/agentTeamSetup_manifest.md) |
| Outbound | [agentTeamSetup_masters](../modules/agentTeamSetup_masters.md) |
| Outbound | [types_agent](../modules/types_agent.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |
