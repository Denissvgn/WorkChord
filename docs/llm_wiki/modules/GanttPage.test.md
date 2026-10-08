# GanttPage.test Module

**Path:** `frontend/src/pages/GanttPage.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/GanttPage.test.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../i18n/i18n` | `i18n` |
| `../store/iterationStore` | `useIterationStore` |
| `../test/renderWithProviders` | `renderWithProviders` |
| `../types/gantt` | `GanttResponse`, `GanttTask` |
| `../types/iteration` | `Iteration` |
| `./GanttPage` | `GanttPage` |
| `@testing-library/react` | `screen`, `waitFor`, `within` |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `ganttServiceMock`, `iterationServiceMock`, `taskServiceMock`, `iterationFixture`, `taskFixture`, `ganttFixture` |
| Module calls | `ganttServiceMock = hoisted`, `iterationServiceMock = hoisted`, `taskServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/i18n/i18n.ts"]
    n1["frontend/src/pages/GanttPage.test.tsx"]
    n2["frontend/src/pages/GanttPage.tsx"]
    n3["frontend/src/store/iterationStore.ts"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n5["frontend/src/types/gantt.ts"]
    n6["frontend/src/types/iteration.ts"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n1 --> n6
    n2 --> n3
    n2 --> n5
    n2 --> n6
    n5 --> n6
    click n0 "../modules/i18n.md"
    click n1 "../modules/GanttPage.test.md"
    click n2 "../modules/GanttPage.md"
    click n3 "../modules/iterationStore.md"
    click n4 "../modules/renderWithProviders.md"
    click n5 "../modules/types_gantt.md"
    click n6 "../modules/types_iteration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [GanttPage](../modules/GanttPage.md) |
| Outbound | [iterationStore](../modules/iterationStore.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_gantt](../modules/types_gantt.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
