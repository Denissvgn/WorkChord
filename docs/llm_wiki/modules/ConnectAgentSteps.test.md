# ConnectAgentSteps.test Module

**Path:** `frontend/src/components/team/ConnectAgentSteps.test.tsx`

## Description

_Auto-generated from `frontend/src/components/team/ConnectAgentSteps.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/agentTeamSetup/connectAgent` | `hasPM`, `runtimeSnippet` | — | compiler-dependent |
| `../../features/agentTeamSetup/masters` | `AGENT_TEAM_STEP_DEFINITIONS` | — | compiler-dependent |
| `../../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../../services/agentService` | `agentService` | — | compiler-dependent |
| `../../services/teamService` | `teamService` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/agent` | `AgentModelCatalogEntry`, `AgentTeamMaster`, `AgentTeamMemberSpec`, `AgentTeamMemberStatus`, `AgentTeamPlan`, `AgentTeamStatus` | Declaration | erased |
| `../ui/SlideOverDrawer` | `SlideOverDrawer` | — | compiler-dependent |
| `./ConnectAgentSteps` | `ConnectAgentSteps` | — | compiler-dependent |
| `@testing-library/react` | `fireEvent`, `screen`, `waitFor`, `within` | — | compiler-dependent |
| `axios` | `AxiosError` | — | compiler-dependent |
| `node:crypto` | `createHash` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `service`, `teams`, `current`, `status`, `model` |
| Module calls | `mock`, `mock`, `mock`, `service = mocked`, `teams = mocked`, `beforeEach`, `afterEach`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/team/ConnectAgentSteps.test.tsx"]
    n1["frontend/src/components/team/ConnectAgentSteps.tsx"]
    n2["frontend/src/components/ui/SlideOverDrawer.tsx"]
    n3["frontend/src/features/agentTeamSetup/connectAgent.ts"]
    n4["frontend/src/features/agentTeamSetup/masters.ts"]
    n5["frontend/src/i18n/i18n.ts"]
    n6["frontend/src/services/agentService.ts"]
    n7["frontend/src/services/teamService.ts"]
    n8["frontend/src/test/renderWithProviders.tsx"]
    n9["frontend/src/types/agent.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n0 --> n5
    n0 --> n6
    n0 --> n7
    n0 --> n8
    n0 --> n9
    n1 --> n2
    n1 --> n3
    n1 --> n6
    n1 --> n7
    n1 --> n9
    n3 --> n9
    n4 --> n9
    n6 --> n9
    n8 --> n5
    click n0 "../modules/ConnectAgentSteps.test.md"
    click n1 "../modules/ConnectAgentSteps.md"
    click n2 "../modules/SlideOverDrawer.md"
    click n3 "../modules/connectAgent.md"
    click n4 "../modules/agentTeamSetup_masters.md"
    click n5 "../modules/i18n.md"
    click n6 "../modules/agentService.md"
    click n7 "../modules/teamService.md"
    click n8 "../modules/renderWithProviders.md"
    click n9 "../modules/types_agent.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [ConnectAgentSteps](../modules/ConnectAgentSteps.md) |
| Outbound | [SlideOverDrawer](../modules/SlideOverDrawer.md) |
| Outbound | [connectAgent](../modules/connectAgent.md) |
| Outbound | [agentTeamSetup_masters](../modules/agentTeamSetup_masters.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [agentService](../modules/agentService.md) |
| Outbound | [teamService](../modules/teamService.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_agent](../modules/types_agent.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
