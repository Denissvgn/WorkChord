# patch_agent_task

**Entry point:** `patch_agent_task` (`http`)
**Source:** [routers_agent](../modules/routers_agent.md)
**Modules touched:** [routers_agent](../modules/routers_agent.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as patch_agent_task
    participant p1 as service.patch_task
    participant p2 as _handle_agent_error
    participant p3 as isinstance
    participant p4 as str
    participant p5 as HTTPException (backend/app/routers/agent.py:_handle_agent_error)
    participant p6 as exc.detail
    participant p7 as HTTPException (backend/app/routers/agent.py:patch_agent_task)
    p0-->>p1: service.patch_task
    p0->>p2: _handle_agent_error
    p2-->>p3: isinstance
    p2-->>p4: str
    p2-->>p4: str
    p2-->>p5: HTTPException (backend/app/routers/agent.py:_handle_agent_error)
    p2-->>p3: isinstance
    p2-->>p5: HTTPException (backend/app/routers/agent.py:_handle_agent_error)
    p2-->>p6: exc.detail
    p2-->>p3: isinstance
    p2-->>p5: HTTPException (backend/app/routers/agent.py:_handle_agent_error)
    p2-->>p6: exc.detail
    p2-->>p3: isinstance
    p2-->>p5: HTTPException (backend/app/routers/agent.py:_handle_agent_error)
    p2-->>p6: exc.detail
    p2-->>p3: isinstance
    p2-->>p4: str
    p2-->>p4: str
    p2-->>p5: HTTPException (backend/app/routers/agent.py:_handle_agent_error)
    p2-->>p3: isinstance
    p2-->>p4: str
    p2-->>p4: str
    p2-->>p5: HTTPException (backend/app/routers/agent.py:_handle_agent_error)
    p2-->>p3: isinstance
    p2-->>p4: str
    p2-->>p4: str
    p2-->>p5: HTTPException (backend/app/routers/agent.py:_handle_agent_error)
    p0-->>p7: HTTPException (backend/app/routers/agent.py:patch_agent_task)
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. patch_agent_task"]
    s2["2. service.patch_task"]
    s3["3. _handle_agent_error"]
    s4["4. isinstance"]
    s5["5. str"]
    s6["6. str"]
    s7["7. HTTPException (backend/app/routers/agent.py:_handle_agent_error)"]
    s8["8. isinstance"]
    s9["9. HTTPException (backend/app/routers/agent.py:_handle_agent_error)"]
    s10["10. exc.detail"]
    s11["11. isinstance"]
    s12["12. HTTPException (backend/app/routers/agent.py:_handle_agent_error)"]
    s1 -. "service.patch_task(task_id, actor, data, idempotency_key)" .-> s2
    s1 -->|"_handle_agent_error(exc)"| s3
    s3 -. "isinstance(exc, AgentPermissionError)" .-> s4
    s3 -. "str(exc)" .-> s5
    s3 -. "str(exc)" .-> s6
    s3 -. "HTTPException (backend/app/routers/agent.py:_handle_agent_error)(status_code=status.HTTP_403_FORBIDDEN, detail=detail)" .-> s7
    s3 -. "isinstance(exc, AgentRoutingConflictError)" .-> s8
    s3 -. "HTTPException (backend/app/routers/agent.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))" .-> s9
    s3 -. "exc.detail(data not statically known)" .-> s10
    s3 -. "isinstance(exc, AgentTeamSetupConflictError)" .-> s11
    s3 -. "HTTPException (backend/app/routers/agent.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))" .-> s12
    click s1 "../modules/routers_agent.md"
    click s3 "../modules/routers_agent.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `patch_agent_task` | `task_id: int`, `data: AgentTaskPatch`, `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `service: Annotated[AgentService, Depends(get_agent_service)]`, `idempotency_key: Annotated[Optional[str], Header(alias='Idempotency-Key')]` | `status` | - | `task` |
| `service.patch_task` | - | - | - | - |
| `_handle_agent_error` | `exc: Exception`, `structured: bool` | `AgentPermissionError`, `status`, `AgentRoutingConflictError`, `status`, `AgentTeamSetupConflictError`, `status`, `TaskVersionConflictError`, `status` | - | - |
| `isinstance` | - | - | - | - |
| `str` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException (backend/app/routers/agent.py:_handle_agent_error)` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `HTTPException (backend/app/routers/agent.py:_handle_agent_error)` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `HTTPException (backend/app/routers/agent.py:_handle_agent_error)` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| patch_agent_task | service.patch_task | 1133 | `service.patch_task(task_id, actor, data, idempotency_key)` |
| patch_agent_task | _handle_agent_error | 1135 | `_handle_agent_error(exc)` |
| _handle_agent_error | isinstance | 254 | `isinstance(exc, AgentPermissionError)` |
| _handle_agent_error | str | 256 | `str(exc)` |
| _handle_agent_error | str | 258 | `str(exc)` |
| _handle_agent_error | HTTPException (backend/app/routers/agent.py:_handle_agent_error) | 260 | `HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)` |
| _handle_agent_error | isinstance | 261 | `isinstance(exc, AgentRoutingConflictError)` |
| _handle_agent_error | HTTPException (backend/app/routers/agent.py:_handle_agent_error) | 262 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _handle_agent_error | exc.detail | 262 | `exc.detail(data not statically known)` |
| _handle_agent_error | isinstance | 263 | `isinstance(exc, AgentTeamSetupConflictError)` |
| _handle_agent_error | HTTPException (backend/app/routers/agent.py:_handle_agent_error) | 264 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `patch_agent_task` | `service.patch_task` | 1133 |
| external_call | `_handle_agent_error` | `isinstance` | 254 |
| external_call | `_handle_agent_error` | `HTTPException` | 260 |
| external_call | `_handle_agent_error` | `isinstance` | 261 |
| external_call | `_handle_agent_error` | `HTTPException` | 262 |
| unresolved_call | `_handle_agent_error` | `exc.detail` | 262 |
| external_call | `_handle_agent_error` | `isinstance` | 263 |
| external_call | `_handle_agent_error` | `HTTPException` | 264 |
| step_limit | `patch_agent_task` | `first 12 steps` | 0 |

## Behavior

This flow starts at `patch_agent_task` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
