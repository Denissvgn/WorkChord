# calendar_rules Module

**Path:** `backend/app/services/calendar_rules.py`

## Description

Resolve local working dates from the annual records explicitly selected by an owner.

Each owner selects one calendar for each covered year in the primary calendar's local time zone. Each dated lookup uses indexed weekends, holidays and shortened-day rules. Cumulative hours and working-day counts let many commitments share one calculation per calendar year. Missing or ambiguous annual rules leave the date uncovered.

## Imports

| Source | Symbols |
|--------|---------|
| `app.commands` | `PlanningConflict` |
| `app.models.calendar` | `Calendar` |
| `app.services.execution_planning_window` | `live_assignments` |
| `app.services.iteration_service` | `IterationService` |
| `datetime` | `date`, `timedelta` |
| `functools` | `cached_property` |
| `math` | `math` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/services/calendar_rules.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/calendar_rules.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (14) |
| Outbound | `backend` (4) |

> All 16 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [YearRules](../entities/YearRules.md) | 21 | — | Indexed working rules for one annual record within a single operation. |
| [AnnualCalendars](../entities/AnnualCalendars.md) | 63 | — | A primary calendar and explicitly selected years in the owner's local time zone. |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `rule_signature` | `(calendar: Calendar) -> tuple` | — | — |
| `task_uses_years` | `(task, years) -> bool` | — | — |
| `issued_coordinates` | `(issued)` | — | — |
| `reserve_iteration_annuals` | *(async)* `(db, iteration_id, data, tasks)` | — | A selection edits planning rules only. Refuse replacing a rule an issued task might still use. |