# create_agent_task

**Entry point:** `create_agent_task` (`http`)
**Source:** [routers_agent](../modules/routers_agent.md)
**Modules touched:** [routers_agent](../modules/routers_agent.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as create_agent_task
    participant p1 as service.create_task
    participant p2 as _handle_agent_error
    participant p3 as isinstance
    participant p4 as str
    participant p5 as HTTPException
    participant p6 as exc.detail
    p0-->>p1: service.create_task
    p0->>p2: _handle_agent_error
    p2-->>p3: isinstance
    p2-->>p4: str
    p2-->>p4: str
    p2-->>p5: HTTPException
    p2-->>p3: isinstance
    p2-->>p5: HTTPException
    p2-->>p6: exc.detail
    p2-->>p3: isinstance
    p2-->>p5: HTTPException
    p2-->>p6: exc.detail
    p2-->>p3: isinstance
    p2-->>p5: HTTPException
    p2-->>p6: exc.detail
    p2-->>p3: isinstance
    p2-->>p4: str
    p2-->>p4: str
    p2-->>p5: HTTPException
    p2-->>p3: isinstance
    p2-->>p4: str
    p2-->>p4: str
    p2-->>p5: HTTPException
    p2-->>p3: isinstance
    p2-->>p4: str
    p2-->>p4: str
    p2-->>p5: HTTPException
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. create_agent_task"]
    s2["2. service.create_task"]
    s3["3. _handle_agent_error"]
    s4["4. isinstance"]
    s5["5. str"]
    s6["6. str"]
    s7["7. HTTPException"]
    s8["8. isinstance"]
    s9["9. HTTPException"]
    s10["10. exc.detail"]
    s11["11. isinstance"]
    s12["12. HTTPException"]
    s1 -. "service.create_task(iteration_id, actor, data, idempotency_key)" .-> s2
    s1 -->|"_handle_agent_error(exc)"| s3
    s3 -. "isinstance(exc, AgentPermissionError)" .-> s4
    s3 -. "str(exc)" .-> s5
    s3 -. "str(exc)" .-> s6
    s3 -. "HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)" .-> s7
    s3 -. "isinstance(exc, AgentRoutingConflictError)" .-> s8
    s3 -. "HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))" .-> s9
    s3 -. "exc.detail(data not statically known)" .-> s10
    s3 -. "isinstance(exc, AgentTeamSetupConflictError)" .-> s11
    s3 -. "HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))" .-> s12
    click s1 "../modules/routers_agent.md"
    click s3 "../modules/routers_agent.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `create_agent_task` | `iteration_id: int`, `data: AgentTaskCreate`, `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `service: Annotated[AgentService, Depends(get_agent_service)]`, `idempotency_key: Annotated[Optional[str], Header(alias='Idempotency-Key')]` | - | - | `task` |
| `service.create_task` | - | - | - | - |
| `_handle_agent_error` | `exc: Exception`, `structured: bool` | `AgentPermissionError`, `status`, `AgentRoutingConflictError`, `status`, `AgentTeamSetupConflictError`, `status`, `TaskVersionConflictError`, `status` | - | - |
| `isinstance` | - | - | - | - |
| `str` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `HTTPException` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| create_agent_task | service.create_task | 1117 | `service.create_task(iteration_id, actor, data, idempotency_key)` |
| create_agent_task | _handle_agent_error | 1119 | `_handle_agent_error(exc)` |
| _handle_agent_error | isinstance | 254 | `isinstance(exc, AgentPermissionError)` |
| _handle_agent_error | str | 256 | `str(exc)` |
| _handle_agent_error | str | 258 | `str(exc)` |
| _handle_agent_error | HTTPException | 260 | `HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)` |
| _handle_agent_error | isinstance | 261 | `isinstance(exc, AgentRoutingConflictError)` |
| _handle_agent_error | HTTPException | 262 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _handle_agent_error | exc.detail | 262 | `exc.detail(data not statically known)` |
| _handle_agent_error | isinstance | 263 | `isinstance(exc, AgentTeamSetupConflictError)` |
| _handle_agent_error | HTTPException | 264 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `create_agent_task` | `service.create_task` | 1117 |
| external_call | `_handle_agent_error` | `isinstance` | 254 |
| external_call | `_handle_agent_error` | `HTTPException` | 260 |
| external_call | `_handle_agent_error` | `isinstance` | 261 |
| external_call | `_handle_agent_error` | `HTTPException` | 262 |
| unresolved_call | `_handle_agent_error` | `exc.detail` | 262 |
| external_call | `_handle_agent_error` | `isinstance` | 263 |
| external_call | `_handle_agent_error` | `HTTPException` | 264 |
| step_limit | `create_agent_task` | `first 12 steps` | 0 |

## Behavior

This flow starts at `create_agent_task` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
