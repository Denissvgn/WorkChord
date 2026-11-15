# ConnectedReadersPanel.test Module

**Path:** `frontend/src/components/settings/ConnectedReadersPanel.test.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/ConnectedReadersPanel.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/identity/identityContext` | `IdentityContext` | — | compiler-dependent |
| `../../features/identity/identityService` | `WorkspaceIdentity` | Declaration | erased |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `./ConnectedReadersPanel` | `ConnectedReadersPanel` | — | compiler-dependent |
| `@testing-library/react` | `screen` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `service`, `person`, `later` |
| Module calls | `service = hoisted`, `mock`, `later = toISOString`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/settings/ConnectedReadersPanel.test.tsx"]
    n1["frontend/src/components/settings/ConnectedReadersPanel.tsx"]
    n2["frontend/src/features/identity/identityContext.ts"]
    n3["frontend/src/features/identity/identityService.ts"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n1 --> n2
    n1 --> n3
    n2 --> n3
    click n0 "../modules/ConnectedReadersPanel.test.md"
    click n1 "../modules/ConnectedReadersPanel.md"
    click n2 "../modules/identityContext.md"
    click n3 "../modules/identityService.md"
    click n4 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [ConnectedReadersPanel](../modules/ConnectedReadersPanel.md) |
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [identityService](../modules/identityService.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
