# ProjectTaskTree.test Module

**Path:** `frontend/src/components/projects/ProjectTaskTree.test.tsx`

## Description

_Auto-generated from `frontend/src/components/projects/ProjectTaskTree.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../test/fixtures/taskDetail` | `taskDetailResponse` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/task` | `Task` | Declaration | erased |
| `./ProjectTaskTree` | `ProjectTaskTree` | — | compiler-dependent |
| `./ProjectTasksTab` | `ProjectTasksTab` | — | compiler-dependent |
| `@testing-library/react` | `fireEvent`, `screen`, `waitFor`, `within` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `services` |
| Module calls | `services = hoisted`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/projects/ProjectTasksTab.tsx"]
    n1["frontend/src/components/projects/ProjectTaskTree.test.tsx"]
    n2["frontend/src/components/projects/ProjectTaskTree.tsx"]
    n3["frontend/src/test/fixtures/taskDetail.ts"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n5["frontend/src/types/task.ts"]
    n0 --> n2
    n0 --> n5
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n2 --> n5
    n3 --> n5
    click n0 "../modules/ProjectTasksTab.md"
    click n1 "../modules/ProjectTaskTree.test.md"
    click n2 "../modules/ProjectTaskTree.md"
    click n3 "../modules/taskDetail.md"
    click n4 "../modules/renderWithProviders.md"
    click n5 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [ProjectTasksTab](../modules/ProjectTasksTab.md) |
| Outbound | [ProjectTaskTree](../modules/ProjectTaskTree.md) |
| Outbound | [taskDetail](../modules/taskDetail.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
