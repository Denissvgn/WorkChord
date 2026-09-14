# calendar_service Module

**Path:** `backend/app/services/calendar_service.py`

## Description

Calendar service with business logic.

## Imports

| Source | Symbols |
|--------|---------|
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
    n0["backend/app/models/calendar.py"]
    n1["backend/app/models/iteration.py"]
    n2["backend/app/routers/calendars.py"]
    n3["backend/app/routers/gantt.py"]
    n4["backend/app/schemas/calendar.py"]
    n5["backend/app/services/agent_routing_service.py"]
    n6["backend/app/services/calendar_service.py"]
    n7["backend/app/services/iteration_service.py"]
    n8["backend/app/services/scheduler_service.py"]
    n9["backend/app/services/team_service.py"]
    n10["backend/app/services/upgrade_service.py"]
    n0 --> n1
    n1 --> n0
    n2 --> n4
    n2 --> n6
    n3 --> n6
    n3 --> n7
    n3 --> n8
    n3 --> n9
    n5 --> n1
    n5 --> n6
    n6 --> n0
    n6 --> n1
    n6 --> n4
    n7 --> n1
    n7 --> n6
    n8 --> n1
    n8 --> n6
    n8 --> n9
    n9 --> n1
    n9 --> n6
    n10 --> n6
    click n0 "../modules/models_calendar.md"
    click n1 "../modules/models_iteration.md"
    click n2 "../modules/calendars.md"
    click n3 "../modules/routers_gantt.md"
    click n4 "../modules/schemas_calendar.md"
    click n5 "../modules/agent_routing_service.md"
    click n6 "../modules/calendar_service.md"
    click n7 "../modules/iteration_service.md"
    click n8 "../modules/scheduler_service.md"
    click n9 "../modules/team_service.md"
    click n10 "../modules/upgrade_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [calendars](../modules/calendars.md) |
| Inbound | [routers_gantt](../modules/routers_gantt.md) |
| Inbound | [agent_routing_service](../modules/agent_routing_service.md) |
| Inbound | [iteration_service](../modules/iteration_service.md) |
| Inbound | [scheduler_service](../modules/scheduler_service.md) |
| Inbound | [team_service](../modules/team_service.md) |
| Inbound | [upgrade_service](../modules/upgrade_service.md) |
| Outbound | [models_calendar](../modules/models_calendar.md) |
| Outbound | [models_iteration](../modules/models_iteration.md) |
| Outbound | [schemas_calendar](../modules/schemas_calendar.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [CalendarService](../entities/CalendarService.md) | 62 | — | Service for calendar operations. |
