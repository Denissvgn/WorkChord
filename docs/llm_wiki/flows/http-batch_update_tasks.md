# batch_update_tasks

**Entry point:** `batch_update_tasks` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [iteration_service](../modules/iteration_service.md), [schemas_task](../modules/schemas_task.md), [tasks](../modules/tasks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as batch_update_tasks
    participant p1 as IterationService
    participant p2 as iteration_service.get_by_id
    participant p3 as HTTPException (backend/app/routers/tasks.py:batch_update_tasks)
    participant p4 as apply_batch_update_items
    participant p5 as service.get_by_id
    participant p6 as ValueError
    participant p7 as hasattr
    participant p8 as service.change_status
    participant p9 as item.update.model_dump
    participant p10 as update_values.pop
    participant p11 as TaskUpdate
    participant p12 as service.update
    participant p13 as updated_tasks_list.append
    participant p14 as service.task_to_response
    participant p15 as results.append
    participant p16 as TaskBatchUpdateResponseItem
    participant p17 as db.commit
    participant p18 as db.rollback
    participant p19 as isinstance
    participant p20 as _raise_task_version_conflict
    participant p21 as HTTPException (backend/app/routers/tasks…aise_task_version_conflict)
    participant p22 as exc.detail
    p0->>p1: IterationService
    p0-->>p2: iteration_service.get_by_id
    p0-->>p3: HTTPException (backend/app/routers/tasks.py:batch_update_tasks)
    p0->>p4: apply_batch_update_items
    p4-->>p5: service.get_by_id
    p4-->>p6: ValueError
    p4-->>p6: ValueError
    p4-->>p7: hasattr
    p4-->>p7: hasattr
    p4-->>p8: service.change_status
    p4-->>p6: ValueError
    p4-->>p9: item.update.model_dump
    p4-->>p10: update_values.pop
    p4->>p11: TaskUpdate
    p4-->>p12: service.update
    p4-->>p9: item.update.model_dump
    p4-->>p10: update_values.pop
    p4->>p11: TaskUpdate
    p4-->>p12: service.update
    p4-->>p6: ValueError
    p4-->>p13: updated_tasks_list.append
    p4-->>p14: service.task_to_response
    p4-->>p15: results.append
    p4->>p16: TaskBatchUpdateResponseItem
    p0-->>p17: db.commit
    p0-->>p18: db.rollback
    p0-->>p19: isinstance
    p0->>p20: _raise_task_version_conflict
    p20-->>p21: HTTPException (backend/app/routers/tasks…aise_task_version_conflict)
    p20-->>p22: exc.detail
```

> Call sequence diagram shows 30 of 36 interactions; 6 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. batch_update_tasks"]
    s2["2. IterationService"]
    s3["3. iteration_service.get_by_id"]
    s4["4. HTTPException (backend/app/routers/tasks.py:batch_update_tasks)"]
    s5["5. apply_batch_update_items"]
    s6["6. service.get_by_id"]
    s7["7. ValueError"]
    s8["8. ValueError"]
    s9["9. hasattr"]
    s10["10. hasattr"]
    s11["11. service.change_status"]
    s12["12. ValueError"]
    s1 -->|"IterationService(db)"| s2
    s1 -. "iteration_service.get_by_id(iteration_id)" .-> s3
    s1 -. "HTTPException (backend/app/routers/tasks.py:batch_update_tasks)(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s4
    s1 -->|"apply_batch_update_items(service, iteration_id, iteration.end_date, data.tasks)"| s5
    s5 -. "service.get_by_id(item.task_id)" .-> s6
    s5 -. "ValueError(...)" .-> s7
    s5 -. "ValueError(...)" .-> s8
    s5 -. "hasattr(task.status, 'value')" .-> s9
    s5 -. "hasattr(item.update.status, 'value')" .-> s10
    s5 -. "service.change_status(task_id=item.task_id, new_status=item.update.status, reason=item.status_reason, expected_version=expected_version)" .-> s11
    s5 -. "ValueError(...)" .-> s12
    b0["mutation update_values.pop"]
    s5 -. "mutation update_values.pop" .-> b0
    b1["mutation service.update"]
    s5 -. "mutation service.update" .-> b1
    b2["mutation update_values.pop"]
    s5 -. "mutation update_values.pop" .-> b2
    b3["mutation service.update"]
    s5 -. "mutation service.update" .-> b3
    b4["mutation updated_tasks_list.append"]
    s5 -. "mutation updated_tasks_list.append" .-> b4
    b5["mutation results.append"]
    s5 -. "mutation results.append" .-> b5
    click s1 "../modules/tasks.md"
    click s2 "../modules/iteration_service.md"
    click s5 "../modules/tasks.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
    class b4 boundary
    class b5 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `batch_update_tasks` | `iteration_id: int`, `data: TaskBatchUpdateRequest`, `service: Annotated[TaskService, Depends(get_task_service)]`, `scheduler_service: Annotated[SchedulerService, Depends(get_scheduler_service)]`, `db: Annotated[AsyncSession, Depends(get_db)]` | `status`, `TaskVersionConflictError`, `status` | `db.commit`, `db.commit`, `db.commit` | `TaskBatchUpdateResponse(...)` |
| `IterationService` | - | - | - | - |
| `iteration_service.get_by_id` | - | - | - | - |
| `HTTPException (backend/app/routers/tasks.py:batch_update_tasks)` | - | - | - | - |
| `apply_batch_update_items` | `service: TaskService`, `iteration_id: int`, `iteration_end_date`, `items` | - | `update_values[...]`, `update_values[...]` | `(...)` |
| `service.get_by_id` | - | - | - | - |
| `ValueError` | - | - | - | - |
| `ValueError` | - | - | - | - |
| `hasattr` | - | - | - | - |
| `hasattr` | - | - | - | - |
| `service.change_status` | - | - | - | - |
| `ValueError` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| batch_update_tasks | IterationService | 236 | `IterationService(db)` |
| batch_update_tasks | iteration_service.get_by_id | 237 | `iteration_service.get_by_id(iteration_id)` |
| batch_update_tasks | HTTPException (backend/app/routers/tasks.py:batch_update_tasks) | 239 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| batch_update_tasks | apply_batch_update_items | 250 | `apply_batch_update_items(service, iteration_id, iteration.end_date, data.tasks)` |
| apply_batch_update_items | service.get_by_id | 175 | `service.get_by_id(item.task_id)` |
| apply_batch_update_items | ValueError | 177 | `ValueError(...)` |
| apply_batch_update_items | ValueError | 179 | `ValueError(...)` |
| apply_batch_update_items | hasattr | 182 | `hasattr(task.status, 'value')` |
| apply_batch_update_items | hasattr | 183 | `hasattr(item.update.status, 'value')` |
| apply_batch_update_items | service.change_status | 192 | `service.change_status(task_id=item.task_id, new_status=item.update.status, reason=item.status_reason, expected_version=expected_version)` |
| apply_batch_update_items | ValueError | 199 | `ValueError(...)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `update_values.pop` | `apply_batch_update_items` | 203 |
| mutation | `service.update` | `apply_batch_update_items` | 207 |
| mutation | `update_values.pop` | `apply_batch_update_items` | 211 |
| mutation | `service.update` | `apply_batch_update_items` | 215 |
| mutation | `updated_tasks_list.append` | `apply_batch_update_items` | 221 |
| mutation | `results.append` | `apply_batch_update_items` | 222 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `batch_update_tasks` | `iteration_service.get_by_id` | 237 |
| external_call | `batch_update_tasks` | `HTTPException` | 239 |
| unresolved_call | `apply_batch_update_items` | `service.get_by_id` | 175 |
| external_call | `apply_batch_update_items` | `ValueError` | 177 |
| external_call | `apply_batch_update_items` | `ValueError` | 179 |
| external_call | `apply_batch_update_items` | `hasattr` | 182 |
| external_call | `apply_batch_update_items` | `hasattr` | 183 |
| unresolved_call | `apply_batch_update_items` | `service.change_status` | 192 |
| external_call | `apply_batch_update_items` | `ValueError` | 199 |
| step_limit | `batch_update_tasks` | `first 12 steps` | 0 |

## Behavior

This flow starts at `batch_update_tasks` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
