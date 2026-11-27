# apiError.routing.test Module

**Path:** `frontend/src/utils/apiError.routing.test.ts`

## Description

_Auto-generated from `frontend/src/utils/apiError.routing.test.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../i18n/i18n` | `changeAppLanguage` | — | compiler-dependent |
| `./apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `refusal` |
| Module calls | `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/i18n/i18n.ts"]
    n1["frontend/src/utils/apiError.routing.test.ts"]
    n2["frontend/src/utils/apiError.ts"]
    n1 --> n0
    n1 --> n2
    n2 --> n0
    click n0 "../modules/i18n.md"
    click n1 "../modules/apiError.routing.test.md"
    click n2 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |
