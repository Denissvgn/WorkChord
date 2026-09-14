# taskFilters.test Module

**Path:** `frontend/src/utils/taskFilters.test.ts`

## Description

_Auto-generated from `frontend/src/utils/taskFilters.test.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/task` | `Task` |
| `./taskFilterDefaults` | `defaultFilters` |
| `./taskFilters` | `filterTaskWithChildren`, `taskMatchesFilters` |
| `vitest` | `describe`, `expect`, `it` |

## Module Signals

| Signal | Values |
|--------|--------|
| Module calls | `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/types/task.ts"]
    n1["frontend/src/utils/taskFilterDefaults.ts"]
    n2["frontend/src/utils/taskFilters.test.ts"]
    n3["frontend/src/utils/taskFilters.ts"]
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n3 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/taskFilterDefaults.md"
    click n2 "../modules/taskFilters.test.md"
    click n3 "../modules/taskFilters.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [taskFilterDefaults](../modules/taskFilterDefaults.md) |
| Outbound | [taskFilters](../modules/taskFilters.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |
