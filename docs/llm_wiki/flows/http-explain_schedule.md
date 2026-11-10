# explain_schedule

**Entry point:** `explain_schedule` (`http`)
**Source:** [routers_llm](../modules/routers_llm.md)
**Modules touched:** [routers_llm](../modules/routers_llm.md), [scheduler_service](../modules/scheduler_service.md), [schemas_llm](../modules/schemas_llm.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as explain_schedule
    participant p1 as SchedulerService
    participant p2 as scheduler_service.schedule_iteration
    participant p3 as HTTPException
    participant p4 as ExplainScheduleRequest
    participant p5 as db.rollback
    participant p6 as llm_service.explain_schedule
    p0->>p1: SchedulerService
    p0-->>p2: scheduler_service.schedule_iteration(iteration_id)
    p0-->>p3: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)
    p0->>p4: ExplainScheduleRequest
    p0-->>p5: db.rollback
    p0-->>p6: llm_service.explain_schedule(decisions=schedule_result.decisions, workload_issues=schedule_result.workload_issues, detail_level=request.detail_level)
```

> Call sequence diagram shows 6 of 6 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 1 (0 omitted); unresolved 3 of 3 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 3; effect analysis evaluated: 1, partial: 0, unavailable: 2. Counts include steps omitted from the displayed trace.

Collector observations for 1 source steps with known totals: observed: 6, emitted: 6, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `explain_schedule` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `SchedulerService` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `scheduler_service.schedule_iteration` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `ExplainScheduleRequest` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `db.rollback` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `llm_service.explain_schedule` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. explain_schedule"]
    s2["2. SchedulerService"]
    s3["3. scheduler_service.schedule_iteration"]
    s4["4. HTTPException"]
    s5["5. ExplainScheduleRequest"]
    s6["6. db.rollback"]
    s7["7. llm_service.explain_schedule"]
    s1 -->|"SchedulerService(db)"| s2
    s1 -. "scheduler_service.schedule_iteration(iteration_id)" .-> s3
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s4
    s1 -->|"ExplainScheduleRequest(data not statically known)"| s5
    s1 -. "db.rollback(data not statically known)" .-> s6
    s1 -. "llm_service.explain_schedule(decisions=schedule_result.decisions, workload_issues=schedule_result.workload_issues, detail_level=request.detail_level)" .-> s7
    click s1 "../modules/routers_llm.md"
    click s2 "../modules/scheduler_service.md"
    click s5 "../modules/schemas_llm.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `explain_schedule` | `iteration_id: int`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]`, `llm_service: Annotated[LLMService, Depends(get_llm_service)]`, `data: Annotated[ExplainScheduleRequest \| None, Body()]` | `status` | - | `...` |
| `SchedulerService` | - | - | - | - |
| `scheduler_service.schedule_iteration` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `ExplainScheduleRequest` | - | - | - | - |
| `db.rollback` | - | - | - | - |
| `llm_service.explain_schedule` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| explain_schedule | SchedulerService | 251 | `SchedulerService(db)` |
| explain_schedule | scheduler_service.schedule_iteration | 252 | `scheduler_service.schedule_iteration(iteration_id)` |
| explain_schedule | HTTPException | 255 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| explain_schedule | ExplainScheduleRequest | 260 | `ExplainScheduleRequest(data not statically known)` |
| explain_schedule | db.rollback | 261 | `db.rollback(data not statically known)` |
| explain_schedule | llm_service.explain_schedule | 262 | `llm_service.explain_schedule(decisions=schedule_result.decisions, workload_issues=schedule_result.workload_issues, detail_level=request.detail_level)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `explain_schedule` | `scheduler_service.schedule_iteration` | 252 |
| external_call | `explain_schedule` | `HTTPException` | 255 |
| unresolved_call | `explain_schedule` | `db.rollback` | 261 |
| unresolved_call | `explain_schedule` | `llm_service.explain_schedule` | 262 |

## Behavior

This flow starts at `explain_schedule` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
