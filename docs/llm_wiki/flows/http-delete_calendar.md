# delete_calendar

**Entry point:** `delete_calendar` (`http`)
**Source:** [calendars](../modules/calendars.md)
**Modules touched:** [calendars](../modules/calendars.md), [schemas_common](../modules/schemas_common.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as delete_calendar
    participant p1 as service.delete
    participant p2 as HTTPException
    participant p3 as str
    participant p4 as MessageResponse
    p0-->>p1: service.delete(calendar_id)
    p0-->>p2: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(...))
    p0-->>p3: str(e)
    p0-->>p2: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)
    p0->>p4: MessageResponse
```

> Call sequence diagram shows 5 of 5 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 3 of 3 (0 omitted); unresolved 1 of 1 (0 omitted). These counts cover the captured static trace.
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
| `delete_calendar` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `service.delete` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `HTTPException` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `MessageResponse` | `unavailable` | `unavailable` | `unavailable` | — | — | — |

```mermaid
flowchart LR
    s1["1. delete_calendar"]
    s2["2. service.delete"]
    s3["3. HTTPException"]
    s4["4. str"]
    s5["5. HTTPException"]
    s6["6. MessageResponse"]
    s1 -. "service.delete(calendar_id)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(...))" .-> s3
    s1 -. "str(e)" .-> s4
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s5
    s1 -->|"MessageResponse(message=..., success=True)"| s6
    click s1 "../modules/calendars.md"
    click s6 "../modules/schemas_common.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `delete_calendar` | `calendar_id: int`, `service: Annotated[CalendarService, Depends(get_calendar_service)]` | `status`, `status` | - | `MessageResponse(...)` |
| `service.delete` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `MessageResponse` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| delete_calendar | service.delete | 84 | `service.delete(calendar_id)` |
| delete_calendar | HTTPException | 86 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(...))` |
| delete_calendar | str | 88 | `str(e)` |
| delete_calendar | HTTPException | 91 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| delete_calendar | MessageResponse | 95 | `MessageResponse(message=..., success=True)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `delete_calendar` | `service.delete` | 84 |
| external_call | `delete_calendar` | `HTTPException` | 86 |
| external_call | `delete_calendar` | `HTTPException` | 91 |

## Behavior

This flow starts at `delete_calendar` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
