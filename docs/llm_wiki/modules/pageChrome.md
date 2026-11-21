# pageChrome Module

**Path:** `frontend/src/test/pageChrome.ts`

## Description

_Auto-generated from `frontend/src/test/pageChrome.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `dom-accessibility-api` | `computeAccessibleName` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `expectPageChrome` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/pages/MyWorkPage.test.tsx"]
    n1["frontend/src/pages/OverviewPage.test.tsx"]
    n2["frontend/src/pages/PlanPage.test.tsx"]
    n3["frontend/src/pages/ProjectsPage.test.tsx"]
    n4["frontend/src/pages/TasksPage.pipeline.test.tsx"]
    n5["frontend/src/pages/TasksPage.toolbar.test.tsx"]
    n6["frontend/src/pages/TeamPage.test.tsx"]
    n7["frontend/src/pages/TriagePage.test.tsx"]
    n8["frontend/src/test/ganttChrome.test.tsx"]
    n9["frontend/src/test/pageChrome.test.tsx"]
    n10["frontend/src/test/pageChrome.ts"]
    n11["frontend/src/test/scopedPageRender.test.tsx"]
    n0 --> n10
    n1 --> n10
    n2 --> n10
    n3 --> n10
    n4 --> n10
    n5 --> n10
    n6 --> n10
    n7 --> n10
    n8 --> n10
    n9 --> n10
    n11 --> n10
    click n0 "../modules/MyWorkPage.test.md"
    click n1 "../modules/OverviewPage.test.md"
    click n2 "../modules/PlanPage.test.md"
    click n3 "../modules/ProjectsPage.test.md"
    click n4 "../modules/TasksPage.pipeline.test.md"
    click n5 "../modules/TasksPage.toolbar.test.md"
    click n6 "../modules/TeamPage.test.md"
    click n7 "../modules/TriagePage.test.md"
    click n8 "../modules/ganttChrome.test.md"
    click n9 "../modules/pageChrome.test.md"
    click n10 "../modules/pageChrome.md"
    click n11 "../modules/scopedPageRender.test.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [MyWorkPage.test](../modules/MyWorkPage.test.md) |
| Inbound | [OverviewPage.test](../modules/OverviewPage.test.md) |
| Inbound | [PlanPage.test](../modules/PlanPage.test.md) |
| Inbound | [ProjectsPage.test](../modules/ProjectsPage.test.md) |
| Inbound | [TasksPage.pipeline.test](../modules/TasksPage.pipeline.test.md) |
| Inbound | [TasksPage.toolbar.test](../modules/TasksPage.toolbar.test.md) |
| Inbound | [TeamPage.test](../modules/TeamPage.test.md) |
| Inbound | [TriagePage.test](../modules/TriagePage.test.md) |
| Inbound | [ganttChrome.test](../modules/ganttChrome.test.md) |
| Inbound | [pageChrome.test](../modules/pageChrome.test.md) |
| Inbound | [scopedPageRender.test](../modules/scopedPageRender.test.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `expectPageChrome` | `(container: HTMLElement, options: { status?: 'migrated' \| 'pending' } = {})` | — | — |
