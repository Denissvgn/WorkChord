# export_iteration

**Entry point:** `export_iteration` (`http`)
**Source:** [export](../modules/export.md)
**Modules touched:** [authority](../modules/authority.md), [commands](../modules/commands.md), [export](../modules/export.md), [iteration_service](../modules/iteration_service.md), and 4 more

**Complete modules touched:**

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [export](../modules/export.md)
- [iteration_service](../modules/iteration_service.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [task_service](../modules/task_service.md)
- [team_service](../modules/team_service.md)
- [time](../modules/time.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as export_iteration
    participant p1 as IterationService
    participant p2 as iteration_service.get_by_id
    participant p3 as HTTPException
    participant p4 as TaskService
    participant p5 as task_service.get_by_iteration
    participant p6 as TeamService
    participant p7 as team_service.get_by_iteration
    participant p8 as aggregate_metrics
    participant p9 as db.info.get
    participant p10 as _scope_conditions(…).get
    participant p11 as _scope_conditions
    participant p12 as tuple
    participant p13 as authority.allows
    participant p14 as iterations.c.project_id.in_
    participant p15 as or_ (backend/app/authority.py:_scope_conditions)
    participant p16 as iterations.c.project_id.is_
    participant p17 as select(…).where (backend/app/authority.py:_scope_conditions, 1)
    participant p18 as select (backend/app/authority.py:_scope_conditions)
    participant p19 as and_ (backend/app/authority.py:_scope_conditions)
    participant p20 as task.c.iteration_id.in_
    participant p21 as task.c.iteration_id.is_
    participant p22 as task.c.project_id.in_
    participant p23 as task.c.project_id.is_
    participant p24 as select(…).where (backend/app/authority.py:_scope_conditions, 3)
    p0->>p1: IterationService
    p0-->>p2: iteration_service.get_by_id
    p0-->>p3: HTTPException
    p0->>p4: TaskService
    p0-->>p5: task_service.get_by_iteration
    p0->>p6: TeamService
    p0-->>p7: team_service.get_by_iteration
    p0->>p8: aggregate_metrics
    p8-->>p9: db.info.get
    p8-->>p10: _scope_conditions(…).get
    p8->>p11: _scope_conditions
    p11-->>p12: tuple
    p11-->>p13: authority.allows
    p11-->>p14: iterations.c.project_id.in_
    p11-->>p15: or_ (backend/app/authority.py:_scope_conditions)
    p11-->>p16: iterations.c.project_id.is_
    p11-->>p17: select(…).where (backend/app/authority.py:_scope_conditions, 1)
    p11-->>p18: select (backend/app/authority.py:_scope_conditions)
    p11-->>p19: and_ (backend/app/authority.py:_scope_conditions)
    p11-->>p15: or_ (backend/app/authority.py:_scope_conditions)
    p11-->>p20: task.c.iteration_id.in_
    p11-->>p19: and_ (backend/app/authority.py:_scope_conditions)
    p11-->>p21: task.c.iteration_id.is_
    p11-->>p22: task.c.project_id.in_
    p11-->>p15: or_ (backend/app/authority.py:_scope_conditions)
    p11-->>p22: task.c.project_id.in_
    p11-->>p23: task.c.project_id.is_
    p11-->>p24: select(…).where (backend/app/authority.py:_scope_conditions, 3)
    p11-->>p18: select (backend/app/authority.py:_scope_conditions)
    p11-->>p19: and_ (backend/app/authority.py:_scope_conditions)
```

> Call sequence diagram shows 30 of 286 interactions; 256 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. export_iteration"]
    s2["2. IterationService"]
    s3["3. iteration_service.get_by_id"]
    s4["4. HTTPException"]
    s5["5. TaskService"]
    s6["6. task_service.get_by_iteration"]
    s7["7. TeamService"]
    s8["8. team_service.get_by_iteration"]
    s9["9. aggregate_metrics"]
    s10["10. db.info.get"]
    s11["11. _scope_conditions(…).get"]
    s12["12. _scope_conditions"]
    s1 -->|"IterationService(db)"| s2
    s1 -. "iteration_service.get_by_id(iteration_id)" .-> s3
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s4
    s1 -->|"TaskService(db)"| s5
    s1 -. "task_service.get_by_iteration(iteration_id, max_tasks=MAX_SYNC_EXPORT_TASKS)" .-> s6
    s1 -->|"TeamService(db)"| s7
    s1 -. "team_service.get_by_iteration(iteration_id)" .-> s8
    s1 -->|"aggregate_metrics(db, iteration_id=iteration_id)"| s9
    s9 -. "db.info.get('authority')" .-> s10
    s9 -. "_scope_conditions(…).get(Task)" .-> s11
    s9 -->|"_scope_conditions(authority)"| s12
    b0["mutation columns.insert"]
    s9 -. "mutation columns.insert" .-> b0
    b1["mutation values.pop"]
    s9 -. "mutation values.pop" .-> b1
    b2["mutation values.pop"]
    s9 -. "mutation values.pop" .-> b2
    b3["mutation values.pop"]
    s9 -. "mutation values.pop" .-> b3
    b4["mutation results.append"]
    s9 -. "mutation results.append" .-> b4
    click s1 "../modules/export.md"
    click s2 "../modules/iteration_service.md"
    click s5 "../modules/task_service.md"
    click s7 "../modules/team_service.md"
    click s9 "../modules/services_work_metrics.md"
    click s12 "../modules/authority.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
    class b4 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `export_iteration` | `iteration_id: int`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | `status`, `MAX_SYNC_EXPORT_TASKS` | - | `JSONResponse(...)` |
| `IterationService` | - | - | - | - |
| `iteration_service.get_by_id` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `TaskService` | - | - | - | - |
| `task_service.get_by_iteration` | - | - | - | - |
| `TeamService` | - | - | - | - |
| `team_service.get_by_iteration` | - | - | - | - |
| `aggregate_metrics` | `db`, `project_id`, `iteration_id`, `project_ids`, `group_by`, `task_ids`, `zone_map` | - | `values[...]`, `values[...]`, `values[...]`, `values[...]`, `values[...]` | `...` |
| `db.info.get` | - | - | - | - |
| `_scope_conditions(…).get` | - | - | - | - |
| `_scope_conditions` | `authority` | - | `conditions[...]` | `conditions` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| export_iteration | IterationService | 82 | `IterationService(db)` |
| export_iteration | iteration_service.get_by_id | 83 | `iteration_service.get_by_id(iteration_id)` |
| export_iteration | HTTPException | 86 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| export_iteration | TaskService | 91 | `TaskService(db)` |
| export_iteration | task_service.get_by_iteration | 92 | `task_service.get_by_iteration(iteration_id, max_tasks=MAX_SYNC_EXPORT_TASKS)` |
| export_iteration | TeamService | 97 | `TeamService(db)` |
| export_iteration | team_service.get_by_iteration | 98 | `team_service.get_by_iteration(iteration_id)` |
| export_iteration | aggregate_metrics | 130 | `aggregate_metrics(db, iteration_id=iteration_id)` |
| aggregate_metrics | db.info.get | 135 | `db.info.get('authority')` |
| aggregate_metrics | _scope_conditions(…).get | 136 | `_scope_conditions(authority).get(Task)` |
| aggregate_metrics | _scope_conditions | 136 | `_scope_conditions(authority)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `columns.insert` | `aggregate_metrics` | 210 |
| mutation | `values.pop` | `aggregate_metrics` | 224 |
| mutation | `values.pop` | `aggregate_metrics` | 227 |
| mutation | `values.pop` | `aggregate_metrics` | 229 |
| mutation | `results.append` | `aggregate_metrics` | 234 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `export_iteration` | `iteration_service.get_by_id` | 83 |
| external_call | `export_iteration` | `HTTPException` | 86 |
| unresolved_call | `export_iteration` | `task_service.get_by_iteration` | 92 |
| unresolved_call | `export_iteration` | `team_service.get_by_iteration` | 98 |
| unresolved_call | `aggregate_metrics` | `db.info.get` | 135 |
| unresolved_call | `aggregate_metrics` | `_scope_conditions(authority).get` | 136 |
| step_limit | `export_iteration` | `first 12 steps` | 0 |

## Behavior

This flow starts at `export_iteration` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
