# get_subtasks

**Entry point:** `get_subtasks` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [iteration_service](../modules/iteration_service.md), [tasks](../modules/tasks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_subtasks
    participant p1 as service.get_by_id
    participant p2 as HTTPException
    participant p3 as IterationService
    participant p4 as iteration_service.get_by_id
    participant p5 as service.task_to_response
    p0-->>p1: service.get_by_id
    p0-->>p2: HTTPException
    p0->>p3: IterationService
    p0-->>p4: iteration_service.get_by_id
    p0-->>p5: service.task_to_response
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_subtasks"]
    s2["2. service.get_by_id"]
    s3["3. HTTPException"]
    s4["4. IterationService"]
    s5["5. iteration_service.get_by_id"]
    s6["6. service.task_to_response"]
    s1 -. "service.get_by_id(task_id)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s3
    s1 -->|"IterationService(db)"| s4
    s1 -. "iteration_service.get_by_id(task.iteration_id)" .-> s5
    s1 -. "service.task_to_response(child, end_date)" .-> s6
    click s1 "../modules/tasks.md"
    click s4 "../modules/iteration_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_subtasks` | `task_id: int`, `service: Annotated[TaskService, Depends(get_task_service)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | `status` | - | `...` |
| `service.get_by_id` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `IterationService` | - | - | - | - |
| `iteration_service.get_by_id` | - | - | - | - |
| `service.task_to_response` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_subtasks | service.get_by_id | 595 | `service.get_by_id(task_id)` |
| get_subtasks | HTTPException | 597 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| get_subtasks | IterationService | 602 | `IterationService(db)` |
| get_subtasks | iteration_service.get_by_id | 603 | `iteration_service.get_by_id(task.iteration_id)` |
| get_subtasks | service.task_to_response | 606 | `service.task_to_response(child, end_date)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_subtasks` | `service.get_by_id` | 595 |
| external_call | `get_subtasks` | `HTTPException` | 597 |
| unresolved_call | `get_subtasks` | `iteration_service.get_by_id` | 603 |
| unresolved_call | `get_subtasks` | `service.task_to_response` | 606 |

## Behavior

This flow starts at `get_subtasks` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
