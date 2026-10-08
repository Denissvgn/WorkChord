# workQueryFreshness Module

**Path:** `frontend/src/features/workQueryFreshness.ts`

## Description

_Auto-generated from `frontend/src/features/workQueryFreshness.ts`._

An explicit workspace registry separates live work, immutable history, editor snapshots, on-demand reference data, settings and identity ownership. Eligible active live queries refresh every 30 seconds while visible, retaining the existing failure backoff. Hidden, disabled and unauthorized queries stop polling. Automatic refresh does not replay more than five accumulated pages or replace editor/history snapshots. Explicit mutation effects limit unrelated settings traffic; unmapped mutations retain legacy work invalidation until adoption is complete.

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
    n0["frontend/src/features/workQueryFreshness.test.ts"]
    n1["frontend/src/features/workQueryFreshness.ts"]
    n2["frontend/src/features/workspaceQueryPolicy.test.ts"]
    n3["frontend/src/features/workspaceQueryPolicy.ts"]
    n0 --> n1
    n2 --> n1
    n2 --> n3
    n3 --> n1
    click n0 "../modules/workQueryFreshness.test.md"
    click n1 "../modules/workQueryFreshness.md"
    click n2 "../modules/workspaceQueryPolicy.test.md"
    click n3 "../modules/workspaceQueryPolicy.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
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