# create_subtask

**Entry point:** `create_subtask` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [iteration_service](../modules/iteration_service.md), [tasks](../modules/tasks.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as create_subtask
    participant p1 as service.create_subtask
    participant p2 as HTTPException
    participant p3 as str
    participant p4 as IterationService
    participant p5 as IterationService.get_by_id
    participant p6 as service.task_to_response
    participant p7 as self.db.execute
    participant p8 as select(…).options(…).where
    participant p9 as select(…).options
    participant p10 as select
    participant p11 as selectinload
    participant p12 as result.scalar_one_or_none
    p0-->>p1: service.create_subtask(task_id, data)
    p0-->>p2: HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))
    p0-->>p3: str(e)
    p0-->>p2: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)
    p0->>p4: IterationService
    p0->>p5: IterationService.get_by_id
    p0-->>p6: service.task_to_response(task, ...)
    p5-->>p7: self.db.execute(...)
    p5-->>p8: select(…).options(…).where(...)
    p5-->>p9: select(…).options(selectinload(...), selectinload(...))
    p5-->>p10: select(Iteration)
    p5-->>p11: selectinload(Iteration.calendar)
    p5-->>p11: selectinload(Iteration.project)
    p5-->>p12: result.scalar_one_or_none
```

> Call sequence diagram shows 14 of 14 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 6 of 6 (0 omitted); unresolved 6 of 6 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 3; effect analysis evaluated: 2, partial: 0, unavailable: 1. Counts include steps omitted from the displayed trace.

Collector observations for 2 source steps with known totals: observed: 10, emitted: 10, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `create_subtask` | `available` | `evaluated` | `available` | `7` | `7` | `0` |
| `service.create_subtask` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `IterationService` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `IterationService.get_by_id` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `self.db.execute` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).options(…).where` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).options` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `selectinload` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. create_subtask"]
    s2["2. service.create_subtask"]
    s3["3. HTTPException"]
    s4["4. str"]
    s5["5. HTTPException"]
    s6["6. IterationService"]
    s7["7. IterationService.get_by_id"]
    s8["8. self.db.execute"]
    s9["9. select(…).options(…).where"]
    s10["10. select(…).options"]
    s11["11. select"]
    s12["12. selectinload"]
    s1 -. "service.create_subtask(task_id, data)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s3
    s1 -. "str(e)" .-> s4
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s5
    s1 -->|"IterationService(db)"| s6
    s1 -->|"IterationService.get_by_id(task.iteration_id)"| s7
    s7 -. "self.db.execute(...)" .-> s8
    s7 -. "select(…).options(…).where(...)" .-> s9
    s7 -. "select(…).options(selectinload(...), selectinload(...))" .-> s10
    s7 -. "select(Iteration)" .-> s11
    s7 -. "selectinload(Iteration.calendar)" .-> s12
    click s1 "../modules/tasks.md"
    click s6 "../modules/iteration_service.md"
    click s7 "../modules/iteration_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `create_subtask` | `task_id: int`, `data: TaskCreate`, `service: Annotated[TaskService, Depends(get_task_service)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | `status`, `status` | - | `service.task_to_response(...)` |
| `service.create_subtask` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `IterationService` | - | - | - | - |
| `IterationService.get_by_id` | `iteration_id: int` | `Iteration` | - | `result.scalar_one_or_none(...)` |
| `self.db.execute` | - | - | - | - |
| `select(…).options(…).where` | - | - | - | - |
| `select(…).options` | - | - | - | - |
| `select` | - | - | - | - |
| `selectinload` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| create_subtask | service.create_subtask | 573 | `service.create_subtask(task_id, data)` |
| create_subtask | HTTPException | 575 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| create_subtask | str | 577 | `str(e)` |
| create_subtask | HTTPException | 580 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| create_subtask | IterationService | 585 | `IterationService(db)` |
| create_subtask | IterationService.get_by_id | 586 | `iteration_service.get_by_id(task.iteration_id)` |
| IterationService.get_by_id | self.db.execute | 323 | `self.db.execute(...)` |
| IterationService.get_by_id | select(…).options(…).where | 324 | `select(Iteration).options(selectinload(Iteration.calendar), selectinload(Iteration.project)).where(...)` |
| IterationService.get_by_id | select(…).options | 324 | `select(Iteration).options(selectinload(...), selectinload(...))` |
| IterationService.get_by_id | select | 324 | `select(Iteration)` |
| IterationService.get_by_id | selectinload | 326 | `selectinload(Iteration.calendar)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `create_subtask` | `service.create_subtask` | 573 |
| external_call | `create_subtask` | `HTTPException` | 575 |
| external_call | `create_subtask` | `HTTPException` | 580 |
| unresolved_call | `IterationService.get_by_id` | `self.db.execute` | 323 |
| unresolved_call | `IterationService.get_by_id` | `select(Iteration).options(selectinload(Iteration.calendar), selectinload(Iteration.project)).where` | 324 |
| unresolved_call | `IterationService.get_by_id` | `select(Iteration).options` | 324 |
| external_call | `IterationService.get_by_id` | `select` | 324 |
| external_call | `IterationService.get_by_id` | `selectinload` | 326 |
| step_limit | `create_subtask` | `first 12 steps` | 0 |

## Behavior

This flow starts at `create_subtask` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
