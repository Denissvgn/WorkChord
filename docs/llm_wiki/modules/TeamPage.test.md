# TeamPage.test Module

**Path:** `frontend/src/pages/TeamPage.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/TeamPage.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/team/directoryModel` | `CONNECTED_WINDOW_MS` | — | compiler-dependent |
| `../test/pageChrome` | `expectPageChrome` | — | compiler-dependent |
| `../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../types/agent` | `AgentActorRosterItem`, `AgentModelBinding` | Declaration | erased |
| `../types/team` | `TeamMemberProfile`, `TeamMemberProfileSkill` | Declaration | erased |
| `../utils/adminAccess` | `clearAdminApiKey`, `setAdminApiKey` | — | compiler-dependent |
| `./TeamPage` | `TeamPage` | — | compiler-dependent |
| `@testing-library/react` | `act`, `screen`, `waitFor`, `within` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `services`, `binding`, `PEOPLE` |
| Module calls | `services = hoisted`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/team/directoryModel.ts"]
    n1["frontend/src/pages/TeamPage.test.tsx"]
    n2["frontend/src/pages/TeamPage.tsx"]
    n3["frontend/src/test/pageChrome.ts"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n5["frontend/src/types/agent.ts"]
    n6["frontend/src/types/team.ts"]
    n7["frontend/src/utils/adminAccess.ts"]
    n0 --> n5
    n0 --> n6
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n1 --> n6
    n1 --> n7
    click n0 "../modules/directoryModel.md"
    click n1 "../modules/TeamPage.test.md"
    click n2 "../modules/TeamPage.md"
    click n3 "../modules/pageChrome.md"
    click n4 "../modules/renderWithProviders.md"
    click n5 "../modules/types_agent.md"
    click n6 "../modules/types_team.md"
    click n7 "../modules/adminAccess.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [directoryModel](../modules/directoryModel.md) |
| Outbound | [TeamPage](../modules/TeamPage.md) |
| Outbound | [pageChrome](../modules/pageChrome.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_agent](../modules/types_agent.md) |
| Outbound | [types_team](../modules/types_team.md) |
| Outbound | [adminAccess](../modules/adminAccess.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
