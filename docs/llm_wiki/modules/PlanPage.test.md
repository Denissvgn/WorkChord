# PlanPage.test Module

**Path:** `frontend/src/pages/PlanPage.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/PlanPage.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../features/scope/scopeStore` | `useScopeStore` | — | compiler-dependent |
| `../features/scope/useWorkScope` | `useSetWorkScope` | — | compiler-dependent |
| `../i18n/i18n` | `changeAppLanguage` | — | compiler-dependent |
| `../navigation/LegacyRedirect` | `LegacyRedirect` | — | compiler-dependent |
| `../test/pageChrome` | `expectPageChrome` | — | compiler-dependent |
| `../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../types/gantt` | `GanttTask`, `SchedulePreviewResponse` | Declaration | erased |
| `../types/iteration` | `IterationPlanningReadinessSummary`, `PlanCheckpoint` | Declaration | erased |
| `../types/task` | `Task`, `TaskBulkOperationRequest` | Declaration | erased |
| `../types/team` | `TeamMember`, `TeamMemberCreate`, `TeamMemberProfile` | Declaration | erased |
| `./PlanPage` | `PlanPage` | — | compiler-dependent |
| `./PlanPage.tsx?raw` | `planPageSource` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor`, `within` | — | compiler-dependent |
| `react-router-dom` | `Route`, `Routes`, `useLocation`, `useNavigate` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `services`, `planning`, `ITERATION`, `PLAN_ENTRY`, `FIXTURES`, `TITLES`, `IDS`, `BLOCKERS_ENTRY`, `scheduleReady` |
| Module calls | `services = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `planning = hoisted`, `mock`, `beforeEach`, `afterEach`, `describe`, `describe`, `describe`, `scheduleReady = summary`, `describe`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/features/scope/scopeStore.ts"]
    n1["frontend/src/features/scope/useWorkScope.ts"]
    n2["frontend/src/i18n/i18n.ts"]
    n3["frontend/src/navigation/LegacyRedirect.tsx"]
    n4["frontend/src/pages/PlanPage.test.tsx"]
    n5["frontend/src/pages/PlanPage.tsx"]
    n6["frontend/src/test/pageChrome.ts"]
    n7["frontend/src/test/renderWithProviders.tsx"]
    n8["frontend/src/types/gantt.ts"]
    n9["frontend/src/types/iteration.ts"]
    n10["frontend/src/types/task.ts"]
    n11["frontend/src/types/team.ts"]
    n1 --> n0
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
    n5 --> n9
    n7 --> n2
    n8 --> n9
    n8 --> n10
    n9 --> n10
    n10 --> n11
    click n0 "../modules/scopeStore.md"
    click n1 "../modules/useWorkScope.md"
    click n2 "../modules/i18n.md"
    click n3 "../modules/LegacyRedirect.md"
    click n4 "../modules/PlanPage.test.md"
    click n5 "../modules/PlanPage.md"
    click n6 "../modules/pageChrome.md"
    click n7 "../modules/renderWithProviders.md"
    click n8 "../modules/types_gantt.md"
    click n9 "../modules/types_iteration.md"
    click n10 "../modules/types_task.md"
    click n11 "../modules/types_team.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [scopeStore](../modules/scopeStore.md) |
| Outbound | [useWorkScope](../modules/useWorkScope.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [LegacyRedirect](../modules/LegacyRedirect.md) |
| Outbound | [PlanPage](../modules/PlanPage.md) |
| Outbound | [pageChrome](../modules/pageChrome.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_gantt](../modules/types_gantt.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [types_team](../modules/types_team.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
