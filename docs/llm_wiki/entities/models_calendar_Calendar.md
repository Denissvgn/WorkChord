# Calendar

**Location:** `backend/app/models/calendar.py:14`
**Kind:** Class
**Bases:** `Base`
**Module:** [models_calendar](../modules/models_calendar.md)

## Description

Production calendar model.

Stores holidays and weekend days configuration for a year.

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `id` | `Mapped[int]` | `mapped_column(Integer, primary_key=True, autoincrement=True)` | — |
| `name` | `Mapped[str]` | `mapped_column(String(255), nullable=False)` | — |
| `timezone` | `Mapped[str]` | `mapped_column(String(64), default='UTC', server_default='UTC', nullable=False)` | — |
| `nominal_day_hours` | `Mapped[float]` | `mapped_column(Float, default=8.0, server_default='8', nullable=False)` | — |
| `year` | `Mapped[int]` | `mapped_column(Integer, nullable=False)` | — |
| `holidays` | `Mapped[list[str]]` | `mapped_column(JSON, default=list)` | — |
| `weekend_days` | `Mapped[list[int]]` | `mapped_column(JSON, default=[5, 6])` | — |
| `short_days` | `Mapped[list[str]]` | `mapped_column(JSON, default=list)` | — |
| `iterations` | `Mapped[list['Iteration']]` | `relationship('Iteration', back_populates='calendar', cascade='all, delete-orphan')` | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `get_holidays_as_dates` | `() -> list[date]` | — | Convert holiday strings to date objects. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Calendar (backend/app/models/calendar.py)"]
    n1["Base (backend/app/database.py)"]
    n2["backend/app/models/__init__.py"]
    n3["backend/app/models/iteration.py"]
    n4["backend/app/services/agent_planning_service.py"]
    n5["CalendarService._parse_holiday_csv (backend/app/services/calendar_service.py)"]
    n6["CalendarService.calculate_working_days (backend/app/services/calendar_service.py)"]
    n7["CalendarService.create (backend/app/services/calendar_service.py)"]
    n8["CalendarService.get_all (backend/app/services/calendar_service.py)"]
    n9["CalendarService.get_by_id (backend/app/services/calendar_service.py)"]
    n10["CalendarService.get_or_create_default (backend/app/services/calendar_service.py)"]
    n11["CalendarService.get_working_dates (backend/app/services/calendar_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    n11 --> n0
    click n0 "../modules/models_calendar.md"
    click n1 "../modules/app_database.md"
    click n2 "../modules/models___init__.md"
    click n3 "../modules/models_iteration.md"
    click n4 "../modules/agent_planning_service.md"
    click n5 "../modules/calendar_service.md"
    click n6 "../modules/calendar_service.md"
    click n7 "../modules/calendar_service.md"
    click n8 "../modules/calendar_service.md"
    click n9 "../modules/calendar_service.md"
    click n10 "../modules/calendar_service.md"
    click n11 "../modules/calendar_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [models_calendar](../modules/models_calendar.md) | 1 | `holidays`, `id`, `iterations`, `name`, `nominal_day_hours`, `short_days`, `timezone`, `weekend_days`, `year` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Base` | [app_database](../modules/app_database.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `__init__` | import | [models___init__](../modules/models___init__.md) | — |
| `iteration` | import | [models_iteration](../modules/models_iteration.md) | — |
| `agent_planning_service` | import | [agent_planning_service](../modules/agent_planning_service.md) | — |
| `CalendarService._parse_holiday_csv` | type_reference | [calendar_service](../modules/calendar_service.md) | — |
| `CalendarService.calculate_working_days` | type_reference | [calendar_service](../modules/calendar_service.md) | — |
| `CalendarService.create` | call | [calendar_service](../modules/calendar_service.md) | 1 |
| `CalendarService.create` | type_reference | [calendar_service](../modules/calendar_service.md) | — |
| `CalendarService.get_all` | type_reference | [calendar_service](../modules/calendar_service.md) | — |
| `CalendarService.get_by_id` | type_reference | [calendar_service](../modules/calendar_service.md) | — |
| `CalendarService.get_or_create_default` | call | [calendar_service](../modules/calendar_service.md) | 1 |
| `CalendarService.get_or_create_default` | type_reference | [calendar_service](../modules/calendar_service.md) | — |
| `CalendarService.get_working_dates` | type_reference | [calendar_service](../modules/calendar_service.md) | — |

> References: showing 12 of 32 logical references; 20 omitted by the 12-row generated summary limit.
