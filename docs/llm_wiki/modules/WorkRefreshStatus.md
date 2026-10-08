# WorkRefreshStatus Module

**Path:** `frontend/src/components/feedback/WorkRefreshStatus.tsx`

## Description

_Auto-generated from `frontend/src/components/feedback/WorkRefreshStatus.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../features/workQueryFreshness` | `WORKSPACE_QUERY_POLICIES` |
| `@tanstack/react-query` | `useQueryClient` |
| `react` | `useEffect`, `useReducer`, `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `WorkRefreshStatus` |

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
| `WorkRefreshStatus` | `()` | — | — |
