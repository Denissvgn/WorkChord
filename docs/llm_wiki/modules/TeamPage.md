# TeamPage Module

**Path:** `frontend/src/pages/TeamPage.tsx`

## Description

The Team tabs share the current URL. Members opens the people and agent directory, Models manages catalog entries and actor bindings, and Connect guides the operator through team setup. The active tab supplies its own header action. Returning to Plan keeps the iteration context.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/common/Button` | `Button` | — | compiler-dependent |
| `../components/planning/PlanReturnBar` | `PlanReturnBar` | — | compiler-dependent |
| `../components/team/AgentModelAdministration` | `ModelHeaderActions` | Specifier | compiler-dependent |
| `../components/team/AgentModelAdministration` | `AgentModelAdministration` | — | compiler-dependent |
| `../components/team/ConnectAgentSteps` | `ConnectAgentSteps` | — | compiler-dependent |
| `../components/team/TeamDirectory` | `DrawerTarget` | Specifier | compiler-dependent |
| `../components/team/TeamDirectory` | `TeamDirectory` | — | compiler-dependent |
| `../components/ui` | `PageHeader`, `PageLayout` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `Plus` | — | compiler-dependent |
| `react` | `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link`, `useSearchParams` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |
| Constants | `TEAM_TABS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/planning/PlanReturnBar.tsx"]
    n2["frontend/src/components/team/AgentModelAdministration.test.tsx"]
    n3["frontend/src/components/team/AgentModelAdministration.tsx"]
    n4["frontend/src/components/team/ConnectAgentSteps.tsx"]
    n5["frontend/src/components/team/TeamDirectory.tsx"]
    n6["frontend/src/components/ui/index.ts"]
    n7["frontend/src/features/identity/IdentityProvider.keepRoute.test.tsx"]
    n8["frontend/src/pages/destinationEmptyStates.test.tsx"]
    n9["frontend/src/pages/TeamPage.test.tsx"]
    n10["frontend/src/pages/TeamPage.transport.test.tsx"]
    n11["frontend/src/pages/TeamPage.tsx"]
    n2 --> n3
    n2 --> n11
    n3 --> n0
    n3 --> n6
    n4 --> n0
    n5 --> n0
    n5 --> n6
    n7 --> n11
    n8 --> n11
    n9 --> n11
    n10 --> n11
    n11 --> n0
    n11 --> n1
    n11 --> n3
    n11 --> n4
    n11 --> n5
    n11 --> n6
    click n0 "../modules/Button.md"
    click n1 "../modules/PlanReturnBar.md"
    click n2 "../modules/AgentModelAdministration.test.md"
    click n3 "../modules/AgentModelAdministration.md"
    click n4 "../modules/ConnectAgentSteps.md"
    click n5 "../modules/TeamDirectory.md"
    click n6 "../modules/index.md"
    click n7 "../modules/IdentityProvider.keepRoute.test.md"
    click n8 "../modules/destinationEmptyStates.test.md"
    click n9 "../modules/TeamPage.test.md"
    click n10 "../modules/TeamPage.transport.test.md"
    click n11 "../modules/TeamPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AgentModelAdministration.test](../modules/AgentModelAdministration.test.md) |
| Inbound | [IdentityProvider.keepRoute.test](../modules/IdentityProvider.keepRoute.test.md) |
| Inbound | [destinationEmptyStates.test](../modules/destinationEmptyStates.test.md) |
| Inbound | [TeamPage.test](../modules/TeamPage.test.md) |
| Inbound | [TeamPage.transport.test](../modules/TeamPage.transport.test.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [PlanReturnBar](../modules/PlanReturnBar.md) |
| Outbound | [AgentModelAdministration](../modules/AgentModelAdministration.md) |
| Outbound | [ConnectAgentSteps](../modules/ConnectAgentSteps.md) |
| Outbound | [TeamDirectory](../modules/TeamDirectory.md) |
| Outbound | [index](../modules/index.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TeamTab](../entities/TeamTab.md) | Type alias | 14 | `(typeof TEAM_TABS)[number]` | — |
