# planning_input_context

**Entry point:** `planning_input_context` (`http`)
**Source:** [routers_task_domain](../modules/routers_task_domain.md)
**Modules touched:** [commands](../modules/commands.md), [planning_input_context](../modules/planning_input_context.md), [routers_task_domain](../modules/routers_task_domain.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as planning_input_context
    participant p1 as HTTPException (backend/app/routers/task_….py:planning_input_context)
    participant p2 as domain_result
    participant p3 as HTTPException (backend/app/routers/task_domain.py:domain_result)
    participant p4 as exc.detail
    participant p5 as str
    participant p6 as observe_planning_input
    participant p7 as revisions
    participant p8 as list
    participant p9 as (…).mappings().first
    participant p10 as (…).mappings
    participant p11 as db.execute
    participant p12 as select(…).where
    participant p13 as select
    participant p14 as LookupError
    participant p15 as PlanningConflict
    participant p16 as len
    participant p17 as json.dumps(…).encode
    participant p18 as json.dumps
    participant p19 as dict
    p0-->>p1: HTTPException (backend/app/routers/task_….py:planning_input_context)
    p0->>p2: domain_result
    p2-->>p3: HTTPException (backend/app/routers/task_domain.py:domain_result)
    p2-->>p4: exc.detail
    p2-->>p3: HTTPException (backend/app/routers/task_domain.py:domain_result)
    p2-->>p5: str
    p2-->>p3: HTTPException (backend/app/routers/task_domain.py:domain_result)
    p2-->>p5: str
    p2-->>p3: HTTPException (backend/app/routers/task_domain.py:domain_result)
    p0->>p6: observe_planning_input
    p6-->>p7: revisions
    p6-->>p8: list
    p6-->>p9: (…).mappings().first
    p6-->>p10: (…).mappings
    p6-->>p11: db.execute
    p6-->>p12: select(…).where
    p6-->>p13: select
    p6-->>p14: LookupError
    p6-->>p7: revisions
    p6->>p15: PlanningConflict
    p6-->>p16: len
    p6-->>p17: json.dumps(…).encode
    p6-->>p18: json.dumps
    p6->>p15: PlanningConflict
    p6-->>p19: dict
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. planning_input_context"]
    s2["2. HTTPException (backend/app/routers/task_….py:planning_input_context)"]
    s3["3. domain_result"]
    s4["4. HTTPException (backend/app/routers/task_domain.py:domain_result)"]
    s5["5. exc.detail"]
    s6["6. HTTPException (backend/app/routers/task_domain.py:domain_result)"]
    s7["7. str"]
    s8["8. HTTPException (backend/app/routers/task_domain.py:domain_result)"]
    s9["9. str"]
    s10["10. HTTPException (backend/app/routers/task_domain.py:domain_result)"]
    s11["11. observe_planning_input"]
    s12["12. revisions"]
    s1 -. "HTTPException (backend/app/routers/task_….py:planning_input_context)(…)" .-> s2
    s1 -->|"domain_result(observe_planning_input(...))"| s3
    s3 -. "HTTPException (backend/app/routers/task_domain.py:domain_result)(409, detail=exc.detail(...))" .-> s4
    s3 -. "exc.detail(data not statically known)" .-> s5
    s3 -. "HTTPException (backend/app/routers/task_domain.py:domain_result)(404, detail=str(...))" .-> s6
    s3 -. "str(exc)" .-> s7
    s3 -. "HTTPException (backend/app/routers/task_domain.py:domain_result)(422, detail=[...])" .-> s8
    s3 -. "str(exc)" .-> s9
    s3 -. "HTTPException (backend/app/routers/task_domain.py:domain_result)(404, detail='Task not found or inaccessible')" .-> s10
    s1 -->|"observe_planning_input(db, kind, resource_id, creating_member=creating_member)"| s11
    s11 -. "revisions(data not statically known)" .-> s12
    click s1 "../modules/routers_task_domain.md"
    click s3 "../modules/routers_task_domain.md"
    click s11 "../modules/planning_input_context.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `planning_input_context` | `kind: Literal['calendar', 'project', 'iteration', 'profile', 'member', 'vacation']`, `resource_id: int`, `db: DB`, `creating_member: bool` | - | - | `...` |
| `HTTPException (backend/app/routers/task_….py:planning_input_context)` | - | - | - | - |
| `domain_result` | `awaitable` | `TaskVersionConflictError` | - | `result` |
| `HTTPException (backend/app/routers/task_domain.py:domain_result)` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `HTTPException (backend/app/routers/task_domain.py:domain_result)` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException (backend/app/routers/task_domain.py:domain_result)` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException (backend/app/routers/task_domain.py:domain_result)` | - | - | - | - |
| `observe_planning_input` | `db`, `kind`, `resource_id`, `creating_member` | - | - | `{...}` |
| `revisions` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| planning_input_context | HTTPException (backend/app/routers/task_….py:planning_input_context) | 33 | `HTTPException(422, detail='Use a positive planning resource identity and a supported member-create context.')` |
| planning_input_context | domain_result | 35 | `domain_result(observe_planning_input(...))` |
| domain_result | HTTPException (backend/app/routers/task_domain.py:domain_result) | 42 | `HTTPException(409, detail=exc.detail(...))` |
| domain_result | exc.detail | 42 | `exc.detail(data not statically known)` |
| domain_result | HTTPException (backend/app/routers/task_domain.py:domain_result) | 44 | `HTTPException(404, detail=str(...))` |
| domain_result | str | 44 | `str(exc)` |
| domain_result | HTTPException (backend/app/routers/task_domain.py:domain_result) | 46 | `HTTPException(422, detail=[...])` |
| domain_result | str | 46 | `str(exc)` |
| domain_result | HTTPException (backend/app/routers/task_domain.py:domain_result) | 48 | `HTTPException(404, detail='Task not found or inaccessible')` |
| planning_input_context | observe_planning_input | 35 | `observe_planning_input(db, kind, resource_id, creating_member=creating_member)` |
| observe_planning_input | revisions | 87 | `revisions(data not statically known)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `planning_input_context` | `HTTPException` | 33 |
| external_call | `domain_result` | `HTTPException` | 42 |
| unresolved_call | `domain_result` | `exc.detail` | 42 |
| external_call | `domain_result` | `HTTPException` | 44 |
| external_call | `domain_result` | `HTTPException` | 46 |
| external_call | `domain_result` | `HTTPException` | 48 |
| unresolved_call | `observe_planning_input` | `revisions` | 87 |
| step_limit | `planning_input_context` | `first 12 steps` | 0 |

## Behavior

This flow starts at `planning_input_context` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
