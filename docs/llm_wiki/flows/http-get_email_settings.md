# get_email_settings

**Entry point:** `get_email_settings` (`http`)
**Source:** [routers_email_settings](../modules/routers_email_settings.md)
**Modules touched:** [routers_email_settings](../modules/routers_email_settings.md), [schemas_email_settings](../modules/schemas_email_settings.md), [settings_read](../modules/settings_read.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_email_settings
    participant p1 as service.get_settings
    participant p2 as HTTPException
    participant p3 as str
    participant p4 as _response
    participant p5 as withholds
    participant p6 as service.db.info.get
    participant p7 as redact_email_settings
    participant p8 as EmailSettingsResponse
    participant p9 as response.model_copy
    p0-->>p1: service.get_settings
    p0-->>p2: HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))
    p0-->>p3: str(exc)
    p0->>p4: _response
    p0->>p5: withholds
    p0-->>p6: service.db.info.get('authority')
    p0->>p7: redact_email_settings
    p4->>p8: EmailSettingsResponse
    p7-->>p9: response.model_copy(update={...})
```

> Call sequence diagram shows 9 of 9 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 2 of 2 (0 omitted); unresolved 3 of 3 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 5; effect analysis evaluated: 4, partial: 0, unavailable: 1. Counts include steps omitted from the displayed trace.

Collector observations for 4 source steps with known totals: observed: 10, emitted: 10, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `get_email_settings` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `service.get_settings` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_response` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `EmailSettingsResponse` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `withholds` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `service.db.info.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `redact_email_settings` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `response.model_copy` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. get_email_settings"]
    s2["2. service.get_settings"]
    s3["3. HTTPException"]
    s4["4. str"]
    s5["5. _response"]
    s6["6. EmailSettingsResponse"]
    s7["7. withholds"]
    s8["8. service.db.info.get"]
    s9["9. redact_email_settings"]
    s10["10. response.model_copy"]
    s1 -. "service.get_settings(data not statically known)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s3
    s1 -. "str(exc)" .-> s4
    s1 -->|"_response(settings)"| s5
    s5 -->|"EmailSettingsResponse(…)"| s6
    s1 -->|"withholds(service.db.info.get(...))"| s7
    s1 -. "service.db.info.get('authority')" .-> s8
    s1 -->|"redact_email_settings(response)"| s9
    s9 -. "response.model_copy(update={...})" .-> s10
    click s1 "../modules/routers_email_settings.md"
    click s5 "../modules/routers_email_settings.md"
    click s6 "../modules/schemas_email_settings.md"
    click s7 "../modules/settings_read.md"
    click s9 "../modules/settings_read.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_email_settings` | `service: Annotated[EmailSettingsService, Depends(get_settings_service)]` | `RuntimeSettingsError`, `status` | - | `...` |
| `service.get_settings` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `_response` | `settings` | - | - | `EmailSettingsResponse(...)` |
| `EmailSettingsResponse` | - | - | - | - |
| `withholds` | `authority` | - | - | `...` |
| `service.db.info.get` | - | - | - | - |
| `redact_email_settings` | `response` | - | - | `response.model_copy(...)` |
| `response.model_copy` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_email_settings | service.get_settings | 49 | `service.get_settings(data not statically known)` |
| get_email_settings | HTTPException | 51 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| get_email_settings | str | 53 | `str(exc)` |
| get_email_settings | _response | 56 | `_response(settings)` |
| _response | EmailSettingsResponse | 24 | `EmailSettingsResponse(enabled=settings.enabled, smtp_host=settings.smtp_host, smtp_port=settings.smtp_port, smtp_user=settings.smtp_user, smtp_from_email=settings.smtp_from_email, smtp_use_tls=settings.smtp_use_tls, has_password=settings.has_password, field_sources=settings.field_sources)` |
| get_email_settings | withholds | 57 | `withholds(service.db.info.get(...))` |
| get_email_settings | service.db.info.get | 57 | `service.db.info.get('authority')` |
| get_email_settings | redact_email_settings | 57 | `redact_email_settings(response)` |
| redact_email_settings | response.model_copy | 59 | `response.model_copy(update={...})` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_email_settings` | `service.get_settings` | 49 |
| external_call | `get_email_settings` | `HTTPException` | 51 |
| unresolved_call | `get_email_settings` | `service.db.info.get` | 57 |
| unresolved_call | `redact_email_settings` | `response.model_copy` | 59 |

## Behavior

This flow starts at `get_email_settings` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
