# list_ready_tasks

**Entry point:** `list_ready_tasks` (`http`)
**Source:** [routers_agent](../modules/routers_agent.md)
**Modules touched:** [routers_agent](../modules/routers_agent.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_ready_tasks
    participant p1 as service.list_ready_tasks
    participant p2 as _handle_agent_error
    participant p3 as service.task_service.task_to_response
    participant p4 as isinstance
    participant p5 as str
    participant p6 as HTTPException
    participant p7 as exc.detail
    p0-->>p1: service.list_ready_tasks(…)
    p0->>p2: _handle_agent_error
    p0-->>p3: service.task_service.task_to_response(task)
    p2-->>p4: isinstance(exc, AgentPermissionError)
    p2-->>p5: str(exc)
    p2-->>p5: str(exc)
    p2-->>p6: HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
    p2-->>p4: isinstance(exc, AgentRoutingConflictError)
    p2-->>p6: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p2-->>p7: exc.detail
    p2-->>p4: isinstance(exc, AgentTeamSetupConflictError)
    p2-->>p6: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p2-->>p7: exc.detail
    p2-->>p4: isinstance(exc, TaskVersionConflictError)
    p2-->>p6: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p2-->>p7: exc.detail
    p2-->>p4: isinstance(exc, AgentConflictError)
    p2-->>p5: str(exc)
    p2-->>p5: str(exc)
    p2-->>p6: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)
    p2-->>p4: isinstance(exc, LookupError)
    p2-->>p5: str(exc)
    p2-->>p5: str(exc)
    p2-->>p6: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
    p2-->>p4: isinstance(exc, ValueError)
    p2-->>p5: str(exc)
    p2-->>p5: str(exc)
    p2-->>p6: HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
```

> Call sequence diagram shows 28 of 28 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 22 of 22 (0 omitted); unresolved 5 of 5 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 2; effect analysis evaluated: 0, partial: 2, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 2 source steps with known totals: observed: 24, emitted: 19, omitted: 5. Unavailable totals are excluded.

- Effect collector omitted observations before flow assembly; displayed effects are partial.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `list_ready_tasks` | `available` | `partial` | `available` | `10` | `9` | `1` |
| `service.list_ready_tasks` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_handle_agent_error` | `available` | `partial` | `available` | `14` | `10` | `4` |
| `isinstance` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `exc.detail` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. list_ready_tasks"]
    s2["2. service.list_ready_tasks"]
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
    s1 -. "service.list_ready_tasks(…)" .-> s2
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
| `list_ready_tasks` | `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `service: Annotated[AgentService, Depends(get_agent_service)]`, `iteration_id: Optional[int]`, `tags: Annotated[Optional[list[str]], Query()]`, `priority_min: Optional[int]`, `priority_max: Optional[int]`, `assignee_id: Optional[int]`, `capabilities: Annotated[Optional[list[str]], Query()]` | - | - | `...` |
| `service.list_ready_tasks` | - | - | - | - |
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
| list_ready_tasks | service.list_ready_tasks | 772 | `service.list_ready_tasks(actor, iteration_id=iteration_id, tags=tags, priority_min=priority_min, priority_max=priority_max, assignee_id=assignee_id, capabilities=capabilities, limit=limit)` |
| list_ready_tasks | _handle_agent_error | 783 | `_handle_agent_error(exc)` |
| _handle_agent_error | isinstance | 271 | `isinstance(exc, AgentPermissionError)` |
| _handle_agent_error | str | 273 | `str(exc)` |
| _handle_agent_error | str | 275 | `str(exc)` |
| _handle_agent_error | HTTPException | 277 | `HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)` |
| _handle_agent_error | isinstance | 278 | `isinstance(exc, AgentRoutingConflictError)` |
| _handle_agent_error | HTTPException | 279 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _handle_agent_error | exc.detail | 279 | `exc.detail(data not statically known)` |
| _handle_agent_error | isinstance | 280 | `isinstance(exc, AgentTeamSetupConflictError)` |
| _handle_agent_error | HTTPException | 281 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `list_ready_tasks` | `service.list_ready_tasks` | 772 |
| external_call | `_handle_agent_error` | `isinstance` | 271 |
| external_call | `_handle_agent_error` | `HTTPException` | 277 |
| external_call | `_handle_agent_error` | `isinstance` | 278 |
| external_call | `_handle_agent_error` | `HTTPException` | 279 |
| unresolved_call | `_handle_agent_error` | `exc.detail` | 279 |
| external_call | `_handle_agent_error` | `isinstance` | 280 |
| external_call | `_handle_agent_error` | `HTTPException` | 281 |
| step_limit | `list_ready_tasks` | `first 12 steps` | 0 |

## Behavior

This flow starts at `list_ready_tasks` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
