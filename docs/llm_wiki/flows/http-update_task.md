# update_task

**Entry point:** `update_task` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [iteration_service](../modules/iteration_service.md), [tasks](../modules/tasks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as update_task
    participant p1 as service.update
    participant p2 as _raise_task_version_conflict
    participant p3 as HTTPException (backend/app/routers/tasks…aise_task_version_conflict)
    participant p4 as exc.detail
    participant p5 as HTTPException (backend/app/routers/tasks.py:update_task)
    participant p6 as str
    participant p7 as IterationService
    participant p8 as iteration_service.get_by_id
    participant p9 as service.task_to_response
    p0-->>p1: service.update
    p0->>p2: _raise_task_version_conflict
    p2-->>p3: HTTPException (backend/app/routers/tasks…aise_task_version_conflict)
    p2-->>p4: exc.detail
    p0-->>p5: HTTPException (backend/app/routers/tasks.py:update_task)
    p0-->>p6: str
    p0-->>p5: HTTPException (backend/app/routers/tasks.py:update_task)
    p0->>p7: IterationService
    p0-->>p8: iteration_service.get_by_id
    p0-->>p9: service.task_to_response
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. update_task"]
    s2["2. service.update"]
    s3["3. _raise_task_version_conflict"]
    s4["4. HTTPException (backend/app/routers/tasks…aise_task_version_conflict)"]
    s5["5. exc.detail"]
    s6["6. HTTPException (backend/app/routers/tasks.py:update_task)"]
    s7["7. str"]
    s8["8. HTTPException (backend/app/routers/tasks.py:update_task)"]
    s9["9. IterationService"]
    s10["10. iteration_service.get_by_id"]
    s11["11. service.task_to_response"]
    s1 -. "service.update(task_id, data)" .-> s2
    s1 -->|"_raise_task_version_conflict(exc)"| s3
    s3 -. "HTTPException (backend/app/routers/tasks…aise_task_version_conflict)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))" .-> s4
    s3 -. "exc.detail(data not statically known)" .-> s5
    s1 -. "HTTPException (backend/app/routers/tasks.py:update_task)(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s6
    s1 -. "str(e)" .-> s7
    s1 -. "HTTPException (backend/app/routers/tasks.py:update_task)(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s8
    s1 -->|"IterationService(db)"| s9
    s1 -. "iteration_service.get_by_id(task.iteration_id)" .-> s10
    s1 -. "service.task_to_response(task, ...)" .-> s11
    b0["mutation service.update"]
    s1 -. "mutation service.update" .-> b0
    click s1 "../modules/tasks.md"
    click s3 "../modules/tasks.md"
    click s9 "../modules/iteration_service.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `update_task` | `task_id: int`, `data: TaskUpdate`, `service: Annotated[TaskService, Depends(get_task_service)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | `TaskVersionConflictError`, `status`, `status` | - | `service.task_to_response(...)` |
| `service.update` | - | - | - | - |
| `_raise_task_version_conflict` | `exc: TaskVersionConflictError` | `status` | - | - |
| `HTTPException (backend/app/routers/tasks…aise_task_version_conflict)` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `HTTPException (backend/app/routers/tasks.py:update_task)` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException (backend/app/routers/tasks.py:update_task)` | - | - | - | - |
| `IterationService` | - | - | - | - |
| `iteration_service.get_by_id` | - | - | - | - |
| `service.task_to_response` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| update_task | service.update | 329 | `service.update(task_id, data)` |
| update_task | _raise_task_version_conflict | 331 | `_raise_task_version_conflict(exc)` |
| _raise_task_version_conflict | HTTPException (backend/app/routers/tasks…aise_task_version_conflict) | 56 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _raise_task_version_conflict | exc.detail | 58 | `exc.detail(data not statically known)` |
| update_task | HTTPException (backend/app/routers/tasks.py:update_task) | 333 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| update_task | str | 335 | `str(e)` |
| update_task | HTTPException (backend/app/routers/tasks.py:update_task) | 338 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| update_task | IterationService | 343 | `IterationService(db)` |
| update_task | iteration_service.get_by_id | 344 | `iteration_service.get_by_id(task.iteration_id)` |
| update_task | service.task_to_response | 346 | `service.task_to_response(task, ...)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `service.update` | `update_task` | 329 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `_raise_task_version_conflict` | `HTTPException` | 56 |
| unresolved_call | `_raise_task_version_conflict` | `exc.detail` | 58 |
| external_call | `update_task` | `HTTPException` | 333 |
| external_call | `update_task` | `HTTPException` | 338 |
| unresolved_call | `update_task` | `iteration_service.get_by_id` | 344 |
| unresolved_call | `update_task` | `service.task_to_response` | 346 |

## Behavior

This flow starts at `update_task` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

Backlog project changes require edit permission in both scopes. Project locks are acquired in ascending ID order and the task scope is rechecked before writing. The complete subtree must have no incoming or outgoing dependency across its boundary. Both backlogs receive transactional recovery points, descendants reserve one version per command, and rejected moves roll everything back. Actual dependency changes invalidate current progress and acceptance through general updates and individual add/remove commands. Immutable evidence history remains available, a command reserves one task version, and no-op dependency requests retain their current version. Locked graph relationships are loaded explicitly before applying a dependency update.
