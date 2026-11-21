# TeamPage.transport.test Module

**Path:** `frontend/src/pages/TeamPage.transport.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/TeamPage.transport.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../features/identity/IdentityProvider` | `IdentityProvider` | — | compiler-dependent |
| `../services/api` | `api`, `IDENTITY_EXPIRED_EVENT` | — | compiler-dependent |
| `../test/fixtures/modelAwareRouting` | `modelAwareRoutingRoster` | — | compiler-dependent |
| `../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../types/agent` | `AgentModelBinding`, `AgentModelCatalogEntry` | Declaration | erased |
| `../types/team` | `TeamMemberProfile` | Declaration | erased |
| `../utils/adminAccess` | `clearAdminApiKey`, `setAdminApiKey` | — | compiler-dependent |
| `../utils/agentAccess` | `clearAgentApiKey`, `setAgentApiKey` | — | compiler-dependent |
| `./TeamPage` | `TeamPage` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor`, `within` | — | compiler-dependent |
| `axios` | `AxiosAdapter`, `AxiosResponse`, `InternalAxiosRequestConfig` | Declaration | erased |
| `axios` | `AxiosError` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `services`, `originalAdapter`, `EXPIRED_TEXT`, `managedSession`, `agentProfile` |
| Module calls | `services = hoisted`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/features/identity/IdentityProvider.tsx"]
    n1["frontend/src/pages/TeamPage.transport.test.tsx"]
    n2["frontend/src/pages/TeamPage.tsx"]
    n3["frontend/src/services/api.ts"]
    n4["frontend/src/test/fixtures/modelAwareRouting.ts"]
    n5["frontend/src/test/renderWithProviders.tsx"]
    n6["frontend/src/types/agent.ts"]
    n7["frontend/src/types/team.ts"]
    n8["frontend/src/utils/adminAccess.ts"]
    n9["frontend/src/utils/agentAccess.ts"]
    n0 --> n3
    n0 --> n8
    n0 --> n9
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n1 --> n6
    n1 --> n7
    n1 --> n8
    n1 --> n9
    n3 --> n8
    n3 --> n9
    n4 --> n6
    click n0 "../modules/IdentityProvider.md"
    click n1 "../modules/TeamPage.transport.test.md"
    click n2 "../modules/TeamPage.md"
    click n3 "../modules/api.md"
    click n4 "../modules/modelAwareRouting.md"
    click n5 "../modules/renderWithProviders.md"
    click n6 "../modules/types_agent.md"
    click n7 "../modules/types_team.md"
    click n8 "../modules/adminAccess.md"
    click n9 "../modules/agentAccess.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [IdentityProvider](../modules/IdentityProvider.md) |
| Outbound | [TeamPage](../modules/TeamPage.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [modelAwareRouting](../modules/modelAwareRouting.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_agent](../modules/types_agent.md) |
| Outbound | [types_team](../modules/types_team.md) |
| Outbound | [adminAccess](../modules/adminAccess.md) |
| Outbound | [agentAccess](../modules/agentAccess.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
