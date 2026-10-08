# personal_inbox

**Entry point:** `personal_inbox` (`http`)
**Source:** [routers_discussion](../modules/routers_discussion.md)
**Modules touched:** [discussion_service](../modules/discussion_service.md), [routers_discussion](../modules/routers_discussion.md), [routers_task_domain](../modules/routers_task_domain.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as personal_inbox
    participant p1 as domain_result
    participant p2 as HTTPException
    participant p3 as exc.detail
    participant p4 as str
    participant p5 as DiscussionService(…).inbox
    participant p6 as DiscussionService
    p0->>p1: domain_result
    p1-->>p2: HTTPException
    p1-->>p3: exc.detail
    p1-->>p2: HTTPException
    p1-->>p4: str
    p1-->>p2: HTTPException
    p1-->>p4: str
    p1-->>p2: HTTPException
    p0-->>p5: DiscussionService(…).inbox
    p0->>p6: DiscussionService
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. personal_inbox"]
    s2["2. domain_result"]
    s3["3. HTTPException"]
    s4["4. exc.detail"]
    s5["5. HTTPException"]
    s6["6. str"]
    s7["7. HTTPException"]
    s8["8. str"]
    s9["9. HTTPException"]
    s10["10. DiscussionService(…).inbox"]
    s11["11. DiscussionService"]
    s1 -->|"domain_result(...)"| s2
    s2 -. "HTTPException(409, detail=exc.detail(...))" .-> s3
    s2 -. "exc.detail(data not statically known)" .-> s4
    s2 -. "HTTPException(404, detail=str(...))" .-> s5
    s2 -. "str(exc)" .-> s6
    s2 -. "HTTPException(422, detail=[...])" .-> s7
    s2 -. "str(exc)" .-> s8
    s2 -. "HTTPException(404, detail='Task not found or inaccessible')" .-> s9
    s1 -. "DiscussionService(…).inbox(after_id=after_id, limit=limit)" .-> s10
    s1 -->|"DiscussionService(db)"| s11
    click s1 "../modules/routers_discussion.md"
    click s2 "../modules/routers_task_domain.md"
    click s11 "../modules/discussion_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `personal_inbox` | `db: DiscussionDatabase`, `after_id: int`, `limit: int` | - | - | `...` |
| `domain_result` | `awaitable` | `TaskVersionConflictError` | - | `result` |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `DiscussionService(…).inbox` | - | - | - | - |
| `DiscussionService` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| personal_inbox | domain_result | 75 | `domain_result(...)` |
| domain_result | HTTPException | 42 | `HTTPException(409, detail=exc.detail(...))` |
| domain_result | exc.detail | 42 | `exc.detail(data not statically known)` |
| domain_result | HTTPException | 44 | `HTTPException(404, detail=str(...))` |
| domain_result | str | 44 | `str(exc)` |
| domain_result | HTTPException | 46 | `HTTPException(422, detail=[...])` |
| domain_result | str | 46 | `str(exc)` |
| domain_result | HTTPException | 48 | `HTTPException(404, detail='Task not found or inaccessible')` |
| personal_inbox | DiscussionService(…).inbox | 75 | `DiscussionService(db).inbox(after_id=after_id, limit=limit)` |
| personal_inbox | DiscussionService | 75 | `DiscussionService(db)` |

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
| unresolved_call | `personal_inbox` | `DiscussionService(db).inbox` | 75 |

## Behavior

Returns a bounded personal inbox joined to currently visible tasks. Read/unread state is independent of task status, and revoked task access removes its notifications from the projection.
