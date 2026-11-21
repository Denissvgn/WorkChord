# TimeEntriesPanel.test Module

**Path:** `frontend/src/components/tasks/TimeEntriesPanel.test.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TimeEntriesPanel.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Button` | `Button` | — | compiler-dependent |
| `../../features/identity/identityContext` | `IdentityContext` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `./TimeEntriesPanel` | `TimeEntriesPanel` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor` | — | compiler-dependent |
| `vitest` | `beforeEach`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `service` |
| Module calls | `service = hoisted`, `mock`, `beforeEach`, `it`, `it`, `it`, `it`, `it`, `it.each([true, false])`, `it` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/tasks/TimeEntriesPanel.test.tsx"]
    n2["frontend/src/components/tasks/TimeEntriesPanel.tsx"]
    n3["frontend/src/features/identity/identityContext.ts"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n2 --> n0
    click n0 "../modules/Button.md"
    click n1 "../modules/TimeEntriesPanel.test.md"
    click n2 "../modules/TimeEntriesPanel.md"
    click n3 "../modules/identityContext.md"
    click n4 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [Button](../modules/Button.md) |
| Outbound | [TimeEntriesPanel](../modules/TimeEntriesPanel.md) |
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
