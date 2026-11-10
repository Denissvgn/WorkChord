# update_iteration

**Entry point:** `update_iteration` (`http`)
**Source:** [iterations](../modules/iterations.md)
**Modules touched:** [iterations](../modules/iterations.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as update_iteration
    participant p1 as service.update
    participant p2 as HTTPException
    participant p3 as str
    participant p4 as service.to_response
    p0-->>p1: service.update(iteration_id, data)
    p0-->>p2: HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))
    p0-->>p3: str(e)
    p0-->>p2: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)
    p0-->>p4: service.to_response(iteration)
```

> Call sequence diagram shows 5 of 5 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 3 of 3 (0 omitted); unresolved 2 of 2 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis evaluated.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 1; effect analysis evaluated: 1, partial: 0, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 1 source steps with known totals: observed: 7, emitted: 7, omitted: 0. Unavailable totals are excluded.

```mermaid
flowchart LR
    s1["1. update_iteration"]
    s2["2. service.update"]
    s3["3. HTTPException"]
    s4["4. str"]
    s5["5. HTTPException"]
    s6["6. service.to_response"]
    s1 -. "service.update(iteration_id, data)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s3
    s1 -. "str(e)" .-> s4
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s5
    s1 -. "service.to_response(iteration)" .-> s6
    b0["mutation service.update"]
    s1 -. "mutation service.update" .-> b0
    click s1 "../modules/iterations.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `update_iteration` | `iteration_id: int`, `data: IterationUpdate`, `service: Annotated[IterationService, Depends(get_iteration_service)]` | `status`, `status` | - | `service.to_response(...)` |
| `service.update` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `service.to_response` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| update_iteration | service.update | 134 | `service.update(iteration_id, data)` |
| update_iteration | HTTPException | 136 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| update_iteration | str | 138 | `str(e)` |
| update_iteration | HTTPException | 141 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| update_iteration | service.to_response | 145 | `service.to_response(iteration)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `service.update` | `update_iteration` | 134 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `update_iteration` | `HTTPException` | 136 |
| external_call | `update_iteration` | `HTTPException` | 141 |
| unresolved_call | `update_iteration` | `service.to_response` | 145 |

## Behavior

This flow starts at `update_iteration` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.

Calendar reassignment refreshes nominal workday and derived effort-day values under the existing planning transaction and version reservations. Canonical hours, unknown or zero estimates, estimate provenance and actual execution records are preserved.
