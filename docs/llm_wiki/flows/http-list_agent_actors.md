# list_agent_actors

**Entry point:** `list_agent_actors` (`http`)
**Source:** [routers_agent](../modules/routers_agent.md)
**Modules touched:** [routers_agent](../modules/routers_agent.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_agent_actors
    participant p1 as service.list_actor_roster
    participant p2 as _handle_agent_error
    participant p3 as isinstance
    participant p4 as str
    participant p5 as HTTPException
    participant p6 as exc.detail
    p0-->>p1: service.list_actor_roster
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
    s1["1. list_agent_actors"]
    s2["2. service.list_actor_roster"]
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
    s1 -. "service.list_actor_roster(actor, include_disabled=include_disabled)" .-> s2
    s1 -->|"_handle_agent_error(exc, structured=True)"| s3
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
| `list_agent_actors` | `actor: Annotated[AgentActor, Depends(get_agent_admin_actor)]`, `service: Annotated[AgentWorkService, Depends(get_agent_work_service)]`, `include_disabled: Annotated[bool, Query()]` | - | - | `...` |
| `service.list_actor_roster` | - | - | - | - |
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
| list_agent_actors | service.list_actor_roster | 590 | `service.list_actor_roster(actor, include_disabled=include_disabled)` |
| list_agent_actors | _handle_agent_error | 595 | `_handle_agent_error(exc, structured=True)` |
| _handle_agent_error | isinstance | 252 | `isinstance(exc, AgentPermissionError)` |
| _handle_agent_error | str | 254 | `str(exc)` |
| _handle_agent_error | str | 256 | `str(exc)` |
| _handle_agent_error | HTTPException | 258 | `HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)` |
| _handle_agent_error | isinstance | 259 | `isinstance(exc, AgentRoutingConflictError)` |
| _handle_agent_error | HTTPException | 260 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _handle_agent_error | exc.detail | 260 | `exc.detail(data not statically known)` |
| _handle_agent_error | isinstance | 261 | `isinstance(exc, AgentTeamSetupConflictError)` |
| _handle_agent_error | HTTPException | 262 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `list_agent_actors` | `service.list_actor_roster` | 590 |
| external_call | `_handle_agent_error` | `isinstance` | 252 |
| external_call | `_handle_agent_error` | `HTTPException` | 258 |
| external_call | `_handle_agent_error` | `isinstance` | 259 |
| external_call | `_handle_agent_error` | `HTTPException` | 260 |
| unresolved_call | `_handle_agent_error` | `exc.detail` | 260 |
| external_call | `_handle_agent_error` | `isinstance` | 261 |
| external_call | `_handle_agent_error` | `HTTPException` | 262 |
| step_limit | `list_agent_actors` | `first 12 steps` | 0 |

## Behavior

This flow starts at `list_agent_actors` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
