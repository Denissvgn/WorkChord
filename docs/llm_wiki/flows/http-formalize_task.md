# formalize_task

**Entry point:** `formalize_task` (`http`)
**Source:** [routers_llm](../modules/routers_llm.md)
**Modules touched:** [query_limits](../modules/query_limits.md), [routers_llm](../modules/routers_llm.md), [task_hierarchy_service](../modules/task_hierarchy_service.md), [task_service](../modules/task_service.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as formalize_task
    participant p1 as TaskService.get_by_id
    participant p2 as TaskService
    participant p3 as TaskService._load_iteration_tree
    participant p4 as TaskHierarchyService._load_iteration_tree
    participant p5 as TaskHierarchyService
    participant p6 as CollectionLimitExceededError
    participant p7 as TaskHierarchyService._task_graph_query
    participant p8 as HTTPException
    participant p9 as db.rollback
    participant p10 as llm_service.formalize_task
    participant p11 as (…).first
    participant p12 as self.db.execute (backend/app/services/task…e.py:TaskService.get_by_id)
    participant p13 as select(…).where (backend/app/services/task…e.py:TaskService.get_by_id)
    participant p14 as select (backend/app/services/task…e.py:TaskService.get_by_id)
    participant p15 as tasks_by_id.get
    participant p16 as select(…).where(…).limit
    participant p17 as select(…).where (backend/app/services/task…rvice._load_iteration_tree)
    participant p18 as select (backend/app/services/task…rvice._load_iteration_tree)
    participant p19 as len
    participant p20 as (…).all
    participant p21 as self.db.scalars
    participant p22 as self.db.execute (backend/app/services/task…rvice._load_iteration_tree)
    participant p23 as self._task_graph_query(…).limit
    participant p24 as list
    participant p25 as result.scalars().all
    participant p26 as result.scalars
    participant p27 as self.load_owner_names
    participant p28 as select(…).where(…).options(…).order_by
    p0->>p1: TaskService.get_by_id
    p0->>p2: TaskService
    p1->>p3: TaskService._load_iteration_tree
    p3->>p4: TaskHierarchyService._load_iteration_tree
    p3->>p5: TaskHierarchyService
    p4->>p6: CollectionLimitExceededError
    p4->>p7: TaskHierarchyService._task_graph_query
    p0-->>p8: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)
    p0-->>p9: db.rollback
    p0-->>p10: llm_service.formalize_task(title=title, description=description, context=data.context)
    p1-->>p11: (…).first
    p1-->>p12: self.db.execute (backend/app/services/task…e.py:TaskService.get_by_id)(...)
    p1-->>p13: select(…).where (backend/app/services/task…e.py:TaskService.get_by_id)(...)
    p1-->>p14: select (backend/app/services/task…e.py:TaskService.get_by_id)(Task.iteration_id, Task.project_id)
    p1-->>p15: tasks_by_id.get(task_id)
    p4-->>p16: select(…).where(…).limit(...)
    p4-->>p17: select(…).where (backend/app/services/task…rvice._load_iteration_tree)(..., ...)
    p4-->>p18: select (backend/app/services/task…rvice._load_iteration_tree)(Task.id)
    p4-->>p19: len(...)
    p4-->>p20: (…).all
    p4-->>p21: self.db.scalars(identities)
    p4-->>p22: self.db.execute (backend/app/services/task…rvice._load_iteration_tree)(...)
    p4-->>p23: self._task_graph_query(…).limit(...)
    p4-->>p24: list(...)
    p4-->>p25: result.scalars().all
    p4-->>p26: result.scalars
    p4-->>p19: len(tasks)
    p4-->>p27: self.load_owner_names(tasks)
    p4-->>p22: self.db.execute (backend/app/services/task…rvice._load_iteration_tree)(...)
    p4-->>p28: select(…).where(…).options(…).order_by(TaskDependency.task_id, TaskDependency.id)
```

> Call sequence diagram shows 30 of 61 interactions; 31 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 6 of 21 (15 omitted); unresolved 17 of 32 (15 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/task_hierarchy_service.py:TaskHierarchyService._task_graph_query` | 19 | - | unresolved | 6 |
| `backend/app/services/task_hierarchy_service.py:TaskHierarchyService._task_graph_query` | 19 | - | external | 8 |
| `backend/app/services/task_hierarchy_service.py:TaskHierarchyService._load_iteration_tree` | 9 | [backend/app/query_limits.py](../modules/query_limits.md) | internal | 1 |
| `backend/app/services/task_hierarchy_service.py:TaskHierarchyService._load_iteration_tree` | 9 | - | unresolved | 9 |
| `backend/app/services/task_hierarchy_service.py:TaskHierarchyService._load_iteration_tree` | 9 | - | external | 7 |
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 9; effect analysis evaluated: 5, partial: 0, unavailable: 4. Counts include steps omitted from the displayed trace.

Collector observations for 5 source steps with known totals: observed: 24, emitted: 24, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `formalize_task` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `TaskService` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `TaskService.get_by_id` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `(…).first` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `self.db.execute (backend/app/services/task…e.py:TaskService.get_by_id)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).where (backend/app/services/task…e.py:TaskService.get_by_id)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select (backend/app/services/task…e.py:TaskService.get_by_id)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `TaskService._load_iteration_tree` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `TaskHierarchyService._load_iteration_tree` | `available` | `evaluated` | `available` | `7` | `7` | `0` |
| `select(…).where(…).limit` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select(…).where (backend/app/services/task…rvice._load_iteration_tree)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `select (backend/app/services/task…rvice._load_iteration_tree)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. formalize_task"]
    s2["2. TaskService"]
    s3["3. TaskService.get_by_id"]
    s4["4. (…).first"]
    s5["5. self.db.execute (backend/app/services/task…e.py:TaskService.get_by_id)"]
    s6["6. select(…).where (backend/app/services/task…e.py:TaskService.get_by_id)"]
    s7["7. select (backend/app/services/task…e.py:TaskService.get_by_id)"]
    s8["8. TaskService._load_iteration_tree"]
    s9["9. TaskHierarchyService._load_iteration_tree"]
    s10["10. select(…).where(…).limit"]
    s11["11. select(…).where (backend/app/services/task…rvice._load_iteration_tree)"]
    s12["12. select (backend/app/services/task…rvice._load_iteration_tree)"]
    s1 -->|"TaskService(db)"| s2
    s1 -->|"TaskService.get_by_id(task_id)"| s3
    s3 -. "(…).first(data not statically known)" .-> s4
    s3 -. "self.db.execute (backend/app/services/task…e.py:TaskService.get_by_id)(...)" .-> s5
    s3 -. "select(…).where (backend/app/services/task…e.py:TaskService.get_by_id)(...)" .-> s6
    s3 -. "select (backend/app/services/task…e.py:TaskService.get_by_id)(Task.iteration_id, Task.project_id)" .-> s7
    s3 -->|"TaskService._load_iteration_tree(row.iteration_id, project_id=row.project_id)"| s8
    s8 -->|"TaskHierarchyService._load_iteration_tree(iteration_id, max_tasks=max_tasks, project_id=project_id)"| s9
    s9 -. "select(…).where(…).limit(...)" .-> s10
    s9 -. "select(…).where (backend/app/services/task…rvice._load_iteration_tree)(..., ...)" .-> s11
    s9 -. "select (backend/app/services/task…rvice._load_iteration_tree)(Task.id)" .-> s12
    b0["mutation roots.append"]
    s9 -. "mutation roots.append" .-> b0
    b1["mutation roots.sort"]
    s9 -. "mutation roots.sort" .-> b1
    click s1 "../modules/routers_llm.md"
    click s2 "../modules/task_service.md"
    click s3 "../modules/task_service.md"
    click s8 "../modules/task_service.md"
    click s9 "../modules/task_hierarchy_service.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `formalize_task` | `task_id: int`, `data: FormalizeRequest`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]`, `llm_service: Annotated[LLMService, Depends(get_llm_service)]` | `status` | - | `...` |
| `TaskService` | - | - | - | - |
| `TaskService.get_by_id` | `task_id: int` | - | - | `None`, `tasks_by_id.get(...)` |
| `(…).first` | - | - | - | - |
| `self.db.execute (backend/app/services/task…e.py:TaskService.get_by_id)` | - | - | - | - |
| `select(…).where (backend/app/services/task…e.py:TaskService.get_by_id)` | - | - | - | - |
| `select (backend/app/services/task…e.py:TaskService.get_by_id)` | - | - | - | - |
| `TaskService._load_iteration_tree` | `iteration_id: int`, `max_tasks: int`, `project_id: int \| None` | - | - | `...` |
| `TaskHierarchyService._load_iteration_tree` | `iteration_id: int`, `max_tasks: int`, `project_id: int \| None` | `TaskDependency` | - | `(...)` |
| `select(…).where(…).limit` | - | - | - | - |
| `select(…).where (backend/app/services/task…rvice._load_iteration_tree)` | - | - | - | - |
| `select (backend/app/services/task…rvice._load_iteration_tree)` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| formalize_task | TaskService | 178 | `TaskService(db)` |
| formalize_task | TaskService.get_by_id | 179 | `task_service.get_by_id(task_id)` |
| TaskService.get_by_id | (…).first | 570 | `(await self.db.execute(select(Task.iteration_id, Task.project_id).where(Task.id == task_id))).first(data not statically known)` |
| TaskService.get_by_id | self.db.execute (backend/app/services/task…e.py:TaskService.get_by_id) | 570 | `self.db.execute(...)` |
| TaskService.get_by_id | select(…).where (backend/app/services/task…e.py:TaskService.get_by_id) | 570 | `select(Task.iteration_id, Task.project_id).where(...)` |
| TaskService.get_by_id | select (backend/app/services/task…e.py:TaskService.get_by_id) | 570 | `select(Task.iteration_id, Task.project_id)` |
| TaskService.get_by_id | TaskService._load_iteration_tree | 573 | `self._load_iteration_tree(row.iteration_id, project_id=row.project_id)` |
| TaskService._load_iteration_tree | TaskHierarchyService._load_iteration_tree | 561 | `TaskHierarchyService(self.db, self.load_owner_names)._load_iteration_tree(iteration_id, max_tasks=max_tasks, project_id=project_id)` |
| TaskHierarchyService._load_iteration_tree | select(…).where(…).limit | 46 | `select(Task.id).where(Task.iteration_id == iteration_id, *([Task.project_id == project_id] if iteration_id is None else [])).limit(...)` |
| TaskHierarchyService._load_iteration_tree | select(…).where (backend/app/services/task…rvice._load_iteration_tree) | 46 | `select(Task.id).where(..., ...)` |
| TaskHierarchyService._load_iteration_tree | select (backend/app/services/task…rvice._load_iteration_tree) | 46 | `select(Task.id)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `roots.append` | `TaskHierarchyService._load_iteration_tree` | 109 |
| mutation | `roots.sort` | `TaskHierarchyService._load_iteration_tree` | 122 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `TaskService.get_by_id` | `(await self.db.execute(select(Task.iteration_id, Task.project_id).where(Task.id == task_id))).first` | 570 |
| unresolved_call | `TaskService.get_by_id` | `self.db.execute` | 570 |
| unresolved_call | `TaskService.get_by_id` | `select(Task.iteration_id, Task.project_id).where` | 570 |
| external_call | `TaskService.get_by_id` | `select` | 570 |
| unresolved_call | `TaskHierarchyService._load_iteration_tree` | `select(Task.id).where(Task.iteration_id == iteration_id, *([Task.project_id == project_id] if iteration_id is None else [])).limit` | 46 |
| unresolved_call | `TaskHierarchyService._load_iteration_tree` | `select(Task.id).where` | 46 |
| external_call | `TaskHierarchyService._load_iteration_tree` | `select` | 46 |
| step_limit | `formalize_task` | `first 12 steps` | 0 |

## Behavior

This flow starts at `formalize_task` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
