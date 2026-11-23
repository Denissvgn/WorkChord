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
| `nominal_day_hours` | `float` | `nominal_day_hours` | No | No | `8` | gt=0; le=24; allow_inf_nan=False | — | — |
| `name` | `str` | `name` | Yes | No | — | min_length=1; max_length=255 | — | — |
| `year` | `int` | `year` | Yes | No | — | ge=2000; le=2100 | — | — |
| `holidays` | `list[str]` | `holidays` | No | No | factory: `list` | — | — | ISO date strings |
| `weekend_days` | `list[int]` | `weekend_days` | No | No | `[5, 6]` | — | — | 0=Mon, 6=Sun |
| `short_days` | `list[str]` | `short_days` | No | No | factory: `list` | — | — | Pre-holiday shortened days |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["CalendarCreate (backend/app/schemas/calendar.py)"]
    n1["PlanningInputRevisions (backend/app/schemas/planning_inputs.py)"]
    n2["create_calendar (backend/app/routers/calendars.py)"]
    n3["backend/app/schemas/__init__.py"]
    n4["CalendarService.create (backend/app/services/calendar_service.py)"]
    n5["calendars (backend/tests/test_annual_calendar_coverage.py)"]
    n6["test_hidden_person_protects_shared_master_without_leaking_their_identity (backend/tests/test_annual_calendar_coverage.py)"]
    n7["test_interior_year_and_snapshot_use_the_explicit_owner (backend/tests/test_annual_calendar_coverage.py)"]
    n8["test_invalid_annual_bindings_and_reverse_dependencies (backend/tests/test_annual_calendar_coverage.py)"]
    n9["test_person_primary_change_preserves_the_ordinary_reservation (backend/tests/test_annual_calendar_coverage.py)"]
    n10["test_replacing_issued_annual_rules_is_scoped_to_the_affected_tasks (backend/tests/test_annual_calendar_coverage.py)"]
    n11["test_empty_scope_remains_valid_for_unused_input_in_strict_mode (backend/tests/test_planning_input_context.py)"]
    n12["test_supplied_empty_scope_detects_new_allocation_in_compatibility_mode (backend/tests/test_planning_input_context.py)"]
    n13["test_created_short_days_apply_once_to_fractional_shared_capacity (backend/tests/test_profile_capacity.py)"]
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
    n12 --> n0
    n13 --> n0
    click n0 "../modules/schemas_calendar.md"
    click n1 "../modules/planning_inputs.md"
    click n2 "../modules/calendars.md"
    click n3 "../modules/schemas___init__.md"
    click n4 "../modules/calendar_service.md"
    click n5 "../modules/test_annual_calendar_coverage.md"
    click n6 "../modules/test_annual_calendar_coverage.md"
    click n7 "../modules/test_annual_calendar_coverage.md"
    click n8 "../modules/test_annual_calendar_coverage.md"
    click n9 "../modules/test_annual_calendar_coverage.md"
    click n10 "../modules/test_annual_calendar_coverage.md"
    click n11 "../modules/test_planning_input_context.md"
    click n12 "../modules/test_planning_input_context.md"
    click n13 "../modules/test_profile_capacity.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_calendar](../modules/schemas_calendar.md) | 0 | `holidays`, `name`, `nominal_day_hours`, `short_days`, `timezone`, `weekend_days`, `year` |

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
| `calendars` | call | [test_annual_calendar_coverage](../modules/test_annual_calendar_coverage.md) | 2 |
| `test_hidden_person_protects_shared_master_without_leaking_their_identity` | call | [test_annual_calendar_coverage](../modules/test_annual_calendar_coverage.md) | 1 |
| `test_interior_year_and_snapshot_use_the_explicit_owner` | call | [test_annual_calendar_coverage](../modules/test_annual_calendar_coverage.md) | 1 |
| `test_invalid_annual_bindings_and_reverse_dependencies` | call | [test_annual_calendar_coverage](../modules/test_annual_calendar_coverage.md) | 2 |
| `test_person_primary_change_preserves_the_ordinary_reservation` | call | [test_annual_calendar_coverage](../modules/test_annual_calendar_coverage.md) | 1 |
| `test_replacing_issued_annual_rules_is_scoped_to_the_affected_tasks` | call | [test_annual_calendar_coverage](../modules/test_annual_calendar_coverage.md) | 1 |
| `test_empty_scope_remains_valid_for_unused_input_in_strict_mode` | call | [test_planning_input_context](../modules/test_planning_input_context.md) | 1 |
| `test_supplied_empty_scope_detects_new_allocation_in_compatibility_mode` | call | [test_planning_input_context](../modules/test_planning_input_context.md) | 1 |
| `test_created_short_days_apply_once_to_fractional_shared_capacity` | call | [test_profile_capacity](../modules/test_profile_capacity.md) | 1 |
