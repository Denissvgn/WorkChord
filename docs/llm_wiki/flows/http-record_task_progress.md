# record_task_progress

**Entry point:** `record_task_progress` (`http`)
**Source:** [routers_task_domain](../modules/routers_task_domain.md)
**Modules touched:** [routers_task_domain](../modules/routers_task_domain.md), [task_brief_service](../modules/task_brief_service.md), [task_service](../modules/task_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as record_task_progress
    participant p1 as domain_result
    participant p2 as HTTPException
    participant p3 as exc.detail
    participant p4 as str
    participant p5 as TaskBriefService(…).write_progress
    participant p6 as TaskBriefService
    participant p7 as TaskService(…).task_to_response
    participant p8 as TaskService
    p0->>p1: domain_result
    p1-->>p2: HTTPException
    p1-->>p3: exc.detail
    p1-->>p2: HTTPException
    p1-->>p4: str
    p1-->>p2: HTTPException
    p0-->>p5: TaskBriefService(…).write_progress
    p0->>p6: TaskBriefService
    p0-->>p7: TaskService(…).task_to_response
    p0->>p8: TaskService
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. record_task_progress"]
    s2["2. domain_result"]
    s3["3. HTTPException"]
    s4["4. exc.detail"]
    s5["5. HTTPException"]
    s6["6. str"]
    s7["7. HTTPException"]
    s8["8. TaskBriefService(…).write_progress"]
    s9["9. TaskBriefService"]
    s10["10. TaskService(…).task_to_response"]
    s11["11. TaskService"]
    s1 -->|"domain_result(...)"| s2
    s2 -. "HTTPException(409, detail=exc.detail(...))" .-> s3
    s2 -. "exc.detail(data not statically known)" .-> s4
    s2 -. "HTTPException(422, detail=[...])" .-> s5
    s2 -. "str(exc)" .-> s6
    s2 -. "HTTPException(404, detail='Task not found or inaccessible')" .-> s7
    s1 -. "TaskBriefService(…).write_progress(task_id, data)" .-> s8
    s1 -->|"TaskBriefService(db)"| s9
    s1 -. "TaskService(…).task_to_response(task)" .-> s10
    s1 -->|"TaskService(db)"| s11
    click s1 "../modules/routers_task_domain.md"
    click s2 "../modules/routers_task_domain.md"
    click s9 "../modules/task_brief_service.md"
    click s11 "../modules/task_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `record_task_progress` | `task_id: int`, `data: ProgressWrite`, `db: DB` | - | - | `...` |
| `domain_result` | `awaitable` | `TaskVersionConflictError` | - | `result` |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `TaskBriefService(…).write_progress` | - | - | - | - |
| `TaskBriefService` | - | - | - | - |
| `TaskService(…).task_to_response` | - | - | - | - |
| `TaskService` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| record_task_progress | domain_result | 164 | `domain_result(...)` |
| domain_result | HTTPException | 29 | `HTTPException(409, detail=exc.detail(...))` |
| domain_result | exc.detail | 29 | `exc.detail(data not statically known)` |
| domain_result | HTTPException | 31 | `HTTPException(422, detail=[...])` |
| domain_result | str | 31 | `str(exc)` |
| domain_result | HTTPException | 33 | `HTTPException(404, detail='Task not found or inaccessible')` |
| record_task_progress | TaskBriefService(…).write_progress | 164 | `TaskBriefService(db).write_progress(task_id, data)` |
| record_task_progress | TaskBriefService | 164 | `TaskBriefService(db)` |
| record_task_progress | TaskService(…).task_to_response | 165 | `TaskService(db).task_to_response(task)` |
| record_task_progress | TaskService | 165 | `TaskService(db)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `domain_result` | `HTTPException` | 29 |
| unresolved_call | `domain_result` | `exc.detail` | 29 |
| external_call | `domain_result` | `HTTPException` | 31 |
| external_call | `domain_result` | `HTTPException` | 33 |
| unresolved_call | `record_task_progress` | `TaskBriefService(db).write_progress` | 164 |
| unresolved_call | `record_task_progress` | `TaskService(db).task_to_response` | 165 |

## Behavior

This flow starts at `record_task_progress` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
