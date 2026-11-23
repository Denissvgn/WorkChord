# workspaceApi Module

**Path:** `frontend/src/test/workspaceApi.ts`

## Description

_Auto-generated from `frontend/src/test/workspaceApi.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../services/api` | `api` | — | compiler-dependent |
| `../types/task` | `Task`, `TaskStatus` | Declaration | erased |
| `vitest` | `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `WORKSPACE_ITERATIONS`, `WORKSPACE_PROJECTS`, `WORKSPACE_RELEASE`, `WORKSPACE_SHARE`, `WORKSPACE_TASKS`, `installWorkspaceApi` |
| Constants | `WORKSPACE_ITERATIONS`, `WORKSPACE_PROJECTS`, `WORKSPACE_TASKS`, `durations`, `ROUTES`, `WORKSPACE_RELEASE`, `WORKSPACE_SHARE`, `DETAIL_ROUTES` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/pages/destinationEmptyStates.test.tsx"]
    n1["frontend/src/services/api.ts"]
    n2["frontend/src/test/accessibilityInvariants.test.tsx"]
    n3["frontend/src/test/pageChrome.test.tsx"]
    n4["frontend/src/test/scopedPageRender.test.tsx"]
    n5["frontend/src/test/workspaceApi.ts"]
    n6["frontend/src/types/task.ts"]
    n0 --> n1
    n0 --> n5
    n2 --> n5
    n3 --> n5
    n4 --> n5
    n5 --> n1
    n5 --> n6
    click n0 "../modules/destinationEmptyStates.test.md"
    click n1 "../modules/api.md"
    click n2 "../modules/accessibilityInvariants.test.md"
    click n3 "../modules/pageChrome.test.md"
    click n4 "../modules/scopedPageRender.test.md"
    click n5 "../modules/workspaceApi.md"
    click n6 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [destinationEmptyStates.test](../modules/destinationEmptyStates.test.md) |
| Inbound | [accessibilityInvariants.test](../modules/accessibilityInvariants.test.md) |
| Inbound | [pageChrome.test](../modules/pageChrome.test.md) |
| Inbound | [scopedPageRender.test](../modules/scopedPageRender.test.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `installWorkspaceApi` | `(extra: Array<[RegExp, (match: RegExpMatchArray) => unknown]> = [])` | — | Answers every GET from the workspace above, with the unplanned ones failing by URL. Restored by `vi.restoreAllMocks`. |
