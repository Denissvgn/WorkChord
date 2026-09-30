# add_dependency

**Entry point:** `add_dependency` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [schemas_common](../modules/schemas_common.md), [tasks](../modules/tasks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as add_dependency
    participant p1 as service.add_dependency
    participant p2 as HTTPException
    participant p3 as str
    participant p4 as MessageResponse
    p0-->>p1: service.add_dependency
    p0-->>p2: HTTPException
    p0-->>p3: str
    p0-->>p2: HTTPException
    p0->>p4: MessageResponse
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. add_dependency"]
    s2["2. service.add_dependency"]
    s3["3. HTTPException"]
    s4["4. str"]
    s5["5. HTTPException"]
    s6["6. MessageResponse"]
    s1 -. "service.add_dependency(task_id, data.depends_on_id)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s3
    s1 -. "str(e)" .-> s4
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Could not add dependency. Check that both tasks exist and are different.')" .-> s5
    s1 -->|"MessageResponse(message=..., success=True)"| s6
    click s1 "../modules/tasks.md"
    click s6 "../modules/schemas_common.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `add_dependency` | `task_id: int`, `data: TaskDependencyCreate`, `service: Annotated[TaskService, Depends(get_task_service)]` | `status`, `status` | - | `MessageResponse(...)` |
| `service.add_dependency` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `MessageResponse` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| add_dependency | service.add_dependency | 617 | `service.add_dependency(task_id, data.depends_on_id)` |
| add_dependency | HTTPException | 619 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| add_dependency | str | 621 | `str(e)` |
| add_dependency | HTTPException | 624 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Could not add dependency. Check that both tasks exist and are different.')` |
| add_dependency | MessageResponse | 628 | `MessageResponse(message=..., success=True)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `add_dependency` | `service.add_dependency` | 617 |
| external_call | `add_dependency` | `HTTPException` | 619 |
| external_call | `add_dependency` | `HTTPException` | 624 |

## Behavior

This flow starts at `add_dependency` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

Actual dependency changes invalidate current progress and acceptance through general updates and individual add/remove commands. Immutable evidence history remains available, a command reserves one task version, and no-op dependency requests retain their current version. Locked graph relationships are loaded explicitly before applying a dependency update.
