# ProjectUpdate

**Location:** `backend/app/schemas/project.py:131`
**Kind:** Pydantic model
**Bases:** `PlanningInputRevisions`
**Module:** [schemas_project](../modules/schemas_project.md)

## Description

Schema for updating a project.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `timezone` | `WorkingZone \| None` | `timezone` | No | Yes | `None` | — | — | — |
| `name` | `Optional[str]` | `name` | No | Yes | `None` | min_length=1; max_length=255 | — | — |
| `description` | `Optional[str]` | `description` | No | Yes | `None` | — | — | — |
| `status` | `Optional[ProjectStatus]` | `status` | No | Yes | `None` | — | — | — |
| `health` | `Optional[ProjectHealth]` | `health` | No | Yes | `None` | — | — | — |
| `owner_id` | `Optional[int]` | `owner_id` | No | Yes | `None` | — | — | — |
| `owner_profile_id` | `Optional[int]` | `owner_profile_id` | No | Yes | `None` | — | — | — |
| `initiative_id` | `Optional[int]` | `initiative_id` | No | Yes | `None` | — | — | — |
| `start_date` | `Optional[date]` | `start_date` | No | Yes | `None` | — | — | — |
| `target_date` | `Optional[date]` | `target_date` | No | Yes | `None` | — | — | — |
| `completed_at` | `Optional[datetime]` | `completed_at` | No | Yes | `None` | — | — | — |
| `sort_order` | `Optional[int]` | `sort_order` | No | Yes | `None` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ProjectUpdate (backend/app/schemas/project.py)"]
    n1["PlanningInputRevisions (backend/app/schemas/planning_inputs.py)"]
    n2["backend/app/mcp_agent_tools.py"]
    n3["update_project (backend/app/routers/agent_planning.py)"]
    n4["create_project_update (backend/app/routers/projects.py)"]
    n5["list_project_updates (backend/app/routers/projects.py)"]
    n6["update_project (backend/app/routers/projects.py)"]
    n7["backend/app/schemas/__init__.py"]
    n8["AgentPlanningService.update_project (backend/app/services/agent_planning_service.py)"]
    n9["ProjectService._calculate_update_freshness (backend/app/services/project_service.py)"]
    n10["ProjectService.create_project_update (backend/app/services/project_service.py)"]
    n11["ProjectService.get_latest_project_update (backend/app/services/project_service.py)"]
    n12["ProjectService.list_project_updates (backend/app/services/project_service.py)"]
    n13["ProjectService.update (backend/app/services/project_service.py)"]
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
    click n0 "../modules/schemas_project.md"
    click n1 "../modules/planning_inputs.md"
    click n2 "../modules/mcp_agent_tools.md"
    click n3 "../modules/routers_agent_planning.md"
    click n4 "../modules/projects.md"
    click n5 "../modules/projects.md"
    click n6 "../modules/projects.md"
    click n7 "../modules/schemas___init__.md"
    click n8 "../modules/agent_planning_service.md"
    click n9 "../modules/project_service.md"
    click n10 "../modules/project_service.md"
    click n11 "../modules/project_service.md"
    click n12 "../modules/project_service.md"
    click n13 "../modules/project_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_project](../modules/schemas_project.md) | 0 | `completed_at`, `description`, `health`, `initiative_id`, `name`, `owner_id`, `owner_profile_id`, `sort_order`, `start_date`, `status`, `target_date`, `timezone` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `PlanningInputRevisions` | [planning_inputs](../modules/planning_inputs.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `update_project` | type_reference | [routers_agent_planning](../modules/routers_agent_planning.md) | — |
| `create_project_update` | type_reference | [projects](../modules/projects.md) | — |
| `list_project_updates` | type_reference | [projects](../modules/projects.md) | — |
| `update_project` | type_reference | [projects](../modules/projects.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `AgentPlanningService.update_project` | type_reference | [agent_planning_service](../modules/agent_planning_service.md) | — |
| `ProjectService._calculate_update_freshness` | type_reference | [project_service](../modules/project_service.md) | — |
| `ProjectService.create_project_update` | type_reference | [project_service](../modules/project_service.md) | — |
| `ProjectService.get_latest_project_update` | type_reference | [project_service](../modules/project_service.md) | — |
| `ProjectService.list_project_updates` | type_reference | [project_service](../modules/project_service.md) | — |
| `ProjectService.update` | type_reference | [project_service](../modules/project_service.md) | — |
