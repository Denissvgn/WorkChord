# TasksPage.pipeline.test Module

**Path:** `frontend/src/pages/TasksPage.pipeline.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/TasksPage.pipeline.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/layout/ScopeBar` | `ScopeBar` | — | compiler-dependent |
| `../features/scope/scopeStore` | `useScopeStore` | — | compiler-dependent |
| `../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../navigation/LegacyRedirect` | `LegacyRedirect` | — | compiler-dependent |
| `../test/pageChrome` | `expectPageChrome` | — | compiler-dependent |
| `../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../types/agent` | `AgentPipeline` | Declaration | erased |
| `../types/task` | `Task` | Declaration | erased |
| `./TasksPage` | `TasksPage` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor`, `within` | — | compiler-dependent |
| `react-router-dom` | `Route`, `Routes`, `useLocation` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |
| Unresolved `dynamic-import` | — (line 231; deferred) | — | unclassified |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `api`, `access`, `stages`, `backlogTasks` |
| Module calls | `api = hoisted`, `access = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/layout/ScopeBar.tsx"]
    n1["frontend/src/features/scope/scopeStore.ts"]
    n2["frontend/src/i18n/i18n.ts"]
    n3["frontend/src/navigation/LegacyRedirect.tsx"]
    n4["frontend/src/pages/TasksPage.pipeline.test.tsx"]
    n5["frontend/src/pages/TasksPage.tsx"]
    n6["frontend/src/test/pageChrome.ts"]
    n7["frontend/src/test/renderWithProviders.tsx"]
    n8["frontend/src/types/agent.ts"]
    n9["frontend/src/types/task.ts"]
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n4 --> n8
    n4 --> n9
    n5 --> n9
    n7 --> n2
    n8 --> n9
    click n0 "../modules/ScopeBar.md"
    click n1 "../modules/scopeStore.md"
    click n2 "../modules/i18n.md"
    click n3 "../modules/LegacyRedirect.md"
    click n4 "../modules/TasksPage.pipeline.test.md"
    click n5 "../modules/TasksPage.md"
    click n6 "../modules/pageChrome.md"
    click n7 "../modules/renderWithProviders.md"
    click n8 "../modules/types_agent.md"
    click n9 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [ScopeBar](../modules/ScopeBar.md) |
| Outbound | [scopeStore](../modules/scopeStore.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [LegacyRedirect](../modules/LegacyRedirect.md) |
| Outbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [pageChrome](../modules/pageChrome.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_agent](../modules/types_agent.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
