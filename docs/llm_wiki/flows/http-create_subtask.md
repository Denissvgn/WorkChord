# create_subtask

**Entry point:** `create_subtask` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [iteration_service](../modules/iteration_service.md), [tasks](../modules/tasks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as create_subtask
    participant p1 as service.create_subtask
    participant p2 as HTTPException
    participant p3 as str
    participant p4 as IterationService
    participant p5 as iteration_service.get_by_id
    participant p6 as service.task_to_response
    p0-->>p1: service.create_subtask
    p0-->>p2: HTTPException
    p0-->>p3: str
    p0-->>p2: HTTPException
    p0->>p4: IterationService
    p0-->>p5: iteration_service.get_by_id
    p0-->>p6: service.task_to_response
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. create_subtask"]
    s2["2. service.create_subtask"]
    s3["3. HTTPException"]
    s4["4. str"]
    s5["5. HTTPException"]
    s6["6. IterationService"]
    s7["7. iteration_service.get_by_id"]
    s8["8. service.task_to_response"]
    s1 -. "service.create_subtask(task_id, data)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s3
    s1 -. "str(e)" .-> s4
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s5
    s1 -->|"IterationService(db)"| s6
    s1 -. "iteration_service.get_by_id(task.iteration_id)" .-> s7
    s1 -. "service.task_to_response(task, ...)" .-> s8
    click s1 "../modules/tasks.md"
    click s6 "../modules/iteration_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `create_subtask` | `task_id: int`, `data: TaskCreate`, `service: Annotated[TaskService, Depends(get_task_service)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | `status`, `status` | - | `service.task_to_response(...)` |
| `service.create_subtask` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `IterationService` | - | - | - | - |
| `iteration_service.get_by_id` | - | - | - | - |
| `service.task_to_response` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| create_subtask | service.create_subtask | 566 | `service.create_subtask(task_id, data)` |
| create_subtask | HTTPException | 568 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| create_subtask | str | 570 | `str(e)` |
| create_subtask | HTTPException | 573 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| create_subtask | IterationService | 578 | `IterationService(db)` |
| create_subtask | iteration_service.get_by_id | 579 | `iteration_service.get_by_id(task.iteration_id)` |
| create_subtask | service.task_to_response | 581 | `service.task_to_response(task, ...)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `create_subtask` | `service.create_subtask` | 566 |
| external_call | `create_subtask` | `HTTPException` | 568 |
| external_call | `create_subtask` | `HTTPException` | 573 |
| unresolved_call | `create_subtask` | `iteration_service.get_by_id` | 579 |
| unresolved_call | `create_subtask` | `service.task_to_response` | 581 |

## Behavior

This flow starts at `create_subtask` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
