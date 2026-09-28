# release_task_claim

**Entry point:** `release_task_claim` (`http`)
**Source:** [routers_agent](../modules/routers_agent.md)
**Modules touched:** [routers_agent](../modules/routers_agent.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as release_task_claim
    participant p1 as service.release_claim
    participant p2 as _handle_agent_error
    participant p3 as isinstance
    participant p4 as str
    participant p5 as HTTPException (backend/app/routers/agent.py:_handle_agent_error)
    participant p6 as exc.detail
    participant p7 as HTTPException (backend/app/routers/agent.py:release_task_claim)
    participant p8 as service.task_service.task_to_response
    p0-->>p1: service.release_claim
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
    p0-->>p7: HTTPException (backend/app/routers/agent.py:release_task_claim)
    p0-->>p8: service.task_service.task_to_response
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. release_task_claim"]
    s2["2. service.release_claim"]
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
    s1 -. "service.release_claim(task_id, actor, idempotency_key)" .-> s2
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
| `release_task_claim` | `task_id: int`, `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `service: Annotated[AgentService, Depends(get_agent_service)]`, `idempotency_key: Annotated[Optional[str], Header(alias='Idempotency-Key')]` | `status` | - | `service.task_service.task_to_response(...)` |
| `service.release_claim` | - | - | - | - |
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
| release_task_claim | service.release_claim | 1093 | `service.release_claim(task_id, actor, idempotency_key)` |
| release_task_claim | _handle_agent_error | 1095 | `_handle_agent_error(exc)` |
| _handle_agent_error | isinstance | 252 | `isinstance(exc, AgentPermissionError)` |
| _handle_agent_error | str | 254 | `str(exc)` |
| _handle_agent_error | str | 256 | `str(exc)` |
| _handle_agent_error | HTTPException (backend/app/routers/agent.py:_handle_agent_error) | 258 | `HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)` |
| _handle_agent_error | isinstance | 259 | `isinstance(exc, AgentRoutingConflictError)` |
| _handle_agent_error | HTTPException (backend/app/routers/agent.py:_handle_agent_error) | 260 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _handle_agent_error | exc.detail | 260 | `exc.detail(data not statically known)` |
| _handle_agent_error | isinstance | 261 | `isinstance(exc, AgentTeamSetupConflictError)` |
| _handle_agent_error | HTTPException (backend/app/routers/agent.py:_handle_agent_error) | 262 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `release_task_claim` | `service.release_claim` | 1093 |
| external_call | `_handle_agent_error` | `isinstance` | 252 |
| external_call | `_handle_agent_error` | `HTTPException` | 258 |
| external_call | `_handle_agent_error` | `isinstance` | 259 |
| external_call | `_handle_agent_error` | `HTTPException` | 260 |
| unresolved_call | `_handle_agent_error` | `exc.detail` | 260 |
| external_call | `_handle_agent_error` | `isinstance` | 261 |
| external_call | `_handle_agent_error` | `HTTPException` | 262 |
| step_limit | `release_task_claim` | `first 12 steps` | 0 |

## Behavior

This flow starts at `release_task_claim` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
