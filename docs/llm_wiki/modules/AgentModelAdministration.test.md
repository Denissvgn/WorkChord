# AgentModelAdministration.test Module

**Path:** `frontend/src/components/team/AgentModelAdministration.test.tsx`

## Description

_Auto-generated from `frontend/src/components/team/AgentModelAdministration.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../i18n/i18n` | `changeAppLanguage` | — | compiler-dependent |
| `../../pages/TeamPage` | `TeamPage` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/agent` | `AgentActor`, `AgentActorRosterItem`, `AgentCapabilities`, `AgentModelBinding`, `AgentModelCatalogEntry` | Declaration | erased |
| `./AgentModelAdministration` | `AgentModelAdministration` | — | compiler-dependent |
| `@testing-library/react` | `act`, `screen`, `waitFor`, `within` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `agentAccessMock`, `adminAccessMock`, `agentServiceMock` |
| Module calls | `agentAccessMock = hoisted`, `adminAccessMock = hoisted`, `agentServiceMock = hoisted`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/team/AgentModelAdministration.test.tsx"]
    n1["frontend/src/components/team/AgentModelAdministration.tsx"]
    n2["frontend/src/i18n/i18n.ts"]
    n3["frontend/src/pages/TeamPage.tsx"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n5["frontend/src/types/agent.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n0 --> n5
    n1 --> n5
    n3 --> n1
    n4 --> n2
    click n0 "../modules/AgentModelAdministration.test.md"
    click n1 "../modules/AgentModelAdministration.md"
    click n2 "../modules/i18n.md"
    click n3 "../modules/TeamPage.md"
    click n4 "../modules/renderWithProviders.md"
    click n5 "../modules/types_agent.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [AgentModelAdministration](../modules/AgentModelAdministration.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [TeamPage](../modules/TeamPage.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_agent](../modules/types_agent.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
