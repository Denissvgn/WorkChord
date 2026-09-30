# move_task

**Entry point:** `move_task` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [iteration_service](../modules/iteration_service.md), [tasks](../modules/tasks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as move_task
    participant p1 as service.move_task
    participant p2 as _raise_task_version_conflict
    participant p3 as HTTPException (backend/app/routers/tasks…aise_task_version_conflict)
    participant p4 as exc.detail
    participant p5 as str
    participant p6 as HTTPException (backend/app/routers/tasks.py:move_task)
    participant p7 as IterationService
    participant p8 as iteration_service.get_by_id
    participant p9 as service.task_to_response
    p0-->>p1: service.move_task
    p0->>p2: _raise_task_version_conflict
    p2-->>p3: HTTPException (backend/app/routers/tasks…aise_task_version_conflict)
    p2-->>p4: exc.detail
    p0-->>p5: str
    p0-->>p6: HTTPException (backend/app/routers/tasks.py:move_task)
    p0-->>p6: HTTPException (backend/app/routers/tasks.py:move_task)
    p0-->>p6: HTTPException (backend/app/routers/tasks.py:move_task)
    p0->>p7: IterationService
    p0-->>p8: iteration_service.get_by_id
    p0-->>p9: service.task_to_response
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. move_task"]
    s2["2. service.move_task"]
    s3["3. _raise_task_version_conflict"]
    s4["4. HTTPException (backend/app/routers/tasks…aise_task_version_conflict)"]
    s5["5. exc.detail"]
    s6["6. str"]
    s7["7. HTTPException (backend/app/routers/tasks.py:move_task)"]
    s8["8. HTTPException (backend/app/routers/tasks.py:move_task)"]
    s9["9. HTTPException (backend/app/routers/tasks.py:move_task)"]
    s10["10. IterationService"]
    s11["11. iteration_service.get_by_id"]
    s12["12. service.task_to_response"]
    s1 -. "service.move_task(…)" .-> s2
    s1 -->|"_raise_task_version_conflict(exc)"| s3
    s3 -. "HTTPException (backend/app/routers/tasks…aise_task_version_conflict)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))" .-> s4
    s3 -. "exc.detail(data not statically known)" .-> s5
    s1 -. "str(e)" .-> s6
    s1 -. "HTTPException (backend/app/routers/tasks.py:move_task)(status_code=status.HTTP_404_NOT_FOUND, detail=detail)" .-> s7
    s1 -. "HTTPException (backend/app/routers/tasks.py:move_task)(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)" .-> s8
    s1 -. "HTTPException (backend/app/routers/tasks.py:move_task)(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s9
    s1 -->|"IterationService(db)"| s10
    s1 -. "iteration_service.get_by_id(task.iteration_id)" .-> s11
    s1 -. "service.task_to_response(task, ...)" .-> s12
    click s1 "../modules/tasks.md"
    click s3 "../modules/tasks.md"
    click s10 "../modules/iteration_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `move_task` | `task_id: int`, `data: TaskMoveRequest`, `service: Annotated[TaskService, Depends(get_task_service)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | `TaskVersionConflictError`, `status`, `status`, `status` | - | `service.task_to_response(...)` |
| `service.move_task` | - | - | - | - |
| `_raise_task_version_conflict` | `exc: TaskVersionConflictError` | `status` | - | - |
| `HTTPException (backend/app/routers/tasks…aise_task_version_conflict)` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException (backend/app/routers/tasks.py:move_task)` | - | - | - | - |
| `HTTPException (backend/app/routers/tasks.py:move_task)` | - | - | - | - |
| `HTTPException (backend/app/routers/tasks.py:move_task)` | - | - | - | - |
| `IterationService` | - | - | - | - |
| `iteration_service.get_by_id` | - | - | - | - |
| `service.task_to_response` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| move_task | service.move_task | 360 | `service.move_task(task_id, target_iteration_id=data.iteration_id, parent_id=data.parent_id, expected_version=data.expected_version, expected_revisions=data.expected_revisions)` |
| move_task | _raise_task_version_conflict | 368 | `_raise_task_version_conflict(exc)` |
| _raise_task_version_conflict | HTTPException (backend/app/routers/tasks…aise_task_version_conflict) | 56 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _raise_task_version_conflict | exc.detail | 58 | `exc.detail(data not statically known)` |
| move_task | str | 370 | `str(e)` |
| move_task | HTTPException (backend/app/routers/tasks.py:move_task) | 372 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)` |
| move_task | HTTPException (backend/app/routers/tasks.py:move_task) | 376 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)` |
| move_task | HTTPException (backend/app/routers/tasks.py:move_task) | 381 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| move_task | IterationService | 386 | `IterationService(db)` |
| move_task | iteration_service.get_by_id | 387 | `iteration_service.get_by_id(task.iteration_id)` |
| move_task | service.task_to_response | 388 | `service.task_to_response(task, ...)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `move_task` | `service.move_task` | 360 |
| external_call | `_raise_task_version_conflict` | `HTTPException` | 56 |
| unresolved_call | `_raise_task_version_conflict` | `exc.detail` | 58 |
| external_call | `move_task` | `HTTPException` | 372 |
| external_call | `move_task` | `HTTPException` | 376 |
| external_call | `move_task` | `HTTPException` | 381 |
| unresolved_call | `move_task` | `iteration_service.get_by_id` | 387 |
| unresolved_call | `move_task` | `service.task_to_response` | 388 |

## Behavior

This flow starts at `move_task` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
