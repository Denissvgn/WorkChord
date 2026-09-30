# useAgentTeamReadiness Module

**Path:** `frontend/src/features/agentTeamSetup/useAgentTeamReadiness.ts`

## Description

_Auto-generated from `frontend/src/features/agentTeamSetup/useAgentTeamReadiness.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/agentService` | `agentService` |
| `./masters` | `stepProgress`, `stepsById` |
| `@tanstack/react-query` | `useQuery` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `useAgentTeamReadiness` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/features/agentTeamSetup/masters.ts"]
    n1["frontend/src/features/agentTeamSetup/useAgentTeamReadiness.ts"]
    n2["frontend/src/pages/AgentTeamSetupMasterPage.tsx"]
    n3["frontend/src/services/agentService.ts"]
    n1 --> n0
    n1 --> n3
    n2 --> n0
    n2 --> n1
    n2 --> n3
    click n0 "../modules/agentTeamSetup_masters.md"
    click n1 "../modules/useAgentTeamReadiness.md"
    click n2 "../modules/AgentTeamSetupMasterPage.md"
    click n3 "../modules/agentService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AgentTeamSetupMasterPage](../modules/AgentTeamSetupMasterPage.md) |
| Outbound | [agentTeamSetup_masters](../modules/agentTeamSetup_masters.md) |
| Outbound | [agentService](../modules/agentService.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useAgentTeamReadiness` | `(topologyKey: string)` | — | — |
