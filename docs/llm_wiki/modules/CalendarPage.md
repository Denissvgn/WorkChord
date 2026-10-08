# CalendarPage Module

**Path:** `frontend/src/pages/CalendarPage.tsx`

## Description

_Auto-generated from `frontend/src/pages/CalendarPage.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../components/calendar/InteractiveCalendar` | `CalendarPeriodNavigator`, `InteractiveCalendar` |
| `../components/common/Button` | `Button` |
| `../components/common/Input` | `Input` |
| `../components/common/useConfirmDialog` | `useConfirmDialog` |
| `../components/feedback/QueryState` | `QueryErrorState` |
| `../components/planning/PlanningWorkbenchFrame` | `PlanningWorkbenchFrame` |
| `../components/ui` | `OverflowMenu` |
| `../features/usePlanningObservation` | `usePlanningObservation` |
| `../i18n/dateLocale` | `dateFnsLocale` |
| `../services/calendarService` | `calendarService` |
| `../services/iterationService` | `iterationService` |
| `../services/planningInputService` | `planningInputService` |
| `../services/teamService` | `teamService` |
| `../store/iterationStore` | `useIterationStore` |
| `../types/calendar` | `Calendar`, `CalendarCreate`, `CalendarUpdate` |
| `../types/team` | `TeamMember`, `Vacation` |
| `../utils/apiError` | `getApiErrorMessage` |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` |
| `date-fns` | `eachDayOfInterval`, `format`, `parseISO`, `Locale` |
| `lucide-react` | `CalendarDays`, `CalendarRange`, `Download`, `Grid`, `List`, `Plane`, `Plus`, `Save`, `Trash2`, `Upload`, `X` |
| `react` | `useEffect`, `useMemo`, `useState` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `Link` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/pages/CalendarPage.tsx"]
    n1 --> n0
    click n1 "../modules/CalendarPage.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `frontend` (17) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 6 | 0 |

> All 17 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [CalendarDraft](../entities/CalendarDraft.md) | Class | 38 | — | — |
| [VacationRow](../entities/VacationRow.md) | Class | 45 | — | — |
| [DateListProps](../entities/DateListProps.md) | Class | 1105 | — | — |
| [DateChipProps](../entities/DateChipProps.md) | Class | 1168 | — | — |
