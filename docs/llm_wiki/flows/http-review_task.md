# review_task

**Entry point:** `review_task` (`http`)
**Source:** [routers_task_domain](../modules/routers_task_domain.md)
**Modules touched:** [agent_readiness](../modules/agent_readiness.md), [commands](../modules/commands.md), [external_link_service](../modules/external_link_service.md), [routers_task_domain](../modules/routers_task_domain.md), and 6 more

**Complete modules touched:**

- [agent_readiness](../modules/agent_readiness.md)
- [commands](../modules/commands.md)
- [external_link_service](../modules/external_link_service.md)
- [routers_task_domain](../modules/routers_task_domain.md)
- [schemas_external_link](../modules/schemas_external_link.md)
- [schemas_task](../modules/schemas_task.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as review_task
    participant p1 as TaskService.task_to_response
    participant p2 as domain_result
    participant p3 as TaskBriefService
    participant p4 as TaskService
    participant p5 as task_signals
    participant p6 as evaluate_agent_readiness
    participant p7 as ExternalLinkService.task_links_to_response
    participant p8 as working_today
    participant p9 as ExternalLinkService.link_to_response
    participant p10 as ExternalLinkService.legacy_task_link_response
    participant p11 as _add_criterion
    participant p12 as current_command
    participant p13 as TaskAssignee
    participant p14 as TaskProject
    participant p15 as TaskMilestone
    participant p16 as TaskClaimedBy
    participant p17 as TaskResponse
    participant p18 as ExternalLinkService
    participant p19 as utc_now
    participant p20 as effective_work_flags
    participant p21 as _dependency_task
    participant p22 as as_utc
    participant p23 as brief_definition_blockers
    participant p24 as _description_is_actionable
    participant p25 as TaskAgentReadiness
    participant p26 as ExternalLinkResponse
    participant p27 as TaskAgentReadinessCriterion
    participant p28 as HTTPException
    participant p29 as TaskBriefService(…).review
    participant p30 as exc.detail
    p0->>p1: TaskService.task_to_response
    p0->>p2: domain_result
    p0->>p3: TaskBriefService
    p0->>p4: TaskService
    p1->>p5: task_signals
    p1->>p6: evaluate_agent_readiness
    p1->>p7: ExternalLinkService.task_links_to_response
    p5->>p8: working_today
    p7->>p9: ExternalLinkService.link_to_response
    p7->>p10: ExternalLinkService.legacy_task_link_response
    p6->>p11: _add_criterion
    p1->>p12: current_command
    p1->>p13: TaskAssignee
    p1->>p14: TaskProject
    p1->>p15: TaskMilestone
    p1->>p16: TaskClaimedBy
    p1->>p17: TaskResponse
    p1->>p18: ExternalLinkService
    p6->>p19: utc_now
    p5->>p20: effective_work_flags
    p6->>p21: _dependency_task
    p6->>p22: as_utc
    p6->>p23: brief_definition_blockers
    p6->>p24: _description_is_actionable
    p6->>p25: TaskAgentReadiness
    p9->>p26: ExternalLinkResponse
    p11->>p27: TaskAgentReadinessCriterion
    p2-->>p28: HTTPException(409, detail=exc.detail(...))
    p0-->>p29: TaskBriefService(…).review(task_id, data)
    p2-->>p30: exc.detail
```

> Call sequence diagram shows 30 of 128 interactions; 98 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 43 (42 omitted); unresolved 2 of 44 (42 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/routers/task_domain.py:domain_result` | 2 | - | external | 5 |
| `backend/app/commands.py:current_command` | 13 | - | external | 2 |
| `backend/app/commands.py:current_command` | 13 | - | unresolved | 1 |
| `backend/app/services/task_service.py:TaskService.task_to_response` | 12 | - | unresolved | 6 |
| `backend/app/services/task_service.py:TaskService.task_to_response` | 12 | - | external | 5 |
| `backend/app/services/work_metrics.py:working_today` | 22 | - | unresolved | 2 |
| `backend/app/services/work_metrics.py:working_today` | 22 | [backend/app/utils/time.py](../modules/time.md) | internal | 2 |
| `backend/app/utils/time.py:as_utc` | 25 | - | unresolved | 2 |
> Omission summary shows 8 of 29 groups; 21 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 42; effect analysis evaluated: 29, partial: 0, unavailable: 13. Counts include steps omitted from the displayed trace.

Collector observations for 29 source steps with known totals: observed: 158, emitted: 158, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `review_task` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `domain_result` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `exc.detail` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str (backend/app/routers/task_domain.py:domain_result)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str (backend/app/routers/task_domain.py:domain_result)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `TaskBriefService(…).review` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `TaskBriefService` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `TaskService.task_to_response` | `available` | `evaluated` | `available` | `7` | `7` | `0` |

```mermaid
flowchart LR
    s1["1. review_task"]
    s2["2. domain_result"]
    s3["3. HTTPException"]
    s4["4. exc.detail"]
    s5["5. HTTPException"]
    s6["6. str (backend/app/routers/task_domain.py:domain_result)"]
    s7["7. HTTPException"]
    s8["8. str (backend/app/routers/task_domain.py:domain_result)"]
    s9["9. HTTPException"]
    s10["10. TaskBriefService(…).review"]
    s11["11. TaskBriefService"]
    s12["12. TaskService.task_to_response"]
    s1 -->|"domain_result(...)"| s2
    s2 -. "HTTPException(409, detail=exc.detail(...))" .-> s3
    s2 -. "exc.detail(data not statically known)" .-> s4
    s2 -. "HTTPException(404, detail=str(...))" .-> s5
    s2 -. "str (backend/app/routers/task_domain.py:domain_result)(exc)" .-> s6
    s2 -. "HTTPException(422, detail=[...])" .-> s7
    s2 -. "str (backend/app/routers/task_domain.py:domain_result)(exc)" .-> s8
    s2 -. "HTTPException(404, detail='Task not found or inaccessible')" .-> s9
    s1 -. "TaskBriefService(…).review(task_id, data)" .-> s10
    s1 -->|"TaskBriefService(db)"| s11
    s1 -->|"TaskService.task_to_response(task)"| s12
    b0["mutation signals.pop"]
    s12 -. "mutation signals.pop" .-> b0
    click s1 "../modules/routers_task_domain.md"
    click s2 "../modules/routers_task_domain.md"
    click s11 "../modules/task_brief_service.md"
    click s12 "../modules/task_service.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `review_task` | `task_id: int`, `data: TaskReviewWrite`, `db: DB` | - | - | `...` |
| `domain_result` | `awaitable` | `TaskVersionConflictError` | - | `result` |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str (backend/app/routers/task_domain.py:domain_result)` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str (backend/app/routers/task_domain.py:domain_result)` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `TaskBriefService(…).review` | - | - | - | - |
| `TaskBriefService` | - | - | - | - |
| `TaskService.task_to_response` | `task: Task`, `iteration_end_date: Optional[date]`, `effective_flags` | `self.db`, `self.agent_capability_slugs` | - | `TaskResponse(...)` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| review_task | domain_result | 241 | `domain_result(...)` |
| domain_result | HTTPException | 51 | `HTTPException(409, detail=exc.detail(...))` |
| domain_result | exc.detail | 51 | `exc.detail(data not statically known)` |
| domain_result | HTTPException | 53 | `HTTPException(404, detail=str(...))` |
| domain_result | str (backend/app/routers/task_domain.py:domain_result) | 53 | `str(exc)` |
| domain_result | HTTPException | 55 | `HTTPException(422, detail=[...])` |
| domain_result | str (backend/app/routers/task_domain.py:domain_result) | 55 | `str(exc)` |
| domain_result | HTTPException | 57 | `HTTPException(404, detail='Task not found or inaccessible')` |
| review_task | TaskBriefService(…).review | 241 | `TaskBriefService(db).review(task_id, data)` |
| review_task | TaskBriefService | 241 | `TaskBriefService(db)` |
| review_task | TaskService.task_to_response | 242 | `TaskService(db).task_to_response(task)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `signals.pop` | `TaskService.task_to_response` | 1669 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `domain_result` | `HTTPException` | 51 |
| unresolved_call | `domain_result` | `exc.detail` | 51 |
| external_call | `domain_result` | `HTTPException` | 53 |
| external_call | `domain_result` | `HTTPException` | 55 |
| external_call | `domain_result` | `HTTPException` | 57 |
| unresolved_call | `review_task` | `TaskBriefService(db).review` | 241 |
| step_limit | `review_task` | `first 12 steps` | 0 |

## Behavior

This flow starts at `review_task` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
