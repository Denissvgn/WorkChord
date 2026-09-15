# CalendarCreate

**Location:** `backend/app/schemas/calendar.py:10`
**Kind:** Pydantic model
**Bases:** `PlanningInputRevisions`
**Module:** [schemas_calendar](../modules/schemas_calendar.md)

## Description

Schema for creating a calendar.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `timezone` | `WorkingZone` | `timezone` | No | No | `'UTC'` | — | — | — |
| `name` | `str` | `name` | Yes | No | — | min_length=1; max_length=255 | — | — |
| `year` | `int` | `year` | Yes | No | — | ge=2000; le=2100 | — | — |
| `holidays` | `list[str]` | `holidays` | No | No | factory: `list` | — | — | ISO date strings |
| `weekend_days` | `list[int]` | `weekend_days` | No | No | `[5, 6]` | — | — | 0=Mon, 6=Sun |
| `short_days` | `list[str]` | `short_days` | No | No | factory: `list` | — | — | Pre-holiday shortened days |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["CalendarCreate (backend/app/schemas/calendar.py)"]
    n1["PlanningInputRevisions (backend/app/schemas/planning_inputs.py)"]
    n2["create_calendar (backend/app/routers/calendars.py)"]
    n3["backend/app/schemas/__init__.py"]
    n4["CalendarService.create (backend/app/services/calendar_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/schemas_calendar.md"
    click n1 "../modules/planning_inputs.md"
    click n2 "../modules/calendars.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/calendar_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_calendar](../modules/schemas_calendar.md) | 0 | `holidays`, `name`, `short_days`, `timezone`, `weekend_days`, `year` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `PlanningInputRevisions` | [planning_inputs](../modules/planning_inputs.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `create_calendar` | type_reference | [calendars](../modules/calendars.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `CalendarService.create` | type_reference | [calendar_service](../modules/calendar_service.md) | — |
