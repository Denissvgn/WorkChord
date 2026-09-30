# CalendarImportResponse

**Location:** `backend/app/schemas/calendar.py:64`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_calendar](../modules/schemas_calendar.md)

## Description

Summary of imported calendar holidays.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `calendar` | `CalendarResponse` | `calendar` | Yes | No | — | — | — | — |
| `imported_count` | `int` | `imported_count` | Yes | No | — | — | — | — |
| `skipped_count` | `int` | `skipped_count` | Yes | No | — | — | — | — |
| `errors` | `list[CalendarImportError]` | `errors` | No | No | factory: `list` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["CalendarImportResponse (backend/app/schemas/calendar.py)"]
    n1["BaseModel"]
    n2["import_calendar_holidays (backend/app/routers/calendars.py)"]
    n3["backend/app/schemas/__init__.py"]
    n4["CalendarService.import_holidays (backend/app/services/calendar_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_calendar.md"
    click n2 "../modules/calendars.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/calendar_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_calendar](../modules/schemas_calendar.md) | 0 | `calendar`, `errors`, `imported_count`, `skipped_count` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `import_calendar_holidays` | type_reference | [calendars](../modules/calendars.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `CalendarService.import_holidays` | call | [calendar_service](../modules/calendar_service.md) | 1 |
| `CalendarService.import_holidays` | type_reference | [calendar_service](../modules/calendar_service.md) | — |
