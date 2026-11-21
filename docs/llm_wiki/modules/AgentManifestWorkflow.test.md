# AgentManifestWorkflow.test Module

**Path:** `frontend/src/components/team/AgentManifestWorkflow.test.tsx`

## Description

_Auto-generated from `frontend/src/components/team/AgentManifestWorkflow.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../i18n/i18n` | `i18n`, `ensureLanguageResources` | — | compiler-dependent |
| `../../test/accessibilityInvariants` | `accessibleNameViolations`, `summaryNameViolations` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/agent` | `AgentTeamStatus` | Declaration | erased |
| `./AgentManifestWorkflow` | `AgentManifestWorkflow` | — | compiler-dependent |
| `@testing-library/react` | `act`, `fireEvent`, `screen`, `waitFor`, `within` | — | compiler-dependent |
| `@testing-library/user-event` | `userEvent` | — | compiler-dependent |
| `axios` | `AxiosError` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `agentServiceMock`, `useAdminAccessMock`, `statusFixture` |
| Module calls | `agentServiceMock = hoisted`, `useAdminAccessMock = hoisted`, `mock`, `mock`, `describe`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/team/AgentManifestWorkflow.test.tsx"]
    n1["frontend/src/components/team/AgentManifestWorkflow.tsx"]
    n2["frontend/src/i18n/i18n.ts"]
    n3["frontend/src/test/accessibilityInvariants.ts"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n5["frontend/src/types/agent.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n0 --> n5
    n1 --> n5
    n4 --> n2
    click n0 "../modules/AgentManifestWorkflow.test.md"
    click n1 "../modules/AgentManifestWorkflow.md"
    click n2 "../modules/i18n.md"
    click n3 "../modules/accessibilityInvariants.md"
    click n4 "../modules/renderWithProviders.md"
    click n5 "../modules/types_agent.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [AgentManifestWorkflow](../modules/AgentManifestWorkflow.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [accessibilityInvariants](../modules/accessibilityInvariants.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_agent](../modules/types_agent.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |
