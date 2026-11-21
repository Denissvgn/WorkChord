# directoryModel.test Module

**Path:** `frontend/src/components/team/directoryModel.test.ts`

## Description

_Auto-generated from `frontend/src/components/team/directoryModel.test.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/agent` | `AgentActorRosterItem`, `AgentModelBinding` | Declaration | erased |
| `../../types/team` | `TeamMemberProfile` | Declaration | erased |
| `./directoryModel` | `agentStatus`, `buildDirectory`, `statusKnown` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `NOW` |
| Module calls | `NOW = parse`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/team/directoryModel.test.ts"]
    n1["frontend/src/components/team/directoryModel.ts"]
    n2["frontend/src/types/agent.ts"]
    n3["frontend/src/types/team.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n2
    n1 --> n3
    click n0 "../modules/directoryModel.test.md"
    click n1 "../modules/directoryModel.md"
    click n2 "../modules/types_agent.md"
    click n3 "../modules/types_team.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [directoryModel](../modules/directoryModel.md) |
| Outbound | [types_agent](../modules/types_agent.md) |
| Outbound | [types_team](../modules/types_team.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |
