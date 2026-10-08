# workspaceQueryPolicy.test Module

**Path:** `frontend/src/features/workspaceQueryPolicy.test.ts`

## Description

_Auto-generated from `frontend/src/features/workspaceQueryPolicy.test.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `./workQueryFreshness` | `WORKSPACE_QUERY_POLICIES` |
| `./workspaceQueryPolicy` | `createWorkspaceQueryClient`, `installWorkspaceQueryPolicy` |
| `@tanstack/react-query` | `QueryObserver` |
| `vitest` | `expect`, `it`, `vi` |

## Module Signals

| Signal | Values |
|--------|--------|
| Module calls | `it.each(['hidden', 'disabled', 'unauthorized', 'too-many-pages'])`, `it`, `it`, `it`, `it` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/features/workQueryFreshness.ts"]
    n1["frontend/src/features/workspaceQueryPolicy.test.ts"]
    n2["frontend/src/features/workspaceQueryPolicy.ts"]
    n1 --> n0
    n1 --> n2
    n2 --> n0
    click n0 "../modules/workQueryFreshness.md"
    click n1 "../modules/workspaceQueryPolicy.test.md"
    click n2 "../modules/workspaceQueryPolicy.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [workQueryFreshness](../modules/workQueryFreshness.md) |
| Outbound | [workspaceQueryPolicy](../modules/workspaceQueryPolicy.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
