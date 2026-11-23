# TaskList.test Module

**Path:** `frontend/src/components/tasks/TaskList.test.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskList.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../i18n/i18n` | `changeAppLanguage` | — | compiler-dependent |
| `../../test/fixtures/taskDetail` | `taskDetailResponse` | — | compiler-dependent |
| `../../test/renderWithProviders` | `createTestQueryClient`, `renderWithProviders` | — | compiler-dependent |
| `../../types/task` | `Task` | Declaration | erased |
| `../../utils/taskFilterDefaults` | `defaultFilters` | — | compiler-dependent |
| `./TaskFiltersBar` | `TaskFilters` | Declaration | erased |
| `./TaskList` | `TaskList` | — | compiler-dependent |
| `./useAgentRowFacts` | `REVIEWER_PAGE_SIZE` | — | compiler-dependent |
| `@testing-library/react` | `act`, `fireEvent`, `screen`, `waitFor`, `within` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `taskServiceMock`, `labelServiceMock`, `teamMock`, `INTERACTIVE` |
| Module calls | `taskServiceMock = hoisted`, `labelServiceMock = hoisted`, `mock`, `mock`, `teamMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `describe`, `it`, `it`, `it`, `describe`, `describe`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/TaskFiltersBar.tsx"]
    n1["frontend/src/components/tasks/TaskList.test.tsx"]
    n2["frontend/src/components/tasks/TaskList.tsx"]
    n3["frontend/src/components/tasks/useAgentRowFacts.ts"]
    n4["frontend/src/i18n/i18n.ts"]
    n5["frontend/src/test/fixtures/taskDetail.ts"]
    n6["frontend/src/test/renderWithProviders.tsx"]
    n7["frontend/src/types/task.ts"]
    n8["frontend/src/utils/taskFilterDefaults.ts"]
    n0 --> n8
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n1 --> n6
    n1 --> n7
    n1 --> n8
    n2 --> n0
    n2 --> n3
    n2 --> n7
    n3 --> n7
    n5 --> n7
    n6 --> n4
    n8 --> n0
    click n0 "../modules/TaskFiltersBar.md"
    click n1 "../modules/TaskList.test.md"
    click n2 "../modules/TaskList.md"
    click n3 "../modules/useAgentRowFacts.md"
    click n4 "../modules/i18n.md"
    click n5 "../modules/taskDetail.md"
    click n6 "../modules/renderWithProviders.md"
    click n7 "../modules/types_task.md"
    click n8 "../modules/taskFilterDefaults.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [TaskFiltersBar](../modules/TaskFiltersBar.md) |
| Outbound | [TaskList](../modules/TaskList.md) |
| Outbound | [useAgentRowFacts](../modules/useAgentRowFacts.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [taskDetail](../modules/taskDetail.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [taskFilterDefaults](../modules/taskFilterDefaults.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
