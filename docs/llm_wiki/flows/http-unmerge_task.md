# unmerge_task

**Entry point:** `unmerge_task` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [iteration_service](../modules/iteration_service.md), [tasks](../modules/tasks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as unmerge_task
    participant p1 as service.get_by_id
    participant p2 as HTTPException
    participant p3 as len
    participant p4 as IterationService
    participant p5 as iteration_service.get_by_id
    participant p6 as service.unmerge_task
    participant p7 as service.task_to_response
    p0-->>p1: service.get_by_id
    p0-->>p2: HTTPException
    p0-->>p3: len
    p0-->>p2: HTTPException
    p0->>p4: IterationService
    p0-->>p5: iteration_service.get_by_id
    p0-->>p6: service.unmerge_task
    p0-->>p7: service.task_to_response
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. unmerge_task"]
    s2["2. service.get_by_id"]
    s3["3. HTTPException"]
    s4["4. len"]
    s5["5. HTTPException"]
    s6["6. IterationService"]
    s7["7. iteration_service.get_by_id"]
    s8["8. service.unmerge_task"]
    s9["9. service.task_to_response"]
    s1 -. "service.get_by_id(task_id)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s3
    s1 -. "len(task.children)" .-> s4
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Task has no children to unmerge')" .-> s5
    s1 -->|"IterationService(db)"| s6
    s1 -. "iteration_service.get_by_id(task.iteration_id)" .-> s7
    s1 -. "service.unmerge_task(task_id, data.delete_parent, expected_revisions=...)" .-> s8
    s1 -. "service.task_to_response(t, ...)" .-> s9
    click s1 "../modules/tasks.md"
    click s6 "../modules/iteration_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `unmerge_task` | `task_id: int`, `data: TaskUnmerge`, `service: Annotated[TaskService, Depends(get_task_service)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | `status`, `status` | - | `...` |
| `service.get_by_id` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `len` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `IterationService` | - | - | - | - |
| `iteration_service.get_by_id` | - | - | - | - |
| `service.unmerge_task` | - | - | - | - |
| `service.task_to_response` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| unmerge_task | service.get_by_id | 744 | `service.get_by_id(task_id)` |
| unmerge_task | HTTPException | 746 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| unmerge_task | len | 751 | `len(task.children)` |
| unmerge_task | HTTPException | 752 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Task has no children to unmerge')` |
| unmerge_task | IterationService | 757 | `IterationService(db)` |
| unmerge_task | iteration_service.get_by_id | 758 | `iteration_service.get_by_id(task.iteration_id)` |
| unmerge_task | service.unmerge_task | 760 | `service.unmerge_task(task_id, data.delete_parent, expected_revisions=...)` |
| unmerge_task | service.task_to_response | 762 | `service.task_to_response(t, ...)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `unmerge_task` | `service.get_by_id` | 744 |
| external_call | `unmerge_task` | `HTTPException` | 746 |
| external_call | `unmerge_task` | `HTTPException` | 752 |
| unresolved_call | `unmerge_task` | `iteration_service.get_by_id` | 758 |
| unresolved_call | `unmerge_task` | `service.unmerge_task` | 760 |
| unresolved_call | `unmerge_task` | `service.task_to_response` | 762 |

## Behavior

This flow starts at `unmerge_task` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
