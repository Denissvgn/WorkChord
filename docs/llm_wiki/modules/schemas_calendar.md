# calendar Module

**Path:** `backend/app/schemas/calendar.py`

## Description

Calendar schemas.

## Imports

| Source | Symbols |
|--------|---------|
| `datetime` | `date` |
| `pydantic` | `BaseModel`, `Field` |
| `typing` | `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/routers/calendars.py"]
    n1["backend/app/schemas/__init__.py"]
    n2["backend/app/schemas/calendar.py"]
    n3["backend/app/services/calendar_service.py"]
    n0 --> n2
    n0 --> n3
    n1 --> n2
    n3 --> n2
    click n0 "../modules/calendars.md"
    click n1 "../modules/schemas___init__.md"
    click n2 "../modules/schemas_calendar.md"
    click n3 "../modules/calendar_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [calendars](../modules/calendars.md) |
| Inbound | [schemas___init__](../modules/schemas___init__.md) |
| Inbound | [calendar_service](../modules/calendar_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [CalendarCreate](../entities/schemas_calendar_CalendarCreate.md) | 8 | `BaseModel` | Schema for creating a calendar. |
| [CalendarUpdate](../entities/schemas_calendar_CalendarUpdate.md) | 17 | `BaseModel` | Schema for updating a calendar. |
| [CalendarResponse](../entities/CalendarResponse.md) | 26 | `BaseModel` | Schema for calendar response. |
| [CalendarImportError](../entities/schemas_calendar_CalendarImportError.md) | 39 | `BaseModel` | One calendar import row that could not be applied. |
| [CalendarImportRequest](../entities/CalendarImportRequest.md) | 45 | `BaseModel` | Request for importing calendar holidays from a public source or CSV text. |
| [CalendarImportResponse](../entities/schemas_calendar_CalendarImportResponse.md) | 53 | `BaseModel` | Summary of imported calendar holidays. |
| [WorkingDaysRequest](../entities/WorkingDaysRequest.md) | 61 | `BaseModel` | Request for calculating working days. |
| [WorkingDaysResponse](../entities/schemas_calendar_WorkingDaysResponse.md) | 67 | `BaseModel` | Response with working days calculation. |
| [HolidayImportRequest](../entities/HolidayImportRequest.md) | 77 | `BaseModel` | Request for importing holidays from external source. |
