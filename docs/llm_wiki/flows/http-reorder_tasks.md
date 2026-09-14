# reorder_tasks

**Entry point:** `reorder_tasks` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [schemas_common](../modules/schemas_common.md), [tasks](../modules/tasks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as reorder_tasks
    participant p1 as service.reorder_tasks
    participant p2 as HTTPException
    participant p3 as str
    participant p4 as MessageResponse
    p0-->>p1: service.reorder_tasks
    p0-->>p2: HTTPException
    p0-->>p3: str
    p0->>p4: MessageResponse
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. reorder_tasks"]
    s2["2. service.reorder_tasks"]
    s3["3. HTTPException"]
    s4["4. str"]
    s5["5. MessageResponse"]
    s1 -. "service.reorder_tasks(data.task_ids, iteration_id=data.iteration_id, parent_id=data.parent_id)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s3
    s1 -. "str(e)" .-> s4
    s1 -->|"MessageResponse(message='Tasks reordered', success=True)"| s5
    click s1 "../modules/tasks.md"
    click s5 "../modules/schemas_common.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `reorder_tasks` | `data: TaskReorder`, `service: Annotated[TaskService, Depends(get_task_service)]` | `status` | - | `MessageResponse(...)` |
| `service.reorder_tasks` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `MessageResponse` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| reorder_tasks | service.reorder_tasks | 673 | `service.reorder_tasks(data.task_ids, iteration_id=data.iteration_id, parent_id=data.parent_id)` |
| reorder_tasks | HTTPException | 679 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| reorder_tasks | str | 679 | `str(e)` |
| reorder_tasks | MessageResponse | 680 | `MessageResponse(message='Tasks reordered', success=True)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `reorder_tasks` | `service.reorder_tasks` | 673 |
| external_call | `reorder_tasks` | `HTTPException` | 679 |

## Behavior

This flow starts at `reorder_tasks` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
