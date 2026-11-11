# append_agent_run_event

**Entry point:** `append_agent_run_event` (`http`)
**Source:** [routers_agent](../modules/routers_agent.md)
**Modules touched:** [routers_agent](../modules/routers_agent.md), [schemas_agent](../modules/schemas_agent.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as append_agent_run_event
    participant p1 as service.append_run_event
    participant p2 as _handle_agent_error
    participant p3 as HTTPException (backend/app/routers/agent.py:append_agent_run_event)
    participant p4 as AgentRunEventResponse
    participant p5 as service.event_to_payload
    participant p6 as isinstance
    participant p7 as str
    participant p8 as HTTPException (backend/app/routers/agent.py:_handle_agent_error)
    participant p9 as exc.detail
    p0-->>p1: service.append_run_event(run_id, actor, data)
    p0->>p2: _handle_agent_error
    p0-->>p3: HTTPException (backend/app/routers/agent.py:append_agent_run_event)(status_code=status.HTTP_404_NOT_FOUND, detail='Run not found')
    p0->>p4: AgentRunEventResponse
    p0-->>p5: service.event_to_payload(event.payload)
    p2-->>p6: isinstance(exc, AgentPermissionError)
    p2-->>p7: str(exc)
    p2-->>p7: str(exc)
    p2-->>p8: HTTPException (backend/app/routers/agent.py:_handle_agent_error)(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
    p2-->>p6: isinstance(exc, AgentRoutingConflictError)
    p2-->>p8: HTTPException (backend/app/routers/agent.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p2-->>p9: exc.detail
    p2-->>p6: isinstance(exc, AgentTeamSetupConflictError)
    p2-->>p8: HTTPException (backend/app/routers/agent.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p2-->>p9: exc.detail
    p2-->>p6: isinstance(exc, TaskVersionConflictError)
    p2-->>p8: HTTPException (backend/app/routers/agent.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p2-->>p9: exc.detail
    p2-->>p6: isinstance(exc, AgentConflictError)
    p2-->>p7: str(exc)
    p2-->>p7: str(exc)
    p2-->>p8: HTTPException (backend/app/routers/agent.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=detail)
    p2-->>p6: isinstance(exc, LookupError)
    p2-->>p7: str(exc)
    p2-->>p7: str(exc)
    p2-->>p8: HTTPException (backend/app/routers/agent.py:_handle_agent_error)(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    p2-->>p6: isinstance(exc, ValueError)
    p2-->>p7: str(exc)
    p2-->>p7: str(exc)
    p2-->>p8: HTTPException (backend/app/routers/agent.py:_handle_agent_error)(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
```

> Call sequence diagram shows 30 of 30 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 23 of 23 (0 omitted); unresolved 5 of 5 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 3; effect analysis evaluated: 1, partial: 1, unavailable: 1. Counts include steps omitted from the displayed trace.

Collector observations for 2 source steps with known totals: observed: 20, emitted: 16, omitted: 4. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `append_agent_run_event` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `service.append_run_event` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_handle_agent_error` | `available` | `partial` | `available` | `14` | `10` | `4` |
| `isinstance` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/agent.py:_handle_agent_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/agent.py:_handle_agent_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `exc.detail` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/agent.py:_handle_agent_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. append_agent_run_event"]
    s2["2. service.append_run_event"]
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
    s1 -. "service.append_run_event(run_id, actor, data)" .-> s2
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
| `append_agent_run_event` | `run_id: int`, `data: AgentRunEventCreate`, `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `service: Annotated[AgentService, Depends(get_agent_service)]` | `status` | - | `AgentRunEventResponse(...)` |
| `service.append_run_event` | - | - | - | - |
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
| append_agent_run_event | service.append_run_event | 1216 | `service.append_run_event(run_id, actor, data)` |
| append_agent_run_event | _handle_agent_error | 1218 | `_handle_agent_error(exc)` |
| _handle_agent_error | isinstance | 271 | `isinstance(exc, AgentPermissionError)` |
| _handle_agent_error | str | 273 | `str(exc)` |
| _handle_agent_error | str | 275 | `str(exc)` |
| _handle_agent_error | HTTPException (backend/app/routers/agent.py:_handle_agent_error) | 277 | `HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)` |
| _handle_agent_error | isinstance | 278 | `isinstance(exc, AgentRoutingConflictError)` |
| _handle_agent_error | HTTPException (backend/app/routers/agent.py:_handle_agent_error) | 279 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _handle_agent_error | exc.detail | 279 | `exc.detail(data not statically known)` |
| _handle_agent_error | isinstance | 280 | `isinstance(exc, AgentTeamSetupConflictError)` |
| _handle_agent_error | HTTPException (backend/app/routers/agent.py:_handle_agent_error) | 281 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `append_agent_run_event` | `service.append_run_event` | 1216 |
| external_call | `_handle_agent_error` | `isinstance` | 271 |
| external_call | `_handle_agent_error` | `HTTPException` | 277 |
| external_call | `_handle_agent_error` | `isinstance` | 278 |
| external_call | `_handle_agent_error` | `HTTPException` | 279 |
| unresolved_call | `_handle_agent_error` | `exc.detail` | 279 |
| external_call | `_handle_agent_error` | `isinstance` | 280 |
| external_call | `_handle_agent_error` | `HTTPException` | 281 |
| step_limit | `append_agent_run_event` | `first 12 steps` | 0 |

## Behavior

This flow starts at `append_agent_run_event` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
