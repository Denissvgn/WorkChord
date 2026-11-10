# savedViewState.test Module

**Path:** `frontend/src/utils/savedViewState.test.ts`

## Description

_Auto-generated from `frontend/src/utils/savedViewState.test.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../types/savedView` | `SavedView` | Declaration | erased |
| `./savedViewState` | `filterSignature`, `savedViewModified` | — | compiler-dependent |
| `./taskFilterDefaults` | `defaultFilters` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Module calls | `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/types/savedView.ts"]
    n1["frontend/src/utils/savedViewState.test.ts"]
    n2["frontend/src/utils/savedViewState.ts"]
    n3["frontend/src/utils/taskFilterDefaults.ts"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n2 --> n0
    n2 --> n3
    click n0 "../modules/savedView.md"
    click n1 "../modules/savedViewState.test.md"
    click n2 "../modules/savedViewState.md"
    click n3 "../modules/taskFilterDefaults.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [savedView](../modules/savedView.md) |
| Outbound | [savedViewState](../modules/savedViewState.md) |
| Outbound | [taskFilterDefaults](../modules/taskFilterDefaults.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |
