# current_task_review

**Entry point:** `current_task_review` (`http`)
**Source:** [routers_task_domain](../modules/routers_task_domain.md)
**Modules touched:** [routers_task_domain](../modules/routers_task_domain.md), [task_detail_service](../modules/task_detail_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as current_task_review
    participant p1 as domain_result
    participant p2 as HTTPException
    participant p3 as exc.detail
    participant p4 as str
    participant p5 as TaskDetailService(…).detail
    participant p6 as TaskDetailService
    participant p7 as db.scalar
    participant p8 as select(…).where(…).order_by(…).limit
    participant p9 as select(…).where(…).order_by
    participant p10 as select(…).where
    participant p11 as select
    participant p12 as TaskReviewRecord.id.desc
    p0->>p1: domain_result
    p1-->>p2: HTTPException
    p1-->>p3: exc.detail
    p1-->>p2: HTTPException
    p1-->>p4: str
    p1-->>p2: HTTPException
    p1-->>p4: str
    p1-->>p2: HTTPException
    p0-->>p5: TaskDetailService(…).detail
    p0->>p6: TaskDetailService
    p0-->>p7: db.scalar
    p0-->>p8: select(…).where(…).order_by(…).limit
    p0-->>p9: select(…).where(…).order_by
    p0-->>p10: select(…).where
    p0-->>p11: select
    p0-->>p12: TaskReviewRecord.id.desc
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. current_task_review"]
    s2["2. domain_result"]
    s3["3. HTTPException"]
    s4["4. exc.detail"]
    s5["5. HTTPException"]
    s6["6. str"]
    s7["7. HTTPException"]
    s8["8. str"]
    s9["9. HTTPException"]
    s10["10. TaskDetailService(…).detail"]
    s11["11. TaskDetailService"]
    s12["12. db.scalar"]
    s1 -->|"domain_result(...)"| s2
    s2 -. "HTTPException(409, detail=exc.detail(...))" .-> s3
    s2 -. "exc.detail(data not statically known)" .-> s4
    s2 -. "HTTPException(404, detail=str(...))" .-> s5
    s2 -. "str(exc)" .-> s6
    s2 -. "HTTPException(422, detail=[...])" .-> s7
    s2 -. "str(exc)" .-> s8
    s2 -. "HTTPException(404, detail='Task not found or inaccessible')" .-> s9
    s1 -. "TaskDetailService(…).detail(task_id, limit=1)" .-> s10
    s1 -->|"TaskDetailService(db)"| s11
    s1 -. "db.scalar(...)" .-> s12
    click s1 "../modules/routers_task_domain.md"
    click s2 "../modules/routers_task_domain.md"
    click s11 "../modules/task_detail_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `current_task_review` | `task_id: int`, `db: DB` | - | - | `{...}` |
| `domain_result` | `awaitable` | `TaskVersionConflictError` | - | `result` |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `TaskDetailService(…).detail` | - | - | - | - |
| `TaskDetailService` | - | - | - | - |
| `db.scalar` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| current_task_review | domain_result | 211 | `domain_result(...)` |
| domain_result | HTTPException | 42 | `HTTPException(409, detail=exc.detail(...))` |
| domain_result | exc.detail | 42 | `exc.detail(data not statically known)` |
| domain_result | HTTPException | 44 | `HTTPException(404, detail=str(...))` |
| domain_result | str | 44 | `str(exc)` |
| domain_result | HTTPException | 46 | `HTTPException(422, detail=[...])` |
| domain_result | str | 46 | `str(exc)` |
| domain_result | HTTPException | 48 | `HTTPException(404, detail='Task not found or inaccessible')` |
| current_task_review | TaskDetailService(…).detail | 211 | `TaskDetailService(db).detail(task_id, limit=1)` |
| current_task_review | TaskDetailService | 211 | `TaskDetailService(db)` |
| current_task_review | db.scalar | 213 | `db.scalar(...)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `domain_result` | `HTTPException` | 42 |
| unresolved_call | `domain_result` | `exc.detail` | 42 |
| external_call | `domain_result` | `HTTPException` | 44 |
| external_call | `domain_result` | `HTTPException` | 46 |
| external_call | `domain_result` | `HTTPException` | 48 |
| unresolved_call | `current_task_review` | `TaskDetailService(db).detail` | 211 |
| unresolved_call | `current_task_review` | `db.scalar` | 213 |
| step_limit | `current_task_review` | `first 12 steps` | 0 |

## Behavior

Checks current task visibility through the bounded detail service, then selects the latest review matching the current task, brief and artifact revisions. The response includes the task version with the verdict or null. This lookup does not depend on the first history page and does not mutate task state.
