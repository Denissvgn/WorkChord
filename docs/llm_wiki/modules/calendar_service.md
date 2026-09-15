# calendar_service Module

**Path:** `backend/app/services/calendar_service.py`

## Description

Calendar service with business logic.

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
    n0["backend/app/commands.py"]
    n1["backend/app/models/calendar.py"]
    n2["backend/app/models/iteration.py"]
    n3["backend/app/routers/calendars.py"]
    n4["backend/app/routers/gantt.py"]
    n5["backend/app/schemas/calendar.py"]
    n6["backend/app/services/agent_routing_service.py"]
    n7["backend/app/services/calendar_service.py"]
    n8["backend/app/services/iteration_service.py"]
    n9["backend/app/services/scheduler_service.py"]
    n10["backend/app/services/team_service.py"]
    n11["backend/app/services/upgrade_service.py"]
    n0 --> n2
    n1 --> n2
    n2 --> n1
    n3 --> n5
    n3 --> n7
    n4 --> n0
    n4 --> n7
    n4 --> n8
    n4 --> n9
    n4 --> n10
    n6 --> n0
    n6 --> n2
    n6 --> n7
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n5
    n8 --> n0
    n8 --> n2
    n8 --> n7
    n9 --> n0
    n9 --> n2
    n9 --> n7
    n9 --> n10
    n10 --> n0
    n10 --> n2
    n10 --> n7
    n11 --> n0
    n11 --> n7
    click n0 "../modules/commands.md"
    click n1 "../modules/models_calendar.md"
    click n2 "../modules/models_iteration.md"
    click n3 "../modules/calendars.md"
    click n4 "../modules/routers_gantt.md"
    click n5 "../modules/schemas_calendar.md"
    click n6 "../modules/agent_routing_service.md"
    click n7 "../modules/calendar_service.md"
    click n8 "../modules/iteration_service.md"
    click n9 "../modules/scheduler_service.md"
    click n10 "../modules/team_service.md"
    click n11 "../modules/upgrade_service.md"
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
| Outbound | [commands](../modules/commands.md) |
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
| [CalendarService](../entities/CalendarService.md) | 64 | — | Service for calendar operations. |
