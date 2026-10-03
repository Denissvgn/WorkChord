# task_command

**Entry point:** `task_command` (`http`)
**Source:** [routers_task_domain](../modules/routers_task_domain.md)
**Modules touched:** [routers_task_domain](../modules/routers_task_domain.md), [task_domain_service](../modules/task_domain_service.md), [task_service](../modules/task_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as task_command
    participant p1 as domain_result
    participant p2 as HTTPException
    participant p3 as exc.detail
    participant p4 as str
    participant p5 as TaskDomainService(…).command
    participant p6 as TaskDomainService
    participant p7 as TaskService(…).task_to_response
    participant p8 as TaskService
    p0->>p1: domain_result
    p1-->>p2: HTTPException
    p1-->>p3: exc.detail
    p1-->>p2: HTTPException
    p1-->>p4: str
    p1-->>p2: HTTPException
    p0-->>p5: TaskDomainService(…).command
    p0->>p6: TaskDomainService
    p0-->>p7: TaskService(…).task_to_response
    p0->>p8: TaskService
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. task_command"]
    s2["2. domain_result"]
    s3["3. HTTPException"]
    s4["4. exc.detail"]
    s5["5. HTTPException"]
    s6["6. str"]
    s7["7. HTTPException"]
    s8["8. TaskDomainService(…).command"]
    s9["9. TaskDomainService"]
    s10["10. TaskService(…).task_to_response"]
    s11["11. TaskService"]
    s1 -->|"domain_result(...)"| s2
    s2 -. "HTTPException(409, detail=exc.detail(...))" .-> s3
    s2 -. "exc.detail(data not statically known)" .-> s4
    s2 -. "HTTPException(422, detail=[...])" .-> s5
    s2 -. "str(exc)" .-> s6
    s2 -. "HTTPException(404, detail='Task not found or inaccessible')" .-> s7
    s1 -. "TaskDomainService(…).command(task_id, data)" .-> s8
    s1 -->|"TaskDomainService(db)"| s9
    s1 -. "TaskService(…).task_to_response(task)" .-> s10
    s1 -->|"TaskService(db)"| s11
    click s1 "../modules/routers_task_domain.md"
    click s2 "../modules/routers_task_domain.md"
    click s9 "../modules/task_domain_service.md"
    click s11 "../modules/task_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `task_command` | `task_id: int`, `data: TaskActionRequest`, `db: DB` | - | - | `...` |
| `domain_result` | `awaitable` | `TaskVersionConflictError` | - | `result` |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `TaskDomainService(…).command` | - | - | - | - |
| `TaskDomainService` | - | - | - | - |
| `TaskService(…).task_to_response` | - | - | - | - |
| `TaskService` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| task_command | domain_result | 137 | `domain_result(...)` |
| domain_result | HTTPException | 29 | `HTTPException(409, detail=exc.detail(...))` |
| domain_result | exc.detail | 29 | `exc.detail(data not statically known)` |
| domain_result | HTTPException | 31 | `HTTPException(422, detail=[...])` |
| domain_result | str | 31 | `str(exc)` |
| domain_result | HTTPException | 33 | `HTTPException(404, detail='Task not found or inaccessible')` |
| task_command | TaskDomainService(…).command | 137 | `TaskDomainService(db).command(task_id, data)` |
| task_command | TaskDomainService | 137 | `TaskDomainService(db)` |
| task_command | TaskService(…).task_to_response | 138 | `TaskService(db).task_to_response(task)` |
| task_command | TaskService | 138 | `TaskService(db)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `domain_result` | `HTTPException` | 29 |
| unresolved_call | `domain_result` | `exc.detail` | 29 |
| external_call | `domain_result` | `HTTPException` | 31 |
| external_call | `domain_result` | `HTTPException` | 33 |
| unresolved_call | `task_command` | `TaskDomainService(db).command` | 137 |
| unresolved_call | `task_command` | `TaskService(db).task_to_response` | 138 |

## Behavior

This flow starts at `task_command` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
