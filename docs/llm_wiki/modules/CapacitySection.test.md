# CapacitySection.test Module

**Path:** `frontend/src/components/capacity/CapacitySection.test.tsx`

## Description

_Auto-generated from `frontend/src/components/capacity/CapacitySection.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/identity/identityContext` | `IdentityContext` | — | compiler-dependent |
| `../../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/iteration` | `Iteration` | Declaration | erased |
| `../../types/team` | `TeamMember` | Declaration | erased |
| `./CapacitySection` | `CapacitySection` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor` | — | compiler-dependent |
| `react` | `ReactElement` | Declaration | erased |
| `react-router-dom` | `useLocation` | — | compiler-dependent |
| `vitest` | `it`, `expect`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `capacityApi` |
| Module calls | `mock`, `mock`, `mock`, `it`, `capacityApi = hoisted`, `mock`, `mock`, `mock`, `it`, `it`, `it` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/capacity/CapacitySection.test.tsx"]
    n1["frontend/src/components/capacity/CapacitySection.tsx"]
    n2["frontend/src/features/identity/identityContext.ts"]
    n3["frontend/src/i18n/i18n.ts"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n5["frontend/src/types/iteration.ts"]
    n6["frontend/src/types/team.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n0 --> n5
    n0 --> n6
    n1 --> n2
    n1 --> n5
    n1 --> n6
    n4 --> n3
    click n0 "../modules/CapacitySection.test.md"
    click n1 "../modules/CapacitySection.md"
    click n2 "../modules/identityContext.md"
    click n3 "../modules/i18n.md"
    click n4 "../modules/renderWithProviders.md"
    click n5 "../modules/types_iteration.md"
    click n6 "../modules/types_team.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [CapacitySection](../modules/CapacitySection.md) |
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |
| Outbound | [types_team](../modules/types_team.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |
