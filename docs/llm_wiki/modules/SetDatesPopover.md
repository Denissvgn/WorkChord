# SetDatesPopover Module

**Path:** `frontend/src/components/projects/SetDatesPopover.tsx`

## Description

_Auto-generated from `frontend/src/components/projects/SetDatesPopover.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/mutationFeedback` | `MutationFeedbackMeta` | Specifier | compiler-dependent |
| `../../features/mutationFeedback` | `feedbackMessage` | — | compiler-dependent |
| `../../services/planningInputService` | `ObservedPlanningInput` | Declaration | erased |
| `../../services/projectService` | `projectService` | — | compiler-dependent |
| `../../types/project` | `Project` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage`, `getApiErrorStatus` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../planning/PlanningInputBoundary` | `PlanningInputBoundary` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQueryClient` | — | compiler-dependent |
| `date-fns` | `addDays`, `format` | — | compiler-dependent |
| `lucide-react` | `CalendarDays` | — | compiler-dependent |
| `react` | `ReactNode` | Declaration | erased |
| `react` | `useCallback`, `useEffect`, `useId`, `useLayoutEffect`, `useRef`, `useState` | — | compiler-dependent |
| `react-dom` | `createPortal` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `SetDatesPopover` |
| Constants | `PANEL_WIDTH`, `GAP`, `EDGE`, `DEFAULT_SPAN_DAYS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/planning/PlanningInputBoundary.tsx"]
    n2["frontend/src/components/projects/RoadmapView.tsx"]
    n3["frontend/src/components/projects/SetDatesPopover.tsx"]
    n4["frontend/src/features/mutationFeedback.ts"]
    n5["frontend/src/services/planningInputService.ts"]
    n6["frontend/src/services/projectService.ts"]
    n7["frontend/src/types/project.ts"]
    n8["frontend/src/utils/apiError.ts"]
    n1 --> n0
    n1 --> n5
    n2 --> n0
    n2 --> n3
    n2 --> n6
    n2 --> n7
    n3 --> n0
    n3 --> n1
    n3 --> n4
    n3 --> n5
    n3 --> n6
    n3 --> n7
    n3 --> n8
    n6 --> n5
    n6 --> n7
    click n0 "../modules/Button.md"
    click n1 "../modules/PlanningInputBoundary.md"
    click n2 "../modules/RoadmapView.md"
    click n3 "../modules/SetDatesPopover.md"
    click n4 "../modules/mutationFeedback.md"
    click n5 "../modules/planningInputService.md"
    click n6 "../modules/projectService.md"
    click n7 "../modules/types_project.md"
    click n8 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [RoadmapView](../modules/RoadmapView.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [PlanningInputBoundary](../modules/PlanningInputBoundary.md) |
| Outbound | [mutationFeedback](../modules/mutationFeedback.md) |
| Outbound | [planningInputService](../modules/planningInputService.md) |
| Outbound | [projectService](../modules/projectService.md) |
| Outbound | [types_project](../modules/types_project.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 6 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ProposedDates](../entities/ProposedDates.md) | Type alias | 25 | `{ start: string; target: string }` | Dates to start from instead of today and four weeks on, as `yyyy-MM-dd`. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `SetDatesPopover` | `({ project, proposed }: { project: Project; proposed?: ProposedDates })` | — | "Set dates" for a project that has none, edited in place: a small popover |
