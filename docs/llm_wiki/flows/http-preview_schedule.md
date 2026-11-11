# preview_schedule

**Entry point:** `preview_schedule` (`http`)
**Source:** [routers_agent_planning](../modules/routers_agent_planning.md)
**Modules touched:** [routers_agent_planning](../modules/routers_agent_planning.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as preview_schedule
    participant p1 as service.preview_schedule
    participant p2 as _handle_agent_error
    participant p3 as isinstance
    participant p4 as HTTPException
    participant p5 as str
    participant p6 as exc.detail
    p0-->>p1: service.preview_schedule(iteration_id, actor, command=command)
    p0->>p2: _handle_agent_error
    p2-->>p3: isinstance(exc, AgentPermissionError)
    p2-->>p4: HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(...))
    p2-->>p5: str(exc)
    p2-->>p3: isinstance(exc, AgentRoutingConflictError)
    p2-->>p4: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p2-->>p6: exc.detail
    p2-->>p3: isinstance(exc, TaskVersionConflictError)
    p2-->>p4: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p2-->>p6: exc.detail
    p2-->>p3: isinstance(exc, AgentConflictError)
    p2-->>p4: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(...))
    p2-->>p5: str(exc)
    p2-->>p3: isinstance(exc, TriageConflictError)
    p2-->>p4: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(...))
    p2-->>p5: str(exc)
    p2-->>p3: isinstance(exc, LookupError)
    p2-->>p4: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(...))
    p2-->>p5: str(exc)
    p2-->>p3: isinstance(exc, ValueError)
    p2-->>p4: HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))
    p2-->>p5: str(exc)
```

> Call sequence diagram shows 23 of 23 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 19 of 19 (0 omitted); unresolved 3 of 3 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 2; effect analysis evaluated: 1, partial: 1, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 2 source steps with known totals: observed: 18, emitted: 14, omitted: 4. Unavailable totals are excluded.

- Effect collector omitted observations before flow assembly; displayed effects are partial.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `preview_schedule` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `service.preview_schedule` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_handle_agent_error` | `available` | `partial` | `available` | `13` | `9` | `4` |
| `isinstance` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `exc.detail` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `exc.detail` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. preview_schedule"]
    s2["2. service.preview_schedule"]
    s3["3. _handle_agent_error"]
    s4["4. isinstance"]
    s5["5. HTTPException"]
    s6["6. str"]
    s7["7. isinstance"]
    s8["8. HTTPException"]
    s9["9. exc.detail"]
    s10["10. isinstance"]
    s11["11. HTTPException"]
    s12["12. exc.detail"]
    s1 -. "service.preview_schedule(iteration_id, actor, command=command)" .-> s2
    s1 -->|"_handle_agent_error(exc)"| s3
    s3 -. "isinstance(exc, AgentPermissionError)" .-> s4
    s3 -. "HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(...))" .-> s5
    s3 -. "str(exc)" .-> s6
    s3 -. "isinstance(exc, AgentRoutingConflictError)" .-> s7
    s3 -. "HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))" .-> s8
    s3 -. "exc.detail(data not statically known)" .-> s9
    s3 -. "isinstance(exc, TaskVersionConflictError)" .-> s10
    s3 -. "HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))" .-> s11
    s3 -. "exc.detail(data not statically known)" .-> s12
    click s1 "../modules/routers_agent_planning.md"
    click s3 "../modules/routers_agent_planning.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `preview_schedule` | `iteration_id: int`, `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `service: Annotated[AgentPlanningService, Depends(get_agent_planning_service)]`, `command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)]` | - | - | `...` |
| `service.preview_schedule` | - | - | - | - |
| `_handle_agent_error` | `exc: Exception` | `AgentPermissionError`, `status`, `AgentRoutingConflictError`, `status`, `TaskVersionConflictError`, `status`, `AgentConflictError`, `status` | - | - |
| `isinstance` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| preview_schedule | service.preview_schedule | 567 | `service.preview_schedule(iteration_id, actor, command=command)` |
| preview_schedule | _handle_agent_error | 573 | `_handle_agent_error(exc)` |
| _handle_agent_error | isinstance | 106 | `isinstance(exc, AgentPermissionError)` |
| _handle_agent_error | HTTPException | 107 | `HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(...))` |
| _handle_agent_error | str | 107 | `str(exc)` |
| _handle_agent_error | isinstance | 108 | `isinstance(exc, AgentRoutingConflictError)` |
| _handle_agent_error | HTTPException | 109 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _handle_agent_error | exc.detail | 109 | `exc.detail(data not statically known)` |
| _handle_agent_error | isinstance | 110 | `isinstance(exc, TaskVersionConflictError)` |
| _handle_agent_error | HTTPException | 111 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _handle_agent_error | exc.detail | 111 | `exc.detail(data not statically known)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `preview_schedule` | `service.preview_schedule` | 567 |
| external_call | `_handle_agent_error` | `isinstance` | 106 |
| external_call | `_handle_agent_error` | `HTTPException` | 107 |
| external_call | `_handle_agent_error` | `isinstance` | 108 |
| external_call | `_handle_agent_error` | `HTTPException` | 109 |
| unresolved_call | `_handle_agent_error` | `exc.detail` | 109 |
| external_call | `_handle_agent_error` | `isinstance` | 110 |
| external_call | `_handle_agent_error` | `HTTPException` | 111 |
| unresolved_call | `_handle_agent_error` | `exc.detail` | 111 |
| step_limit | `preview_schedule` | `first 12 steps` | 0 |

## Behavior

This flow starts at `preview_schedule` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
