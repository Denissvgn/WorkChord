# preview_iteration_schedule

**Entry point:** `preview_iteration_schedule` (`http`)
**Source:** [routers_gantt](../modules/routers_gantt.md)
**Modules touched:** [iteration_service](../modules/iteration_service.md), [routers_gantt](../modules/routers_gantt.md), [schemas_gantt](../modules/schemas_gantt.md), [schemas_task](../modules/schemas_task.md), and 2 more

**Complete modules touched:**

- [iteration_service](../modules/iteration_service.md)
- [routers_gantt](../modules/routers_gantt.md)
- [schemas_gantt](../modules/schemas_gantt.md)
- [schemas_task](../modules/schemas_task.md)
- [task_service](../modules/task_service.md)
- [tasks](../modules/tasks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as preview_iteration_schedule
    participant p1 as IterationService
    participant p2 as TaskService
    participant p3 as iteration_service.get_by_id
    participant p4 as HTTPException
    participant p5 as apply_batch_update_items
    participant p6 as service.get_by_id
    participant p7 as ValueError
    participant p8 as hasattr
    participant p9 as service.change_status
    participant p10 as item.update.model_dump
    participant p11 as update_values.pop
    participant p12 as TaskUpdate
    participant p13 as service.update
    participant p14 as updated_tasks_list.append
    participant p15 as service.task_to_response
    participant p16 as results.append
    participant p17 as TaskBatchUpdateResponseItem
    participant p18 as service.schedule_iteration
    participant p19 as task_service.get_by_iteration
    participant p20 as _task_to_gantt
    participant p21 as attributes.instance_state
    p0->>p1: IterationService
    p0->>p2: TaskService
    p0-->>p3: iteration_service.get_by_id
    p0-->>p4: HTTPException
    p0->>p5: apply_batch_update_items
    p5-->>p6: service.get_by_id
    p5-->>p7: ValueError
    p5-->>p7: ValueError
    p5-->>p8: hasattr
    p5-->>p8: hasattr
    p5-->>p9: service.change_status
    p5-->>p7: ValueError
    p5-->>p10: item.update.model_dump
    p5-->>p11: update_values.pop
    p5->>p12: TaskUpdate
    p5-->>p13: service.update
    p5-->>p10: item.update.model_dump
    p5-->>p11: update_values.pop
    p5->>p12: TaskUpdate
    p5-->>p13: service.update
    p5-->>p7: ValueError
    p5-->>p14: updated_tasks_list.append
    p5-->>p15: service.task_to_response
    p5-->>p16: results.append
    p5->>p17: TaskBatchUpdateResponseItem
    p0-->>p18: service.schedule_iteration
    p0-->>p19: task_service.get_by_iteration
    p0->>p20: _task_to_gantt
    p20-->>p21: attributes.instance_state
    p20-->>p21: attributes.instance_state
```

> Call sequence diagram shows 30 of 60 interactions; 30 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. preview_iteration_schedule"]
    s2["2. IterationService"]
    s3["3. TaskService"]
    s4["4. iteration_service.get_by_id"]
    s5["5. HTTPException"]
    s6["6. apply_batch_update_items"]
    s7["7. service.get_by_id"]
    s8["8. ValueError"]
    s9["9. ValueError"]
    s10["10. hasattr"]
    s11["11. hasattr"]
    s12["12. service.change_status"]
    s1 -->|"IterationService(db)"| s2
    s1 -->|"TaskService(db)"| s3
    s1 -. "iteration_service.get_by_id(iteration_id)" .-> s4
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s5
    s1 -->|"apply_batch_update_items(task_service, iteration_id, iteration.end_date, data.changes)"| s6
    s6 -. "service.get_by_id(item.task_id)" .-> s7
    s6 -. "ValueError(...)" .-> s8
    s6 -. "ValueError(...)" .-> s9
    s6 -. "hasattr(task.status, 'value')" .-> s10
    s6 -. "hasattr(item.update.status, 'value')" .-> s11
    s6 -. "service.change_status(task_id=item.task_id, new_status=item.update.status, reason=item.status_reason, expected_version=expected_version)" .-> s12
    b0["mutation gantt_tasks.append"]
    s1 -. "mutation gantt_tasks.append" .-> b0
    b1["mutation overdue_ids.append"]
    s1 -. "mutation overdue_ids.append" .-> b1
    b2["mutation overdue_ids.append"]
    s1 -. "mutation overdue_ids.append" .-> b2
    b3["mutation update_values.pop"]
    s6 -. "mutation update_values.pop" .-> b3
    b4["mutation service.update"]
    s6 -. "mutation service.update" .-> b4
    b5["mutation update_values.pop"]
    s6 -. "mutation update_values.pop" .-> b5
    b6["mutation service.update"]
    s6 -. "mutation service.update" .-> b6
    b7["mutation updated_tasks_list.append"]
    s6 -. "mutation updated_tasks_list.append" .-> b7
    click s1 "../modules/routers_gantt.md"
    click s2 "../modules/iteration_service.md"
    click s3 "../modules/task_service.md"
    click s6 "../modules/tasks.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
    class b4 boundary
    class b5 boundary
    class b6 boundary
    class b7 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `preview_iteration_schedule` | `iteration_id: int`, `data: SchedulePreviewRequest`, `service: Annotated[SchedulerService, Depends(get_scheduler_service)]`, `db: Annotated[AsyncSession, Depends(get_db)]` | `status`, `status`, `status` | `db.commit`, `db.commit` | `SchedulePreviewResponse(...)` |
| `IterationService` | - | - | - | - |
| `TaskService` | - | - | - | - |
| `iteration_service.get_by_id` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `apply_batch_update_items` | `service: TaskService`, `iteration_id: int`, `iteration_end_date`, `items` | - | `update_values[...]`, `update_values[...]` | `(...)` |
| `service.get_by_id` | - | - | - | - |
| `ValueError` | - | - | - | - |
| `ValueError` | - | - | - | - |
| `hasattr` | - | - | - | - |
| `hasattr` | - | - | - | - |
| `service.change_status` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| preview_iteration_schedule | IterationService | 68 | `IterationService(db)` |
| preview_iteration_schedule | TaskService | 69 | `TaskService(db)` |
| preview_iteration_schedule | iteration_service.get_by_id | 70 | `iteration_service.get_by_id(iteration_id)` |
| preview_iteration_schedule | HTTPException | 72 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| preview_iteration_schedule | apply_batch_update_items | 86 | `apply_batch_update_items(task_service, iteration_id, iteration.end_date, data.changes)` |
| apply_batch_update_items | service.get_by_id | 175 | `service.get_by_id(item.task_id)` |
| apply_batch_update_items | ValueError | 177 | `ValueError(...)` |
| apply_batch_update_items | ValueError | 179 | `ValueError(...)` |
| apply_batch_update_items | hasattr | 182 | `hasattr(task.status, 'value')` |
| apply_batch_update_items | hasattr | 183 | `hasattr(item.update.status, 'value')` |
| apply_batch_update_items | service.change_status | 192 | `service.change_status(task_id=item.task_id, new_status=item.update.status, reason=item.status_reason, expected_version=expected_version)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `gantt_tasks.append` | `preview_iteration_schedule` | 101 |
| mutation | `overdue_ids.append` | `preview_iteration_schedule` | 103 |
| mutation | `overdue_ids.append` | `preview_iteration_schedule` | 106 |
| mutation | `update_values.pop` | `apply_batch_update_items` | 203 |
| mutation | `service.update` | `apply_batch_update_items` | 207 |
| mutation | `update_values.pop` | `apply_batch_update_items` | 211 |
| mutation | `service.update` | `apply_batch_update_items` | 215 |
| mutation | `updated_tasks_list.append` | `apply_batch_update_items` | 221 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `preview_iteration_schedule` | `iteration_service.get_by_id` | 70 |
| external_call | `preview_iteration_schedule` | `HTTPException` | 72 |
| unresolved_call | `apply_batch_update_items` | `service.get_by_id` | 175 |
| external_call | `apply_batch_update_items` | `ValueError` | 177 |
| external_call | `apply_batch_update_items` | `ValueError` | 179 |
| external_call | `apply_batch_update_items` | `hasattr` | 182 |
| external_call | `apply_batch_update_items` | `hasattr` | 183 |
| unresolved_call | `apply_batch_update_items` | `service.change_status` | 192 |
| step_limit | `preview_iteration_schedule` | `first 12 steps` | 0 |

## Behavior

This flow starts at `preview_iteration_schedule` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
