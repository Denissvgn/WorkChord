# workQueryFreshness Module

**Path:** `frontend/src/features/workQueryFreshness.ts`

## Description

_Auto-generated from `frontend/src/features/workQueryFreshness.ts`._

Shared work queries refresh on focus and every 30 seconds in the foreground, with bounded failure backoff and mutation invalidation. Background and unauthorized polling stop; identity-specific clients prevent old-account cache reuse.

## Imports

| Source | Symbols |
|--------|---------|
| `@tanstack/react-query` | `QueryClient` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `WORK_QUERY_KEYS`, `installWorkFreshness` |
| Constants | `WORK_QUERY_KEYS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/features/identity/IdentityProvider.tsx"]
    n1["frontend/src/features/workQueryFreshness.ts"]
    n2["frontend/src/main.tsx"]
    n0 --> n1
    n2 --> n0
    n2 --> n1
    click n0 "../modules/IdentityProvider.md"
    click n1 "../modules/workQueryFreshness.md"
    click n2 "../modules/src_main.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [IdentityProvider](../modules/IdentityProvider.md) |
| Inbound | [src_main](../modules/src_main.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `installWorkFreshness` | `(client: QueryClient)` | — | — |