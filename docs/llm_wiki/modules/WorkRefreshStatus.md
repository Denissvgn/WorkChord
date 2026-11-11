# WorkRefreshStatus Module

**Path:** `frontend/src/components/feedback/WorkRefreshStatus.tsx`

## Description

_Auto-generated from `frontend/src/components/feedback/WorkRefreshStatus.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/workQueryFreshness` | `WORKSPACE_QUERY_POLICIES` | — | compiler-dependent |
| `@tanstack/react-query` | `useQueryClient` | — | compiler-dependent |
| `react` | `useEffect`, `useReducer`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `WorkRefreshStatus` |
| Constants | `STALE_AFTER_MS`, `RECHECK_MS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/feedback/WorkRefreshStatus.tsx"]
    n1["frontend/src/components/layout/AppShell.tsx"]
    n2["frontend/src/features/workQueryFreshness.ts"]
    n0 --> n2
    n1 --> n0
    click n0 "../modules/WorkRefreshStatus.md"
    click n1 "../modules/AppShell.md"
    click n2 "../modules/workQueryFreshness.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AppShell](../modules/AppShell.md) |
| Outbound | [workQueryFreshness](../modules/workQueryFreshness.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `WorkRefreshStatus` | `()` | — | Silent while work data is fresh; says so, with a way to refresh, only when it may be out of date. |
