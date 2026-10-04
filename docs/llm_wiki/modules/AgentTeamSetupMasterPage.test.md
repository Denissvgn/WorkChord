# AgentTeamSetupMasterPage.test Module

**Path:** `frontend/src/pages/AgentTeamSetupMasterPage.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/AgentTeamSetupMasterPage.test.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../i18n/i18n` | `i18n`, `ensureLanguageResources` |
| `../test/accessibilityInvariants` | `accessibleNameViolations`, `summaryNameViolations` |
| `../test/renderWithProviders` | `renderWithProviders` |
| `../types/agent` | `AgentTeamStatus` |
| `./AgentTeamSetupMasterPage` | `AgentTeamSetupMasterPage` |
| `@testing-library/react` | `act`, `fireEvent`, `screen`, `waitFor`, `within` |
| `@testing-library/user-event` | `userEvent` |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `agentServiceMock`, `useAdminAccessMock`, `statusFixture` |
| Module calls | `agentServiceMock = hoisted`, `useAdminAccessMock = hoisted`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/i18n/i18n.ts"]
    n1["frontend/src/pages/AgentTeamSetupMasterPage.test.tsx"]
    n2["frontend/src/pages/AgentTeamSetupMasterPage.tsx"]
    n3["frontend/src/test/accessibilityInvariants.ts"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n5["frontend/src/types/agent.ts"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n2 --> n5
    click n0 "../modules/i18n.md"
    click n1 "../modules/AgentTeamSetupMasterPage.test.md"
    click n2 "../modules/AgentTeamSetupMasterPage.md"
    click n3 "../modules/accessibilityInvariants.md"
    click n4 "../modules/renderWithProviders.md"
    click n5 "../modules/types_agent.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [AgentTeamSetupMasterPage](../modules/AgentTeamSetupMasterPage.md) |
| Outbound | [accessibilityInvariants](../modules/accessibilityInvariants.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_agent](../modules/types_agent.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
