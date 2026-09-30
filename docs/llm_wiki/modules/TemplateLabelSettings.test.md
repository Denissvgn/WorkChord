# TemplateLabelSettings.test Module

**Path:** `frontend/src/components/settings/TemplateLabelSettings.test.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/TemplateLabelSettings.test.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../test/renderWithProviders` | `renderWithProviders` |
| `../../types/label` | `Label`, `LabelGroup` |
| `./TemplateLabelSettings` | `TemplateLabelSettings` |
| `@testing-library/react` | `act`, `screen`, `waitFor`, `within` |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `labelServiceMock`, `templateServiceMock`, `toastMock` |
| Module calls | `labelServiceMock = hoisted`, `templateServiceMock = hoisted`, `toastMock = hoisted`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/TemplateLabelSettings.test.tsx"]
    n1["frontend/src/components/settings/TemplateLabelSettings.tsx"]
    n2["frontend/src/test/renderWithProviders.tsx"]
    n3["frontend/src/types/label.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n3
    click n0 "../modules/TemplateLabelSettings.test.md"
    click n1 "../modules/TemplateLabelSettings.md"
    click n2 "../modules/renderWithProviders.md"
    click n3 "../modules/types_label.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [TemplateLabelSettings](../modules/TemplateLabelSettings.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_label](../modules/types_label.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
