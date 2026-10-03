# TaskCreate

**Location:** `backend/app/schemas/task.py:38`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_task](../modules/schemas_task.md)

## Description

Schema for creating a task.

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `validate_source_url` | field | source_url | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `expected_revision` | `Optional[int]` | `expected_revision` | No | Yes | `None` | ge=1 | — | — |
| `title` | `str` | `title` | Yes | No | — | max_length=500; min_length=1 | — | — |
| `description` | `Optional[str]` | `description` | No | Yes | `None` | — | — | — |
| `parent_id` | `Optional[int]` | `parent_id` | No | Yes | `None` | — | — | — |
| `priority` | `int` | `priority` | No | No | `5` | ge=1; le=10 | — | — |
| `effort_days` | `Optional[float]` | `effort_days` | No | Yes | `None` | allow_inf_nan=False; ge=0 | — | — |
| `effort_hours` | `Optional[float]` | `effort_hours` | No | Yes | `None` | allow_inf_nan=False; ge=0 | — | — |
| `owner_profile_id` | `Optional[int]` | `owner_profile_id` | No | Yes | `None` | ge=1 | — | — |
| `brief` | `Optional[TaskBrief]` | `brief` | No | Yes | `None` | — | — | — |
| `estimate_provenance` | `Optional[Literal['unknown', 'assumed', 'estimated']]` | `estimate_provenance` | No | Yes | `None` | — | — | — |
| `assignee_id` | `Optional[int]` | `assignee_id` | No | Yes | `None` | — | — | — |
| `project_id` | `Optional[int]` | `project_id` | No | Yes | `None` | — | — | — |
| `milestone_id` | `Optional[int]` | `milestone_id` | No | Yes | `None` | — | — | — |
| `depends_on` | `list[int]` | `depends_on` | No | No | factory: `list` | — | — | Task IDs |
| `is_optional` | `bool` | `is_optional` | No | No | `False` | — | — | — |
| `is_deferred` | `bool` | `is_deferred` | No | No | `False` | — | — | — |
| `tags` | `list[str]` | `tags` | No | No | factory: `list` | — | — | — |
| `sort_order` | `int` | `sort_order` | No | No | `0` | — | — | — |
| `min_start_date` | `Optional[date]` | `min_start_date` | No | Yes | `None` | — | — | — |
| `max_end_date` | `Optional[date]` | `max_end_date` | No | Yes | `None` | — | — | — |
| `external_key` | `Optional[str]` | `external_key` | No | Yes | `None` | max_length=255 | — | — |
| `source` | `Optional[str]` | `source` | No | Yes | `None` | max_length=100 | — | — |
| `source_url` | `Optional[str]` | `source_url` | No | Yes | `None` | max_length=1000 | — | — |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `validate_source_url` | `(value: Optional[str]) -> Optional[str]` | `@field_validator('source_url')`, `@classmethod` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskCreate (backend/app/schemas/task.py)"]
    n1["BaseModel"]
    n2["AgentTaskCreate (backend/app/schemas/agent.py)"]
    n3["backend/app/mcp_agent_tools.py"]
    n4["_import_task_record (backend/app/routers/export.py)"]
    n5["backend/app/routers/snapshots.py"]
    n6["create_backlog_task (backend/app/routers/task_domain.py)"]
    n7["create_subtask (backend/app/routers/tasks.py)"]
    n8["create_task (backend/app/routers/tasks.py)"]
    n9["backend/app/schemas/__init__.py"]
    n10["backend/app/schemas/agent.py"]
    n11["AgentPlanningService.create_task (backend/app/services/agent_planning_service.py)"]
    n12["AgentService.create_task (backend/app/services/agent_service.py)"]
    n13["TaskService.create (backend/app/services/task_service.py)"]
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
    click n0 "../modules/schemas_task.md"
    click n2 "../modules/schemas_agent.md"
    click n3 "../modules/mcp_agent_tools.md"
    click n4 "../modules/export.md"
    click n5 "../modules/snapshots.md"
    click n6 "../modules/routers_task_domain.md"
    click n7 "../modules/tasks.md"
    click n8 "../modules/tasks.md"
    click n9 "../modules/schemas___init__.md"
    click n10 "../modules/schemas_agent.md"
    click n11 "../modules/agent_planning_service.md"
    click n12 "../modules/agent_service.md"
    click n13 "../modules/task_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_task](../modules/schemas_task.md) | 1 | `assignee_id`, `brief`, `depends_on`, `description`, `effort_days`, `effort_hours`, `estimate_provenance`, `expected_revision`, `external_key`, `is_deferred`, `is_optional`, `max_end_date` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
| Subclass | `AgentTaskCreate` | [schemas_agent](../modules/schemas_agent.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mcp_agent_tools` | import | [mcp_agent_tools](../modules/mcp_agent_tools.md) | — |
| `_import_task_record` | call | [export](../modules/export.md) | 1 |
| `snapshots` | import | [snapshots](../modules/snapshots.md) | — |
| `create_backlog_task` | type_reference | [routers_task_domain](../modules/routers_task_domain.md) | — |
| `create_subtask` | type_reference | [tasks](../modules/tasks.md) | — |
| `create_task` | type_reference | [tasks](../modules/tasks.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `agent` | import | [schemas_agent](../modules/schemas_agent.md) | — |
| `AgentPlanningService.create_task` | type_reference | [agent_planning_service](../modules/agent_planning_service.md) | — |
| `AgentService.create_task` | call | [agent_service](../modules/agent_service.md) | 1 |
| `AgentService.create_task` | type_reference | [agent_service](../modules/agent_service.md) | — |
| `TaskService.create` | type_reference | [task_service](../modules/task_service.md) | — |

> References: showing 12 of 44 logical references; 32 omitted by the 12-row generated summary limit.
