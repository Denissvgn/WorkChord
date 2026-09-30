# refresh_github_external_link

**Entry point:** `refresh_github_external_link` (`http`)
**Source:** [tasks](../modules/tasks.md)
**Modules touched:** [tasks](../modules/tasks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as refresh_github_external_link
    participant p1 as github_service.refresh_pull_request_status
    participant p2 as HTTPException
    participant p3 as str
    participant p4 as link_service.link_to_response
    p0-->>p1: github_service.refresh_pull_request_status
    p0-->>p2: HTTPException
    p0-->>p3: str
    p0-->>p2: HTTPException
    p0-->>p4: link_service.link_to_response
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. refresh_github_external_link"]
    s2["2. github_service.refresh_pull_request_status"]
    s3["3. HTTPException"]
    s4["4. str"]
    s5["5. HTTPException"]
    s6["6. link_service.link_to_response"]
    s1 -. "github_service.refresh_pull_request_status(link_id)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s3
    s1 -. "str(e)" .-> s4
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s5
    s1 -. "link_service.link_to_response(link)" .-> s6
    click s1 "../modules/tasks.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `refresh_github_external_link` | `link_id: int`, `github_service: Annotated[GitHubStatusService, Depends(get_github_status_service)]`, `link_service: Annotated[ExternalLinkService, Depends(get_external_link_service)]` | `ExternalLinkValidationError`, `status`, `status` | - | `link_service.link_to_response(...)` |
| `github_service.refresh_pull_request_status` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `link_service.link_to_response` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| refresh_github_external_link | github_service.refresh_pull_request_status | 501 | `github_service.refresh_pull_request_status(link_id)` |
| refresh_github_external_link | HTTPException | 503 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| refresh_github_external_link | str | 505 | `str(e)` |
| refresh_github_external_link | HTTPException | 509 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| refresh_github_external_link | link_service.link_to_response | 513 | `link_service.link_to_response(link)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `refresh_github_external_link` | `github_service.refresh_pull_request_status` | 501 |
| external_call | `refresh_github_external_link` | `HTTPException` | 503 |
| external_call | `refresh_github_external_link` | `HTTPException` | 509 |
| unresolved_call | `refresh_github_external_link` | `link_service.link_to_response` | 513 |

## Behavior

This flow starts at `refresh_github_external_link` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
