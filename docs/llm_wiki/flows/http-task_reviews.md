# task_reviews

**Entry point:** `task_reviews` (`http`)
**Source:** [routers_task_domain](../modules/routers_task_domain.md)
**Modules touched:** [routers_task_domain](../modules/routers_task_domain.md), [task_detail_service](../modules/task_detail_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as task_reviews
    participant p1 as domain_result
    participant p2 as HTTPException
    participant p3 as exc.detail
    participant p4 as str
    participant p5 as TaskDetailService(…).detail
    participant p6 as TaskDetailService
    participant p7 as list
    participant p8 as (…).all
    participant p9 as db.scalars
    participant p10 as select(…).where(…).order_by(…).limit
    participant p11 as select(…).where(…).order_by
    participant p12 as select(…).where
    participant p13 as select
    p0->>p1: domain_result
    p1-->>p2: HTTPException
    p1-->>p3: exc.detail
    p1-->>p2: HTTPException
    p1-->>p4: str
    p1-->>p2: HTTPException
    p0-->>p5: TaskDetailService(…).detail
    p0->>p6: TaskDetailService
    p0-->>p7: list
    p0-->>p8: (…).all
    p0-->>p9: db.scalars
    p0-->>p10: select(…).where(…).order_by(…).limit
    p0-->>p11: select(…).where(…).order_by
    p0-->>p12: select(…).where
    p0-->>p13: select
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. task_reviews"]
    s2["2. domain_result"]
    s3["3. HTTPException"]
    s4["4. exc.detail"]
    s5["5. HTTPException"]
    s6["6. str"]
    s7["7. HTTPException"]
    s8["8. TaskDetailService(…).detail"]
    s9["9. TaskDetailService"]
    s10["10. list"]
    s11["11. (…).all"]
    s12["12. db.scalars"]
    s1 -->|"domain_result(...)"| s2
    s2 -. "HTTPException(409, detail=exc.detail(...))" .-> s3
    s2 -. "exc.detail(data not statically known)" .-> s4
    s2 -. "HTTPException(422, detail=[...])" .-> s5
    s2 -. "str(exc)" .-> s6
    s2 -. "HTTPException(404, detail='Task not found or inaccessible')" .-> s7
    s1 -. "TaskDetailService(…).detail(task_id, limit=1)" .-> s8
    s1 -->|"TaskDetailService(db)"| s9
    s1 -. "list(...)" .-> s10
    s1 -. "(…).all(data not statically known)" .-> s11
    s1 -. "db.scalars(...)" .-> s12
    click s1 "../modules/routers_task_domain.md"
    click s2 "../modules/routers_task_domain.md"
    click s9 "../modules/task_detail_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `task_reviews` | `task_id: int`, `db: DB`, `limit: int`, `after_id: int` | - | - | `list(...)` |
| `domain_result` | `awaitable` | `TaskVersionConflictError` | - | `result` |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `TaskDetailService(…).detail` | - | - | - | - |
| `TaskDetailService` | - | - | - | - |
| `list` | - | - | - | - |
| `(…).all` | - | - | - | - |
| `db.scalars` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| task_reviews | domain_result | 150 | `domain_result(...)` |
| domain_result | HTTPException | 29 | `HTTPException(409, detail=exc.detail(...))` |
| domain_result | exc.detail | 29 | `exc.detail(data not statically known)` |
| domain_result | HTTPException | 31 | `HTTPException(422, detail=[...])` |
| domain_result | str | 31 | `str(exc)` |
| domain_result | HTTPException | 33 | `HTTPException(404, detail='Task not found or inaccessible')` |
| task_reviews | TaskDetailService(…).detail | 150 | `TaskDetailService(db).detail(task_id, limit=1)` |
| task_reviews | TaskDetailService | 150 | `TaskDetailService(db)` |
| task_reviews | list | 151 | `list(...)` |
| task_reviews | (…).all | 151 | `(await db.scalars(select(TaskReviewRecord).where(TaskReviewRecord.original_task_id == task_id, TaskReviewRecord.id > after_id).order_by(TaskReviewRecord.id).limit(limit))).all(data not statically known)` |
| task_reviews | db.scalars | 151 | `db.scalars(...)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `domain_result` | `HTTPException` | 29 |
| unresolved_call | `domain_result` | `exc.detail` | 29 |
| external_call | `domain_result` | `HTTPException` | 31 |
| external_call | `domain_result` | `HTTPException` | 33 |
| unresolved_call | `task_reviews` | `TaskDetailService(db).detail` | 150 |
| unresolved_call | `task_reviews` | `(await db.scalars(select(TaskReviewRecord).where(TaskReviewRecord.original_task_id == task_id, TaskReviewRecord.id > after_id).order_by(TaskReviewRecord.id).limit(limit))).all` | 151 |
| unresolved_call | `task_reviews` | `db.scalars` | 151 |
| step_limit | `task_reviews` | `first 12 steps` | 0 |

## Behavior

This flow starts at `task_reviews` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
