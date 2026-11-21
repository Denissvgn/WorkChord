# masters Module

**Path:** `frontend/src/features/agentTeamSetup/masters.ts`

## Description

_Auto-generated from `frontend/src/features/agentTeamSetup/masters.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/agent` | `AgentTeamSetupStep`, `AgentTeamStepState` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AGENT_TEAM_STEP_DEFINITIONS`, `AgentTeamStepId`, `stateTone`, `stepProgress`, `stepsById` |
| Constants | `AGENT_TEAM_STEP_IDS`, `AGENT_TEAM_STEP_DEFINITIONS` |
| Module calls | `AGENT_TEAM_STEP_DEFINITIONS = map` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/settings/AgentTeamStepList.tsx"]
    n1["frontend/src/components/team/AgentManifestWorkflow.tsx"]
    n2["frontend/src/components/team/ConnectAgentSteps.test.tsx"]
    n3["frontend/src/features/agentTeamSetup/masters.test.ts"]
    n4["frontend/src/features/agentTeamSetup/masters.ts"]
    n5["frontend/src/features/agentTeamSetup/useAgentTeamReadiness.ts"]
    n6["frontend/src/types/agent.ts"]
    n0 --> n4
    n0 --> n5
    n1 --> n0
    n1 --> n4
    n1 --> n5
    n1 --> n6
    n2 --> n4
    n2 --> n6
    n3 --> n4
    n3 --> n6
    n4 --> n6
    n5 --> n4
    click n0 "../modules/AgentTeamStepList.md"
    click n1 "../modules/AgentManifestWorkflow.md"
    click n2 "../modules/ConnectAgentSteps.test.md"
    click n3 "../modules/agentTeamSetup_masters.test.md"
    click n4 "../modules/agentTeamSetup_masters.md"
    click n5 "../modules/useAgentTeamReadiness.md"
    click n6 "../modules/types_agent.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AgentTeamStepList](../modules/AgentTeamStepList.md) |
| Inbound | [AgentManifestWorkflow](../modules/AgentManifestWorkflow.md) |
| Inbound | [ConnectAgentSteps.test](../modules/ConnectAgentSteps.test.md) |
| Inbound | [agentTeamSetup_masters.test](../modules/agentTeamSetup_masters.test.md) |
| Inbound | [useAgentTeamReadiness](../modules/useAgentTeamReadiness.md) |
| Outbound | [types_agent](../modules/types_agent.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [AgentTeamStepDefinition](../entities/AgentTeamStepDefinition.md) | Interface | 15 | — | — |
| [AgentTeamStepId](../entities/AgentTeamStepId.md) | Type alias | 13 | `typeof AGENT_TEAM_STEP_IDS[number]` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `stepsById` | `(steps: AgentTeamSetupStep[] \| undefined) -> Record<AgentTeamStepId, AgentTeamSetupStep \| undefined>` | — | — |
| `stepProgress` | `(steps: AgentTeamSetupStep[] \| undefined) -> { done: number; total: number } \| null` | — | — |
| `stateTone` | `(state: AgentTeamStepState \| undefined) -> 'done' \| 'warn' \| 'blocked' \| 'todo'` | — | — |
