# get_agent_model_catalog_entry

**Entry point:** `get_agent_model_catalog_entry` (`http`)
**Source:** [agent_catalog](../modules/agent_catalog.md)
**Modules touched:** [agent_catalog](../modules/agent_catalog.md), [routers_agent_planning](../modules/routers_agent_planning.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_agent_model_catalog_entry
    participant p1 as _handle_model_error
    participant p2 as _handle_agent_error
    participant p3 as isinstance (backend/app/routers/agent…log.py:_handle_model_error)
    participant p4 as service.get_catalog
    participant p5 as catalog_key.strip().lower
    participant p6 as catalog_key.strip
    participant p7 as HTTPException (backend/app/routers/agent…log.py:_handle_model_error)
    participant p8 as exc.detail (backend/app/routers/agent…log.py:_handle_model_error)
    participant p9 as str (backend/app/routers/agent…log.py:_handle_model_error)
    participant p10 as isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)
    participant p11 as HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)
    participant p12 as str (backend/app/routers/agent…ing.py:_handle_agent_error)
    participant p13 as exc.detail (backend/app/routers/agent…ing.py:_handle_agent_error)
    p0->>p1: _handle_model_error
    p1->>p2: _handle_agent_error
    p1-->>p3: isinstance (backend/app/routers/agent…log.py:_handle_model_error)(exc, AgentModelConflictError)
    p0-->>p4: service.get_catalog(actor, ...)
    p0-->>p5: catalog_key.strip().lower
    p0-->>p6: catalog_key.strip
    p1-->>p7: HTTPException (backend/app/routers/agent…log.py:_handle_model_error)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p1-->>p8: exc.detail (backend/app/routers/agent…log.py:_handle_model_error)
    p1-->>p3: isinstance (backend/app/routers/agent…log.py:_handle_model_error)(exc, LookupError)
    p1-->>p7: HTTPException (backend/app/routers/agent…log.py:_handle_model_error)(status_code=status.HTTP_404_NOT_FOUND, detail={...})
    p1-->>p9: str (backend/app/routers/agent…log.py:_handle_model_error)(exc)
    p2-->>p10: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, AgentPermissionError)
    p2-->>p11: HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)(status_code=status.HTTP_403_FORBIDDEN, detail=str(...))
    p2-->>p12: str (backend/app/routers/agent…ing.py:_handle_agent_error)(exc)
    p2-->>p10: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, AgentRoutingConflictError)
    p2-->>p11: HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p2-->>p13: exc.detail (backend/app/routers/agent…ing.py:_handle_agent_error)
    p2-->>p10: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, TaskVersionConflictError)
    p2-->>p11: HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p2-->>p13: exc.detail (backend/app/routers/agent…ing.py:_handle_agent_error)
    p2-->>p10: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, AgentConflictError)
    p2-->>p11: HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=str(...))
    p2-->>p12: str (backend/app/routers/agent…ing.py:_handle_agent_error)(exc)
    p2-->>p10: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, TriageConflictError)
    p2-->>p11: HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)(status_code=status.HTTP_409_CONFLICT, detail=str(...))
    p2-->>p12: str (backend/app/routers/agent…ing.py:_handle_agent_error)(exc)
    p2-->>p10: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, LookupError)
    p2-->>p11: HTTPException (backend/app/routers/agent…ing.py:_handle_agent_error)(status_code=status.HTTP_404_NOT_FOUND, detail=str(...))
    p2-->>p12: str (backend/app/routers/agent…ing.py:_handle_agent_error)(exc)
    p2-->>p10: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, ValueError)
```

> Call sequence diagram shows 30 of 32 interactions; 2 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 22 of 24 (2 omitted); unresolved 6 of 6 (0 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/routers/agent_planning.py:_handle_agent_error` | 12 | - | external | 2 |
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 3; effect analysis evaluated: 2, partial: 1, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 3 source steps with known totals: observed: 21, emitted: 17, omitted: 4. Unavailable totals are excluded.

- Effect collector omitted observations before flow assembly; displayed effects are partial.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `get_agent_model_catalog_entry` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `service.get_catalog` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `catalog_key.strip().lower` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `catalog_key.strip` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_handle_model_error` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `isinstance (backend/app/routers/agent…log.py:_handle_model_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/agent…log.py:_handle_model_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `exc.detail (backend/app/routers/agent…log.py:_handle_model_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance (backend/app/routers/agent…log.py:_handle_model_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException (backend/app/routers/agent…log.py:_handle_model_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str (backend/app/routers/agent…log.py:_handle_model_error)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_handle_agent_error` | `available` | `partial` | `available` | `13` | `9` | `4` |

```mermaid
flowchart LR
    s1["1. get_agent_model_catalog_entry"]
    s2["2. service.get_catalog"]
    s3["3. catalog_key.strip().lower"]
    s4["4. catalog_key.strip"]
    s5["5. _handle_model_error"]
    s6["6. isinstance (backend/app/routers/agent…log.py:_handle_model_error)"]
    s7["7. HTTPException (backend/app/routers/agent…log.py:_handle_model_error)"]
    s8["8. exc.detail (backend/app/routers/agent…log.py:_handle_model_error)"]
    s9["9. isinstance (backend/app/routers/agent…log.py:_handle_model_error)"]
    s10["10. HTTPException (backend/app/routers/agent…log.py:_handle_model_error)"]
    s11["11. str (backend/app/routers/agent…log.py:_handle_model_error)"]
    s12["12. _handle_agent_error"]
    s1 -. "service.get_catalog(actor, ...)" .-> s2
    s1 -. "catalog_key.strip().lower(data not statically known)" .-> s3
    s1 -. "catalog_key.strip(data not statically known)" .-> s4
    s1 -->|"_handle_model_error(exc)"| s5
    s5 -. "isinstance (backend/app/routers/agent…log.py:_handle_model_error)(exc, AgentModelConflictError)" .-> s6
    s5 -. "HTTPException (backend/app/routers/agent…log.py:_handle_model_error)(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))" .-> s7
    s5 -. "exc.detail (backend/app/routers/agent…log.py:_handle_model_error)(data not statically known)" .-> s8
    s5 -. "isinstance (backend/app/routers/agent…log.py:_handle_model_error)(exc, LookupError)" .-> s9
    s5 -. "HTTPException (backend/app/routers/agent…log.py:_handle_model_error)(status_code=status.HTTP_404_NOT_FOUND, detail={...})" .-> s10
    s5 -. "str (backend/app/routers/agent…log.py:_handle_model_error)(exc)" .-> s11
    s5 -->|"_handle_agent_error(exc)"| s12
    click s1 "../modules/agent_catalog.md"
    click s5 "../modules/agent_catalog.md"
    click s12 "../modules/routers_agent_planning.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_agent_model_catalog_entry` | `catalog_key: str`, `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `service: Annotated[AgentModelCatalogService, Depends(get_agent_model_catalog_service)]` | - | - | `...` |
| `service.get_catalog` | - | - | - | - |
| `catalog_key.strip().lower` | - | - | - | - |
| `catalog_key.strip` | - | - | - | - |
| `_handle_model_error` | `exc: Exception` | `AgentModelConflictError`, `status`, `status` | - | - |
| `isinstance (backend/app/routers/agent…log.py:_handle_model_error)` | - | - | - | - |
| `HTTPException (backend/app/routers/agent…log.py:_handle_model_error)` | - | - | - | - |
| `exc.detail (backend/app/routers/agent…log.py:_handle_model_error)` | - | - | - | - |
| `isinstance (backend/app/routers/agent…log.py:_handle_model_error)` | - | - | - | - |
| `HTTPException (backend/app/routers/agent…log.py:_handle_model_error)` | - | - | - | - |
| `str (backend/app/routers/agent…log.py:_handle_model_error)` | - | - | - | - |
| `_handle_agent_error` | `exc: Exception` | `AgentPermissionError`, `status`, `AgentRoutingConflictError`, `status`, `TaskVersionConflictError`, `status`, `AgentConflictError`, `status` | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_agent_model_catalog_entry | service.get_catalog | 172 | `service.get_catalog(actor, ...)` |
| get_agent_model_catalog_entry | catalog_key.strip().lower | 172 | `catalog_key.strip().lower(data not statically known)` |
| get_agent_model_catalog_entry | catalog_key.strip | 172 | `catalog_key.strip(data not statically known)` |
| get_agent_model_catalog_entry | _handle_model_error | 174 | `_handle_model_error(exc)` |
| _handle_model_error | isinstance (backend/app/routers/agent…log.py:_handle_model_error) | 51 | `isinstance(exc, AgentModelConflictError)` |
| _handle_model_error | HTTPException (backend/app/routers/agent…log.py:_handle_model_error) | 52 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _handle_model_error | exc.detail (backend/app/routers/agent…log.py:_handle_model_error) | 54 | `exc.detail(data not statically known)` |
| _handle_model_error | isinstance (backend/app/routers/agent…log.py:_handle_model_error) | 56 | `isinstance(exc, LookupError)` |
| _handle_model_error | HTTPException (backend/app/routers/agent…log.py:_handle_model_error) | 57 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={...})` |
| _handle_model_error | str (backend/app/routers/agent…log.py:_handle_model_error) | 61 | `str(exc)` |
| _handle_model_error | _handle_agent_error | 64 | `_handle_agent_error(exc)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_agent_model_catalog_entry` | `service.get_catalog` | 172 |
| unresolved_call | `get_agent_model_catalog_entry` | `catalog_key.strip().lower` | 172 |
| unresolved_call | `get_agent_model_catalog_entry` | `catalog_key.strip` | 172 |
| external_call | `_handle_model_error` | `isinstance` | 51 |
| external_call | `_handle_model_error` | `HTTPException` | 52 |
| unresolved_call | `_handle_model_error` | `exc.detail` | 54 |
| external_call | `_handle_model_error` | `isinstance` | 56 |
| external_call | `_handle_model_error` | `HTTPException` | 57 |
| step_limit | `get_agent_model_catalog_entry` | `first 12 steps` | 0 |

## Behavior

This flow starts at `get_agent_model_catalog_entry` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
