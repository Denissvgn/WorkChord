# apiError Module

**Path:** `frontend/src/utils/apiError.ts`

## Description

_Auto-generated from `frontend/src/utils/apiError.ts`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ApiErrorKind`, `ApiFieldError`, `NormalizedApiError`, `getApiErrorMessage`, `getApiErrorStatus`, `getApiFieldErrors`, `normalizeApiError` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/utils/apiError.ts"]
    n0 --> n1
    click n1 "../modules/apiError.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (44) |

> All 44 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ApiFieldError](../entities/ApiFieldError.md) | Class | 3 | — | — |
| [NormalizedApiError](../entities/NormalizedApiError.md) | Class | 8 | — | — |
| [ApiErrorShape](../entities/ApiErrorShape.md) | Class | 17 | — | — |
| [ApiErrorKind](../entities/ApiErrorKind.md) | Type alias | 1 | — | — |
| [UnknownRecord](../entities/UnknownRecord.md) | Type alias | 26 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `normalizeApiError` | `(error: unknown, fallback: string) -> NormalizedApiError` | — | — |
| `getApiErrorMessage` | `(error: unknown, fallback: string)` | — | — |
| `getApiErrorStatus` | `(error: unknown)` | — | — |
| `getApiFieldErrors` | `(error: unknown, fallback: string)` | — | — |
