# TasksPage.toolbar.test Module

**Path:** `frontend/src/pages/TasksPage.toolbar.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/TasksPage.toolbar.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../test/pageChrome` | `expectPageChrome` | — | compiler-dependent |
| `../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../types/savedView` | `SavedView` | Declaration | erased |
| `../types/task` | `Task` | Declaration | erased |
| `./TasksPage` | `TasksPage` | — | compiler-dependent |
| `@testing-library/react` | `cleanup`, `fireEvent`, `screen`, `waitFor`, `within` | — | compiler-dependent |
| `node:fs` | `readFileSync` | — | compiler-dependent |
| `node:path` | `resolve` | — | compiler-dependent |
| `node:url` | `pathToFileURL` | — | compiler-dependent |
| `postcss` | `postcss` | — | compiler-dependent |
| `react-router-dom` | `useLocation` | — | compiler-dependent |
| `tailwindcss` | `tailwindcss` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |
| Unresolved `dynamic-import` | — (line 473; deferred) | — | unclassified |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `workScopeMock`, `iterationServiceMock`, `taskServiceMock`, `savedViewServiceMock`, `css`, `ana`, `TASKS`, `anaPlannedView`, `LAYOUT_PROPERTIES` |
| Module calls | `workScopeMock = hoisted`, `iterationServiceMock = hoisted`, `taskServiceMock = hoisted`, `savedViewServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `css = readFileSync`, `describe`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/i18n/i18n.ts"]
    n1["frontend/src/pages/TasksPage.toolbar.test.tsx"]
    n2["frontend/src/pages/TasksPage.tsx"]
    n3["frontend/src/test/pageChrome.ts"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n5["frontend/src/types/savedView.ts"]
    n6["frontend/src/types/task.ts"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n1 --> n6
    n2 --> n5
    n2 --> n6
    n4 --> n0
    click n0 "../modules/i18n.md"
    click n1 "../modules/TasksPage.toolbar.test.md"
    click n2 "../modules/TasksPage.md"
    click n3 "../modules/pageChrome.md"
    click n4 "../modules/renderWithProviders.md"
    click n5 "../modules/savedView.md"
    click n6 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [pageChrome](../modules/pageChrome.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [savedView](../modules/savedView.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |
