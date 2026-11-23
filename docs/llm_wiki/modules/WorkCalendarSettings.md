# WorkCalendarSettings Module

**Path:** `frontend/src/components/settings/WorkCalendarSettings.tsx`

## Description

Settings hosts work-calendar editing. The selected calendar and draft generation bind delayed reads and saves to the intended calendar. Unsaved changes to the year, weekend pattern and day marks remain together until the user saves or discards them.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Select` | `Select` | — | compiler-dependent |
| `../../features/usePlanningObservation` | `usePlanningObservation` | — | compiler-dependent |
| `../../i18n/dateLocale` | `dateFnsLocale` | — | compiler-dependent |
| `../../services/calendarService` | `calendarService` | — | compiler-dependent |
| `../../services/planningInputService` | `planningInputService` | — | compiler-dependent |
| `../../types/calendar` | `Calendar`, `CalendarCreate`, `CalendarUpdate` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../calendar/InteractiveCalendar` | `CalendarPeriodNavigator`, `InteractiveCalendar` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/Input` | `Input` | — | compiler-dependent |
| `../common/Modal` | `Modal` | — | compiler-dependent |
| `../common/UnsavedLeaveGuard` | `UnsavedLeaveGuard` | — | compiler-dependent |
| `../common/buttonStyles` | `buttonClassName` | — | compiler-dependent |
| `../common/useConfirmDialog` | `useConfirmDialog` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `../planning/PlanningWorkbenchFrame` | `PlanningWorkbenchFrame` | — | compiler-dependent |
| `../ui` | `OverflowMenu` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `date-fns` | `Locale` | Declaration | erased |
| `date-fns` | `eachDayOfInterval`, `format`, `parseISO` | — | compiler-dependent |
| `lucide-react` | `CalendarDays`, `CalendarRange`, `Download`, `Grid`, `List`, `Plus`, `Save`, `Trash2`, `Upload`, `X` | — | compiler-dependent |
| `react` | `ComponentProps` | Declaration | erased |
| `react` | `useEffect`, `useMemo`, `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `useSearchParams` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `DateChip`, `default` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/settings/WorkCalendarSettings.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/WorkCalendarSettings.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (3) |
| Outbound | `frontend` (17) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 6 | 0 |

> All 20 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [CalendarDraft](../entities/CalendarDraft.md) | Interface | 47 | — | — |
| [DateListProps](../entities/DateListProps.md) | Interface | 932 | — | — |
| [DateChipProps](../entities/DateChipProps.md) | Interface | 993 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `DateChip` | `({ dateKey, locale, label, onRemove }: DateChipProps)` | — | — |