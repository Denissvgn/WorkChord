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
    participant p9 as validate_report_scope
    participant p10 as as_utc
    participant p11 as utc_now
    participant p12 as CollectionLimitExceededError
    participant p13 as internal_authority
    participant p14 as DeliveryQueueItem
    participant p15 as DeliveryMetricsResponse
    participant p16 as AuthorityError
    participant p17 as Settings
    participant p18 as DurationSamples
    participant p19 as HTTPException
    participant p20 as exc.detail
    participant p21 as ValueError (backend/app/services/deli…veryMetricsService.report)
    participant p22 as str
    participant p23 as self.db.get
    p0->>p1: DeliveryMetricsService.report
    p0->>p2: domain_result
    p0->>p3: DeliveryMetricsService
    p1->>p4: require_project
    p1->>p5: DeliveryMetricsService._window_observations
    p1->>p6: summarize_observations
    p4->>p7: get_settings
    p6->>p8: _samples
    p1->>p9: validate_report_scope
    p1->>p10: as_utc
    p1->>p11: utc_now
    p1->>p12: CollectionLimitExceededError
    p1->>p13: internal_authority
    p1->>p14: DeliveryQueueItem
    p1->>p15: DeliveryMetricsResponse
    p4->>p16: AuthorityError
    p7->>p17: Settings
    p8->>p18: DurationSamples
    p2-->>p19: HTTPException(409, detail=exc.detail(...))
    p2-->>p20: exc.detail
    p1-->>p21: ValueError (backend/app/services/deli…veryMetricsService.report)('Observation window must be between 1 and 366 elapsed days')
    p2-->>p19: HTTPException(404, detail=str(...))
    p2-->>p22: str(exc)
    p1-->>p23: self.db.get(Project, project_id)
    p2-->>p19: HTTPException(422, detail=[...])
    p1-->>p21: ValueError (backend/app/services/deli…veryMetricsService.report)('Project not found or inaccessible')
    p2-->>p22: str(exc)
    p1-->>p23: self.db.get(Iteration, iteration_id)
    p2-->>p19: HTTPException(404, detail='Task not found or inaccessible')
    p1-->>p21: ValueError (backend/app/services/deli…veryMetricsService.report)('Iteration not found or inaccessible')
```

> Call sequence diagram shows 30 of 186 interactions; 156 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 9 of 66 (57 omitted); unresolved 3 of 85 (82 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/delivery_metrics_service.py:validate_report_scope` | 11 | - | external | 4 |
| `backend/app/authority.py:require_project` | 17 | - | unresolved | 2 |
| `backend/app/authority.py:require_project` | 17 | [backend/app/authority.py](../modules/authority.md) | internal | 1 |
| `backend/app/utils/time.py:as_utc` | 28 | - | unresolved | 2 |
| `backend/app/utils/time.py:utc_now` | 31 | - | external | 1 |
| `backend/app/services/delivery_metrics_service.py:DeliveryMetricsService.report` | 10 | - | external | 20 |
| `backend/app/services/delivery_metrics_service.py:DeliveryMetricsService.report` | 10 | - | unresolved | 41 |
| `backend/app/services/delivery_metrics_service.py:DeliveryMetricsService._window_observations` | 52 | - | unresolved | 29 |
> Omission summary shows 8 of 19 groups; 11 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 36; effect analysis evaluated: 23, partial: 1, unavailable: 12. Counts include steps omitted from the displayed trace.

Collector observations for 24 source steps with known totals: observed: 136, emitted: 126, omitted: 10. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `delivery_metrics` | `available` | `evaluated` | `available` | `8` | `8` | `0` |
| `domain_result` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `exc.detail` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `DeliveryMetricsService.report` | `available` | `partial` | `available` | `29` | `19` | `10` |
| `validate_report_scope` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `ValueError (backend/app/services/deli….py:validate_report_scope)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

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
    s11["11. validate_report_scope"]
    s12["12. ValueError (backend/app/services/deli….py:validate_report_scope)"]
    s1 -->|"domain_result(...)"| s2
    s2 -. "HTTPException(409, detail=exc.detail(...))" .-> s3
    s2 -. "exc.detail(data not statically known)" .-> s4
    s2 -. "HTTPException(404, detail=str(...))" .-> s5
    s2 -. "str(exc)" .-> s6
    s2 -. "HTTPException(422, detail=[...])" .-> s7
    s2 -. "str(exc)" .-> s8
    s2 -. "HTTPException(404, detail='Task not found or inaccessible')" .-> s9
    s1 -->|"DeliveryMetricsService.report(…)"| s10
    s10 -->|"validate_report_scope(project_id, iteration_id, backlog=backlog, all_projects=all_projects, all_projects_backlog=all_projects_backlog)"| s11
    s11 -. "ValueError (backend/app/services/deli….py:validate_report_scope)('Workspace backlog requires all projects')" .-> s12
    b0["mutation recovery.append"]
    s10 -. "mutation recovery.append" .-> b0
    b1["mutation review.sort"]
    s10 -. "mutation review.sort" .-> b1
    b2["mutation recovery.sort"]
    s10 -. "mutation recovery.sort" .-> b2
    click s1 "../modules/routers_task_domain.md"
    click s2 "../modules/routers_task_domain.md"
    click s10 "../modules/delivery_metrics_service.md"
    click s11 "../modules/delivery_metrics_service.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `delivery_metrics` | `db: DB`, `project_id: int \| None`, `iteration_id: int \| None`, `lookback_days: int`, `backlog: bool`, `all_projects: bool`, `all_projects_backlog: bool` | - | - | `...` |
| `domain_result` | `awaitable` | `TaskVersionConflictError` | - | `result` |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `DeliveryMetricsService.report` | `project_id`, `iteration_id`, `lookback_days`, `now`, `backlog`, `all_projects`, `all_projects_backlog` | `self.db`, `Project`, `Iteration`, `DeliveryObservation`, `Task`, `DeliveryObservation`, `Task`, `DeliveryObservation` | - | `DeliveryMetricsResponse(...)` |
| `validate_report_scope` | `project_id`, `iteration_id`, `backlog`, `all_projects`, `all_projects_backlog` | - | - | - |
| `ValueError (backend/app/services/deli….py:validate_report_scope)` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| delivery_metrics | domain_result | 78 | `domain_result(...)` |
| domain_result | HTTPException | 55 | `HTTPException(409, detail=exc.detail(...))` |
| domain_result | exc.detail | 55 | `exc.detail(data not statically known)` |
| domain_result | HTTPException | 57 | `HTTPException(404, detail=str(...))` |
| domain_result | str | 57 | `str(exc)` |
| domain_result | HTTPException | 59 | `HTTPException(422, detail=[...])` |
| domain_result | str | 59 | `str(exc)` |
| domain_result | HTTPException | 61 | `HTTPException(404, detail='Task not found or inaccessible')` |
| delivery_metrics | DeliveryMetricsService.report | 78 | `DeliveryMetricsService(db).report(project_id=project_id, iteration_id=iteration_id, lookback_days=lookback_days, backlog=backlog, all_projects=all_projects, all_projects_backlog=all_projects_backlog)` |
| DeliveryMetricsService.report | validate_report_scope | 157 | `validate_report_scope(project_id, iteration_id, backlog=backlog, all_projects=all_projects, all_projects_backlog=all_projects_backlog)` |
| validate_report_scope | ValueError (backend/app/services/deli….py:validate_report_scope) | 25 | `ValueError('Workspace backlog requires all projects')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `recovery.append` | `DeliveryMetricsService.report` | 208 |
| mutation | `review.sort` | `DeliveryMetricsService.report` | 211 |
| mutation | `recovery.sort` | `DeliveryMetricsService.report` | 212 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `domain_result` | `HTTPException` | 55 |
| unresolved_call | `domain_result` | `exc.detail` | 55 |
| external_call | `domain_result` | `HTTPException` | 57 |
| external_call | `domain_result` | `HTTPException` | 59 |
| external_call | `domain_result` | `HTTPException` | 61 |
| external_call | `validate_report_scope` | `ValueError` | 25 |
| step_limit | `delivery_metrics` | `first 12 steps` | 0 |

## Behavior

This flow starts at `delivery_metrics` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
