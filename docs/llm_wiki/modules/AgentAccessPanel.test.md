# AgentAccessPanel.test Module

**Path:** `frontend/src/components/settings/AgentAccessPanel.test.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/AgentAccessPanel.test.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../test/renderWithProviders` | `createTestQueryClient`, `renderWithProviders` |
| `../../types/agent` | `AgentCapabilities` |
| `./AgentAccessPanel` | `AgentAccessPanel` |
| `@testing-library/react` | `act`, `screen`, `waitFor` |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `agentAccessHookMock`, `agentAccessStorageMock`, `agentServiceMock`, `PRINCIPAL_QUERY_PREFIXES` |
| Module calls | `agentAccessHookMock = hoisted`, `agentAccessStorageMock = hoisted`, `agentServiceMock = hoisted`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/AgentAccessPanel.test.tsx"]
    n1["frontend/src/components/settings/AgentAccessPanel.tsx"]
    n2["frontend/src/test/renderWithProviders.tsx"]
    n3["frontend/src/types/agent.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    click n0 "../modules/AgentAccessPanel.test.md"
    click n1 "../modules/AgentAccessPanel.md"
    click n2 "../modules/renderWithProviders.md"
    click n3 "../modules/types_agent.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [AgentAccessPanel](../modules/AgentAccessPanel.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_agent](../modules/types_agent.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
