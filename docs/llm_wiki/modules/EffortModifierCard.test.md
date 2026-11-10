# EffortModifierCard.test Module

**Path:** `frontend/src/components/settings/EffortModifierCard.test.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/EffortModifierCard.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/schedulingRules` | `EffortModifier` | Declaration | erased |
| `./EffortModifierCard` | `EffortModifierCard` | — | compiler-dependent |
| `@testing-library/react` | `screen` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Module calls | `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/settings/EffortModifierCard.test.tsx"]
    n1["frontend/src/components/settings/EffortModifierCard.tsx"]
    n2["frontend/src/test/renderWithProviders.tsx"]
    n3["frontend/src/types/schedulingRules.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n3
    click n0 "../modules/EffortModifierCard.test.md"
    click n1 "../modules/EffortModifierCard.md"
    click n2 "../modules/renderWithProviders.md"
    click n3 "../modules/schedulingRules.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [EffortModifierCard](../modules/EffortModifierCard.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [schedulingRules](../modules/schedulingRules.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
