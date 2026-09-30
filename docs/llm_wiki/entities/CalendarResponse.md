# CalendarResponse

**Location:** `backend/app/schemas/calendar.py:34`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_calendar](../modules/schemas_calendar.md)

## Description

Schema for calendar response.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `from_attributes` | `True` | config_class |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `timezone` | `str` | `timezone` | No | No | `'UTC'` | — | — | — |
| `nominal_day_hours` | `float` | `nominal_day_hours` | No | No | `8` | — | — | — |
| `id` | `int` | `id` | Yes | No | — | — | — | — |
| `name` | `str` | `name` | Yes | No | — | — | — | — |
| `year` | `int` | `year` | Yes | No | — | — | — | — |
| `holidays` | `list[str]` | `holidays` | Yes | No | — | — | — | — |
| `weekend_days` | `list[int]` | `weekend_days` | Yes | No | — | — | — | — |
| `short_days` | `list[str]` | `short_days` | No | No | `[]` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["CalendarResponse (backend/app/schemas/calendar.py)"]
    n1["BaseModel"]
    n2["create_calendar (backend/app/routers/calendars.py)"]
    n3["get_calendar (backend/app/routers/calendars.py)"]
    n4["get_calendars (backend/app/routers/calendars.py)"]
    n5["update_calendar (backend/app/routers/calendars.py)"]
    n6["backend/app/schemas/__init__.py"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/schemas_calendar.md"
    click n2 "../modules/calendars.md"
    click n3 "../modules/calendars.md"
    click n4 "../modules/calendars.md"
    click n5 "../modules/calendars.md"
    click n6 "../modules/schemas___init__.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_calendar](../modules/schemas_calendar.md) | 0 | `holidays`, `id`, `name`, `nominal_day_hours`, `short_days`, `timezone`, `weekend_days`, `year` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `create_calendar` | type_reference | [calendars](../modules/calendars.md) | — |
| `get_calendar` | type_reference | [calendars](../modules/calendars.md) | — |
| `get_calendars` | type_reference | [calendars](../modules/calendars.md) | — |
| `update_calendar` | type_reference | [calendars](../modules/calendars.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
