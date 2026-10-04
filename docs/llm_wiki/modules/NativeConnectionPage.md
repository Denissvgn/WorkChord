# NativeConnectionPage Module

**Path:** `frontend/src/pages/NativeConnectionPage.tsx`

## Description

Provides explicit browser consent for the Android companion. It shows the signed-in account and verification code, requires a matching-code checkbox, and resets consent when the request or principal changes. Loading, failure, retry, and approval are separate visible states.

## Imports

| Source | Symbols |
|--------|---------|
| `../components/common/Button` | `Button` |
| `../features/identity/identityContext` | `useIdentity` |
| `../services/api` | `api` |
| `../utils/apiError` | `getApiErrorMessage` |
| `@tanstack/react-query` | `useQuery` |
| `react` | `useState` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `useSearchParams` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/features/identity/identityContext.ts"]
    n2["frontend/src/pages/NativeConnectionPage.test.tsx"]
    n3["frontend/src/pages/NativeConnectionPage.tsx"]
    n4["frontend/src/services/api.ts"]
    n5["frontend/src/utils/apiError.ts"]
    n2 --> n1
    n2 --> n3
    n3 --> n0
    n3 --> n1
    n3 --> n4
    n3 --> n5
    click n0 "../modules/Button.md"
    click n1 "../modules/identityContext.md"
    click n2 "../modules/NativeConnectionPage.test.md"
    click n3 "../modules/NativeConnectionPage.md"
    click n4 "../modules/api.md"
    click n5 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [NativeConnectionPage.test](../modules/NativeConnectionPage.test.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `NativeConnectionPage` | `()` | — | — |