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
| Inbound | `backend` (17) |
| Outbound | `backend` (2) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

> All 19 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [IterationCreate](../entities/schemas_iteration_IterationCreate.md) | 12 | `BaseModel` | Schema for creating an iteration. |
| [IterationUpdate](../entities/schemas_iteration_IterationUpdate.md) | 23 | `PlanningInputRevisions` | Schema for updating an iteration. |
| [IterationSeriesStop](../entities/schemas_iteration_IterationSeriesStop.md) | 34 | `BaseModel` | Stop rule for generating a back-to-back iteration series. |
| [IterationSeriesCreate](../entities/schemas_iteration_IterationSeriesCreate.md) | 50 | `BaseModel` | Schema for creating multiple back-to-back iterations. |
| [IterationProjectSummary](../entities/IterationProjectSummary.md) | 62 | `BaseModel` | Compact project identity embedded in iteration responses. |
| [IterationResponse](../entities/IterationResponse.md) | 73 | `BaseModel` | — |
| [IterationSeriesResponse](../entities/schemas_iteration_IterationSeriesResponse.md) | 94 | `BaseModel` | Response returned after creating an iteration series. |
| [IterationSummary](../entities/schemas_iteration_IterationSummary.md) | 99 | `WorkMetricSummary` | Summary statistics for an iteration. |
| [PlanCheckpoint](../entities/schemas_iteration_PlanCheckpoint.md) | 122 | `BaseModel` | One of the six plan checkpoints, in the order people and the PM work them. |
| [InvertedDependency](../entities/schemas_iteration_InvertedDependency.md) | 130 | `BaseModel` | A saved dependency whose dates start the dependent on or before its prerequisite's last day. |
| [IterationPlanningReadinessSummary](../entities/schemas_iteration_IterationPlanningReadinessSummary.md) | 140 | `BaseModel` | Compact planning inputs used by persistent navigation. |
| [IterationPage](../entities/IterationPage.md) | 168 | `BaseModel` | — |
| [IterationDateMoveRequest](../entities/IterationDateMoveRequest.md) | 176 | `PlanningInputRevisions` | A proposed iteration start, end and calendar to check against shared capacity. |
| [IterationPeriod](../entities/IterationPeriod.md) | 201 | `BaseModel` | An iteration's dates and annual calendars. |
| [DateMoveBooking](../entities/DateMoveBooking.md) | 212 | `BaseModel` | Hours one other iteration books from the same person on one date. |
| [DateMoveShortfall](../entities/DateMoveShortfall.md) | 220 | `BaseModel` | One person and date where the proposed period requests more than the person has. |
| [DateMoveProfile](../entities/DateMoveProfile.md) | 237 | `BaseModel` | How the proposed period fits one person of the iteration team. |
| [IterationDateMovePreview](../entities/IterationDateMovePreview.md) | 249 | `BaseModel` | Shared capacity for a proposed iteration period. Nothing is saved. |
