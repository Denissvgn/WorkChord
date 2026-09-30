# usePlanningReadiness.test Module

**Path:** `frontend/src/features/planningMasters/usePlanningReadiness.test.tsx`

## Description

_Auto-generated from `frontend/src/features/planningMasters/usePlanningReadiness.test.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../store/iterationStore` | `useIterationStore` |
| `../../types/gantt` | `GanttResponse`, `GanttTask` |
| `../../types/iteration` | `Iteration` |
| `../../types/task` | `Task` |
| `../../types/team` | `TeamMember` |
| `./usePlanningReadiness` | `countPlanningExceptions`, `enrichPlanningTeamMembers`, `hasSavedPlanningSchedule`, `planningLeafTasks`, `usePlanningReadiness` |
| `@tanstack/react-query` | `QueryClient`, `QueryClientProvider` |
| `@testing-library/react` | `act`, `renderHook`, `waitFor` |
| `react` | `ReactNode` |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `serviceMocks`, `iteration`, `member` |
| Module calls | `serviceMocks = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `describe`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/features/planningMasters/usePlanningReadiness.test.tsx"]
    n1["frontend/src/features/planningMasters/usePlanningReadiness.ts"]
    n2["frontend/src/store/iterationStore.ts"]
    n3["frontend/src/types/gantt.ts"]
    n4["frontend/src/types/iteration.ts"]
    n5["frontend/src/types/task.ts"]
    n6["frontend/src/types/team.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n0 --> n5
    n0 --> n6
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n1 --> n6
    n3 --> n4
    n3 --> n5
    n5 --> n6
    click n0 "../modules/usePlanningReadiness.test.md"
    click n1 "../modules/usePlanningReadiness.md"
    click n2 "../modules/iterationStore.md"
    click n3 "../modules/types_gantt.md"
    click n4 "../modules/types_iteration.md"
    click n5 "../modules/types_task.md"
    click n6 "../modules/types_team.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [usePlanningReadiness](../modules/usePlanningReadiness.md) |
| Outbound | [iterationStore](../modules/iterationStore.md) |
| Outbound | [types_gantt](../modules/types_gantt.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [types_team](../modules/types_team.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |
