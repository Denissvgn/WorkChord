# TemplateLabelSettings.test Module

**Path:** `frontend/src/components/settings/TemplateLabelSettings.test.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/TemplateLabelSettings.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/MutationSuccessFeedback` | `MutationSuccessFeedback` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/label` | `Label`, `LabelGroup` | Declaration | erased |
| `./TemplateLabelSettings` | `TemplateLabelSettings` | — | compiler-dependent |
| `@testing-library/react` | `act`, `screen`, `waitFor`, `within` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `labelServiceMock`, `templateServiceMock`, `toastMock` |
| Module calls | `labelServiceMock = hoisted`, `templateServiceMock = hoisted`, `toastMock = hoisted`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/settings/TemplateLabelSettings.test.tsx"]
    n1["frontend/src/components/settings/TemplateLabelSettings.tsx"]
    n2["frontend/src/features/MutationSuccessFeedback.tsx"]
    n3["frontend/src/test/renderWithProviders.tsx"]
    n4["frontend/src/types/label.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n1 --> n4
    click n0 "../modules/TemplateLabelSettings.test.md"
    click n1 "../modules/TemplateLabelSettings.md"
    click n2 "../modules/MutationSuccessFeedback.md"
    click n3 "../modules/renderWithProviders.md"
    click n4 "../modules/types_label.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [TemplateLabelSettings](../modules/TemplateLabelSettings.md) |
| Outbound | [MutationSuccessFeedback](../modules/MutationSuccessFeedback.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_label](../modules/types_label.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
