# get_my_agent_work

**Entry point:** `get_my_agent_work` (`http`)
**Source:** [routers_agent](../modules/routers_agent.md)
**Modules touched:** [routers_agent](../modules/routers_agent.md), [time](../modules/time.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_my_agent_work
    participant p1 as service.get_work
    participant p2 as _handle_agent_error
    participant p3 as isinstance
    participant p4 as str (backend/app/routers/agent.py:_handle_agent_error)
    participant p5 as HTTPException
    participant p6 as exc.detail
    participant p7 as service.work_etag
    participant p8 as max
    participant p9 as int
    p0-->>p1: service.get_work
    p0->>p2: _handle_agent_error
    p2-->>p3: isinstance
    p2-->>p4: str (backend/app/routers/agent.py:_handle_agent_error)
    p2-->>p4: str (backend/app/routers/agent.py:_handle_agent_error)
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
    p2-->>p4: str (backend/app/routers/agent.py:_handle_agent_error)
    p2-->>p4: str (backend/app/routers/agent.py:_handle_agent_error)
    p2-->>p5: HTTPException
    p2-->>p3: isinstance
    p2-->>p4: str (backend/app/routers/agent.py:_handle_agent_error)
    p2-->>p4: str (backend/app/routers/agent.py:_handle_agent_error)
    p2-->>p5: HTTPException
    p2-->>p3: isinstance
    p2-->>p4: str (backend/app/routers/agent.py:_handle_agent_error)
    p2-->>p4: str (backend/app/routers/agent.py:_handle_agent_error)
    p2-->>p5: HTTPException
    p0-->>p7: service.work_etag
    p0-->>p8: max
    p0-->>p9: int
```

> Call sequence diagram shows 30 of 42 interactions; 12 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_my_agent_work"]
    s2["2. service.get_work"]
    s3["3. _handle_agent_error"]
    s4["4. isinstance"]
    s5["5. str (backend/app/routers/agent.py:_handle_agent_error)"]
    s6["6. str (backend/app/routers/agent.py:_handle_agent_error)"]
    s7["7. HTTPException"]
    s8["8. isinstance"]
    s9["9. HTTPException"]
    s10["10. exc.detail"]
    s11["11. isinstance"]
    s12["12. HTTPException"]
    s1 -. "service.get_work(actor, limit=limit, cursor=cursor)" .-> s2
    s1 -->|"_handle_agent_error(exc, structured=True)"| s3
    s3 -. "isinstance(exc, AgentPermissionError)" .-> s4
    s3 -. "str (backend/app/routers/agent.py:_handle_agent_error)(exc)" .-> s5
    s3 -. "str (backend/app/routers/agent.py:_handle_agent_error)(exc)" .-> s6
    s3 -. "HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)" .-> s7
    s3 -. "isinstance(exc, AgentRoutingConflictError)" .-> s8
    s3 -. "HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))" .-> s9
    s3 -. "exc.detail(data not statically known)" .-> s10
    s3 -. "isinstance(exc, AgentTeamSetupConflictError)" .-> s11
    s3 -. "HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))" .-> s12
    b0["mutation response.headers.update"]
    s1 -. "mutation response.headers.update" .-> b0
    click s1 "../modules/routers_agent.md"
    click s3 "../modules/routers_agent.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_my_agent_work` | `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `service: Annotated[AgentWorkService, Depends(get_agent_work_service)]`, `response: Response`, `limit: int`, `cursor: Optional[str]`, `if_none_match: Annotated[Optional[str], Header(alias='If-None-Match')]` | `status` | `cache_headers[...]` | `Response(...)`, `decision` |
| `service.get_work` | - | - | - | - |
| `_handle_agent_error` | `exc: Exception`, `structured: bool` | `AgentPermissionError`, `status`, `AgentRoutingConflictError`, `status`, `AgentTeamSetupConflictError`, `status`, `TaskVersionConflictError`, `status` | - | - |
| `isinstance` | - | - | - | - |
| `str (backend/app/routers/agent.py:_handle_agent_error)` | - | - | - | - |
| `str (backend/app/routers/agent.py:_handle_agent_error)` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `HTTPException` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_my_agent_work | service.get_work | 777 | `service.get_work(actor, limit=limit, cursor=cursor)` |
| get_my_agent_work | _handle_agent_error | 779 | `_handle_agent_error(exc, structured=True)` |
| _handle_agent_error | isinstance | 252 | `isinstance(exc, AgentPermissionError)` |
| _handle_agent_error | str (backend/app/routers/agent.py:_handle_agent_error) | 254 | `str(exc)` |
| _handle_agent_error | str (backend/app/routers/agent.py:_handle_agent_error) | 256 | `str(exc)` |
| _handle_agent_error | HTTPException | 258 | `HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)` |
| _handle_agent_error | isinstance | 259 | `isinstance(exc, AgentRoutingConflictError)` |
| _handle_agent_error | HTTPException | 260 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _handle_agent_error | exc.detail | 260 | `exc.detail(data not statically known)` |
| _handle_agent_error | isinstance | 261 | `isinstance(exc, AgentTeamSetupConflictError)` |
| _handle_agent_error | HTTPException | 262 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `response.headers.update` | `get_my_agent_work` | 794 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_my_agent_work` | `service.get_work` | 777 |
| external_call | `_handle_agent_error` | `isinstance` | 252 |
| external_call | `_handle_agent_error` | `HTTPException` | 258 |
| external_call | `_handle_agent_error` | `isinstance` | 259 |
| external_call | `_handle_agent_error` | `HTTPException` | 260 |
| unresolved_call | `_handle_agent_error` | `exc.detail` | 260 |
| external_call | `_handle_agent_error` | `isinstance` | 261 |
| external_call | `_handle_agent_error` | `HTTPException` | 262 |
| step_limit | `get_my_agent_work` | `first 12 steps` | 0 |

## Behavior

This flow starts at `get_my_agent_work` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
