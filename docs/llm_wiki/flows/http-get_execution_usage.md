# get_execution_usage

**Entry point:** `get_execution_usage` (`http`)
**Source:** [routers_agent](../modules/routers_agent.md)
**Modules touched:** [execution_usage_service](../modules/execution_usage_service.md), [routers_agent](../modules/routers_agent.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_execution_usage
    participant p1 as ExecutionUsageService(…).latest
    participant p2 as ExecutionUsageService
    participant p3 as _handle_agent_error
    participant p4 as isinstance
    participant p5 as str
    participant p6 as HTTPException
    participant p7 as exc.detail
    p0-->>p1: ExecutionUsageService(…).latest
    p0->>p2: ExecutionUsageService
    p0->>p3: _handle_agent_error
    p3-->>p4: isinstance
    p3-->>p5: str
    p3-->>p5: str
    p3-->>p6: HTTPException
    p3-->>p4: isinstance
    p3-->>p6: HTTPException
    p3-->>p7: exc.detail
    p3-->>p4: isinstance
    p3-->>p6: HTTPException
    p3-->>p7: exc.detail
    p3-->>p4: isinstance
    p3-->>p6: HTTPException
    p3-->>p7: exc.detail
    p3-->>p4: isinstance
    p3-->>p5: str
    p3-->>p5: str
    p3-->>p6: HTTPException
    p3-->>p4: isinstance
    p3-->>p5: str
    p3-->>p5: str
    p3-->>p6: HTTPException
    p3-->>p4: isinstance
    p3-->>p5: str
    p3-->>p5: str
    p3-->>p6: HTTPException
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_execution_usage"]
    s2["2. ExecutionUsageService(…).latest"]
    s3["3. ExecutionUsageService"]
    s4["4. _handle_agent_error"]
    s5["5. isinstance"]
    s6["6. str"]
    s7["7. str"]
    s8["8. HTTPException"]
    s9["9. isinstance"]
    s10["10. HTTPException"]
    s11["11. exc.detail"]
    s12["12. isinstance"]
    s1 -. "ExecutionUsageService(…).latest(actor, run_id)" .-> s2
    s1 -->|"ExecutionUsageService(db)"| s3
    s1 -->|"_handle_agent_error(exc, structured=True)"| s4
    s4 -. "isinstance(exc, AgentPermissionError)" .-> s5
    s4 -. "str(exc)" .-> s6
    s4 -. "str(exc)" .-> s7
    s4 -. "HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)" .-> s8
    s4 -. "isinstance(exc, AgentRoutingConflictError)" .-> s9
    s4 -. "HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))" .-> s10
    s4 -. "exc.detail(data not statically known)" .-> s11
    s4 -. "isinstance(exc, AgentTeamSetupConflictError)" .-> s12
    click s1 "../modules/routers_agent.md"
    click s3 "../modules/execution_usage_service.md"
    click s4 "../modules/routers_agent.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_execution_usage` | `run_id: int`, `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]` | - | - | `...` |
| `ExecutionUsageService(…).latest` | - | - | - | - |
| `ExecutionUsageService` | - | - | - | - |
| `_handle_agent_error` | `exc: Exception`, `structured: bool` | `AgentPermissionError`, `status`, `AgentRoutingConflictError`, `status`, `AgentTeamSetupConflictError`, `status`, `TaskVersionConflictError`, `status` | - | - |
| `isinstance` | - | - | - | - |
| `str` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `isinstance` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_execution_usage | ExecutionUsageService(…).latest | 1345 | `ExecutionUsageService(db).latest(actor, run_id)` |
| get_execution_usage | ExecutionUsageService | 1345 | `ExecutionUsageService(db)` |
| get_execution_usage | _handle_agent_error | 1347 | `_handle_agent_error(exc, structured=True)` |
| _handle_agent_error | isinstance | 254 | `isinstance(exc, AgentPermissionError)` |
| _handle_agent_error | str | 256 | `str(exc)` |
| _handle_agent_error | str | 258 | `str(exc)` |
| _handle_agent_error | HTTPException | 260 | `HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)` |
| _handle_agent_error | isinstance | 261 | `isinstance(exc, AgentRoutingConflictError)` |
| _handle_agent_error | HTTPException | 262 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _handle_agent_error | exc.detail | 262 | `exc.detail(data not statically known)` |
| _handle_agent_error | isinstance | 263 | `isinstance(exc, AgentTeamSetupConflictError)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_execution_usage` | `ExecutionUsageService(db).latest` | 1345 |
| external_call | `_handle_agent_error` | `isinstance` | 254 |
| external_call | `_handle_agent_error` | `HTTPException` | 260 |
| external_call | `_handle_agent_error` | `isinstance` | 261 |
| external_call | `_handle_agent_error` | `HTTPException` | 262 |
| unresolved_call | `_handle_agent_error` | `exc.detail` | 262 |
| external_call | `_handle_agent_error` | `isinstance` | 263 |
| step_limit | `get_execution_usage` | `first 12 steps` | 0 |

## Behavior

This flow starts at `get_execution_usage` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
