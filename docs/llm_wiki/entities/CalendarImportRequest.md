# CalendarImportRequest

**Location:** `backend/app/schemas/calendar.py:45`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_calendar](../modules/schemas_calendar.md)

## Description

Request for importing calendar holidays from a public source or CSV text.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `source` | `str` | `source` | Yes | No | — | — | — | 'public' or 'csv' |
| `country` | `Optional[str]` | `country` | No | Yes | `None` | — | — | Country code for public holidays |
| `year` | `Optional[int]` | `year` | No | Yes | `None` | ge=2000; le=2100 | — | — |
| `csv_text` | `Optional[str]` | `csv_text` | No | Yes | `None` | — | — | CSV text with a date column |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["CalendarImportRequest (backend/app/schemas/calendar.py)"]
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
| [schemas_calendar](../modules/schemas_calendar.md) | 0 | `country`, `csv_text`, `source`, `year` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `import_calendar_holidays` | type_reference | [calendars](../modules/calendars.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `CalendarService.import_holidays` | type_reference | [calendar_service](../modules/calendar_service.md) | — |
