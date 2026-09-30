# VacationUpdate

**Location:** `backend/app/schemas/team.py:41`
**Kind:** Pydantic model
**Bases:** `PlanningInputRevisions`
**Module:** [schemas_team](../modules/schemas_team.md)

## Description

Schema for partially updating a vacation period.

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `reject_null_date` | field | start_date, end_date | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `start_date` | `Optional[date]` | `start_date` | No | Yes | `None` | — | — | — |
| `end_date` | `Optional[date]` | `end_date` | No | Yes | `None` | — | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `reject_null_date` | `(value)` | `@field_validator('start_date', 'end_date')`, `@classmethod` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["VacationUpdate (backend/app/schemas/team.py)"]
    n1["PlanningInputRevisions (backend/app/schemas/planning_inputs.py)"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["update_vacation (backend/app/routers/agent_planning.py)"]
    n4["AgentPlanningService.update_vacation (backend/app/services/agent_planning_service.py)"]
    n5["TeamService.update_vacation (backend/app/services/team_service.py)"]
    n6["test_partial_absence_update_cannot_clear_required_dates (backend/tests/test_profile_capacity.py)"]
    n7["test_shared_absence_revisions_legacy_adapter_and_stale_write (backend/tests/test_profile_capacity.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/schemas_team.md"
    click n1 "../modules/planning_inputs.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_agent_planning.md"
    click n4 "../modules/agent_planning_service.md"
    click n5 "../modules/team_service.md"
    click n6 "../modules/test_profile_capacity.md"
    click n7 "../modules/test_profile_capacity.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_team](../modules/schemas_team.md) | 1 | `end_date`, `start_date` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `PlanningInputRevisions` | [planning_inputs](../modules/planning_inputs.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `update_vacation` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `AgentPlanningService.update_vacation` | type_reference | [agent_planning_service](../modules/agent_planning_service.md) | — |
| `TeamService.update_vacation` | type_reference | [team_service](../modules/team_service.md) | — |
| `test_partial_absence_update_cannot_clear_required_dates` | call | [test_profile_capacity](../modules/test_profile_capacity.md) | 2 |
| `test_shared_absence_revisions_legacy_adapter_and_stale_write` | call | [test_profile_capacity](../modules/test_profile_capacity.md) | 1 |
