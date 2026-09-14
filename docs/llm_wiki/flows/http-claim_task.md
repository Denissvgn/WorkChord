# claim_task

**Entry point:** `claim_task` (`http`)
**Source:** [routers_agent](../modules/routers_agent.md)
**Modules touched:** [routers_agent](../modules/routers_agent.md), [schemas_agent](../modules/schemas_agent.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as claim_task
    participant p1 as service.claim_task
    participant p2 as _handle_agent_error
    participant p3 as isinstance
    participant p4 as str
    participant p5 as HTTPException (backend/app/routers/agent.py:_handle_agent_error)
    participant p6 as exc.detail
    participant p7 as HTTPException (backend/app/routers/agent.py:claim_task)
    participant p8 as _claim_response
    participant p9 as HTTPException (backend/app/routers/agent.py:_claim_response)
    p0-->>p1: service.claim_task
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
    p0-->>p7: HTTPException (backend/app/routers/agent.py:claim_task)
    p0->>p8: _claim_response
    p8-->>p9: HTTPException (backend/app/routers/agent.py:_claim_response)
```

> Call sequence diagram shows 30 of 32 interactions; 2 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. claim_task"]
    s2["2. service.claim_task"]
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
    s1 -. "service.claim_task(task_id, actor, data, idempotency_key)" .-> s2
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
| `claim_task` | `task_id: int`, `data: TaskClaimRequest`, `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `service: Annotated[AgentService, Depends(get_agent_service)]`, `idempotency_key: Annotated[Optional[str], Header(alias='Idempotency-Key')]` | `status` | - | `_claim_response(...)` |
| `service.claim_task` | - | - | - | - |
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
| claim_task | service.claim_task | 1048 | `service.claim_task(task_id, actor, data, idempotency_key)` |
| claim_task | _handle_agent_error | 1050 | `_handle_agent_error(exc)` |
| _handle_agent_error | isinstance | 244 | `isinstance(exc, AgentPermissionError)` |
| _handle_agent_error | str | 246 | `str(exc)` |
| _handle_agent_error | str | 248 | `str(exc)` |
| _handle_agent_error | HTTPException (backend/app/routers/agent.py:_handle_agent_error) | 250 | `HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)` |
| _handle_agent_error | isinstance | 251 | `isinstance(exc, AgentRoutingConflictError)` |
| _handle_agent_error | HTTPException (backend/app/routers/agent.py:_handle_agent_error) | 252 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _handle_agent_error | exc.detail | 252 | `exc.detail(data not statically known)` |
| _handle_agent_error | isinstance | 253 | `isinstance(exc, AgentTeamSetupConflictError)` |
| _handle_agent_error | HTTPException (backend/app/routers/agent.py:_handle_agent_error) | 254 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `claim_task` | `service.claim_task` | 1048 |
| external_call | `_handle_agent_error` | `isinstance` | 244 |
| external_call | `_handle_agent_error` | `HTTPException` | 250 |
| external_call | `_handle_agent_error` | `isinstance` | 251 |
| external_call | `_handle_agent_error` | `HTTPException` | 252 |
| unresolved_call | `_handle_agent_error` | `exc.detail` | 252 |
| external_call | `_handle_agent_error` | `isinstance` | 253 |
| external_call | `_handle_agent_error` | `HTTPException` | 254 |
| step_limit | `claim_task` | `first 12 steps` | 0 |

## Behavior

This flow starts at `claim_task` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
