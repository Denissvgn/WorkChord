# workQueryFreshness Module

**Path:** `frontend/src/features/workQueryFreshness.ts`

## Description

Unauthorized query failures remove cached server data and suppress automatic retries and polling. Live retained-window heads participate in declared mutation effects through their owning root. Visible active windows retain the foreground interval and bounded error backoff; immutable histories and editor observations remain distinct.

## Imports

| Source | Symbols |
|--------|---------|
| `@tanstack/react-query` | `QueryClient` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `WORKSPACE_QUERY_POLICIES`, `WORK_QUERY_KEYS`, `installWorkFreshness` |
| Constants | `ROOTS_BY_POLICY`, `WORKSPACE_QUERY_POLICIES`, `WORK_QUERY_KEYS`, `MUTATION_ROOT_EFFECTS` |
| Module calls | `WORKSPACE_QUERY_POLICIES = fromEntries` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/feedback/WorkRefreshStatus.tsx"]
    n1["frontend/src/features/workQueryFreshness.test.ts"]
    n2["frontend/src/features/workQueryFreshness.ts"]
    n3["frontend/src/features/workspaceQueryPolicy.test.ts"]
    n4["frontend/src/features/workspaceQueryPolicy.ts"]
    n0 --> n2
    n1 --> n2
    n3 --> n2
    n3 --> n4
    n4 --> n2
    click n0 "../modules/WorkRefreshStatus.md"
    click n1 "../modules/workQueryFreshness.test.md"
    click n2 "../modules/workQueryFreshness.md"
    click n3 "../modules/workspaceQueryPolicy.test.md"
    click n4 "../modules/workspaceQueryPolicy.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [WorkRefreshStatus](../modules/WorkRefreshStatus.md) |
| Inbound | [workQueryFreshness.test](../modules/workQueryFreshness.test.md) |
| Inbound | [workspaceQueryPolicy.test](../modules/workspaceQueryPolicy.test.md) |
| Inbound | [workspaceQueryPolicy](../modules/workspaceQueryPolicy.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [QueryPolicy](../entities/QueryPolicy.md) | Type alias | 3 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `installWorkFreshness` | `(client: QueryClient)` | — | — |