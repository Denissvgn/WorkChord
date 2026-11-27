# create_agent_model_catalog_entry

**Entry point:** `create_agent_model_catalog_entry` (`http`)
**Source:** [agent_catalog](../modules/agent_catalog.md)
**Modules touched:** [agent_catalog](../modules/agent_catalog.md), [routers_agent_planning](../modules/routers_agent_planning.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as create_agent_model_catalog_entry
    participant p1 as _handle_model_error
    participant p2 as _handle_agent_error
    participant p3 as isinstance (backend/app/routers/agent…log.py:_handle_model_error)
    participant p4 as service.create_catalog
    participant p5 as HTTPException (backend/app/routers/agent…log.py:_handle_model_error)
    participant p6 as exc.detail (backend/app/routers/agent…log.py:_handle_model_error)
    participant p7 as str (backend/app/routers/agent…log.py:_handle_model_error)
    participant p8 as isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)
    participant p9 as HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)
    participant p10 as str (backend/app/routers/agent…ing.py:_handle_agent_error)
    participant p11 as exc.detail (backend/app/routers/agent…ing.py:_handle_agent_error)
    p0->>p1: _handle_model_error
    p1->>p2: _handle_agent_error
    p1-->>p3: isinstance (backend/app/routers/agent…log.py:_handle_model_error)(exc, AgentModelConflictError)
    p0-->>p4: service.create_catalog(actor, data, command=command)
    p1-->>p5: HTTPException (backend/app/routers/agent…log.py:_handle_model_error)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p1-->>p6: exc.detail (backend/app/routers/agent…log.py:_handle_model_error)
    p1-->>p3: isinstance (backend/app/routers/agent…log.py:_handle_model_error)(exc, LookupError)
    p1-->>p5: HTTPException (backend/app/routers/agent…log.py:_handle_model_error)(status_code=status.HTTP_404_NOT_FOUND, detail={...})
    p1-->>p7: str (backend/app/routers/agent…log.py:_handle_model_error)(exc)
    p2-->>p8: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, AgentPermissionError)
    p2-->>p9: HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)(status_code=status.HTTP_403_FORBIDDEN, detail=str(...))
    p2-->>p10: str (backend/app/routers/agent…ing.py:_handle_agent_error)(exc)
    p2-->>p8: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, AgentRoutingConflictError)
    p2-->>p9: HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p2-->>p11: exc.detail (backend/app/routers/agent…ing.py:_handle_agent_error)
    p2-->>p8: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, TaskVersionConflictError)
    p2-->>p9: HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p2-->>p11: exc.detail (backend/app/routers/agent…ing.py:_handle_agent_error)
    p2-->>p8: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, AgentConflictError)
    p2-->>p9: HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=str(...))
    p2-->>p10: str (backend/app/routers/agent…ing.py:_handle_agent_error)(exc)
    p2-->>p8: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, TriageConflictError)
    p2-->>p9: HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=str(...))
    p2-->>p10: str (backend/app/routers/agent…ing.py:_handle_agent_error)(exc)
    p2-->>p8: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, LookupError)
    p2-->>p9: HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)(status_code=status.HTTP_404_NOT_FOUND, detail=str(...))
    p2-->>p10: str (backend/app/routers/agent…ing.py:_handle_agent_error)(exc)
    p2-->>p8: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, SourceLinkRefused)
    p2-->>p9: HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)(status_code=status.HTTP_400_BAD_REQUEST, detail=exc.detail(...))
    p2-->>p11: exc.detail (backend/app/routers/agent…ing.py:_handle_agent_error)
```

> Call sequence diagram shows 30 of 33 interactions; 3 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 23 of 26 (3 omitted); unresolved 5 of 5 (0 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/routers/agent_planning.py:_handle_agent_error` | 10 | - | external | 3 |
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 3; effect analysis evaluated: 2, partial: 1, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 3 source steps with known totals: observed: 24, emitted: 18, omitted: 6. Unavailable totals are excluded.

- Effect collector omitted observations before flow assembly; displayed effects are partial.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `create_agent_model_catalog_entry` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `service.create_catalog` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_handle_model_error` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `isinstance (backend/app/routers/agent…log.py:_handle_model_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/agent…log.py:_handle_model_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `exc.detail (backend/app/routers/agent…log.py:_handle_model_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance (backend/app/routers/agent…log.py:_handle_model_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/agent…log.py:_handle_model_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str (backend/app/routers/agent…log.py:_handle_model_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_handle_agent_error` | `available` | `partial` | `available` | `15` | `9` | `6` |
| `isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. create_agent_model_catalog_entry"]
    s2["2. service.create_catalog"]
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
    s1 -. "service.create_catalog(actor, data, command=command)" .-> s2
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
| `create_agent_model_catalog_entry` | `data: AgentModelCatalogCreate`, `actor: Annotated[AgentActor, Depends(get_model_catalog_principal)]`, `service: Annotated[AgentModelCatalogService, Depends(get_agent_model_catalog_service)]`, `command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)]` | - | - | `...` |
| `service.create_catalog` | - | - | - | - |
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
| create_agent_model_catalog_entry | service.create_catalog | 288 | `service.create_catalog(actor, data, command=command)` |
| create_agent_model_catalog_entry | _handle_model_error | 290 | `_handle_model_error(exc)` |
| _handle_model_error | isinstance (backend/app/routers/agent…log.py:_handle_model_error) | 142 | `isinstance(exc, AgentModelConflictError)` |
| _handle_model_error | HTTPException (backend/app/routers/agent…log.py:_handle_model_error) | 143 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _handle_model_error | exc.detail (backend/app/routers/agent…log.py:_handle_model_error) | 145 | `exc.detail(data not statically known)` |
| _handle_model_error | isinstance (backend/app/routers/agent…log.py:_handle_model_error) | 147 | `isinstance(exc, LookupError)` |
| _handle_model_error | HTTPException (backend/app/routers/agent…log.py:_handle_model_error) | 148 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={...})` |
| _handle_model_error | str (backend/app/routers/agent…log.py:_handle_model_error) | 152 | `str(exc)` |
| _handle_model_error | _handle_agent_error | 155 | `_handle_agent_error(exc)` |
| _handle_agent_error | isinstance (backend/app/routers/agent…ing.py:_handle_agent_error) | 110 | `isinstance(exc, AgentPermissionError)` |
| _handle_agent_error | HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error) | 111 | `HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(...))` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `create_agent_model_catalog_entry` | `service.create_catalog` | 288 |
| external_call | `_handle_model_error` | `isinstance` | 142 |
| external_call | `_handle_model_error` | `HTTPException` | 143 |
| unresolved_call | `_handle_model_error` | `exc.detail` | 145 |
| external_call | `_handle_model_error` | `isinstance` | 147 |
| external_call | `_handle_model_error` | `HTTPException` | 148 |
| external_call | `_handle_agent_error` | `isinstance` | 110 |
| external_call | `_handle_agent_error` | `HTTPException` | 111 |
| step_limit | `create_agent_model_catalog_entry` | `first 12 steps` | 0 |

## Behavior

This flow starts at `create_agent_model_catalog_entry` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
