# acknowledge_agent_team_runtime

**Entry point:** `acknowledge_agent_team_runtime` (`http`)
**Source:** [routers_agent](../modules/routers_agent.md)
**Modules touched:** [routers_agent](../modules/routers_agent.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as acknowledge_agent_team_runtime
    participant p1 as HTTPException (backend/app/routers/agent…owledge_agent_team_runtime)
    participant p2 as service.acknowledge_runtime
    participant p3 as _handle_agent_error
    participant p4 as isinstance
    participant p5 as str
    participant p6 as HTTPException (backend/app/routers/agent.py:_handle_agent_error)
    participant p7 as exc.detail
    p0-->>p1: HTTPException (backend/app/routers/agent…owledge_agent_team_runtime)(status_code=status.HTTP_401_UNAUTHORIZED, detail='Missing X-Agent-API-Key header')
    p0-->>p2: service.acknowledge_runtime(api_key, data)
    p0->>p3: _handle_agent_error
    p3-->>p4: isinstance(exc, AgentPermissionError)
    p3-->>p5: str(exc)
    p3-->>p5: str(exc)
    p3-->>p6: HTTPException (backend/app/routers/agent.py:_handle_agent_error)(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
    p3-->>p4: isinstance(exc, AgentRoutingConflictError)
    p3-->>p6: HTTPException (backend/app/routers/agent.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p3-->>p7: exc.detail
    p3-->>p4: isinstance(exc, AgentTeamSetupConflictError)
    p3-->>p6: HTTPException (backend/app/routers/agent.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p3-->>p7: exc.detail
    p3-->>p4: isinstance(exc, TaskVersionConflictError)
    p3-->>p6: HTTPException (backend/app/routers/agent.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p3-->>p7: exc.detail
    p3-->>p4: isinstance(exc, AgentConflictError)
    p3-->>p5: str(exc)
    p3-->>p5: str(exc)
    p3-->>p6: HTTPException (backend/app/routers/agent.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=detail)
    p3-->>p4: isinstance(exc, LookupError)
    p3-->>p5: str(exc)
    p3-->>p5: str(exc)
    p3-->>p6: HTTPException (backend/app/routers/agent.py:_handle_agent_error)(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    p3-->>p4: isinstance(exc, ValueError)
    p3-->>p5: str(exc)
    p3-->>p5: str(exc)
    p3-->>p6: HTTPException (backend/app/routers/agent.py:_handle_agent_error)(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
```

> Call sequence diagram shows 28 of 28 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 23 of 23 (0 omitted); unresolved 4 of 4 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 2; effect analysis evaluated: 1, partial: 1, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 2 source steps with known totals: observed: 22, emitted: 18, omitted: 4. Unavailable totals are excluded.

- Effect collector omitted observations before flow assembly; displayed effects are partial.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `acknowledge_agent_team_runtime` | `available` | `evaluated` | `available` | `8` | `8` | `0` |
| `HTTPException (backend/app/routers/agent…owledge_agent_team_runtime)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `service.acknowledge_runtime` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_handle_agent_error` | `available` | `partial` | `available` | `14` | `10` | `4` |
| `isinstance` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/agent.py:_handle_agent_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/agent.py:_handle_agent_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `exc.detail` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. acknowledge_agent_team_runtime"]
    s2["2. HTTPException (backend/app/routers/agent…owledge_agent_team_runtime)"]
    s3["3. service.acknowledge_runtime"]
    s4["4. _handle_agent_error"]
    s5["5. isinstance"]
    s6["6. str"]
    s7["7. str"]
    s8["8. HTTPException (backend/app/routers/agent.py:_handle_agent_error)"]
    s9["9. isinstance"]
    s10["10. HTTPException (backend/app/routers/agent.py:_handle_agent_error)"]
    s11["11. exc.detail"]
    s12["12. isinstance"]
    s1 -. "HTTPException (backend/app/routers/agent…owledge_agent_team_runtime)(status_code=status.HTTP_401_UNAUTHORIZED, detail='Missing X-Agent-API-Key header')" .-> s2
    s1 -. "service.acknowledge_runtime(api_key, data)" .-> s3
    s1 -->|"_handle_agent_error(exc, structured=True)"| s4
    s4 -. "isinstance(exc, AgentPermissionError)" .-> s5
    s4 -. "str(exc)" .-> s6
    s4 -. "str(exc)" .-> s7
    s4 -. "HTTPException (backend/app/routers/agent.py:_handle_agent_error)(status_code=status.HTTP_403_FORBIDDEN, detail=detail)" .-> s8
    s4 -. "isinstance(exc, AgentRoutingConflictError)" .-> s9
    s4 -. "HTTPException (backend/app/routers/agent.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))" .-> s10
    s4 -. "exc.detail(data not statically known)" .-> s11
    s4 -. "isinstance(exc, AgentTeamSetupConflictError)" .-> s12
    click s1 "../modules/routers_agent.md"
    click s4 "../modules/routers_agent.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `acknowledge_agent_team_runtime` | `data: AgentTeamRuntimeAcknowledgement`, `response: Response`, `service: Annotated[AgentTeamSetupService, Depends(get_agent_team_setup_service)]`, `api_key: Annotated[Optional[str], Header(alias='X-Agent-API-Key')]` | `status` | `response.headers[...]`, `response.headers[...]` | `result` |
| `HTTPException (backend/app/routers/agent…owledge_agent_team_runtime)` | - | - | - | - |
| `service.acknowledge_runtime` | - | - | - | - |
| `_handle_agent_error` | `exc: Exception`, `structured: bool` | `AgentPermissionError`, `status`, `AgentRoutingConflictError`, `status`, `AgentTeamSetupConflictError`, `status`, `TaskVersionConflictError`, `status` | - | - |
| `isinstance` | - | - | - | - |
| `str` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException (backend/app/routers/agent.py:_handle_agent_error)` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `HTTPException (backend/app/routers/agent.py:_handle_agent_error)` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `isinstance` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| acknowledge_agent_team_runtime | HTTPException (backend/app/routers/agent…owledge_agent_team_runtime) | 549 | `HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Missing X-Agent-API-Key header')` |
| acknowledge_agent_team_runtime | service.acknowledge_runtime | 554 | `service.acknowledge_runtime(api_key, data)` |
| acknowledge_agent_team_runtime | _handle_agent_error | 556 | `_handle_agent_error(exc, structured=True)` |
| _handle_agent_error | isinstance | 271 | `isinstance(exc, AgentPermissionError)` |
| _handle_agent_error | str | 273 | `str(exc)` |
| _handle_agent_error | str | 275 | `str(exc)` |
| _handle_agent_error | HTTPException (backend/app/routers/agent.py:_handle_agent_error) | 277 | `HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)` |
| _handle_agent_error | isinstance | 278 | `isinstance(exc, AgentRoutingConflictError)` |
| _handle_agent_error | HTTPException (backend/app/routers/agent.py:_handle_agent_error) | 279 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _handle_agent_error | exc.detail | 279 | `exc.detail(data not statically known)` |
| _handle_agent_error | isinstance | 280 | `isinstance(exc, AgentTeamSetupConflictError)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `acknowledge_agent_team_runtime` | `HTTPException` | 549 |
| unresolved_call | `acknowledge_agent_team_runtime` | `service.acknowledge_runtime` | 554 |
| external_call | `_handle_agent_error` | `isinstance` | 271 |
| external_call | `_handle_agent_error` | `HTTPException` | 277 |
| external_call | `_handle_agent_error` | `isinstance` | 278 |
| external_call | `_handle_agent_error` | `HTTPException` | 279 |
| unresolved_call | `_handle_agent_error` | `exc.detail` | 279 |
| external_call | `_handle_agent_error` | `isinstance` | 280 |
| step_limit | `acknowledge_agent_team_runtime` | `first 12 steps` | 0 |

## Behavior

This flow starts at `acknowledge_agent_team_runtime` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
