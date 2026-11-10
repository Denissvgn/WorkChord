# update_external_link

**Entry point:** `update_external_link` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [tasks](../modules/tasks.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as update_external_link
    participant p1 as ExternalLinkUpdate.model_validate
    participant p2 as HTTPException
    participant p3 as str
    participant p4 as link_service.update
    participant p5 as link_service.link_to_response
    p0-->>p1: ExternalLinkUpdate.model_validate(raw_data)
    p0-->>p2: HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))
    p0-->>p3: str(e)
    p0-->>p4: link_service.update(link_id, data)
    p0-->>p2: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)
    p0-->>p5: link_service.link_to_response(link)
```

> Call sequence diagram shows 6 of 6 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 3 of 3 (0 omitted); unresolved 3 of 3 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis evaluated.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 1; effect analysis evaluated: 1, partial: 0, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 1 source steps with known totals: observed: 8, emitted: 8, omitted: 0. Unavailable totals are excluded.

```mermaid
flowchart LR
    s1["1. update_external_link"]
    s2["2. ExternalLinkUpdate.model_validate"]
    s3["3. HTTPException"]
    s4["4. str"]
    s5["5. link_service.update"]
    s6["6. HTTPException"]
    s7["7. link_service.link_to_response"]
    s1 -. "ExternalLinkUpdate.model_validate(raw_data)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s3
    s1 -. "str(e)" .-> s4
    s1 -. "link_service.update(link_id, data)" .-> s5
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s6
    s1 -. "link_service.link_to_response(link)" .-> s7
    b0["mutation link_service.update"]
    s1 -. "mutation link_service.update" .-> b0
    click s1 "../modules/tasks.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `update_external_link` | `link_id: int`, `raw_data: Annotated[dict, Body(...)]`, `link_service: Annotated[ExternalLinkService, Depends(get_external_link_service)]` | `ValidationError`, `status`, `status` | - | `link_service.link_to_response(...)` |
| `ExternalLinkUpdate.model_validate` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `link_service.update` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `link_service.link_to_response` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| update_external_link | ExternalLinkUpdate.model_validate | 529 | `ExternalLinkUpdate.model_validate(raw_data)` |
| update_external_link | HTTPException | 531 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| update_external_link | str | 533 | `str(e)` |
| update_external_link | link_service.update | 536 | `link_service.update(link_id, data)` |
| update_external_link | HTTPException | 538 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| update_external_link | link_service.link_to_response | 542 | `link_service.link_to_response(link)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `link_service.update` | `update_external_link` | 536 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `update_external_link` | `ExternalLinkUpdate.model_validate` | 529 |
| external_call | `update_external_link` | `HTTPException` | 531 |
| external_call | `update_external_link` | `HTTPException` | 538 |
| unresolved_call | `update_external_link` | `link_service.link_to_response` | 542 |

## Behavior

This flow starts at `update_external_link` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
