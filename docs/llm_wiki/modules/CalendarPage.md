# CalendarPage Module

**Path:** `frontend/src/pages/CalendarPage.tsx`

## Description

Calendar operations freeze controls while pending, bind delayed completion to the active resource and draft generation, and recheck resource identity after asynchronous CSV reads.

Calendar reads and writes retain resource and draft generation boundaries. Pending reads freeze editable controls; every write invalidates older CSV reads, and explicit reload only applies to the observed resource/generation.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/calendar/InteractiveCalendar` | `CalendarPeriodNavigator`, `InteractiveCalendar` | — | compiler-dependent |
| `../components/common/Button` | `Button` | — | compiler-dependent |
| `../components/common/Input` | `Input` | — | compiler-dependent |
| `../components/common/useConfirmDialog` | `useConfirmDialog` | — | compiler-dependent |
| `../components/feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `../components/planning/PlanningWorkbenchFrame` | `PlanningWorkbenchFrame` | — | compiler-dependent |
| `../components/team/VacationCsvImport` | `VacationCsvImport` | — | compiler-dependent |
| `../components/ui` | `OverflowMenu` | — | compiler-dependent |
| `../features/usePlanningObservation` | `usePlanningObservation` | — | compiler-dependent |
| `../i18n/dateLocale` | `dateFnsLocale` | — | compiler-dependent |
| `../services/calendarService` | `calendarService` | — | compiler-dependent |
| `../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../services/planningInputService` | `planningInputService` | — | compiler-dependent |
| `../services/teamService` | `teamService` | — | compiler-dependent |
| `../store/iterationStore` | `useIterationStore`, `pickDefaultIteration` | — | compiler-dependent |
| `../types/calendar` | `Calendar`, `CalendarCreate`, `CalendarUpdate` | Declaration | erased |
| `../types/team` | `TeamMember`, `Vacation` | Declaration | erased |
| `../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `date-fns` | `Locale` | Declaration | erased |
| `date-fns` | `eachDayOfInterval`, `format`, `parseISO` | — | compiler-dependent |
| `lucide-react` | `CalendarDays`, `CalendarRange`, `Download`, `Grid`, `List`, `Plane`, `Plus`, `Save`, `Trash2`, `Upload`, `X` | — | compiler-dependent |
| `react` | `useEffect`, `useMemo`, `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/pages/CalendarPage.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/CalendarPage.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (1) |
| Outbound | `frontend` (18) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 6 | 0 |

> All 19 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [CalendarDraft](../entities/CalendarDraft.md) | Interface | 39 | — | — |
| [VacationRow](../entities/VacationRow.md) | Interface | 46 | — | — |
| [DateListProps](../entities/DateListProps.md) | Interface | 1147 | — | — |
| [DateChipProps](../entities/DateChipProps.md) | Interface | 1210 | — | — |