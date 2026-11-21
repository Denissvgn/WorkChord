# IterationUpdate

**Location:** `backend/app/schemas/iteration.py:23`
**Kind:** Pydantic model
**Bases:** `PlanningInputRevisions`
**Module:** [schemas_iteration](../modules/schemas_iteration.md)

## Description

Schema for updating an iteration.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `name` | `Optional[str]` | `name` | No | Yes | `None` | max_length=255; min_length=1 | — | — |
| `calendar_id` | `Optional[int]` | `calendar_id` | No | Yes | `None` | — | — | — |
| `additional_calendar_ids` | `list[int] \| None` | `additional_calendar_ids` | No | Yes | `None` | max_length=100 | — | — |
| `project_id` | `Optional[int]` | `project_id` | No | Yes | `None` | — | — | — |
| `start_date` | `Optional[date]` | `start_date` | No | Yes | `None` | — | — | — |
| `end_date` | `Optional[date]` | `end_date` | No | Yes | `None` | — | — | — |
| `manager_email` | `Optional[str]` | `manager_email` | No | Yes | `None` | max_length=255 | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["IterationUpdate (backend/app/schemas/iteration.py)"]
    n1["PlanningInputRevisions (backend/app/schemas/planning_inputs.py)"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["update_iteration (backend/app/routers/agent_planning.py)"]
    n4["update_iteration (backend/app/routers/iterations.py)"]
    n5["backend/app/schemas/__init__.py"]
    n6["AgentPlanningService.update_iteration (backend/app/services/agent_planning_service.py)"]
    n7["IterationService.changed_calendar_selection (backend/app/services/iteration_service.py)"]
    n8["IterationService.update (backend/app/services/iteration_service.py)"]
    n9["test_interior_year_and_snapshot_use_the_explicit_owner (backend/tests/test_annual_calendar_coverage.py)"]
    n10["test_invalid_annual_bindings_and_reverse_dependencies (backend/tests/test_annual_calendar_coverage.py)"]
    n11["test_replacing_issued_annual_rules_is_scoped_to_the_affected_tasks (backend/tests/test_annual_calendar_coverage.py)"]
    n12["test_moving_iteration_dates_requires_schedule_recalculation (backend/tests/test_schedule_working_date.py)"]
    n13["test_recalculation_preserves_started_dates_outside_moved_iteration (backend/tests/test_schedule_working_date.py)"]
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
    click n0 "../modules/schemas_iteration.md"
    click n1 "../modules/planning_inputs.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_agent_planning.md"
    click n4 "../modules/iterations.md"
    click n5 "../modules/schemas___init__.md"
    click n6 "../modules/agent_planning_service.md"
    click n7 "../modules/iteration_service.md"
    click n8 "../modules/iteration_service.md"
    click n9 "../modules/test_annual_calendar_coverage.md"
    click n10 "../modules/test_annual_calendar_coverage.md"
    click n11 "../modules/test_annual_calendar_coverage.md"
    click n12 "../modules/test_schedule_working_date.md"
    click n13 "../modules/test_schedule_working_date.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_iteration](../modules/schemas_iteration.md) | 0 | `additional_calendar_ids`, `calendar_id`, `end_date`, `manager_email`, `name`, `project_id`, `start_date` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `PlanningInputRevisions` | [planning_inputs](../modules/planning_inputs.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `update_iteration` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `update_iteration` | type_reference | [iterations](../modules/iterations.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `AgentPlanningService.update_iteration` | type_reference | [agent_planning_service](../modules/agent_planning_service.md) | — |
| `IterationService.changed_calendar_selection` | type_reference | [iteration_service](../modules/iteration_service.md) | — |
| `IterationService.update` | type_reference | [iteration_service](../modules/iteration_service.md) | — |
| `test_interior_year_and_snapshot_use_the_explicit_owner` | call | [test_annual_calendar_coverage](../modules/test_annual_calendar_coverage.md) | 1 |
| `test_invalid_annual_bindings_and_reverse_dependencies` | call | [test_annual_calendar_coverage](../modules/test_annual_calendar_coverage.md) | 1 |
| `test_replacing_issued_annual_rules_is_scoped_to_the_affected_tasks` | call | [test_annual_calendar_coverage](../modules/test_annual_calendar_coverage.md) | 1 |
| `test_moving_iteration_dates_requires_schedule_recalculation` | call | [test_schedule_working_date](../modules/test_schedule_working_date.md) | 1 |
| `test_recalculation_preserves_started_dates_outside_moved_iteration` | call | [test_schedule_working_date](../modules/test_schedule_working_date.md) | 1 |

> References: showing 12 of 13 logical references; 1 omitted by the 12-row generated summary limit.
