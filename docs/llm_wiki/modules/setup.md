# setup Module

**Path:** `frontend/src/test/setup.ts`

## Description

_Auto-generated from `frontend/src/test/setup.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../i18n/i18n` | `i18n` | — | compiler-dependent |
| `@testing-library/jest-dom/vitest` | — | — | present |
| `@testing-library/react` | `cleanup` | — | compiler-dependent |
| `vitest` | `afterEach` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Module calls | `afterEach` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/i18n/i18n.ts"]
    n1["frontend/src/test/setup.ts"]
    n1 --> n0
    click n0 "../modules/i18n.md"
    click n1 "../modules/setup.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [i18n](../modules/i18n.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
