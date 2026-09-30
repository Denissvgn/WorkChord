# create_backlog_task

**Entry point:** `create_backlog_task` (`http`)
**Source:** [routers_task_domain](../modules/routers_task_domain.md)
**Modules touched:** [routers_task_domain](../modules/routers_task_domain.md), [task_service](../modules/task_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as create_backlog_task
    participant p1 as HTTPException (backend/app/routers/task_…ain.py:create_backlog_task)
    participant p2 as domain_result
    participant p3 as HTTPException (backend/app/routers/task_domain.py:domain_result)
    participant p4 as exc.detail
    participant p5 as str
    participant p6 as TaskService(…).create
    participant p7 as TaskService
    participant p8 as data.model_copy
    participant p9 as TaskService(…).task_to_response
    p0-->>p1: HTTPException (backend/app/routers/task_…ain.py:create_backlog_task)
    p0->>p2: domain_result
    p2-->>p3: HTTPException (backend/app/routers/task_domain.py:domain_result)
    p2-->>p4: exc.detail
    p2-->>p3: HTTPException (backend/app/routers/task_domain.py:domain_result)
    p2-->>p5: str
    p2-->>p3: HTTPException (backend/app/routers/task_domain.py:domain_result)
    p0-->>p6: TaskService(…).create
    p0->>p7: TaskService
    p0-->>p8: data.model_copy
    p0-->>p9: TaskService(…).task_to_response
    p0->>p7: TaskService
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. create_backlog_task"]
    s2["2. HTTPException (backend/app/routers/task_…ain.py:create_backlog_task)"]
    s3["3. domain_result"]
    s4["4. HTTPException (backend/app/routers/task_domain.py:domain_result)"]
    s5["5. exc.detail"]
    s6["6. HTTPException (backend/app/routers/task_domain.py:domain_result)"]
    s7["7. str"]
    s8["8. HTTPException (backend/app/routers/task_domain.py:domain_result)"]
    s9["9. TaskService(…).create"]
    s10["10. TaskService"]
    s11["11. data.model_copy"]
    s12["12. TaskService(…).task_to_response"]
    s1 -. "HTTPException (backend/app/routers/task_…ain.py:create_backlog_task)(422, detail=[...])" .-> s2
    s1 -->|"domain_result(...)"| s3
    s3 -. "HTTPException (backend/app/routers/task_domain.py:domain_result)(409, detail=exc.detail(...))" .-> s4
    s3 -. "exc.detail(data not statically known)" .-> s5
    s3 -. "HTTPException (backend/app/routers/task_domain.py:domain_result)(422, detail=[...])" .-> s6
    s3 -. "str(exc)" .-> s7
    s3 -. "HTTPException (backend/app/routers/task_domain.py:domain_result)(404, detail='Task not found or inaccessible')" .-> s8
    s1 -. "TaskService(…).create(None, data.model_copy(...))" .-> s9
    s1 -->|"TaskService(db)"| s10
    s1 -. "data.model_copy(update={...})" .-> s11
    s1 -. "TaskService(…).task_to_response(task)" .-> s12
    click s1 "../modules/routers_task_domain.md"
    click s3 "../modules/routers_task_domain.md"
    click s10 "../modules/task_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `create_backlog_task` | `project_id: int`, `data: TaskCreate`, `db: DB` | - | - | `...` |
| `HTTPException (backend/app/routers/task_…ain.py:create_backlog_task)` | - | - | - | - |
| `domain_result` | `awaitable` | `TaskVersionConflictError` | - | `result` |
| `HTTPException (backend/app/routers/task_domain.py:domain_result)` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `HTTPException (backend/app/routers/task_domain.py:domain_result)` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException (backend/app/routers/task_domain.py:domain_result)` | - | - | - | - |
| `TaskService(…).create` | - | - | - | - |
| `TaskService` | - | - | - | - |
| `data.model_copy` | - | - | - | - |
| `TaskService(…).task_to_response` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| create_backlog_task | HTTPException (backend/app/routers/task_…ain.py:create_backlog_task) | 109 | `HTTPException(422, detail=[...])` |
| create_backlog_task | domain_result | 110 | `domain_result(...)` |
| domain_result | HTTPException (backend/app/routers/task_domain.py:domain_result) | 29 | `HTTPException(409, detail=exc.detail(...))` |
| domain_result | exc.detail | 29 | `exc.detail(data not statically known)` |
| domain_result | HTTPException (backend/app/routers/task_domain.py:domain_result) | 31 | `HTTPException(422, detail=[...])` |
| domain_result | str | 31 | `str(exc)` |
| domain_result | HTTPException (backend/app/routers/task_domain.py:domain_result) | 33 | `HTTPException(404, detail='Task not found or inaccessible')` |
| create_backlog_task | TaskService(…).create | 110 | `TaskService(db).create(None, data.model_copy(...))` |
| create_backlog_task | TaskService | 110 | `TaskService(db)` |
| create_backlog_task | data.model_copy | 110 | `data.model_copy(update={...})` |
| create_backlog_task | TaskService(…).task_to_response | 111 | `TaskService(db).task_to_response(task)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `create_backlog_task` | `HTTPException` | 109 |
| external_call | `domain_result` | `HTTPException` | 29 |
| unresolved_call | `domain_result` | `exc.detail` | 29 |
| external_call | `domain_result` | `HTTPException` | 31 |
| external_call | `domain_result` | `HTTPException` | 33 |
| unresolved_call | `create_backlog_task` | `TaskService(db).create` | 110 |
| unresolved_call | `create_backlog_task` | `data.model_copy` | 110 |
| unresolved_call | `create_backlog_task` | `TaskService(db).task_to_response` | 111 |
| step_limit | `create_backlog_task` | `first 12 steps` | 0 |

## Behavior

This flow starts at `create_backlog_task` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
