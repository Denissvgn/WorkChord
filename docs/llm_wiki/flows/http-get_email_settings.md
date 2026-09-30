# get_email_settings

**Entry point:** `get_email_settings` (`http`)
**Source:** [routers_email_settings](../modules/routers_email_settings.md)
**Modules touched:** [routers_email_settings](../modules/routers_email_settings.md), [schemas_email_settings](../modules/schemas_email_settings.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_email_settings
    participant p1 as service.get_settings
    participant p2 as HTTPException
    participant p3 as str
    participant p4 as _response
    participant p5 as EmailSettingsResponse
    p0-->>p1: service.get_settings
    p0-->>p2: HTTPException
    p0-->>p3: str
    p0->>p4: _response
    p4->>p5: EmailSettingsResponse
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_email_settings"]
    s2["2. service.get_settings"]
    s3["3. HTTPException"]
    s4["4. str"]
    s5["5. _response"]
    s6["6. EmailSettingsResponse"]
    s1 -. "service.get_settings(data not statically known)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s3
    s1 -. "str(exc)" .-> s4
    s1 -->|"_response(settings)"| s5
    s5 -->|"EmailSettingsResponse(…)"| s6
    click s1 "../modules/routers_email_settings.md"
    click s5 "../modules/routers_email_settings.md"
    click s6 "../modules/schemas_email_settings.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_email_settings` | `service: Annotated[EmailSettingsService, Depends(get_settings_service)]` | `RuntimeSettingsError`, `status` | - | `_response(...)` |
| `service.get_settings` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `_response` | `settings` | - | - | `EmailSettingsResponse(...)` |
| `EmailSettingsResponse` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_email_settings | service.get_settings | 49 | `service.get_settings(data not statically known)` |
| get_email_settings | HTTPException | 51 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| get_email_settings | str | 53 | `str(exc)` |
| get_email_settings | _response | 56 | `_response(settings)` |
| _response | EmailSettingsResponse | 24 | `EmailSettingsResponse(enabled=settings.enabled, smtp_host=settings.smtp_host, smtp_port=settings.smtp_port, smtp_user=settings.smtp_user, smtp_from_email=settings.smtp_from_email, smtp_use_tls=settings.smtp_use_tls, has_password=settings.has_password, field_sources=settings.field_sources)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_email_settings` | `service.get_settings` | 49 |
| external_call | `get_email_settings` | `HTTPException` | 51 |

## Behavior

This flow starts at `get_email_settings` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
