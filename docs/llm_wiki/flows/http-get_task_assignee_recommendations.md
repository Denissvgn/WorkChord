# get_task_assignee_recommendations

**Entry point:** `get_task_assignee_recommendations` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [tasks](../modules/tasks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_task_assignee_recommendations
    participant p1 as service.recommend_for_task
    participant p2 as HTTPException
    p0-->>p1: service.recommend_for_task
    p0-->>p2: HTTPException
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_task_assignee_recommendations"]
    s2["2. service.recommend_for_task"]
    s3["3. HTTPException"]
    s1 -. "service.recommend_for_task(task_id)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s3
    click s1 "../modules/tasks.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_task_assignee_recommendations` | `task_id: int`, `service: Annotated[AssigneeRecommendationService, Depends(get_assignee_recommendation_service)]` | `status` | - | `recommendations` |
| `service.recommend_for_task` | - | - | - | - |
| `HTTPException` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_task_assignee_recommendations | service.recommend_for_task | 313 | `service.recommend_for_task(task_id)` |
| get_task_assignee_recommendations | HTTPException | 315 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_task_assignee_recommendations` | `service.recommend_for_task` | 313 |
| external_call | `get_task_assignee_recommendations` | `HTTPException` | 315 |

## Behavior

This flow starts at `get_task_assignee_recommendations` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
