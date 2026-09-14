# delete_task

**Entry point:** `delete_task` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [schemas_common](../modules/schemas_common.md), [tasks](../modules/tasks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as delete_task
    participant p1 as service.delete
    participant p2 as HTTPException
    participant p3 as MessageResponse
    p0-->>p1: service.delete
    p0-->>p2: HTTPException
    p0->>p3: MessageResponse
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. delete_task"]
    s2["2. service.delete"]
    s3["3. HTTPException"]
    s4["4. MessageResponse"]
    s1 -. "service.delete(task_id)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s3
    s1 -->|"MessageResponse(message=..., success=True)"| s4
    click s1 "../modules/tasks.md"
    click s4 "../modules/schemas_common.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `delete_task` | `task_id: int`, `service: Annotated[TaskService, Depends(get_task_service)]` | `status` | - | `MessageResponse(...)` |
| `service.delete` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `MessageResponse` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| delete_task | service.delete | 409 | `service.delete(task_id)` |
| delete_task | HTTPException | 411 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| delete_task | MessageResponse | 415 | `MessageResponse(message=..., success=True)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `delete_task` | `service.delete` | 409 |
| external_call | `delete_task` | `HTTPException` | 411 |

## Behavior

This flow starts at `delete_task` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
