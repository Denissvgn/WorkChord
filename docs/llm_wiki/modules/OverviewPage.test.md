# OverviewPage.test Module

**Path:** `frontend/src/pages/OverviewPage.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/OverviewPage.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/layout/CommandMenu` | `CommandMenu` | — | compiler-dependent |
| `../features/firstRun/getStartedVisibility` | `useGetStartedVisibility` | — | compiler-dependent |
| `../features/scope/scopeStore` | `useScopeStore` | — | compiler-dependent |
| `../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../test/pageChrome` | `expectPageChrome` | — | compiler-dependent |
| `../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../types/agent` | `AgentPipeline` | Declaration | erased |
| `../types/iteration` | `Iteration`, `PlanCheckpoint` | Declaration | erased |
| `../types/task` | `Task`, `TaskReference` | Declaration | erased |
| `./OverviewPage` | `OverviewPage` | — | compiler-dependent |
| `./TasksPage` | `TasksPage` | — | compiler-dependent |
| `@testing-library/react` | `act`, `screen`, `waitFor`, `within` | — | compiler-dependent |
| `react-router-dom` | `Route`, `Routes`, `useLocation` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `api`, `access`, `TODAY`, `ITERATIONS`, `ALPHA_TASKS`, `BETA_TASKS`, `PAST_TASKS`, `TASKS_BY_ITERATION`, `STAGES`, `BACKLOG` |
| Module calls | `api = hoisted`, `access = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/layout/CommandMenu.tsx"]
    n1["frontend/src/features/firstRun/getStartedVisibility.ts"]
    n2["frontend/src/features/scope/scopeStore.ts"]
    n3["frontend/src/i18n/i18n.ts"]
    n4["frontend/src/pages/OverviewPage.test.tsx"]
    n5["frontend/src/pages/OverviewPage.tsx"]
    n6["frontend/src/pages/TasksPage.tsx"]
    n7["frontend/src/test/pageChrome.ts"]
    n8["frontend/src/test/renderWithProviders.tsx"]
    n9["frontend/src/types/agent.ts"]
    n10["frontend/src/types/iteration.ts"]
    n11["frontend/src/types/task.ts"]
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n4 --> n8
    n4 --> n9
    n4 --> n10
    n4 --> n11
    n5 --> n10
    n5 --> n11
    n6 --> n11
    n8 --> n3
    n9 --> n11
    click n0 "../modules/CommandMenu.md"
    click n1 "../modules/getStartedVisibility.md"
    click n2 "../modules/scopeStore.md"
    click n3 "../modules/i18n.md"
    click n4 "../modules/OverviewPage.test.md"
    click n5 "../modules/OverviewPage.md"
    click n6 "../modules/TasksPage.md"
    click n7 "../modules/pageChrome.md"
    click n8 "../modules/renderWithProviders.md"
    click n9 "../modules/types_agent.md"
    click n10 "../modules/types_iteration.md"
    click n11 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [CommandMenu](../modules/CommandMenu.md) |
| Outbound | [getStartedVisibility](../modules/getStartedVisibility.md) |
| Outbound | [scopeStore](../modules/scopeStore.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [OverviewPage](../modules/OverviewPage.md) |
| Outbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [pageChrome](../modules/pageChrome.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_agent](../modules/types_agent.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
