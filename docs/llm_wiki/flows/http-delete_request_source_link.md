# delete_request_source_link

**Entry point:** `delete_request_source_link` (`http`)
**Source:** [request_sources](../modules/request_sources.md)
**Modules touched:** [request_sources](../modules/request_sources.md), [schemas_common](../modules/schemas_common.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as delete_request_source_link
    participant p1 as service.unlink
    participant p2 as HTTPException
    participant p3 as MessageResponse
    p0-->>p1: service.unlink(link_id)
    p0-->>p2: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)
    p0->>p3: MessageResponse
```

> Call sequence diagram shows 3 of 3 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 1 (0 omitted); unresolved 1 of 1 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 2; effect analysis evaluated: 1, partial: 0, unavailable: 1. Counts include steps omitted from the displayed trace.

Collector observations for 1 source steps with known totals: observed: 5, emitted: 5, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `delete_request_source_link` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `service.unlink` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `MessageResponse` | `unavailable` | `unavailable` | `unavailable` | — | — | — |

```mermaid
flowchart LR
    s1["1. delete_request_source_link"]
    s2["2. service.unlink"]
    s3["3. HTTPException"]
    s4["4. MessageResponse"]
    s1 -. "service.unlink(link_id)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s3
    s1 -->|"MessageResponse(message=..., success=True)"| s4
    b0["filesystem_write service.unlink"]
    s1 -. "filesystem_write service.unlink" .-> b0
    click s1 "../modules/request_sources.md"
    click s4 "../modules/schemas_common.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `delete_request_source_link` | `link_id: int`, `service: Annotated[RequestSourceService, Depends(get_request_source_service)]` | `status` | - | `MessageResponse(...)` |
| `service.unlink` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `MessageResponse` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| delete_request_source_link | service.unlink | 104 | `service.unlink(link_id)` |
| delete_request_source_link | HTTPException | 106 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| delete_request_source_link | MessageResponse | 110 | `MessageResponse(message=..., success=True)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| filesystem_write | `service.unlink` | `delete_request_source_link` | 104 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `delete_request_source_link` | `HTTPException` | 106 |

## Behavior

This flow starts at `delete_request_source_link` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
