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
    n1["frontend/src/features/workQueryFreshness.test.ts"]
    n2["frontend/src/features/workQueryFreshness.ts"]
    n3["frontend/src/main.tsx"]
    n0 --> n2
    n1 --> n2
    n3 --> n0
    n3 --> n2
    click n0 "../modules/IdentityProvider.md"
    click n1 "../modules/workQueryFreshness.test.md"
    click n2 "../modules/workQueryFreshness.md"
    click n3 "../modules/src_main.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [IdentityProvider](../modules/IdentityProvider.md) |
| Inbound | [workQueryFreshness.test](../modules/workQueryFreshness.test.md) |
| Inbound | [src_main](../modules/src_main.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `installWorkFreshness` | `(client: QueryClient)` | — | — |