# update_github_settings

**Entry point:** `update_github_settings` (`http`)
**Source:** [routers_system_settings](../modules/routers_system_settings.md)
**Modules touched:** [routers_system_settings](../modules/routers_system_settings.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as update_github_settings
    participant p1 as service.update_github
    participant p2 as _bad_request
    participant p3 as HTTPException
    participant p4 as str
    p0-->>p1: service.update_github
    p0->>p2: _bad_request
    p2-->>p3: HTTPException
    p2-->>p4: str
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. update_github_settings"]
    s2["2. service.update_github"]
    s3["3. _bad_request"]
    s4["4. HTTPException"]
    s5["5. str"]
    s1 -. "service.update_github(data)" .-> s2
    s1 -->|"_bad_request(exc)"| s3
    s3 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s4
    s3 -. "str(error)" .-> s5
    click s1 "../modules/routers_system_settings.md"
    click s3 "../modules/routers_system_settings.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `update_github_settings` | `data: GitHubRuntimeSettingsUpdate`, `service: Annotated[RuntimeSettingsService, Depends(get_runtime_settings_service)]` | `RuntimeSettingsError` | - | `...` |
| `service.update_github` | - | - | - | - |
| `_bad_request` | `error: ValueError` | `status` | - | `HTTPException(...)` |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| update_github_settings | service.update_github | 75 | `service.update_github(data)` |
| update_github_settings | _bad_request | 77 | `_bad_request(exc)` |
| _bad_request | HTTPException | 33 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| _bad_request | str | 33 | `str(error)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `update_github_settings` | `service.update_github` | 75 |
| external_call | `_bad_request` | `HTTPException` | 33 |

## Behavior

This flow starts at `update_github_settings` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
