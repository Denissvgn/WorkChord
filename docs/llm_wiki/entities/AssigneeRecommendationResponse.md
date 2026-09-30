# AssigneeRecommendationResponse

**Location:** `backend/app/schemas/team.py:352`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_team](../modules/schemas_team.md)

## Description

Explainable candidate score for assigning a task or triage item.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `team_member_id` | `int` | `team_member_id` | Yes | No | — | — | — | — |
| `name` | `str` | `name` | Yes | No | — | — | — | — |
| `position` | `str` | `position` | Yes | No | — | — | — | — |
| `profile_id` | `Optional[int]` | `profile_id` | No | Yes | `None` | — | — | — |
| `score` | `float` | `score` | Yes | No | — | — | — | — |
| `confidence` | `float` | `confidence` | Yes | No | — | — | — | — |
| `matched_skills` | `list[str]` | `matched_skills` | No | No | factory: `list` | — | — | — |
| `weakness_matches` | `list[str]` | `weakness_matches` | No | No | factory: `list` | — | — | — |
| `workload_warnings` | `list[str]` | `workload_warnings` | No | No | factory: `list` | — | — | — |
| `rationale` | `str` | `rationale` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AssigneeRecommendationResponse (backend/app/schemas/team.py)"]
    n1["BaseModel"]
    n2["get_task_assignee_recommendations (backend/app/routers/tasks.py)"]
    n3["get_triage_assignee_recommendations (backend/app/routers/triage.py)"]
    n4["backend/app/schemas/__init__.py"]
    n5["backend/app/schemas/task.py"]
    n6["AssigneeRecommendationService._rank (backend/app/services/assignee_recommendation_service.py)"]
    n7["AssigneeRecommendationService._score_candidate (backend/app/services/assignee_recommendation_service.py)"]
    n8["AssigneeRecommendationService.recommend_for_task (backend/app/services/assignee_recommendation_service.py)"]
    n9["AssigneeRecommendationService.recommend_for_triage (backend/app/services/assignee_recommendation_service.py)"]
    n10["TaskBulkOperationService._auto_assignee_for_task (backend/app/services/task_bulk_operation_service.py)"]
    n11["TaskBulkOperationService._build_update (backend/app/services/task_bulk_operation_service.py)"]
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
    click n0 "../modules/schemas_team.md"
    click n2 "../modules/tasks.md"
    click n3 "../modules/routers_triage.md"
    click n4 "../modules/schemas___init__.md"
    click n5 "../modules/schemas_task.md"
    click n6 "../modules/assignee_recommendation_service.md"
    click n7 "../modules/assignee_recommendation_service.md"
    click n8 "../modules/assignee_recommendation_service.md"
    click n9 "../modules/assignee_recommendation_service.md"
    click n10 "../modules/task_bulk_operation_service.md"
    click n11 "../modules/task_bulk_operation_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_team](../modules/schemas_team.md) | 0 | `confidence`, `matched_skills`, `name`, `position`, `profile_id`, `rationale`, `score`, `team_member_id`, `weakness_matches`, `workload_warnings` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_task_assignee_recommendations` | type_reference | [tasks](../modules/tasks.md) | — |
| `get_triage_assignee_recommendations` | type_reference | [routers_triage](../modules/routers_triage.md) | — |
| `__init__` | import | [schemas___init__](../modules/schemas___init__.md) | — |
| `task` | import | [schemas_task](../modules/schemas_task.md) | — |
| `AssigneeRecommendationService._rank` | type_reference | [assignee_recommendation_service](../modules/assignee_recommendation_service.md) | — |
| `AssigneeRecommendationService._score_candidate` | call | [assignee_recommendation_service](../modules/assignee_recommendation_service.md) | 1 |
| `AssigneeRecommendationService._score_candidate` | type_reference | [assignee_recommendation_service](../modules/assignee_recommendation_service.md) | — |
| `AssigneeRecommendationService.recommend_for_task` | type_reference | [assignee_recommendation_service](../modules/assignee_recommendation_service.md) | — |
| `AssigneeRecommendationService.recommend_for_triage` | type_reference | [assignee_recommendation_service](../modules/assignee_recommendation_service.md) | — |
| `TaskBulkOperationService._auto_assignee_for_task` | type_reference | [task_bulk_operation_service](../modules/task_bulk_operation_service.md) | — |
| `TaskBulkOperationService._build_update` | type_reference | [task_bulk_operation_service](../modules/task_bulk_operation_service.md) | — |
