# AnnualCalendars

**Location:** `backend/app/services/calendar_rules.py:63`
**Kind:** Class
**Bases:** —
**Module:** [calendar_rules](../modules/calendar_rules.md)

## Description

A primary calendar and explicitly selected years in the owner's local time zone.

An annual selection belongs to one iteration or profile. The lookup uses the calendar explicitly assigned to the date's year. Replacement checks compare the selected record identity and its actual rules.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(primary: Calendar, additional = ())` | — | — |
| `for_iteration` | `(iteration)` | `@classmethod` | — |
| `missing_years` | `(start: date, end: date) -> list[int]` | — | — |
| `signature` | `() -> list[dict]` | — | Stable JSON-native inputs for both planning and routing evidence hashes. |
| `replaced_years` | `(updated) -> set[int]` | — | — |
| `hours` | `(day: date) -> float \| None` | — | — |
| `dated_rules` | `(start: date, end: date)` | — | — |
| `period_totals` | `(start: date, end: date)` | — | — |
| `working_dates` | `(start: date, end: date) -> list[date]` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AnnualCalendars (backend/app/services/calendar_rules.py)"]
    n1["backend/app/mcp_agent_tools.py"]
    n2["get_working_days (backend/app/routers/calendars.py)"]
    n3["backend/app/routers/gantt.py"]
    n4["backend/app/services/agent_planning_service.py"]
    n5["AgentRoutingService._capacity_inputs (backend/app/services/agent_routing_service.py)"]
    n6["AnnualCalendars.for_iteration (backend/app/services/calendar_rules.py)"]
    n7["reserve_iteration_annuals (backend/app/services/calendar_rules.py)"]
    n8["CalendarService.calculate_working_days (backend/app/services/calendar_service.py)"]
    n9["CalendarService.get_working_dates (backend/app/services/calendar_service.py)"]
    n10["CapacityService._projection (backend/app/services/capacity_service.py)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    click n0 "../modules/calendar_rules.md"
    click n1 "../modules/mcp_agent_tools.md"
    click n2 "../modules/calendars.md"
    click n3 "../modules/routers_gantt.md"
    click n4 "../modules/agent_planning_service.md"
    click n5 "../modules/agent_routing_service.md"
    click n6 "../modules/calendar_rules.md"
    click n7 "../modules/calendar_rules.md"
    click n8 "../modules/calendar_service.md"
    click n9 "../modules/calendar_service.md"
    click n10 "../modules/capacity_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [calendar_rules](../modules/calendar_rules.md) | 9 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `get_working_days` | call | [calendars](../modules/calendars.md) | 1 |
| `gantt` | import | [routers_gantt](../modules/routers_gantt.md) | — |
| `agent_planning_service` | import | [agent_planning_service](../modules/agent_planning_service.md) | — |
| `AgentRoutingService._capacity_inputs` | call | [agent_routing_service](../modules/agent_routing_service.md) | 1 |
| `AnnualCalendars.for_iteration` | call | [calendar_rules](../modules/calendar_rules.md) | 1 |
| `reserve_iteration_annuals` | call | [calendar_rules](../modules/calendar_rules.md) | 1 |
| `CalendarService.calculate_working_days` | call | [calendar_service](../modules/calendar_service.md) | 1 |
| `CalendarService.calculate_working_days` | type_reference | [calendar_service](../modules/calendar_service.md) | — |
| `CalendarService.get_working_dates` | call | [calendar_service](../modules/calendar_service.md) | 1 |
| `CalendarService.get_working_dates` | type_reference | [calendar_service](../modules/calendar_service.md) | — |
| `CapacityService._projection` | call | [capacity_service](../modules/capacity_service.md) | 1 |

> References: showing 12 of 17 logical references; 5 omitted by the 12-row generated summary limit.
