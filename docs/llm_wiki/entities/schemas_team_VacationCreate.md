# VacationCreate

**Location:** `backend/app/schemas/team.py:28`
**Kind:** Pydantic model
**Bases:** `PlanningInputRevisions`
**Module:** [schemas_team](../modules/schemas_team.md)

## Description

Schema for creating a vacation.

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `validate_date_range` | model | — | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `start_date` | `date` | `start_date` | Yes | No | — | — | — | — |
| `end_date` | `date` | `end_date` | Yes | No | — | — | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `validate_date_range` | `() -> 'VacationCreate'` | `@model_validator(mode='after')` | Reject an inverted vacation period. |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["VacationCreate (backend/app/schemas/team.py)"]
    n1["PlanningInputRevisions (backend/app/schemas/planning_inputs.py)"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["create_vacation (backend/app/routers/agent_planning.py)"]
    n4["_process_import (backend/app/routers/export.py)"]
    n5["_validate_snapshot_task_payloads (backend/app/routers/snapshots.py)"]
    n6["add_vacation (backend/app/routers/team.py)"]
    n7["backend/app/schemas/__init__.py"]
    n8["VacationCreate.validate_date_range (backend/app/schemas/team.py)"]
    n9["AgentPlanningService.create_vacation (backend/app/services/agent_planning_service.py)"]
    n10["TeamService.add_vacation (backend/app/services/team_service.py)"]
    n11["TeamService.import_vacations (backend/app/services/team_service.py)"]
    n12["test_iteration_restore_preserves_current_shared_absence (backend/tests/test_profile_capacity.py)"]
    n13["test_reassigning_allocation_does_not_transfer_private_absence (backend/tests/test_profile_capacity.py)"]
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
    click n0 "../modules/schemas_team.md"
    click n1 "../modules/planning_inputs.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_agent_planning.md"
    click n4 "../modules/export.md"
    click n5 "../modules/snapshots.md"
    click n6 "../modules/routers_team.md"
    click n7 "../modules/schemas___init__.md"
    click n8 "../modules/schemas_team.md"
    click n9 "../modules/agent_planning_service.md"
    click n10 "../modules/team_service.md"
    click n11 "../modules/team_service.md"
    click n12 "../modules/test_profile_capacity.md"
    click n13 "../modules/test_profile_capacity.md"
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
| `create_vacation` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `_process_import` | call | [export](../modules/export.md) | 1 |
| `_validate_snapshot_task_payloads` | call | [snapshots](../modules/snapshots.md) | 1 |
| `add_vacation` | type_reference | [routers_team](../modules/routers_team.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `VacationCreate.validate_date_range` | type_reference | [schemas_team](../modules/schemas_team.md) | — |
| `AgentPlanningService.create_vacation` | type_reference | [agent_planning_service](../modules/agent_planning_service.md) | — |
| `TeamService.add_vacation` | type_reference | [team_service](../modules/team_service.md) | — |
| `TeamService.import_vacations` | call | [team_service](../modules/team_service.md) | 1 |
| `test_iteration_restore_preserves_current_shared_absence` | call | [test_profile_capacity](../modules/test_profile_capacity.md) | 1 |
| `test_reassigning_allocation_does_not_transfer_private_absence` | call | [test_profile_capacity](../modules/test_profile_capacity.md) | 1 |

> References: showing 12 of 13 logical references; 1 omitted by the 12-row generated summary limit.
