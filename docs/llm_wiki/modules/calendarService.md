# calendarService Module

**Path:** `frontend/src/services/calendarService.ts`

## Description

_Auto-generated from `frontend/src/services/calendarService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/calendar` | `Calendar`, `CalendarCreate`, `CalendarImportResponse`, `CalendarUpdate`, `WorkingDaysResponse` |
| `./api` | `api` |
| `./planningInputService` | `revisionHeaders`, `ObservedRevisions` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `calendarService` |
| Constants | `calendarService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/PersonCapacity.tsx"]
    n1["frontend/src/pages/CalendarPage.tsx"]
    n2["frontend/src/services/api.ts"]
    n3["frontend/src/services/calendarService.ts"]
    n4["frontend/src/services/planningInputService.ts"]
    n5["frontend/src/types/calendar.ts"]
    n0 --> n2
    n0 --> n3
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n4 --> n2
    click n0 "../modules/PersonCapacity.md"
    click n1 "../modules/CalendarPage.md"
    click n2 "../modules/api.md"
    click n3 "../modules/calendarService.md"
    click n4 "../modules/planningInputService.md"
    click n5 "../modules/types_calendar.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [PersonCapacity](../modules/PersonCapacity.md) |
| Inbound | [CalendarPage](../modules/CalendarPage.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [planningInputService](../modules/planningInputService.md) |
| Outbound | [types_calendar](../modules/types_calendar.md) |
