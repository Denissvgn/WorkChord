# delivery_metrics

**Entry point:** `delivery_metrics` (`http`)
**Source:** [routers_task_domain](../modules/routers_task_domain.md)
**Modules touched:** [authority](../modules/authority.md), [config](../modules/config.md), [delivery_metrics](../modules/delivery_metrics.md), [delivery_metrics_service](../modules/delivery_metrics_service.md), and 3 more

**Complete modules touched:**

- [authority](../modules/authority.md)
- [config](../modules/config.md)
- [delivery_metrics](../modules/delivery_metrics.md)
- [delivery_metrics_service](../modules/delivery_metrics_service.md)
- [query_limits](../modules/query_limits.md)
- [routers_task_domain](../modules/routers_task_domain.md)
- [time](../modules/time.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as delivery_metrics
    participant p1 as DeliveryMetricsService.report
    participant p2 as domain_result
    participant p3 as DeliveryMetricsService
    participant p4 as require_project
    participant p5 as DeliveryMetricsService._window_observations
    participant p6 as summarize_observations
    participant p7 as get_settings
    participant p8 as _samples
    participant p9 as as_utc
    participant p10 as utc_now
    participant p11 as CollectionLimitExceededError
    participant p12 as internal_authority
    participant p13 as DeliveryQueueItem
    participant p14 as DeliveryMetricsResponse
    participant p15 as AuthorityError
    participant p16 as Settings
    participant p17 as DurationSamples
    participant p18 as HTTPException
    participant p19 as exc.detail
    participant p20 as ValueError
    participant p21 as str
    participant p22 as self.db.get
    p0->>p1: DeliveryMetricsService.report
    p0->>p2: domain_result
    p0->>p3: DeliveryMetricsService
    p1->>p4: require_project
    p1->>p5: DeliveryMetricsService._window_observations
    p1->>p6: summarize_observations
    p4->>p7: get_settings
    p6->>p8: _samples
    p1->>p9: as_utc
    p1->>p10: utc_now
    p1->>p11: CollectionLimitExceededError
    p1->>p12: internal_authority
    p1->>p13: DeliveryQueueItem
    p1->>p14: DeliveryMetricsResponse
    p4->>p15: AuthorityError
    p7->>p16: Settings
    p8->>p17: DurationSamples
    p2-->>p18: HTTPException(409, detail=exc.detail(...))
    p2-->>p19: exc.detail
    p1-->>p20: ValueError('Select a project or an iteration')
    p1-->>p20: ValueError('Observation window must be between 1 and 366 elapsed days')
    p2-->>p18: HTTPException(404, detail=str(...))
    p2-->>p21: str(exc)
    p1-->>p22: self.db.get(Project, project_id)
    p2-->>p18: HTTPException(422, detail=[...])
    p1-->>p20: ValueError('Project not found or inaccessible')
    p2-->>p21: str(exc)
    p1-->>p22: self.db.get(Iteration, iteration_id)
    p2-->>p18: HTTPException(404, detail='Task not found or inaccessible')
    p1-->>p20: ValueError('Iteration not found or inaccessible')
```

> Call sequence diagram shows 30 of 176 interactions; 146 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 10 of 62 (52 omitted); unresolved 3 of 80 (77 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/authority.py:require_project` | 13 | - | unresolved | 2 |
| `backend/app/authority.py:require_project` | 13 | [backend/app/authority.py](../modules/authority.md) | internal | 1 |
| `backend/app/utils/time.py:as_utc` | 24 | - | unresolved | 2 |
| `backend/app/utils/time.py:utc_now` | 27 | - | external | 1 |
| `backend/app/services/delivery_metrics_service.py:DeliveryMetricsService.report` | 10 | - | external | 20 |
| `backend/app/services/delivery_metrics_service.py:DeliveryMetricsService.report` | 10 | - | unresolved | 36 |
| `backend/app/services/delivery_metrics_service.py:DeliveryMetricsService._window_observations` | 43 | - | unresolved | 29 |
| `backend/app/services/delivery_metrics_service.py:DeliveryMetricsService._window_observations` | 43 | - | external | 10 |
> Omission summary shows 8 of 18 groups; 10 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 35; effect analysis evaluated: 22, partial: 1, unavailable: 12. Counts include steps omitted from the displayed trace.

Collector observations for 23 source steps with known totals: observed: 125, emitted: 115, omitted: 10. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `delivery_metrics` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `domain_result` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `exc.detail` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `DeliveryMetricsService.report` | `available` | `partial` | `available` | `26` | `16` | `10` |
| `ValueError` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `ValueError` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. delivery_metrics"]
    s2["2. domain_result"]
    s3["3. HTTPException"]
    s4["4. exc.detail"]
    s5["5. HTTPException"]
    s6["6. str"]
    s7["7. HTTPException"]
    s8["8. str"]
    s9["9. HTTPException"]
    s10["10. DeliveryMetricsService.report"]
    s11["11. ValueError"]
    s12["12. ValueError"]
    s1 -->|"domain_result(...)"| s2
    s2 -. "HTTPException(409, detail=exc.detail(...))" .-> s3
    s2 -. "exc.detail(data not statically known)" .-> s4
    s2 -. "HTTPException(404, detail=str(...))" .-> s5
    s2 -. "str(exc)" .-> s6
    s2 -. "HTTPException(422, detail=[...])" .-> s7
    s2 -. "str(exc)" .-> s8
    s2 -. "HTTPException(404, detail='Task not found or inaccessible')" .-> s9
    s1 -->|"DeliveryMetricsService.report(project_id=project_id, iteration_id=iteration_id, lookback_days=lookback_days)"| s10
    s10 -. "ValueError('Select a project or an iteration')" .-> s11
    s10 -. "ValueError('Observation window must be between 1 and 366 elapsed days')" .-> s12
    b0["mutation recovery.append"]
    s10 -. "mutation recovery.append" .-> b0
    b1["mutation review.sort"]
    s10 -. "mutation review.sort" .-> b1
    b2["mutation recovery.sort"]
    s10 -. "mutation recovery.sort" .-> b2
    click s1 "../modules/routers_task_domain.md"
    click s2 "../modules/routers_task_domain.md"
    click s10 "../modules/delivery_metrics_service.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `delivery_metrics` | `db: DB`, `project_id: int \| None`, `iteration_id: int \| None`, `lookback_days: int` | - | - | `...` |
| `domain_result` | `awaitable` | `TaskVersionConflictError` | - | `result` |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `DeliveryMetricsService.report` | `project_id`, `iteration_id`, `lookback_days`, `now` | `self.db`, `Project`, `Iteration`, `DeliveryObservation`, `Task`, `DeliveryObservation`, `Task`, `DeliveryObservation` | - | `DeliveryMetricsResponse(...)` |
| `ValueError` | - | - | - | - |
| `ValueError` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| delivery_metrics | domain_result | 71 | `domain_result(...)` |
| domain_result | HTTPException | 51 | `HTTPException(409, detail=exc.detail(...))` |
| domain_result | exc.detail | 51 | `exc.detail(data not statically known)` |
| domain_result | HTTPException | 53 | `HTTPException(404, detail=str(...))` |
| domain_result | str | 53 | `str(exc)` |
| domain_result | HTTPException | 55 | `HTTPException(422, detail=[...])` |
| domain_result | str | 55 | `str(exc)` |
| domain_result | HTTPException | 57 | `HTTPException(404, detail='Task not found or inaccessible')` |
| delivery_metrics | DeliveryMetricsService.report | 71 | `DeliveryMetricsService(db).report(project_id=project_id, iteration_id=iteration_id, lookback_days=lookback_days)` |
| DeliveryMetricsService.report | ValueError | 143 | `ValueError('Select a project or an iteration')` |
| DeliveryMetricsService.report | ValueError | 145 | `ValueError('Observation window must be between 1 and 366 elapsed days')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `recovery.append` | `DeliveryMetricsService.report` | 190 |
| mutation | `review.sort` | `DeliveryMetricsService.report` | 193 |
| mutation | `recovery.sort` | `DeliveryMetricsService.report` | 194 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `domain_result` | `HTTPException` | 51 |
| unresolved_call | `domain_result` | `exc.detail` | 51 |
| external_call | `domain_result` | `HTTPException` | 53 |
| external_call | `domain_result` | `HTTPException` | 55 |
| external_call | `domain_result` | `HTTPException` | 57 |
| external_call | `DeliveryMetricsService.report` | `ValueError` | 143 |
| external_call | `DeliveryMetricsService.report` | `ValueError` | 145 |
| step_limit | `delivery_metrics` | `first 12 steps` | 0 |

## Behavior

This flow starts at `delivery_metrics` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
