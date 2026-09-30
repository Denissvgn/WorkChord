# create_task_github_external_link

**Entry point:** `create_task_github_external_link` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [tasks](../modules/tasks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as create_task_github_external_link
    participant p1 as GitHubExternalLinkCreate.model_validate
    participant p2 as link_service.create_task_github_link
    participant p3 as HTTPException
    participant p4 as str
    participant p5 as link_service.link_to_response
    p0-->>p1: GitHubExternalLinkCreate.model_validate
    p0-->>p2: link_service.create_task_github_link
    p0-->>p3: HTTPException
    p0-->>p4: str
    p0-->>p3: HTTPException
    p0-->>p4: str
    p0-->>p3: HTTPException
    p0-->>p4: str
    p0-->>p3: HTTPException
    p0-->>p5: link_service.link_to_response
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. create_task_github_external_link"]
    s2["2. GitHubExternalLinkCreate.model_validate"]
    s3["3. link_service.create_task_github_link"]
    s4["4. HTTPException"]
    s5["5. str"]
    s6["6. HTTPException"]
    s7["7. str"]
    s8["8. HTTPException"]
    s9["9. str"]
    s10["10. HTTPException"]
    s11["11. link_service.link_to_response"]
    s1 -. "GitHubExternalLinkCreate.model_validate(raw_data)" .-> s2
    s1 -. "link_service.create_task_github_link(task_id, data.url)" .-> s3
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s4
    s1 -. "str(e)" .-> s5
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s6
    s1 -. "str(e)" .-> s7
    s1 -. "HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(...))" .-> s8
    s1 -. "str(e)" .-> s9
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s10
    s1 -. "link_service.link_to_response(link)" .-> s11
    click s1 "../modules/tasks.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `create_task_github_external_link` | `task_id: int`, `raw_data: Annotated[dict, Body(...)]`, `link_service: Annotated[ExternalLinkService, Depends(get_external_link_service)]` | `ValidationError`, `status`, `ExternalLinkValidationError`, `status`, `ExternalLinkConflictError`, `status`, `status` | - | `link_service.link_to_response(...)` |
| `GitHubExternalLinkCreate.model_validate` | - | - | - | - |
| `link_service.create_task_github_link` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `link_service.link_to_response` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| create_task_github_external_link | GitHubExternalLinkCreate.model_validate | 466 | `GitHubExternalLinkCreate.model_validate(raw_data)` |
| create_task_github_external_link | link_service.create_task_github_link | 467 | `link_service.create_task_github_link(task_id, data.url)` |
| create_task_github_external_link | HTTPException | 469 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| create_task_github_external_link | str | 471 | `str(e)` |
| create_task_github_external_link | HTTPException | 474 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| create_task_github_external_link | str | 476 | `str(e)` |
| create_task_github_external_link | HTTPException | 479 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(...))` |
| create_task_github_external_link | str | 481 | `str(e)` |
| create_task_github_external_link | HTTPException | 485 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| create_task_github_external_link | link_service.link_to_response | 489 | `link_service.link_to_response(link)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `create_task_github_external_link` | `GitHubExternalLinkCreate.model_validate` | 466 |
| unresolved_call | `create_task_github_external_link` | `link_service.create_task_github_link` | 467 |
| external_call | `create_task_github_external_link` | `HTTPException` | 469 |
| external_call | `create_task_github_external_link` | `HTTPException` | 474 |
| external_call | `create_task_github_external_link` | `HTTPException` | 479 |
| external_call | `create_task_github_external_link` | `HTTPException` | 485 |
| unresolved_call | `create_task_github_external_link` | `link_service.link_to_response` | 489 |

## Behavior

This flow starts at `create_task_github_external_link` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
