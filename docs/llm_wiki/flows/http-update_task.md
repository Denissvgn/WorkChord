# update_task

**Entry point:** `update_task` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [iteration_service](../modules/iteration_service.md), [tasks](../modules/tasks.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as update_task
    participant p1 as service.update
    participant p2 as _raise_task_version_conflict
    participant p3 as HTTPException (backend/app/routers/tasks.py:update_task)
    participant p4 as str
    participant p5 as IterationService
    participant p6 as IterationService.get_by_id
    participant p7 as service.task_to_response
    participant p8 as HTTPException (backend/app/routers/tasks…aise_task_version_conflict)
    participant p9 as self.db.execute
    participant p10 as exc.detail
    participant p11 as select(…).options(…).where
    participant p12 as select(…).options
    participant p13 as select
    participant p14 as selectinload
    participant p15 as result.scalar_one_or_none
    p0-->>p1: service.update(task_id, data)
    p0->>p2: _raise_task_version_conflict
    p0-->>p3: HTTPException (backend/app/routers/tasks.py:update_task)(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))
    p0-->>p4: str(e)
    p0-->>p3: HTTPException (backend/app/routers/tasks.py:update_task)(status_code=status.HTTP_404_NOT_FOUND, detail=...)
    p0->>p5: IterationService
    p0->>p6: IterationService.get_by_id
    p0-->>p7: service.task_to_response(task, ...)
    p2-->>p8: HTTPException (backend/app/routers/tasks…aise_task_version_conflict)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p6-->>p9: self.db.execute(...)
    p2-->>p10: exc.detail
    p6-->>p11: select(…).options(…).where(...)
    p6-->>p12: select(…).options(selectinload(...), selectinload(...))
    p6-->>p13: select(Iteration)
    p6-->>p14: selectinload(Iteration.calendar)
    p6-->>p14: selectinload(Iteration.project)
    p6-->>p15: result.scalar_one_or_none
```

> Call sequence diagram shows 17 of 17 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 7 of 7 (0 omitted); unresolved 7 of 7 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 4; effect analysis evaluated: 3, partial: 0, unavailable: 1. Counts include steps omitted from the displayed trace.

Collector observations for 3 source steps with known totals: observed: 14, emitted: 14, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `update_task` | `available` | `evaluated` | `available` | `9` | `9` | `0` |
| `service.update` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_raise_task_version_conflict` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `HTTPException (backend/app/routers/tasks…aise_task_version_conflict)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `exc.detail` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/tasks.py:update_task)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/tasks.py:update_task)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `IterationService` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `IterationService.get_by_id` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `self.db.execute` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).options(…).where` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

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
    s10["10. IterationService.get_by_id"]
    s11["11. self.db.execute"]
    s12["12. select(…).options(…).where"]
    s1 -. "service.update(task_id, data)" .-> s2
    s1 -->|"_raise_task_version_conflict(exc)"| s3
    s3 -. "HTTPException (backend/app/routers/tasks…aise_task_version_conflict)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))" .-> s4
    s3 -. "exc.detail(data not statically known)" .-> s5
    s1 -. "HTTPException (backend/app/routers/tasks.py:update_task)(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s6
    s1 -. "str(e)" .-> s7
    s1 -. "HTTPException (backend/app/routers/tasks.py:update_task)(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s8
    s1 -->|"IterationService(db)"| s9
    s1 -->|"IterationService.get_by_id(task.iteration_id)"| s10
    s10 -. "self.db.execute(...)" .-> s11
    s10 -. "select(…).options(…).where(...)" .-> s12
    b0["mutation service.update"]
    s1 -. "mutation service.update" .-> b0
    click s1 "../modules/tasks.md"
    click s3 "../modules/tasks.md"
    click s9 "../modules/iteration_service.md"
    click s10 "../modules/iteration_service.md"
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
| `IterationService.get_by_id` | `iteration_id: int` | `Iteration` | - | `result.scalar_one_or_none(...)` |
| `self.db.execute` | - | - | - | - |
| `select(…).options(…).where` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| update_task | service.update | 334 | `service.update(task_id, data)` |
| update_task | _raise_task_version_conflict | 336 | `_raise_task_version_conflict(exc)` |
| _raise_task_version_conflict | HTTPException (backend/app/routers/tasks…aise_task_version_conflict) | 59 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _raise_task_version_conflict | exc.detail | 61 | `exc.detail(data not statically known)` |
| update_task | HTTPException (backend/app/routers/tasks.py:update_task) | 338 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| update_task | str | 340 | `str(e)` |
| update_task | HTTPException (backend/app/routers/tasks.py:update_task) | 343 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| update_task | IterationService | 348 | `IterationService(db)` |
| update_task | IterationService.get_by_id | 349 | `iteration_service.get_by_id(task.iteration_id)` |
| IterationService.get_by_id | self.db.execute | 323 | `self.db.execute(...)` |
| IterationService.get_by_id | select(…).options(…).where | 324 | `select(Iteration).options(selectinload(Iteration.calendar), selectinload(Iteration.project)).where(...)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `service.update` | `update_task` | 334 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `_raise_task_version_conflict` | `HTTPException` | 59 |
| unresolved_call | `_raise_task_version_conflict` | `exc.detail` | 61 |
| external_call | `update_task` | `HTTPException` | 338 |
| external_call | `update_task` | `HTTPException` | 343 |
| unresolved_call | `IterationService.get_by_id` | `self.db.execute` | 323 |
| unresolved_call | `IterationService.get_by_id` | `select(Iteration).options(selectinload(Iteration.calendar), selectinload(Iteration.project)).where` | 324 |
| step_limit | `update_task` | `first 12 steps` | 0 |

## Behavior

This flow starts at `update_task` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

Backlog project changes require edit permission in both scopes. Project locks are acquired in ascending ID order and the task scope is rechecked before writing. The complete subtree must have no incoming or outgoing dependency across its boundary. Both backlogs receive transactional recovery points, descendants reserve one version per command, and rejected moves roll everything back. Actual dependency changes invalidate current progress and acceptance through general updates and individual add/remove commands. Immutable evidence history remains available, a command reserves one task version, and no-op dependency requests retain their current version. Locked graph relationships are loaded explicitly before applying a dependency update.
