# create_task_external_link

**Entry point:** `create_task_external_link` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [tasks](../modules/tasks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as create_task_external_link
    participant p1 as TaskExternalLinkCreate.model_validate
    participant p2 as HTTPException
    participant p3 as str
    participant p4 as link_service.create_task_link
    participant p5 as link_service.link_to_response
    p0-->>p1: TaskExternalLinkCreate.model_validate
    p0-->>p2: HTTPException
    p0-->>p3: str
    p0-->>p4: link_service.create_task_link
    p0-->>p2: HTTPException
    p0-->>p5: link_service.link_to_response
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. create_task_external_link"]
    s2["2. TaskExternalLinkCreate.model_validate"]
    s3["3. HTTPException"]
    s4["4. str"]
    s5["5. link_service.create_task_link"]
    s6["6. HTTPException"]
    s7["7. link_service.link_to_response"]
    s1 -. "TaskExternalLinkCreate.model_validate(raw_data)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s3
    s1 -. "str(e)" .-> s4
    s1 -. "link_service.create_task_link(task_id, data)" .-> s5
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s6
    s1 -. "link_service.link_to_response(link)" .-> s7
    click s1 "../modules/tasks.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `create_task_external_link` | `task_id: int`, `raw_data: Annotated[dict, Body(...)]`, `link_service: Annotated[ExternalLinkService, Depends(get_external_link_service)]` | `ValidationError`, `status`, `status` | - | `link_service.link_to_response(...)` |
| `TaskExternalLinkCreate.model_validate` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `link_service.create_task_link` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `link_service.link_to_response` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| create_task_external_link | TaskExternalLinkCreate.model_validate | 436 | `TaskExternalLinkCreate.model_validate(raw_data)` |
| create_task_external_link | HTTPException | 438 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| create_task_external_link | str | 440 | `str(e)` |
| create_task_external_link | link_service.create_task_link | 443 | `link_service.create_task_link(task_id, data)` |
| create_task_external_link | HTTPException | 445 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| create_task_external_link | link_service.link_to_response | 449 | `link_service.link_to_response(link)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `create_task_external_link` | `TaskExternalLinkCreate.model_validate` | 436 |
| external_call | `create_task_external_link` | `HTTPException` | 438 |
| unresolved_call | `create_task_external_link` | `link_service.create_task_link` | 443 |
| external_call | `create_task_external_link` | `HTTPException` | 445 |
| unresolved_call | `create_task_external_link` | `link_service.link_to_response` | 449 |

## Behavior

This flow starts at `create_task_external_link` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
