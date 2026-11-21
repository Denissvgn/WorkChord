# GanttPage.test Module

**Path:** `frontend/src/pages/GanttPage.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/GanttPage.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/common/Button` | `Button` | — | compiler-dependent |
| `../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../store/iterationStore` | `useIterationStore` | — | compiler-dependent |
| `../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../types/gantt` | `GanttResponse`, `GanttTask` | Declaration | erased |
| `../types/iteration` | `Iteration` | Declaration | erased |
| `./GanttPage` | `GanttPage` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor`, `within` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `ganttServiceMock`, `iterationServiceMock`, `taskServiceMock`, `iterationFixture`, `taskFixture`, `ganttFixture` |
| Module calls | `ganttServiceMock = hoisted`, `iterationServiceMock = hoisted`, `taskServiceMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/i18n/i18n.ts"]
    n2["frontend/src/pages/GanttPage.test.tsx"]
    n3["frontend/src/pages/GanttPage.tsx"]
    n4["frontend/src/store/iterationStore.ts"]
    n5["frontend/src/test/renderWithProviders.tsx"]
    n6["frontend/src/types/gantt.ts"]
    n7["frontend/src/types/iteration.ts"]
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n2 --> n7
    n3 --> n0
    n3 --> n6
    n3 --> n7
    n5 --> n1
    n6 --> n7
    click n0 "../modules/Button.md"
    click n1 "../modules/i18n.md"
    click n2 "../modules/GanttPage.test.md"
    click n3 "../modules/GanttPage.md"
    click n4 "../modules/iterationStore.md"
    click n5 "../modules/renderWithProviders.md"
    click n6 "../modules/types_gantt.md"
    click n7 "../modules/types_iteration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [Button](../modules/Button.md) |
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
