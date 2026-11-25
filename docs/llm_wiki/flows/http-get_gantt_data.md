# get_gantt_data

**Entry point:** `get_gantt_data` (`http`)
**Source:** [routers_gantt](../modules/routers_gantt.md)
**Modules touched:** [authority](../modules/authority.md), [calendar_rules](../modules/calendar_rules.md), [calendar_service](../modules/calendar_service.md), [commands](../modules/commands.md), and 13 more

**Complete modules touched:**

- [authority](../modules/authority.md)
- [calendar_rules](../modules/calendar_rules.md)
- [calendar_service](../modules/calendar_service.md)
- [commands](../modules/commands.md)
- [dependency_order](../modules/dependency_order.md)
- [iteration_service](../modules/iteration_service.md)
- [query_limits](../modules/query_limits.md)
- [routers_gantt](../modules/routers_gantt.md)
- [schemas_calendar](../modules/schemas_calendar.md)
- [schemas_gantt](../modules/schemas_gantt.md)
- [schemas_iteration](../modules/schemas_iteration.md)
- [schemas_team](../modules/schemas_team.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [task_hierarchy_service](../modules/task_hierarchy_service.md)
- [task_service](../modules/task_service.md)
- [team_service](../modules/team_service.md)
- [time](../modules/time.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_gantt_data
    participant p1 as TaskService.get_by_iteration
    participant p2 as TeamService.get_by_iteration
    participant p3 as CalendarService.calculate_working_days
    participant p4 as AnnualCalendars.for_iteration
    participant p5 as _task_to_gantt
    participant p6 as inverted_saved_dependencies
    participant p7 as IterationService
    participant p8 as TaskService
    participant p9 as TeamService
    participant p10 as IterationService.get_by_id
    participant p11 as CalendarService
    participant p12 as _overdue_task_ids
    participant p13 as GanttResponse
    participant p14 as IterationResponse
    participant p15 as included_work_ids
    participant p16 as TaskService._task_graph_query
    participant p17 as task_signals
    participant p18 as TaskService._load_iteration_tree
    participant p19 as TeamService._attach_assignee_profiles
    participant p20 as TaskHierarchyService._load_iteration_tree
    participant p21 as working_today
    participant p22 as AnnualCalendars
    participant p23 as TeamService._member_options
    participant p24 as WorkingDaysResponse
    participant p25 as CollectionLimitExceededError
    participant p26 as GanttAssignee
    participant p27 as GanttMilestone
    participant p28 as InvertedDependency
    participant p29 as HTTPException
    participant p30 as IterationProjectSummary.model_validate
    p0->>p1: TaskService.get_by_iteration
    p0->>p2: TeamService.get_by_iteration
    p0->>p3: CalendarService.calculate_working_days
    p0->>p4: AnnualCalendars.for_iteration
    p0->>p5: _task_to_gantt
    p0->>p6: inverted_saved_dependencies
    p0->>p7: IterationService
    p0->>p8: TaskService
    p0->>p9: TeamService
    p0->>p10: IterationService.get_by_id
    p0->>p11: CalendarService
    p0->>p12: _overdue_task_ids
    p0->>p13: GanttResponse
    p0->>p14: IterationResponse
    p6->>p15: included_work_ids
    p1->>p16: TaskService._task_graph_query
    p5->>p17: task_signals
    p1->>p18: TaskService._load_iteration_tree
    p2->>p19: TeamService._attach_assignee_profiles
    p18->>p20: TaskHierarchyService._load_iteration_tree
    p17->>p21: working_today
    p4->>p22: AnnualCalendars
    p2->>p23: TeamService._member_options
    p3->>p24: WorkingDaysResponse
    p1->>p25: CollectionLimitExceededError
    p5->>p26: GanttAssignee
    p5->>p27: GanttMilestone
    p6->>p28: InvertedDependency
    p0-->>p29: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)
    p0-->>p30: IterationProjectSummary.model_validate(iteration.project)
```

> Call sequence diagram shows 30 of 248 interactions; 218 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 84 (83 omitted); unresolved 1 of 118 (117 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/iteration_service.py:IterationService.get_by_id` | 5 | - | unresolved | 4 |
| `backend/app/services/iteration_service.py:IterationService.get_by_id` | 5 | - | external | 3 |
| `backend/app/services/task_service.py:TaskService.get_by_iteration` | 13 | - | unresolved | 6 |
| `backend/app/services/task_service.py:TaskService._task_graph_query` | 17 | [backend/app/services/task_hierarchy_service.py](../modules/task_hierarchy_service.md) | internal | 2 |
| `backend/app/services/task_hierarchy_service.py:TaskHierarchyService._task_graph_query` | 18 | - | unresolved | 6 |
| `backend/app/services/task_hierarchy_service.py:TaskHierarchyService._task_graph_query` | 18 | - | external | 8 |
| `backend/app/services/task_service.py:TaskService.get_by_iteration` | 13 | - | external | 2 |
| `backend/app/services/task_hierarchy_service.py:TaskHierarchyService._load_iteration_tree` | 41 | - | unresolved | 20 |
> Omission summary shows 8 of 47 groups; 39 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 47; effect analysis evaluated: 25, partial: 0, unavailable: 22. Counts include steps omitted from the displayed trace.

Collector observations for 25 source steps with known totals: observed: 126, emitted: 126, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `get_gantt_data` | `available` | `evaluated` | `available` | `10` | `10` | `0` |
| `IterationService` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `TaskService` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `TeamService` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `IterationService.get_by_id` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `self.db.execute (backend/app/services/iter…terationService.get_by_id)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).options(…).where (backend/app/services/iter…terationService.get_by_id)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).options (backend/app/services/iter…terationService.get_by_id)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select (backend/app/services/iter…terationService.get_by_id)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `selectinload (backend/app/services/iter…terationService.get_by_id)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `selectinload (backend/app/services/iter…terationService.get_by_id)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `result.scalar_one_or_none` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. get_gantt_data"]
    s2["2. IterationService"]
    s3["3. TaskService"]
    s4["4. TeamService"]
    s5["5. IterationService.get_by_id"]
    s6["6. self.db.execute (backend/app/services/iter…terationService.get_by_id)"]
    s7["7. select(…).options(…).where (backend/app/services/iter…terationService.get_by_id)"]
    s8["8. select(…).options (backend/app/services/iter…terationService.get_by_id)"]
    s9["9. select (backend/app/services/iter…terationService.get_by_id)"]
    s10["10. selectinload (backend/app/services/iter…terationService.get_by_id)"]
    s11["11. selectinload (backend/app/services/iter…terationService.get_by_id)"]
    s12["12. result.scalar_one_or_none"]
    s1 -->|"IterationService(db)"| s2
    s1 -->|"TaskService(db)"| s3
    s1 -->|"TeamService(db)"| s4
    s1 -->|"IterationService.get_by_id(iteration_id)"| s5
    s5 -. "self.db.execute (backend/app/services/iter…terationService.get_by_id)(...)" .-> s6
    s5 -. "select(…).options(…).where (backend/app/services/iter…terationService.get_by_id)(...)" .-> s7
    s5 -. "select(…).options (backend/app/services/iter…terationService.get_by_id)(selectinload(...), selectinload(...))" .-> s8
    s5 -. "select (backend/app/services/iter…terationService.get_by_id)(Iteration)" .-> s9
    s5 -. "selectinload (backend/app/services/iter…terationService.get_by_id)(Iteration.calendar)" .-> s10
    s5 -. "selectinload (backend/app/services/iter…terationService.get_by_id)(Iteration.project)" .-> s11
    s5 -. "result.scalar_one_or_none(data not statically known)" .-> s12
    b0["mutation gantt_tasks.append"]
    s1 -. "mutation gantt_tasks.append" .-> b0
    b1["mutation pending.pop"]
    s1 -. "mutation pending.pop" .-> b1
    b2["mutation pending.extend"]
    s1 -. "mutation pending.extend" .-> b2
    b3["mutation vacation_dates.update"]
    s1 -. "mutation vacation_dates.update" .-> b3
    click s1 "../modules/routers_gantt.md"
    click s2 "../modules/iteration_service.md"
    click s3 "../modules/task_service.md"
    click s4 "../modules/team_service.md"
    click s5 "../modules/iteration_service.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_gantt_data` | `iteration_id: int`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | `status` | `node.has_inverted_dependency`, `member_vacations[...]` | `GanttResponse(...)` |
| `IterationService` | - | - | - | - |
| `TaskService` | - | - | - | - |
| `TeamService` | - | - | - | - |
| `IterationService.get_by_id` | `iteration_id: int` | `Iteration` | - | `result.scalar_one_or_none(...)` |
| `self.db.execute (backend/app/services/iter…terationService.get_by_id)` | - | - | - | - |
| `select(…).options(…).where (backend/app/services/iter…terationService.get_by_id)` | - | - | - | - |
| `select(…).options (backend/app/services/iter…terationService.get_by_id)` | - | - | - | - |
| `select (backend/app/services/iter…terationService.get_by_id)` | - | - | - | - |
| `selectinload (backend/app/services/iter…terationService.get_by_id)` | - | - | - | - |
| `selectinload (backend/app/services/iter…terationService.get_by_id)` | - | - | - | - |
| `result.scalar_one_or_none` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_gantt_data | IterationService | 137 | `IterationService(db)` |
| get_gantt_data | TaskService | 138 | `TaskService(db)` |
| get_gantt_data | TeamService | 139 | `TeamService(db)` |
| get_gantt_data | IterationService.get_by_id | 144 | `iteration_service.get_by_id(iteration_id)` |
| IterationService.get_by_id | self.db.execute (backend/app/services/iter…terationService.get_by_id) | 338 | `self.db.execute(...)` |
| IterationService.get_by_id | select(…).options(…).where (backend/app/services/iter…terationService.get_by_id) | 339 | `select(Iteration).options(selectinload(Iteration.calendar), selectinload(Iteration.project)).where(...)` |
| IterationService.get_by_id | select(…).options (backend/app/services/iter…terationService.get_by_id) | 339 | `select(Iteration).options(selectinload(...), selectinload(...))` |
| IterationService.get_by_id | select (backend/app/services/iter…terationService.get_by_id) | 339 | `select(Iteration)` |
| IterationService.get_by_id | selectinload (backend/app/services/iter…terationService.get_by_id) | 341 | `selectinload(Iteration.calendar)` |
| IterationService.get_by_id | selectinload (backend/app/services/iter…terationService.get_by_id) | 342 | `selectinload(Iteration.project)` |
| IterationService.get_by_id | result.scalar_one_or_none | 346 | `result.scalar_one_or_none(data not statically known)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `gantt_tasks.append` | `get_gantt_data` | 179 |
| mutation | `pending.pop` | `get_gantt_data` | 188 |
| mutation | `pending.extend` | `get_gantt_data` | 190 |
| mutation | `vacation_dates.update` | `get_gantt_data` | 209 |

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
| step_limit | `get_gantt_data` | `first 12 steps` | 0 |

## Behavior

This flow starts at `get_gantt_data` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
