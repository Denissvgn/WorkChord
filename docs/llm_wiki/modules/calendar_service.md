# calendar_service Module

**Path:** `backend/app/services/calendar_service.py`

## Description

Calendar service with business logic.

Creation persists submitted shortened working days along with the declared zone, nominal hours, holidays and weekends. Existing capacity arithmetic applies the one-hour reduction once on working days; holidays, weekends and canonical person absences retain precedence.

Nominal-workday edits use the same task-unit refresh helper as iteration calendar reassignment, within the existing planning-input transaction.

## Imports

| Source | Symbols |
|--------|---------|
| `app.commands` | `commit_or_flush`, `schedule_input_command` |
| `app.models.calendar` | `Calendar` |
| `app.models.iteration` | `Iteration` |
| `app.schemas.calendar` | `CalendarCreate`, `CalendarImportError`, `CalendarImportRequest`, `CalendarImportResponse`, `CalendarUpdate`, `WorkingDaysResponse` |
| `collections.abc` | `Iterable` |
| `csv` | `csv` |
| `datetime` | `date`, `timedelta` |
| `io` | `StringIO` |
| `sqlalchemy` | `func`, `select` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `typing` | `Sequence` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/calendar_service.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/calendar_service.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (8) |
| Outbound | `backend` (4) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [CalendarService](../entities/CalendarService.md) | 64 | — | Service for calendar operations. |
