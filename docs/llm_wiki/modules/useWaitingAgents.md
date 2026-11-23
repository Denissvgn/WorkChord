# useWaitingAgents Module

**Path:** `frontend/src/features/agentTeamSetup/useWaitingAgents.ts`

## Description

_Auto-generated from `frontend/src/features/agentTeamSetup/useWaitingAgents.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/agentService` | `agentService` | — | compiler-dependent |
| `./connectAgent` | `waitingMembers` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `useWaitingAgents` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/team/TeamProfileManager.tsx"]
    n1["frontend/src/features/agentTeamSetup/connectAgent.ts"]
    n2["frontend/src/features/agentTeamSetup/useWaitingAgents.ts"]
    n3["frontend/src/services/agentService.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n2 --> n1
    n2 --> n3
    click n0 "../modules/TeamProfileManager.md"
    click n1 "../modules/connectAgent.md"
    click n2 "../modules/useWaitingAgents.md"
    click n3 "../modules/agentService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TeamProfileManager](../modules/TeamProfileManager.md) |
| Outbound | [connectAgent](../modules/connectAgent.md) |
| Outbound | [agentService](../modules/agentService.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useWaitingAgents` | `(enabled: boolean)` | — | The team status and topology the Connect steps read, under the same query keys, so a drawer and the |
