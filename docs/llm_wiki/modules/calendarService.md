# calendarService Module

**Path:** `frontend/src/services/calendarService.ts`

## Description

_Auto-generated from `frontend/src/services/calendarService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../types/calendar` | `Calendar`, `CalendarCreate`, `CalendarImportResponse`, `CalendarUpdate`, `WorkingDaysResponse` |
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `calendarService` |
| Constants | `calendarService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/pages/CalendarPage.tsx"]
    n1["frontend/src/services/api.ts"]
    n2["frontend/src/services/calendarService.ts"]
    n3["frontend/src/types/calendar.ts"]
    n0 --> n2
    n0 --> n3
    n2 --> n1
    n2 --> n3
    click n0 "../modules/CalendarPage.md"
    click n1 "../modules/api.md"
    click n2 "../modules/calendarService.md"
    click n3 "../modules/types_calendar.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [CalendarPage](../modules/CalendarPage.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [types_calendar](../modules/types_calendar.md) |
