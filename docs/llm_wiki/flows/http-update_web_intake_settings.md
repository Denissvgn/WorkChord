# update_web_intake_settings

**Entry point:** `update_web_intake_settings` (`http`)
**Source:** [routers_system_settings](../modules/routers_system_settings.md)
**Modules touched:** [routers_system_settings](../modules/routers_system_settings.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as update_web_intake_settings
    participant p1 as service.update_web_intake
    participant p2 as _bad_request
    participant p3 as HTTPException
    participant p4 as str
    p0-->>p1: service.update_web_intake(data)
    p0->>p2: _bad_request
    p2-->>p3: HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))
    p2-->>p4: str(error)
```

> Call sequence diagram shows 4 of 4 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 2 of 2 (0 omitted); unresolved 1 of 1 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis evaluated.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 2; effect analysis evaluated: 2, partial: 0, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 2 source steps with known totals: observed: 7, emitted: 7, omitted: 0. Unavailable totals are excluded.

```mermaid
flowchart LR
    s1["1. update_web_intake_settings"]
    s2["2. service.update_web_intake"]
    s3["3. _bad_request"]
    s4["4. HTTPException"]
    s5["5. str"]
    s1 -. "service.update_web_intake(data)" .-> s2
    s1 -->|"_bad_request(exc)"| s3
    s3 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s4
    s3 -. "str(error)" .-> s5
    click s1 "../modules/routers_system_settings.md"
    click s3 "../modules/routers_system_settings.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `update_web_intake_settings` | `data: WebIntakeRuntimeSettingsUpdate`, `service: Annotated[RuntimeSettingsService, Depends(get_runtime_settings_service)]` | `RuntimeSettingsError` | - | `...` |
| `service.update_web_intake` | - | - | - | - |
| `_bad_request` | `error: ValueError` | `status` | - | `HTTPException(...)` |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| update_web_intake_settings | service.update_web_intake | 87 | `service.update_web_intake(data)` |
| update_web_intake_settings | _bad_request | 89 | `_bad_request(exc)` |
| _bad_request | HTTPException | 33 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| _bad_request | str | 33 | `str(error)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `update_web_intake_settings` | `service.update_web_intake` | 87 |
| external_call | `_bad_request` | `HTTPException` | 33 |

## Behavior

This flow starts at `update_web_intake_settings` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
