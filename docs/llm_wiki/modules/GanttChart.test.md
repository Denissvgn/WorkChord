# GanttChart.test Module

**Path:** `frontend/src/components/gantt/GanttChart.test.tsx`

## Description

_Auto-generated from `frontend/src/components/gantt/GanttChart.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/gantt` | `GanttTask`, `SchedulePreviewResponse`, `ScheduleResult` | Declaration | erased |
| `../../utils/formatDate` | `formatDate` | — | compiler-dependent |
| `./GanttChart` | `GanttChart` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `ganttServiceMock`, `taskFixture`, `scheduleResult`, `previewFixture` |
| Module calls | `ganttServiceMock = hoisted`, `mock`, `mock`, `mock`, `describe`, `describe`, `describe`, `describe`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/gantt/GanttChart.test.tsx"]
    n1["frontend/src/components/gantt/GanttChart.tsx"]
    n2["frontend/src/i18n/i18n.ts"]
    n3["frontend/src/test/renderWithProviders.tsx"]
    n4["frontend/src/types/gantt.ts"]
    n5["frontend/src/utils/formatDate.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n0 --> n5
    n1 --> n4
    n1 --> n5
    n3 --> n2
    click n0 "../modules/GanttChart.test.md"
    click n1 "../modules/GanttChart.md"
    click n2 "../modules/i18n.md"
    click n3 "../modules/renderWithProviders.md"
    click n4 "../modules/types_gantt.md"
    click n5 "../modules/formatDate.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [GanttChart](../modules/GanttChart.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_gantt](../modules/types_gantt.md) |
| Outbound | [formatDate](../modules/formatDate.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
