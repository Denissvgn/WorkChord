# task_mention_options

**Entry point:** `task_mention_options` (`http`)
**Source:** [routers_discussion](../modules/routers_discussion.md)
**Modules touched:** [authority](../modules/authority.md), [config](../modules/config.md), [discussion_service](../modules/discussion_service.md), [routers_discussion](../modules/routers_discussion.md), and 2 more

**Complete modules touched:**

- [authority](../modules/authority.md)
- [config](../modules/config.md)
- [discussion_service](../modules/discussion_service.md)
- [routers_discussion](../modules/routers_discussion.md)
- [routers_task_domain](../modules/routers_task_domain.md)
- [sql_semantics](../modules/sql_semantics.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as task_mention_options
    participant p1 as DiscussionService.mention_options
    participant p2 as domain_result
    participant p3 as DiscussionService
    participant p4 as DiscussionService.task
    participant p5 as portable_contains
    participant p6 as require_project
    participant p7 as get_settings
    participant p8 as internal_authority
    participant p9 as normalize_text
    participant p10 as _escaped_like
    participant p11 as AuthorityError
    participant p12 as Settings
    participant p13 as HTTPException
    participant p14 as exc.detail
    participant p15 as len
    participant p16 as ValueError (backend/app/services/disc…ionService.mention_options)
    participant p17 as str
    participant p18 as select(…).where (backend/app/services/disc…Service.mention_options, 1)
    participant p19 as select (backend/app/services/disc…ionService.mention_options)
    participant p20 as select(…).where (backend/app/services/disc…Service.mention_options, 2)
    participant p21 as WorkspaceMembership.role.in_
    participant p22 as select(…).where (backend/app/services/disc…ionService.mention_options)
    participant p23 as Principal.enabled.is_
    participant p24 as or_
    p0->>p1: DiscussionService.mention_options
    p0->>p2: domain_result
    p0->>p3: DiscussionService
    p1->>p4: DiscussionService.task
    p1->>p5: portable_contains
    p4->>p6: require_project
    p6->>p7: get_settings
    p1->>p8: internal_authority
    p5->>p9: normalize_text
    p5->>p10: _escaped_like
    p4->>p11: AuthorityError
    p7->>p12: Settings
    p2-->>p13: HTTPException(409, detail=exc.detail(...))
    p2-->>p14: exc.detail
    p1-->>p15: len(query)
    p2-->>p13: HTTPException(404, detail=str(...))
    p1-->>p16: ValueError (backend/app/services/disc…ionService.mention_options)('Use a bounded mention query')
    p2-->>p17: str(exc)
    p2-->>p13: HTTPException(422, detail=[...])
    p1-->>p18: select(…).where (backend/app/services/disc…Service.mention_options, 1)(...)
    p2-->>p17: str(exc)
    p1-->>p19: select (backend/app/services/disc…ionService.mention_options)(ProjectMembership.principal_id)
    p2-->>p13: HTTPException(404, detail='Task not found or inaccessible')
    p1-->>p20: select(…).where (backend/app/services/disc…Service.mention_options, 2)(WorkspaceMembership.role.in_(...))
    p1-->>p19: select (backend/app/services/disc…ionService.mention_options)(WorkspaceMembership.principal_id)
    p1-->>p21: WorkspaceMembership.role.in_([...])
    p1-->>p22: select(…).where (backend/app/services/disc…ionService.mention_options)(..., Principal.enabled.is_(...), ..., or_(...))
    p1-->>p19: select (backend/app/services/disc…ionService.mention_options)(Principal.id, Principal.display_name)
    p1-->>p23: Principal.enabled.is_(True)
    p1-->>p24: or_(Principal.id.in_(...), Principal.id.in_(...))
```

> Call sequence diagram shows 30 of 70 interactions; 40 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 12 of 20 (8 omitted); unresolved 6 of 33 (27 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/discussion_service.py:DiscussionService.task` | 11 | - | unresolved | 9 |
| `backend/app/services/discussion_service.py:DiscussionService.task` | 11 | - | external | 4 |
| `backend/app/authority.py:require_project` | 17 | - | unresolved | 2 |
| `backend/app/authority.py:require_project` | 17 | [backend/app/authority.py](../modules/authority.md) | internal | 2 |
| `backend/app/services/discussion_service.py:DiscussionService.task` | 11 | [backend/app/authority.py](../modules/authority.md) | internal | 1 |
| `backend/app/authority.py:internal_authority` | 28 | - | unresolved | 1 |
| `backend/app/services/discussion_service.py:DiscussionService.task` | 11 | [backend/app/services/discussion_service.py](../modules/discussion_service.md) | internal | 1 |
| `backend/app/services/discussion_service.py:DiscussionService.mention_options` | 10 | - | unresolved | 7 |
> Omission summary shows 8 of 15 groups; 7 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 18; effect analysis evaluated: 13, partial: 0, unavailable: 5. Counts include steps omitted from the displayed trace.

Collector observations for 13 source steps with known totals: observed: 54, emitted: 54, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `task_mention_options` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `domain_result` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `exc.detail` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `DiscussionService.mention_options` | `available` | `evaluated` | `available` | `10` | `10` | `0` |
| `DiscussionService.task` | `available` | `evaluated` | `available` | `7` | `7` | `0` |
| `self.db.scalar` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. task_mention_options"]
    s2["2. domain_result"]
    s3["3. HTTPException"]
    s4["4. exc.detail"]
    s5["5. HTTPException"]
    s6["6. str"]
    s7["7. HTTPException"]
    s8["8. str"]
    s9["9. HTTPException"]
    s10["10. DiscussionService.mention_options"]
    s11["11. DiscussionService.task"]
    s12["12. self.db.scalar"]
    s1 -->|"domain_result(...)"| s2
    s2 -. "HTTPException(409, detail=exc.detail(...))" .-> s3
    s2 -. "exc.detail(data not statically known)" .-> s4
    s2 -. "HTTPException(404, detail=str(...))" .-> s5
    s2 -. "str(exc)" .-> s6
    s2 -. "HTTPException(422, detail=[...])" .-> s7
    s2 -. "str(exc)" .-> s8
    s2 -. "HTTPException(404, detail='Task not found or inaccessible')" .-> s9
    s1 -->|"DiscussionService.mention_options(task_id, query=q, limit=limit, after_id=after_id)"| s10
    s10 -->|"DiscussionService.task(task_id)"| s11
    s11 -. "self.db.scalar(...)" .-> s12
    click s1 "../modules/routers_discussion.md"
    click s2 "../modules/routers_task_domain.md"
    click s10 "../modules/discussion_service.md"
    click s11 "../modules/discussion_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `task_mention_options` | `task_id: int`, `db: DiscussionDatabase`, `q: str`, `after_id: int`, `limit: int` | - | - | `...` |
| `domain_result` | `awaitable` | `TaskVersionConflictError` | - | `result` |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `DiscussionService.mention_options` | `task_id`, `query`, `limit`, `after_id` | `self.db`, `ProjectMembership`, `Principal`, `Principal`, `Principal` | - | `{...}` |
| `DiscussionService.task` | `task_id`, `writing`, `lock` | `self.db`, `self.db` | - | `...`, `task` |
| `self.db.scalar` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| task_mention_options | domain_result | 44 | `domain_result(...)` |
| domain_result | HTTPException | 51 | `HTTPException(409, detail=exc.detail(...))` |
| domain_result | exc.detail | 51 | `exc.detail(data not statically known)` |
| domain_result | HTTPException | 53 | `HTTPException(404, detail=str(...))` |
| domain_result | str | 53 | `str(exc)` |
| domain_result | HTTPException | 55 | `HTTPException(422, detail=[...])` |
| domain_result | str | 55 | `str(exc)` |
| domain_result | HTTPException | 57 | `HTTPException(404, detail='Task not found or inaccessible')` |
| task_mention_options | DiscussionService.mention_options | 44 | `DiscussionService(db).mention_options(task_id, query=q, limit=limit, after_id=after_id)` |
| DiscussionService.mention_options | DiscussionService.task | 47 | `self.task(task_id)` |
| DiscussionService.task | self.db.scalar | 30 | `self.db.scalar(...)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `domain_result` | `HTTPException` | 51 |
| unresolved_call | `domain_result` | `exc.detail` | 51 |
| external_call | `domain_result` | `HTTPException` | 53 |
| external_call | `domain_result` | `HTTPException` | 55 |
| external_call | `domain_result` | `HTTPException` | 57 |
| unresolved_call | `DiscussionService.task` | `self.db.scalar` | 30 |
| step_limit | `task_mention_options` | `first 12 steps` | 0 |

## Behavior

This flow starts at `task_mention_options` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
