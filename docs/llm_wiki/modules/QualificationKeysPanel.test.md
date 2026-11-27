# QualificationKeysPanel.test Module

**Path:** `frontend/src/components/settings/QualificationKeysPanel.test.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/QualificationKeysPanel.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/agent` | `RoutingQualificationKey`, `RoutingQualificationKeyRegistry` | Declaration | erased |
| `./QualificationKeysPanel` | `QualificationKeysPanel` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor`, `within` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `agentServiceMock` |
| Module calls | `agentServiceMock = hoisted`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/settings/QualificationKeysPanel.test.tsx"]
    n1["frontend/src/components/settings/QualificationKeysPanel.tsx"]
    n2["frontend/src/test/renderWithProviders.tsx"]
    n3["frontend/src/types/agent.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n3
    click n0 "../modules/QualificationKeysPanel.test.md"
    click n1 "../modules/QualificationKeysPanel.md"
    click n2 "../modules/renderWithProviders.md"
    click n3 "../modules/types_agent.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [QualificationKeysPanel](../modules/QualificationKeysPanel.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_agent](../modules/types_agent.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
