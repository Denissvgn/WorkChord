# check_task_routing

**Entry point:** `check_task_routing` (`http`)
**Source:** [routers_task_domain](../modules/routers_task_domain.md)
**Modules touched:** [authority](../modules/authority.md), [commands](../modules/commands.md), [manual_provenance_service](../modules/manual_provenance_service.md), [query_limits](../modules/query_limits.md), and 6 more

**Complete modules touched:**

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [manual_provenance_service](../modules/manual_provenance_service.md)
- [query_limits](../modules/query_limits.md)
- [review_provenance](../modules/review_provenance.md)
- [routers_task_domain](../modules/routers_task_domain.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_replacement_service](../modules/task_replacement_service.md)
- [task_routing](../modules/task_routing.md)
- [task_routing_service](../modules/task_routing_service.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as check_task_routing
    participant p1 as TaskBriefService.routing_check
    participant p2 as domain_result
    participant p3 as TaskBriefService
    participant p4 as check_routing
    participant p5 as project_policy
    participant p6 as assignee_models
    participant p7 as _contributor_publishers
    participant p8 as _issues
    participant p9 as suggest_routing
    participant p10 as different_publisher_required
    participant p11 as _rung_from
    participant p12 as review_history
    participant p13 as _attempt_history
    participant p14 as carried_contributors
    participant p15 as RoutingCheck
    participant p16 as RoutingIssue
    participant p17 as catalog_entries
    participant p18 as _Facts
    participant p19 as _verifier_profiles
    participant p20 as _refreshed
    participant p21 as AssigneeModels
    participant p22 as _available
    participant p23 as _choose_first_rung
    participant p24 as _rank
    participant p25 as RoutingReviewer
    participant p26 as RoutingRung
    participant p27 as current_command
    participant p28 as replacing
    participant p29 as HTTPException
    participant p30 as self.tasks.get_by_id
    p0->>p1: TaskBriefService.routing_check
    p0->>p2: domain_result
    p0->>p3: TaskBriefService
    p1->>p4: check_routing
    p4->>p5: project_policy
    p4->>p6: assignee_models
    p4->>p7: _contributor_publishers
    p4->>p8: _issues
    p4->>p9: suggest_routing
    p5->>p10: different_publisher_required
    p9->>p11: _rung_from
    p7->>p12: review_history
    p12->>p13: _attempt_history
    p12->>p14: carried_contributors
    p4->>p15: RoutingCheck
    p4->>p16: RoutingIssue
    p4->>p17: catalog_entries
    p4->>p18: _Facts
    p4->>p19: _verifier_profiles
    p4->>p20: _refreshed
    p6->>p21: AssigneeModels
    p8->>p22: _available
    p9->>p23: _choose_first_rung
    p9->>p24: _rank
    p11->>p25: RoutingReviewer
    p11->>p26: RoutingRung
    p10->>p27: current_command
    p14->>p28: replacing
    p2-->>p29: HTTPException(409, detail=exc.detail(...))
    p1-->>p30: self.tasks.get_by_id(task_id)
```

> Call sequence diagram shows 30 of 207 interactions; 177 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 44 (43 omitted); unresolved 1 of 103 (102 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/routers/task_domain.py:domain_result` | 2 | - | unresolved | 1 |
| `backend/app/routers/task_domain.py:domain_result` | 2 | - | external | 5 |
| `backend/app/services/task_brief_service.py:TaskBriefService.routing_check` | 10 | - | external | 1 |
| `backend/app/services/task_brief_service.py:TaskBriefService.routing_check` | 10 | - | unresolved | 2 |
| `backend/app/services/task_routing_service.py:check_routing` | 14 | - | external | 5 |
| `backend/app/services/task_routing_service.py:check_routing` | 14 | - | unresolved | 5 |
| `backend/app/services/review_provenance.py:different_publisher_required` | 19 | - | unresolved | 4 |
| `backend/app/services/review_provenance.py:different_publisher_required` | 19 | - | external | 2 |
> Omission summary shows 8 of 42 groups; 34 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 61; effect analysis evaluated: 42, partial: 4, unavailable: 15. Counts include steps omitted from the displayed trace.

Collector observations for 46 source steps with known totals: observed: 294, emitted: 285, omitted: 9. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `check_task_routing` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `domain_result` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `exc.detail` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `TaskBriefService.routing_check` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `self.tasks.get_by_id` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `LookupError` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. check_task_routing"]
    s2["2. domain_result"]
    s3["3. HTTPException"]
    s4["4. exc.detail"]
    s5["5. HTTPException"]
    s6["6. str"]
    s7["7. HTTPException"]
    s8["8. str"]
    s9["9. HTTPException"]
    s10["10. TaskBriefService.routing_check"]
    s11["11. self.tasks.get_by_id"]
    s12["12. LookupError"]
    s1 -->|"domain_result(...)"| s2
    s2 -. "HTTPException(409, detail=exc.detail(...))" .-> s3
    s2 -. "exc.detail(data not statically known)" .-> s4
    s2 -. "HTTPException(404, detail=str(...))" .-> s5
    s2 -. "str(exc)" .-> s6
    s2 -. "HTTPException(422, detail=[...])" .-> s7
    s2 -. "str(exc)" .-> s8
    s2 -. "HTTPException(404, detail='Task not found or inaccessible')" .-> s9
    s1 -->|"TaskBriefService.routing_check(task_id, assignee_id)"| s10
    s10 -. "self.tasks.get_by_id(task_id)" .-> s11
    s10 -. "LookupError('Task not found or inaccessible')" .-> s12
    click s1 "../modules/routers_task_domain.md"
    click s2 "../modules/routers_task_domain.md"
    click s10 "../modules/task_brief_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `check_task_routing` | `task_id: int`, `db: DB`, `assignee_id: int \| None` | - | - | `...` |
| `domain_result` | `awaitable` | `TaskVersionConflictError` | - | `result` |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `TaskBriefService.routing_check` | `task_id`, `assignee_id`, `use_current_assignee` | `self.db` | - | `...` |
| `self.tasks.get_by_id` | - | - | - | - |
| `LookupError` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| check_task_routing | domain_result | 267 | `domain_result(...)` |
| domain_result | HTTPException | 56 | `HTTPException(409, detail=exc.detail(...))` |
| domain_result | exc.detail | 56 | `exc.detail(data not statically known)` |
| domain_result | HTTPException | 58 | `HTTPException(404, detail=str(...))` |
| domain_result | str | 58 | `str(exc)` |
| domain_result | HTTPException | 60 | `HTTPException(422, detail=[...])` |
| domain_result | str | 60 | `str(exc)` |
| domain_result | HTTPException | 62 | `HTTPException(404, detail='Task not found or inaccessible')` |
| check_task_routing | TaskBriefService.routing_check | 267 | `TaskBriefService(db).routing_check(task_id, assignee_id)` |
| TaskBriefService.routing_check | self.tasks.get_by_id | 332 | `self.tasks.get_by_id(task_id)` |
| TaskBriefService.routing_check | LookupError | 334 | `LookupError('Task not found or inaccessible')` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `domain_result` | `HTTPException` | 56 |
| unresolved_call | `domain_result` | `exc.detail` | 56 |
| external_call | `domain_result` | `HTTPException` | 58 |
| external_call | `domain_result` | `HTTPException` | 60 |
| external_call | `domain_result` | `HTTPException` | 62 |
| unresolved_call | `TaskBriefService.routing_check` | `self.tasks.get_by_id` | 332 |
| external_call | `TaskBriefService.routing_check` | `LookupError` | 334 |
| step_limit | `check_task_routing` | `first 12 steps` | 0 |
| truncated_flow | `check_task_routing` | `depth limit` | 0 |

## Behavior

This flow starts at `check_task_routing` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
