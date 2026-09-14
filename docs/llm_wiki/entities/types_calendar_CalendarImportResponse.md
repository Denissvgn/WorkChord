# CalendarImportResponse

**Location:** `frontend/src/types/calendar.ts:38`
**Kind:** Class
**Bases:** —
**Module:** [types_calendar](../modules/types_calendar.md)

## Description

_Auto-generated from `CalendarImportResponse` in `frontend/src/types/calendar.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `calendar` | `Calendar` | *required* | — |
| `imported_count` | `number` | *required* | — |
| `skipped_count` | `number` | *required* | — |
| `errors` | `CalendarImportError[]` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["CalendarImportResponse (frontend/src/types/calendar.ts)"]
    n1["frontend/src/services/calendarService.ts"]
    n1 --> n0
    click n0 "../modules/types_calendar.md"
    click n1 "../modules/calendarService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_calendar](../modules/types_calendar.md) | 0 | `calendar`, `errors`, `imported_count`, `skipped_count` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `calendarService` | import | [calendarService](../modules/calendarService.md) | — |
