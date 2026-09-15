# reorder_tasks

**Entry point:** `reorder_tasks` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [commands](../modules/commands.md), [schemas_common](../modules/schemas_common.md), [tasks](../modules/tasks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as reorder_tasks
    participant p1 as service.reorder_tasks
    participant p2 as HTTPException
    participant p3 as str
    participant p4 as current_command
    participant p5 as getattr
    participant p6 as isinstance
    participant p7 as info.get
    participant p8 as MessageResponse
    p0-->>p1: service.reorder_tasks
    p0-->>p2: HTTPException
    p0-->>p3: str
    p0->>p4: current_command
    p4-->>p5: getattr
    p4-->>p6: isinstance
    p4-->>p7: info.get
    p0-->>p3: str
    p0->>p8: MessageResponse
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. reorder_tasks"]
    s2["2. service.reorder_tasks"]
    s3["3. HTTPException"]
    s4["4. str"]
    s5["5. current_command"]
    s6["6. getattr"]
    s7["7. isinstance"]
    s8["8. info.get"]
    s9["9. str"]
    s10["10. MessageResponse"]
    s1 -. "service.reorder_tasks(data.task_ids, iteration_id=data.iteration_id, parent_id=data.parent_id, expected_revision=data.expected_revision)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s3
    s1 -. "str(e)" .-> s4
    s1 -->|"current_command(service.db)"| s5
    s5 -. "getattr(db, 'info', None)" .-> s6
    s5 -. "isinstance(info, dict)" .-> s7
    s5 -. "info.get('command')" .-> s8
    s1 -. "str(...)" .-> s9
    s1 -->|"MessageResponse(message='Tasks reordered', success=True)"| s10
    click s1 "../modules/tasks.md"
    click s5 "../modules/commands.md"
    click s10 "../modules/schemas_common.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `reorder_tasks` | `data: TaskReorder`, `response: Response`, `service: Annotated[TaskService, Depends(get_task_service)]` | `status` | `response.headers[...]` | `MessageResponse(...)` |
| `service.reorder_tasks` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `current_command` | `db` | - | - | `...` |
| `getattr` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `info.get` | - | - | - | - |
| `str` | - | - | - | - |
| `MessageResponse` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| reorder_tasks | service.reorder_tasks | 660 | `service.reorder_tasks(data.task_ids, iteration_id=data.iteration_id, parent_id=data.parent_id, expected_revision=data.expected_revision)` |
| reorder_tasks | HTTPException | 667 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| reorder_tasks | str | 667 | `str(e)` |
| reorder_tasks | current_command | 669 | `current_command(service.db)` |
| current_command | getattr | 38 | `getattr(db, 'info', None)` |
| current_command | isinstance | 39 | `isinstance(info, dict)` |
| current_command | info.get | 39 | `info.get('command')` |
| reorder_tasks | str | 671 | `str(...)` |
| reorder_tasks | MessageResponse | 672 | `MessageResponse(message='Tasks reordered', success=True)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `reorder_tasks` | `service.reorder_tasks` | 660 |
| external_call | `reorder_tasks` | `HTTPException` | 667 |
| external_call | `current_command` | `getattr` | 38 |
| external_call | `current_command` | `isinstance` | 39 |
| unresolved_call | `current_command` | `info.get` | 39 |

## Behavior

This flow starts at `reorder_tasks` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
