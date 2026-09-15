# iteration Module

**Path:** `backend/app/schemas/iteration.py`

## Description

Iteration schemas.

## Imports

| Source | Symbols |
|--------|---------|
| `app.schemas.planning_inputs` | `PlanningInputRevisions`, `WorkingZone` |
| `app.schemas.work_metrics` | `WorkMetricSummary` |
| `datetime` | `date` |
| `pydantic` | `BaseModel`, `Field`, `model_validator` |
| `typing` | `Literal`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend"]
    n1["backend/app/schemas/iteration.py"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/schemas_iteration.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `backend` (10) |
| Outbound | `backend` (2) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [IterationCreate](../entities/schemas_iteration_IterationCreate.md) | 12 | `BaseModel` | Schema for creating an iteration. |
| [IterationUpdate](../entities/schemas_iteration_IterationUpdate.md) | 22 | `PlanningInputRevisions` | Schema for updating an iteration. |
| [IterationSeriesStop](../entities/schemas_iteration_IterationSeriesStop.md) | 32 | `BaseModel` | Stop rule for generating a back-to-back iteration series. |
| [IterationSeriesCreate](../entities/schemas_iteration_IterationSeriesCreate.md) | 48 | `BaseModel` | Schema for creating multiple back-to-back iterations. |
| [IterationProjectSummary](../entities/IterationProjectSummary.md) | 59 | `BaseModel` | Compact project identity embedded in iteration responses. |
| [IterationResponse](../entities/IterationResponse.md) | 70 | `BaseModel` | Schema for iteration response. |
| [IterationSeriesResponse](../entities/schemas_iteration_IterationSeriesResponse.md) | 88 | `BaseModel` | Response returned after creating an iteration series. |
| [IterationSummary](../entities/schemas_iteration_IterationSummary.md) | 93 | `WorkMetricSummary` | Summary statistics for an iteration. |
| [IterationPlanningReadinessSummary](../entities/schemas_iteration_IterationPlanningReadinessSummary.md) | 109 | `BaseModel` | Compact planning inputs used by persistent navigation. |
