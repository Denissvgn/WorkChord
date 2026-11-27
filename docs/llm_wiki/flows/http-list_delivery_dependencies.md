# list_delivery_dependencies

**Entry point:** `list_delivery_dependencies` (`http`)
**Source:** [delivery_dependencies](../modules/delivery_dependencies.md)
**Modules touched:** [authority](../modules/authority.md), [config](../modules/config.md), [delivery_dependencies](../modules/delivery_dependencies.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), and 4 more

**Complete modules touched:**

- [authority](../modules/authority.md)
- [config](../modules/config.md)
- [delivery_dependencies](../modules/delivery_dependencies.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [github_reconciliation_service](../modules/github_reconciliation_service.md)
- [routers_task_domain](../modules/routers_task_domain.md)
- [task_replacement_service](../modules/task_replacement_service.md)
- [task_service](../modules/task_service.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_delivery_dependencies
    participant p1 as DeliveryDependencyService.projection
    participant p2 as domain_result
    participant p3 as DeliveryDependencyService
    participant p4 as require_project
    participant p5 as DeliveryDependencyService._accepted
    participant p6 as DeliveryDependencyService._merge_evidence
    participant p7 as get_settings
    participant p8 as delivering_leaves
    participant p9 as DeliveryDependencyService._hold
    participant p10 as TaskService._task_subtree_ids
    participant p11 as GitHubReconciliationService._pull_links
    participant p12 as TaskService
    participant p13 as GitHubReconciliationService
    participant p14 as AuthorityError
    participant p15 as pull_state
    participant p16 as Settings
    participant p17 as internal_authority
    participant p18 as HTTPException
    participant p19 as self.db.scalar
    participant p20 as exc.detail
    participant p21 as select(…).where (backend/app/services/deli…encyService.projection, 1)
    participant p22 as select (backend/app/services/deli…endencyService.projection)
    participant p23 as str
    participant p24 as ValueError
    participant p25 as (…).all (backend/app/services/deli…endencyService.projection)
    participant p26 as self.db.scalars (backend/app/services/deli…endencyService.projection)
    p0->>p1: DeliveryDependencyService.projection
    p0->>p2: domain_result
    p0->>p3: DeliveryDependencyService
    p1->>p4: require_project
    p1->>p5: DeliveryDependencyService._accepted
    p1->>p6: DeliveryDependencyService._merge_evidence
    p4->>p7: get_settings
    p5->>p8: delivering_leaves
    p1->>p9: DeliveryDependencyService._hold
    p5->>p10: TaskService._task_subtree_ids
    p6->>p11: GitHubReconciliationService._pull_links
    p5->>p12: TaskService
    p6->>p13: GitHubReconciliationService
    p4->>p14: AuthorityError
    p6->>p15: pull_state
    p7->>p16: Settings
    p8->>p17: internal_authority
    p2-->>p18: HTTPException(409, detail=exc.detail(...))
    p1-->>p19: self.db.scalar(...)
    p2-->>p20: exc.detail
    p1-->>p21: select(…).where (backend/app/services/deli…encyService.projection, 1)(...)
    p2-->>p18: HTTPException(404, detail=str(...))
    p1-->>p22: select (backend/app/services/deli…endencyService.projection)(Task)
    p2-->>p23: str(exc)
    p1-->>p24: ValueError('Task not found or inaccessible')
    p2-->>p18: HTTPException(422, detail=[...])
    p2-->>p23: str(exc)
    p1-->>p25: (…).all (backend/app/services/deli…endencyService.projection)
    p2-->>p18: HTTPException(404, detail='Task not found or inaccessible')
    p1-->>p26: self.db.scalars (backend/app/services/deli…endencyService.projection)(...)
```

> Call sequence diagram shows 30 of 109 interactions; 79 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 8 of 31 (23 omitted); unresolved 5 of 58 (53 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/authority.py:require_project` | 15 | - | unresolved | 2 |
| `backend/app/authority.py:require_project` | 15 | [backend/app/authority.py](../modules/authority.md) | internal | 1 |
| `backend/app/services/delivery_dependency_service.py:DeliveryDependencyService.projection` | 10 | - | unresolved | 10 |
| `backend/app/services/delivery_dependency_service.py:DeliveryDependencyService.projection` | 10 | - | external | 2 |
| `backend/app/services/task_service.py:TaskService._task_subtree_ids` | 34 | - | unresolved | 5 |
| `backend/app/services/task_service.py:TaskService._task_subtree_ids` | 34 | - | external | 1 |
| `backend/app/services/delivery_dependency_service.py:DeliveryDependencyService._accepted` | 33 | - | unresolved | 7 |
| `backend/app/services/delivery_dependency_service.py:DeliveryDependencyService._accepted` | 33 | - | external | 4 |
> Omission summary shows 8 of 20 groups; 12 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 21; effect analysis evaluated: 15, partial: 0, unavailable: 6. Counts include steps omitted from the displayed trace.

Collector observations for 15 source steps with known totals: observed: 74, emitted: 74, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `list_delivery_dependencies` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `domain_result` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `exc.detail` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `DeliveryDependencyService.projection` | `available` | `evaluated` | `available` | `13` | `13` | `0` |
| `self.db.scalar` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).where (backend/app/services/deli…encyService.projection, 1)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. list_delivery_dependencies"]
    s2["2. domain_result"]
    s3["3. HTTPException"]
    s4["4. exc.detail"]
    s5["5. HTTPException"]
    s6["6. str"]
    s7["7. HTTPException"]
    s8["8. str"]
    s9["9. HTTPException"]
    s10["10. DeliveryDependencyService.projection"]
    s11["11. self.db.scalar"]
    s12["12. select(…).where (backend/app/services/deli…encyService.projection, 1)"]
    s1 -->|"domain_result(...)"| s2
    s2 -. "HTTPException(409, detail=exc.detail(...))" .-> s3
    s2 -. "exc.detail(data not statically known)" .-> s4
    s2 -. "HTTPException(404, detail=str(...))" .-> s5
    s2 -. "str(exc)" .-> s6
    s2 -. "HTTPException(422, detail=[...])" .-> s7
    s2 -. "str(exc)" .-> s8
    s2 -. "HTTPException(404, detail='Task not found or inaccessible')" .-> s9
    s1 -->|"DeliveryDependencyService.projection(task_id)"| s10
    s10 -. "self.db.scalar(...)" .-> s11
    s10 -. "select(…).where (backend/app/services/deli…encyService.projection, 1)(...)" .-> s12
    b0["mutation result.append"]
    s10 -. "mutation result.append" .-> b0
    b1["mutation entry.update"]
    s10 -. "mutation entry.update" .-> b1
    b2["mutation entry.update"]
    s10 -. "mutation entry.update" .-> b2
    b3["mutation result.append"]
    s10 -. "mutation result.append" .-> b3
    click s1 "../modules/delivery_dependencies.md"
    click s2 "../modules/routers_task_domain.md"
    click s10 "../modules/delivery_dependency_service.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `list_delivery_dependencies` | `task_id: int`, `db: DeliveryDatabase` | - | - | `...` |
| `domain_result` | `awaitable` | `TaskVersionConflictError` | - | `result` |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `DeliveryDependencyService.projection` | `task_id` | `Task`, `self.db`, `Task`, `ProjectMilestone` | `entry[...]`, `entry[...]`, `entry[...]` | `result` |
| `self.db.scalar` | - | - | - | - |
| `select(…).where (backend/app/services/deli…encyService.projection, 1)` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| list_delivery_dependencies | domain_result | 19 | `domain_result(...)` |
| domain_result | HTTPException | 55 | `HTTPException(409, detail=exc.detail(...))` |
| domain_result | exc.detail | 55 | `exc.detail(data not statically known)` |
| domain_result | HTTPException | 57 | `HTTPException(404, detail=str(...))` |
| domain_result | str | 57 | `str(exc)` |
| domain_result | HTTPException | 59 | `HTTPException(422, detail=[...])` |
| domain_result | str | 59 | `str(exc)` |
| domain_result | HTTPException | 61 | `HTTPException(404, detail='Task not found or inaccessible')` |
| list_delivery_dependencies | DeliveryDependencyService.projection | 19 | `DeliveryDependencyService(db).projection(task_id)` |
| DeliveryDependencyService.projection | self.db.scalar | 55 | `self.db.scalar(...)` |
| DeliveryDependencyService.projection | select(…).where (backend/app/services/deli…encyService.projection, 1) | 55 | `select(Task).where(...)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `result.append` | `DeliveryDependencyService.projection` | 70 |
| mutation | `entry.update` | `DeliveryDependencyService.projection` | 77 |
| mutation | `entry.update` | `DeliveryDependencyService.projection` | 81 |
| mutation | `result.append` | `DeliveryDependencyService.projection` | 87 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `domain_result` | `HTTPException` | 55 |
| unresolved_call | `domain_result` | `exc.detail` | 55 |
| external_call | `domain_result` | `HTTPException` | 57 |
| external_call | `domain_result` | `HTTPException` | 59 |
| external_call | `domain_result` | `HTTPException` | 61 |
| unresolved_call | `DeliveryDependencyService.projection` | `self.db.scalar` | 55 |
| unresolved_call | `DeliveryDependencyService.projection` | `select(Task).where` | 55 |
| step_limit | `list_delivery_dependencies` | `first 12 steps` | 0 |

## Behavior

Shows current delivery readiness for an authorized task. A target must have current attributed acceptance; hidden or missing targets expose a generic unavailable blocker without target identity or status.
