# iteration Module

**Path:** `backend/app/schemas/iteration.py`

## Description

Iteration schemas.

## Imports

| Source | Symbols |
|--------|---------|
| `datetime` | `date` |
| `pydantic` | `BaseModel`, `Field`, `model_validator` |
| `typing` | `Literal`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/mcp_agent_tools.py"]
    n1["backend/app/routers/agent_planning.py"]
    n2["backend/app/routers/export.py"]
    n3["backend/app/routers/gantt.py"]
    n4["backend/app/routers/iterations.py"]
    n5["backend/app/routers/projects.py"]
    n6["backend/app/schemas/__init__.py"]
    n7["backend/app/schemas/gantt.py"]
    n8["backend/app/schemas/iteration.py"]
    n9["backend/app/services/agent_planning_service.py"]
    n10["backend/app/services/iteration_service.py"]
    n0 --> n3
    n0 --> n8
    n0 --> n9
    n0 --> n10
    n1 --> n0
    n1 --> n8
    n1 --> n9
    n2 --> n8
    n2 --> n10
    n3 --> n7
    n3 --> n8
    n3 --> n10
    n4 --> n8
    n4 --> n10
    n5 --> n8
    n5 --> n10
    n6 --> n7
    n6 --> n8
    n7 --> n8
    n9 --> n8
    n9 --> n10
    n10 --> n8
    click n0 "../modules/mcp_agent_tools.md"
    click n1 "../modules/routers_agent_planning.md"
    click n2 "../modules/export.md"
    click n3 "../modules/routers_gantt.md"
    click n4 "../modules/iterations.md"
    click n5 "../modules/projects.md"
    click n6 "../modules/schemas___init__.md"
    click n7 "../modules/schemas_gantt.md"
    click n8 "../modules/schemas_iteration.md"
    click n9 "../modules/agent_planning_service.md"
    click n10 "../modules/iteration_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [routers_agent_planning](../modules/routers_agent_planning.md) |
| Inbound | [export](../modules/export.md) |
| Inbound | [routers_gantt](../modules/routers_gantt.md) |
| Inbound | [iterations](../modules/iterations.md) |
| Inbound | [projects](../modules/projects.md) |
| Inbound | [schemas___init__](../modules/schemas___init__.md) |
| Inbound | [schemas_gantt](../modules/schemas_gantt.md) |
| Inbound | [agent_planning_service](../modules/agent_planning_service.md) |
| Inbound | [iteration_service](../modules/iteration_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [IterationCreate](../entities/schemas_iteration_IterationCreate.md) | 8 | `BaseModel` | Schema for creating an iteration. |
| [IterationUpdate](../entities/schemas_iteration_IterationUpdate.md) | 18 | `BaseModel` | Schema for updating an iteration. |
| [IterationSeriesStop](../entities/schemas_iteration_IterationSeriesStop.md) | 28 | `BaseModel` | Stop rule for generating a back-to-back iteration series. |
| [IterationSeriesCreate](../entities/schemas_iteration_IterationSeriesCreate.md) | 44 | `BaseModel` | Schema for creating multiple back-to-back iterations. |
| [IterationProjectSummary](../entities/IterationProjectSummary.md) | 55 | `BaseModel` | Compact project identity embedded in iteration responses. |
| [IterationResponse](../entities/IterationResponse.md) | 66 | `BaseModel` | Schema for iteration response. |
| [IterationSeriesResponse](../entities/schemas_iteration_IterationSeriesResponse.md) | 82 | `BaseModel` | Response returned after creating an iteration series. |
| [IterationSummary](../entities/schemas_iteration_IterationSummary.md) | 87 | `BaseModel` | Summary statistics for an iteration. |
| [IterationPlanningReadinessSummary](../entities/schemas_iteration_IterationPlanningReadinessSummary.md) | 103 | `BaseModel` | Compact planning inputs used by persistent navigation. |
