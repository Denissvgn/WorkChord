# NativeConnectionPage Module

**Path:** `frontend/src/pages/NativeConnectionPage.tsx`

## Description

Provides explicit browser consent for the Android companion. It shows the signed-in account and verification code, requires a matching-code checkbox, and resets consent when the request or principal changes. Loading, failure, retry, and approval are separate visible states.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/common/Button` | `Button` | — | compiler-dependent |
| `../components/common/DisabledReason` | `DisabledReason` | — | compiler-dependent |
| `../features/identity/identityContext` | `useIdentity` | — | compiler-dependent |
| `../services/api` | `api` | — | compiler-dependent |
| `../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `react` | `useEffect`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `useSearchParams` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/DisabledReason.tsx"]
    n2["frontend/src/features/identity/identityContext.ts"]
    n3["frontend/src/pages/NativeConnectionPage.test.tsx"]
    n4["frontend/src/pages/NativeConnectionPage.tsx"]
    n5["frontend/src/services/api.ts"]
    n6["frontend/src/utils/apiError.ts"]
    n3 --> n2
    n3 --> n4
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n5
    n4 --> n6
    click n0 "../modules/Button.md"
    click n1 "../modules/DisabledReason.md"
    click n2 "../modules/identityContext.md"
    click n3 "../modules/NativeConnectionPage.test.md"
    click n4 "../modules/NativeConnectionPage.md"
    click n5 "../modules/api.md"
    click n6 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [NativeConnectionPage.test](../modules/NativeConnectionPage.test.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [DisabledReason](../modules/DisabledReason.md) |
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