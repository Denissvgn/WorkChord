# seedDisplay.test Module

**Path:** `frontend/src/i18n/seedDisplay.test.ts`

## Description

_Auto-generated from `frontend/src/i18n/seedDisplay.test.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../types/label` | `LabelGroupBrief` | Declaration | erased |
| `./i18n` | `changeAppLanguage` | — | compiler-dependent |
| `./seedDisplay` | `labelDisplay`, `labelGroupDisplay` | — | compiler-dependent |
| `vitest` | `afterEach`, `describe`, `expect`, `it` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Module calls | `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/i18n/i18n.ts"]
    n1["frontend/src/i18n/seedDisplay.test.ts"]
    n2["frontend/src/i18n/seedDisplay.ts"]
    n3["frontend/src/types/label.ts"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n2 --> n0
    n2 --> n3
    click n0 "../modules/i18n.md"
    click n1 "../modules/seedDisplay.test.md"
    click n2 "../modules/seedDisplay.md"
    click n3 "../modules/types_label.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [seedDisplay](../modules/seedDisplay.md) |
| Outbound | [types_label](../modules/types_label.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |
