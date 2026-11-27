# lookup_tasks

**Entry point:** `lookup_tasks` (`http`)
**Source:** [routers_task_domain](../modules/routers_task_domain.md)
**Modules touched:** [authority](../modules/authority.md), [config](../modules/config.md), [routers_task_domain](../modules/routers_task_domain.md), [sql_semantics](../modules/sql_semantics.md), and 3 more

**Complete modules touched:**

- [authority](../modules/authority.md)
- [config](../modules/config.md)
- [routers_task_domain](../modules/routers_task_domain.md)
- [sql_semantics](../modules/sql_semantics.md)
- [task_detail](../modules/task_detail.md)
- [task_detail_service](../modules/task_detail_service.md)
- [task_display_state](../modules/task_display_state.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as lookup_tasks
    participant p1 as TaskDetailService.lookup
    participant p2 as domain_result
    participant p3 as TaskDetailService
    participant p4 as TaskDetailService.references
    participant p5 as require_project
    participant p6 as task_state_clause
    participant p7 as portable_contains
    participant p8 as TaskDetailService.page
    participant p9 as state_clause
    participant p10 as get_settings
    participant p11 as displayed_state_expression
    participant p12 as validate_state_filter
    participant p13 as normalize_text
    participant p14 as AuthorityError
    participant p15 as _escaped_like
    participant p16 as TaskReferencePage
    participant p17 as Settings
    participant p18 as withdrawn_by_successor
    participant p19 as HTTPException
    participant p20 as exc.detail
    participant p21 as aliased
    participant p22 as statement.where
    participant p23 as str
    participant p24 as Task.is_summary.is_
    participant p25 as select(…).where(…).exists
    participant p26 as select(…).where (backend/app/services/task…:TaskDetailService.lookup)
    p0->>p1: TaskDetailService.lookup
    p0->>p2: domain_result
    p0->>p3: TaskDetailService
    p1->>p4: TaskDetailService.references
    p1->>p5: require_project
    p1->>p6: task_state_clause
    p1->>p7: portable_contains
    p1->>p8: TaskDetailService.page
    p6->>p9: state_clause
    p5->>p10: get_settings
    p4->>p11: displayed_state_expression
    p1->>p12: validate_state_filter
    p7->>p13: normalize_text
    p5->>p14: AuthorityError
    p7->>p15: _escaped_like
    p8->>p16: TaskReferencePage
    p10->>p17: Settings
    p11->>p18: withdrawn_by_successor
    p2-->>p19: HTTPException(409, detail=exc.detail(...))
    p2-->>p20: exc.detail
    p1-->>p21: aliased(Task)
    p2-->>p19: HTTPException(404, detail=str(...))
    p1-->>p22: statement.where(Task.is_summary.is_(...), ...)
    p2-->>p23: str(exc)
    p1-->>p24: Task.is_summary.is_(False)
    p2-->>p19: HTTPException(422, detail=[...])
    p1-->>p25: select(…).where(…).exists
    p2-->>p23: str(exc)
    p1-->>p26: select(…).where (backend/app/services/task…:TaskDetailService.lookup)(...)
    p2-->>p19: HTTPException(404, detail='Task not found or inaccessible')
```

> Call sequence diagram shows 30 of 105 interactions; 75 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 7 of 29 (22 omitted); unresolved 5 of 52 (47 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/task_detail_service.py:TaskDetailService.references` | 11 | - | unresolved | 10 |
| `backend/app/services/task_detail_service.py:TaskDetailService.references` | 11 | - | external | 2 |
| `backend/app/services/task_display_state.py:displayed_state_expression` | 16 | - | external | 1 |
| `backend/app/services/task_display_state.py:displayed_state_expression` | 16 | - | unresolved | 1 |
| `backend/app/services/task_display_state.py:withdrawn_by_successor` | 19 | - | external | 2 |
| `backend/app/services/task_display_state.py:withdrawn_by_successor` | 19 | - | unresolved | 2 |
| `backend/app/services/task_detail_service.py:TaskDetailService.lookup` | 10 | - | external | 9 |
| `backend/app/authority.py:require_project` | 38 | - | unresolved | 2 |
> Omission summary shows 8 of 24 groups; 16 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 25; effect analysis evaluated: 18, partial: 2, unavailable: 5. Counts include steps omitted from the displayed trace.

Collector observations for 20 source steps with known totals: observed: 91, emitted: 85, omitted: 6. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `lookup_tasks` | `available` | `partial` | `available` | `12` | `9` | `3` |
| `domain_result` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `exc.detail` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `TaskDetailService.lookup` | `available` | `partial` | `available` | `20` | `17` | `3` |
| `TaskDetailService.references` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `select(…).outerjoin(…).outerjoin` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. lookup_tasks"]
    s2["2. domain_result"]
    s3["3. HTTPException"]
    s4["4. exc.detail"]
    s5["5. HTTPException"]
    s6["6. str"]
    s7["7. HTTPException"]
    s8["8. str"]
    s9["9. HTTPException"]
    s10["10. TaskDetailService.lookup"]
    s11["11. TaskDetailService.references"]
    s12["12. select(…).outerjoin(…).outerjoin"]
    s1 -->|"domain_result(...)"| s2
    s2 -. "HTTPException(409, detail=exc.detail(...))" .-> s3
    s2 -. "exc.detail(data not statically known)" .-> s4
    s2 -. "HTTPException(404, detail=str(...))" .-> s5
    s2 -. "str(exc)" .-> s6
    s2 -. "HTTPException(422, detail=[...])" .-> s7
    s2 -. "str(exc)" .-> s8
    s2 -. "HTTPException(404, detail='Task not found or inaccessible')" .-> s9
    s1 -->|"TaskDetailService.lookup(…)"| s10
    s10 -->|"TaskDetailService.references(data not statically known)"| s11
    s11 -. "select(…).outerjoin(…).outerjoin(Iteration, ...)" .-> s12
    click s1 "../modules/routers_task_domain.md"
    click s2 "../modules/routers_task_domain.md"
    click s10 "../modules/task_detail_service.md"
    click s11 "../modules/task_detail_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `lookup_tasks` | `db: DB`, `project_id: int \| None`, `iteration_id: int \| None`, `q: str \| None`, `backlog_only: bool`, `limit: int`, `after_id: int`, `task_status: str \| None` | - | - | `...` |
| `domain_result` | `awaitable` | `TaskVersionConflictError` | - | `result` |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `TaskDetailService.lookup` | `project_id`, `iteration_id`, `query`, `backlog_only`, `limit`, `after_id`, `status`, `parent_id` | `Task`, `self.db`, `Task`, `Task`, `Task`, `self.db`, `Task`, `Task` | - | `...` |
| `TaskDetailService.references` | - | `Task` | - | `...` |
| `select(…).outerjoin(…).outerjoin` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| lookup_tasks | domain_result | 150 | `domain_result(...)` |
| domain_result | HTTPException | 56 | `HTTPException(409, detail=exc.detail(...))` |
| domain_result | exc.detail | 56 | `exc.detail(data not statically known)` |
| domain_result | HTTPException | 58 | `HTTPException(404, detail=str(...))` |
| domain_result | str | 58 | `str(exc)` |
| domain_result | HTTPException | 60 | `HTTPException(422, detail=[...])` |
| domain_result | str | 60 | `str(exc)` |
| domain_result | HTTPException | 62 | `HTTPException(404, detail='Task not found or inaccessible')` |
| lookup_tasks | TaskDetailService.lookup | 150 | `TaskDetailService(db).lookup(project_id=project_id, iteration_id=iteration_id, query=q, backlog_only=backlog_only, limit=limit, after_id=after_id, status=task_status, parent_id=parent_id, roots_only=roots_only, leaf_only=leaf_only)` |
| TaskDetailService.lookup | TaskDetailService.references | 76 | `self.references(data not statically known)` |
| TaskDetailService.references | select(…).outerjoin(…).outerjoin | 44 | `select(Task.id, Task.title, Task.version, Task.status, displayed_state_expression(id_column=Task.id, status_column=Task.status, canceled_at_column=Task.canceled_at).label('displayed_state'), Task.project_id, Task.iteration_id, Task.parent_id, Task.owner_profile_id, Project.name.label('project_name'), Iteration.name.label('iteration_name'), Task.blocked_reason, Task.canceled_at, and_(Task.status == 'closed', Task.accepted_at.is_not(None), Task.accepted_by_principal_id.is_not(None), Task.accepted_version.is_not(None), Task.accepted_version == Task.version, Task.canceled_at.is_(None)).label('acceptance_current')).outerjoin(Project, Project.id == Task.project_id).outerjoin(Iteration, ...)` |

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
| unresolved_call | `TaskDetailService.references` | `select(Task.id, Task.title, Task.version, Task.status, displayed_state_expression(id_column=Task.id, status_column=Task.status, canceled_at_column=Task.canceled_at).label('displayed_state'), Task.project_id, Task.iteration_id, Task.parent_id, Task.owner_profile_id, Project.name.label('project_name'), Iteration.name.label('iteration_name'), Task.blocked_reason, Task.canceled_at, and_(Task.status == 'closed', Task.accepted_at.is_not(None), Task.accepted_by_principal_id.is_not(None), Task.accepted_version.is_not(None), Task.accepted_version == Task.version, Task.canceled_at.is_(None)).label('acceptance_current')).outerjoin(Project, Project.id == Task.project_id).outerjoin` | 44 |
| step_limit | `lookup_tasks` | `first 12 steps` | 0 |

## Behavior

This flow starts at `lookup_tasks` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
