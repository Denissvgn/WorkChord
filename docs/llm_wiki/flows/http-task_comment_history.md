# task_comment_history

**Entry point:** `task_comment_history` (`http`)
**Source:** [routers_discussion](../modules/routers_discussion.md)
**Modules touched:** [authority](../modules/authority.md), [config](../modules/config.md), [discussion_service](../modules/discussion_service.md), [routers_discussion](../modules/routers_discussion.md), and 1 more

**Complete modules touched:**

- [authority](../modules/authority.md)
- [config](../modules/config.md)
- [discussion_service](../modules/discussion_service.md)
- [routers_discussion](../modules/routers_discussion.md)
- [routers_task_domain](../modules/routers_task_domain.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as task_comment_history
    participant p1 as DiscussionService.history
    participant p2 as domain_result
    participant p3 as DiscussionService
    participant p4 as DiscussionService.task
    participant p5 as require_project
    participant p6 as get_settings
    participant p7 as AuthorityError
    participant p8 as internal_authority
    participant p9 as Settings
    participant p10 as HTTPException
    participant p11 as exc.detail
    participant p12 as self.db.scalar (backend/app/services/disc…:DiscussionService.history)
    participant p13 as select(…).where (backend/app/services/disc…:DiscussionService.history)
    participant p14 as str
    participant p15 as select (backend/app/services/disc…:DiscussionService.history)
    participant p16 as ValueError (backend/app/services/disc…:DiscussionService.history)
    participant p17 as (…).all
    participant p18 as self.db.scalars
    participant p19 as select(…).where(…).order_by(…).limit
    participant p20 as select(…).where(…).order_by
    participant p21 as select(…).where (backend/app/services/disc…scussionService.history, 1)
    participant p22 as len
    participant p23 as self.db.scalar (backend/app/services/disc….py:DiscussionService.task)
    p0->>p1: DiscussionService.history
    p0->>p2: domain_result
    p0->>p3: DiscussionService
    p1->>p4: DiscussionService.task
    p4->>p5: require_project
    p5->>p6: get_settings
    p4->>p7: AuthorityError
    p4->>p8: internal_authority
    p6->>p9: Settings
    p2-->>p10: HTTPException(409, detail=exc.detail(...))
    p2-->>p11: exc.detail
    p1-->>p12: self.db.scalar (backend/app/services/disc…:DiscussionService.history)(...)
    p2-->>p10: HTTPException(404, detail=str(...))
    p1-->>p13: select(…).where (backend/app/services/disc…:DiscussionService.history)(..., ...)
    p2-->>p14: str(exc)
    p1-->>p15: select (backend/app/services/disc…:DiscussionService.history)(TaskComment)
    p2-->>p10: HTTPException(422, detail=[...])
    p1-->>p16: ValueError (backend/app/services/disc…:DiscussionService.history)('Comment not found or inaccessible')
    p2-->>p14: str(exc)
    p1-->>p16: ValueError (backend/app/services/disc…:DiscussionService.history)('Use a bounded history cursor')
    p2-->>p10: HTTPException(404, detail='Task not found or inaccessible')
    p1-->>p17: (…).all
    p1-->>p18: self.db.scalars(...)
    p1-->>p19: select(…).where(…).order_by(…).limit(...)
    p1-->>p20: select(…).where(…).order_by(TaskCommentRevision.version)
    p1-->>p21: select(…).where (backend/app/services/disc…scussionService.history, 1)(..., ...)
    p1-->>p15: select (backend/app/services/disc…:DiscussionService.history)(TaskCommentRevision)
    p1-->>p22: len(rows)
    p1-->>p22: len(rows)
    p4-->>p23: self.db.scalar (backend/app/services/disc….py:DiscussionService.task)(...)
```

> Call sequence diagram shows 30 of 48 interactions; 18 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 12 of 16 (4 omitted); unresolved 9 of 20 (11 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/discussion_service.py:DiscussionService.task` | 11 | - | unresolved | 8 |
| `backend/app/services/discussion_service.py:DiscussionService.task` | 11 | - | external | 4 |
| `backend/app/authority.py:require_project` | 17 | - | unresolved | 2 |
| `backend/app/authority.py:require_project` | 17 | [backend/app/authority.py](../modules/authority.md) | internal | 2 |
| `backend/app/authority.py:internal_authority` | 28 | - | unresolved | 1 |
| `backend/app/services/discussion_service.py:DiscussionService.task` | 11 | [backend/app/services/discussion_service.py](../modules/discussion_service.md) | internal | 1 |
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 13; effect analysis evaluated: 8, partial: 0, unavailable: 5. Counts include steps omitted from the displayed trace.

Collector observations for 8 source steps with known totals: observed: 37, emitted: 37, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `task_comment_history` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `domain_result` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `exc.detail` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `DiscussionService.history` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `DiscussionService.task` | `available` | `evaluated` | `available` | `7` | `7` | `0` |
| `self.db.scalar (backend/app/services/disc….py:DiscussionService.task)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. task_comment_history"]
    s2["2. domain_result"]
    s3["3. HTTPException"]
    s4["4. exc.detail"]
    s5["5. HTTPException"]
    s6["6. str"]
    s7["7. HTTPException"]
    s8["8. str"]
    s9["9. HTTPException"]
    s10["10. DiscussionService.history"]
    s11["11. DiscussionService.task"]
    s12["12. self.db.scalar (backend/app/services/disc….py:DiscussionService.task)"]
    s1 -->|"domain_result(...)"| s2
    s2 -. "HTTPException(409, detail=exc.detail(...))" .-> s3
    s2 -. "exc.detail(data not statically known)" .-> s4
    s2 -. "HTTPException(404, detail=str(...))" .-> s5
    s2 -. "str(exc)" .-> s6
    s2 -. "HTTPException(422, detail=[...])" .-> s7
    s2 -. "str(exc)" .-> s8
    s2 -. "HTTPException(404, detail='Task not found or inaccessible')" .-> s9
    s1 -->|"DiscussionService.history(task_id, comment_id, after_version=after_version, limit=limit)"| s10
    s10 -->|"DiscussionService.task(task_id)"| s11
    s11 -. "self.db.scalar (backend/app/services/disc….py:DiscussionService.task)(...)" .-> s12
    click s1 "../modules/routers_discussion.md"
    click s2 "../modules/routers_task_domain.md"
    click s10 "../modules/discussion_service.md"
    click s11 "../modules/discussion_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `task_comment_history` | `task_id: int`, `comment_id: int`, `db: DiscussionDatabase`, `after_version: int`, `limit: int` | - | - | `...` |
| `domain_result` | `awaitable` | `TaskVersionConflictError` | - | `result` |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `DiscussionService.history` | `task_id`, `comment_id`, `after_version`, `limit` | `TaskComment` | - | `{...}` |
| `DiscussionService.task` | `task_id`, `writing`, `lock` | `self.db`, `self.db` | - | `...`, `task` |
| `self.db.scalar (backend/app/services/disc….py:DiscussionService.task)` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| task_comment_history | domain_result | 60 | `domain_result(...)` |
| domain_result | HTTPException | 51 | `HTTPException(409, detail=exc.detail(...))` |
| domain_result | exc.detail | 51 | `exc.detail(data not statically known)` |
| domain_result | HTTPException | 53 | `HTTPException(404, detail=str(...))` |
| domain_result | str | 53 | `str(exc)` |
| domain_result | HTTPException | 55 | `HTTPException(422, detail=[...])` |
| domain_result | str | 55 | `str(exc)` |
| domain_result | HTTPException | 57 | `HTTPException(404, detail='Task not found or inaccessible')` |
| task_comment_history | DiscussionService.history | 60 | `DiscussionService(db).history(task_id, comment_id, after_version=after_version, limit=limit)` |
| DiscussionService.history | DiscussionService.task | 115 | `self.task(task_id)` |
| DiscussionService.task | self.db.scalar (backend/app/services/disc….py:DiscussionService.task) | 54 | `self.db.scalar(...)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `domain_result` | `HTTPException` | 51 |
| unresolved_call | `domain_result` | `exc.detail` | 51 |
| external_call | `domain_result` | `HTTPException` | 53 |
| external_call | `domain_result` | `HTTPException` | 55 |
| external_call | `domain_result` | `HTTPException` | 57 |
| unresolved_call | `DiscussionService.task` | `self.db.scalar` | 54 |
| step_limit | `task_comment_history` | `first 12 steps` | 0 |

## Behavior

Reads bounded immutable revisions only after authorizing the original task scope and comment identity. Discussion history is separate from progress and review verdicts.
