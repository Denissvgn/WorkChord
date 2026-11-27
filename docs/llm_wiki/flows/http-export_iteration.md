# export_iteration

**Entry point:** `export_iteration` (`http`)
**Source:** [export](../modules/export.md)
**Modules touched:** [authority](../modules/authority.md), [commands](../modules/commands.md), [export](../modules/export.md), [iteration_service](../modules/iteration_service.md), and 8 more

**Complete modules touched:**

- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [export](../modules/export.md)
- [iteration_service](../modules/iteration_service.md)
- [query_limits](../modules/query_limits.md)
- [schemas_team](../modules/schemas_team.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [task_display_state](../modules/task_display_state.md)
- [task_hierarchy_service](../modules/task_hierarchy_service.md)
- [task_service](../modules/task_service.md)
- [team_service](../modules/team_service.md)
- [time](../modules/time.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as export_iteration
    participant p1 as TaskService.get_by_iteration
    participant p2 as TeamService.get_by_iteration
    participant p3 as aggregate_metrics
    participant p4 as _task_to_export
    participant p5 as IterationService
    participant p6 as IterationService.get_by_id
    participant p7 as TaskService
    participant p8 as TeamService
    participant p9 as TaskService._task_graph_query
    participant p10 as TaskService._load_iteration_tree
    participant p11 as TeamService._attach_assignee_profiles
    participant p12 as working_today
    participant p13 as state_clause
    participant p14 as displayed_state_expression
    participant p15 as TaskHierarchyService._load_iteration_tree
    participant p16 as utc_now
    participant p17 as _scope_conditions
    participant p18 as TeamService._member_options
    participant p19 as CollectionLimitExceededError
    participant p20 as HierarchyScopeError
    participant p21 as TaskHierarchyService._task_graph_query
    participant p22 as internal_authority
    participant p23 as validate_state_filter
    participant p24 as TaskHierarchyService
    participant p25 as as_utc
    participant p26 as withdrawn_by_successor
    participant p27 as TeamMemberProfileCompact
    participant p28 as HTTPException
    participant p29 as iteration.start_date.isoformat
    participant p30 as iteration.end_date.isoformat
    p0->>p1: TaskService.get_by_iteration
    p0->>p2: TeamService.get_by_iteration
    p0->>p3: aggregate_metrics
    p0->>p4: _task_to_export
    p0->>p5: IterationService
    p0->>p6: IterationService.get_by_id
    p0->>p7: TaskService
    p0->>p8: TeamService
    p1->>p9: TaskService._task_graph_query
    p1->>p10: TaskService._load_iteration_tree
    p2->>p11: TeamService._attach_assignee_profiles
    p3->>p12: working_today
    p3->>p13: state_clause
    p3->>p14: displayed_state_expression
    p10->>p15: TaskHierarchyService._load_iteration_tree
    p3->>p16: utc_now
    p3->>p17: _scope_conditions
    p2->>p18: TeamService._member_options
    p1->>p19: CollectionLimitExceededError
    p3->>p20: HierarchyScopeError
    p9->>p21: TaskHierarchyService._task_graph_query
    p11->>p22: internal_authority
    p13->>p23: validate_state_filter
    p9->>p24: TaskHierarchyService
    p12->>p25: as_utc
    p14->>p26: withdrawn_by_successor
    p11->>p27: TeamMemberProfileCompact
    p0-->>p28: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)
    p0-->>p29: iteration.start_date.isoformat
    p0-->>p30: iteration.end_date.isoformat
```

> Call sequence diagram shows 30 of 432 interactions; 402 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 157 (156 omitted); unresolved 2 of 235 (233 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/iteration_service.py:IterationService.get_by_id` | 3 | - | unresolved | 4 |
| `backend/app/services/iteration_service.py:IterationService.get_by_id` | 3 | - | external | 3 |
| `backend/app/services/task_service.py:TaskService.get_by_iteration` | 13 | - | unresolved | 6 |
| `backend/app/services/task_hierarchy_service.py:TaskHierarchyService._task_graph_query` | 18 | - | unresolved | 6 |
| `backend/app/services/task_hierarchy_service.py:TaskHierarchyService._task_graph_query` | 18 | - | external | 8 |
| `backend/app/services/task_service.py:TaskService.get_by_iteration` | 13 | - | external | 2 |
| `backend/app/services/task_hierarchy_service.py:TaskHierarchyService._load_iteration_tree` | 41 | - | unresolved | 20 |
| `backend/app/services/task_hierarchy_service.py:TaskHierarchyService._load_iteration_tree` | 41 | - | external | 11 |
> Omission summary shows 8 of 43 groups; 35 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 41; effect analysis evaluated: 29, partial: 1, unavailable: 11. Counts include steps omitted from the displayed trace.

Collector observations for 30 source steps with known totals: observed: 138, emitted: 135, omitted: 3. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `export_iteration` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `IterationService` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `IterationService.get_by_id` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `self.db.execute (backend/app/services/iter…terationService.get_by_id)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).options(…).where (backend/app/services/iter…terationService.get_by_id)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).options (backend/app/services/iter…terationService.get_by_id)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select (backend/app/services/iter…terationService.get_by_id)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `selectinload (backend/app/services/iter…terationService.get_by_id)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `selectinload (backend/app/services/iter…terationService.get_by_id)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `result.scalar_one_or_none` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `TaskService` | `unavailable` | `unavailable` | `unavailable` | — | — | — |

```mermaid
flowchart LR
    s1["1. export_iteration"]
    s2["2. IterationService"]
    s3["3. IterationService.get_by_id"]
    s4["4. self.db.execute (backend/app/services/iter…terationService.get_by_id)"]
    s5["5. select(…).options(…).where (backend/app/services/iter…terationService.get_by_id)"]
    s6["6. select(…).options (backend/app/services/iter…terationService.get_by_id)"]
    s7["7. select (backend/app/services/iter…terationService.get_by_id)"]
    s8["8. selectinload (backend/app/services/iter…terationService.get_by_id)"]
    s9["9. selectinload (backend/app/services/iter…terationService.get_by_id)"]
    s10["10. result.scalar_one_or_none"]
    s11["11. HTTPException"]
    s12["12. TaskService"]
    s1 -->|"IterationService(db)"| s2
    s1 -->|"IterationService.get_by_id(iteration_id)"| s3
    s3 -. "self.db.execute (backend/app/services/iter…terationService.get_by_id)(...)" .-> s4
    s3 -. "select(…).options(…).where (backend/app/services/iter…terationService.get_by_id)(...)" .-> s5
    s3 -. "select(…).options (backend/app/services/iter…terationService.get_by_id)(selectinload(...), selectinload(...))" .-> s6
    s3 -. "select (backend/app/services/iter…terationService.get_by_id)(Iteration)" .-> s7
    s3 -. "selectinload (backend/app/services/iter…terationService.get_by_id)(Iteration.calendar)" .-> s8
    s3 -. "selectinload (backend/app/services/iter…terationService.get_by_id)(Iteration.project)" .-> s9
    s3 -. "result.scalar_one_or_none(data not statically known)" .-> s10
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s11
    s1 -->|"TaskService(db)"| s12
    click s1 "../modules/export.md"
    click s2 "../modules/iteration_service.md"
    click s3 "../modules/iteration_service.md"
    click s12 "../modules/task_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `export_iteration` | `iteration_id: int`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | `status`, `MAX_SYNC_EXPORT_TASKS` | - | `JSONResponse(...)` |
| `IterationService` | - | - | - | - |
| `IterationService.get_by_id` | `iteration_id: int` | `Iteration` | - | `result.scalar_one_or_none(...)` |
| `self.db.execute (backend/app/services/iter…terationService.get_by_id)` | - | - | - | - |
| `select(…).options(…).where (backend/app/services/iter…terationService.get_by_id)` | - | - | - | - |
| `select(…).options (backend/app/services/iter…terationService.get_by_id)` | - | - | - | - |
| `select (backend/app/services/iter…terationService.get_by_id)` | - | - | - | - |
| `selectinload (backend/app/services/iter…terationService.get_by_id)` | - | - | - | - |
| `selectinload (backend/app/services/iter…terationService.get_by_id)` | - | - | - | - |
| `result.scalar_one_or_none` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `TaskService` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| export_iteration | IterationService | 82 | `IterationService(db)` |
| export_iteration | IterationService.get_by_id | 83 | `iteration_service.get_by_id(iteration_id)` |
| IterationService.get_by_id | self.db.execute (backend/app/services/iter…terationService.get_by_id) | 338 | `self.db.execute(...)` |
| IterationService.get_by_id | select(…).options(…).where (backend/app/services/iter…terationService.get_by_id) | 339 | `select(Iteration).options(selectinload(Iteration.calendar), selectinload(Iteration.project)).where(...)` |
| IterationService.get_by_id | select(…).options (backend/app/services/iter…terationService.get_by_id) | 339 | `select(Iteration).options(selectinload(...), selectinload(...))` |
| IterationService.get_by_id | select (backend/app/services/iter…terationService.get_by_id) | 339 | `select(Iteration)` |
| IterationService.get_by_id | selectinload (backend/app/services/iter…terationService.get_by_id) | 341 | `selectinload(Iteration.calendar)` |
| IterationService.get_by_id | selectinload (backend/app/services/iter…terationService.get_by_id) | 342 | `selectinload(Iteration.project)` |
| IterationService.get_by_id | result.scalar_one_or_none | 346 | `result.scalar_one_or_none(data not statically known)` |
| export_iteration | HTTPException | 86 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| export_iteration | TaskService | 91 | `TaskService(db)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `IterationService.get_by_id` | `self.db.execute` | 338 |
| unresolved_call | `IterationService.get_by_id` | `select(Iteration).options(selectinload(Iteration.calendar), selectinload(Iteration.project)).where` | 339 |
| unresolved_call | `IterationService.get_by_id` | `select(Iteration).options` | 339 |
| external_call | `IterationService.get_by_id` | `select` | 339 |
| external_call | `IterationService.get_by_id` | `selectinload` | 341 |
| external_call | `IterationService.get_by_id` | `selectinload` | 342 |
| unresolved_call | `IterationService.get_by_id` | `result.scalar_one_or_none` | 346 |
| external_call | `export_iteration` | `HTTPException` | 86 |
| step_limit | `export_iteration` | `first 12 steps` | 0 |

## Behavior

This flow starts at `export_iteration` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
