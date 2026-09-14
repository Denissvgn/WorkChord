# WorkingDaysResponse

**Location:** `frontend/src/types/calendar.ts:26`
**Kind:** Class
**Bases:** —
**Module:** [types_calendar](../modules/types_calendar.md)

## Description

_Auto-generated from `WorkingDaysResponse` in `frontend/src/types/calendar.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `total_days` | `number` | *required* | — |
| `working_days` | `number` | *required* | — |
| `holidays` | `string[]` | *required* | — |
| `weekends` | `string[]` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["WorkingDaysResponse (frontend/src/types/calendar.ts)"]
    n1["frontend/src/services/calendarService.ts"]
    n1 --> n0
    click n0 "../modules/types_calendar.md"
    click n1 "../modules/calendarService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_calendar](../modules/types_calendar.md) | 0 | `holidays`, `total_days`, `weekends`, `working_days` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `calendarService` | import | [calendarService](../modules/calendarService.md) | — |
