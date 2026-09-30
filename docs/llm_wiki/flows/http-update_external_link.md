# update_external_link

**Entry point:** `update_external_link` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [tasks](../modules/tasks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as update_external_link
    participant p1 as ExternalLinkUpdate.model_validate
    participant p2 as HTTPException
    participant p3 as str
    participant p4 as link_service.update
    participant p5 as link_service.link_to_response
    p0-->>p1: ExternalLinkUpdate.model_validate
    p0-->>p2: HTTPException
    p0-->>p3: str
    p0-->>p4: link_service.update
    p0-->>p2: HTTPException
    p0-->>p5: link_service.link_to_response
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
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
| update_external_link | ExternalLinkUpdate.model_validate | 526 | `ExternalLinkUpdate.model_validate(raw_data)` |
| update_external_link | HTTPException | 528 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| update_external_link | str | 530 | `str(e)` |
| update_external_link | link_service.update | 533 | `link_service.update(link_id, data)` |
| update_external_link | HTTPException | 535 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| update_external_link | link_service.link_to_response | 539 | `link_service.link_to_response(link)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `link_service.update` | `update_external_link` | 533 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `update_external_link` | `ExternalLinkUpdate.model_validate` | 526 |
| external_call | `update_external_link` | `HTTPException` | 528 |
| external_call | `update_external_link` | `HTTPException` | 535 |
| unresolved_call | `update_external_link` | `link_service.link_to_response` | 539 |

## Behavior

This flow starts at `update_external_link` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
