# ganttChrome.test Module

**Path:** `frontend/src/test/ganttChrome.test.tsx`

## Description

_Auto-generated from `frontend/src/test/ganttChrome.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../pages/GanttPage` | `GanttPage` | — | compiler-dependent |
| `../store/iterationStore` | `useIterationStore` | — | compiler-dependent |
| `../types/gantt` | `GanttResponse`, `GanttTask` | Declaration | erased |
| `../types/iteration` | `Iteration` | Declaration | erased |
| `./pageChrome` | `expectPageChrome` | — | compiler-dependent |
| `./renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `within` | — | compiler-dependent |
| `vitest` | `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `services`, `iterationFixture`, `taskFixture`, `ganttFixture` |
| Module calls | `services = hoisted`, `mock`, `mock`, `it` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/pages/GanttPage.tsx"]
    n1["frontend/src/store/iterationStore.ts"]
    n2["frontend/src/test/ganttChrome.test.tsx"]
    n3["frontend/src/test/pageChrome.ts"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n5["frontend/src/types/gantt.ts"]
    n6["frontend/src/types/iteration.ts"]
    n0 --> n5
    n0 --> n6
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n5 --> n6
    click n0 "../modules/GanttPage.md"
    click n1 "../modules/iterationStore.md"
    click n2 "../modules/ganttChrome.test.md"
    click n3 "../modules/pageChrome.md"
    click n4 "../modules/renderWithProviders.md"
    click n5 "../modules/types_gantt.md"
    click n6 "../modules/types_iteration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [GanttPage](../modules/GanttPage.md) |
| Outbound | [iterationStore](../modules/iterationStore.md) |
| Outbound | [pageChrome](../modules/pageChrome.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_gantt](../modules/types_gantt.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
