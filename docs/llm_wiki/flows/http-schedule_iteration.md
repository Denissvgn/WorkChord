# schedule_iteration

**Entry point:** `schedule_iteration` (`http`)
**Source:** [routers_gantt](../modules/routers_gantt.md)
**Modules touched:** [iteration_service](../modules/iteration_service.md), [routers_gantt](../modules/routers_gantt.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as schedule_iteration
    participant p1 as IterationService
    participant p2 as IterationService.get_by_id
    participant p3 as HTTPException
    participant p4 as service.schedule_iteration
    participant p5 as self.db.execute
    participant p6 as select(…).options(…).where
    participant p7 as select(…).options
    participant p8 as select
    participant p9 as selectinload
    participant p10 as result.scalar_one_or_none
    p0->>p1: IterationService
    p0->>p2: IterationService.get_by_id
    p0-->>p3: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)
    p0-->>p4: service.schedule_iteration(iteration_id, expected_revision=..., expected_planning_revision=..., commit_baseline=True, rebaseline_reason=...)
    p2-->>p5: self.db.execute(...)
    p2-->>p6: select(…).options(…).where(...)
    p2-->>p7: select(…).options(selectinload(...), selectinload(...))
    p2-->>p8: select(Iteration)
    p2-->>p9: selectinload(Iteration.calendar)
    p2-->>p9: selectinload(Iteration.project)
    p2-->>p10: result.scalar_one_or_none
```

> Call sequence diagram shows 11 of 11 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 4 of 4 (0 omitted); unresolved 5 of 5 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 3; effect analysis evaluated: 2, partial: 0, unavailable: 1. Counts include steps omitted from the displayed trace.

Collector observations for 2 source steps with known totals: observed: 9, emitted: 9, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `schedule_iteration` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `IterationService` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `IterationService.get_by_id` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `self.db.execute` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).options(…).where` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).options` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `selectinload` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `selectinload` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `result.scalar_one_or_none` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `service.schedule_iteration` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. schedule_iteration"]
    s2["2. IterationService"]
    s3["3. IterationService.get_by_id"]
    s4["4. self.db.execute"]
    s5["5. select(…).options(…).where"]
    s6["6. select(…).options"]
    s7["7. select"]
    s8["8. selectinload"]
    s9["9. selectinload"]
    s10["10. result.scalar_one_or_none"]
    s11["11. HTTPException"]
    s12["12. service.schedule_iteration"]
    s1 -->|"IterationService(db)"| s2
    s1 -->|"IterationService.get_by_id(iteration_id)"| s3
    s3 -. "self.db.execute(...)" .-> s4
    s3 -. "select(…).options(…).where(...)" .-> s5
    s3 -. "select(…).options(selectinload(...), selectinload(...))" .-> s6
    s3 -. "select(Iteration)" .-> s7
    s3 -. "selectinload(Iteration.calendar)" .-> s8
    s3 -. "selectinload(Iteration.project)" .-> s9
    s3 -. "result.scalar_one_or_none(data not statically known)" .-> s10
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s11
    s1 -. "service.schedule_iteration(iteration_id, expected_revision=..., expected_planning_revision=..., commit_baseline=True, rebaseline_reason=...)" .-> s12
    click s1 "../modules/routers_gantt.md"
    click s2 "../modules/iteration_service.md"
    click s3 "../modules/iteration_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `schedule_iteration` | `iteration_id: int`, `service: Annotated[SchedulerService, Depends(get_scheduler_service)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]`, `data: ScheduleApplyRequest \| None` | `status` | - | `result` |
| `IterationService` | - | - | - | - |
| `IterationService.get_by_id` | `iteration_id: int` | `Iteration` | - | `result.scalar_one_or_none(...)` |
| `self.db.execute` | - | - | - | - |
| `select(…).options(…).where` | - | - | - | - |
| `select(…).options` | - | - | - | - |
| `select` | - | - | - | - |
| `selectinload` | - | - | - | - |
| `selectinload` | - | - | - | - |
| `result.scalar_one_or_none` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `service.schedule_iteration` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| schedule_iteration | IterationService | 40 | `IterationService(db)` |
| schedule_iteration | IterationService.get_by_id | 41 | `iteration_service.get_by_id(iteration_id)` |
| IterationService.get_by_id | self.db.execute | 323 | `self.db.execute(...)` |
| IterationService.get_by_id | select(…).options(…).where | 324 | `select(Iteration).options(selectinload(Iteration.calendar), selectinload(Iteration.project)).where(...)` |
| IterationService.get_by_id | select(…).options | 324 | `select(Iteration).options(selectinload(...), selectinload(...))` |
| IterationService.get_by_id | select | 324 | `select(Iteration)` |
| IterationService.get_by_id | selectinload | 326 | `selectinload(Iteration.calendar)` |
| IterationService.get_by_id | selectinload | 327 | `selectinload(Iteration.project)` |
| IterationService.get_by_id | result.scalar_one_or_none | 331 | `result.scalar_one_or_none(data not statically known)` |
| schedule_iteration | HTTPException | 44 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| schedule_iteration | service.schedule_iteration | 49 | `service.schedule_iteration(iteration_id, expected_revision=..., expected_planning_revision=..., commit_baseline=True, rebaseline_reason=...)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `IterationService.get_by_id` | `self.db.execute` | 323 |
| unresolved_call | `IterationService.get_by_id` | `select(Iteration).options(selectinload(Iteration.calendar), selectinload(Iteration.project)).where` | 324 |
| unresolved_call | `IterationService.get_by_id` | `select(Iteration).options` | 324 |
| external_call | `IterationService.get_by_id` | `select` | 324 |
| external_call | `IterationService.get_by_id` | `selectinload` | 326 |
| external_call | `IterationService.get_by_id` | `selectinload` | 327 |
| unresolved_call | `IterationService.get_by_id` | `result.scalar_one_or_none` | 331 |
| external_call | `schedule_iteration` | `HTTPException` | 44 |
| unresolved_call | `schedule_iteration` | `service.schedule_iteration` | 49 |

## Behavior

Applies the scheduler under shared planning and iteration reservations. A supplied stale planning basis conflicts. Canonical absence, calendar and allocation constraints protect commitments, while actual execution dates remain unchanged. Forecasts outside allocation dates cannot be silently committed.
