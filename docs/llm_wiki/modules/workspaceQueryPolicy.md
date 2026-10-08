# workspaceQueryPolicy Module

**Path:** `frontend/src/features/workspaceQueryPolicy.ts`

## Description

Creates the identity/access-scoped workspace client and installs both shared work freshness and planning navigation invalidation on that client. Disposal unsubscribes both listeners, cancels pending requests and clears the old cache, preventing old-account responses from entering replacement access state. The outer shell client retains identity ownership without duplicate work-policy registration.

## Imports

| Source | Symbols |
|--------|---------|
| `./planningMasters/planningNavigationInvalidation` | `installPlanningNavigationInvalidation` |
| `./workQueryFreshness` | `installWorkFreshness` |
| `@tanstack/react-query` | `QueryClient` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `createWorkspaceQueryClient`, `installWorkspaceQueryPolicy` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/features/identity/IdentityProvider.tsx"]
    n1["frontend/src/features/planningMasters/planningNavigationInvalidation.ts"]
    n2["frontend/src/features/useLiveWindow.test.tsx"]
    n3["frontend/src/features/workQueryFreshness.ts"]
    n4["frontend/src/features/workspaceQueryPolicy.test.ts"]
    n5["frontend/src/features/workspaceQueryPolicy.ts"]
    n0 --> n5
    n2 --> n5
    n4 --> n3
    n4 --> n5
    n5 --> n1
    n5 --> n3
    click n0 "../modules/IdentityProvider.md"
    click n1 "../modules/planningNavigationInvalidation.md"
    click n2 "../modules/useLiveWindow.test.md"
    click n3 "../modules/workQueryFreshness.md"
    click n4 "../modules/workspaceQueryPolicy.test.md"
    click n5 "../modules/workspaceQueryPolicy.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [IdentityProvider](../modules/IdentityProvider.md) |
| Inbound | [useLiveWindow.test](../modules/useLiveWindow.test.md) |
| Inbound | [workspaceQueryPolicy.test](../modules/workspaceQueryPolicy.test.md) |
| Outbound | [planningNavigationInvalidation](../modules/planningNavigationInvalidation.md) |
| Outbound | [workQueryFreshness](../modules/workQueryFreshness.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `createWorkspaceQueryClient` | `(accessKey: string)` | — | — |
| `installWorkspaceQueryPolicy` | `(client: QueryClient)` | — | — |
