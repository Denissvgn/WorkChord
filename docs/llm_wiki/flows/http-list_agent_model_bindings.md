# list_agent_model_bindings

**Entry point:** `list_agent_model_bindings` (`http`)
**Source:** [agent_catalog](../modules/agent_catalog.md)
**Modules touched:** [agent_catalog](../modules/agent_catalog.md), [routers_agent_planning](../modules/routers_agent_planning.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_agent_model_bindings
    participant p1 as service.list_bindings
    participant p2 as _handle_model_error
    participant p3 as isinstance (backend/app/routers/agent…log.py:_handle_model_error)
    participant p4 as HTTPException (backend/app/routers/agent…log.py:_handle_model_error)
    participant p5 as exc.detail (backend/app/routers/agent…log.py:_handle_model_error)
    participant p6 as str (backend/app/routers/agent…log.py:_handle_model_error)
    participant p7 as _handle_agent_error
    participant p8 as isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)
    participant p9 as HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)
    participant p10 as str (backend/app/routers/agent…ing.py:_handle_agent_error)
    participant p11 as exc.detail (backend/app/routers/agent…ing.py:_handle_agent_error)
    p0-->>p1: service.list_bindings(actor, actor_id=actor_id, include_disabled=include_disabled)
    p0->>p2: _handle_model_error
    p2-->>p3: isinstance (backend/app/routers/agent…log.py:_handle_model_error)(exc, AgentModelConflictError)
    p2-->>p4: HTTPException (backend/app/routers/agent…log.py:_handle_model_error)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p2-->>p5: exc.detail (backend/app/routers/agent…log.py:_handle_model_error)
    p2-->>p3: isinstance (backend/app/routers/agent…log.py:_handle_model_error)(exc, LookupError)
    p2-->>p4: HTTPException (backend/app/routers/agent…log.py:_handle_model_error)(status_code=status.HTTP_404_NOT_FOUND, detail={...})
    p2-->>p6: str (backend/app/routers/agent…log.py:_handle_model_error)(exc)
    p2->>p7: _handle_agent_error
    p7-->>p8: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, AgentPermissionError)
    p7-->>p9: HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)(status_code=status.HTTP_403_FORBIDDEN, detail=str(...))
    p7-->>p10: str (backend/app/routers/agent…ing.py:_handle_agent_error)(exc)
    p7-->>p8: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, AgentRoutingConflictError)
    p7-->>p9: HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p7-->>p11: exc.detail (backend/app/routers/agent…ing.py:_handle_agent_error)
    p7-->>p8: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, TaskVersionConflictError)
    p7-->>p9: HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p7-->>p11: exc.detail (backend/app/routers/agent…ing.py:_handle_agent_error)
    p7-->>p8: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, AgentConflictError)
    p7-->>p9: HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=str(...))
    p7-->>p10: str (backend/app/routers/agent…ing.py:_handle_agent_error)(exc)
    p7-->>p8: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, TriageConflictError)
    p7-->>p9: HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=str(...))
    p7-->>p10: str (backend/app/routers/agent…ing.py:_handle_agent_error)(exc)
    p7-->>p8: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, LookupError)
    p7-->>p9: HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)(status_code=status.HTTP_404_NOT_FOUND, detail=str(...))
    p7-->>p10: str (backend/app/routers/agent…ing.py:_handle_agent_error)(exc)
    p7-->>p8: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, ValueError)
    p7-->>p9: HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))
    p7-->>p10: str (backend/app/routers/agent…ing.py:_handle_agent_error)(exc)
```

> Call sequence diagram shows 30 of 30 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 24 of 24 (0 omitted); unresolved 4 of 4 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 3; effect analysis evaluated: 2, partial: 1, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 3 source steps with known totals: observed: 22, emitted: 18, omitted: 4. Unavailable totals are excluded.

- Effect collector omitted observations before flow assembly; displayed effects are partial.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `list_agent_model_bindings` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `service.list_bindings` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_handle_model_error` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `isinstance (backend/app/routers/agent…log.py:_handle_model_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/agent…log.py:_handle_model_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `exc.detail (backend/app/routers/agent…log.py:_handle_model_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance (backend/app/routers/agent…log.py:_handle_model_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/agent…log.py:_handle_model_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str (backend/app/routers/agent…log.py:_handle_model_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_handle_agent_error` | `available` | `partial` | `available` | `13` | `9` | `4` |
| `isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. list_agent_model_bindings"]
    s2["2. service.list_bindings"]
    s3["3. _handle_model_error"]
    s4["4. isinstance (backend/app/routers/agent…log.py:_handle_model_error)"]
    s5["5. HTTPException (backend/app/routers/agent…log.py:_handle_model_error)"]
    s6["6. exc.detail (backend/app/routers/agent…log.py:_handle_model_error)"]
    s7["7. isinstance (backend/app/routers/agent…log.py:_handle_model_error)"]
    s8["8. HTTPException (backend/app/routers/agent…log.py:_handle_model_error)"]
    s9["9. str (backend/app/routers/agent…log.py:_handle_model_error)"]
    s10["10. _handle_agent_error"]
    s11["11. isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)"]
    s12["12. HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)"]
    s1 -. "service.list_bindings(actor, actor_id=actor_id, include_disabled=include_disabled)" .-> s2
    s1 -->|"_handle_model_error(exc)"| s3
    s3 -. "isinstance (backend/app/routers/agent…log.py:_handle_model_error)(exc, AgentModelConflictError)" .-> s4
    s3 -. "HTTPException (backend/app/routers/agent…log.py:_handle_model_error)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))" .-> s5
    s3 -. "exc.detail (backend/app/routers/agent…log.py:_handle_model_error)(data not statically known)" .-> s6
    s3 -. "isinstance (backend/app/routers/agent…log.py:_handle_model_error)(exc, LookupError)" .-> s7
    s3 -. "HTTPException (backend/app/routers/agent…log.py:_handle_model_error)(status_code=status.HTTP_404_NOT_FOUND, detail={...})" .-> s8
    s3 -. "str (backend/app/routers/agent…log.py:_handle_model_error)(exc)" .-> s9
    s3 -->|"_handle_agent_error(exc)"| s10
    s10 -. "isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, AgentPermissionError)" .-> s11
    s10 -. "HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)(status_code=status.HTTP_403_FORBIDDEN, detail=str(...))" .-> s12
    click s1 "../modules/agent_catalog.md"
    click s3 "../modules/agent_catalog.md"
    click s10 "../modules/routers_agent_planning.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `list_agent_model_bindings` | `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `service: Annotated[AgentModelCatalogService, Depends(get_agent_model_catalog_service)]`, `actor_id: Annotated[int \| None, Query(ge=1)]`, `include_disabled: Annotated[bool, Query()]` | - | - | `...` |
| `service.list_bindings` | - | - | - | - |
| `_handle_model_error` | `exc: Exception` | `AgentModelConflictError`, `status`, `status` | - | - |
| `isinstance (backend/app/routers/agent…log.py:_handle_model_error)` | - | - | - | - |
| `HTTPException (backend/app/routers/agent…log.py:_handle_model_error)` | - | - | - | - |
| `exc.detail (backend/app/routers/agent…log.py:_handle_model_error)` | - | - | - | - |
| `isinstance (backend/app/routers/agent…log.py:_handle_model_error)` | - | - | - | - |
| `HTTPException (backend/app/routers/agent…log.py:_handle_model_error)` | - | - | - | - |
| `str (backend/app/routers/agent…log.py:_handle_model_error)` | - | - | - | - |
| `_handle_agent_error` | `exc: Exception` | `AgentPermissionError`, `status`, `AgentRoutingConflictError`, `status`, `TaskVersionConflictError`, `status`, `AgentConflictError`, `status` | - | - |
| `isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)` | - | - | - | - |
| `HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| list_agent_model_bindings | service.list_bindings | 278 | `service.list_bindings(actor, actor_id=actor_id, include_disabled=include_disabled)` |
| list_agent_model_bindings | _handle_model_error | 284 | `_handle_model_error(exc)` |
| _handle_model_error | isinstance (backend/app/routers/agent…log.py:_handle_model_error) | 51 | `isinstance(exc, AgentModelConflictError)` |
| _handle_model_error | HTTPException (backend/app/routers/agent…log.py:_handle_model_error) | 52 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _handle_model_error | exc.detail (backend/app/routers/agent…log.py:_handle_model_error) | 54 | `exc.detail(data not statically known)` |
| _handle_model_error | isinstance (backend/app/routers/agent…log.py:_handle_model_error) | 56 | `isinstance(exc, LookupError)` |
| _handle_model_error | HTTPException (backend/app/routers/agent…log.py:_handle_model_error) | 57 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={...})` |
| _handle_model_error | str (backend/app/routers/agent…log.py:_handle_model_error) | 61 | `str(exc)` |
| _handle_model_error | _handle_agent_error | 64 | `_handle_agent_error(exc)` |
| _handle_agent_error | isinstance (backend/app/routers/agent…ing.py:_handle_agent_error) | 106 | `isinstance(exc, AgentPermissionError)` |
| _handle_agent_error | HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error) | 107 | `HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(...))` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `list_agent_model_bindings` | `service.list_bindings` | 278 |
| external_call | `_handle_model_error` | `isinstance` | 51 |
| external_call | `_handle_model_error` | `HTTPException` | 52 |
| unresolved_call | `_handle_model_error` | `exc.detail` | 54 |
| external_call | `_handle_model_error` | `isinstance` | 56 |
| external_call | `_handle_model_error` | `HTTPException` | 57 |
| external_call | `_handle_agent_error` | `isinstance` | 106 |
| external_call | `_handle_agent_error` | `HTTPException` | 107 |
| step_limit | `list_agent_model_bindings` | `first 12 steps` | 0 |

## Behavior

This flow starts at `list_agent_model_bindings` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
