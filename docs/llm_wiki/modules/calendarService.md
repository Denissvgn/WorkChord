# calendarService Module

**Path:** `frontend/src/services/calendarService.ts`

## Description

_Auto-generated from `frontend/src/services/calendarService.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../types/calendar` | `Calendar`, `CalendarCreate`, `CalendarImportResponse`, `CalendarUpdate`, `WorkingDaysResponse` | Declaration | erased |
| `./api` | `api` | — | compiler-dependent |
| `./planningInputService` | `ObservedRevisions` | Specifier | compiler-dependent |
| `./planningInputService` | `revisionHeaders` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `calendarService` |
| Constants | `calendarService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/iteration/IterationForm.tsx"]
    n1["frontend/src/components/planning/PlanIterationCheckpoint.tsx"]
    n2["frontend/src/components/settings/WorkCalendarSettings.tsx"]
    n3["frontend/src/components/tasks/PersonCapacity.tsx"]
    n4["frontend/src/services/api.ts"]
    n5["frontend/src/services/calendarService.ts"]
    n6["frontend/src/services/planningInputService.ts"]
    n7["frontend/src/types/calendar.ts"]
    n0 --> n5
    n0 --> n6
    n1 --> n5
    n2 --> n5
    n2 --> n6
    n2 --> n7
    n3 --> n4
    n3 --> n5
    n5 --> n4
    n5 --> n6
    n5 --> n7
    n6 --> n4
    click n0 "../modules/IterationForm.md"
    click n1 "../modules/PlanIterationCheckpoint.md"
    click n2 "../modules/WorkCalendarSettings.md"
    click n3 "../modules/PersonCapacity.md"
    click n4 "../modules/api.md"
    click n5 "../modules/calendarService.md"
    click n6 "../modules/planningInputService.md"
    click n7 "../modules/types_calendar.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [IterationForm](../modules/IterationForm.md) |
| Inbound | [PlanIterationCheckpoint](../modules/PlanIterationCheckpoint.md) |
| Inbound | [WorkCalendarSettings](../modules/WorkCalendarSettings.md) |
| Inbound | [PersonCapacity](../modules/PersonCapacity.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [planningInputService](../modules/planningInputService.md) |
| Outbound | [types_calendar](../modules/types_calendar.md) |
