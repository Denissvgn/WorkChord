# TeamMemberUpdate

**Location:** `backend/app/schemas/team.py:89`
**Kind:** Pydantic model
**Bases:** `PlanningInputRevisions`
**Module:** [schemas_team](../modules/schemas_team.md)

## Description

Schema for updating a team member.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `name` | `Optional[str]` | `name` | No | Yes | `None` | max_length=255; min_length=1 | — | — |
| `position` | `Optional[str]` | `position` | No | Yes | `None` | max_length=255; min_length=1 | — | — |
| `email` | `Optional[str]` | `email` | No | Yes | `None` | max_length=255 | — | — |
| `profile_id` | `Optional[int]` | `profile_id` | No | Yes | `None` | — | — | — |
| `availability_percent` | `Optional[float]` | `availability_percent` | No | Yes | `None` | ge=0; le=100 | — | — |
| `professionalism_coefficient` | `Optional[float]` | `professionalism_coefficient` | No | Yes | `None` | ge=0.5; le=5.0 | — | — |
| `operational_utilization` | `Optional[float]` | `operational_utilization` | No | Yes | `None` | ge=0; le=100 | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TeamMemberUpdate (backend/app/schemas/team.py)"]
    n1["PlanningInputRevisions (backend/app/schemas/planning_inputs.py)"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["update_team_member (backend/app/routers/agent_planning.py)"]
    n4["update_team_member (backend/app/routers/team.py)"]
    n5["backend/app/schemas/__init__.py"]
    n6["AgentPlanningService.update_team_member (backend/app/services/agent_planning_service.py)"]
    n7["TeamService.update (backend/app/services/team_service.py)"]
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
    click n4 "../modules/routers_team.md"
    click n5 "../modules/schemas___init__.md"
    click n6 "../modules/agent_planning_service.md"
    click n7 "../modules/team_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_team](../modules/schemas_team.md) | 0 | `availability_percent`, `email`, `name`, `operational_utilization`, `position`, `professionalism_coefficient`, `profile_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `PlanningInputRevisions` | [planning_inputs](../modules/planning_inputs.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `update_team_member` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `update_team_member` | type_reference | [routers_team](../modules/routers_team.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `AgentPlanningService.update_team_member` | type_reference | [agent_planning_service](../modules/agent_planning_service.md) | — |
| `TeamService.update` | type_reference | [team_service](../modules/team_service.md) | — |
