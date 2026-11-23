# WorkRefreshStatus Module

**Path:** `frontend/src/components/feedback/WorkRefreshStatus.tsx`

## Description

_Auto-generated from `frontend/src/components/feedback/WorkRefreshStatus.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Button` | `Button` | — | compiler-dependent |
| `../../features/workQueryFreshness` | `WORKSPACE_QUERY_POLICIES` | — | compiler-dependent |
| `@tanstack/react-query` | `notifyManager`, `useQueryClient` | — | compiler-dependent |
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
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/feedback/WorkRefreshStatus.test.tsx"]
    n2["frontend/src/components/feedback/WorkRefreshStatus.tsx"]
    n3["frontend/src/components/layout/AppShell.tsx"]
    n4["frontend/src/features/workQueryFreshness.ts"]
    n1 --> n0
    n1 --> n2
    n2 --> n0
    n2 --> n4
    n3 --> n2
    click n0 "../modules/Button.md"
    click n1 "../modules/WorkRefreshStatus.test.md"
    click n2 "../modules/WorkRefreshStatus.md"
    click n3 "../modules/AppShell.md"
    click n4 "../modules/workQueryFreshness.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [WorkRefreshStatus.test](../modules/WorkRefreshStatus.test.md) |
| Inbound | [AppShell](../modules/AppShell.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [workQueryFreshness](../modules/workQueryFreshness.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `WorkRefreshStatus` | `()` | — | Silent while work data is fresh; says so, with a way to refresh, only when it may be out of date. |
