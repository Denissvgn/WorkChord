# Calendar

**Location:** `frontend/src/types/calendar.ts:1`
**Kind:** Class
**Bases:** —
**Module:** [types_calendar](../modules/types_calendar.md)

## Description

_Auto-generated from `Calendar` in `frontend/src/types/calendar.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `timezone` | `string` | No | — | — |
| `nominal_day_hours` | `number` | No | — | — |
| `id` | `number` | Yes | — | — |
| `name` | `string` | Yes | — | — |
| `year` | `number` | Yes | — | — |
| `holidays` | `string[]` | Yes | — | — |
| `weekend_days` | `number[]` | Yes | — | — |
| `short_days` | `string[]` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Calendar (frontend/src/types/calendar.ts)"]
    n1["frontend/src/pages/CalendarPage.tsx"]
    n2["frontend/src/services/calendarService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_calendar.md"
    click n1 "../modules/CalendarPage.md"
    click n2 "../modules/calendarService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_calendar](../modules/types_calendar.md) | 0 | `holidays`, `id`, `name`, `nominal_day_hours`, `short_days`, `timezone`, `weekend_days`, `year` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `CalendarPage` | import | [CalendarPage](../modules/CalendarPage.md) | — |
| `calendarService` | import | [calendarService](../modules/calendarService.md) | — |
